import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from streamlit_folium import st_folium
import folium

# Define the layout with three tabs
tab1, tab2 = st.tabs(["About Me", "Regional and Demographic Distribution of Patient Pathologies in France"])

# Tab 1: About Me
with tab1:
    # Sidebar with personal details
    with st.sidebar:
        st.image("./photo_ines.png", caption="Inès Duflos", use_column_width=True)
        st.subheader("Contact Information")
        st.write("[LinkedIn Profile](https://www.linkedin.com/in/in%C3%A8s-duflos-553327229/)")
        st.write("📞 Phone: 07 81 74 54 58")
        st.write("📧 Email: ines.duflos@efrei.net")
        
    # Main content
    st.title("Welcome to My Portfolio")
    st.write("""
        Hello! I am Inès Duflos, currently a student at EFREI Paris specializing in Bioinformatics. 
        I hold a Computer Science degree from Paris-Saclay University and have pursued healthcare studies as both a major and minor for several years. 
        This portfolio showcases various data visualization projects completed during my data science courses. 
        Please explore the different tabs to view my work. 
    """)

    # Languages section
    st.header("Languages")
    st.write("""
    - **French**: C2 (Native Speaker)  
    - **English**: C1 (Linguaskill Certification)  
    - **Spanish**: A2 
    """)

    # Coding skills section with a visual bar chart
    st.header("Coding Skills")
    data_coding = pd.DataFrame({
        'languages': ['Python', 'C++/C', 'Java', 'SQL', 'Ocaml', 'JavaScript', 'HTML/CSS'],
        'level': [9, 9, 9, 7, 7, 5, 5]
    }) 
    chart = alt.Chart(data_coding).mark_bar().encode(
        y=alt.Y('languages', sort='-x', title="Programming Languages"),
        x=alt.X('level', scale=alt.Scale(domain=[0, 10]), title="Proficiency Level"),
        color=alt.Color('languages', 
                    scale=alt.Scale(
                        domain=['Python', 'C++/C', 'Java', 'SQL', 'Ocaml', 'JavaScript', 'HTML/CSS'],
                        range=['#F06292', '#9575CD', '#64B5F6', '#81C784', '#FFF176', '#FFB74D', '#E57373']
                    ), legend=None),
        tooltip=['languages', 'level']
    ).properties(
        width='container', height=300
    )
    st.altair_chart(chart, use_container_width=True)
    st.write("The coding proficiency is rated on a scale of 1 to 10.")

    # Soft skills section
    st.header("Soft Skills")
    st.write("""
    - Rigorous  
    - Curious  
    - Creative  
    - Teamwork-Oriented  
    - Adaptable  
    - Strong Communication  
    - Problem-Solver 
    """)

    # Interests section
    st.header("Interests")
    st.write("""
        Outside of my academic and professional pursuits, I am passionate about a variety of hobbies, including:
    
        - 📸 **Photography**  
        - 🎶 **Music**  
        - 🎤 **Concerts**  
        - ✈️ **Traveling**  
        - 🎭 **Theatre** 
    """)

