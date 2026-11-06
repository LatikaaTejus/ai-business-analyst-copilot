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

  # AI Section
  st.markdown("---")
  st.subheader("💬 AI Business Analyst Assistant")
  st.markdown(
      "Type your free Groq API key below and ask strategic questions about this"
      " data."
  )

  groq_api_key = st.text_input(
      "Enter your Free Groq API Key:", type="password", placeholder="gsk_..."
  )
  user_question = st.text_input(
      "Ask a question (e.g., 'What is driving churn in month-to-month"
      " contracts?'):"
  )

  if user_question and groq_api_key:
    client = Groq(api_key=groq_api_key)
    prompt = (
        f"You are an expert Business Analyst. Based on a Telco dataset with"
        f" {total_customers} customers and an overall churn rate of"
        f" {churn_rate:.1f}%, answer this question concisely with actionable"
        f" business recommendations: {user_question}"
    )

    with st.spinner("AI is analyzing the business metrics..."):
      chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.1-8b-instant",
)
      )
      st.success(chat_completion.choices[0].message.content)
  elif user_question and not groq_api_key:
    st.warning("Please enter your free Groq API key above to use the AI.")

except Exception as e:
  st.error(
      f"⚠️ Error loading dataset: {e}. Make sure 'Telco-Customer-Churn.csv' is"
      " uploaded in the same GitHub repository as app.py!"
  )
