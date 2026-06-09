import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PIPELINE_STEPS = [
    "make_dataset.py",
    "data_quality_report.py",
    "business_threshold_analysis.py",
    "score_orders.py",
    "precision_policy_experiments.py",
    "make_report_plots.py",
]

TRAINING_STEPS = [
    "cv_tune_lightgbm.py",
]


def main() -> None:
    steps = PIPELINE_STEPS.copy()
    if "--retrain" in sys.argv:
        steps = ["make_dataset.py", *TRAINING_STEPS, *PIPELINE_STEPS[1:]]

    env = {**os.environ, "LOKY_MAX_CPU_COUNT": os.environ.get("LOKY_MAX_CPU_COUNT", "4")}
    for script_name in steps:
        script_path = ROOT / "src" / script_name
        print(f"\nRunning {script_name}...")
        subprocess.run([sys.executable, str(script_path)], cwd=ROOT, env=env, check=True)

    print("\nFull industry-ready artifact pipeline completed.")
    print("Use --retrain to rerun cross-validated model tuning.")


if __name__ == "__main__":
    main()
