import math

def calculate_full_match_stats(home_xg, away_xg, max_goals=10):
    """
    Calculates individual goal probabilities AND match outcome probabilities.
    """
    
    # Poisson formula: P(k) = (lambda^k * e^-lambda) / k!
    def poisson(k, lamb):
        return (math.pow(lamb, k) * math.exp(-lamb)) / math.factorial(k)

    # 1. Generate probabilities for 0 to max_goals for both teams
    home_probs = [poisson(i, home_xg) for i in range(max_goals + 1)]
    away_probs = [poisson(i, away_xg) for i in range(max_goals + 1)]

    # --- PART A: Print Individual Goal Probabilities Table ---
    print(f"\n--- Goal Probabilities Breakdown ---")
    print(f"Home xG: {home_xg} | Away xG: {away_xg}")
    print("-" * 35)
    print(f"{'Goals':<6} | {'Home %':<10} | {'Away %':<10}")
    print("-" * 35)
    
    for k in range(max_goals + 1):
        h_pct = home_probs[k] * 100
        a_pct = away_probs[k] * 100
        # Only print rows where at least one team has > 0.1% chance to keep it clean
        if h_pct > 0.01 or a_pct > 0.01:
             print(f"{k:<6} | {h_pct:<10.2f} | {a_pct:<10.2f}")

    # --- PART B: Calculate Win/Draw/Loss Probabilities ---
    prob_home_more = 0
    prob_same = 0
    prob_home_less = 0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            joint_prob = home_probs[h] * away_probs[a]
            
            if h > a:
                prob_home_more += joint_prob
            elif h == a:
                prob_same += joint_prob
            else: # h < a
                prob_home_less += joint_prob

    # --- PART C: Print Match Outcome ---
    print("\n--- Match Outcome Probabilities ---")
    print("-" * 35)
    print(f"{'Outcome':<20} | {'Probability':<10}")
    print("-" * 35)
    print(f"{'Home Win':<20} | {prob_home_more * 100:.2f}%")
    print(f"{'Draw':<20} | {prob_same * 100:.2f}%")
    print(f"{'Away Win':<20} | {prob_home_less * 100:.2f}%")
    print("-" * 35)

# Main Execution
if __name__ == "__main__":
    def get_valid_xg(prompt):
        """Prompt until a non-blank, non-negative numeric value is entered."""
        while True:
            s = input(prompt).strip()
            if s == "":
                print("Input cannot be blank. Please enter a numeric value.")
                continue
            try:
                val = float(s)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                continue
            if val < 0:
                print("Error: Expected goals cannot be negative.")
                continue
            return val

    # Get inputs, reprompting on blank/invalid values
    h_xg = get_valid_xg("Enter Expected Goals for HOME team: ")
    a_xg = get_valid_xg("Enter Expected Goals for AWAY team: ")

    calculate_full_match_stats(h_xg, a_xg)