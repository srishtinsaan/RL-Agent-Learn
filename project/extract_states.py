import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# INPUT FILES
# -------------------------

LIVE_STEP_LOG = os.path.join(
    BASE_DIR,
    "results",
    "logs",
    "live_step_log.csv"
)

WITHOUT_RL_STATS = os.path.join(
    BASE_DIR,
    "results",
    "network_stats",
    "without_rl_stats.csv"
)

# -------------------------
# OUTPUT DIRECTORY
# -------------------------

FINAL_DIR = os.path.join(BASE_DIR, "final")
os.makedirs(FINAL_DIR, exist_ok=True)

WITH_RL_OUT = os.path.join(
    FINAL_DIR,
    "with_rl.csv"
)

WITHOUT_RL_OUT = os.path.join(
    FINAL_DIR,
    "without_rl.csv"
)

TARGET_ROWS = 6000


# -------------------------
# WITH RL
# -------------------------

def create_with_rl_csv():

    if not os.path.exists(LIVE_STEP_LOG):
        raise FileNotFoundError(
            f"File not found:\n{LIVE_STEP_LOG}"
        )

    df = pd.read_csv(LIVE_STEP_LOG)

    required_cols = [
        "mac_fill",
        "flood_pressure",
        "avg_age"
    ]

    missing = [
        col for col in required_cols
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns in live_step_log.csv: {missing}"
        )

    df = df[required_cols]

    if len(df) < TARGET_ROWS:
        raise ValueError(
            f"with_rl source has only {len(df)} rows "
            f"(expected at least {TARGET_ROWS})"
        )

    df = df.head(TARGET_ROWS)

    df.to_csv(
        WITH_RL_OUT,
        index=False
    )

    print(
        f"[OK] Created {WITH_RL_OUT}"
        f" ({len(df)} rows)"
    )


# -------------------------
# WITHOUT RL
# -------------------------

def create_without_rl_csv():

    if not os.path.exists(WITHOUT_RL_STATS):
        raise FileNotFoundError(
            f"File not found:\n{WITHOUT_RL_STATS}"
        )

    df = pd.read_csv(WITHOUT_RL_STATS)

    required_cols = [
        "mac_fill",
        "flood_pressure",
        "avg_age"
    ]

    missing = [
        col for col in required_cols
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns in without_rl_stats.csv: {missing}"
        )

    df = df[required_cols]

    # Normalize MAC fill
    # Anything above 1 becomes 1
    df["mac_fill"] = df["mac_fill"].clip(
        lower=0.0,
        upper=1.0
    )

    if len(df) < TARGET_ROWS:
        raise ValueError(
            f"without_rl source has only {len(df)} rows "
            f"(expected at least {TARGET_ROWS})"
        )

    df = df.head(TARGET_ROWS)

    df.to_csv(
        WITHOUT_RL_OUT,
        index=False
    )

    print(
        f"[OK] Created {WITHOUT_RL_OUT}"
        f" ({len(df)} rows)"
    )


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":

    print("\nCreating comparison CSV files...\n")

    create_with_rl_csv()
    # create_without_rl_csv()

    print("\nDone!")