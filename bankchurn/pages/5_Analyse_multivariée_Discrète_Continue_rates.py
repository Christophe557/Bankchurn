import matplotlib.axes
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from home import variables_list_initialization

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.markdown(
    "##### Ratio de la variable discrète (uniquement 2 catégories) selon la distribution de la variable continue : Analyse multivariée discrète / continue"
)


def continuous_analysis(
    v: str, w: dict, axis1: matplotlib.axes, bins: int = 20, rightaxis: bool = True
) -> matplotlib.axes:
    """_return axis with a multivaried analysis from the dataframe df :
            histogram of continuous variable : v
            plot char of discret 2-categories variable : w["variables"]
        more readable presentation than a multi-stack histogram

    Args:
        v (str): name of continuous variable (column )
        w (dict): description of discret variable (must have only 2 categories, non more). Keys :
            "variable" : column name in df (ex: "Gender")
            "selected_value" : the value of whom the ratio is calculated (ex: "Male")
            "label" : label (ex : "male rate")
        axis1 (matplotlib.axes): _description_
        bins (int, optional): number of bins of histogram. Defaults to 20.
        rightaxis (bool, optional): True if axes is on the right end of fig, for displaying ticks and y label on the right. If False, ticks and y labels are not displayed. Defaults to True.

    Returns:
        matplotlib.axes: resulted matplotlib axes
    """

    axis1.hist(
        df[v],
        bins=bins,
        color="lightblue",
        edgecolor="black",
    )
    axis1.set_title(v)
    axis1.grid(visible=False)

    step = (max(df[v]) - min(df[v])) / bins
    X = np.linspace(min(df[v]) + step / 2, max(df[v] - step / 2), bins)
    Y = list()
    for x in X:
        interval = f"{v} >= {x-step/2} and {v} <= {x+step/2}"
        if df.query(interval).shape[0] != 0:
            Y.append(
                df[df[w["variable"]] == w["selected_value"]].query(interval).shape[0]
                / df.query(interval).shape[0]
            )
        else:
            Y.append(0)
    axis2 = axis1.twinx()

    axis2.plot(X, Y, "--ro")
    axis2.set_ylim(0, 1)
    axis2.set_ylabel(w["label"], color="red")
    axis2.tick_params(axis="y", labelcolor="red", color="red")
    axis2.yaxis.set_major_formatter("{x:.0%}")
    axis2.grid(visible=False)
    for x, y in zip(X, Y):
        axis2.text(x + 0.05, y + 0.05, f"{y:.0%}", fontsize="x-small", c="red")
    if not rightaxis:
        axis2.set(ylabel=None, yticklabels=[])
    return axis1


@st.cache_data()
def multi_cont(cont_list: list, ratio_list: list, gbins: int = 20) -> matplotlib.figure:
    """_return a figure with axes, each axe display a multivaried analysis between:
            a variable from cont_list
            a discret 2-categories variable from ratio_list

    Args:
        cont_list (list): list of str (name of continuous variables)
        ratio_list (list): list of dict for description of discret varaibles (varaible name, selected_value for ratio, label)
        gbins (int, optional): number of bins of histogram. Defaults to 20.

    Returns:
        matplotlib.figure: the resulted figure
    """
    fig, ax = plt.subplots(
        len(ratio_list) * ((len(cont_list) + 2) // 3), 3, figsize=(20, 40)
    )
    fig.suptitle(f"ANALYSE MULTIVARIEE VARIABLES CONTINUES AVEC RATIOS")
    for i, w in enumerate(ratio_list):
        if w["variable"] == "Tenure":
            bins = 11
        else:
            bins = gbins
        for j, v in enumerate(cont_list):
            axis = ax[2 * i + j // 3, j % 3]
            axis = continuous_analysis(
                v, w, axis, bins=bins, rightaxis=(j != 0 and j % 2 == 0)
            )
            axis.grid(visible=False)
        # ax[2*i+1, 2].set_axis_off()
        ax[2 * i + 1, 2].remove()
    fig.tight_layout()
    return fig


ratio_list = [
    {"variable": "Exited", "selected_value": 1.0, "label": "churn rate"},
    {"variable": "Gender", "selected_value": "Male", "label": "male rate"},
    {"variable": "HasCrCard", "selected_value": 1.0, "label": "credit card rate"},
    {
        "variable": "IsActiveMember",
        "selected_value": 1.0,
        "label": "active member rate",
    },
]


fig7 = multi_cont(cont_list, ratio_list)
st.pyplot(fig7)
