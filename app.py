import streamlit as st
import pandas as pd
from altair.vega import autosize

import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df= pd.read_csv('athlete_events.csv')
region_df= pd.read_csv('noc_regions.csv')

df = preprocess.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://cdn.freebiesupply.com/logos/large/2x/olympic-logo-png-transparent.png')
user_menu= st.sidebar.radio(
    'select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)
# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Years",years)
    selected_country = st.sidebar.selectbox("Select country",country)

    medal = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Medal Tally ')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Tally in' + str(selected_year))
    st.table(medal)
if user_menu == 'Overall Analysis':

    edtions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athlete = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Edition")
        st.title(edtions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(event)
    with col2:
        st.header("Athlete")
        st.title(athlete)
    with col3:
        st.header("Nation")
        st.title(nation)

    nations_over_time=helper.data_over_time(df,'region')

    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the year")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')

    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Participating Events over the year")
    st.plotly_chart(fig)

    #athleats over time

    athlete_over_time=helper.data_over_time(df,'Name')

    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athlete over the year")
    st.plotly_chart(fig)

    st.title("No. of Events over time of every sports")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Sucessful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select Sport',sport_list)

    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+' Medal Tally over Year')
    st.plotly_chart(fig)

    st.title(selected_country+' Excels in the following sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of '+selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == "Athlete-wise Analysis":

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x=[]
    name=[]
    famous_sports = ['BasketBall', 'Judo', 'Football', 'Tug-of-war', 'Athletics',
                     'Swimming', 'Badmintion', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting',
                     'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
                     'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming',
                     'Table Tennis', 'Baseball', 'Rhytmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        mask = (athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold') & df['Age'].notna()
        temp = athlete_df.loc[mask, 'Age']
        if not temp.empty:
            x.append(temp)
            name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age w.r.t sports")
    st.plotly_chart(fig)

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title('Height Vs Weight')
    selected_sport  = st.selectbox('Select Sports',sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax= sns.scatterplot(x='Weight',y='Height',data=temp_df,hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men Vs Women Participation over the Year')
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False,width=800,height=600)
    st.plotly_chart(fig)
