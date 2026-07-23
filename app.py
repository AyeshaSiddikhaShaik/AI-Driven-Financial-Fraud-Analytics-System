import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="AI-Driven Financial Fraud Analytics System",
    page_icon="💳",
    layout="wide"
)

# ---------- Load Dataset ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "paysim_feature_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

# ---------- KPIs ----------
total_transactions = len(df)
fraud_transactions = int(df["isFraud"].sum())
fraud_rate = round((fraud_transactions / total_transactions) * 100, 2)
avg_amount = round(df["amount"].mean(), 2)

# ---------- Sidebar ----------
st.sidebar.image(
    "https://img.icons8.com/color/96/bank-card-back-side.png",
    width=80
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "📊 Analytics",
        "🤖 Fraud Prediction",
        "📁 Upload CSV",
        "📋 Data Explorer",
        "ℹ️ About"
    ]
)

# ---------- Dashboard ----------
if page == "🏠 Dashboard":

    st.title("💳 AI-Driven Financial Fraud Analytics System")

    st.markdown("""
### Intelligent Detection of Financial Fraud using Machine Learning

Analyze transaction patterns, detect fraudulent activities,
and gain valuable insights through an interactive dashboard.
""")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Transactions", f"{total_transactions:,}")

    c2.metric("Fraud Cases", f"{fraud_transactions:,}")

    c3.metric("Fraud Rate", f"{fraud_rate}%")

    c4.metric("Average Amount", f"₹ {avg_amount:,.2f}")

    st.divider()

    st.subheader("📌 Project Highlights")

    a, b = st.columns(2)

    with a:
        st.success("""
✔ Random Forest Model

✔ Isolation Forest

✔ Feature Engineering

✔ Fraud Analytics
""")

    with b:
        st.info("""
Dataset : PaySim

Language : Python

Visualization : Power BI + Streamlit

Deployment : Streamlit Cloud
""")
        
elif page == "📊 Analytics":

    import plotly.express as px

    st.title("📊 Fraud Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            df,
            names="isFraud",
            title="Fraud vs Genuine Transactions",
            hole=0.45
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df.groupby("type")["isFraud"].sum().reset_index(),
            x="type",
            y="isFraud",
            title="Fraud Transactions by Type",
            color="type"
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        df,
        x="amount",
        nbins=50,
        title="Transaction Amount Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Fraud Prediction":

    import joblib
    import numpy as np
    import os

    st.title("🤖 AI Fraud Prediction")
    st.info("Enter transaction details to predict whether the transaction is Fraudulent or Genuine.")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "fraud_detection_model.pkl"
    )

    ENCODER_PATH = os.path.join(
        BASE_DIR,
        "models",
        "label_encoder.pkl"
    )

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    col1, col2 = st.columns(2)

    with col1:
        txn_type = st.selectbox(
            "Transaction Type",
            ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
        )

        amount = st.number_input(
            "Transaction Amount",
            min_value=0.0,
            value=1000.0
        )

        oldbalanceOrg = st.number_input(
            "Old Sender Balance",
            min_value=0.0,
            value=5000.0
        )

    with col2:

        newbalanceOrig = st.number_input(
            "New Sender Balance",
            min_value=0.0,
            value=4000.0
        )

        oldbalanceDest = st.number_input(
            "Old Receiver Balance",
            min_value=0.0,
            value=2000.0
        )

        newbalanceDest = st.number_input(
            "New Receiver Balance",
            min_value=0.0,
            value=3000.0
        )

    if st.button("🔍 Predict Fraud"):

        txn_type_encoded = encoder.transform([txn_type])[0]

        balanceOrigDiff = oldbalanceOrg - newbalanceOrig
        balanceDestDiff = newbalanceDest - oldbalanceDest

        amount_to_balance_ratio = (
            amount / oldbalanceOrg
            if oldbalanceOrg != 0
            else amount
        )

        high_value_transaction = 1 if amount > 200000 else 0

        zero_balance_sender = 1 if newbalanceOrig == 0 else 0

        zero_balance_receiver = 1 if newbalanceDest == 0 else 0

        input_data = pd.DataFrame([{
            "type": txn_type_encoded,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            "balanceOrigDiff": balanceOrigDiff,
            "balanceDestDiff": balanceDestDiff,
            "amount_to_balance_ratio": amount_to_balance_ratio,
            "high_value_transaction": high_value_transaction,
            "zero_balance_sender": zero_balance_sender,
            "zero_balance_receiver": zero_balance_receiver
        }])

        prediction = model.predict(input_data)[0]

        confidence = model.predict_proba(input_data)[0].max() * 100

        st.divider()

        if prediction == 1:

            st.error("🚨 Fraudulent Transaction Detected")

        else:

            st.success("✅ Genuine Transaction")

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

        st.subheader("Risk Analysis")

        if amount > 200000:
            st.write("• High transaction amount")

        if txn_type == "TRANSFER":
            st.write("• Transfer transaction")

        if txn_type == "CASH_OUT":
            st.write("• Cash Out transaction")

        if zero_balance_sender:
            st.write("• Sender balance became zero")

        if zero_balance_receiver:
            st.write("• Receiver balance is zero")

        if prediction == 0:
            st.write("• No major fraud indicators detected")

elif page == "📁 Upload CSV":

    st.title("📁 Upload CSV")

    uploaded = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded is not None:

        new_df = pd.read_csv(uploaded)

        st.success("File Uploaded Successfully")

        st.write(new_df.head())

        st.write("Rows :", new_df.shape[0])
        st.write("Columns :", new_df.shape[1])
elif page == "📋 Data Explorer":

    st.title("📋 Data Explorer")

    st.dataframe(df)

    st.write("Dataset Shape :", df.shape)

    st.write("Missing Values")

    st.write(df.isnull().sum())

elif page == "ℹ️ About":

    st.title("ℹ️ About This Project")

    st.markdown("""
## AI-Driven Financial Fraud Analytics System

### Technologies Used

- Python
- Pandas
- Scikit-Learn
- Random Forest
- Isolation Forest
- Power BI
- Streamlit

### Dataset

PaySim Synthetic Financial Dataset

### Objective

Detect fraudulent financial transactions using Machine Learning and visualize insights through an interactive dashboard.

### Developed By

Ayesha Siddikha
B.Tech AI & Data Science
""")                    
