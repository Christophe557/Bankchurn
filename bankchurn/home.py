import os
import io
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


projectpath = os.path.abspath(os.path.dirname(__file__))
# Configurer la mise en page de la page Streamlit pour qu'elle soit large
st.set_page_config(layout="wide")

# Titre principal de l'application
st.title("Projet Kaggle/Bank churn")
st.subheader("Exploratory Data Analysis")


@st.cache_data(ttl=60)
def load_data(filename: str) -> pd.DataFrame:
    """Load dataset from the file in dataset directory

    Args:
        filename (str): name of the file

    Returns:
        pd.DataFrame: dataframe data
    """
    data = pd.read_csv(os.path.join(projectpath, "dataset", filename))
    return data


def variables_list_initialization():
    """initialization of :
    dataset : session_df
    list of discret variables : session_disc_list
    list of continuous variables : session_cont_list
    """
    if "session_df" not in st.session_state:
        st.session_state.session_df = load_data("train_data.csv")
    if "session_disc_list" not in st.session_state:
        st.session_state.session_disc_list = [
            "NumOfProducts",
            "Geography",
            "Gender",
            "HasCrCard",
            "IsActiveMember",
            "Exited",
        ]
    if "session_cont_list" not in st.session_state:
        st.session_state.session_cont_list = [
            "CreditScore",
            "Age",
            "Tenure",
            "Balance",
            "EstimatedSalary",
        ]


variables_list_initialization()

df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list


# -----------------------------------------------------------------------------------
st.markdown("### 1- Généralités")
st.markdown("##### Dataset (5 premières lignes)")

st.dataframe(df.head())

st.markdown("##### Lignes / colonnes : ")
st.write(df.shape)

st.markdown("##### Infomations :")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())
