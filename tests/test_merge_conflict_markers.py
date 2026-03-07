from pathlib import Path

TARGET_FILES = (
    "api/showdog_api.py",
    "static/pricing.html",
)
CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def test_target_files_have_no_merge_conflict_markers():
    repo_root = Path(__file__).resolve().parents[1]

    for relative_path in TARGET_FILES:
        lines = (repo_root / relative_path).read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()
            marker = next((m for m in CONFLICT_MARKERS if stripped.startswith(m)), None)
            assert marker is None, f"{relative_path}:{line_number} contains merge conflict marker: {marker}"
