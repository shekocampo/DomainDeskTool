from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

import dns.resolver

from config import RESOLVERS


@dataclass
class DnsResult:
    ns_results: dict[str, list[str] | str] = field(default_factory=dict)
    a_results: dict[str, list[str] | str] = field(default_factory=dict)
    ns_consistency: str = "not_found"
    a_consistency: str = "not_found"


def _normalize_ns(value: str) -> str:
    return value.lower().rstrip(".")


def _query_resolver(resolver_name: str, resolver_ip: str, domain: str) -> tuple[str, list[str] | str, list[str] | str]:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]
    resolver.timeout = 10
    resolver.lifetime = 10

    ns_result: list[str] | str
    try:
        answers = resolver.resolve(domain, "NS")
        ns_result = sorted(_normalize_ns(str(r.target)) for r in answers)
    except dns.resolver.NXDOMAIN:
        ns_result = "NXDOMAIN"
    except dns.resolver.NoAnswer:
        ns_result = "NoAnswer"
    except dns.resolver.Timeout:
        ns_result = "Timeout"
    except Exception as exc:
        ns_result = f"Error: {exc}"

    a_result: list[str] | str
    try:
        answers = resolver.resolve(domain, "A")
        a_result = sorted(str(r) for r in answers)
    except dns.resolver.NXDOMAIN:
        a_result = "NXDOMAIN"
    except dns.resolver.NoAnswer:
        a_result = "NoAnswer"
    except dns.resolver.Timeout:
        a_result = "Timeout"
    except Exception as exc:
        a_result = f"Error: {exc}"

    return resolver_name, ns_result, a_result


def _assess_consistency(results: dict[str, list[str] | str]) -> str:
    values = list(results.values())
    if not values:
        return "not_found"

    success_sets = [v for v in values if isinstance(v, list)]
    if not success_sets:
        return "not_found"

    first = frozenset(success_sets[0])
    if all(frozenset(s) == first for s in success_sets[1:]):
        if len(success_sets) == len(values):
            return "consistent"
        return "inconsistent"
    return "inconsistent"


def check(domain: str) -> DnsResult:
    result = DnsResult()
    try:
        with ThreadPoolExecutor(max_workers=len(RESOLVERS)) as executor:
            futures = {
                executor.submit(_query_resolver, name, ip, domain): name
                for name, ip in RESOLVERS.items()
            }
            for future in as_completed(futures):
                try:
                    resolver_name, ns_result, a_result = future.result()
                    result.ns_results[resolver_name] = ns_result
                    result.a_results[resolver_name] = a_result
                except Exception as exc:
                    name = futures[future]
                    error_msg = f"Error: {exc}"
                    result.ns_results[name] = error_msg
                    result.a_results[name] = error_msg

        result.ns_consistency = _assess_consistency(result.ns_results)
        result.a_consistency = _assess_consistency(result.a_results)
    except Exception as exc:
        for name in RESOLVERS:
            error_msg = f"Error: {exc}"
            result.ns_results[name] = error_msg
            result.a_results[name] = error_msg
    return result
