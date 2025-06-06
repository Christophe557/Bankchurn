import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes
import matplotlib.figure
import streamlit as st
from home import variables_list_initialization

st.set_page_config(layout="wide")

variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list


st.markdown("### 4- Analyse multivariée discrète/discrète avec ratio")


def discret_analysis(
    v: str, w: dict, axis1: matplotlib.axes, rightaxis: bool = True
) -> matplotlib.axes:
    """return axis with a multivaried analysis from the dataframe df :
            bar chart of discret variable #1 : v
            plot char of discret 2-categories variable #2 : w["variables"]
        information get from crosstab between v and w
        more readable presentation than a heatmap of crosstab

    Args:
        v (str): name of variable (column label) #1
        w (dict): description of discret variable (must have only 2 categories, non more). Keys :
            "variable" : column name in df (ex: "Gender")
            "selected_value" : the value of whom the ratio is calculated (ex: "Male")
            "label" : label (ex : "male rate")
        axis1 (matplotlib.axes): initial empty matplotlib axes
        rightaxis (bool, optional): True if axes is on the right end of fig, for displaying ticks and y label on the right. If False, ticks and y labels are not displayed. Defaults to True.

    Returns:
        matplotlib.axes: resulted matplotlib axes
    """

    cstb = pd.crosstab(df[v], df[w["variable"]])
    cols = list(cstb.columns)
    cstb["sum"] = cstb[cols[0]] + cstb[cols[1]]
    cstb[w["label"]] = cstb[w["selected_value"]] / cstb["sum"]
    # print(cstb)
    # print("axe x :", [ str(i) for i in cstb.index])
    # print("axe y1: ", list(cstb["sum"]))
    # print("axe y2: ", list(cstb[cr]))
    # print("axe y2%:", [ f"{p:.2%}" for p in cstb[cr]])

    categories = [str(i) for i in cstb.index]
    axis1.bar(
        categories,
        height=cstb["sum"],
        width=0.5,
        color="lightblue",
        edgecolor="black",
        label=f"{v} count",
    )
    totalvalues = sum([h for h in axis1.containers[0].datavalues])
    values = [f"{h*100/totalvalues:.0f}%" for h in axis1.containers[0].datavalues]
    axis1.bar_label(
        axis1.containers[0],
        labels=values,
    )
    axis1.set_ylim(0, 140000)
    axis1.set_title(v)

    axis2 = axis1.twinx()
    axis2.plot(
        categories,
        list(cstb[w["label"]]),
        "--ro",  # équivalent à la ligne suivante
        # linestyle="--", color="red", # marker="o",
        label=w["label"],
    )
    axis2.set_ylim(0, 1)
    axis2.set_ylabel(w["label"], color="red")
    axis2.tick_params(axis="y", labelcolor="red", color="red")
    axis2.yaxis.set_major_formatter("{x:.0%}")

    for x, y in enumerate(cstb[w["label"]]):
        axis2.text(x + 0.10, y, f"{y:.0%}", c="red")
    if not rightaxis:
        axis2.set(ylabel=None, yticklabels=[])
    return axis1


@st.cache_data()
def multi_disc(disc_list: list, ratio_list: list) -> matplotlib.figure:
    """return a figure with axes, each axe display a multivaried analysis between:
            a variable from disc_list
            a discret 2-categories variable from ratio_list

    Args:
        disc_list (list): list of str (name of continuous variables)
        ratio_list (list): list of dict for description of discret varaibles (varaible name, selected_value for ratio, label)


    Returns:
        matplotlib.figure: the resulted figure
    """
    fig, ax = plt.subplots(
        len(ratio_list) * ((len(disc_list) + 2) // 3), 3, sharey=True, figsize=(20, 50)
    )
    fig.suptitle(f"ANALYSE MULTIVARIEE VARIABLES DISCRETES AVEC RATIOS")
    for i, w in enumerate(ratio_list):
        for j, v in enumerate(disc_list):
            axis = ax[2 * i + j // 3, j % 3]
            axis = discret_analysis(v, w, axis, rightaxis=(j % 3 == 2))
            axis.grid(visible=False)

    # fig, ax = plt.subplots(2, 3, sharey=True, figsize=(15, 6))
    # fig.suptitle(f"ANALYSE MULTIVARIEE VARIABLES DISCRETES + {cr}")
    # for i, v in enumerate(disc_list):
    #     axis = ax[i // 3, i % 3]
    #     axis = discret_analysis(v, w, cr, axis, rightaxis=(i % 3 == 2))

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

# for w, cr in zip(
#     ["Exited", "Gender", "HasCrCard", "IsActiveMember"],
#     ["churn rate", "male rate", "creditcard rate", "activemember rate"],
# ):
fig = multi_disc(disc_list, ratio_list)
st.pyplot(fig)
