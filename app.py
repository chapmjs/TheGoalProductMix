"""
Shiny Express App: The Goal - Production Optimization
Interactive optimization model based on Eliyahu Goldratt's Theory of Constraints
"""

from shiny.express import input, render, ui
from shinywidgets import render_plotly
import plotly.graph_objects as go
import plotly.express as px
from the_goal_optimization import create_goal_optimization_model
import pandas as pd

# Page configuration
ui.page_opts(
    title="The Goal - Production Optimization",
    fillable=False
)

# Header
with ui.div(style="background-color: #1e3a8a; color: white; padding: 20px; margin-bottom: 20px; border-radius: 8px;"):
    ui.h2("The Goal: Production Scheduling Optimization", style="margin: 0;")
    ui.p("Based on Eliyahu Goldratt's Theory of Constraints", style="margin: 5px 0 0 0; font-style: italic;")

# Layout with sidebar and main content
with ui.layout_sidebar():
    # Sidebar with inputs
    with ui.sidebar(width=350, style="background-color: #f8fafc;"):
        ui.h4("📊 Model Parameters")
        
        ui.markdown("---")
        ui.h5("🏭 Work Center Capacities (hours/week)")
        
        ui.input_slider(
            "machining_capacity",
            "Machining Center:",
            min=100, max=300, value=200, step=10
        )
        
        ui.input_slider(
            "heat_treatment_capacity",
            "Heat Treatment (Bottleneck):",
            min=80, max=240, value=160, step=10
        )
        
        ui.input_slider(
            "assembly_capacity",
            "Assembly Center:",
            min=100, max=300, value=180, step=10
        )
        
        ui.markdown("---")
        ui.h5("📦 Product Parameters")
        
        ui.input_slider(
            "demand_a",
            "Max Demand - Product A:",
            min=0, max=100, value=50, step=5
        )
        
        ui.input_slider(
            "demand_b",
            "Max Demand - Product B:",
            min=0, max=150, value=80, step=5
        )
        
        ui.input_slider(
            "profit_a",
            "Profit per unit - Product A ($):",
            min=50, max=150, value=90, step=5
        )
        
        ui.input_slider(
            "profit_b",
            "Profit per unit - Product B ($):",
            min=30, max=100, value=60, step=5
        )
        
        ui.markdown("---")
        ui.markdown("""
        **Theory of Constraints Concepts:**
        - Bottleneck determines system throughput
        - Non-bottlenecks should support the bottleneck
        - Focus improvement efforts on the constraint
        """)
    
    # Main content area
    with ui.layout_columns(col_widths=[12, 12]):
        # Results card
        with ui.card():
            ui.card_header("🎯 Optimal Production Plan")
            
            @render.ui
            def results_summary():
                results, _ = create_goal_optimization_model(
                    heat_treatment_capacity=input.heat_treatment_capacity(),
                    machining_capacity=input.machining_capacity(),
                    assembly_capacity=input.assembly_capacity(),
                    demand_a=input.demand_a(),
                    demand_b=input.demand_b(),
                    profit_a=input.profit_a(),
                    profit_b=input.profit_b()
                )
                
                return ui.HTML(f"""
                <div style="padding: 10px;">
                    <div style="background-color: #dbeafe; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                        <h4 style="margin-top: 0; color: #1e40af;">Maximum Throughput: ${results['total_throughput']:,.2f}</h4>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #16a34a;">
                            <h5 style="margin-top: 0; color: #15803d;">Product A</h5>
                            <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{results['product_a']:.2f} units</p>
                            <p style="color: #666; margin: 0;">Contribution: ${results['product_a'] * input.profit_a():,.2f}</p>
                        </div>
                        
                        <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                            <h5 style="margin-top: 0; color: #d97706;">Product B</h5>
                            <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{results['product_b']:.2f} units</p>
                            <p style="color: #666; margin: 0;">Contribution: ${results['product_b'] * input.profit_b():,.2f}</p>
                        </div>
                    </div>
                    
                    <div style="background-color: #fee2e2; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #dc2626;">
                        <h5 style="margin-top: 0; color: #991b1b;">🔍 System Bottleneck</h5>
                        <p style="font-size: 18px; font-weight: bold; margin: 0;">{results['bottleneck']}</p>
                        <p style="color: #666; margin: 5px 0 0 0; font-style: italic;">
                            "An hour lost at the bottleneck is an hour lost for the entire system" - The Goal
                        </p>
                    </div>
                </div>
                """)
        
        # Capacity utilization visualization
        with ui.card():
            ui.card_header("📈 Work Center Utilization")
            
            @render_plotly
            def capacity_chart():
                results, _ = create_goal_optimization_model(
                    heat_treatment_capacity=input.heat_treatment_capacity(),
                    machining_capacity=input.machining_capacity(),
                    assembly_capacity=input.assembly_capacity(),
                    demand_a=input.demand_a(),
                    demand_b=input.demand_b(),
                    profit_a=input.profit_a(),
                    profit_b=input.profit_b()
                )
                
                work_centers = ['Machining', 'Heat Treatment', 'Assembly']
                used = [
                    results['machining_used'],
                    results['heat_treatment_used'],
                    results['assembly_used']
                ]
                capacity = [
                    results['machining_capacity'],
                    results['heat_treatment_capacity'],
                    results['assembly_capacity']
                ]
                utilization = [
                    results['machining_utilization'],
                    results['heat_treatment_utilization'],
                    results['assembly_utilization']
                ]
                
                # Determine colors based on utilization
                colors = ['#10b981' if u < 95 else '#ef4444' for u in utilization]
                
                fig = go.Figure()
                
                # Add capacity bars
                fig.add_trace(go.Bar(
                    name='Available Capacity',
                    x=work_centers,
                    y=capacity,
                    marker_color='#e5e7eb',
                    text=[f'{c:.0f}h' for c in capacity],
                    textposition='outside'
                ))
                
                # Add used capacity bars
                fig.add_trace(go.Bar(
                    name='Used Capacity',
                    x=work_centers,
                    y=used,
                    marker_color=colors,
                    text=[f'{u:.1f}h<br>({p:.1f}%)' for u, p in zip(used, utilization)],
                    textposition='inside'
                ))
                
                fig.update_layout(
                    barmode='overlay',
                    title='Capacity Utilization by Work Center',
                    yaxis_title='Hours',
                    showlegend=True,
                    height=400,
                    hovermode='x unified'
                )
                
                return fig
    
    # Bottom section - Constraint analysis
    with ui.layout_columns(col_widths=[12]):
        with ui.card():
            ui.card_header("🔬 Constraint Sensitivity Analysis")
            
            @render.data_frame
            def constraint_table():
                results, _ = create_goal_optimization_model(
                    heat_treatment_capacity=input.heat_treatment_capacity(),
                    machining_capacity=input.machining_capacity(),
                    assembly_capacity=input.assembly_capacity(),
                    demand_a=input.demand_a(),
                    demand_b=input.demand_b(),
                    profit_a=input.profit_a(),
                    profit_b=input.profit_b()
                )
                
                df = results['constraints_df'].copy()
                df['Shadow_Price'] = df['Shadow_Price'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
                df['Slack'] = df['Slack'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
                
                # Clean up constraint names for display
                df['Constraint'] = df['Constraint'].str.replace('_', ' ').str.title()
                
                return df
            
            ui.markdown("""
            **Shadow Price Interpretation:**
            - Shows the value of one additional unit of the constraint
            - For capacity constraints: value of one more hour
            - Helps identify where investments would be most valuable
            
            **Slack:**
            - Amount of unused capacity in each constraint
            - Zero slack = binding constraint (bottleneck)
            """)
    
    # Educational content
    with ui.layout_columns(col_widths=[6, 6]):
        with ui.card():
            ui.card_header("📚 Key Concepts from The Goal")
            ui.markdown("""
            **Goldratt's Five Focusing Steps:**
            
            1. **IDENTIFY** the system's constraint(s)
            2. **EXPLOIT** the constraint(s)
            3. **SUBORDINATE** everything else to the above decision
            4. **ELEVATE** the system's constraint(s)
            5. **Repeat** - Don't let inertia become the constraint
            
            **Core Metrics:**
            - **Throughput**: Rate of generating money through sales
            - **Inventory**: Money invested in things to sell
            - **Operating Expense**: Money spent to convert inventory into throughput
            
            **Key Insight**: Local optimums ≠ Global optimum. Optimizing non-bottlenecks doesn't improve system throughput!
            """)
        
        with ui.card():
            ui.card_header("🎓 Discussion Questions for Teams")
            ui.markdown("""
            1. **What happens to throughput if you increase the bottleneck capacity by 20%?**
               - Try adjusting the Heat Treatment capacity slider
            
            2. **Should we increase capacity at non-bottleneck work centers?**
               - Consider the relationship between utilization and throughput
            
            3. **What's the value of one additional hour at each work center?**
               - Look at the shadow prices in the constraint analysis
            
            4. **How does product mix affect total throughput?**
               - Experiment with different profit margins
            
            5. **What if demand constraints are binding instead of capacity?**
               - Try increasing demand limits - what changes?
            
            6. **How does this relate to the Herbie hiking analogy from the book?**
               - Consider how the bottleneck determines the pace
            """)
