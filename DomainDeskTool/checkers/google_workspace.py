from dataclasses import dataclass

from bs4 import BeautifulSoup

from config import GOOGLE_TOOLBOX_URL
from utils.http import safe_get


@dataclass
class GoogleWorkspaceResult:
    status: str = "unknown"
    error: str | None = None


def check(domain: str) -> GoogleWorkspaceResult:
    result = GoogleWorkspaceResult()
    try:
        response, error = safe_get(GOOGLE_TOOLBOX_URL.format(domain=domain))
        if error:
            result.error = error
            return result
        if response is None or response.status_code != 200:
            result.error = (
                f"HTTP {response.status_code}" if response else "No response"
            )
            return result

        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        if not body:
            result.error = "No body content found"
            return result

        text = body.get_text().lower()

        if "being taken over" in text or "takeover" in text:
            result.status = "takeover_in_progress"
        elif (
            "not currently" in text
            or "no account" in text
            or "not associated" in text
        ):
            result.status = "no_account"
        elif "existing" in text or "associated with" in text:
            result.status = "existing_account"
        else:
            result.error = "Could not determine status from page content"
    except Exception as exc:
        result.error = str(exc)
    return result
