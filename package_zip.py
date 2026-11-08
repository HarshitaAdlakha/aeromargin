"""Builds the submission ZIP: code and small supporting files only (no videos, no keys, no node_modules).
    python package_zip.py        -> dist/aeromargin.zip
Checks: size < 50 MB, no .env, no video/audio, no file containing an API-key pattern."""
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist" / "aeromargin.zip"
SKIP_DIRS = {".git", "node_modules", "__pycache__", "dist", "build", ".venv", "scratch"}
SKIP_EXT = {".mp4", ".mp3", ".webm", ".mov", ".wav", ".pptx", ".pyc"}
SKIP_FILES = {".env"}
KEY = re.compile(r"(sk-(proj-)?[A-Za-z0-9_-]{20,}|nvapi-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,}|AQ\.[A-Za-z0-9_-]{30,})")


def files():
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if p.is_dir() or any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.name in SKIP_FILES or p.suffix.lower() in SKIP_EXT:
            continue
        yield p, rel


def main():
    OUT.parent.mkdir(exist_ok=True)
    n = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p, rel in files():
            if p.suffix.lower() in {".py", ".md", ".json", ".html", ".txt", ".mjs", ".js", ".log", ".example", ".gitignore", ""}:
                text = p.read_text(encoding="utf-8", errors="ignore")
                if KEY.search(text):
                    raise SystemExit(f"refusing to package: key-like string in {rel}")
            z.write(p, Path("aeromargin") / rel)
            n += 1
    mb = OUT.stat().st_size / 1e6
    assert mb < 50, f"ZIP is {mb:.1f} MB (limit 50 MB)"
    print(f"wrote {OUT} ({n} files, {mb:.2f} MB); no .env, no media, no key-like strings")


if __name__ == "__main__":
    main()
