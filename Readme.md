# The Goal - Product Mix Optimization Exercise

An interactive optimization exercise based on Eliyahu Goldratt's *The Goal* that teaches Theory of Constraints concepts through hands-on linear programming.

## Learning Objectives

After completing this exercise, students will be able to:

1. Formulate a product mix optimization problem using PuLP
2. Identify bottleneck resources in a production system
3. Interpret shadow prices and understand their managerial implications
4. Apply Theory of Constraints principles to maximize throughput
5. Use interactive visualization to explore "what-if" scenarios

## Background: The Goal

In *The Goal*, Alex Rogo discovers that his plant's performance is limited by bottleneck resources. The five focusing steps of Theory of Constraints are:

1. **IDENTIFY** the constraint (bottleneck)
2. **EXPLOIT** the constraint (maximize its productivity)
3. **SUBORDINATE** everything else to the constraint
4. **ELEVATE** the constraint (increase its capacity)
5. **REPEAT** - find the next constraint

This exercise lets you experience these concepts through optimization.

## Files

- `the_goal_optimization.py` - Standalone Python script with PuLP model
- `app.py` - Interactive Shiny Express application
- `requirements.txt` - Required Python packages

## Installation

### Option 1: Using pip

```bash
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
conda create -n thegoal python=3.11
conda activate thegoal
pip install -r requirements.txt
```

## Usage

### Running the Standalone Model

To see the optimization results in the terminal:

```bash
python the_goal_optimization.py
```

This will output:
- Optimal production quantities for each product
- Work center utilization rates
- Bottleneck identification
- Shadow prices for additional capacity

### Running the Interactive Shiny App

To launch the interactive web application:

```bash
shiny run app.py
```

Then open your browser to the URL shown (typically `http://localhost:8000`)

The app allows you to:
- Modify contribution margins for each product
- Adjust capacity at each work center
- Change market demand constraints
- See real-time optimization results
- Visualize bottleneck analysis
- Explore shadow prices

## The Scenario

You are Alex Rogo, plant manager at UniCo Manufacturing. Your plant produces three products:

**Products:**
- Model X: $90 contribution margin per unit
- Model Y: $100 contribution margin per unit  
- Model Z: $70 contribution margin per unit

**Work Centers:**
- Machining: 160 hours/month capacity
- Heat Treatment: 140 hours/month capacity (bottleneck!)
- Assembly: 160 hours/month capacity
- Quality Control: 160 hours/month capacity

**Market Demand:**
- Model X: 50 units/month maximum
- Model Y: 60 units/month maximum
- Model Z: 80 units/month maximum

## Exercise Questions

### Part 1: Basic Analysis

1. Run the optimization with default parameters. What is the optimal production mix?
2. Which work center is the bottleneck? How do you know?
3. What is the maximum monthly throughput you can achieve?
4. Are any products at their demand limit? What does this mean?

### Part 2: Shadow Price Analysis

5. What is the shadow price of the bottleneck resource?
6. If you could add 10 hours of capacity to any work center, which should you choose and why?
7. How much would total throughput increase with those 10 additional hours?

### Part 3: Theory of Constraints Application

8. **Identify:** Which resource is your constraint? Run the model to confirm.

9. **Exploit:** The shadow price tells you the value of one more hour. What operational changes could you make to "squeeze" more productivity from the bottleneck without adding capacity?

10. **Subordinate:** Why is it important to keep non-bottleneck resources from overproducing? What problems does this cause?

11. **Elevate:** Increase the bottleneck capacity by 20 hours. What happens to:
    - Total throughput?
    - The bottleneck location (does it shift)?
    - Shadow prices?

12. **Repeat:** After elevating the first constraint, what becomes the new bottleneck?

### Part 4: What-If Scenarios

Use the Shiny app to explore these scenarios:

13. **Demand Surge:** Double the demand for Model Y. What happens to the production mix and throughput?

14. **Product Mix Decision:** Model X has the highest contribution margin. Should you focus exclusively on Model X? Why or why not?

15. **Capacity Investment:** You have $10,000 to invest in additional capacity. If one hour of capacity costs:
    - Machining: $50/hour
    - Heat Treatment: $100/hour
    - Assembly: $40/hour
    - QC: $30/hour
    
    Where should you invest to maximize ROI?

16. **Price Change:** A competitor drops their price. To remain competitive, you must reduce Model Z's contribution margin to $50. How does this affect your optimal mix?

## Advanced Extensions

For students who finish early or want deeper challenges:

1. **Multi-Period Model:** Extend the model to plan production across multiple months with inventory holding costs

2. **Setup Times:** Add changeover times between products that consume capacity but don't add value

3. **Quality Issues:** Model Y has a 10% defect rate at QC. How does this affect the optimal mix?

4. **Batch Sizing:** Add minimum and maximum batch size constraints (e.g., Model X must be made in batches of 10)

5. **Make-or-Buy Decision:** What if you could outsource some production? Add binary variables to model this decision

## Key Takeaways

- **Throughput matters most:** Focus on maximizing contribution margin, not minimizing costs
- **Bottlenecks limit everything:** An hour lost at the bottleneck is an hour lost for the entire system
- **Shadow prices guide decisions:** They quantify the value of relaxing constraints
- **Local optimization ≠ Global optimization:** Keeping every resource busy doesn't maximize throughput
- **Constraints shift:** Breaking one bottleneck reveals the next one

## Theory of Constraints Vocabulary

- **Throughput (T):** Rate at which the system generates money through sales
- **Inventory (I):** Money invested in things the system intends to sell
- **Operating Expense (OE):** Money spent to convert inventory into throughput
- **Constraint:** Anything that limits the system from achieving higher throughput
- **Bottleneck:** A resource whose capacity is less than or equal to demand
- **Non-bottleneck:** A resource whose capacity exceeds demand
- **Drum-Buffer-Rope:** Scheduling system that synchronizes the plant to the bottleneck

## References

- Goldratt, E. M., & Cox, J. (2004). *The Goal: A Process of Ongoing Improvement*. North River Press.
- Winston, W. L., & Goldberg, J. B. (2004). *Operations Research: Applications and Algorithms*. Brooks/Cole.

## Deployment Options

### Deploy to Posit Connect Cloud

```bash
rsconnect deploy shiny . --name your-app-name --title "The Goal Optimizer"
```

### Deploy to shinyapps.io

```bash
rsconnect deploy shiny . --name your-app-name --title "The Goal Optimizer"
```

### Run locally for class demo

```bash
shiny run app.py --reload
```

## Tips for Students

1. **Start with defaults:** Run the base case first to understand the baseline
2. **Change one thing at a time:** This helps you understand cause and effect
3. **Use the visualizations:** The charts make patterns easier to see
4. **Think like Alex Rogo:** What would you do if this were your plant?
5. **Question the shadow prices:** Do they make intuitive sense given the production requirements?

## Support

For questions about this exercise, contact your instructor or refer to:
- PuLP documentation: https://coin-or.github.io/pulp/
- Shiny for Python: https://shiny.posit.co/py/

---

*"Tell me how you measure me, and I will tell you how I will behave."* - Eliyahu M. Goldratt
