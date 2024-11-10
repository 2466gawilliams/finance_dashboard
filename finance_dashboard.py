# advanced_finance_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, get_session, FinancialEntry

# Initialize the database
engine = init_db()
session = get_session(engine)

# Set the title of the app
st.title("📈 Advanced Personal Finance Dashboard with Persistence")

# User Authentication Placeholder (We'll implement this in the next section)
# For now, assume a single user named 'G.A.'
current_user = 'G.A.'

# Sidebar for user input
st.sidebar.header("Enter Your Financial Details")

def add_entry():
    """Function to add a new monthly entry to the database."""
    month = st.sidebar.selectbox("Month", [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    year = st.sidebar.number_input("Year", min_value=2000, max_value=2100, value=2024)
    income = st.sidebar.number_input("Monthly Income ($)", min_value=0, value=5000)
    
    st.sidebar.subheader("Expenses")
    rent = st.sidebar.number_input("Rent/Mortgage ($)", min_value=0, value=1500)
    utilities = st.sidebar.number_input("Utilities ($)", min_value=0, value=300)
    groceries = st.sidebar.number_input("Groceries ($)", min_value=0, value=400)
    transportation = st.sidebar.number_input("Transportation ($)", min_value=0, value=200)
    entertainment = st.sidebar.number_input("Entertainment ($)", min_value=0, value=150)
    others = st.sidebar.number_input("Others ($)", min_value=0, value=100)
    
    if st.sidebar.button("Add Entry"):
        total_expenses = rent + utilities + groceries + transportation + entertainment + others
        savings = income - total_expenses
        entry = FinancialEntry(
            user=current_user,
            month=month,
            year=year,
            income=income,
            rent=rent,
            utilities=utilities,
            groceries=groceries,
            transportation=transportation,
            entertainment=entertainment,
            others=others,
            total_expenses=total_expenses,
            savings=savings
        )
        session.add(entry)
        session.commit()
        st.sidebar.success("Entry added successfully!")

add_entry()

# Fetch data from the database
def load_data(user):
    entries = session.query(FinancialEntry).filter(FinancialEntry.user == user).all()
    data = [{
        'Month': f"{entry.month} {entry.year}",
        'Income': entry.income,
        'Rent/Mortgage': entry.rent,
        'Utilities': entry.utilities,
        'Groceries': entry.groceries,
        'Transportation': entry.transportation,
        'Entertainment': entry.entertainment,
        'Others': entry.others,
        'Total Expenses': entry.total_expenses,
        'Savings': entry.savings,
        'Timestamp': entry.timestamp
    } for entry in entries]
    return pd.DataFrame(data)

df = load_data(current_user)

if not df.empty:
    # Overview Section
    st.header("📊 Overview")
    total_income = df['Income'].sum()
    total_expenses = df['Total Expenses'].sum()
    total_savings = df['Savings'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Total Savings", f"${total_savings:,.2f}")
    
    # Expense Distribution Pie Chart
    st.subheader("💸 Expenses Distribution")
    expense_categories = ['Rent/Mortgage', 'Utilities', 'Groceries', 'Transportation', 'Entertainment', 'Others']
    expense_sum = df[expense_categories].sum().reset_index()
    expense_sum.columns = ['Category', 'Amount']
    fig_pie = px.pie(expense_sum, values='Amount', names='Category', title='Expenses Breakdown', hole=0.3)
    st.plotly_chart(fig_pie)
    
    # Income vs Expenses Bar Chart
    st.subheader("💰 Income vs Expenses")
    fig_bar = px.bar(
        df,
        x='Month',
        y=['Income', 'Total Expenses'],
        barmode='group',
        title='Monthly Income vs Expenses'
    )
    st.plotly_chart(fig_bar)
    
    # Savings Over Time Line Chart
    st.subheader("📈 Savings Over Time")
    fig_line = px.line(
        df,
        x='Month',
        y='Savings',
        title='Monthly Savings',
        markers=True
    )
    st.plotly_chart(fig_line)
    
    # Savings Goals
    st.subheader("🎯 Savings Goals")
    goal = st.number_input("Set a Savings Goal ($)", min_value=0, value=10000)
    current_savings = df['Savings'].sum()
    
    # Calculate progress towards savings goal
    progress = (current_savings / goal) * 100 if goal > 0 else 0
    progress = min(progress, 100)  # Cap progress at 100%
    
    # Display progress bar
    st.progress(int(progress))
    
    # Display progress information
    st.write(f"**Current Savings:** ${current_savings:,.2f} / **Goal:** ${goal:,.2f} ({progress:.2f}%)")
    
    # Data Table with Option to Download
    st.subheader("🗃️ Detailed Data")
    st.dataframe(df)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name='personal_finance_data.csv',
        mime='text/csv',
    )
else:
    st.info("Please add your financial details using the sidebar to see the dashboard.")

# Optional: Add a footer
st.markdown("---")
st.write("© 2024 Advanced Personal Finance Dashboard with Persistence")
