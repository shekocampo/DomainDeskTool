import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

from checkers import dns_check, google_workspace, rdap
from checkers.dns_check import DnsResult
from checkers.google_workspace import GoogleWorkspaceResult
from checkers.rdap import RdapResult
from config import RESOLVERS
from formatters import note
from utils import tld_classifier


def _validate_domain(raw: str) -> str:
    domain = raw.strip().lower()
    if not domain:
        raise ValueError("Domain cannot be empty.")
    if " " in domain:
        raise ValueError("Domain cannot contain spaces.")
    if "://" in domain:
        raise ValueError("Domain must not include a protocol (http:// or https://).")
    if "." not in domain:
        raise ValueError("Domain must contain at least one dot.")
    return domain


def _warn_subdomain(domain: str, tld_info: tld_classifier.TldInfo) -> None:
    tld_labels = tld_info.tld.lstrip(".").split(".")
    domain_labels = domain.split(".")
    non_tld_labels = len(domain_labels) - len(tld_labels)
    if non_tld_labels > 1:
        print(
            f"Warning: '{domain}' looks like a subdomain "
            f"(expected a naked domain like example{tld_info.tld}).",
            file=sys.stderr,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Research a domain and output a formatted internal note."
    )
    parser.add_argument("domain", help="Naked domain to research (e.g. example.com)")
    parser.add_argument(
        "--output",
        "-o",
        metavar="PATH",
        help="Write the note to a .txt file at this path",
    )
    args = parser.parse_args()

    try:
        domain = _validate_domain(args.domain)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        tld_info = tld_classifier.classify(domain)
    except Exception as exc:
        print(f"Error classifying TLD: {exc}", file=sys.stderr)
        sys.exit(1)

    _warn_subdomain(domain, tld_info)

    try:
        rdap_result = rdap.lookup(domain)
    except Exception as exc:
        rdap_result = RdapResult(rdap_available=False, error=str(exc))

    dns_result = DnsResult()
    gws_result = GoogleWorkspaceResult()

    with ThreadPoolExecutor(max_workers=2) as executor:
        dns_future = executor.submit(_safe_dns_check, domain)
        gws_future = executor.submit(_safe_gws_check, domain)
        dns_result = dns_future.result()
        gws_result = gws_future.result()

    note_text = note.assemble(domain, tld_info, rdap_result, dns_result, gws_result)
    print(note_text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(note_text)
        print(f"Note saved to {args.output}")


def _safe_dns_check(domain: str) -> DnsResult:
    try:
        return dns_check.check(domain)
    except Exception as exc:
        result = DnsResult()
        error_msg = f"Error: {exc}"
        for name in RESOLVERS:
            result.ns_results[name] = error_msg
            result.a_results[name] = error_msg
        return result


def _safe_gws_check(domain: str) -> GoogleWorkspaceResult:
    try:
        return google_workspace.check(domain)
    except Exception as exc:
        return GoogleWorkspaceResult(status="unknown", error=str(exc))


if __name__ == "__main__":
    main()
