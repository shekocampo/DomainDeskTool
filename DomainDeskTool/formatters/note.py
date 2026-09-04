from datetime import datetime

from config import (
    DNSCHECKER_A_URL,
    DNSCHECKER_NS_URL,
    GOOGLE_TOOLBOX_URL,
    ICANN_LOOKUP_URL,
    RESOLVERS,
    WHOIS_URL,
    WHATSMYDNS_A_URL,
    WHATSMYDNS_NS_URL,
)
from checkers.dns_check import DnsResult
from checkers.google_workspace import GoogleWorkspaceResult
from checkers.rdap import RdapResult
from utils.tld_classifier import TldInfo

AGENT_NOTES_SECTION = """6. AGENT NOTES
   ════════════════════════════════════════

   CUSTOMER VERIFICATION
   Status:         [ ] Verified   [ ] Not Verified
   Verified email: ___________________________________
   Zight link:     ___________________________________
                   (screenshot of verification status, if applicable)

   WAYFINDER
   Link:           ___________________________________
                   (Wayfinder > search domain > copy URL)

   GENERAL NOTES
   ─────────────────────────────────────────────────
   Steps taken:

   ·

   DNS records of note:

   ·

   Zight screenshots:

   ·

   Open / related tickets:

   ·

   ─────────────────────────────────────────────────"""


def _consistency_label(consistency: str) -> str:
    if consistency == "consistent":
        return "[CONSISTENT]"
    if consistency == "inconsistent":
        return "[INCONSISTENT — propagation may be in progress]"
    return "[NOT FOUND]"


def _format_resolver_results(
    results: dict[str, list[str] | str],
) -> list[str]:
    lines = []
    for name, ip in RESOLVERS.items():
        value = results.get(name, "No result")
        if isinstance(value, list):
            display = ", ".join(value) if value else "(empty)"
        else:
            display = value
        lines.append(f"   {name} ({ip}): {display}")
    return lines


def _gws_status_text(gws_result: GoogleWorkspaceResult) -> str:
    mapping = {
        "existing_account": "Existing Google account found — domain is in use",
        "no_account": "No Google account found",
        "takeover_in_progress": "⚠ TAKEOVER IN PROGRESS — review carefully",
    }
    text = mapping.get(gws_result.status, "Status unknown — check link in Section 5")
    if gws_result.status == "unknown" and gws_result.error:
        text += f"\n   Error: {gws_result.error}"
    return text


def assemble(
    domain: str,
    tld_info: TldInfo,
    rdap_result: RdapResult,
    dns_result: DnsResult,
    gws_result: GoogleWorkspaceResult,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []

    lines.append("DOMAIN RESEARCH NOTE")
    lines.append("═" * 40)
    lines.append(f"Domain:    {domain}")
    lines.append(f"Generated: {timestamp}")
    lines.append(f"TLD:       {tld_info.tld} ({tld_info.tld_type})")
    lines.append("")

    # Section 1 — Registrar Information
    lines.append("1. REGISTRAR INFORMATION")
    lines.append("   ════════════════════════════════════════")
    if rdap_result.rdap_available:
        lines.append(f"   Registrar:       {rdap_result.registrar or 'Unknown'}")
        status = ", ".join(rdap_result.status_codes) if rdap_result.status_codes else "None"
        lines.append(f"   Status codes:    {status}")
        lines.append(f"   Registered:      {rdap_result.registered_date or 'Unknown'}")
        lines.append(f"   Expiry:          {rdap_result.expiry_date or 'Unknown'}")
        lines.append("   Nameservers:")
        if rdap_result.nameservers:
            for ns in rdap_result.nameservers:
                lines.append(f"      {ns}")
        else:
            lines.append("      (none)")
    else:
        lines.append("   [RDAP UNAVAILABLE — check WhoIS link in Section 5]")
        if rdap_result.error:
            lines.append(f"   Error: {rdap_result.error}")
    lines.append("")

    # Section 2 — DNS: Nameservers
    lines.append("2. DNS: NAMESERVERS")
    lines.append("   ════════════════════════════════════════")
    lines.extend(_format_resolver_results(dns_result.ns_results))
    lines.append(f"   {_consistency_label(dns_result.ns_consistency)}")
    lines.append("")

    # Section 3 — DNS: A Records
    lines.append("3. DNS: A RECORDS")
    lines.append("   ════════════════════════════════════════")
    lines.extend(_format_resolver_results(dns_result.a_results))
    lines.append(f"   {_consistency_label(dns_result.a_consistency)}")
    lines.append("")

    # Section 4 — Google Workspace
    lines.append("4. GOOGLE WORKSPACE")
    lines.append("   ════════════════════════════════════════")
    lines.append(f"   {_gws_status_text(gws_result)}")
    lines.append("")

    # Section 5 — Reference Links
    lines.append("5. REFERENCE LINKS")
    lines.append("   ════════════════════════════════════════")
    lines.append(f"   ICANN Lookup:         {ICANN_LOOKUP_URL.format(domain=domain)}")
    lines.append(f"   WhoIS:                {WHOIS_URL.format(domain=domain)}")
    if tld_info.cctld_whois_url:
        lines.append(f"   ccTLD Registry WhoIS: {tld_info.cctld_whois_url}")
    lines.append(f"   NS Propagation:       {WHATSMYDNS_NS_URL.format(domain=domain)}")
    lines.append(f"   NS Propagation (alt): {DNSCHECKER_NS_URL.format(domain=domain)}")
    lines.append(f"   A Propagation:        {WHATSMYDNS_A_URL.format(domain=domain)}")
    lines.append(f"   A Propagation (alt):  {DNSCHECKER_A_URL.format(domain=domain)}")
    lines.append(
        f"   Google Workspace:     {GOOGLE_TOOLBOX_URL.format(domain=domain)}"
    )
    lines.append("")

    # Section 6 — Agent Notes
    lines.append(AGENT_NOTES_SECTION)

    return "\n".join(lines)
