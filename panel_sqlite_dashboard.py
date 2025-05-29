import pandas as pd
import sqlite3
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import pearsonr
import statsmodels.api as sm
from create_excel_with_sheet import create_excel_with_sheet  # From artifact_id: bb15d88c-e4e2-4ac7-bede-1a29c40a6707
from pathlib import Path

# Enable Panel extension
pn.extension('plotly')

# Load data from SQLite
def load_data(db_path="sales.db"):
    try:
        if not Path(db_path).exists():
            print(f"Error: Database '{db_path}' not found.")
            return None
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        conn.close()
        
        # Categorize day using match/case
        def categorize_day(day):
            try:
                match day.lower():
                    case "monday":
                        return "Work starts"
                    case "friday":
                        return "Work ends"
                    case "saturday" | "sunday":
                        return "Weekend"
                    case _:
                        return "Regular day"
            except AttributeError:
                return "Invalid"
        
        df["day_category"] = df["day"].apply(categorize_day)
        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Compute advanced statistics
def compute_statistics(df):
    try:
        # Descriptive statistics
        desc_stats = df[["age", "sales"]].describe().to_dict()
        
        # Pearson correlation
        corr, p_value = pearsonr(df["age"], df["sales"])
        
        # Linear regression
        X = sm.add_constant(df["age"])  # Add intercept
        model = sm.OLS(df["sales"], X).fit()
        regression_summary = {
            "slope": model.params[1],
            "intercept": model.params[0],
            "r_squared": model.rsquared,
            "p_value": model.pvalues[1]
        }
        
        return {
            "descriptive": desc_stats,
            "correlation": {"coefficient": corr, "p_value": p_value},
            "regression": regression_summary
        }
    except Exception as e:
        print(f"Error computing statistics: {e}")
        return None

# Create dashboard
def create_dashboard(category="All"):
    df = load_data()
    if df is None:
        return pn.pane.Markdown("Error: Failed to load data.")
    
    # Filter DataFrame
    filtered_df = df if category == "All" else df[df["day_category"] == category]
    
    # Save to Excel
    excel_file = "panel_sales_data.xlsx"
    sheet_name = "SalesAnalysis"
    create_excel_with_sheet(excel_file, sheet_name, filtered_df.to_dict('records'))
    
    # Create table
    table = pn.widgets.DataFrame(filtered_df, name="Sales Data", width=800)
    
    # Create bar chart
    bar_fig = px.bar(
        filtered_df,
        x="name",
        y="sales",
        color="day_category",
        title=f"Sales by Person ({category})",
        labels={"sales": "Sales Amount ($)", "name": "Person"}
    )
    bar_fig.update_layout(plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9")
    bar_plot = pn.pane.Plotly(bar_fig)
    
    # Create scatter plot with regression line
    scatter_fig = px.scatter(
        filtered_df,
        x="age",
        y="sales",
        color="day_category",
        title=f"Sales vs. Age ({category})",
        labels={"sales": "Sales Amount ($)", "age": "Age"}
    )
    if not filtered_df.empty:
        stats = compute_statistics(filtered_df)
        if stats and stats["regression"]:
            reg = stats["regression"]
            x_range = [filtered_df["age"].min(), filtered_df["age"].max()]
            y_pred = [reg["intercept"] + reg["slope"] * x for x in x_range]
            scatter_fig.add_trace(go.Scatter(
                x=x_range, y=y_pred, mode="lines", name="Regression Line",
                line={"color": "red", "dash": "dash"}
            ))
    scatter_fig.update_layout(plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9")
    scatter_plot = pn.pane.Plotly(scatter_fig)
    
    # Statistical summary
    stats = compute_statistics(filtered_df)
    if stats:
        stats_text = f"""
        ### Statistical Summary
        **Descriptive Statistics**:
        - Age: Mean={stats['descriptive']['age']['mean']:.2f}, Std={stats['descriptive']['age']['std']:.2f}
        - Sales: Mean={stats['descriptive']['sales']['mean']:.2f}, Std={stats['descriptive']['sales']['std']:.2f}
        
        **Correlation (Age vs. Sales)**:
        - Coefficient: {stats['correlation']['coefficient']:.3f}
        - P-value: {stats['correlation']['p_value']:.3f}
        
        **Linear Regression (Sales ~ Age)**:
        - Slope: {stats['regression']['slope']:.2f}
        - Intercept: {stats['regression']['intercept']:.2f}
        - R²: {stats['regression']['r_squared']:.3f}
        - P-value: {stats['regression']['p_value']:.3f}
        """
    else:
        stats_text = "Error: Unable to compute statistics."
    stats_pane = pn.pane.Markdown(stats_text)
    
    return pn.Column(table, bar_plot, scatter_plot, stats_pane)

# Create dropdown
category_select = pn.widgets.Select(
    name="Filter by Day Category",
    options=["All"] + list(load_data()["day_category"].unique()),
    value="All"
)

# Bind dropdown to dashboard
dashboard = pn.bind(create_dashboard, category=category_select)

# Layout
layout = pn.Column(
    pn.pane.Markdown("# Sales Analysis Dashboard (SQLite)"),
    category_select,
    dashboard
)

# Serve the dashboard
layout.servable()