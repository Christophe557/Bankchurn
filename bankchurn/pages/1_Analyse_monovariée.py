import matplotlib.pyplot as plt
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list


st.markdown("### 3- Analyse monovariée")
st.markdown("##### Analyse monovariée discrète")


@st.cache_data()
def mono_disc():
    fig, ax = plt.subplots(2, 3, sharey=True, figsize=(15, 6))
    fig.suptitle("ANALYSE MONOVARIEE VARIABLES DISCRETES")
    for i, v in enumerate(disc_list):
        axis = ax[i // 3, i % 3]
        df[v].value_counts(sort=False).plot(
            ax=axis,
            kind="bar",
            color="lightblue",
            edgecolor="black",
            title=v,
        )
        axis.set(xlabel=None)
        axis.set_xticklabels(axis.get_xticklabels(), rotation=0)
        totalvalues = sum([h for h in axis.containers[0].datavalues])
        values = [f"{h*100/totalvalues:.0f}%" for h in axis.containers[0].datavalues]
        axis.bar_label(
            axis.containers[0],
            labels=values,
        )
    fig.tight_layout()

    return fig


# ax[1, 3].remove()
fig1 = mono_disc()
st.pyplot(fig1)

st.markdown("##### Analyse monovariée continue")


@st.cache_data()
def mono_cont():
    fig, ax = plt.subplots(2, 3, figsize=(15, 6))
    fig.suptitle("ANALYSE MONOVARIEE VARIABLES CONTINUES")
    for i, v in enumerate(cont_list):
        bins = 20
        if v == "Tenure":
            bins = 11
        # bins = min(20, df[v].unique().shape[0])
        df[v].plot(
            ax=ax[i // 3, i % 3],
            kind="hist",
            bins=bins,
            color="lightblue",
            edgecolor="black",
            title=v,
        )
        if i % 3 != 0:
            ax[i // 3, i % 3].set(ylabel=None)
    ax[1, 2].remove()
    fig.tight_layout()

    return fig


@st.cache_data()
def mono_cont2():
    fig, ax = plt.subplots(
        2, 5, squeeze=True, figsize=(15, 4), gridspec_kw={"height_ratios": [3, 1]}
    )
    fig.suptitle("ANALYSE MONOVARIEE VARIABLES CONTINUES")
    for i, v in enumerate(cont_list):
        df[v].plot(
            ax=ax[0, i],
            kind="hist",
            bins=20,
            color="lightblue",
            edgecolor="black",
            title=v,
        )
        ax[0, i].set(xlabel=None, xticklabels=[])
        if i > 0:
            ax[0, i].set(ylabel=None)

    for i, v in enumerate(cont_list):
        df[v].plot(
            ax=ax[1, i],
            kind="box",
            vert=False,
            # orientation="horizontal",
            color="black",
        )
        ax[1, i].set(ylabel=None, yticklabels=[])
    fig.tight_layout()
    return fig


fig2 = mono_cont2()
st.pyplot(fig2)
