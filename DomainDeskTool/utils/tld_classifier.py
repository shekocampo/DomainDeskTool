from dataclasses import dataclass

from config import (
    CCTLD_WHOIS_URLS,
    SQUARESPACE_CCTLDS,
    SQUARESPACE_TLDS,
    WHOIS_URL,
)

_KNOWN_MULTI_LABEL_TLDS = sorted(
    {tld for tld in SQUARESPACE_CCTLDS | set(CCTLD_WHOIS_URLS) if tld.count(".") >= 2},
    key=len,
    reverse=True,
)


@dataclass
class TldInfo:
    tld: str
    tld_type: str
    is_squarespace_tld: bool
    whois_url: str
    cctld_whois_url: str | None


def _extract_tld(domain: str) -> str:
    labels = domain.lower().split(".")
    if len(labels) < 2:
        return f".{labels[-1]}" if labels else ""

    for multi in _KNOWN_MULTI_LABEL_TLDS:
        suffix = multi.lstrip(".")
        suffix_labels = suffix.split(".")
        if len(labels) >= len(suffix_labels) + 1:
            candidate = "." + ".".join(labels[-len(suffix_labels) :])
            if candidate == multi:
                return multi

    return f".{labels[-1]}"


def classify(domain: str) -> TldInfo:
    tld = _extract_tld(domain)
    is_standard = tld in SQUARESPACE_TLDS
    is_cctld = tld in SQUARESPACE_CCTLDS

    if is_standard:
        tld_type = "standard"
    elif is_cctld:
        tld_type = "cctld"
    else:
        tld_type = "unknown"

    cctld_whois_url = CCTLD_WHOIS_URLS.get(tld)
    if cctld_whois_url:
        whois_url = cctld_whois_url
    else:
        whois_url = WHOIS_URL.format(domain=domain)

    return TldInfo(
        tld=tld,
        tld_type=tld_type,
        is_squarespace_tld=is_standard or is_cctld,
        whois_url=whois_url,
        cctld_whois_url=cctld_whois_url,
    )
