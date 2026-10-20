#!/usr/bin/env python3
"""Compare declared dependencies with the latest registry versions.

Supports: package.json (npm), requirements.txt and pyproject.toml (PyPI).
Usage: python check_deps.py [project_dir]
Needs network access. Standard library only.
"""
import json, re, sys, urllib.request, urllib.error
from pathlib import Path

TIMEOUT = 10


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return json.load(r)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def clean(v):
    m = re.search(r"\d+(\.\d+)*", v or "")
    return m.group(0) if m else v


def major(v):
    try:
        return int(clean(v).split(".")[0])
    except (ValueError, AttributeError):
        return None


def npm_deps(root):
    p = root / "package.json"
    if not p.exists():
        return
    data = json.loads(p.read_text())
    for sect in ("dependencies", "devDependencies"):
        for name, ver in data.get(sect, {}).items():
            yield "npm", name, ver


def pypi_deps(root):
    pat = r"([A-Za-z0-9_.\-]+)\s*(?:[=<>~!]+\s*([\w.\-]+))?"
    req = root / "requirements.txt"
    if req.exists():
        for line in req.read_text().splitlines():
            line = line.split("#")[0].strip()
            if not line or line.startswith("-"):
                continue
            m = re.match(pat, line)
            if m:
                yield "pypi", m.group(1), m.group(2) or ""
    pp = root / "pyproject.toml"
    if pp.exists():
        m = re.search(r"dependencies\s*=\s*\[(.*?)\]", pp.read_text(), re.S)
        if m:
            for item in re.findall(r"[\"']([^\"']+)[\"']", m.group(1)):
                mm = re.match(pat, item)
                if mm:
                    yield "pypi", mm.group(1), mm.group(2) or ""


def latest(eco, name):
    if eco == "npm":
        d = fetch(f"https://registry.npmjs.org/{name.replace('/', '%2F')}/latest")
        if d:
            return d.get("version"), d.get("deprecated")
    else:
        d = fetch(f"https://pypi.org/pypi/{name}/json")
        if d:
            yanked = "yanked" if any(f.get("yanked") for f in d.get("urls", [])) else None
            return d["info"]["version"], yanked
    return None, None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    deps = list(npm_deps(root)) + list(pypi_deps(root))
    if not deps:
        print("No package.json / requirements.txt / pyproject.toml found.")
        return 0
    print(f"{'ECO':5} {'PACKAGE':32} {'DECLARED':14} {'LATEST':12} STATUS")
    flagged = 0
    for eco, name, ver in deps:
        lat, warn = latest(eco, name)
        if lat is None:
            status = "? registry lookup failed"
        elif warn:
            status = f"DEPRECATED/YANKED: {warn}"; flagged += 1
        elif not ver:
            status = "unpinned"
        elif major(ver) is not None and major(lat) is not None and major(lat) > major(ver):
            status = f"MAJOR behind ({major(ver)} -> {major(lat)}): read migration guide"; flagged += 1
        elif clean(ver) != lat:
            status = "minor/patch behind"
        else:
            status = "ok"
        print(f"{eco:5} {name[:32]:32} {ver[:14]:14} {(lat or '-')[:12]:12} {status}")
    print(f"\n{flagged} package(s) need attention.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
