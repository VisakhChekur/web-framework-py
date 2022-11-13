from dataclasses import dataclass
from pprint import pprint
from typing import Tuple
from urllib.parse import urlparse, parse_qs, unquote


@dataclass
class ParsedURL:

    controller_path: str
    path: str
    queries: dict[str, list[str]] | None


def parse_url(url: str) -> ParsedURL:

    unquoted_url = unquote(url)
    parsed_url = urlparse(unquoted_url)
    queries = parse_qs(parsed_url.query)
    controller, path = _parse_path(parsed_url.path)
    return ParsedURL(controller, path, queries)


def _parse_path(path: str) -> Tuple[str, str]:

    if path.startswith("/"):
        path = path[1:]

    path_components = path.split("/", 1)
    # Only controller name present
    if len(path_components) == 1:
        return path_components[0], ""
    return path_components[0], path_components[1]


if __name__ == "__main__":

    url = "/controller_name/other-path-related-stuff/blah/blah/blah"
    parsed_url = parse_url(url)
    print()
    pprint(parsed_url.__dict__)
    print()
