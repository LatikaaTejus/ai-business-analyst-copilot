# Business Requirements Document (BRD)
## AI-Powered Customer Churn & Business Insights Copilot

### 1. Executive Summary
In subscription-based telecommunications businesses, customer churn directly impacts annual recurring revenue (ARR). While traditional business intelligence (BI) dashboards display macro-level metrics, non-technical stakeholders (such as Customer Success and Retention Marketing teams) often struggle to extract ad-hoc behavioral insights without writing custom SQL queries. This project introduces a self-service, AI-powered analytics copilot designed to bridge the gap between static reporting and dynamic, conversational business strategy.

### 2. Business Objectives
* **Reduce Churn Risk:** Identify high-risk subscriber segments (specifically month-to-month contracts and specific payment methodologies) to target with automated retention campaigns.
* **Democratize Data Access:** Enable non-technical department leaders to query customer telemetry in plain natural language.
* **Accelerate Decision-Making:** Reduce the time-to-insight from hours of manual dashboard filtering to sub-second conversational AI recommendations.

### 3. Target Stakeholders & Users
* **Executive Leadership:** Requires high-level KPI summaries and overall business risk exposure.
* **Customer Success Managers (CSMs):** Require granular visibility into customer drop-off patterns to design loyalty interventions.
* **Data Analysts / BI Engineers:** Benefit from an automated baseline analytics layer that handles repetitive ad-hoc inquiries.

### 4. Functional Requirements
* **F1: Executive KPI Tracking:** The system must automatically compute and display total active user volume, total churned volume, and baseline churn rates.
* **F2: Visual Analytics:** The system must render interactive multidimensional charts (e.g., Churn distribution across contract tiers) to highlight behavioral patterns.
* **F3: Natural Language Copilot:** The system must integrate a secure Large Language Model (LLM) API capable of ingesting dataset statistics and answering strategic ad-hoc business prompts.
* **F4: Enterprise Security:** API credentials must be decoupled from source code and managed via secure environment secret vaults (`st.secrets`).

### 5. Success Metrics (KPIs)
* 100% uptime and accessibility via cloud deployment.
* Sub-2-second response latency for natural language business recommendations.
* Elimination of hardcoded secrets to comply with institutional security standards.
