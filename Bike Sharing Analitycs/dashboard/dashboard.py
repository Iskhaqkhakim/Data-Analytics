import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Fungsi untuk memuat data
def load_data():
    # Gantilah dengan path file Anda
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    # Rename columns dan preprocessing lainnya
    day_df.rename(columns={'yr': 'year', 'mnth': 'month', 'weekday': 'one_of_week', 'weathersit': 'weather_situation', 
                            'windspeed': 'wind_speed', 'cnt': 'count_cr', 'hum': 'humidity'}, inplace=True)
    hour_df.rename(columns={'yr': 'year', 'hr': 'hours', 'mnth': 'month', 'weekday': 'one_of_week', 
                             'weathersit': 'weather_situation', 'windspeed': 'wind_speed', 'cnt': 'count_cr', 
                             'hum': 'humidity'}, inplace=True)

    # Season, month, weather, dan hari diterjemahkan
    day_df.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
    hour_df.season.replace((1, 2, 3, 4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
    day_df.month.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 
                         ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), inplace=True)
    hour_df.month.replace((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 
                          ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), inplace=True)
    day_df.weather_situation.replace((1, 2, 3, 4), ('Clear', 'Misty', 'Light_rainsnow', 'Heavy_rainsnow'), inplace=True)
    hour_df.weather_situation.replace((1, 2, 3, 4), ('Clear', 'Misty', 'Light_rainsnow', 'Heavy_rainsnow'), inplace=True)
    day_df.one_of_week.replace((0, 1, 2, 3, 4, 5, 6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)
    hour_df.one_of_week.replace((0, 1, 2, 3, 4, 5, 6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)
    day_df.year.replace((0, 1), ('2011', '2012'), inplace=True)
    hour_df.year.replace((0, 1), ('2011', '2012'), inplace=True)
    day_df['humidity'] = day_df['humidity'] * 100
    hour_df['humidity'] = hour_df['humidity'] * 100

    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# Dashboard Streamlit
st.title("Dashboard Penyewaan Sepeda")

# Menampilkan data berdasarkan rentang waktu yang dipilih
st.header("Pilih Rentang Waktu untuk Data Penyewaan Sepeda")

# Menambahkan selector untuk memilih rentang tanggal
start_date = st.date_input(
    "Pilih Tanggal Mulai:", 
    value=day_df['dteday'].min(),  # Default ke tanggal awal dataset
    min_value=day_df['dteday'].min(), 
    max_value=day_df['dteday'].max()
)
end_date = st.date_input(
    "Pilih Tanggal Selesai:", 
    value=day_df['dteday'].max(),  # Default ke tanggal akhir dataset
    min_value=day_df['dteday'].min(), 
    max_value=day_df['dteday'].max()
)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan grafik jumlah penyewaan sepeda berdasarkan rentang tanggal yang dipilih
st.subheader(f"Grafik Penyewaan Sepeda pada Rentang Tanggal {start_date} hingga {end_date}")
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(x="dteday", y="count_cr", data=filtered_day_df, ax=ax, marker='o', color='b')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title(f"Penyewaan Sepeda pada Rentang Tanggal {start_date} hingga {end_date}")
st.pyplot(fig)

# Tombol untuk menampilkan grafik analisis berdasarkan musim
sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()

# Grafik Penyewaan Sepeda Terbanyak dan Terdikit Berdasarkan Jam
st.header("Jam dengan Penyewaan Sepeda Terbanyak dan Terdikit")

# Barplot Jam dengan Penyewaan Terbanyak
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette="Blues", ax=ax1)
ax1.set_xlabel("Jam")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.set_title("Jam dengan Penyewaan Sepeda Terbanyak")
st.pyplot(fig1)

# Barplot Jam dengan Penyewaan Terdikit
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette="Reds", ax=ax2)
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")
ax2.set_title("Jam dengan Penyewaan Sepeda Terdikit")
st.pyplot(fig2)

with st.expander("Keterangan"):
    st.write(
        """Berdasarkan gambar di atas, dapat dilihat bahwa penyewaan sepeda paling banyak terjadi pada pukul 17:00 dengan sekitar 336.860 penyewaan. Sebaliknya, penyewaan sepeda paling sedikit terjadi pada pukul 04:00, dengan hanya sekitar 4.428 penyewaan. """
    )
# Grafik Penyewaan Sepeda Berdasarkan Musim
st.subheader("Penyewaan Sepeda Berdasarkan Musim")

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="count_cr", data=day_df, palette="Set2", ax=ax3)
ax3.set_xlabel("Musim")
ax3.set_ylabel("Jumlah Penyewaan")
ax3.set_title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig3)

with st.expander("Keterangan"):
    st.write(
        """ Berdasarkan gambar di atas, dapat dilihat bahwa musim dengan jumlah penyewaan terbanyak adalah musim Fall (musim gugur), dengan total penyewaan mencapai 1.061.129 penyewaan."""
    )
    
