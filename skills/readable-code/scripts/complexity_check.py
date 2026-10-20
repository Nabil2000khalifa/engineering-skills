#!/usr/bin/env python3
"""Flag overly long/complex code.

Python: per-function length, parameter count, nesting depth (AST based).
Other languages: file length heuristic only.
Usage: python complexity_check.py [dir] [--max-lines 40] [--max-params 5] [--max-depth 4]
"""
import argparse, ast, sys
from pathlib import Path

SKIP = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", "target", ".next"}
OTHER_EXT = {".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".rs", ".rb", ".php", ".cs", ".kt", ".swift"}
BRANCH = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith, ast.Match)


def depth(node, d=0):
    best = d
    for child in ast.iter_child_nodes(node):
        best = max(best, depth(child, d + 1 if isinstance(child, BRANCH) else d))
    return best


def check_py(path, a):
    out = []
    try:
        tree = ast.parse(path.read_text())
    except (SyntaxError, UnicodeDecodeError):
        return out
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = (n.end_lineno or n.lineno) - n.lineno + 1
            params = len(n.args.args) + len(n.args.kwonlyargs)
            dep = depth(n)
            issues = []
            if length > a.max_lines: issues.append(f"{length} lines")
            if params > a.max_params: issues.append(f"{params} params")
            if dep > a.max_depth: issues.append(f"nesting {dep}")
            if issues:
                out.append(f"{path}:{n.lineno} {n.name}(): " + ", ".join(issues))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", nargs="?", default=".")
    ap.add_argument("--max-lines", type=int, default=40)
    ap.add_argument("--max-params", type=int, default=5)
    ap.add_argument("--max-depth", type=int, default=4)
    ap.add_argument("--max-file", type=int, default=400)
    a = ap.parse_args()
    findings = []
    for p in Path(a.dir).rglob("*"):
        if not p.is_file() or any(x in SKIP for x in p.parts):
            continue
        if p.suffix == ".py":
            findings += check_py(p, a)
        if p.suffix == ".py" or p.suffix in OTHER_EXT:
            try:
                n = len(p.read_text(errors="ignore").splitlines())
            except OSError:
                continue
            if n > a.max_file:
                findings.append(f"{p}: file is {n} lines (consider splitting)")
    print("\n".join(findings) if findings else "No complexity issues found.")
    print(f"\n{len(findings)} finding(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
