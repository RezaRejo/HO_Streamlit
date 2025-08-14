# sales.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/supermarket_sales.csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

df = load_data()

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")
st.title("Supermarket Sales Dashboard")
st.markdown("Visualisasi interaktif penjualan supermarket dengan berbagai filter dan grafik.")

# Sidebar Filters
st.sidebar.header("Filter Data")
city_options = df['City'].unique()
selected_city = st.sidebar.selectbox("Pilih Kota", options=city_options)

product_options = df['Product line'].unique()
selected_products = st.sidebar.multiselect("Pilih Product Line", options=product_options, default=product_options)

min_total, max_total = st.sidebar.slider(
    "Rentang Total Penjualan",
    min_value=float(df['Total'].min()), 
    max_value=float(df['Total'].max()),
    value=(float(df['Total'].min()), float(df['Total'].max()))
)

gender_options = df['Gender'].unique()
selected_gender = st.sidebar.radio("Pilih Gender", options=["Semua"] + list(gender_options))

payment_options = df['Payment'].unique()
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", options=payment_options, default=payment_options)

search_invoice = st.sidebar.text_input("Cari Invoice ID")

# Filter data
filtered_df = df[
    (df['City'] == selected_city) &
    (df['Product line'].isin(selected_products)) &
    (df['Total'] >= min_total) &
    (df['Total'] <= max_total) &
    (df['Payment'].isin(selected_payment))
]

if selected_gender != "Semua":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if search_invoice:
    filtered_df = filtered_df[filtered_df['Invoice ID'].str.contains(search_invoice, case=False)]

# METRICS
total_sales = filtered_df['Total'].sum()
avg_rating = filtered_df['Rating'].mean()
total_transactions = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Penjualan", f"${total_sales:,.2f}")
col2.metric("Rata-rata Rating", f"{avg_rating:.2f}")
col3.metric("Total Transaksi", f"{total_transactions}")

st.markdown("---")

# VISUALISASI
# Bar Chart - Rata-rata Penjualan per Product Line
st.subheader("Rata-rata Penjualan per Product Line")
avg_sales = filtered_df.groupby('Product line')['Total'].mean().sort_values(ascending=True)
fig_bar = px.bar(
    avg_sales,
    x=avg_sales.values,
    y=avg_sales.index,
    orientation='h',
    labels={"x": "Rata-rata Total Penjualan", "y": "Product Line"},
    color=avg_sales.values,
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart - Proporsi Gender
st.subheader("Proporsi Gender")
gender_counts = filtered_df['Gender'].value_counts()
fig_pie = px.pie(
    names=gender_counts.index,
    values=gender_counts.values,
    hole=0.4,
    color=gender_counts.index,
    color_discrete_map={"Female": "#FF69B4", "Male": "#1E90FF"}
)
st.plotly_chart(fig_pie, use_container_width=True)

# Line Chart - Tren Penjualan Harian
st.subheader("Tren Penjualan Harian")
daily_sales = filtered_df.groupby('Date')['Total'].sum().reset_index()
fig_line = px.line(
    daily_sales,
    x='Date',
    y='Total',
    markers=True,
    labels={"Total": "Total Penjualan", "Date": "Tanggal"},
    line_shape="spline"
)
st.plotly_chart(fig_line, use_container_width=True)

# Tabel Data
st.subheader("Data Penjualan (Hasil Filter)")
st.dataframe(filtered_df)

st.markdown("---")
st.markdown("*Dashboard ini dibuat menggunakan Streamlit & Plotly untuk visualisasi interaktif.*")
