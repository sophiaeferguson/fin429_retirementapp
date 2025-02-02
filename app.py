import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title = "FIN429 Retirement App", page_icon="🧐")

st.title ("FIN429 Retirement App")
st.subheader("Plan you retirement savings with expense tracking, loan repayment calculator, investment return calculator, and more!")

# Section 1: Income and Expenses (takes user inputs of basic information such as monthly income and expenses, plots this data into a pie chart)

# Monthly Income
st.header("Monthly Income")
annual_salary = st.number_input ("Enter your annual salary ($):", min_value =0.0, step = 1000.0, value =50000.0)
tax_rate = st.slider ("Select your tax rate (%):", min_value = 0.0, max_value =50.0, value =20.0, step=1.0)

# Calculate take-home monthly income
tax_rate = tax_rate / 100
monthly_income = (annual_salary * (1 - tax_rate)) / 12
st.write(f"Your monthly take-home income is: **${monthly_income:.2f}**")

# Monthly Expenses
st.header("Monthly Expenses")
rent = st.number_input("Monthly Rent ($):", min_value=0.0, step=50.0, value=1000.0)
food = st.number_input("Monthly Food Budget ($):", min_value=0.0, step=50.0, value=500.0)
transport = st.number_input("Monthly Transport Costs ($):", min_value=0.0, step=50.0, value=200.0)

total_expenses = rent + food + transport
monthly_savings = max(monthly_income - total_expenses, 0)

st.write(f"Your total monthly expenses are: **${total_expenses:.2f}**")
st.write(f"Your estimated monthly savings are: **${monthly_savings:.2f}**")

#Pie Chart of Expenses, created by Josue Rivas
st.header("Pie Chart of Expenses")
labels = ['Rent', 'Food', 'Transport']
values = [rent, food, transport]
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
st.plotly_chart(fig, use_container_width=True)


# Section 2: Savings Goals (takes user inputs of savings goals, contribution, etc. Calculates progress and gives dynamic feedback based on the inputs of the user)

st.title("Retirement Savings Goal Tracker")

st.subheader("Track your savings progress and forecast future growth.")

# User Inputs
current_savings = st.number_input( "Enter your current savings ($):", min_value=0.0, step=1000.0, value=10000.0)
savings_goal = st.number_input( "Set your savings goal ($):", min_value=0.0, step=1000.0, value=500000.0)
monthly_contribution = st.number_input( "Monthly Contribution ($):", min_value=0.0, step=50.0, value= 500.0)
annual_return = st.slider( "Expected Annual Return (%):", min_value=0.0,max_value=15.0, value=8.0)/100
years_to_retirement = st.slider( "Years to Retirement:", min_value=1, max_value=50, value=30, step=1)

# Calculating projected savings over time
total_months = years_to_retirement * 12
monthly_return_rate = (1 + (annual_return/12))
savings_over_time = [current_savings]
future_savings = current_savings
for month in range (total_months):
    future_savings = (future_savings*monthly_return_rate) + monthly_contribution
    savings_over_time.append(future_savings)

# Display projected savings at retirement
st.write(f"**Future savings: ${future_savings:,.2f}**")

# Progress Calculation
progress = min (future_savings / savings_goal, 1.0 )
st.write(f"**Progress toward your goal: {progress * 100:.2f} %**" )
st.progress(progress)

# Dynamic Feedback
if progress == 0 :
    st.warning("You haven't started yet. Time to begin saving!")
elif progress < 0.3 :
    st.warning(f"You're at {progress * 100:.2f}%—consider increasing your savings rate!")
elif progress < 0.5 :
    st.info( "You're making progress! Keep going!" )
elif progress < 1.0 :
    st.success( "You're on track! Keep pushing toward your goal!" )
else :
    st.success( "Congratulations! You've reached your retirement savings goal! 🎉")

# Visualization of Savings Growth Over Time

st.subheader( "Projected Savings Growth Over Time" )
fig = go.Figure()
fig.add_trace(go.Scatter(x= list ( range (total_months + 1)), y=savings_over_time, mode= 'lines' , name= 'Savings' ))
fig.update_layout(title= "Savings Growth Over Time" , xaxis_title= "Months" , yaxis_title= "Total Savings ($)" )
st.plotly_chart(fig, use_container_width= True )



