def get_reward(
    old_fill,
    new_fill,
    old_flood,
    new_flood,
    old_age,
    new_age,
    action
):
    reward = 0

    
    # MAC FILL
    HIGH_FILL = 0.8
    CRITICAL_FILL = 0.95

    # FLOOD_P
    HIGH_FLOOD = 0.05

    # AGE

    # stale age threshold conditions :
    stale_age_threshold = 0.15

    # fresh age threshold conditions :
    fresh_age_threshold = 0.01

    fill_gain = old_fill - new_fill
    flood_gain = old_flood - new_flood
    age_gain = old_age - new_age


# ------- 
    if action == "LEARN_MAC":

        # penalty
        if old_fill > CRITICAL_FILL:
            reward -= 5
        if old_flood > HIGH_FLOOD:
            reward -= 5

        
            
#----------------
    if action == "EVICT_ENTRY":

        # reward
        if old_age > stale_age_threshold:
            if old_fill > CRITICAL_FILL:
                reward += 7
            elif old_fill > HIGH_FILL:
                reward += 5

        # penalty
        elif old_fill < 0.5:
            reward -= 10
        elif old_age < fresh_age_threshold:
            reward -= 5

# ------------
    if action == "INCREASE_AGING":

        # reward
        if old_flood > HIGH_FLOOD:
            if old_fill > HIGH_FILL:
                reward += 7
            else:
                reward += 5

        # penalty (separate ifs)
        if old_flood == 0 and old_fill < 0.5:
            reward -= 5
        if old_age < fresh_age_threshold:
            reward -= 3

# -----------
    if action == "DECREASE_AGING":

        # reward
        if old_fill < HIGH_FILL and old_flood == 0:
            if old_age > stale_age_threshold:
                reward += 7
            else:
                reward += 5

        # penalty (separate ifs)
        if old_fill > CRITICAL_FILL:
            reward -= 7
        if old_flood > HIGH_FLOOD:
            reward -= 5



    reward += (
        20 * flood_gain +
        5 * fill_gain +   
        2 * age_gain
    )

    # situation : for logging
    if new_fill >= 0.95:
        situation = "CRITICAL"
    elif new_fill >= 0.80:
        situation = "PREVENTIVE"
    else:
        situation = "NORMAL"

    # outcome : for logging
    if new_fill < old_fill and new_flood < old_flood:
        outcome = "improved"
    elif new_fill > old_fill or new_flood > old_flood:
        outcome = "degraded"
    else:
        outcome = "neutral"

    return reward, outcome, situation

