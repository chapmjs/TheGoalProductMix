"""
Example Scenarios - Instructor Guide
Use this to generate answer keys or test different scenarios
"""

from the_goal_optimization import create_goal_optimization_model, format_results
import pandas as pd

def run_scenario(name, **kwargs):
    """Run a scenario with custom parameters and display results."""
    print("\n" + "="*80)
    print(f"SCENARIO: {name}")
    print("="*80)
    print(f"Parameters: {kwargs}")
    print()
    
    results, model = create_goal_optimization_model(**kwargs)
    print(format_results(results))
    
    # Return key metrics for comparison
    return {
        "scenario": name,
        "product_a": results["product_a"],
        "product_b": results["product_b"],
        "throughput": results["total_throughput"],
        "bottleneck": results["bottleneck"],
        "ht_utilization": results["heat_treatment_utilization"]
    }

# Collect results for comparison
all_results = []

# Scenario 1: Baseline (Default Parameters)
all_results.append(run_scenario(
    "Baseline - Default Parameters",
    # Uses all defaults
))

# Scenario 2: Increase Bottleneck Capacity by 25%
all_results.append(run_scenario(
    "Increase Bottleneck by 25%",
    heat_treatment_capacity=200  # Up from 160
))

# Scenario 3: Increase Bottleneck Capacity by 50%
all_results.append(run_scenario(
    "Increase Bottleneck by 50%",
    heat_treatment_capacity=240  # Up from 160
))

# Scenario 4: Increase Non-Bottleneck (Machining) by 50%
all_results.append(run_scenario(
    "Increase Non-Bottleneck (Machining) by 50%",
    machining_capacity=300  # Up from 200
))

# Scenario 5: Equal Profit Margins
all_results.append(run_scenario(
    "Equal Profit Margins ($75 each)",
    profit_a=75,
    profit_b=75
))

# Scenario 6: Product A Much More Profitable
all_results.append(run_scenario(
    "Product A Premium Priced ($140)",
    profit_a=140  # Up from $90
))

# Scenario 7: High Demand Scenario
all_results.append(run_scenario(
    "High Demand for Both Products",
    demand_a=100,
    demand_b=150
))

# Scenario 8: Balanced Capacities (No Clear Bottleneck)
all_results.append(run_scenario(
    "Balanced Capacities",
    heat_treatment_capacity=180,
    machining_capacity=180,
    assembly_capacity=180
))

# Scenario 9: Assembly Becomes Bottleneck
all_results.append(run_scenario(
    "Assembly as Bottleneck",
    heat_treatment_capacity=200,
    machining_capacity=200,
    assembly_capacity=140
))

# Scenario 10: Demand-Constrained
all_results.append(run_scenario(
    "Low Demand Scenario",
    demand_a=20,
    demand_b=30
))

# Create comparison table
print("\n" + "="*80)
print("SCENARIO COMPARISON SUMMARY")
print("="*80)

df = pd.DataFrame(all_results)
print(df.to_string(index=False))

# Additional Analysis
print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

# Compare baseline to increased bottleneck capacity
baseline_throughput = all_results[0]["throughput"]
increased_bottleneck_throughput = all_results[1]["throughput"]
throughput_increase = increased_bottleneck_throughput - baseline_throughput
capacity_increase = 40  # From 160 to 200 hours

print(f"\n1. VALUE OF BOTTLENECK CAPACITY:")
print(f"   - Baseline throughput: ${baseline_throughput:,.2f}")
print(f"   - After 40-hour increase: ${increased_bottleneck_throughput:,.2f}")
print(f"   - Increase: ${throughput_increase:,.2f}")
print(f"   - Value per hour: ${throughput_increase/capacity_increase:.2f}/hour")

# Compare to non-bottleneck increase
nonbottleneck_throughput = all_results[3]["throughput"]
nonbottleneck_increase = nonbottleneck_throughput - baseline_throughput

print(f"\n2. VALUE OF NON-BOTTLENECK CAPACITY:")
print(f"   - After 100-hour Machining increase: ${nonbottleneck_throughput:,.2f}")
print(f"   - Change from baseline: ${nonbottleneck_increase:,.2f}")
print(f"   - Lesson: Increasing non-bottleneck capacity has NO EFFECT!")

# Product mix changes
print(f"\n3. PRODUCT MIX DYNAMICS:")
print(f"   - Baseline: {all_results[0]['product_a']:.1f}A, {all_results[0]['product_b']:.1f}B")
print(f"   - Equal profits: {all_results[4]['product_a']:.1f}A, {all_results[4]['product_b']:.1f}B")
print(f"   - Product A premium: {all_results[5]['product_a']:.1f}A, {all_results[5]['product_b']:.1f}B")
print(f"   - Lesson: Mix depends on profit per bottleneck hour, not just profit per unit!")

# Bottleneck shifts
print(f"\n4. BOTTLENECK IDENTIFICATION:")
for result in all_results:
    print(f"   - {result['scenario']}: {result['bottleneck']}")
print(f"   - Lesson: Bottleneck can shift when constraints change!")

# Create a visual summary
print("\n" + "="*80)
print("THROUGHPUT COMPARISON (Bar Chart Data)")
print("="*80)
max_throughput = max(r["throughput"] for r in all_results)
for result in all_results:
    bar_length = int((result["throughput"] / max_throughput) * 50)
    bar = "█" * bar_length
    print(f"{result['scenario'][:30]:30s} {bar} ${result['throughput']:,.0f}")

print("\n" + "="*80)
print("ANSWER KEY HIGHLIGHTS")
print("="*80)
print("""
1. Why does the baseline produce only Product B?
   → Product B generates $30/bottleneck hour vs Product A's $22.50/bottleneck hour
   
2. What's the value of increasing Heat Treatment capacity by 1 hour?
   → Approximately $30/hour (the shadow price of the constraint)
   
3. Should we invest in more Machining capacity?
   → No! It has zero shadow price because it's not the bottleneck
   
4. At what profit level for Product A does the mix include both products?
   → When Product A profit exceeds $120 (when it becomes more efficient at the bottleneck)
   
5. If we increase Heat Treatment to 240 hours, what becomes the new bottleneck?
   → Check the scenario results above - likely Machining or Assembly
   
6. Why is non-bottleneck utilization less than 100%?
   → By design! They should support the bottleneck, not work at full capacity
   
7. How does this relate to Herbie on the hike?
   → Herbie determines the group's pace. Making others faster doesn't help the group.
""")

print("\n" + "="*80)
print("TEACHING TIPS")
print("="*80)
print("""
1. START SIMPLE: Begin with baseline scenario, then change one variable at a time

2. USE PREDICTIONS: Ask students to predict results before running scenarios

3. EMPHASIZE COUNTERINTUITIVE INSIGHTS:
   - Lower utilization can be good
   - Higher efficiency at one station doesn't help system
   - Product with lower profit margin might be better choice

4. CONNECT TO THE BOOK:
   - Herbie = Heat Treatment (the bottleneck)
   - Jonah's advice = Focus on the constraint
   - Five Focusing Steps = Systematic approach to improvement

5. COMMON STUDENT MISTAKES:
   - Thinking all resources should be 100% utilized
   - Choosing product based on profit margin alone
   - Believing local optimization helps system performance
""")

if __name__ == "__main__":
    print("\nScenario analysis complete! Use these results to create:")
    print("- Answer keys for student worksheets")
    print("- Examples for class presentations")
    print("- Test questions with specific scenarios")
    print("- Discussion points about counterintuitive results")
