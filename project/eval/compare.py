import csv
from collections import defaultdict

def load_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

def avg(rows, key):
    return sum(float(r[key]) for r in rows) / len(rows)

def aggregate_rl(step_log_path):
    rows = load_csv(step_log_path)

    episodes = defaultdict(list)
    for row in rows:
        episodes[row['Episode']].append(row)

    aggregated = []
    for ep, steps in episodes.items():
        critical   = sum(1 for s in steps if s['Situation'] == 'CRITICAL')
        preventive = sum(1 for s in steps if s['Situation'] == 'PREVENTIVE')
        normal     = sum(1 for s in steps if s['Situation'] == 'NORMAL')

        aggregated.append({
            'Episode':          ep,
            'Avg_Fill':         avg(steps, 'mac_fill'),
            'Avg_Flood':        avg(steps, 'flood_pressure'),
            'Avg_Age':          avg(steps, 'avg_age'),
            'Critical_Steps':   critical,
            'Preventive_Steps': preventive,
            'Normal_Steps':     normal
        })

    return aggregated

def aggregate_baseline(episode_log_path):
    return load_csv(episode_log_path)

def compare():
    rl_step_log      = 'project/results/logs/live_step_log.csv'
    baseline_ep_log  = 'project/results/eval/baseline_episode_log.csv'

    rl   = aggregate_rl(rl_step_log)
    base = aggregate_baseline(baseline_ep_log)

    rl_avg_fill      = avg(rl,   'Avg_Fill')
    rl_avg_flood     = avg(rl,   'Avg_Flood')
    rl_avg_age       = avg(rl,   'Avg_Age')
    rl_critical      = sum(int(r['Critical_Steps'])   for r in rl)
    rl_preventive    = sum(int(r['Preventive_Steps']) for r in rl)
    rl_normal        = sum(int(r['Normal_Steps'])     for r in rl)

    base_avg_fill    = avg(base,  'Avg_Fill')
    base_avg_flood   = avg(base,  'Avg_Flood')
    base_avg_age     = avg(base,  'Avg_Age')
    base_critical    = sum(int(r['Critical_Steps'])   for r in base)
    base_preventive  = sum(int(r['Preventive_Steps']) for r in base)
    base_normal      = sum(int(r['Normal_Steps'])     for r in base)

    print("=" * 55)
    print(f"{'Metric':<28} {'Baseline':>10} {'RL Agent':>10}")
    print("=" * 55)
    print(f"{'Avg MAC Fill':<28} {base_avg_fill:>10.4f} {rl_avg_fill:>10.4f}")
    print(f"{'Avg Flood Pressure':<28} {base_avg_flood:>10.4f} {rl_avg_flood:>10.4f}")
    print(f"{'Avg Age':<28} {base_avg_age:>10.4f} {rl_avg_age:>10.4f}")
    print(f"{'Total Critical Steps':<28} {base_critical:>10} {rl_critical:>10}")
    print(f"{'Total Preventive Steps':<28} {base_preventive:>10} {rl_preventive:>10}")
    print(f"{'Total Normal Steps':<28} {base_normal:>10} {rl_normal:>10}")
    print("=" * 55)

if __name__ == '__main__':
    compare()