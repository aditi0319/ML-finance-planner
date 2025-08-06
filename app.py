import streamlit as st
import numpy as np
# import plotly.graph_objects as go

# Function to calculate SIP
def calculate_sip(goal_amount, annual_return_rate, years):
    if goal_amount <= 0 or years <= 0:
        raise ValueError("Goal amount and years must be greater than 0.")
    r = annual_return_rate / 12 / 100
    n = years * 12
    sip = goal_amount * r / ((1 + r)**n - 1) if r > 0 else goal_amount / n
    return round(sip, 2)

# Function to generate chart
# def generate_projection_chart(values, title):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=list(range(1, len(values) + 1)),
#         y=values,
#         mode='lines+markers',
#         line=dict(color='teal'),
#         fill='tozeroy',
#         name="Investment Growth"
#     ))
#     fig.update_layout(
#         title=title,
#         xaxis_title="Months" if len(values) > 12 else "Years",
#         yaxis_title="Investment Value (₹)",
#         plot_bgcolor='rgba(248, 248, 255, 1)',
#         paper_bgcolor='rgba(248, 248, 255, 1)',
#         font=dict(color='black')
#     )
#     return fig

# Function to return allocation based on goal_type
# def get_allocation(goal_type):
#     if goal_type == "Education":
#         return {"Mutual Funds": 0.7, "Gold": 0.1, "FD": 0.2}
#     elif goal_type == "Retirement":
#         return {"Mutual Funds": 0.6, "Gold": 0.2, "FD": 0.2}
#     elif goal_type == "Vacation":
#         return {"Mutual Funds": 0.5, "Gold": 0.3, "FD": 0.2}
#     elif goal_type == "Wedding":
#         return {"Mutual Funds": 0.5, "Gold": 0.4, "FD": 0.1}
#     else:
#         return {"Mutual Funds": 0.7, "Gold": 0.1, "FD": 0.2}

# Page config
st.set_page_config(page_title=" Financial Planner", layout="centered")
st.title(" Financial Planning App")

# Only SIP Calculator tab
st.header(" SIP Goal Planner")

salary = st.number_input("Monthly Salary (₹)", min_value=5000, max_value=200000, value=30000, step=1000, key="sip_salary_input")
expenses = st.number_input("Monthly Expenses (₹)", min_value=1000, max_value=salary - 1000, value=20000, step=500, key="sip_expenses_input")
goal_amount = st.number_input("Target Goal Amount (₹)", min_value=10000, max_value=10000000, value=500000, step=10000, key="sip_goal_input")
years_to_goal = st.slider("Years to Achieve Goal", 1, 30, 4, key="sip_years_slider")
expected_return = st.slider("Expected Return Rate (p.a.)", 1.0, 20.0, 12.0, 0.5, key="sip_return_slider")

goal_type = st.selectbox(
    "Select Goal Type",
    ["Education", "Car/Bike", "Retirement", "Vacation", "Wedding"],
    key="goal_type_selectbox"
)

def get_allocation(goal_type):
    allocations = {
        "Education": {"Mutual Funds": 0.6, "Gold": 0.3, "FD": 0.1},
        "Asset(Car,Bike)": {"Mutual Funds": 0.5, "Gold": 0.5, "FD": 0.2},
        "Retirement": {"Mutual Funds": 0.7, "Gold": 0.2, "FD": 0.1},
        "Vacation": {"Mutual Funds": 0.4, "Gold": 0.5, "FD": 0.1},
        "Wedding": {"Mutual Funds": 0.5, "Gold": 0.4, "FD": 0.1},
    }
    return allocations.get(goal_type, {"Mutual Funds": 0.5, "Gold": 0.4, "FD": 0.1})


if st.button("🔍 Predict SIP", key="sip_predict_btn"):
    
    try:
        recommended_sip = calculate_sip(goal_amount, expected_return, years_to_goal)
        st.success(f"You need to invest ₹{recommended_sip:,} per month to reach ₹{goal_amount:,} in {years_to_goal} years.")

        # Allocation
        allocation = get_allocation(goal_type)
        st.subheader("📊 Suggested Allocation")
        for name, pct in allocation.items():
            st.write(f"{name}: ₹{recommended_sip * pct:.2f} ({int(pct * 100)}%)")

        # Chart
        # months = years_to_goal * 12
        # values = [recommended_sip * (((1 + expected_return/12/100) ** i - 1) / (expected_return/12/100)) for i in range(1, months + 1)]
        # fig = generate_projection_chart(values, "Projected SIP Growth")
        # st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

