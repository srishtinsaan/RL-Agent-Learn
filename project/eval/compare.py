import os
import pandas as pd
import matplotlib.pyplot as plt

RL_FILE = "project/final/with_rl.csv"
BASE_FILE = "project/final/without_rl.csv"

OUTPUT_DIR = "project/results/eval"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================
# LOAD DATA
# ==========================

rl = pd.read_csv(RL_FILE)
base = pd.read_csv(BASE_FILE)

# Keep same number of rows
rows = min(len(rl), len(base))

rl = rl.head(rows)
base = base.head(rows)

print(f"\nComparing {rows} rows\n")


# ==========================
# BASIC METRICS
# ==========================

rl_fill = rl["mac_fill"].mean()
base_fill = base["mac_fill"].mean()

rl_flood = rl["flood_pressure"].mean()
base_flood = base["flood_pressure"].mean()

rl_age = rl["avg_age"].mean()
base_age = base["avg_age"].mean()


# ==========================
# STATES
# ==========================

def count_states(df):

    critical = (df["mac_fill"] >= 0.95).sum()

    preventive = (
        (df["mac_fill"] >= 0.80)
        & (df["mac_fill"] < 0.95)
    ).sum()

    normal = (df["mac_fill"] < 0.80).sum()

    return critical, preventive, normal


base_critical, base_preventive, base_normal = count_states(base)

rl_critical, rl_preventive, rl_normal = count_states(rl)


# ==========================
# IMPROVEMENTS
# ==========================

def pct_improvement(old, new):

    if old == 0:
        return 0

    return ((old - new) / old) * 100


flood_reduction = pct_improvement(
    base_flood,
    rl_flood
)

critical_reduction = pct_improvement(
    base_critical,
    rl_critical
)

normal_increase = (
    ((rl_normal - base_normal) / base_normal) * 100
    if base_normal > 0
    else 0
)

fill_efficiency = (
    ((abs(base_fill - 1.0) - abs(rl_fill - 1.0))
     / abs(base_fill - 1.0))
    * 100
    if abs(base_fill - 1.0) > 0
    else 0
)

base_stability = (
    (1 - base_flood) * 50
    + (1 - min(base_fill, 1)) * 25
    + (1 - base_age) * 25
)

rl_stability = (
    (1 - rl_flood) * 50
    + (1 - min(rl_fill, 1)) * 25
    + (1 - rl_age) * 25
)

stability_gain = (
    ((rl_stability - base_stability)
     / base_stability)
    * 100
    if base_stability != 0
    else 0
)


# ==========================
# PRINT REPORT
# ==========================

print("=" * 65)
print("          RL NETWORK EVALUATION REPORT")
print("=" * 65)

print(f"{'Metric':30s} {'Baseline':>12s} {'RL':>12s}")
print("-" * 65)

print(f"{'Average MAC Fill':30s} {base_fill:12.4f} {rl_fill:12.4f}")
print(f"{'Average Flood Pressure':30s} {base_flood:12.4f} {rl_flood:12.4f}")
print(f"{'Average Age':30s} {base_age:12.4f} {rl_age:12.4f}")

print("-" * 65)

print(f"{'Critical States':30s} {base_critical:12d} {rl_critical:12d}")
print(f"{'Preventive States':30s} {base_preventive:12d} {rl_preventive:12d}")
print(f"{'Normal States':30s} {base_normal:12d} {rl_normal:12d}")

print("-" * 65)

print(f"Flood Reduction (%)            : {flood_reduction:.2f}%")
print(f"Critical Reduction (%)         : {critical_reduction:.2f}%")
print(f"Normal State Increase (%)      : {normal_increase:.2f}%")
print(f"Fill Efficiency Improvement (%) : {fill_efficiency:.2f}%")
print(f"Network Stability Gain (%)     : {stability_gain:.2f}%")

print("=" * 65)


# ==========================
# CHART 1
# AVG METRICS
# ==========================

metrics = [
    "MAC Fill",
    "Flood Pressure",
    "Average Age"
]

base_values = [
    base_fill,
    base_flood,
    base_age
]

rl_values = [
    rl_fill,
    rl_flood,
    rl_age
]

x = range(len(metrics))
width = 0.35

plt.figure(figsize=(8, 5))

plt.bar(
    [i - width/2 for i in x],
    base_values,
    width,
    label="Baseline"
)

plt.bar(
    [i + width/2 for i in x],
    rl_values,
    width,
    label="RL"
)

plt.xticks(x, metrics)
plt.ylabel("Value")
plt.title("Average Metrics Comparison")
plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "avg_metrics_comparison.png"
    )
)

plt.close()


# ==========================
# CHART 2
# STATE DISTRIBUTION
# ==========================

states = [
    "Critical",
    "Preventive",
    "Normal"
]

base_states = [
    base_critical,
    base_preventive,
    base_normal
]

rl_states = [
    rl_critical,
    rl_preventive,
    rl_normal
]

x = range(len(states))

plt.figure(figsize=(8, 5))

plt.bar(
    [i - width/2 for i in x],
    base_states,
    width,
    label="Baseline"
)

plt.bar(
    [i + width/2 for i in x],
    rl_states,
    width,
    label="RL"
)

plt.xticks(x, states)
plt.ylabel("Count")
plt.title("State Distribution")
plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "state_distribution.png"
    )
)

plt.close()


# ==========================
# CHART 3
# IMPROVEMENTS
# ==========================

improvement_labels = [
    "Flood\nReduction",
    "Critical\nReduction",
    "Normal\nIncrease",
    "Stability\nGain"
]

improvement_values = [
    flood_reduction,
    critical_reduction,
    normal_increase,
    stability_gain
]

plt.figure(figsize=(8, 5))

plt.bar(
    improvement_labels,
    improvement_values
)

plt.ylabel("Percentage (%)")
plt.title("RL Improvement over Baseline")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "improvement_summary.png"
    )
)

plt.close()


print("\nCharts saved in:")
print(OUTPUT_DIR)