import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ollama

convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.1:8b', messages=convo, stream=True)
    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    convo.append({'role': 'assistant', 'content': response})
    return response

# Streamlit UI
st.title("Budget Optimization Assistant")

st.header("Enter Your Financial Data")

income = st.number_input("Total Monthly Income", min_value=0)
entertainment = st.number_input("Total Spend on Entertainment", min_value=0)
bills = st.number_input("Total Spend on Bills", min_value=0)
food = st.number_input("Total Spend on Food", min_value=0)
emi = st.number_input("Total EMI", min_value=0)

if st.button("Analyze"):
    # Parse expenses
    expense_dict = {
        "Entertainment": entertainment,
        "Bills": bills,
        "Food": food,
        "EMI": emi
    }

    # Convert to DataFrame for visualization
    expense_df = pd.DataFrame(list(expense_dict.items()), columns=["Category", "Amount"])

    # Generate recommendation
    total_expenses = sum(expense_dict.values())
    prompt = f'Total Income: {income}\nExpenses: {expense_dict}\nTotal Expenses: {total_expenses}. Give me plan to reduce expenses on entertainment and bills.recommend the best ongoing offers on e-commerce platforms like Flipkart, Amazon, and others for categories like electronics, fashion, and home appliances'
    response = stream_response(prompt=prompt)
    
    st.write("**Recommendation:**")
    st.write(response)

    # Visualize data
    st.write("**Expenses Breakdown:**")
    fig, ax = plt.subplots()
    ax.pie(expense_df["Amount"], labels=expense_df["Category"], autopct='%1.1f%%')
    st.pyplot(fig)

    st.write("**Expenses vs. Savings:**")
    savings = income - total_expenses
    fig, ax = plt.subplots()
    ax.bar(["Savings", "Expenses"], [savings, total_expenses])
    st.pyplot(fig)
    st.header("Query Based on Analysis")
    follow_up_prompt = st.text_input("Ask a follow-up question based on the recommendation")
    if st.button("Run Follow-up Query"):
        follow_up_response = stream_response(prompt=f"{response}\n{follow_up_prompt}")
        st.write(follow_up_response)


