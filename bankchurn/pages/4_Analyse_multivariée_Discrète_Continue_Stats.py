import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.markdown("##### Statistiques : Analyse multivariée discrète / continue")


@st.cache_data()
def multi_disc_cont_stat():
    fig, ax = plt.subplots(len(cont_list), len(disc_list), figsize=(15, 15))
    fig.suptitle(
        "ANALYSES MULTIVARIEE DISCRETE/CONTINUE 2 à 2\nStatistique par catégorie"
    )
    for i, v in enumerate(cont_list):
        for j, w in enumerate(disc_list):
            sns.boxplot(
                ax=ax[i, j],
                data=df,
                x=w,
                y=v,
                hue=w,
                palette="Set2",
                legend=False,
            )

            if i != 0 and i != len(cont_list) - 1:
                ax[i, j].set(xlabel=None, xticklabels=[])
            if j != 0 and j != len(disc_list) - 1:
                ax[i, j].set(ylabel=None, yticklabels=[])

            if i == 0:
                ax[i, j].xaxis.tick_top()
                ax[i, j].xaxis.set_label_position("top")
            if i == len(cont_list) - 1:
                ax[i, j].xaxis.tick_bottom()
                ax[i, j].xaxis.set_label_position("bottom")

            if j == 0:
                ax[i, j].yaxis.tick_left()
                ax[i, j].yaxis.set_label_position("left")
            if j == len(disc_list) - 1:
                ax[i, j].yaxis.tick_right()
                ax[i, j].yaxis.set_label_position("right")

    return fig


fig6 = multi_disc_cont_stat()
st.pyplot(fig6)
