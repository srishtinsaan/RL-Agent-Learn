import sys, os, csv
sys.path.append(os.path.dirname(__file__))
from project.rl.env import LiveEnv
from project.rl.states import LiveStateEncoder

def run_baseline(switch='g0_s0', episodes=200, steps_per_ep=30):
    env     = LiveEnv(switch=switch)
    encoder = LiveStateEncoder(bins=8)

    log_path         = 'project/results/eval/baseline_step_log.csv'
    episode_log_path = 'project/results/eval/baseline_episode_log.csv'
    os.makedirs('project/results/eval', exist_ok=True)

    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Episode', 'Step',
            'mac_fill', 'flood_pressure', 'avg_age',
            'Situation', 'Outcome'
        ])

    with open(episode_log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Episode', 'Avg_Fill', 'Avg_Flood', 'Avg_Age', 'Critical_Steps', 'Preventive_Steps', 'Normal_Steps'])

    for ep in range(episodes):
        state_info = env.get_live_state()

        ep_fill, ep_flood, ep_age = [], [], []
        critical, preventive, normal = 0, 0, 0

        for step in range(steps_per_ep):
            # fixed action: REBALANCE (no learning)
            next_state_info, reward, info = env.step(3)

            fill  = info['mac_fill']
            flood = info['flood_pressure']
            age   = info['avg_age']

            ep_fill.append(fill)
            ep_flood.append(flood)
            ep_age.append(age)

            sit = info['situation']
            if sit == 'CRITICAL':    critical += 1
            elif sit == 'PREVENTIVE': preventive += 1
            else:                     normal += 1

            with open(log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    ep+1, step+1,
                    fill, flood, age,
                    sit, info['outcome']
                ])

            state_info = next_state_info

        with open(episode_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                ep+1,
                round(sum(ep_fill)  / len(ep_fill),  4),
                round(sum(ep_flood) / len(ep_flood),  4),
                round(sum(ep_age)   / len(ep_age),    4),
                critical, preventive, normal
            ])

        print(f"Baseline Ep {ep+1} | avg_fill: {sum(ep_fill)/len(ep_fill):.3f} | avg_flood: {sum(ep_flood)/len(ep_flood):.3f}")

if __name__ == '__main__':
    run_baseline()