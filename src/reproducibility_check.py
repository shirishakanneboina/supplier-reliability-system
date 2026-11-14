
import hashlib
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "raw"


def get_file_hashes():
    """Calculate SHA-256 hashes for all generated CSV files."""

    hashes = {}

    for file_path in sorted(DATA_DIR.glob("*.csv")):
        file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        hashes[file_path.name] = file_hash

    return hashes


def run_generator():
    """Run the complete data generation pipeline."""

    result = subprocess.run(
        [sys.executable, "src/main.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("\nDATA GENERATION FAILED!")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)

    if "SUPPLIER RELIABILITY SYSTEM COMPLETED!" not in result.stdout:
        print("\nCould not confirm successful data generation.")
        print(result.stdout)
        raise SystemExit(1)

    print("Data generation completed successfully.")


def main():
    print("=" * 55)
    print("SUPPLIER DATA REPRODUCIBILITY TEST")
    print("=" * 55)

    print("\nRUN 1: Generating datasets...")
    run_generator()
    first_hashes = get_file_hashes()

    print("\nRUN 2: Generating datasets again...")
    run_generator()
    second_hashes = get_file_hashes()

    print("\nCOMPARING DATASET CHECKSUMS")
    print("-" * 55)

    if first_hashes.keys() != second_hashes.keys():
        print("FAILED: Dataset file names are different.")
        raise SystemExit(1)

    all_match = True

    for filename in first_hashes:
        matches = first_hashes[filename] == second_hashes[filename]

        print(f"{filename}: {'MATCH' if matches else 'DIFFERENT'}")

        if not matches:
            all_match = False

    print("\n" + "=" * 55)

    if all_match:
        print("REPRODUCIBILITY TEST PASSED!")
        print("All CSV datasets are identical across both runs.")
    else:
        print("REPRODUCIBILITY TEST FAILED!")
        print("Some datasets changed between runs.")

    print("=" * 55)


if __name__ == "__main__":
    main()