# Tab 2: Regional and Demographic Distribution of Patient Pathologies in France
with tab2:
    path3 = "./effectifs.csv"
    
    @st.cache_data
    def load_data(url):
        # Load the CSV file

        data = pd.read_csv(url, delimiter=';')
        return data

    # Load and display data
    url = 'https://data.ameli.fr/api/explore/v2.1/catalog/datasets/effectifs/exports/csv?use_labels=true'
    data = load_data(url)
    
    # Sample of the data
    st.write("Voici un aperçu des données sur la répartition des pathologies par région en France :")
    #st.write("Sample of the data on regional and demographic distribution of patient pathologies in France:")

    # Pagination controls
    rows_per_page = 100
    total_rows = len(data)
    page_number = st.number_input('Page number:', min_value=1, max_value=(total_rows // rows_per_page) + 1, step=1)

    # Calculate start and end rows for current page
    start_row = (page_number - 1) * rows_per_page
    end_row = start_row + rows_per_page

    # Display a page of data
    st.write(f"Displaying rows {start_row} to {end_row}")
    st.dataframe(data[start_row:end_row])

    # Répartition des pathologies par sexe
    st.header("Répartition des pathologies par sexe")

    # Filtrer pour ne garder que les hommes et les femmes
    data_filtered = data[(data['libelle_sexe'] == 'hommes') | (data['libelle_sexe'] == 'femmes')]

    # Utiliser le nom correct de la colonne Npop
    patho_by_sexe = data_filtered.groupby(['patho_niv1', 'libelle_sexe'])['Npop'].sum().reset_index()

    # Créer le graphique Altair
    chart_sexe = alt.Chart(patho_by_sexe).mark_bar().encode(
        x=alt.X('patho_niv1:N', title='Type de Pathologie'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),  # Corriger ici
        color='libelle_sexe:N',  # Coloration par sexe
        tooltip=['patho_niv1', 'libelle_sexe', 'Npop']  # Corriger ici aussi
    ).properties(
        title="Répartition des Pathologies par Sexe",
        width=800
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_sexe, use_container_width=True)

    # Répartition des pathologies par tranche d'âge
    st.header("Répartition des pathologies par tranche d'âge")

    # Filtrer pour ne garder que les hommes et les femmes
    data_filtered = data[(data['libelle_classe_age'] !=  'tous âges') & (data['libelle_sexe'] != 'tous sexes')]

    # Créer un ordre personnalisé pour les tranches d'âge
    age_order = ['de 0 à 4 ans', 'de 5 à 9 ans', 'de 10 à 14 ans', 'de 15 à 19 ans', 'de 20 à 24 ans', 
             'de 25 à 29 ans', 'de 30 à 34 ans', 'de 35 à 39 ans', 'de 40 à 44 ans', 'de 45 à 49 ans',
             'de 50 à 54 ans', 'de 55 à 59 ans', 'de 60 à 64 ans', 'de 65 à 69 ans', 'de 70 à 74 ans', 
             'de 75 à 79 ans', 'de 80 à 84 ans', 'de 85 à 89 ans', 'de 90 à 94 ans', 'plus de 95 ans']

    # Transformer explicitement la colonne 'libelle_classe_age' pour avoir l'ordre souhaité
    data_filtered['libelle_classe_age'] = pd.Categorical(data_filtered['libelle_classe_age'], categories=age_order, ordered=True)

    # Grouper les données par type de pathologie et tranche d'âge
    patho_by_age = data_filtered.groupby(['patho_niv1', 'libelle_classe_age'])['Npop'].sum().reset_index()
    patho_by_age = patho_by_age.sort_values(by='libelle_classe_age')

    # Créer le graphique en utilisant cet ordre
    chart_age = alt.Chart(patho_by_age).mark_bar().encode(
        x=alt.X('patho_niv1:N', title='Type de Pathologie', sort=None),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        color=alt.Color('libelle_classe_age:N', sort=age_order),  # Utiliser l'ordre défini pour les tranches d'âge
        tooltip=['patho_niv1', 'libelle_classe_age', 'Npop']
    ).properties(
        title="Répartition des Pathologies par Tranche d'Âge",
        width=800
    )
    st.altair_chart(chart_age, use_container_width=True)

    # Tendances des pathologies au fil du temps
    st.header("Tendances des pathologies au fil du temps")

    patho_by_year = data_filtered.groupby(['annee', 'patho_niv1'])['Npop'].sum().reset_index()

    chart_year = alt.Chart(patho_by_year).mark_line().encode(
        x=alt.X('annee:O', title='Année'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        color='patho_niv1:N',  # Coloration par type de pathologie
        tooltip=['annee', 'patho_niv1', 'Npop']
    ).properties(
        title="Tendances des Pathologies au Fil du Temps",
        width=800
    ).interactive()

    st.altair_chart(chart_year, use_container_width=True)

    # Graphique de l'évolution des Cancers au fil des ans
    st.header("Évolution des Cancers au Fil des Ans")

    # Filtrer les données pour les pathologies de type "Cancers"
    data_cancers = data[data['patho_niv1'] == 'Cancers']

    # Grouper les données par année pour les Cancers
    patho_cancers_by_year = data_cancers.groupby(['annee'])['Npop'].sum().reset_index()

    # Créer le graphique de l'évolution des Cancers au fil des ans
    chart_cancers_year = alt.Chart(patho_cancers_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Année'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        tooltip=['annee', 'Npop']
    ).properties(
        title="Évolution des Cancers au Fil des Ans",
        width=800
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_cancers_year, use_container_width=True)

    # Graphique de l'évolution des pathologies de niveau 2 liées aux Cancers au fil des ans
    st.header("Évolution des Pathologies de Niveau 2 liées aux Cancers au Fil des Ans")

    # Filtrer les données pour les pathologies de niveau 1 "Cancers"
    data_cancers_niv2 = data[data['patho_niv1'] == 'Cancers']

    # Grouper les données par année et pathologie de niveau 2 pour les Cancers
    patho_cancers_niv2_by_year = data_cancers_niv2.groupby(['annee', 'patho_niv2'])['Npop'].sum().reset_index()

    # Créer le graphique de l'évolution des pathologies de niveau 2 liées aux Cancers au fil des ans
    chart_cancers_niv2_year = alt.Chart(patho_cancers_niv2_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Année'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        color='patho_niv2:N',  # Chaque pathologie de niveau 2 aura une couleur différente
        tooltip=['annee', 'patho_niv2', 'Npop']  # Tooltip pour montrer les détails
    ).properties(
        title="Évolution des Pathologies de Niveau 2 liées aux Cancers au Fil des Ans",
        width=800
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_cancers_niv2_year, use_container_width=True)

    # Graphique de l'évolution des pathologies de niveau 2 liées aux Cancers au fil des ans
    st.header("Évolution des Pathologies de Niveau 3 liées aux Cancers au Fil des Ans")

    # Filtrer les données pour les pathologies de niveau 1 "Cancers"
    data_cancers_niv3 = data[data['patho_niv1'] == 'Cancers']

    # Grouper les données par année et pathologie de niveau 2 pour les Cancers
    patho_cancers_niv3_by_year = data_cancers_niv2.groupby(['annee', 'patho_niv3'])['Npop'].sum().reset_index()

    # Créer le graphique de l'évolution des pathologies de niveau 2 liées aux Cancers au fil des ans
    chart_cancers_niv3_year = alt.Chart(patho_cancers_niv3_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Année'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        color='patho_niv3:N',  # Chaque pathologie de niveau 2 aura une couleur différente
        tooltip=['annee', 'patho_niv3', 'Npop']  # Tooltip pour montrer les détails
    ).properties(
        title="Évolution des Pathologies de Niveau 3 liées aux Cancers au Fil des Ans",
        width=800
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_cancers_niv3_year, use_container_width=True)

    # Filtrer les données par pathologies de niveau 1 égales à "Cancers"
    data_cancers = data[data['patho_niv1'] == 'Cancers']

    # Sélection d'une année spécifique pour observer les cancers sur une année donnée
    st.header("Sélectionnez une année pour observer les cancers")

    # Liste des années disponibles dans les données
    years_available = data_cancers['annee'].unique()
    year_selected = st.selectbox("Choisissez une année", years_available)

    # Filtrer les données pour l'année sélectionnée
    data_cancers_year_selected = data_cancers[data_cancers['annee'] == year_selected]

    # Graphique de la répartition des cancers (niveau 2) pour une année spécifique
    st.header(f"Répartition des types de cancers (niveau 2) pour l'année {year_selected}")

    # Grouper les données par pathologie de niveau 2 pour l'année sélectionnée
    patho_cancers_niv2_year_selected = data_cancers_year_selected.groupby(['patho_niv2'])['Npop'].sum().reset_index()

    # Créer le graphique pour les pathologies de niveau 2 pour l'année sélectionnée
    chart_cancers_niv2_year_selected = alt.Chart(patho_cancers_niv2_year_selected).mark_bar().encode(
        x=alt.X('patho_niv2:N', title='Type de Cancer (Niveau 2)'),
        y=alt.Y('Npop:Q', title='Nombre de Patients'),
        color='patho_niv2:N',
        tooltip=['patho_niv2', 'Npop']
    ).properties(
        title=f"Répartition des Cancers (Niveau 2) pour l'année {year_selected}",
        width=800
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_cancers_niv2_year_selected, use_container_width=True)

    # Focus sur un type particulier de cancer de niveau 2
    st.header("Sélectionnez un type de cancer (niveau 2) pour voir son évolution")

    # Liste des pathologies de niveau 2 disponibles
    pathologies_niv2_available = data_cancers['patho_niv2'].unique()
    patho_niv2_selected = st.selectbox("Choisissez un type de cancer de niveau 2", pathologies_niv2_available)

    # Filtrer les données pour la pathologie de niveau 2 sélectionnée
    data_cancer_niv2_selected = data_cancers[data_cancers['patho_niv2'] == patho_niv2_selected]

    # Analyse des cancers par tranche d'âge pour une année donnée
    st.header(f"Répartition des Cancers par tranche d'âge pour l'année {year_selected}")

    # Filtrer les données par tranche d'âge et sexe pour l'année sélectionnée
    data_age_cancers_year_selected = data_cancers_year_selected[
        (data_cancers_year_selected['libelle_classe_age'] != 'tous âges') & 
        (data_cancers_year_selected['libelle_sexe'] != 'tous sexes')
    ]

    # Grouper les données par classe d'âge et sexe
    patho_age_sex_year_selected = data_age_cancers_year_selected.groupby(
        ['libelle_classe_age', 'libelle_sexe']
    )['Npop'].sum().reset_index()

    # Créer le graphique Altair montrant la répartition par tranche d'âge et sexe
    chart_age_sex_cancers_year_selected = alt.Chart(patho_age_sex_year_selected).mark_bar().encode(
        x=alt.X('libelle_classe_age:N', title="Classe d'âge"),
        y=alt.Y('Npop:Q', title="Nombre de patients"),
        color='libelle_sexe:N',  # Coloration par sexe
        tooltip=['libelle_classe_age', 'libelle_sexe', 'Npop']
    ).properties(
        title=f"Répartition des Cancers par tranche d'âge et sexe pour l'année {year_selected}",
        width=800
    ).configure_axis(
        labelAngle=-45  # Rotation des labels pour améliorer la lisibilité
    ).interactive()

    # Afficher le graphique
    st.altair_chart(chart_age_sex_cancers_year_selected, use_container_width=True)
