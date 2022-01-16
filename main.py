import streamlit as st
import pandas as pd
import numpy as np

import altair as alt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import plotly.graph_objects as go


#st.image(" COVID-19.jpg", width = 800)
import base64

main_bg = "covid_19.jpeg"
main_bg_ext = "jpeg"

side_bg = "covid_19.jpeg"
side_bg_ext = "jpeg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Add a title
st.title('Number of New Cases and Deaths of Covid-19 in The World Wide')
# Add some text
st.text('This app is designed to give important information about covid_19') 
st.text('during 01/2020 - 04/2021')

dataset_name=st.sidebar.selectbox("Select Dateset",("covid_19 in The world wide ","Covid_19 cases in the world","Covid_19 deaths in the world"))


if dataset_name =="covid_19 in The world wide ":
    st.write(dataset_name)
    df1=pd.read_csv("covid_19.csv")
    st.sidebar.text("what do you want to display")
    if st.sidebar.checkbox("countries effected"):
        st.map(df1)
    if st.sidebar.checkbox("countries and the level of effection"):
        fig = px.choropleth(df1, locations=df1['Country'],color=df1['New_cases']#, hover_data= ['New_cases','New_deaths'],
                   ,locationmode='country names',hover_name=df1['Country'],
                    color_continuous_scale=px.colors.sequential.Redor, width=800, height=500)
      
        fig.update_layout(title='Number of Covid 19 New Cases around the world')

        st.plotly_chart(fig)

elif dataset_name =="Covid_19 cases in the world":
    st.write(dataset_name)
    st.sidebar.text("what do you want to display")
    if st.sidebar.checkbox("line charts of new cases depending on countries"):
        st.text('This graph shows the number of new cases in coutries :')
        cases=pd.read_csv("cases.csv")
        subset_data = cases
        country_name_input = st.multiselect(
        'Country name',
        cases.groupby('Country').count().reset_index()['Country'].tolist())
        if len(country_name_input) > 0:
             subset_data = cases[cases['Country'].isin(country_name_input)]
        total_cases_graph  =alt.Chart(subset_data).transform_filter(alt.datum.New_cases > 0).mark_line().encode(
        x=alt.X('month(Date_reported)'),
        y=alt.Y('sum(New_cases):Q',  title='New cases'),
        color='Country',
        tooltip = 'sum(New_cases)',
        ).properties(
        width=800,
        height=500
        ).configure_axis(
        labelFontSize=17,
        titleFontSize=20)
        st.altair_chart(total_cases_graph)

    if st.sidebar.checkbox("line charts of new cases depending on date"):
        date=pd.read_csv("covid19_by_date.csv")  
        date.set_index(date['Country'],inplace=True)
        date.drop('Country',axis='columns', inplace=True)    
        all_columns_names = date.columns.tolist()
        col_y = st.multiselect('Which date do you want to show', all_columns_names)
        fig = make_subplots(shared_xaxes=True)

        for i in range(len(col_y)):
            fig.add_trace(go.Line(x = date.index, y = date[col_y[i]],name=col_y[i]))
        st.plotly_chart(fig)

else:
    st.write(dataset_name)
    st.sidebar.text("what do you want to display")
    if st.sidebar.checkbox("line charts of new deaths depending on countries"):
        st.text('This graph shows the number of new deaths in coutries :')
        cases=pd.read_csv("cases.csv")
        subset_data = cases
        country_name_input = st.multiselect(
        'Country name',
        cases.groupby('Country').count().reset_index()['Country'].tolist())
        if len(country_name_input) > 0:
             subset_data = cases[cases['Country'].isin(country_name_input)]
        total_cases_graph  =alt.Chart(subset_data).transform_filter(alt.datum.New_cases > 0).mark_line().encode(
        x=alt.X('month(Date_reported):O'),
        y=alt.Y('sum(New_deaths):Q',  title='New deaths'),
        color='Country',
        tooltip = 'sum(New_deaths)',
        ).properties(
        width=800,
        height=500
        ).configure_axis(
        labelFontSize=17,
        titleFontSize=20)
        st.altair_chart(total_cases_graph)
    if st.sidebar.checkbox("line charts of new deaths depending on date"):
        date_deaths=pd.read_csv("covid19_Deaths_byDate.csv")
        date_deaths.set_index(date_deaths['Country'],inplace=True)
        date_deaths.drop('Country',axis='columns', inplace=True)    
        all_columns_names = date_deaths.columns.tolist()
        col_y = st.multiselect('Which date do you want to show', all_columns_names)
        fig = make_subplots(shared_xaxes=True)

        for i in range(len(col_y)):
            fig.add_trace(go.Line(x = date_deaths.index, y = date_deaths[col_y[i]],name=col_y[i]))
        st.plotly_chart(fig)


