import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list


st.markdown("##### Comptage par catégorie : Analyse multivariée discrète / continue")


@st.cache_data()
def multi_disc_cont_count():
    sns.set(font_scale=0.6)
    fig, ax = plt.subplots(len(disc_list), len(cont_list), figsize=(15, 15))
    fig.suptitle("ANALYSES MULTIVARIEE DISCRETE/CONTINUE 2 à 2\nComptage par catégorie")
    for i, v in enumerate(disc_list):
        for j, w in enumerate(cont_list):
            sns.histplot(
                ax=ax[i, j],
                data=df,
                stat="count",
                multiple="stack",
                x=w,
                hue=v,
                palette="Set2",
                element="bars",
                bins=20,
                legend=j == 0,
            )

            if i != 0 and i != len(disc_list) - 1:
                ax[i, j].set(xlabel=None, xticklabels=[])
            if j != 0 and j != len(cont_list) - 1:
                ax[i, j].set(ylabel=None, yticklabels=[])

            if i == 0:
                ax[i, j].xaxis.tick_top()
                ax[i, j].xaxis.set_label_position("top")
            if i == len(disc_list) - 1:
                ax[i, j].xaxis.tick_bottom()
                ax[i, j].xaxis.set_label_position("bottom")

            if j == 0:
                ax[i, j].yaxis.set_label_text(f"{v} count")
                ax[i, j].yaxis.tick_left()
                ax[i, j].yaxis.set_label_position("left")
            if j == len(cont_list) - 1:
                ax[i, j].yaxis.tick_right()
                ax[i, j].yaxis.set_label_position("right")

    return fig


fig5 = multi_disc_cont_count()
st.pyplot(fig5)
