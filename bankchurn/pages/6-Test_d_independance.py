import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import scipy
from scipy.stats import binomtest, chisquare, ttest_1samp, chi2_contingency
from scipy.stats import ttest_ind, f_oneway, pearsonr

from home import variables_list_initialization

st.set_page_config(layout="wide")


def format_df(df: pd.DataFrame, stat=False) -> pd.DataFrame:
    """Formatte les cellules du dataframe affichant des p-values et coefficients de corrélation

    Args:
        df (pd.DataFrame): le tableau à afficher
        stat:   False[default] : mise en forme des p-values
                True : mise en forme des coefficients de corrélation (entre -1 et 1)
    Returns:
        pd.DataFrame: le tableau de p-values, affichées en % avec 2 décimales et :
            variables indépendantes ou faible corrélation : fond vert
                si p-value > seuil de 2% ou abs(coef. de corrélation) < seuil de 0.2
            variables dépendantes ou forte corrélation : fond rouge
                si p-value < seuil de 2% ou abs(coef. de corrélation) > seuil de 0.2

    """
    pvalue_threshold = 0.02
    stat_threshold = 0.005

    match stat:
        case False:  # formattage p-value
            condition = (
                lambda x: f"background-color: {'#dfd' if x>pvalue_threshold else '#fbb'}"
            )
            formattage = lambda x: f"{float(x):.2%}"

        case True:  # formattage scoefficient de corrélation
            condition = (
                lambda x: f"background-color: {'#dfd' if abs(x)<stat_threshold else '#fbb'}"
            )
            formattage = lambda x: f"{float(x):.4f}"

    return df.style.map(condition).format(formattage)


variables_list_initialization()
df = st.session_state.session_df
disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.markdown("##### Tests d'indépendance des variables : ")

st.markdown(
    "##### > Probabilité d'indépendance de 2 variables discrètes entre elles (chi2_independancy): pvalue"
)
chi2_matrix = pd.DataFrame(
    [
        [chi2_contingency(pd.crosstab(df[u], df[v])).pvalue for u in disc_list]
        for v in disc_list
    ],
    columns=disc_list,
    index=disc_list,
)
st.dataframe(format_df(chi2_matrix))

# séparation des variables discrètes selon qu'elles prennent 2, 3 ou plus valeurs :
disc_values = {
    i: [d for d in disc_list if df[d].value_counts().shape[0] == i] for i in range(2, 5)
}
student_list = sum([disc_values[i] for i in disc_values.keys() if i == 2], [])
anova_list = sum([disc_values[i] for i in disc_values.keys() if i > 2], [])


st.markdown(
    "##### > Probabilité d'indépendance entre une variable discrète prenant 2 valeurs et une variable continue (test de student): pvalue"
)
student_matrix = pd.DataFrame(
    [
        [
            ttest_ind(
                df[df[u] == df[u].unique()[0]][v], df[df[u] == df[u].unique()[1]][v]
            ).pvalue
            for u in student_list
        ]
        for v in cont_list
    ],
    index=cont_list,
    columns=student_list,
)
st.dataframe(format_df(student_matrix))

st.markdown(
    "##### > Probabilité d'indépendance entre une variable discrète et une variable continue (test de anova): pvalue"
)
anova_matrix = pd.DataFrame(
    [
        [f_oneway(*df.groupby(u)[v].apply(list)).pvalue for u in disc_list]
        for v in cont_list
    ],
    index=cont_list,
    columns=disc_list,
)
st.dataframe(format_df(anova_matrix))

st.markdown(
    "##### > Probabilité d'indépendance entre 2 variable continues (test de pearson): pvalue"
)
pearson_pvalue_matrix = pd.DataFrame(
    [[pearsonr(df[x], df[y]).pvalue for x in cont_list] for y in cont_list],
    index=cont_list,
    columns=cont_list,
)
st.dataframe(format_df(pearson_pvalue_matrix))

st.markdown(
    "##### > Corrélation (de -1.00 à 1.00) entre 2 variable continues (test de pearson): statistic"
)
pearson_stat_matrix = pd.DataFrame(
    [[pearsonr(df[x], df[y]).statistic for x in cont_list] for y in cont_list],
    index=cont_list,
    columns=cont_list,
)
st.dataframe(format_df(pearson_stat_matrix, stat=True))
