import plotly.figure_factory as ff
import streamlit as st
import seaborn as sns
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
# widening the layout
st.set_page_config(layout="wide")

# data loading
df,region_df = helper.data_load('athlete_events.csv','noc_regions.csv')


# preprocessing
df = preprocessor.preprocess(df,region_df)

#giving different Options to user
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis'))
#Option Selection
if user_menu == 'Medal Tally' :
    # making dropdown list of years and countries
    years,countries = helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select a year',years)
    selected_country=st.sidebar.selectbox('Select a country',countries)
    #medal tally
    med_tally = helper.med_tell(df,selected_year,selected_country)
    #Displaying different titles based on user choice
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'Medal Tally in {selected_year} Olympics ')
    if selected_year == 'Overall' and selected_country != 'Overall':    
        st.title(f'Medal Tally of {selected_country} in Olympics ')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f'Medal Tally of {selected_country} in {selected_year} Oylmpics')        

    st.table(med_tally)
# Overall Analysis
if user_menu == 'Overall Analysis':
    st.title('Top Stats :')
    Editions=df['Year'].unique().shape[0] -1
    Hosts=df['City'].unique() .shape [0] 
    Sports=df['Sport'].unique().shape [0]
    Events=df['Event'].unique().shape[0]
    Nations=df['region'].unique().shape[0]
    Athletes=df['Name'].unique().shape[0]
    #making columns
    col1, col2, col3  = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(Editions)
    with col2:
        st.header('Sports')
        st.title(Sports)    
    with col3:
        st.header('Hosts')
        st.title(Hosts)
    # Another row of colmns   
    col1, col2, col3  = st.columns(3)
    with col1:
        st.header('Nations')
        st.title(Nations)
    with col2:
        st.header('Athletes')
        st.title(Athletes)    
    with col3:
        st.header('Events')
        st.title(Events)
                  
    # plotting  graphs
    #1)
    st.title('Participating Nations Over Time ')     
    time_wise_nations = helper.data_over_time(df,'NOC')
    fig = px.line(time_wise_nations,x='Editions',y='NOC')
    st.plotly_chart(fig)          

    st.title('No of Events Over Time ')     
    time_wise_events = helper.data_over_time(df,'Event')
    fig = px.line(time_wise_events,x='Editions',y='Event')
    st.plotly_chart(fig)          

    st.title('No of Athletes Over Time ')     
    time_wise_athletes = helper.data_over_time(df,'Name')
    fig = px.line(time_wise_athletes,x='Editions',y='Athletes')
    st.plotly_chart(fig) 
    # heatmap
    st.title('No, of Events over time(Per_Sport)')
    pivot_t = helper.pivot_table(df)
    fig,ax = plt.subplots(figsize =(20,20))
    sns.heatmap(pivot_t,ax=ax,annot=True)
    st.pyplot(fig)
    # title
    st.title('Top 10 Athletes in Olympic History') 
    #making a dropdow for user to select sport
    sports_list = helper.fetch_sports(df)
    selected_sport=st.selectbox('Select a sport',sports_list)
    # fetching the top athletes
    top_athle_df=helper.top_athle(df,selected_sport)
    st.table(top_athle_df)
# selecting option
if user_menu == 'Country wise Analysis':
    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0,'Overall')
    selected_country=st.sidebar.selectbox('Select a country',countries)
    if selected_country == 'Overall':
        st.title('Total Medals Given per year')
    else:
        st.title(f'{selected_country} Medal Tally Over Time')    
    country_medal_tally = helper.country_medals(df,selected_country)
    if country_medal_tally is None:
        st.warning(f'{selected_country}  donot  won  any  medal')
    else:
        fig=px.line(country_medal_tally,x='Year',y='Medal')
        st.plotly_chart(fig)
    # country performance in different sports
    
    country_pivot_t=helper.country_medal_hm(df,selected_country)
    if selected_country == 'Overall':
        st.title('Total Medals given per year per sport')
    else:
        st.title(f'{selected_country} Performance in different sport overtime')
    # plotting heatmap
    if country_pivot_t is None:
        st.warning(f'{selected_country}  donot  won  any  medal')
    else:    
        fig,ax = plt.subplots(figsize=(25,25))
        sns.heatmap(country_pivot_t,ax=ax,annot=True)
        st.pyplot(fig)
    # fetching top athletes of a country :
    if selected_country!='Overall':
        st.title(f'Top 10 Athletes of {selected_country}')
        top_players_df=helper.top_player(df,selected_country)
        if top_players_df is None:
            st.warning(f'{selected_country}  donot  won  any  medal')
        st.table(top_players_df)
#Option selection
if user_menu == "Athlete wise Analysis":
    # age distribution of athletes
    Overall_age,Gold_age,Silver_age,Bronze_age =helper.age_analysis(df)
    fig=ff.create_distplot([Overall_age,Gold_age,Silver_age,Bronze_age],['Overall age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age of Athletes')
    
    st.plotly_chart(fig)
    # age distribution of athletes winning gold wrt sport
    
    sports=df['Sport'].unique().tolist()
    Ages,Sport_name=helper.gold_win_age(df,sports)
    fig=ff.create_distplot(Ages,Sport_name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age of Athletes wrt sport(Gold Winning)')
    
    st.plotly_chart(fig)

    #making a dropdow for user to select sport
    sports_list = helper.fetch_sports(df)
    selected_sport=st.selectbox('Select a sport',sports_list)
    athlete_df=helper.avg_weight_height(df,selected_sport)
    # making a scatterplot
    fig,ax = plt.subplots(figsize=(10,10))     
    ax =sns.scatterplot( x =athlete_df['Weight'], y =athlete_df['Height'],
                        hue=athlete_df['Medal'],style=athlete_df['Sex'],s=60)
    st.pyplot(fig)