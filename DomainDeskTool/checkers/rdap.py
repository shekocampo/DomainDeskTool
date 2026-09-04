from dataclasses import dataclass, field

from config import RDAP_URL
from utils.http import safe_get


@dataclass
class RdapResult:
    registrar: str | None = None
    status_codes: list[str] = field(default_factory=list)
    registered_date: str | None = None
    expiry_date: str | None = None
    nameservers: list[str] = field(default_factory=list)
    rdap_available: bool = False
    error: str | None = None


def _normalize_ns(ns: str) -> str:
    return ns.lower().rstrip(".")


def _extract_registrar(entities: list) -> str | None:
    for entity in entities:
        roles = entity.get("roles", [])
        if "registrar" not in roles:
            continue
        vcard = entity.get("vcardArray")
        if not vcard or len(vcard) < 2:
            continue
        for item in vcard[1]:
            if item[0] == "fn":
                return item[3]
    return None


def _extract_event_date(events: list, action: str) -> str | None:
    for event in events:
        if event.get("eventAction") == action:
            return event.get("eventDate")
    return None


def lookup(domain: str) -> RdapResult:
    result = RdapResult()
    try:
        response, error = safe_get(RDAP_URL.format(domain=domain))
        if error:
            result.error = error
            return result
        if response is None or response.status_code != 200:
            result.error = (
                f"HTTP {response.status_code}" if response else "No response"
            )
            return result

        data = response.json()
        result.rdap_available = True
        result.status_codes = data.get("status", [])
        result.registered_date = _extract_event_date(
            data.get("events", []), "registration"
        )
        result.expiry_date = _extract_event_date(
            data.get("events", []), "expiration"
        )
        result.registrar = _extract_registrar(data.get("entities", []))
        result.nameservers = sorted(
            _normalize_ns(ns["ldhName"])
            for ns in data.get("nameservers", [])
            if ns.get("ldhName")
        )
    except Exception as exc:
        result.rdap_available = False
        result.error = str(exc)
    return result