# Section 3: Investments, created by Sophia Ferguson (takes user inputs of all variables in compound interest formula, calculates return on investment based on the inputs)
st.header ("Investment Return Calculator")
P = st.number_input("Enter your initial investment: ($):", min_value =0.0, step = 1.0, value =1.0)
i = st.number_input("Enter your interest rate: (%):", min_value =0.0, step = 1.0, value =1.0)
i= i/100
n = st.number_input ("Enter the number of times interest is compunded per year: ", min_value = 1.0, step = 1.0, value =1.0)
t = st.number_input ("Enter the number of years you are holding the investment for", min_value=0.0, step =1.0, value =1.0)

compound_interest_calc = P*(1+i/n)** (n*t)
st.write (f"Your return on this investment is: **${compound_interest_calc:,.2f}**")

# Section 4: Inflation/Growth Rate Comparasion (takes user inputs of expected inflation rate, growth rate, years to retirement and calculates Future Value with growth rate adjusted for inflation - plots this data)
st.header("Inflation and Growth Rate Comparison")
st.subheader("Compare the impact of inflation rates to your financial growth rate over time.")

inflation_rate = st.slider("Select Expected Annual Inflation Rate (%):", min_value=0.0, max_value=10.0, value=2.5, step=0.1)/100
growth_rate = st.slider("Expected Portfolio Growth:", min_value=0.0, max_value=10.0, value=2.5, step=.01)/100
years_to_retirement = st.slider("Years until retirement:", min_value=1, max_value=50, value=30, step=1)

# Portfolio Growth Rate (adjusted for inflation)
yearly_return_rate = growth_rate - inflation_rate

# Array Creation for Expected/Real Savings
expected_savings = [monthly_savings]
real_savings = [monthly_savings]

# Monthly Future Value Calculation
for month in range(1, years_to_retirement*12):
  expected_savings.append(monthly_savings+expected_savings[-1]*(1 + (growth_rate/12)))
  real_savings.append(monthly_savings+real_savings[-1]*(1 + (yearly_return_rate/12)))
  
# Plotting Inflation Rate and Growth Rate
plt.figure(figsize=(10, 6))
plt.plot(expected_savings, label='Expected Savings', color='blue', marker='o')
plt.plot(real_savings, label='Inflation-Adjusted Savings', color='green', linestyle='--')

plt.title('Impact of Inflation on Savings For Each Month Until Retirement', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Amount (USD)', fontsize=12)
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.pyplot(plt)

#Section 5: Loan Repayment Calculator, created by Natalie Simkins. Takes in user inputs for loan principal, interest rate, loan term, and then creates an amortization table based on the information.
from tabulate import tabulate as tb
st.header ("Loan Repayment Calculator")
#Taking user inputs for loan principal, interest rate, and loan term.
r = st.number_input("Annual Interest Rate (%):", min_value=0.0, step=0.1, value=5.0)/100/12
PV = st.number_input("Original Loan Principal Amount ($):", min_value=0.0, step=1000.0, value=50000.0)
N = (st.number_input("Loan Term (years):", min_value=1, step=1, value=5))*12
#Calculating and displaying the payment per month.
PMT = r*PV/(1-(1+r)**-N)
st.write("Assuming a monthly payment of **${:,.2f}**".format(PMT))
st.write(f"Please see the amortization table below for a detailed breakdown of your loan payment schedule.")
#Loan Amortization Schedule function. Creates a list and then iterates through and appends values to calculate the remaining loan balance after each payment period.
def AmortizationSchedule(PV, r, N, PMT):
    # Creating the list to store the amortization schedule
    schedule = []
    beginning_balance = PV
    #Iterating through until there are no payments left
    for i in range(1, N+1):
        interest = beginning_balance * r
        principal = PMT - interest
        ending_balance = beginning_balance - principal
        schedule.append((i, beginning_balance, PMT, interest, principal, ending_balance))
        beginning_balance = ending_balance
    return schedule
#Printing the amortization table
st.write(tb(AmortizationSchedule(PV, r, N, PMT), headers=['Month', 'Beginning Balance', 'Payment', 'Interest', 'Principal', 'End Balance'], tablefmt='github', floatfmt=",.2f"))

