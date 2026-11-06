from groq import Groq
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Business Analyst Copilot", page_icon="📊", layout="wide"
)

st.title("📊 AI-Powered Business Insights Copilot")
st.markdown(
    "Analyze customer churn data and ask our AI Copilot strategic business"
    " questions."
)


# Load data securely with caching
@st.cache_data
def load_data():
  # This matches the filename you will upload to GitHub
  return pd.read_csv("Telco-Customer-Churn.csv")


try:
  df = load_data()

  # Key Business Metrics
  total_customers = len(df)
  churned = len(df[df["Churn"] == "Yes"])
  churn_rate = (churned / total_customers) * 100

  col1, col2, col3 = st.columns(3)
  col1.metric("Total Customers", f"{total_customers:,}")
  col2.metric("Churned Customers", f"{churned:,}")
  col3.metric("Overall Churn Rate", f"{churn_rate:.1f}%")

  # Interactive Chart
  fig = px.histogram(
      df,
      x="Contract",
      color="Churn",
      barmode="group",
      title="Customer Churn Distribution by Contract Type",
  )
  st.plotly_chart(fig, use_container_width=True)


# AI Section (Using Secure Streamlit Secrets)
st.markdown("---")
st.subheader("💬 AI Business Analyst Assistant")

# Check if the secret is configured
if "GROQ_API_KEY" in st.secrets:
  groq_api_key = st.secrets["GROQ_API_KEY"]

  user_question = st.text_input(
      "Ask a strategic question (e.g., 'What is driving churn in month-to-month"
      " contracts?'):"
  )

  if user_question:
    client = Groq()
    prompt = (
        f"You are an expert Business Analyst. Based on a Telco dataset with"
        f" {total_customers} customers and an overall churn rate of"
        f" {churn_rate:.1f}%, answer this question concisely with actionable"
        f" business recommendations: {user_question}"
    )

    with st.spinner("AI is analyzing the business metrics..."):
      chat_completion = client.chat.completions.create(
          messages=[{"role": "user", "content": prompt}],
          model="openai/gpt-oss-20b",
      )
      st.success(chat_completion.choices[0].message.content)
else:
  st.warning(
      "⚠️ Groq API Key not found in Streamlit Secrets. Please configure it in"
      " your app settings."
  )
