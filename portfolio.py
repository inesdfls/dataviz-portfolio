import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
import json
import requests

# Define the layout with two tabs: "About Me" and "Regional and Demographic Distribution"
tab1, tab2 = st.tabs(["About Me", "Regional and Demographic Distribution of Patient Pathologies in France"])

# Tab 1: Personal introduction
with tab1:
    # Sidebar with contact information
    with st.sidebar:
        st.image("./photo_ines.png", caption="Inès Duflos", use_column_width=True)
        st.subheader("Contact Information")
        st.write("[LinkedIn Profile](https://www.linkedin.com/in/in%C3%A8s-duflos-553327229/)")
        st.write("📞 Phone: 07 81 74 54 58")
        st.write("📧 Email: ines.duflos@efrei.net")
    
    # Main portfolio introduction
    st.title("Welcome to My Portfolio")
    st.write("""
        Hello! I am Inès Duflos, currently a student at EFREI Paris specializing in Bioinformatics. 
        I hold a Computer Science degree from Paris-Saclay University and have pursued healthcare studies as both a major and minor for several years. 
        This portfolio showcases various data visualization projects completed during my data science courses. 
        Please explore the different tabs to view my work. 
    """)

    # Languages proficiency
    st.header("Languages")
    st.write("""
    - **French**: C2 (Native Speaker)  
    - **English**: C1 (Linguaskill Certification)  
    - **Spanish**: A2 
    """)

    # Coding skills with proficiency visualization
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

    # Soft skills
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

    # Personal interests
    st.header("Interests")
    st.write("""
        Outside of my academic and professional pursuits, I am passionate about a variety of hobbies, including:
    
        - 📸 **Photography**  
        - 🎶 **Music**  
        - 🎤 **Concerts**  
        - ✈️ **Traveling**  
        - 🎭 **Theatre** 
    """)

