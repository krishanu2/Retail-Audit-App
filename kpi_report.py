import pandas as pd

df = pd.read_excel('output/Cleaned_Data.xlsx')

# KPI 1: Total rows after cleaning
total_rows = len(df)

# KPI 2: Total mismatched prices
price_mismatches = df['Price_Flag'].sum()

# KPI 3: Store-wise sales summary
store_sales = df.groupby('Source_File')['Total'].sum()

# KPI 4: Top 5 most sold products
top_products = df.groupby('Product line')['Total'].sum().sort_values(ascending=False).head(5)

# Print KPIs
print("📊 Reconciliation KPI Report")
print(f"✔ Total Cleaned Rows: {total_rows}")
print(f"✔ Products with Price Mismatches: {price_mismatches}")
print("\n💰 Store-wise Sales:")
print(store_sales)
print("\n🏆 Top 5 Product Lines by Sales:")
print(top_products)
