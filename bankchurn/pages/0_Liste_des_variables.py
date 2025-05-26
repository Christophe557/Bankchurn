import streamlit as st
from home import variables_list_initialization

st.markdown("### 2- Liste des variables")

variables_list_initialization()

disc_list = st.session_state.session_disc_list
cont_list = st.session_state.session_cont_list

st.table(
    {
        "": ["Identifiants ", "Variables discrètes", "Variables continues", "Autres"],
        "Variables": [
            "ID",
            " | ".join(disc_list),
            " | ".join(cont_list),
            "CustomerID | Surname",
        ],
    }
)

if st.button("add B"):
    st.session_state.session_disc_list.append("bbbbbbbbb")
