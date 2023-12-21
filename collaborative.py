import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import random
def py(userid):
    df = pd.read_csv('./sim5000new.csv')
    userdf=pd.read_csv("./survey_results_public.csv")
    df_list = df.values.tolist()
    user = userid
    m1=max(df_list[user][1:user+1])
    m2=max(df_list[user][user+2:])
    ma=max(m1,m2)
    # print(ma)
    suser=(df_list[user].index(ma)-1)
    respondent = userdf[userdf['Respondent'] == suser]
    # experience=int((respondent['YearsCoding'].split('-'))[0])
    experience=respondent['YearsCoding']
    years_of_exp =int(experience.astype(str).str.split('-', expand=True)[0])
    # print(experience)
    # experience=int(experience[0])
    skills=respondent['LanguageWorkedWith'].astype(str).str.replace(';', ',')
    r = userdf[userdf['Respondent'] == user]
    cols_to_display = ['LanguageWorkedWith', 'PlatformWorkedWith', 'DatabaseWorkedWith','FrameworkWorkedWith','DevType']
    display_df = respondent[cols_to_display]
    display_df1= r[cols_to_display]
    table_html = display_df.to_html(index=False)
    table_html1 = display_df1.to_html(index=False)
    return table_html,table_html1,years_of_exp,skills