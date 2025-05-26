import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.markdown("### 4- Analyse multivariée")
st.markdown("##### Analyse multivariée discrète / discrète")


@st.cache_data()
def multi_disc_disc():
    sns.set(font_scale=0.8)
    fig, ax = plt.subplots(len(disc_list) - 1, len(disc_list) - 1, figsize=(15, 15))
    fig.suptitle("HEATMAP ANALYSE MULTIVARIEE DISCRETE/DISCRETE 2 à 2")
    for i, v in enumerate(disc_list[:-1]):
        for j, w in enumerate(disc_list[:-1]):
            crtab = pd.crosstab(df[v], df[w], normalize=True)
            mask = crtab[(crtab == 0.0)].replace(0.0, True)
            sns.heatmap(
                ax=ax[i, j],
                data=crtab,
                mask=mask,
                annot=True,
                annot_kws={"size": 10},
                vmin=0,
                vmax=0.5,
                fmt=".1%",
                linewidth=2,
                linecolor="white",
                square=False,
                cbar=False,
                cmap="Oranges",
            )

            if i != 0 and i != len(disc_list) - 2:
                ax[i, j].set(xlabel=None, xticklabels=[])
            if j != 0 and j != len(disc_list) - 2:
                ax[i, j].set(ylabel=None, yticklabels=[])

            if i == 0:
                ax[i, j].xaxis.tick_top()
                ax[i, j].xaxis.set_label_position("top")
            if i == len(disc_list) - 2:
                ax[i, j].xaxis.tick_bottom()
                ax[i, j].xaxis.set_label_position("bottom")

            if j == 0:
                ax[i, j].yaxis.tick_left()
                ax[i, j].yaxis.set_label_position("left")
            if j == len(disc_list) - 2:
                ax[i, j].yaxis.tick_right()
                ax[i, j].yaxis.set_label_position("right")
    return fig


fig3 = multi_disc_disc()
st.pyplot(fig3)


@st.cache_data()
def multi_disc_y():
    st.markdown("##### Analyse multivariée discrète / étiquette y")
    fig, ax = plt.subplots(1, len(disc_list) - 1, figsize=(20, 4))
    fig.suptitle("HEATMAP CORRELATION VARIABLES DISCRETE / ETIQUETTE Y")
    for i, v in enumerate(disc_list[:-1]):
        sns.heatmap(
            ax=ax[i],
            data=pd.crosstab(df[disc_list[-1]], df[v], normalize=True),
            annot=True,
            annot_kws={"size": 10},
            vmin=0,
            vmax=0.5,
            fmt=".1%",
            yticklabels=((i == 0) | (i == len(disc_list) - 2)),
            linewidth=2,
            linecolor="white",
            square=False,
            cbar=False,
            cmap="Oranges",
        )

        if i != 0 and i != len(disc_list) - 2:
            ax[i].set(ylabel=None)

        if i == 0:
            ax[i].yaxis.tick_left()
            ax[i].yaxis.set_label_position("left")
        if i == len(disc_list) - 2:
            ax[i].yaxis.tick_right()
            ax[i].yaxis.set_label_position("right")
    return fig


fig4 = multi_disc_y()
st.pyplot(fig4)
