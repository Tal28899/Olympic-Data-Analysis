import pandas as pd
import streamlit as st
@st.cache_data
def preprocess(df,region_df):
    # Masking the dataframe summer olympics only
    df= df[df['Season'] == 'Summer']
    #droping the duplicate rows
    df = df.drop_duplicates()
    # merging 
    df=df.merge(region_df, on = 'NOC', how ='left')
    # one hot encoding
    df=pd.concat([df,pd.get_dummies(df['Medal'],dtype=(int))],axis=1)
    return df
