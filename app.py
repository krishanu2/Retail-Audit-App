import streamlit as st
import pandas as pd
import os
import io
import zipfile
import datetime
from fpdf import FPDF
from scipy.stats import zscore
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import plotly.express as px
import plotly.graph_objects as go

# Load email credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Page setup
st.set_page_config(page_title="Retail Auditor", layout="wide")
if os.path.exists("banner.png"):
    st.image("banner.png", use_column_width=True)

st.title("🧠 Retail Spreadmart Auditor")
st.caption("Audits store Excel files and identifies issues like duplicates, mismatches, and anomalies.")

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("audit_history", exist_ok=True)

if st.button("🚀 Start Full Audit"):
    all_dfs = []
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            df = pd.read_excel(os.path.join("data", file))
            df['Source_File'] = file
            all_dfs.append(df)

    if not all_dfs:
        st.error("❌ No Excel files found in /data folder.")
        st.stop()

    combined_df = pd.concat(all_dfs, ignore_index=True)
    st.success(f"✅ Loaded {len(combined_df)} rows from {len(all_dfs)} files.")
    st.write("📄 Preview:", combined_df.head())

    audit_log = {'Total Rows': len(combined_df)}

    # Duplicate detection
    dupes = combined_df.duplicated(subset=['Invoice ID', 'Product line', 'Date'], keep=False)
    dup_df = combined_df[dupes]
    audit_log['Duplicate Entries'] = len(dup_df)

    # Price mismatch
    mismatch = combined_df.groupby('Product line')['Unit price'].nunique()
    bad_lines = mismatch[mismatch > 1].index.tolist()
    mismatch_df = combined_df[combined_df['Product line'].isin(bad_lines)]
    audit_log['Products with Price Mismatches'] = len(bad_lines)

    audit_log['Missing Values'] = combined_df.isnull().sum().sum()

    # Cleaned data
    cleaned_df = combined_df.drop_duplicates(subset=['Invoice ID', 'Product line', 'Date'])
    cleaned_df.fillna("MISSING", inplace=True)
    cleaned_df['Price_Flag'] = cleaned_df.groupby('Product line')['Unit price'].transform('nunique') > 1

    # Anomaly Detection
    z_total = zscore(cleaned_df['Total'])
    z_qty = zscore(cleaned_df['Quantity'])
    cleaned_df['Anomaly_Flag'] = (abs(z_total) > 2.5) | (abs(z_qty) > 2.5)
    anomalies_df = cleaned_df[cleaned_df['Anomaly_Flag'] == True]

    # Save versioned audit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M%p")
    version_file = f"audit_{timestamp}.xlsx"
    cleaned_df.to_excel(os.path.join("audit_history", version_file), index=False)

    # KPI display
    st.header("📊 Reconciliation KPIs")
    for k, v in audit_log.items():
        st.metric(label=k, value=v)

    # Charts
    clean_count = audit_log['Total Rows'] - audit_log['Duplicate Entries']
    pie = px.pie(values=[clean_count, audit_log['Duplicate Entries']], names=['Clean Rows', 'Duplicates'], title='🧮 Duplicate Entry Distribution')
    st.plotly_chart(pie, use_container_width=True)

    product_count = combined_df['Product line'].nunique()
    bar = go.Figure(data=[
        go.Bar(name='Mismatched', x=['Price Check'], y=[audit_log['Products with Price Mismatches']], marker_color='red'),
        go.Bar(name='Consistent', x=['Price Check'], y=[product_count - audit_log['Products with Price Mismatches']], marker_color='green')
    ])
    bar.update_layout(title='💸 Product Price Consistency', barmode='stack')
    st.plotly_chart(bar, use_container_width=True)

    # Expanders
    with st.expander("❗ Duplicate Entries"):
        st.dataframe(dup_df)
    with st.expander("💸 Price Mismatches"):
        st.dataframe(mismatch_df)
    with st.expander("🧼 Cleaned Data"):
        st.dataframe(cleaned_df)
    with st.expander("🧠 Suspicious Transactions"):
        st.dataframe(anomalies_df)

    # Download files
    cleaned_buf = io.BytesIO()
    cleaned_df.to_excel(cleaned_buf, index=False)

    audit_csv = pd.DataFrame(list(audit_log.items()), columns=['Issue', 'Count']).to_csv(index=False).encode()
    st.download_button("⬇ Cleaned Data", cleaned_buf.getvalue(), "Cleaned_Data.xlsx")
    st.download_button("⬇ Audit Log", audit_csv, "Audit_Log.csv")

    # ZIP
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zipf:
        zipf.writestr("Cleaned_Data.xlsx", cleaned_buf.getvalue())
        zipf.writestr("Audit_Log.csv", audit_csv)
    st.download_button("📦 Download All (ZIP)", zip_buf.getvalue(), "Audit_Reports.zip")

    # PDF
    if st.button("🖨️ Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Retail Audit Report", ln=True, align='C')
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt=f"Date: {timestamp}", ln=True)
        pdf.ln(5)
        for k, v in audit_log.items():
            pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
        pdf_data = pdf.output(dest='S').encode('latin1')
        st.download_button("📄 Download PDF", pdf_data, "Audit_Report.pdf")

    # Email
    st.subheader("📧 Send Audit Report")
    recipient = st.text_input("Recipient Email")
    if st.button("📨 Send Email"):
        if not recipient:
            st.warning("Enter recipient email.")
        else:
            try:
                msg = EmailMessage()
                msg['Subject'] = "Your Retail Audit Report"
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = recipient
                msg.set_content("Please find attached your audit report.")
                msg.add_attachment(zip_buf.getvalue(), maintype='application', subtype='zip', filename='Audit_Reports.zip')
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                st.success(f"✅ Email sent to {recipient}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Audit history
st.subheader("📂 Previous Audit Reports")
history_files = sorted(os.listdir("audit_history"), reverse=True)
selected_file = st.selectbox("View a previous report:", history_files)
if selected_file:
    hist_df = pd.read_excel(os.path.join("audit_history", selected_file))
    st.dataframe(hist_df.head())
    buf = io.BytesIO()
    hist_df.to_excel(buf, index=False)
    st.download_button(f"⬇ Download {selected_file}", buf.getvalue(), selected_file)
