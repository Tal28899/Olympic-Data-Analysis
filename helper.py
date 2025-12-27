import pandas as pd
import streamlit as st
#data loading
@st.cache_data
def data_load(file1,file2):
    df=pd.read_csv(file1)
    region_df=pd.read_csv(file2)
    return df , region_df

# medal tally dataframe
@st.cache_data
def med_tell(df,selected_year,selected_country):
    # making data on the basis user selection
    if selected_year != 'Overall':
        df=df[df['Year']==selected_year]
        year_groupby = 1
    if selected_country != 'Overall':
        df=df[df['region'] == selected_country]
    
        
    if selected_year == 'Overall' and selected_country != 'Overall':
        medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
        medal_tally=medal_tally.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(['Gold']).reset_index()
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze'] 
    else:
        medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
        medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values(['Gold','Silver','Bronze'],ascending = False).reset_index()
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze'] 
    
    return medal_tally

# making dropdown list of years and countries
@st.cache_data
def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country
# fetching data over time
@st.cache_data
def data_over_time(df,col):
    if col =='Name':
        df=df.rename(columns={'Name': 'Athletes'})
        col  = 'Athletes'
    time_wise_data=df.drop_duplicates(['Year',col]).value_counts(['Year']).reset_index().sort_values(['Year'])
    time_wise_data=time_wise_data.rename(columns={'Year' : 'Editions','count' : col})
    return time_wise_data
#pivot table
@st.cache_data  
def pivot_table(df):
    pivot_t=df[['Year','Sport','Event']].drop_duplicates()
    pivot_t=pivot_t.pivot_table(index='Sport',columns = 'Year',values = 'Event',aggfunc='count').fillna(0).astype('int')
    return pivot_t

# list of sports
@st.cache_data
def fetch_sports(df):
    sports=df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')
    return sports

# fetching top athletes
@st.cache_data
def top_athle(df,sport):
    tem_df = df.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        tem_df = tem_df[tem_df['Sport'] == sport]
    tem_df=tem_df[['Name','Sport','region','Medal']].groupby(['Sport','region','Name']).count()['Medal'].reset_index()
    tem_df=tem_df.sort_values('Medal',ascending = False)
    # modifying data frame
    tem_df=tem_df.rename(columns={'region' : 'Coutry', 'Name' :'Athlete','Medal' : 'Medals'})
    tem_df = tem_df.reset_index(drop=True)
    tem_df.index += 1
    
    return tem_df.head(10)
# Country medal tally over time
@st.cache_data
def country_medals(df,region):
    tem_df=df.dropna(subset=['Medal'])
    tem_df=tem_df.drop_duplicates(['Team',	'NOC',	'Games',	'Year',		'City',	'Sport',	'Event',	'Medal'])
    if region != 'Overall': 
        tem_df=tem_df[tem_df['region'] == region]
        if tem_df.empty:
            return None 
    tem_df=tem_df.groupby('Year').count()['Medal'].reset_index()
    return tem_df 
# country performance in different sports
@st.cache_data
def country_medal_hm(df,country):
    tem_df=df.dropna(subset=['Medal'])
    tem_df=tem_df.drop_duplicates(['Team',	'NOC',	'Games',	'Year',		'City',	'Sport',	'Event',	'Medal'])
    if country != 'Overall':
        tem_df=tem_df[tem_df['region'] == country]
        if tem_df.empty:
            return None 
    tem_df=tem_df[['Year','Sport','region','Medal']]# i will not use drop_duplicate here because many athletes from same country ,year,can compete for same sport and win medal                 
    tem_df=tem_df.pivot_table(index='Sport',columns='Year',values = 'Medal',aggfunc='count' ) .fillna(0).astype(int) 
    return tem_df
#fetching top athletes of a country 
@st.cache_data
def top_player(df,selected_country):
    tem_df=df.dropna(subset=['Medal'])
    tem_df=tem_df[tem_df['region']==selected_country]
    if tem_df.empty:
        return None
    tem_df=tem_df[['Name','region','Medal','Sport']].groupby(['region','Name','Sport']).count()['Medal'].reset_index()
    if tem_df.empty:
        return None
    tem_df=tem_df.sort_values('Medal',ascending = False)
    tem_df=tem_df.drop('region',axis=1)
    tem_df=tem_df.rename(columns={'Name' : 'Athlete','Medal':'Medals'})
    tem_df = tem_df.reset_index(drop=True)
    tem_df.index += 1
    return tem_df.head(10)
# age distribution 

@st.cache_data
def age_analysis(df):
    athlete_df= df.drop_duplicates(subset=['Name','region'])
    Overall_age=athlete_df['Age'].dropna()
    Gold_age=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    Silver_age=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    Bronze_age=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    return Overall_age,Gold_age,Silver_age,Bronze_age
# age distribution of athletes winning gold wrt sport
@st.cache_data
def gold_win_age(df,sports):
    Ages=[]
    S_name=[]
    for sport in sports:
        tem_df= df.drop_duplicates(subset=['Name','region'])
        tem_df=tem_df[tem_df['Sport'] == sport]
        age_series=tem_df[tem_df['Medal'] == 'Gold']['Age'].dropna()
        if len(age_series) >= 2 and age_series.nunique() >= 2:
            Ages.append(age_series)
            S_name.append(sport)
    return Ages,S_name

@st.cache_data    #making a scatter plot of athletes height and weight
def avg_weight_height(df,sport):
    athlete_df= df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal']=athlete_df['Medal'].fillna('No Medal')
    if sport != 'Overall':
        athlete_df=athlete_df[athlete_df['Sport'] == sport]
    return athlete_df 