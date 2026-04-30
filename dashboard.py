import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==============================
# Konfigurasi Halaman Streamlit
# ==============================
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# ==============================
# Helper Functions
# ==============================
@st.cache_data
def load_data():
    # Memuat data bersih
    df_day = pd.read_csv("day_clean.csv")
    df_hour = pd.read_csv("hour_clean.csv")
    
    # Memastikan format datetime
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    return df_day, df_hour

def temp_cluster(temp):
    if temp < 12.3:
        return 'Cold'
    elif temp < 24.6:
        return 'Moderate'
    else:
        return 'Warm'

# Load data
df_day, df_hour = load_data()

# ==============================
# Komponen Interaktif: Sidebar
# ==============================
with st.sidebar:
    st.title("🚲 Filter Data")
    st.markdown("Gunakan opsi di bawah ini untuk memfilter data pada dashboard.")
    
    # 1. Filter Rentang Waktu (Date Input)
    min_date = df_day['dteday'].min().date()
    max_date = df_day['dteday'].max().date()
    
    date_range = st.date_input(
        label="Pilih Rentang Waktu:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Mengamankan input jika pengguna hanya memilih 1 tanggal
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
        
    st.markdown("---")
    
    # 2. Filter Kategori Cuaca (Multiselect)
    weather_options = ['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Light Rain', 'Heavy Rain/Snow Fog']
    selected_weather = st.multiselect(
        label="Pilih Kondisi Cuaca:",
        options=weather_options,
        default=weather_options # Default menampilkan semua cuaca
    )

# ==============================
# Menerapkan Filter ke Dataframe
# ==============================
# Dataframe ini akan berubah dinamis sesuai input pengguna di sidebar
filtered_day = df_day[
    (df_day['dteday'].dt.date >= start_date) & 
    (df_day['dteday'].dt.date <= end_date) &
    (df_day['weathersit'].isin(selected_weather))
]

filtered_hour = df_hour[
    (df_hour['dteday'].dt.date >= start_date) & 
    (df_hour['dteday'].dt.date <= end_date) &
    (df_hour['weathersit'].isin(selected_weather))
]

# ==============================
# Tampilan Dashboard Utama
# ==============================
st.title("🚲 Bike Sharing Data Analytics Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis penyewaan sepeda secara interaktif. Silakan gunakan menu filter di sebelah kiri untuk menyesuaikan visualisasi.")

st.markdown("---")

# ==============================
# Bagian 1: Analisis Cuaca (Pertanyaan Bisnis 1)
# ==============================
st.header("1. Dampak Cuaca terhadap Total Penyewaan")

# Persiapan Data (Menggunakan filtered_day)
weather_analysis = filtered_day.groupby('weathersit')['cnt'].mean().reset_index()
weather_analysis = weather_analysis.sort_values(by='cnt', ascending=False)

# Cek apakah data kosong setelah difilter
if weather_analysis.empty:
    st.warning("Data tidak tersedia untuk kombinasi filter ini. Silakan sesuaikan filter di sidebar.")
else:
    # Visualisasi
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='weathersit',
        y='cnt',
        data=weather_analysis,
        palette='viridis',
        hue='weathersit',
        legend=False,
        ax=ax1
    )
    # Judul grafik dibuat dinamis
    ax1.set_title(f'Rata-rata Penyewaan Sepeda ({start_date.strftime("%b %Y")} - {end_date.strftime("%b %Y")})', fontsize=15)
    ax1.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax1.set_ylabel('Rata-rata Jumlah Sewa (cnt)', fontsize=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig1)
    
    with st.expander("Lihat Penjelasan"):
        st.write("Visualisasi ini menunjukkan bahwa rata-rata jumlah penyewaan sepeda menurun drastis seiring dengan memburuknya cuaca.")

st.markdown("---")

# ==============================
# Bagian 2: Tren Jam Sibuk (Pertanyaan Bisnis 2)
# ==============================
st.header("2. Tren Penyewaan Pengguna Terdaftar pada Hari Kerja")

# Persiapan Data (Menggunakan filtered_hour)
df_workingday = filtered_hour[filtered_hour['workingday'] == 'Workingday'].copy()

if df_workingday.empty:
    st.warning("Data hari kerja tidak tersedia untuk kombinasi filter ini.")
