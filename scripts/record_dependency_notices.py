"""Inventory installed package metadata and exact license/notice files; no inferred licenses."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/dependency_provenance.json")
    parser.add_argument("--notices", type=Path, default=ROOT / "docs/DEPENDENCY_NOTICES.txt")
    args = parser.parse_args()
    packages, blocks = [], []
    for dist in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower()):
        info = dist.metadata
        files = []
        for item in dist.files or []:
            name = Path(str(item)).name.lower()
            if not name.startswith(("license", "licence", "copying", "copyright", "notice")):
                continue
            path = Path(dist.locate_file(item))
            if not path.is_file():
                continue
            raw = path.read_bytes()
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            files.append({"installed_relative_path": str(item), "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
            blocks.append(f"\n===== {info['Name']} {dist.version} / {item} =====\n{content}\n")
        packages.append({"name": info["Name"], "version": dist.version,
                         "license_expression": info.get("License-Expression"),
                         "license_metadata": info.get("License"),
                         "license_classifiers": [s for s in info.get_all("Classifier", []) if s.startswith("License ::")],
                         "project_urls": info.get_all("Project-URL", []), "home_page": info.get("Home-page"),
                         "modification": "Unmodified installed dependency; no package code or wheels vendored.",
                         "notice_files": files,
                         "evidence_status": "RECORDED" if files else "NO_LOCAL_NOTICE_FILE"})
    args.notices.parent.mkdir(parents=True, exist_ok=True)
    args.notices.write_text("Installed dependency notices — exact text retained; separator headings added.\n"
                            "This inventory describes the invoking environment, not uninspected platform wheels.\n"
                            + "".join(blocks), encoding="utf-8", newline="\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
                                      "packages": packages, "notices_sha256": sha256(args.notices.read_bytes()).hexdigest()},
                                     ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"packages": len(packages), "notice_files": sum(len(p['notice_files']) for p in packages),
                      "without_notice_files": [p['name'] for p in packages if not p['notice_files']],
                      "notice_bytes": args.notices.stat().st_size}))


if __name__ == "__main__":
    main()
