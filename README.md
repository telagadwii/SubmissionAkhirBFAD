# 🚲 Bike Sharing Data Analytics Dashboard

## 📌 Project Overview
Proyek ini merupakan portofolio analisis data yang berfokus pada evaluasi performa sistem *Bike Sharing* di Washington D.C. Dashboard interaktif ini dibangun menggunakan **Streamlit** untuk memvisualisasikan temuan dari *Exploratory Data Analysis* (EDA) serta analisis lanjutan berbasis *clustering* (binning) suhu.

🔗 **Live Dashboard:** [Kunjungi Dashboard di Streamlit Cloud](https://dashboard-punya-telaga.streamlit.app/) 

## ❓ Business Questions
Analisis dalam proyek ini dirancang secara spesifik untuk menjawab dua pertanyaan bisnis berikut:
1. Bagaimana penurunan rata-rata jumlah penyewaan sepeda pada hari dengan kondisi cuaca buruk dibandingkan dengan cuaca cerah selama tahun 2012 di Washington D.C.?
2. Berapa rata-rata volume penyewaan pengguna terdaftar pada jam sibuk pagi (07:00-09:00) dan sore (16:00-18:00) di hari kerja selama tahun 2011-2012?

## 📊 Key Insights
* **Sensitivitas Cuaca:** Terdapat korelasi negatif yang ekstrem antara cuaca buruk dan jumlah penyewaan. Pada tahun 2012, rata-rata penyewaan harian turun drastis dari 6.003 (saat cuaca cerah) menjadi hanya 2.126 (saat hujan/salju).
* **Pola Komuter Bimodal:** Pengguna terdaftar (*registered*) menjadikan sepeda sebagai moda transportasi komuter harian dengan lonjakan tertinggi terjadi pada jam sibuk sore (16:00-18:00) yang mengungguli jam sibuk pagi (07:00-09:00).
* **Pengaruh Suhu pada Jam Sibuk:** Analisis *clustering* menunjukkan bahwa volume penyewaan di jam sibuk tertahan secara signifikan ketika suhu udara berada di kategori *Cold* (< 12.3°C), sementara kategori *Moderate* dan *Warm* memicu lonjakan penyewaan tertinggi.

## 📂 File Structures
```text
/bike-sharing-dashboard
│
├── dashboard.py         # Skrip utama untuk aplikasi Streamlit
├── day_clean.csv        # Dataset agregasi harian (sudah dibersihkan)
├── hour_clean.csv       # Dataset agregasi per jam (sudah dibersihkan)
├── requirements.txt     # Daftar library Python yang dibutuhkan
└── README.md            # Dokumentasi proyek ini
