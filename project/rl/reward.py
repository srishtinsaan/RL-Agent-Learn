def get_reward(
    action,
    old_fill,
    new_fill,
    old_flood,
    new_flood,
    old_age,
    new_age
):
    """
    Reward function for:
        0 = EVICT_ENTRY
        1 = INCREASE_AGING
        2 = DECREASE_AGING
        3 = LEARN_MAC (NO_OP)
    """

    TARGET_FILL = 0.60

    flood_gain = old_flood - new_flood

    fill_gain = (
        abs(old_fill - TARGET_FILL)
        - abs(new_fill - TARGET_FILL)
    )

    age_gain = old_age - new_age

    reward = (
        50 * flood_gain
        + 10 * fill_gain
        + 5 * age_gain
    )

    # Action costs
    action_cost = {
        0: 0.10,   # EVICT_ENTRY
        1: 0.05,   # INCREASE_AGING
        2: 0.05,   # DECREASE_AGING
        3: 0.01    # LEARN_MAC / NO_OP
    }

    reward -= action_cost[action]

    # ---------- Action-specific shaping ----------

    # LEARN_MAC / NO_OP
    if action == 3:
        if new_fill < 0.60:
            reward += 2
        elif new_fill >= 0.80:
            reward -= 20

    # EVICT_ENTRY
    elif action == 0:
        if old_age > 0.50:
            reward += 5

        if old_fill < 0.30:
            reward -= 10

    # INCREASE_AGING
    elif action == 1:
        if old_age > 0.60:
            reward += 3

    # DECREASE_AGING
    elif action == 2:
        if old_flood > 0.50:
            reward += 3

    # ---------- Situation labels ----------

    situation = "NORMAL"

    if new_fill >= 0.95:
        reward -= 15
        situation = "CRITICAL"

    elif new_fill >= 0.80:
        reward += 3
        situation = "PREVENTIVE"

    # ---------- Outcome labels ----------

    if reward > 0:
        outcome = "improved"
    elif reward < 0:
        outcome = "degraded"
    else:
        outcome = "neutral"

    return reward, outcome, situation