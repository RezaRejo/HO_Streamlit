import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Judul
st.title("🚗 Dashboard Penjualan Mobil")
st.markdown("Project ini menampilkan data penjualan mobil dengan visualisasi interaktif.")

# Contoh Dataset
data = {
    "Merek": ["Toyota", "Honda", "Suzuki", "Mitsubishi", "Toyota", "Honda", "Suzuki", "Mitsubishi"],
    "Model": ["Avanza", "Civic", "Ertiga", "Xpander", "Fortuner", "HR-V", "Baleno", "Pajero"],
    "Tahun": [2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022],
    "Harga": [220_000_000, 350_000_000, 200_000_000, 280_000_000,
              500_000_000, 400_000_000, 250_000_000, 600_000_000],
    "Terjual": [120, 80, 60, 70, 90, 75, 55, 65]
}
df = pd.DataFrame(data)

# Filter
st.sidebar.header("Filter Data")
merek_filter = st.sidebar.multiselect("Pilih Merek", df["Merek"].unique(), default=df["Merek"].unique())
tahun_filter = st.sidebar.multiselect("Pilih Tahun", df["Tahun"].unique(), default=df["Tahun"].unique())
harga_min, harga_max = st.sidebar.slider("Pilih Range Harga", int(df["Harga"].min()), int(df["Harga"].max()), 
                                         (int(df["Harga"].min()), int(df["Harga"].max())), step=10000000)

# Apply Filter
df_filtered = df[(df["Merek"].isin(merek_filter)) & 
                 (df["Tahun"].isin(tahun_filter)) & 
                 (df["Harga"].between(harga_min, harga_max))]

# Statistik
st.subheader("📊 Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Unit Terjual", df_filtered["Terjual"].sum())
col2.metric("Rata-rata Harga", f"Rp {df_filtered['Harga'].mean():,.0f}")
col3.metric("Mobil Terlaris", df_filtered.loc[df_filtered["Terjual"].idxmax(), "Model"] if not df_filtered.empty else "-")

# Visualisasi Bar Chart
st.subheader("Penjualan per Merek")
fig_bar = px.bar(df_filtered, x="Merek", y="Terjual", color="Merek", barmode="group", title="Jumlah Terjual per Merek")
st.plotly_chart(fig_bar)

# Visualisasi Line Chart
st.subheader("Tren Penjualan per Tahun")
fig_line = px.line(df_filtered, x="Tahun", y="Terjual", color="Merek", markers=True)
st.plotly_chart(fig_line)

# Visualisasi Pie Chart
st.subheader("Pangsa Pasar per Merek")
fig_pie = px.pie(df_filtered, names="Merek", values="Terjual", title="Market Share")
st.plotly_chart(fig_pie)

# Tabel Data
st.subheader("📋 Data Penjualan Mobil")
st.dataframe(df_filtered)
