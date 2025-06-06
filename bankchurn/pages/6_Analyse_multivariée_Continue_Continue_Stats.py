import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.markdown("##### Nuages de points : Analyse multivariée continue / continue")


@st.cache_data()
def multi_cont_cont():
    sns.set(font_scale=0.6)
    fig, ax = plt.subplots(5, 5, figsize=(15, 15))
    fig.suptitle("ANALYSES MULTIVARIEE CONTINUE/CONTINUE 2 à 2\nNuages de points")
    for i, v in enumerate(cont_list):
        for j, w in enumerate(cont_list):
            sns.scatterplot(
                ax=ax[i, j],
                data=df,
                x=w,
                y=v,
                hue="Exited",
                palette="Set2",
                alpha=0.5,
                legend=i + j == 0,
                s=5,
            )

            if i != 0 and i != len(cont_list) - 1:
                ax[i, j].set(xlabel=None, xticklabels=[])
            if j != 0 and j != len(cont_list) - 1:
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
            if j == len(cont_list) - 1:
                ax[i, j].yaxis.tick_right()
                ax[i, j].yaxis.set_label_position("right")
    return fig


fig7 = multi_cont_cont()
st.pyplot(fig7)
