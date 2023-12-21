import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import correlation
def pearson(user_experience,user_skills):
    jobs_df_c = pd.read_csv('data2.csv')
    user_job_location = 'Pune'
    filtered_jobs_df_c = jobs_df_c[(jobs_df_c['experience'].apply(lambda x: int(x.split('-')[0])) >= user_experience)]
    filtered_jobs_df_c = filtered_jobs_df_c.assign(location_similarity=np.where(filtered_jobs_df_c['location'].apply(lambda x: x[0]) == user_job_location, 1, 0))
    filtered_jobs_df_c = filtered_jobs_df_c.assign(location_similarity=filtered_jobs_df_c['location_similarity'] * 0.1) # reduce the weight of location similarity
    filtered_jobs_df_c = filtered_jobs_df_c.drop(columns=['job_title']) # remove the job title column
    count_vect = CountVectorizer()
    skills_bow = count_vect.fit_transform(filtered_jobs_df_c['skills'].apply(lambda x: ' '.join(eval(x))))
    user_skills_bow = count_vect.transform([' '.join(user_skills)])
    pearson_sim = 1 - np.apply_along_axis(correlation, 1, skills_bow.toarray(), user_skills_bow.toarray().T)
    filtered_jobs_df_c = filtered_jobs_df_c.assign(similarity=pearson_sim.flatten())
    filtered_jobs_df_c = filtered_jobs_df_c.sort_values(['similarity', 'location_similarity', 'experience'], ascending=[False, False, True])
    # filtered_jobs_df_c = filtered_jobs_df_c.drop(columns=['location_similarity','url','Unnamed:8'])
    filtered_jobs_df_c = filtered_jobs_df_c.drop(columns=['location_similarity','url','Unnamed: 8'])
    recommended_jobs = filtered_jobs_df_c.head(5)
    table_html = recommended_jobs.to_html(index=False)
    return table_html