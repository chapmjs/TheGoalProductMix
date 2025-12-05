"""
The Goal - Product Mix Optimization Exercise
Based on Theory of Constraints concepts from Eliyahu Goldratt's "The Goal"

Scenario:
You are Alex Rogo, plant manager at UniCo Manufacturing. Your plant produces three 
products (Model X, Model Y, and Model Z). Each product must go through four work 
centers: Machining, Heat Treatment, Assembly, and Quality Control.

The plant operates 160 hours per month. Your goal is to maximize throughput 
(contribution margin) while respecting the capacity constraints at each work center.

One of these work centers is likely a bottleneck - just like the NCX-10 and 
heat treatment ovens in the book!
"""

from pulp import *

def solve_product_mix():
    # =============================================================================
    # PROBLEM DATA
    # =============================================================================
    
    # Products and their contribution margins (selling price - materials cost)
    products = ['Model_X', 'Model_Y', 'Model_Z']
    contribution_margin = {
        'Model_X': 90,   # $ per unit
        'Model_Y': 100,  # $ per unit  
        'Model_Z': 70    # $ per unit
    }
    
    # Work centers and their available capacity (hours per month)
    work_centers = ['Machining', 'Heat_Treatment', 'Assembly', 'Quality_Control']
    capacity = {
        'Machining': 160,
        'Heat_Treatment': 140,  # This might be our bottleneck!
        'Assembly': 160,
        'Quality_Control': 160
    }
    
    # Processing time required at each work center (hours per unit)
    processing_time = {
        ('Model_X', 'Machining'): 2.0,
        ('Model_X', 'Heat_Treatment'): 3.0,
        ('Model_X', 'Assembly'): 1.5,
        ('Model_X', 'Quality_Control'): 0.5,
        
        ('Model_Y', 'Machining'): 1.5,
        ('Model_Y', 'Heat_Treatment'): 2.5,
        ('Model_Y', 'Assembly'): 2.0,
        ('Model_Y', 'Quality_Control'): 1.0,
        
        ('Model_Z', 'Machining'): 1.0,
        ('Model_Z', 'Heat_Treatment'): 2.0,
        ('Model_Z', 'Assembly'): 1.0,
        ('Model_Z', 'Quality_Control'): 0.5,
    }
    
    # Market demand constraints (maximum units we can sell per month)
    max_demand = {
        'Model_X': 50,
        'Model_Y': 60,
        'Model_Z': 80
    }
    
    # =============================================================================
    # BUILD THE OPTIMIZATION MODEL
    # =============================================================================
    
    # Create the optimization problem
    prob = LpProblem("UniCo_Product_Mix", LpMaximize)
    
    # Decision variables: how many units of each product to produce
    production = LpVariable.dicts("Production", products, lowBound=0, cat='Continuous')
    
    # Objective function: Maximize total contribution margin (throughput)
    prob += lpSum([contribution_margin[p] * production[p] for p in products]), "Total_Throughput"
    
    # Capacity constraints: Don't exceed available hours at each work center
    for wc in work_centers:
        prob += (
            lpSum([processing_time[(p, wc)] * production[p] for p in products]) <= capacity[wc],
            f"Capacity_{wc}"
        )
    
    # Demand constraints: Don't produce more than we can sell
    for p in products:
        prob += production[p] <= max_demand[p], f"Demand_{p}"
    
    # =============================================================================
    # SOLVE THE MODEL
    # =============================================================================
    
    # Solve using the default solver
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # =============================================================================
    # ANALYZE AND DISPLAY RESULTS
    # =============================================================================
    
    results = {
        'status': LpStatus[prob.status],
        'optimal_throughput': value(prob.objective),
        'production_plan': {},
        'work_center_utilization': {},
        'bottleneck_analysis': {},
        'shadow_prices': {}
    }
    
    # Production quantities
    for p in products:
        results['production_plan'][p] = production[p].varValue
    
    # Calculate utilization at each work center
    for wc in work_centers:
        hours_used = sum([processing_time[(p, wc)] * production[p].varValue for p in products])
        utilization_pct = (hours_used / capacity[wc]) * 100
        results['work_center_utilization'][wc] = {
            'hours_used': hours_used,
            'capacity': capacity[wc],
            'utilization_pct': utilization_pct,
            'slack_hours': capacity[wc] - hours_used
        }
    
    # Identify bottleneck(s) - work centers at or near 100% utilization
    for wc in work_centers:
        if results['work_center_utilization'][wc]['utilization_pct'] >= 99:
            results['bottleneck_analysis'][wc] = 'BOTTLENECK'
        elif results['work_center_utilization'][wc]['utilization_pct'] >= 90:
            results['bottleneck_analysis'][wc] = 'Near Capacity'
        else:
            results['bottleneck_analysis'][wc] = 'Has Slack'
    
    # Extract shadow prices (dual values) for capacity constraints
    for name, constraint in prob.constraints.items():
        if 'Capacity' in name:
            results['shadow_prices'][name] = constraint.pi
    
    return results, prob


def print_results(results):
    """Print formatted results"""
    print("\n" + "="*70)
    print("UNICO MANUFACTURING - OPTIMAL PRODUCTION PLAN")
    print("="*70)
    
    print(f"\nSolution Status: {results['status']}")
    print(f"Maximum Monthly Throughput: ${results['optimal_throughput']:,.2f}")
    
    print("\n" + "-"*70)
    print("PRODUCTION PLAN")
    print("-"*70)
    for product, quantity in results['production_plan'].items():
        print(f"{product:12s}: {quantity:6.2f} units")
    
    print("\n" + "-"*70)
    print("WORK CENTER UTILIZATION")
    print("-"*70)
    print(f"{'Work Center':<20} {'Used':<10} {'Capacity':<10} {'Utilization':<12} {'Slack'}")
    print("-"*70)
    for wc, util in results['work_center_utilization'].items():
        status = results['bottleneck_analysis'].get(wc, '')
        marker = " ← BOTTLENECK!" if status == "BOTTLENECK" else ""
        print(f"{wc:<20} {util['hours_used']:>6.2f} hrs {util['capacity']:>6.0f} hrs "
              f"{util['utilization_pct']:>9.1f}%   {util['slack_hours']:>6.2f} hrs{marker}")
    
    print("\n" + "-"*70)
    print("SHADOW PRICES (Value of Additional Capacity)")
    print("-"*70)
    print("How much would throughput increase with one more hour of capacity?")
    for constraint, shadow_price in results['shadow_prices'].items():
        wc_name = constraint.replace('Capacity_', '')
        if shadow_price is not None and shadow_price > 0:
            print(f"{wc_name:<20}: ${shadow_price:.2f} per additional hour")
    
    print("\n" + "="*70)
    print("INSIGHTS FROM THE GOAL")
    print("="*70)
    print("""
Remember from The Goal:
1. Identify the bottleneck(s) - constraints that limit throughput
2. Exploit the bottleneck - use every minute productively
3. Subordinate everything else to the bottleneck decision
4. Elevate the bottleneck - increase its capacity if justified
5. Repeat - when you break one bottleneck, find the next one!

The shadow prices tell you how valuable additional capacity would be at each
work center. Focus improvement efforts where they create the most value!
    """)


if __name__ == "__main__":
    results, prob = solve_product_mix()
    print_results(results)
