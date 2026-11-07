from groq import Groq
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Business Analyst Copilot", page_icon="📊", layout="wide"
)

# App Header
st.title("📊 AI-Powered Customer Churn & Business Insights Copilot")
st.markdown(
    "Enterprise-grade analytics dashboard combining automated data processing"
    " with an LLM-powered business copilot."
)


# Load data securely with caching
@st.cache_data
def load_data():
  return pd.read_csv("Telco-Customer-Churn.csv")


try:
  df = load_data()

  # Key Business Metrics Calculations
  total_customers = len(df)
  churned_df = df[df["Churn"] == "Yes"]
  churned_count = len(churned_df)
  churn_rate = (churned_count / total_customers) * 100

  # Financial Impact Metric ($ Loss Calculation)
  if "MonthlyCharges" in df.columns:
    monthly_revenue_at_risk = churned_df["MonthlyCharges"].sum()
  else:
    monthly_revenue_at_risk = 0.0

  # --- CREATE PROFESSIONAL TABS ---
  tab1, tab2, tab3 = st.tabs([
      " Executive Dashboard",
      " Data Explorer",
      " AI Business Copilot",
  ])

  with tab1:
    st.subheader("Executive KPI Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Churned Customers", f"{churned_count:,}")
    col3.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
    col4.metric(
        "Monthly Revenue Loss", f"${monthly_revenue_at_risk:,.2f}", delta="-Risk"
    )

    st.markdown("---")

    # Interactive Chart
    fig = px.histogram(
        df,
        x="Contract",
        color="Churn",
        barmode="group",
        title="Customer Churn Distribution by Contract Type",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Professional Analyst Commentary Box
    st.info(
        f" **Analyst Insight:** Month-to-month contracts exhibit"
        " disproportionate churn rates compared to long-term commitments."
        f" Current monthly revenue exposure stands at"
        f" **${monthly_revenue_at_risk:,.2f}**. Retention campaigns should"
        " target month-to-month subscribers within their first 90 days of"
        " tenure."
    )

  with tab2:
    st.subheader("Raw Telemetry & Segment Filtering")
    st.markdown(
        "Explore underlying subscriber records and filter by contract or"
        " payment type."
    )

    selected_contract = st.selectbox(
        "Filter by Contract Type:",
        options=["All"] + list(df["Contract"].unique()),
    )

    if selected_contract != "All":
      filtered_df = df[df["Contract"] == selected_contract]
    else:
      filtered_df = df

    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.caption(
        f"Showing {len(filtered_df):,} filtered records out of"
        f" {len(df):,} total records."
    )

  with tab3:
    st.subheader("AI Business Analyst Assistant")
    st.markdown(
        "Ask strategic business questions regarding customer retention and"
        " churn drivers."
    )

    # Pre-set prompts for recruiters/hiring managers
    st.markdown("**Sample Strategic Prompts to Try:**")
    st.markdown(
        "* `What pricing strategy can reduce drop-off in month-to-month"
        " contracts?`\n* `How can we convert high-risk subscribers into 1-year"
        " contracts?`\n* `Draft an executive summary of our top revenue retention"
        " risks.`"
    )

    if "GROQ_API_KEY" in st.secrets:
      groq_api_key = st.secrets["GROQ_API_KEY"]

      user_question = st.text_input(
          "Enter your business query:",
          placeholder=(
              "e.g., What pricing strategy can reduce drop-off in"
              " month-to-month contracts?"
          ),
      )

      if user_question:
        client = Groq(api_key=groq_api_key)
        prompt = (
            f"You are an expert Enterprise Business Analyst. Based on a Telco"
            f" dataset with {total_customers} customers, an overall churn"
            f" rate of {churn_rate:.1f}%, and a monthly revenue risk of"
            f" ${monthly_revenue_at_risk:,.2f}, answer this question concisely"
            f" with actionable, professional business recommendations:"
            f" {user_question}"
        )

        with st.spinner("AI Copilot is analyzing enterprise metrics..."):
          chat_completion = client.chat.completions.create(
              messages=[{"role": "user", "content": prompt}],
              model="openai/gpt-oss-20b",
          )
          st.success(chat_completion.choices[0].message.content)
    else:
      st.warning(
          "Groq API Key not found in Streamlit Secrets. Please configure it"
          " in your Streamlit app settings."
      )

except Exception as e:
  st.error(
      f"Error loading dataset: {e}. Make sure 'Telco-Customer-Churn.csv' is"
      " uploaded in your GitHub repository."
  )
