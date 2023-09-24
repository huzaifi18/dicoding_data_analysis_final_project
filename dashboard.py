import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

all_df = pd.read_csv("all_data.csv")
all_df["date"] = pd.to_datetime(all_df["date"])
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)
min_date = all_df["date"].min()
max_date = all_df["date"].max()
 
st.set_page_config(layout="wide")
st.title('Dashboard Kualitas Udara')
st.markdown(
            """
            By Huzaifi Hafizhahullah
            """
            )
cols1, cols2, cols3 = st.columns([2, 1, 1])
my_expander = st.expander("Expand", expanded=True)
with my_expander:
    with cols1:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    with cols2:
        selected_reference = st.selectbox(
        label="Referensi Waktu",
        options=('Tahun', 'Hari', "Jam"),
        placeholder="Pilih satuan waktu..."
        )

    with cols3:
        selected_station = st.selectbox(
        label="Station",
        options=('Semua','Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
        'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan',
        'Wanliu', 'Wanshouxigong'),
        )

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

def plot_polutan(df, reference):
    for i in polutan:    
        fig, ax=plt.subplots(figsize=(15, 5))
        sns.pointplot(x=reference, y=i, data=df, hue="station", errorbar=None, ax=ax, palette=sns.color_palette("Paired")[:13])
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.ylabel(rf"{i} ($\mu g/m^{3}$", fontsize=10)
        plt.title(f"Tingkat {i} Rata-Rata")
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        st.pyplot(fig)

def plot_station_a_year(df):
    df_=df
    for i in polutan:
        fig, ax=plt.subplots(figsize=(10, 5))
        sns.barplot(
            y="station",
            x=i,
            data= df_.sort_values(by=i, ascending=False),
            palette=colors_,
            errorbar=None
        )
        plt.title(f"Tingkat {i} untuk Setiap Station", loc="center", fontsize=15)
        plt.xlabel(rf"{i} ($\mu g/m^{3}$)",fontsize=15)
        plt.ylabel(None)
        st.pyplot(fig)
    print(df_.sort_values(by=i, ascending=False))

def air_quality_station_maker(df):
    _station_air_quality = {}
    for stations in df.station.unique():
        air_quality_count = (df[df['station']==stations]
                            .air_quality
                            .value_counts())
        air_quality_sum = (df[df['station']==stations]
                        .air_quality
                        .value_counts()
                        .sum())
        percentage = air_quality_count / air_quality_sum * 100
        _station_air_quality[stations] = percentage.reset_index().rename(columns={'air_quality': 'percentage', "index":"air_quality"})
    return _station_air_quality
        

def air_quality_status(df):
    station_air_quality = air_quality_station_maker(df)

    fig, ax=plt.subplots(figsize=(10, 5))
    colours = {'Good': '#77DD77',
           'Moderate': '#80e2FF',
           'Unhealthy': '#FFD700',
           'Very Unhealthy': '#FF6F61',
           'Hazardous':'#C23B22'
           }    
    try:
        labels = station_air_quality[selected_station]["percentage"].sort_values()
        ax = plt.pie(station_air_quality[selected_station]["count"],
                    labels=labels,
                    autopct='%1.1f%%',
                    pctdistance=1.14,
                    labeldistance=1.3,
                    startangle=140,
                    explode=(station_air_quality[selected_station]["count"] == station_air_quality[selected_station]["count"].max())*0.1,
                    colors=[colours[key] for key in labels])
        plt.legend(station_air_quality[selected_station]["percentage"].sort_values(), bbox_to_anchor=(1,0.72), loc="lower right", 
                                bbox_transform=plt.gcf().transFigure)
        st.pyplot(fig)
    except Exception as e:
        st.markdown(
                    """
                    Silakan tentukan station yang ingin Anda lihat
                    """
                    )

def good_air_quality_comparison(df):
    station_air_quality = air_quality_station_maker(df)
    extract_pct = [[pct for pct in station_air_quality[station]["count"]] for station in df.station.unique()]

    air_quality_segmented = pd.DataFrame(extract_pct,
                                    columns=df.air_quality.unique())
    air_quality_segmented["station"] = df.station.unique()

    try:
        fig, ax=plt.subplots(figsize=(10, 5))
        sns.barplot(
            y="Good",
            x="station",
            data=air_quality_segmented.sort_values(by="Good", ascending=False),
            palette=_colors)
        plt.xticks(rotation=45)
        plt.ylabel(None)
        plt.xlabel(None)
        plt.tick_params(axis='x', labelsize=12)
        st.pyplot(fig)
    except Exception as e:
        st.markdown(
            """
            Terjadi Kesalahan
            """
            )

polutan = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
_colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_ = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
reference_dict = {
    'Tahun':"year",
    'Hari':'day_name',
    "Jam":'hour'
}


col1, col2 = st.columns([2, 1])

with col1:
    st.header("Tren Tingkat Polutan Dalam Waktu")
    with st.container():
        if start_date.year == end_date.year and selected_reference == "Tahun":
            plot_station_a_year(all_df[all_df['year']==int(start_date.year)])

        elif selected_station == 'Semua':
            plot_polutan(main_df, reference_dict[selected_reference])

        else:
            plot_polutan(main_df[main_df['station']==selected_station], reference_dict[selected_reference])

with col2:
    st.header('Kategori Kualitas Udara Berdasarkan Kandungan PM2.5')
    air_quality_status(main_df)
    st.header('Perbandingan Persentase Kualitas Udara \"Good\" ')
    good_air_quality_comparison(main_df)