import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('https://raw.githubusercontent.com/Zkeera/Project-Analisis-Data/refs/heads/main/Data/day.csv')
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return day_df

day_df = load_data()

# Sidebar menu
with st.sidebar:
    selected = option_menu('Dashboard Menu', ['Home', 'Cuaca vs Penyewaan', 'Hari Kerja vs Akhir Pekan'],
                          icons=['house', 'cloud-sun', 'calendar'], menu_icon='menu-app', default_index=0)

st.title('🚴‍♂️ Dashboard Analisis Penyewaan Sepeda')
st.markdown('### 📊 Data penyewaan sepeda berdasarkan cuaca dan hari.')

# Fitur interaktif: Filtering berdasarkan tanggal dan musim
st.sidebar.subheader("Filter Data")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [day_df['dteday'].min(), day_df['dteday'].max()])
season_filter = st.sidebar.multiselect("Pilih Musim", options=[1, 2, 3, 4], default=[1, 2, 3, 4],
                                       format_func=lambda x: {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}[x])

# Filter data berdasarkan input
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(date_range[0])) & (day_df['dteday'] <= pd.to_datetime(date_range[1])) & (day_df['season'].isin(season_filter))]

if selected == 'Cuaca vs Penyewaan':
    st.header('🌦️ Pengaruh Cuaca Terhadap Penyewaan Sepeda')
    weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
    weather_avg['weathersit'] = weather_avg['weathersit'].map(weather_labels)
    
    fig, ax = plt.subplots()
    sns.barplot(data=weather_avg, x='weathersit', y='cnt', ax=ax, palette='coolwarm')
    ax.set_title('Rata-rata Penyewaan Berdasarkan Cuaca')
    st.pyplot(fig)
    
    st.markdown("""
    **Hasil Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda**
    - Cuaca cerah atau sedikit berawan memiliki rata-rata penyewaan tertinggi.
    - Cuaca mendung sedikit lebih rendah.
    - Hujan ringan atau salju ringan secara signifikan menurunkan penyewaan.
    - Tidak ada data untuk kondisi hujan lebat atau badai.
    """)

elif selected == 'Hari Kerja vs Akhir Pekan':
    st.header('📅 Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan')
    filtered_df['is_weekend'] = filtered_df['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
    weekend_avg = filtered_df.groupby('is_weekend')['cnt'].mean().reset_index()
    weekend_avg['is_weekend'] = weekend_avg['is_weekend'].map({0: 'Hari Kerja', 1: 'Akhir Pekan'})
    
    fig, ax = plt.subplots()
    sns.barplot(data=weekend_avg, x='is_weekend', y='cnt', ax=ax, palette='viridis')
    ax.set_title('Rata-rata Penyewaan Berdasarkan Jenis Hari')
    st.pyplot(fig)
    
    st.markdown("""
    **Hasil Analisis Penyewaan Sepeda: Hari Kerja vs Akhir Pekan**
    - Hari kerja memiliki rata-rata penyewaan sedikit lebih tinggi dibandingkan dengan akhir pekan.
    - Perbedaannya tidak terlalu signifikan, namun menunjukkan tren sedikit lebih ramai saat hari kerja.
    """)
