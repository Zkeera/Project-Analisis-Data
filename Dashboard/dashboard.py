import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/Zkeera/Project-Analisis-Data/refs/heads/main/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/Zkeera/Project-Analisis-Data/refs/heads/main/hour.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar menu (Menghapus 'Penyewaan per Jam')
with st.sidebar:
    selected = option_menu('Dashboard Menu', ['Home', 'Cuaca vs Penyewaan', 'Hari Kerja vs Akhir Pekan'],
                          icons=['house', 'cloud-sun', 'calendar'], menu_icon='menu-app', default_index=0)

st.title('🚴‍♂️ Dashboard Analisis Penyewaan Sepeda')
st.markdown('### 📊 Data penyewaan sepeda berdasarkan cuaca dan hari.')

if selected == 'Cuaca vs Penyewaan':
    st.header('🌦️ Pengaruh Cuaca Terhadap Penyewaan Sepeda')
    weather_avg = day_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    weather_avg['weathersit'] = weather_avg['weathersit'].map(weather_labels)
    
    fig, ax = plt.subplots()
    sns.barplot(data=weather_avg, x='weathersit', y='cnt', ax=ax, palette='coolwarm')
    ax.set_title('Rata-rata Penyewaan Berdasarkan Cuaca')
    st.pyplot(fig)
    
    # Tambahan keterangan analisis
    st.markdown("""
    **Hasil Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda**
    - Cuaca cerah atau sedikit berawan memiliki rata-rata penyewaan tertinggi (±4877 sepeda).
    - Cuaca mendung sedikit lebih rendah (±4036 sepeda).
    - Hujan ringan atau salju ringan secara signifikan menurunkan penyewaan (±1803 sepeda).
    - Tidak ada data untuk kondisi hujan lebat atau badai (kategori 4).
    """)

elif selected == 'Hari Kerja vs Akhir Pekan':
    st.header('📅 Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan')
    day_df['is_weekend'] = day_df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
    weekend_avg = day_df.groupby('is_weekend')['cnt'].mean().reset_index()
    weekend_avg['is_weekend'] = weekend_avg['is_weekend'].map({0: 'Hari Kerja', 1: 'Akhir Pekan'})
    
    fig, ax = plt.subplots()
    sns.barplot(data=weekend_avg, x='is_weekend', y='cnt', ax=ax, palette='viridis')
    ax.set_title('Rata-rata Penyewaan Berdasarkan Jenis Hari')
    st.pyplot(fig)
    
    # Tambahan keterangan analisis
    st.markdown("""
    **Hasil Analisis Penyewaan Sepeda: Hari Kerja vs Akhir Pekan**
    - Hari kerja memiliki rata-rata penyewaan sedikit lebih tinggi (±4551 sepeda) 
      dibandingkan dengan akhir pekan (±4390 sepeda).
    - Perbedaannya tidak terlalu signifikan, namun menunjukkan tren sedikit lebih ramai saat hari kerja.
    """)
