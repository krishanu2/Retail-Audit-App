# 🧠 Retail Spreadmart Auditor

A professional-grade audit dashboard for small and medium retail chains that rely on Excel for store-level data management. Built with **Python + Streamlit**, it automatically cleans, audits, and analyzes sales data across multiple stores — and generates downloadable audit reports.

---

## 📌 Key Features

- 📁 **Excel Consolidation**: Combines multiple store sales Excel files
- 🧼 **Data Cleaning**: Removes duplicates, fills missing values
- ❗ **Error Detection**:
  - Duplicate transactions
  - Price mismatches within product lines
  - Z-score-based anomaly detection
- 📊 **Dashboards**: KPIs and interactive Plotly charts
- 📄 **PDF/Excel/ZIP Reports**: Download clean data and audit summaries
- 📧 **Email Delivery**: Send reports via Gmail in one click
- 🗂️ **Versioned History**: Saves all audits for future reference

---

## 📸 Demo Preview

![App Screenshot](banner.png) <!-- optional if you upload a banner -->

---

## 🚀 Tech Stack

| Tool        | Purpose                         |
|-------------|----------------------------------|
| Python      | Core scripting & data handling   |
| Streamlit   | Interactive web dashboard        |
| Pandas      | Excel file reading & cleaning    |
| Plotly      | Interactive charts & KPIs        |
| SciPy       | Z-score anomaly detection        |
| FPDF        | PDF generation for audit reports |
| dotenv      | Secure email credential handling |

---

## 📂 Project Structure

Retail-Audit-App/
├── app.py # Main Streamlit app
├── data/ # Upload store Excel files here
├── audit_history/ # Stores past audit versions
├── output/ # Temporary folder for reports
├── requirements.txt # Install dependencies
├── .env # Add your email credentials here
└── README.md # You're reading it!


---

## 🧪 Run Locally

1. **Clone the repo**

```bash
git clone https://github.com/krishanu2/Retail-Audit-App.git
cd Retail-Audit-App

pip install -r requirements.txt


EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

streamlit run app.py


📦 Generate Reports
Cleaned Excel ✅

Audit Log CSV ✅

ZIP download ✅

PDF Report ✅

Email Report Delivery ✅

🧠 About the Developer
Made with 💙 by Krishanu Mahapatra
