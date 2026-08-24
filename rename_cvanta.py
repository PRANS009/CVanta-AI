from pathlib import Path
import shutil

files = [
    Path("templates/index.html"),
    Path("templates/resume_builder.html"),
    Path("templates/result.html"),
    Path("README.md"),
]

replacements = {
    "AI Resume Analyzer": "CVanta AI",
    "AI Resume Builder": "CVanta AI Resume Builder",
    "Resume Analyzer": "CVanta AI",
    "← Back to Analyzer": "← Back to CVanta AI",
    "<title>AI Resume Builder</title>": "<title>CVanta AI | Resume Builder</title>",
    "<title>AI Resume Analyzer</title>": "<title>CVanta AI | Resume & Career Intelligence</title>",
}

for file_path in files:

    if not file_path.exists():
        print(f"Skipped: {file_path}")
        continue

    backup = file_path.with_suffix(file_path.suffix + ".bak")

    if not backup.exists():
        shutil.copy2(file_path, backup)

    text = file_path.read_text(encoding="utf-8")

    for old, new in replacements.items():
        text = text.replace(old, new)

    file_path.write_text(text, encoding="utf-8")

    print(f"Updated: {file_path}")

print("\n✅ Branding changed to CVanta AI")
print("Tagline: One Resume. Every Career.")
