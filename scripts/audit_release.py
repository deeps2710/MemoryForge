"""Read-only release checks: syntax, local document links, sensitive-file patterns and protected bytes."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "83a70f39c6772b7ac948830a39fc989b33a234d7"


def main():
    names = sorted(set(subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT
    ).decode().strip("\0").split("\0")))
    broken, secret_hits, syntax_errors, todo_hits, forbidden = [], [], [], [], []
    secret_patterns = {
        "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "api_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b"),
    }
    local_links = 0
    for name in names:
        path = ROOT / name
        if not path.is_file():
            continue
        if any(p in {"__pycache__", ".venv", ".local", ".pytest_cache"} for p in Path(name).parts) or path.name in {"secrets.toml", ".env"}:
            forbidden.append(name)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".py":
            try:
                ast.parse(content, filename=name)
            except SyntaxError as error:
                syntax_errors.append({"file": name, "line": error.lineno})
            for number, line in enumerate(content.splitlines(), 1):
                if re.search(r"\b(?:TODO|FIXME|HACK)\b", line) and name != "scripts/audit_release.py":
                    todo_hits.append({"file": name, "line": number})
        for rule, pattern in secret_patterns.items():
            for match in pattern.finditer(content):
                secret_hits.append({"file": name, "line": content[:match.start()].count("\n")+1, "rule": rule})
        if path.suffix == ".md" and name != "docs/DEVELOPMENT_BRIEF.md":
            for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", content):
                target = target.strip().strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                local_links += 1
                if not (path.parent / target).exists():
                    broken.append({"file": name, "target": target})
    protected_names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASELINE], cwd=ROOT).decode().splitlines()
    protected = {}
    for name in protected_names:
        if name.startswith(("artifacts/", "tests/", "src/")) and name != "src/ui.py" or name in {"assets/memoryforge-logo.png", "html"} or name.startswith("output/pdf/"):
            original = subprocess.check_output(["git", "show", f"{BASELINE}:{name}"], cwd=ROOT)
            current = (ROOT / name).read_bytes()
            # Source text may have a platform line ending; compare logical LF bytes.
            if Path(name).suffix in {".py", ".json"} or name == "html":
                original, current = original.replace(b"\r\n", b"\n"), current.replace(b"\r\n", b"\n")
            protected[name] = {"unchanged": original == current, "sha256": sha256(current).hexdigest()}
    result = {"status": "PASS" if not any([broken, secret_hits, syntax_errors, forbidden, todo_hits]) and all(v["unchanged"] for v in protected.values()) else "FAIL",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "baseline": BASELINE,
              "files_inspected": len(names), "local_markdown_links_checked": local_links,
              "broken_local_links": broken, "secret_pattern_hits": secret_hits,
              "syntax_errors": syntax_errors, "active_code_todos": todo_hits,
              "forbidden_tracked_or_unignored_paths": forbidden, "protected_files": protected,
              "limits": "Pattern scan is not proof of no possible secret; no external-link or vulnerability claim. Existing unrelated html is preserved, not used. Historical reports remain historical."}
    (ROOT / "artifacts/phase4_cleanup.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "protected_files"}, indent=2))
    print(f"Protected prior files unchanged: {sum(v['unchanged'] for v in protected.values())}/{len(protected)}")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
