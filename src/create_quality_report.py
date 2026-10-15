from datetime import datetime
from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_FILE = REPORT_DIR / "portfolio_quality_report.txt"


def check_path(relative_path):
    path = PROJECT_DIR / relative_path
    return path.exists()


def run_command(command):
    try:
        result = subprocess.run(
            command,
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            check=False,
        )

        return result.returncode, result.stdout, result.stderr

    except OSError as error:
        return 1, "", str(error)


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("NIGERIAN E-COMMERCE SALES ANALYTICS")
    lines.append("PORTFOLIO QUALITY REPORT")
    lines.append("=" * 55)
    lines.append(
        "Generated: "
        + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    )
    lines.append("")

    required_paths = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "docs/data_dictionary.md",
        "data/ecommerce_sales.csv",
        "data/ecommerce_sales_clean.csv",
        "data/customers.csv",
        "src/run_pipeline.py",
        "tests/test_data_quality.py",
        "tests/test_financial_metrics.py",
    ]

    lines.append("1. REQUIRED FILES")
    lines.append("-" * 55)

    missing = []

    for relative_path in required_paths:
        exists = check_path(relative_path)

        status = "PASS" if exists else "FAIL"

        lines.append(f"[{status}] {relative_path}")

        if not exists:
            missing.append(relative_path)

    lines.append("")
    lines.append("2. AUTOMATED TESTS")
    lines.append("-" * 55)

    test_code, test_stdout, test_stderr = run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
        ]
    )

    if test_code == 0:
        lines.append("[PASS] Automated tests completed successfully.")
        lines.append(test_stdout.strip())
    else:
        lines.append("[FAIL] Automated tests reported an error.")

        if test_stdout.strip():
            lines.append(test_stdout.strip())

        if test_stderr.strip():
            lines.append(test_stderr.strip())

    lines.append("")
    lines.append("3. GIT REPOSITORY")
    lines.append("-" * 55)

    git_code, git_stdout, git_stderr = run_command(
        ["git", "rev-parse", "--show-toplevel"]
    )

    if git_code == 0:
        lines.append("[PASS] Git repository detected.")
        lines.append(f"Repository root: {git_stdout.strip()}")
    else:
        lines.append("[FAIL] Git repository not detected.")

        if git_stderr.strip():
            lines.append(git_stderr.strip())

    lines.append("")
    lines.append("4. DATA DISCLAIMER")
    lines.append("-" * 55)
    lines.append(
        "The dataset is synthetic and intended for educational "
        "and portfolio purposes."
    )
    lines.append(
        "Its results must not be presented as verified Nigerian "
        "e-commerce market statistics."
    )

    lines.append("")
    lines.append("5. OVERALL CHECK")
    lines.append("-" * 55)

    if not missing and test_code == 0 and git_code == 0:
        lines.append(
            "PASS: File, test, and Git checks completed successfully."
        )
    else:
        lines.append(
            "REVIEW REQUIRED: One or more checks did not pass."
        )

    lines.append("")
    lines.append(
        "This report checks selected project requirements. "
        "It does not certify analytical correctness, accounting accuracy, "
        "or real-world representativeness."
    )

    REPORT_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(lines))
    print(f"\nReport saved to: {REPORT_FILE}")

    if missing or test_code != 0 or git_code != 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())