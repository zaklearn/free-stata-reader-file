
import subprocess
import requests
import streamlit as st
import pandas as pd
import pyreadstat

def main():
    # Configuration du style Streamlit
    st.set_page_config(page_title="Visualisation des données Stata", layout="wide")

    # Sidebar
    with st.sidebar:
        st.title("Options")
        st.markdown("### À propos")
        st.write("Cet outil permet de téléverser un fichier Stata (.dta), de visualiser les données et de les exporter en formats CSV ou Excel.")
        st.markdown("**Développé par :** [Zakaria Benhoumad](https://www.linkedin.com/in/zakaria-benhoumad)")

        # Chargement du fichier Stata
        uploaded_file = st.file_uploader("Téléversez un fichier Stata", type=["dta"])

    st.title("Visualisation des données Stata")

    if uploaded_file is not None:
        try:
            # Sauvegarder le fichier temporairement
            with open("temp_file.dta", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Lecture des données Stata
            df, meta = pyreadstat.read_dta("temp_file.dta")

            # Aperçu des données
            with st.expander("Afficher/Masquer l'aperçu des données"):
                st.subheader("Aperçu des données")
                st.write(df.head())

            # Afficher la table complète
            st.subheader("Tableau des données")
            st.dataframe(df, use_container_width=True)

            # Options de téléchargement
            st.subheader("Téléchargement des données")
            csv = df.to_csv(index=False).encode('utf-8')
            excel = df.to_excel("temp_file.xlsx", index=False)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Télécharger en CSV",
                    data=csv,
                    file_name="exported_data.csv",
                    mime="text/csv"
                )
            with col2:
                st.download_button(
                    label="Télécharger en Excel",
                    data=open("temp_file.xlsx", "rb"),
                    file_name="exported_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")

if __name__ == "__main__":
    main()
