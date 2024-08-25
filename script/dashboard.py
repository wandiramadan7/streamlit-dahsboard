import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load preprocessed data
df = pd.read_csv(r'..\data\financial_risk.csv')

# Set page config to wide layout
st.set_page_config(layout="wide")

# Custom CSS to force content to take full screen width
st.markdown(
    """
    <style>
    .main {
        max-width: 100vw;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Baris 1
with st.container():
    st.markdown(
        """
        <style>
        .row1 {
            background-color: #ffaa00; 
            padding: 10px;
            border-radius: 5px;
            display: flex;
            gap: 10px; /* Space between columns */
        }
        .col {
            background-color: #ffaa00;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        <div class="row1">
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.title('Financial Risk Dashboard')
    with col2:
        # Gender Filter with 'Select All' option
        gender_options = ['Select All'] + df['Gender'].unique().tolist()
        selected_gender = st.selectbox('Gender', options=gender_options)

        if selected_gender == 'Select All':
            selected_gender = df['Gender'].unique()
        else:
            selected_gender = [selected_gender]
    with col3:
        # Education Level Filter with 'Select All' option
        education_options = ['Select All'] + df['Education Level'].unique().tolist()
        selected_education = st.selectbox('Education Level', options=education_options)

        if selected_education == 'Select All':
            selected_education = df['Education Level'].unique()
        else:
            selected_education = [selected_education]
    with col4:
        # Employment Status Filter with 'Select All' option
        employment_options = ['Select All'] + df['Employment Status'].unique().tolist()
        selected_employment = st.selectbox('Employment Status', options=employment_options)

        if selected_employment == 'Select All':
            selected_employment = df['Employment Status'].unique()
        else:
            selected_employment = [selected_employment] 


# Apply filters to data
filtered_df = df[(df['Gender'].isin(selected_gender)) & 
                 (df['Education Level'].isin(selected_education)) & 
                 (df['Employment Status'].isin(selected_employment))]

with st.container():
    st.markdown(
        """
        <style>
        .row1 {
            background-color: #ffaa00; 
            padding: 10px;
            border-radius: 5px;
            border: 2px solid #ffaa00;
        }
        </style>
        <div class="row1">
        """,
        unsafe_allow_html=True
    )
    # Header KPIs
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1,1]) 
    col1.metric("Average of Income", f"{filtered_df['Income_K'].mean():,.2f}K")
    col2.metric("Average of Loan Amount", f"{filtered_df['Loan_Amount_K'].mean():,.2f}K")
    col3.metric("Average of Credit Score", f"{filtered_df['Credit Score'].mean():,.2f}")
    col4.metric("Average of Assets Value", f"{filtered_df['Assets_Value_K'].mean():,.2f}K")
    col5.metric("Average of Years at Current Job", f"{filtered_df['Years at Current Job'].mean():.2f}")


with st.container():
    st.markdown(
        """
        <style>
        .row1 {
            background-color: #ffaa00; 
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        <div class="row1">
        """,
        unsafe_allow_html=True
    )
    # Second row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Rasio lebar: 1:1:1:2:3
    with col1:
        # Loan Amount by Loan Purpose
        st.subheader('Loan Amount by Loan Purpose')
        loan_purpose_data = filtered_df.groupby('Loan Purpose')['Loan Amount'].sum()
        st.bar_chart(loan_purpose_data)
    with col2:
        # Clients by Education Level
        st.subheader('Clients by Education Level')
        education_level_data = filtered_df['Education Level'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(education_level_data, labels=education_level_data.index, autopct='%1.2f%%', colors=['#FF6347', '#FFA500', '#FFD700', '#FF4500'])
        st.pyplot(fig)
    with col3:
        # Average of Income by Gender
        st.subheader('Average of Income by Gender')
        gender_income_data = filtered_df.groupby('Gender')['Income'].mean()
        fig, ax = plt.subplots()
        ax.pie(gender_income_data, labels=gender_income_data.index, autopct='%1.2f%%', colors=['#FF6347', '#FFA500', '#FFD700'])
        st.pyplot(fig)
    with col4:
        # Numbers Clients by Risk Rating
        st.subheader('Numbers Clients by Risk Rating')
        risk_rating_data = filtered_df['Risk Rating'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(risk_rating_data, labels=[f"{i} ({v/len(filtered_df)*100:.0f}%)" for i, v in risk_rating_data.items()], autopct='%1.1f%%', colors=['#FF6347', '#FFA500', '#FFD700'])
        st.pyplot(fig)


with st.container():
    st.markdown(
        """
        <style>
        .row1 {
            background-color: #ffaa00; 
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        <div class="row1">
        """,
        unsafe_allow_html=True
    )
    #third row
    col1, col2, col3 = st.columns([1, 1, 1])  
    with col1:
        # Clients by Age Group
        st.subheader('Clients by Age Group')
        age_group_data = filtered_df['Age_Group'].value_counts()
        st.bar_chart(age_group_data)
    with col2:
        # Numbers Clients by Debt-to-Income Ratio
        st.subheader('Numbers Clients by Debt-to-Income Ratio (bins)')
        debt_to_income_data = filtered_df['Debt_to_Income_Bin'].value_counts().sort_index()
        st.bar_chart(debt_to_income_data)
    with col3:
        # Detail Table
        st.subheader('Detail')
        st.dataframe(filtered_df[['Income', 'Credit Score', 'Loan Amount', 'Assets Value']])


# Custom Styles
st.markdown("""
    <style>
    .stMetric {
        color: #F2B071;
        background-color: #F2B071;
        border: 2px solid #F2B071;
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
