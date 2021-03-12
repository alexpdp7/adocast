#!/usr/bin/env python3
import json
import sys
from xml.etree import ElementTree


def walk_adoc_ast(ast, f):
    if not isinstance(ast, dict):
        return
    yield from f(ast)
    for block in ast['blocks']:
        yield from walk_adoc_ast(block, f)


def extract_links(node):
    if not "content" in node:
        return
    content = f"<fake xmlns:xl='xl'>{node['content']}</fake>"
    et = ElementTree.fromstring(content)
    for link in et.findall(".//link"):
        yield (link, node)


def link_json(parts):
    link, node = parts
    return {
        "link": link.attrib["{xl}href"],
        "source_location": node['source_location'],
    }


def main():
    d = json.load(sys.stdin)
    json.dump(list(map(link_json, walk_adoc_ast(d, extract_links))), sys.stdout)


if __name__ == "__main__":
    main()
