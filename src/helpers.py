import re


def rgx_extract_match(regex: str, text: str) -> str | None:
    match = re.match(regex, text)
    if match:
        return match.group()
    return None
