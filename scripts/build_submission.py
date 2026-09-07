"""Build the portal's source/PDF ZIP with explicit inclusion rules and byte verification."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {"app.py", "README.md", "LICENSE", "requirements.txt", "requirements-lock.txt",
             "requirements-pdf.txt", ".gitignore", ".gitattributes"}
PREFIXES = ("src/", "tests/", "scripts/", "docs/", "assets/", "artifacts/", "output/pdf/")
REQUIRED = {"app.py", "README.md", "LICENSE", "artifacts/encoder.pt",
            "artifacts/phase3_evidence.json", "docs/DEMO_SCRIPT.md",
            "docs/SUBMISSION_READINESS_REPORT.md", "docs/SUBMISSION_INSTRUCTIONS_AUDIT.md",
            "docs/PDF_FONT_NOTICES.txt", "requirements.txt", "requirements-lock.txt",
            "output/pdf/MemoryForge_Concept_Summary.pdf", "output/pdf/MemoryForge_Blog.pdf"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output/submission/MemoryForge_Submission_DRAFT.zip")
    args = parser.parse_args()
    candidates = git("ls-files", "-z", "--cached", "--others", "--exclude-standard").decode("utf-8").split("\0")
    selected = sorted({name for name in candidates if name and
                       (name in TOP_FILES or name == ".streamlit/config.toml" or name.startswith(PREFIXES))})
    if missing := REQUIRED - set(selected):
        raise RuntimeError(f"Missing required deliverables: {sorted(missing)}")
    payload = {}
    for name in selected:
        path = ROOT / name
        resolved = path.resolve()
        if not resolved.is_relative_to(ROOT.resolve()) or path.is_symlink():
            raise ValueError(f"Unsafe package path: {name}")
        if any(part in {"__pycache__", ".git", ".venv", ".local"} for part in path.parts):
            raise ValueError(f"Unexpected cache in selected source: {name}")
        if path.name == "secrets.toml" or path.name.startswith(".env"):
            raise ValueError(f"Unexpected secret configuration in package: {name}")
        payload[name] = path.read_bytes()
    package_note = (
        "# MemoryForge — Pathway Track solution package\n\n"
        "Packaging status: DRAFT pending the manual actions in docs/SUBMISSION_READINESS_REPORT.md.\n"
        "This ZIP is not evidence that a competition entry has been submitted.\n\n"
        "Start with README.md for the project claim, current deployment status and install/run commands.\n"
        "Repository: https://github.com/deeps2710/MemoryForge\n"
        "Live application: use only a verified public URL recorded in README.md.\n\n"
        "Written deliverables:\n"
        "- output/pdf/MemoryForge_Concept_Summary.pdf — one page; the required concept briefing.\n"
        "- output/pdf/MemoryForge_Blog.pdf — four-page project blog; submission-format draft,\n"
        "  since the organizer and ZIP field do not define a separate blog format.\n"
        "- docs/PDF_FONT_NOTICES.txt — notices for fonts embedded in both PDFs.\n\n"
        "The real app, trained checkpoint, tests, numerical evidence and source/license records are included.\n"
        "No local environments, repository history, credentials, or unrelated original html are included.\n"
        "FILE_MANIFEST.json records source revision and SHA-256 for every other entry.\n"
    ).encode("utf-8")
    payload["START_HERE.md"] = package_note
    manifest = {"source_head": git("rev-parse", "HEAD").decode().strip(),
                "source_working_tree_dirty": bool(git("status", "--porcelain").strip()),
                "files": {name: {"bytes": len(data), "sha256": sha256(data).hexdigest()}
                          for name, data in sorted(payload.items())}}
    payload["FILE_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo("MemoryForge/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(args.output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("ZIP CRC verification failed")
        for name, data in payload.items():
            if archive.read("MemoryForge/" + name) != data:
                raise RuntimeError(f"Packaged bytes differ: {name}")
    result = {"status": "PASS", "files": len(payload), "bytes": args.output.stat().st_size,
              "sha256": sha256(args.output.read_bytes()).hexdigest(),
              "source_head": manifest["source_head"],
              "source_working_tree_dirty": manifest["source_working_tree_dirty"],
              "all_entries_verified_against_source": True,
              "submission_status": "NOT SUBMITTED; see readiness report"}
    args.output.with_suffix(".verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