# Tab 2: Data analysis on patient pathologies in France
with tab2:
    
    st.title("Exploring Regional and Demographic Patterns of Pathologies in France")
    st.write("""
        This project is inspired by my academic journey in bioinformatics and my deep interest in public health data analysis. 
        I selected a dataset from the [French Open Data platform](https://www.data.gouv.fr/fr/datasets/pathologies-effectif-de-patients-par-pathologie-sexe-classe-dage-et-territoire-departement-region/), 
        which provides detailed information on patient populations managed by the national health insurance system in France. 
        The dataset includes records of patients categorized by pathology, chronic treatment, or care episodes, as well as demographic breakdowns by age, gender, region, and department.

        The goal of this analysis is to uncover demographic trends and highlight important healthcare insights. 
        By examining the distribution of pathologies across different regions and populations, we can gain valuable understanding of the healthcare landscape in France, which can inform decisions on resource allocation, awareness campaigns, and preventive strategies.

        The dataset encompasses a wide range of medical conditions such as cardiovascular diseases, diabetes, psychiatric disorders, and chronic respiratory diseases. 
        It also includes information on hospitalizations and chronic treatments, offering a comprehensive view of the healthcare needs and resource usage in the population. 
        The prevalence data, showing the proportion of the population affected by each condition, provides essential insights into the burden of disease across different demographic groups.

        Through this analysis, I aim to contribute to a better understanding of the challenges faced by the healthcare system and support data-driven approaches to improving healthcare delivery and policy-making.
    """)


    @st.cache_data
    def load_data(url):
        # Load the dataset containing regional and demographic data on pathologies
        data = pd.read_csv(url, delimiter=';')
        return data

    url = 'https://data.ameli.fr/api/explore/v2.1/catalog/datasets/effectifs/exports/csv?use_labels=true'
    data = load_data(url)
    
    # Data overview section
    st.write("Here is an overview of the data on the distribution of pathologies by region in France:")

    # Pagination for data preview
    rows_per_page = 100
    total_rows = len(data)
    page_number = st.number_input('Page number:', min_value=1, max_value=(total_rows // rows_per_page) + 1, step=1)

    start_row = (page_number - 1) * rows_per_page
    end_row = start_row + rows_per_page

    st.write(f"Displaying rows {start_row} to {end_row}")
    st.dataframe(data[start_row:end_row])

    # Distribution of pathologies by gender
    st.header("Pathology distribution by gender")
    data_filtered = data[(data['libelle_sexe'] == 'hommes') | (data['libelle_sexe'] == 'femmes')]

    patho_by_sexe = data_filtered.groupby(['patho_niv1', 'libelle_sexe'])['Npop'].sum().reset_index()

    chart_sexe = alt.Chart(patho_by_sexe).mark_bar().encode(
        x=alt.X('patho_niv1:N', title='Type of Pathology'),
        y=alt.Y('Npop:Q', title='Number of Patients'),
        color='libelle_sexe:N',
        tooltip=['patho_niv1', 'libelle_sexe', 'Npop']
    ).properties(
        title="Distribution of Pathologies by Gender",
        width=800
    ).interactive()

    st.altair_chart(chart_sexe, use_container_width=True)

    # Distribution of pathologies by age group
    st.header("Pathology distribution by age group")
    data_filtered = data[(data['libelle_classe_age'] !=  'tous âges') & (data['libelle_sexe'] != 'tous sexes')]

    age_order = ['de 0 à 4 ans', 'de 5 à 9 ans', 'de 10 à 14 ans', 'de 15 à 19 ans', 'de 20 à 24 ans', 
             'de 25 à 29 ans', 'de 30 à 34 ans', 'de 35 à 39 ans', 'de 40 à 44 ans', 'de 45 à 49 ans',
             'de 50 à 54 ans', 'de 55 à 59 ans', 'de 60 à 64 ans', 'de 65 à 69 ans', 'de 70 à 74 ans', 
             'de 75 à 79 ans', 'de 80 à 84 ans', 'de 85 à 89 ans', 'de 90 à 94 ans', 'plus de 95 ans']

    data_filtered['libelle_classe_age'] = pd.Categorical(data_filtered['libelle_classe_age'], categories=age_order, ordered=True)

    patho_by_age = data_filtered.groupby(['patho_niv1', 'libelle_classe_age'])['Npop'].sum().reset_index()
    patho_by_age = patho_by_age.sort_values(by='libelle_classe_age')

    chart_age = alt.Chart(patho_by_age).mark_bar().encode(
        x=alt.X('patho_niv1:N', title='Type of Pathology', sort=None),
        y=alt.Y('Npop:Q', title='Number of Patients'),
        color=alt.Color('libelle_classe_age:N', sort=age_order),
        tooltip=['patho_niv1', 'libelle_classe_age', 'Npop']
    ).properties(
        title="Distribution of Pathologies by Age Group",
        width=800
    )
    st.altair_chart(chart_age, use_container_width=True)

    st.write("""
        The distribution of pathologies by gender and age group shows a balanced spread across most categories. 
        While this may seem ideal, it could actually obscure critical trends or disparities in specific diseases or demographic groups. 
        A more nuanced analysis might reveal areas where healthcare resources need to be more targeted and focused.
    """)

    # Trends of pathologies over time
    st.header("Trends of pathologies over time")
    patho_by_year = data_filtered.groupby(['annee', 'patho_niv1'])['Npop'].sum().reset_index()

    chart_year = alt.Chart(patho_by_year).mark_line().encode(
        x=alt.X('annee:O', title='Year'),
        y=alt.Y('Npop:Q', title='Number of Patients'),
        color='patho_niv1:N',
        tooltip=['annee', 'patho_niv1', 'Npop']
    ).properties(
        title="Trends of Pathologies Over Time",
        width=800
    ).interactive()

    st.altair_chart(chart_year, use_container_width=True)

    st.write("""
        The trends of pathologies over time reveal a steady increase across several categories, 
        with "Maladies Cardioneurovasculaires" and "Cancers" being the most prevalent. 
        While most pathologies show moderate growth, the consistently high number of cancer patients highlights the need for deeper analysis. 
        For the rest of this analysis, I will focus on cancer trends to better understand its evolution and demographic impact.
    """)

    # Evolution of cancer cases over time
    st.header("Evolution of Cancer Cases Over Time")
    data_cancers = data[data['patho_niv1'] == 'Cancers']
    patho_cancers_by_year = data_cancers.groupby(['annee'])['Npop'].sum().reset_index()

    chart_cancers_year = alt.Chart(patho_cancers_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Year'),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        tooltip=['annee', 'Npop']
    ).properties(
        title="Evolution of Cancer Cases Over Time",
        width=800
    ).interactive()

    st.altair_chart(chart_cancers_year, use_container_width=True)

    st.write("""
        The evolution of cancer cases over time, as shown in this graph, reflects a relatively stable trend between 2015 and 2022, 
        with a slight but steady increase. This trend aligns with the general patterns seen across other pathologies, 
        where chronic conditions like cancers and long-term illnesses show persistent or growing patient numbers. 
        Compared to other pathologies, cancer remains one of the most significant burdens in terms of healthcare. Given this context, 
        focusing on cancer cases can provide important insights into resource needs and healthcare priorities for the future.
    """)


    # Evolution of level 2 pathologies linked to cancers
    st.header("Evolution of Level 2 Pathologies Linked to Cancers Over Time")
    data_cancers_niv2 = data[data['patho_niv1'] == 'Cancers']
    patho_cancers_niv2_by_year = data_cancers_niv2.groupby(['annee', 'patho_niv2'])['Npop'].sum().reset_index()

    chart_cancers_niv2_year = alt.Chart(patho_cancers_niv2_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Year'),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        color='patho_niv2:N',
        tooltip=['annee', 'patho_niv2', 'Npop']
    ).properties(
        title="Evolution of Level 2 Pathologies Linked to Cancers Over Time",
        width=800
    ).interactive()

    st.altair_chart(chart_cancers_niv2_year, use_container_width=True)

    # Evolution of level 3 pathologies linked to cancers
    st.header("Evolution of Level 3 Pathologies Linked to Cancers Over Time")
    data_cancers_niv3 = data[data['patho_niv1'] == 'Cancers']
    patho_cancers_niv3_by_year = data_cancers_niv2.groupby(['annee', 'patho_niv3'])['Npop'].sum().reset_index()

    chart_cancers_niv3_year = alt.Chart(patho_cancers_niv3_by_year).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Year'),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        color='patho_niv3:N',
        tooltip=['annee', 'patho_niv3', 'Npop']
    ).properties(
        title="Evolution of Level 3 Pathologies Linked to Cancers Over Time",
        width=800
    ).interactive()

    st.altair_chart(chart_cancers_niv3_year, use_container_width=True)

    st.write("""
        The **Evolution of Level 2 Pathologies Linked to Cancers Over Time** chart shows a general stability in the number of level 2 cancer cases (grouped by primary type) from 2015 to 2022. Colorectal cancer appears as the most frequent, followed by breast cancer in women. All types show a slight increase, indicating a growing need for attention to these pathologies.
        
        The **Evolution of Level 3 Pathologies Linked to Cancers Over Time** provides more detail, breaking down level 3 pathologies, with active and under-surveillance colorectal cancers leading. The trends show a slight upward movement, emphasizing the importance of ongoing surveillance for cancer patients.
        
        These observations suggest that while cancer cases have remained relatively stable, the gradual rise in cases highlights the need for further research and prevention efforts.
    """)

    # Cancer distribution by year (level 2)
    st.header("Select a year to observe cancer cases")
    years_available = data_cancers['annee'].unique()
    year_selected = st.selectbox("Choose a year", years_available)

    data_cancers_year_selected = data_cancers[data_cancers['annee'] == year_selected]

    st.header(f"Distribution of Cancer Types (Level 2) for the year {year_selected}")
    patho_cancers_niv2_year_selected = data_cancers_year_selected.groupby(['patho_niv2'])['Npop'].sum().reset_index()

    chart_cancers_niv2_year_selected = alt.Chart(patho_cancers_niv2_year_selected).mark_bar().encode(
        x=alt.X('patho_niv2:N', title='Type of Cancer (Level 2)'),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        color='patho_niv2:N',
        tooltip=['patho_niv2', 'Npop']
    ).properties(
        title=f"Distribution of Cancer Types (Level 2) for the year {year_selected}",
        width=800
    ).interactive()

    st.altair_chart(chart_cancers_niv2_year_selected, use_container_width=True)

    # Distribution of cancers by age group and gender for the year selected
    st.header(f"Distribution of Cancers by Age Group for the Year {year_selected}")
    data_age_cancers_year_selected = data_cancers_year_selected[
        (data_cancers_year_selected['libelle_classe_age'] != 'tous âges') & 
        (data_cancers_year_selected['libelle_sexe'] != 'tous sexes')
    ]

    patho_age_sex_year_selected = data_age_cancers_year_selected.groupby(
        ['libelle_classe_age', 'libelle_sexe']
    )['Npop'].sum().reset_index()

    chart_age_sex_cancers_year_selected = alt.Chart(patho_age_sex_year_selected).mark_bar().encode(
        x=alt.X('libelle_classe_age:N', title="Age Group"),
        y=alt.Y('Npop:Q', title="Number of Patients"),
        color='libelle_sexe:N',
        tooltip=['libelle_classe_age', 'libelle_sexe', 'Npop']
    ).properties(
        title=f"Distribution of Cancers by Age Group and Gender for the Year {year_selected}",
        width=800
    ).configure_axis(
        labelAngle=-45
    ).interactive()

    st.altair_chart(chart_age_sex_cancers_year_selected, use_container_width=True)

    st.write("""
        The distribution of cancer types, regardless of the selected year, shows that the different categories of cancers (Level 2) remain relatively stable in terms of case numbers, with no significant changes across the years. This is consistent across types such as colorectal, breast, prostate, and lung cancers, which maintain similar proportions over time.

        As for the distribution by age group and gender, we observe some minor fluctuations between years, but nothing particularly pronounced. The highest number of cases consistently appears in the 45 to 74 age range, while younger age groups tend to show far fewer cases. This overall stability suggests that the demographic profile of cancer incidence remains fairly consistent year by year, allowing for reliable trends analysis across different periods.
    """)


    # Cancer analysis with geographical mapping
    @st.cache_data
    def load_geojson():
        geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
        response = requests.get(geojson_url)
        geojson_data = response.json()
        return geojson_data

    geojson_data = load_geojson()

    dept_coordinates = {
    '01': [46.2500, 5.0000], '02': [49.5000, 3.5000], '03': [46.3333, 3.1667], '04': [44.0833, 6.2333],
    '05': [44.6667, 6.3333], '06': [43.6667, 7.1500], '07': [44.7500, 4.5833], '08': [49.5000, 4.7500],
    '09': [42.9167, 1.5833], '10': [48.3333, 4.0833], '11': [43.0833, 2.4167], '12': [44.3333, 2.6667],
    '13': [43.5167, 5.3833], '14': [49.1667, -0.3500], '15': [45.0333, 2.6667], '16': [45.6667, 0.1667],
    '17': [45.7500, -0.6333], '18': [47.0833, 2.4167], '19': [45.3667, 1.8667], '2A': [41.8333, 8.7500],
    '2B': [42.3667, 9.1667], '21': [47.3167, 5.0167], '22': [48.5000, -2.8333], '23': [46.0833, 2.1667],
    '24': [45.0000, 0.7500], '25': [47.1667, 6.3333], '26': [44.7500, 5.2500], '27': [49.0167, 1.0000],
    '28': [48.3333, 1.2500], '29': [48.1667, -4.0833], '30': [44.1667, 4.0833], '31': [43.6667, 1.3333],
    '32': [43.6667, 0.5833], '33': [44.8333, -0.6667], '34': [43.6667, 3.8333], '35': [48.0833, -1.6667],
    '36': [46.6667, 1.5833], '37': [47.3333, 0.6667], '38': [45.3333, 5.5833], '39': [46.7500, 5.7500],
    '40': [44.0000, -0.7500], '41': [47.5833, 1.3333], '42': [45.6667, 4.2500], '43': [45.0833, 3.9167],
    '44': [47.3333, -1.6667], '45': [47.9167, 2.1333], '46': [44.6667, 1.6667], '47': [44.5000, 0.4167],
    '48': [44.6667, 3.5000], '49': [47.3333, -0.5833], '50': [49.1167, -1.4000], '51': [49.0833, 4.0000],
    '52': [48.0000, 5.3333], '53': [48.0833, -0.7667], '54': [48.8333, 6.1667], '55': [49.0833, 5.3333],
    '56': [47.8333, -3.0000], '57': [49.0000, 6.5000], '58': [47.0000, 3.6667], '59': [50.6667, 3.0833],
    '60': [49.4167, 2.4167], '61': [48.5000, 0.1667], '62': [50.4167, 2.7500], '63': [45.7500, 3.1667],
    '64': [43.2500, -0.5833], '65': [43.0833, 0.1667], '66': [42.5000, 2.7500], '67': [48.5833, 7.7500],
    '68': [47.7500, 7.3333], '69': [45.7500, 4.8333], '70': [47.6667, 6.0833], '71': [46.6667, 4.4167],
    '72': [47.9167, 0.2500], '73': [45.5833, 6.4167], '74': [46.0833, 6.5833], '75': [48.8566, 2.3522],
    '76': [49.6667, 0.5833], '77': [48.6667, 2.7500], '78': [48.8333, 1.9167], '79': [46.3333, -0.5000],
    '80': [50.0000, 2.5000], '81': [43.6667, 2.2500], '82': [44.0833, 1.2500], '83': [43.4167, 6.0000],
    '84': [44.0000, 5.0000], '85': [46.6667, -1.6667], '86': [46.5833, 0.3333], '87': [45.8333, 1.3333],
    '88': [48.0833, 6.6667], '89': [47.7833, 3.5667], '90': [47.6167, 6.8333], '91': [48.6167, 2.4000],
    '92': [48.8333, 2.2500], '93': [48.9167, 2.4167], '94': [48.7667, 2.4667], '95': [49.0500, 2.1167],
    '971': [16.2650, -61.5500], '972': [14.6415, -61.0242], '973': [3.9339, -53.1258], '974': [-21.1151, 55.5364],
    '976': [-12.8275, 45.1667]   
    }  
    
    st.header("Map of Cancer Cases and Prevalence by Department")

    years_available = data_cancers['annee'].unique()
    year_selected = st.selectbox("Choose a year", years_available, key="year_selectbox_dept")
    data_cancers_year_selected = data_cancers[data_cancers['annee'] == year_selected]
    cancer_by_dept = data_cancers_year_selected.groupby('dept')[['Npop', 'prev']].sum().reset_index()
    dept_coords_df = pd.DataFrame.from_dict(dept_coordinates, orient='index', columns=['latitude', 'longitude']).reset_index()
    dept_coords_df.rename(columns={'index': 'dept'}, inplace=True)
    cancer_by_dept = cancer_by_dept[cancer_by_dept['dept'] != '999']
    cancer_by_dept = pd.merge(cancer_by_dept, dept_coords_df, on='dept', how='left')

    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    min_npop = cancer_by_dept['Npop'].min()
    max_npop = cancer_by_dept['Npop'].max()
    cancer_by_dept['radius'] = ((cancer_by_dept['Npop'] - min_npop) / (max_npop - min_npop)) * 8 + 2
    cancer_by_dept['prev_normalized'] = cancer_by_dept['prev'] / cancer_by_dept['prev'].max()
    cancer_by_dept['prev_radius'] = cancer_by_dept['prev_normalized'] * 15 
    
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=cancer_by_dept,
        columns=["dept", "Npop"],
        key_on="feature.properties.code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Cancer Cases",
    ).add_to(m)

    for idx, row in cancer_by_dept.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['prev_radius']*0.5,
            popup=f"Department: {row['dept']}<br>Cancer Cases: {row['Npop']}<br>Prevalence: {row['prev']}",
            color="blue",
            fill=True,
            fill_opacity=0.6,
        ).add_to(m)

    st_folium(m, width=800, height=800)

    st.write("""
        The map displaying cancer cases and prevalence by department clearly shows that the departments with the highest number of cases are Nord (59), Paris (75), Bouches-du-Rhône (13), and Rhône (69). These areas, likely due to their higher population densities and various regional factors, stand out in terms of cancer cases.

        Given that Nord (59) has the largest number of cases, I will focus on this department for a more detailed analysis to better understand the distribution and trends of cancer cases within this region.
    """)

    # Analysis of cancer cases in department 59
    st.header("Analysis of Cancer Cases in Department 59")

    data_59 = data_cancers[data_cancers['dept'] == '59']

    st.subheader("Evolution of Cancer Cases in Department 59 Over the Years")

    cases_by_year_59 = data_59.groupby('annee')['Npop'].sum().reset_index()

    chart_cases_year_59 = alt.Chart(cases_by_year_59).mark_line(point=True).encode(
        x=alt.X('annee:O', title='Year'),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        tooltip=['annee', 'Npop']
    ).properties(
        title="Evolution of Cancer Cases in Department 59",
        width=800
    ).interactive()

    st.altair_chart(chart_cases_year_59, use_container_width=True)

    st.subheader("Distribution of Cancer Types in Department 59")

    cases_by_type_59 = data_59.groupby('patho_niv2')['Npop'].sum().reset_index()

    chart_cases_type_59 = alt.Chart(cases_by_type_59).mark_bar().encode(
        x=alt.X('patho_niv2:N', title='Type of Cancer (Level 2)', sort=None),
        y=alt.Y('Npop:Q', title='Number of Cases'),
        color='patho_niv2:N',
        tooltip=['patho_niv2', 'Npop']
    ).properties(
        title="Distribution of Cancer Types in Department 59",
        width=800
    ).interactive()

    st.altair_chart(chart_cases_type_59, use_container_width=True)

    # Distribution of cancer cases by age group and gender in Department 59
    st.subheader("Distribution of Cancer Cases by Age Group and Gender in Department 59")

    data_59_filtered = data_59[(data_59['libelle_classe_age'] != 'tous âges') & (data_59['libelle_sexe'] != 'tous sexes')]

    cases_by_age_sex_59 = data_59_filtered.groupby(['libelle_classe_age', 'libelle_sexe'])['Npop'].sum().reset_index()

    chart_cases_age_sex_59 = alt.Chart(cases_by_age_sex_59).mark_bar().encode(
        x=alt.X('libelle_classe_age:N', title="Age Group"),
        y=alt.Y('Npop:Q', title="Number of Cases"),
        color='libelle_sexe:N',
        tooltip=['libelle_classe_age', 'libelle_sexe', 'Npop']
    ).properties(
        title="Distribution of Cancer Cases by Age Group and Gender in Department 59",
        width=800
    ).configure_axis(
        labelAngle=-45
    ).interactive()

    st.altair_chart(chart_cases_age_sex_59, use_container_width=True)

    st.write(""" 
        In Department 59, cancer cases have remained consistently high from 2015 to 2022, indicating a persistent health challenge. The most common types are colorectal and lung, following national trends.

        Age distribution shows that the majority of cases occur in individuals aged 45 to 74, with a slight female predominance. This pattern highlights the need for targeted interventions in this age group to better manage and reduce cancer cases in the region. 
    """)

    st.subheader("Conclusion")
    st.write("""
        In conclusion, this analysis of cancer distribution across France, with a particular focus on Department 59, provides valuable insights into critical healthcare trends and priorities. By examining cancer cases over time, as well as their distribution by age group and gender, we have identified key patterns, such as the consistently high cancer rates in Department 59, particularly for colorectal and lung cancers. The age group most affected—between 45 and 74—mirrors national trends and highlights the need for targeted prevention, early detection, and treatment strategies for this demographic.

        However, there are a few limitations in the dataset that might have influenced the analysis. One of the challenges is the uniform distribution of data across regions and demographic groups, which, while balanced, could potentially mask disparities or localized healthcare issues. This even distribution may limit the ability to detect specific trends or anomalies that could better inform resource allocation and interventions, particularly in underserved areas.

        Additionally, the dataset only includes individuals who are actively engaged with the healthcare system, meaning that unreported or undiagnosed cases may not be represented. Furthermore, aggregating the data into broad categories (Levels 1, 2, and 3) limits the granularity of analysis for more specific cancer subtypes, which could provide deeper insights into particular healthcare challenges.

        Finally, the dataset spans the years 2015 to 2022, which, while helpful, might not capture long-term healthcare trends or the impact of more recent healthcare policies. Despite these limitations, the data provides a solid foundation for understanding national cancer trends and offers a starting point for further research and public health initiatives aimed at addressing the growing burden of cancer in France.
    """)