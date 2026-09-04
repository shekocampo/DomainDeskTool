import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({"User-Agent": "domain-research-tool/1.0"})

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

_DEFAULT_TIMEOUT = 10


def safe_get(url: str) -> tuple[requests.Response | None, str | None]:
    try:
        response = session.get(url, timeout=_DEFAULT_TIMEOUT)
        return response, None
    except requests.RequestException as exc:
        return None, str(exc)
