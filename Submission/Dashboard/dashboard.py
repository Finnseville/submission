import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state")["customer_id"].nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bystate_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city")["customer_id"].nunique().reset_index()
    bycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bycity_df

main_df = pd.read_csv("main_data.csv")
bystate_df = create_bystate_df(main_df)
bycity_df = create_bycity_df(main_df)

st.header('Customer Data:sparkles:')

with st.sidebar:
    st.write("Filters")
    kategori_data = st.radio(
        "Jenis kategori",
        ("Berdasarkan Negara", "Berdasarkan Kota")
    )

    visualisasi = st.radio(  
        "Jenis visualisasi",
        ("Diagram Batang", "Pie Chart")
    )

if kategori_data == "Berdasarkan Negara":
    top_10_states = bystate_df.nlargest(10, "customer_count")

    if visualisasi == "Diagram Batang":
        fig, ax = plt.subplots(figsize=(20, 10))
        colors = ["#90CAF9"] + ["#D3D3D3"] * (len(top_10_states) - 1)
        sns.barplot(
            x="customer_count",
            y="customer_state",
            data=top_10_states,
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of customers by State (Diagram Batang)", loc="center", fontsize=30)
        st.pyplot(fig)

    elif visualisasi == "Pie Chart":
        fig, ax = plt.subplots(figsize=(10, 10))
        top_10_states.set_index("customer_state", inplace=True)
        top_10_states["customer_count"].plot.pie(
            autopct="%1.1f%%",
            startangle=90,
            ax=ax
        )
        ax.set_title("Number of customers by State (Pie Chart)", loc="center", fontsize=30)
        ax.set_ylabel(None)
        st.pyplot(fig)

elif kategori_data == "Berdasarkan Kota":
    top_10_cities = bycity_df.nlargest(10, "customer_count")

    if visualisasi == "Diagram Batang":
        fig, ax = plt.subplots(figsize=(20, 10))
        colors = ["#90CAF9"] + ["#D3D3D3"] * (len(top_10_cities) - 1)
        sns.barplot(
            x="customer_count",
            y="customer_city",
            data=top_10_cities,
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of customers by City (Diagram Batang)", loc="center", fontsize=30)
        st.pyplot(fig)

    elif visualisasi == "Pie Chart":
        fig, ax = plt.subplots(figsize=(10, 10))
        top_10_cities.set_index("customer_city", inplace=True)
        top_10_cities["customer_count"].plot.pie( 
            autopct="%1.1f%%",
            startangle=90,
            ax=ax
        )
        ax.set_title("Number of customers by City (Pie Chart)", loc="center", fontsize=30)
        ax.set_ylabel(None)
        st.pyplot(fig)

st.write(bycity_df)