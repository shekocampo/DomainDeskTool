RESOLVERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "Quad9": "9.9.9.9",
}

RDAP_URL = "https://rdap.org/domain/{domain}"

ICANN_LOOKUP_URL = "https://lookup.icann.org/lookup?name={domain}"
WHOIS_URL = "https://www.whois.com/whois/{domain}"
WHATSMYDNS_NS_URL = "https://www.whatsmydns.net/#NS/{domain}"
WHATSMYDNS_A_URL = "https://www.whatsmydns.net/#A/{domain}"
DNSCHECKER_NS_URL = "https://dnschecker.org/#NS/{domain}"
DNSCHECKER_A_URL = "https://dnschecker.org/#A/{domain}"
GOOGLE_TOOLBOX_URL = (
    "https://toolbox.googleapps.com/apps/recovery/domain_in_use?domain={domain}"
)

SQUARESPACE_TLDS = {
    ".com", ".net", ".org", ".biz", ".info", ".app", ".dev", ".io", ".co", ".ai",
    ".blog", ".shop", ".store", ".online", ".site", ".website", ".design", ".studio",
    ".gallery", ".photography", ".photo", ".video", ".art", ".music", ".band", ".media",
    ".news", ".press", ".pub", ".agency", ".consulting", ".marketing", ".services",
    ".solutions", ".tech", ".digital", ".software", ".systems", ".email", ".domains",
    ".host", ".hosting", ".cloud", ".land", ".properties", ".estate", ".realty",
    ".house", ".homes", ".apartments", ".construction", ".contractors", ".legal", ".law",
    ".attorney", ".lawyer", ".accountant", ".tax", ".finance", ".money", ".investments",
    ".fund", ".capital", ".ventures", ".clinic", ".dental", ".doctor", ".health",
    ".healthcare", ".fitness", ".yoga", ".gym", ".salon", ".spa", ".bar", ".cafe",
    ".catering", ".pizza", ".restaurant", ".menu", ".food", ".recipes", ".cooking",
    ".wine", ".beer", ".coffee", ".boutique", ".clothing", ".fashion", ".shoes",
    ".jewelry", ".accessories", ".education", ".school", ".academy", ".college",
    ".training", ".coach", ".dog", ".vet", ".farm", ".garden", ".flowers", ".gifts",
    ".toys", ".games", ".game", ".poker", ".casino", ".bet", ".travel", ".flights",
    ".hotel", ".vacation", ".rentals", ".tours", ".events", ".wedding", ".church",
    ".charity", ".foundation", ".ngo", ".social", ".community", ".club", ".family",
    ".singles", ".dating", ".adult", ".xxx", ".sex", ".porn",
}

SQUARESPACE_CCTLDS = {
    ".ca", ".co.uk", ".org.uk", ".uk", ".de", ".fr", ".it", ".nl", ".eu", ".au",
    ".com.au", ".co.au", ".nz", ".co.nz", ".mx", ".com.mx", ".jp", ".in", ".co.in",
    ".kr", ".co.kr", ".us", ".me", ".cc", ".pw", ".pl",
}

CCTLD_WHOIS_URLS = {
    ".ca": "https://www.cira.ca/en/domain-names/whois/",
    ".de": "https://www.denic.de/en/whois/",
    ".fr": "https://www.afnic.fr/en/domain-names-and-support/everything-there-is-to-know-about-domain-names/find-a-domain-name-or-a-holder-using-whois/",
    ".it": "https://web-whois.nic.it/",
    ".nl": "https://www.sidn.nl/en/whois",
    ".eu": "https://whois.eurid.eu/en/",
    ".au": "https://whois.auda.org.au/",
    ".com.au": "https://whois.auda.org.au/",
    ".nz": "https://www.dnc.org.nz/whois/",
    ".co.nz": "https://www.dnc.org.nz/whois/",
    ".jp": "https://whois.jprs.jp/en/",
    ".pl": "https://www.dns.pl/en/whois",
    ".us": "https://www.whois.us/",
    ".me": "https://www.nic.me/whois.do",
    ".co.uk": "https://www.nominet.uk/whois/",
    ".org.uk": "https://www.nominet.uk/whois/",
    ".uk": "https://www.nominet.uk/whois/",
}
