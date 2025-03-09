import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Definisi fungsi
def create_daily_users_df(df):
    return df[["Date", "Total Users"]].copy()

def create_total_registered_users_df(df):
    return df[["Date", "Registered Users"]].copy()

def create_total_casual_users_df(df):
    return df[["Date", "Casual Users"]].copy()

def create_daily_users_by_weather(df):
    detail_penyewa_cuaca = df.groupby("Weather Condition")["Total Users"].sum().reset_index()
    detail_penyewa_cuaca["Total Users"] /= 1_000  # Ubah ke ribuan
    return detail_penyewa_cuaca

def create_daily_users_by_season(df):
    detail_penyewa_musim = df.groupby("Season")["Total Users"].sum().reset_index()
    detail_penyewa_musim["Total Users"] /= 1_000  # Ubah ke ribuan
    return detail_penyewa_musim

def create_hourly_users_df(df):
    detail_penyewa_jam = df.groupby("Hour")["Total Users"].sum().reset_index()
    detail_penyewa_jam["Total Users"] /= 1_000  # Ubah ke ribuan
    return detail_penyewa_jam

# Load dataset
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Konversi "Date" ke datetime
day_df["Date"] = pd.to_datetime(day_df["Date"])
hour_df["Date"] = pd.to_datetime(hour_df["Date"])

# Sort data
day_df.sort_values(by="Date", inplace=True)
hour_df.sort_values(by="Date", inplace=True)

# Reset index setelah sorting
day_df.reset_index(drop=True, inplace=True)
hour_df.reset_index(drop=True, inplace=True)

# Ambil rentang tanggal
min_date_days = day_df["Date"].min().date()
max_date_days = day_df["Date"].max().date()

min_date_hour = hour_df["Date"].min().date()
max_date_hour = hour_df["Date"].max().date()

# Sidebar
with st.sidebar:
    st.image("Logo.png")  # Tambahkan logo perusahaan
    
    # Pilih rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# Filter dataset berdasarkan rentang waktu
main_df_days = day_df[(day_df["Date"] >= pd.to_datetime(start_date)) & 
                       (day_df["Date"] <= pd.to_datetime(end_date))]

main_df_hour = hour_df[(hour_df["Date"] >= pd.to_datetime(start_date)) & 
                        (hour_df["Date"] <= pd.to_datetime(end_date))]

# Buat dataset untuk visualisasi
daily_users_df = create_daily_users_df(main_df_days)
registered_users = create_total_registered_users_df(main_df_days)
casual_users = create_total_casual_users_df(main_df_days)
detail_penyewa_cuaca = create_daily_users_by_weather(main_df_days)
detail_penyewa_musim = create_daily_users_by_season(main_df_days)
detail_penyewa_jam = create_hourly_users_df(main_df_hour)

# Header aplikasi
st.header('Bike Sharing Dashboard')

# Informasi Total, Registered, Casual, Avg Users
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", value=daily_users_df["Total Users"].sum())

with col2:
    st.metric("Registered Users", value=registered_users["Registered Users"].sum())

with col3:
    st.metric("Casual Users", value=casual_users["Casual Users"].sum())

with col4:
    avg_users = round(daily_users_df["Total Users"].mean(), 2)
    st.metric("Rata-rata Users per Hari", value=avg_users)

# Visualisasi 1: Tren Penyewaan Sepeda
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["Date"],
    daily_users_df["Total Users"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)

ax.set_title("Tren Penyewaan Sepeda", fontsize=30, fontweight="bold")
ax.set_xlabel("Periode", fontsize=15)
ax.set_ylabel("Jumlah Penyewa", fontsize=15)
ax.grid(True)

st.pyplot(fig)

# Visualisasi 5: Pie Chart Registered vs Casual Users
fig, ax = plt.subplots()
ax.pie(
    [registered_users["Registered Users"].sum(), casual_users["Casual Users"].sum()],
    labels=["Registered Users", "Casual Users"],
    autopct="%1.1f%%",
    colors=["#90CAF9", "#FFAB91"],
    explode=(0.1, 0),
    shadow=True,
    startangle=5
)
ax.set_title("Registered vs Casual Users", fontsize=14, fontweight="bold")

st.pyplot(fig)

# Visualisasi 2: Penyewaan Berdasarkan Cuaca
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=detail_penyewa_cuaca,
    x="Weather Condition",
    y="Total Users",
    palette=["#344CB7", "#7BC9FF", "#FFAB91"],
    ax=ax
)

ax.set_title("Perbedaan Jumlah Penyewa Sepeda Berdasarkan Kondisi Cuaca", fontsize=25, fontweight="bold")
ax.set_xlabel("Kondisi Cuaca", fontsize=15)
ax.set_ylabel("Jumlah Penyewa (Ribuan)", fontsize=15)
ax.set_ylim(0, detail_penyewa_cuaca["Total Users"].max() * 1.2)

st.pyplot(fig)

# Visualisasi 3: Penyewaan Berdasarkan Musim
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=detail_penyewa_musim,
    x="Season",
    y="Total Users",
    palette=["#344CB7", "#7BC9FF", "#FFAB91", "#FFAB91"],
    ax=ax
)

ax.set_title("Perbedaan Jumlah Penyewa Sepeda Berdasarkan Musim", fontsize=25, fontweight="bold")
ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Jumlah Penyewa (Ribuan)", fontsize=15)
ax.set_ylim(0, detail_penyewa_musim["Total Users"].max() * 1.2)

st.pyplot(fig)

# Visualisasi 4: Tren Penyewaan Sepeda Berdasarkan Jam
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=detail_penyewa_jam,
    x="Hour",
    y="Total Users",
    marker="o",
    color="#344CB7",
    linewidth=2,
    ax=ax
)

ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam", fontsize=14, fontweight="bold")
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewa (Ribuan)", fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)