else:
    workingday_hourly = df_workingday.groupby('hr')['registered'].mean().reset_index()
    
    # Menghitung metrik dinamis
    morning_rush = df_workingday[(df_workingday['hr'] >= 7) & (df_workingday['hr'] <= 9)]
    evening_rush = df_workingday[(df_workingday['hr'] >= 16) & (df_workingday['hr'] <= 18)]
    
    # Pengamanan jika rata-rata bernilai NaN
    avg_morning = morning_rush['registered'].mean() if not morning_rush.empty else 0
    avg_evening = evening_rush['registered'].mean() if not evening_rush.empty else 0
    
    # Menampilkan metrik
    col1, col2 = st.columns(2)
    col1.metric("Rata-rata Jam Sibuk Pagi (07:00-09:00)", f"{avg_morning:.2f} Penyewa")
    col2.metric("Rata-rata Jam Sibuk Sore (16:00-18:00)", f"{avg_evening:.2f} Penyewa")
    
    # Visualisasi
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x='hr',
        y='registered',
        data=workingday_hourly,
        marker='o',
        color='tab:blue',
        linewidth=2.5,
        ax=ax2
    )
    
    # Highlight jam sibuk
    ax2.axvspan(7, 9, color='orange', alpha=0.2, label='Jam Sibuk Pagi')
    ax2.axvspan(16, 18, color='red', alpha=0.2, label='Jam Sibuk Sore')
    
    ax2.set_title('Tren Penyewaan Pengguna Terdaftar pada Hari Kerja', fontsize=15)
    ax2.set_xlabel('Jam (0-23)', fontsize=12)
    ax2.set_ylabel('Rata-rata Penyewa Terdaftar', fontsize=12)
    ax2.set_xticks(range(0, 24))
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    st.pyplot(fig2)

st.markdown("---")

# ==============================
# Bagian 3: Analisis Lanjutan (Clustering Suhu)
# ==============================
st.header("3. Pengaruh Suhu terhadap Tren Penyewaan di Jam Sibuk (Analisis Lanjutan)")

if not df_workingday.empty:
    # Persiapan Data (Binning)
    df_workingday['temp_category'] = df_workingday['temp'].apply(temp_cluster)
    
    # Mengatur urutan kategori agar rapi di legenda
    df_workingday['temp_category'] = pd.Categorical(
        df_workingday['temp_category'], 
        categories=['Cold', 'Moderate', 'Warm'], 
        ordered=True
    )
    
    workingday_hourly_temp = df_workingday.groupby(['hr', 'temp_category'], observed=True)['registered'].mean().reset_index()
    
    # Cek apakah data setelah grouping tidak kosong
    if not workingday_hourly_temp.empty:
        # Visualisasi
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            x='hr',
            y='registered',
            hue='temp_category',
            data=workingday_hourly_temp,
            marker='o',
            palette=['#4fc3f7', '#aed581', '#ff8a65'], # Biru, Hijau, Oranye
            linewidth=2.5,
            ax=ax3
        )
        
        # Highlight jam sibuk
        ax3.axvspan(7, 9, color='orange', alpha=0.2, label='Jam Sibuk Pagi')
        ax3.axvspan(16, 18, color='red', alpha=0.2, label='Jam Sibuk Sore')
        
        ax3.set_title('Tren Penyewaan Berdasarkan Suhu di Hari Kerja', fontsize=15)
        ax3.set_xlabel('Jam (0-23)', fontsize=12)
        ax3.set_ylabel('Rata-rata Penyewa Terdaftar', fontsize=12)
        ax3.set_xticks(range(0, 24))
        
        ax3.legend(title='Keterangan', loc='upper left', bbox_to_anchor=(1, 1))
        ax3.grid(True, linestyle=':', alpha=0.6)
        
        st.pyplot(fig3)
        
        with st.expander("Lihat Penjelasan Lanjutan"):
            st.write("Hasil clustering sederhana (binning) memperlihatkan bahwa suhu **Cold** secara konsisten menekan volume penyewaan di bawah rata-rata sepanjang hari. Sebaliknya, saat suhu berada di kategori **Moderate** dan **Warm**, terjadi lonjakan penyewaan komuter yang signifikan.")

st.caption("Copyright © 2026 - Data Analytics Project")
