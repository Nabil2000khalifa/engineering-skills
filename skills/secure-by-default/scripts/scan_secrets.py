#!/usr/bin/env python3
"""Lightweight secret and risky-pattern scanner. Not a replacement for gitleaks/trufflehog.

Usage: python scan_secrets.py [dir]
Exit code 1 if findings exist.
"""
import re, sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".next", "target"}
MAX_BYTES = 1_000_000

SECRETS = {
    "AWS access key": r"AKIA[0-9A-Z]{16}",
    "Private key block": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----",
    "GitHub token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "Slack token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    "Stripe live key": r"sk_live_[0-9a-zA-Z]{20,}",
    "Google API key": r"AIza[0-9A-Za-z_\-]{35}",
    "Generic secret assignment": r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]",
}
RISKY = {
    "eval/exec call": r"\b(?:eval|exec)\s*\(",
    "shell=True": r"shell\s*=\s*True",
    "TLS verification disabled": r"verify\s*=\s*False|rejectUnauthorized\s*:\s*false|InsecureSkipVerify\s*:\s*true",
    "Unsafe deserialization": r"pickle\.loads?\(|yaml\.load\((?![^)]*Loader)",
    "Weak hash for security": r"\b(?:md5|sha1)\s*\(",
    "SQL built with string formatting": r"(?i)(?:select|insert|update|delete)\b[^\n]*(?:\"\s*\+\s*\w+|%s|\{[^}]+\}|\bf['\"])",
    "innerHTML assignment": r"\.innerHTML\s*=",
    "Math.random near secret/token": r"(?i)(?:token|secret|password|session)[^\n]*Math\.random",
}
PLACEHOLDER = re.compile(r"(?i)example|changeme|your[_-]|xxx|placeholder|dummy|<.*>|\$\{|process\.env|os\.environ")
SELF = Path(__file__).resolve()


def scan(root: Path):
    findings = []
    for p in root.rglob("*"):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts) or p.resolve() == SELF:
            continue
        if p.stat().st_size > MAX_BYTES or p.name.endswith((".lock", ".min.js", ".png", ".jpg", ".pdf", ".zip")):
            continue
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for label, pat in SECRETS.items():
                if re.search(pat, line) and not PLACEHOLDER.search(line):
                    findings.append(("SECRET", label, p, i))
            for label, pat in RISKY.items():
                if re.search(pat, line):
                    findings.append(("RISK", label, p, i))
    return findings


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    res = scan(root)
    for kind, label, path, line in sorted(res, key=lambda r: (r[0] != "SECRET", str(r[2]), r[3])):
        print(f"[{kind}] {label}: {path}:{line}")
    print(f"\n{len(res)} finding(s). Review each; RISK items may be false positives.")
    sys.exit(1 if res else 0)
