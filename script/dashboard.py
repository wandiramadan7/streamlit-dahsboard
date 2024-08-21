import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load preprocessed data
df = pd.read_csv(r'..\data\financial_risk.csv')

# Dashboard Filters
st.sidebar.header("Filter Options")
selected_gender = st.sidebar.multiselect('Gender', options=df['Gender'].unique(), default=df['Gender'].unique())
selected_education = st.sidebar.multiselect('Education Level', options=df['Education Level'].unique(), default=df['Education Level'].unique())
selected_employment = st.sidebar.multiselect('Employment Status', options=df['Employment Status'].unique(), default=df['Employment Status'].unique())

# Apply filters to data
filtered_df = df[(df['Gender'].isin(selected_gender)) & 
                 (df['Education Level'].isin(selected_education)) & 
                 (df['Employment Status'].isin(selected_employment))]

# Streamlit dashboard layout
st.title('Financial Risk Dashboard')

# Header KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Average of Income", f"{filtered_df['Income_K'].mean():,.2f}K")
col2.metric("Average of Loan Amount", f"{filtered_df['Loan_Amount_K'].mean():,.2f}K")
col3.metric("Average of Credit Score", f"{filtered_df['Credit Score'].mean():,.2f}")
col4.metric("Average of Assets Value", f"{filtered_df['Assets_Value_K'].mean():,.2f}K")
col5.metric("Average of Years at Current Job", f"{filtered_df['Years at Current Job'].mean():.2f}")

# Loan Amount by Loan Purpose
st.subheader('Loan Amount by Loan Purpose')
loan_purpose_data = filtered_df.groupby('Loan Purpose')['Loan Amount'].sum()
st.bar_chart(loan_purpose_data)

# Clients by Education Level
st.subheader('Clients by Education Level')
education_level_data = filtered_df['Education Level'].value_counts()
fig, ax = plt.subplots()
ax.pie(education_level_data, labels=education_level_data.index, autopct='%1.2f%%', colors=['#FF6347', '#FFA500', '#FFD700', '#FF4500'])
st.pyplot(fig)

# Average of Income by Gender
st.subheader('Average of Income by Gender')
gender_income_data = filtered_df.groupby('Gender')['Income'].mean()
fig, ax = plt.subplots()
ax.pie(gender_income_data, labels=gender_income_data.index, autopct='%1.2f%%', colors=['#FF6347', '#FFA500', '#FFD700'])
st.pyplot(fig)

# Numbers Clients by Risk Rating
st.subheader('Numbers Clients by Risk Rating')
risk_rating_data = filtered_df['Risk Rating'].value_counts()
fig, ax = plt.subplots()
ax.pie(risk_rating_data, labels=[f"{i} ({v/len(filtered_df)*100:.0f}%)" for i, v in risk_rating_data.items()], autopct='%1.1f%%', colors=['#FF6347', '#FFA500', '#FFD700'])
st.pyplot(fig)

# Numbers Clients by Debt-to-Income Ratio
st.subheader('Numbers Clients by Debt-to-Income Ratio (bins)')
debt_to_income_data = filtered_df['Debt_to_Income_Bin'].value_counts().sort_index()
st.bar_chart(debt_to_income_data)

# Clients by Age Group
st.subheader('Clients by Age Group')
age_group_data = filtered_df['Age_Group'].value_counts()
st.bar_chart(age_group_data)

# Detail Table
st.subheader('Detail')
st.dataframe(filtered_df[['Income', 'Credit Score', 'Loan Amount', 'Assets Value']])

# Custom Styles
st.markdown("""
    <style>
    .stMetric {
        color: #FF4500;
        background-color: #F5F5F5;
        border: 2px solid #FFA500;
    }
    .stBarChart {
        color: #FFA500;
    }
    .stTable {
        background-color: #FF6347;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)
