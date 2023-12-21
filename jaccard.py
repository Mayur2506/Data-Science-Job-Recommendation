import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import pairwise_distances
def jaccard(user_experience,user_skills):
    # Load the job dataset into a Pandas DataFrame
    jobs_df = pd.read_csv('data2.csv')

    # Define the user's skills and years of experience
    # user_skills = ['Performance tuning', 'PGDCA', 'code', 'technical', 'developing', 'cloud', 'Coding', 'web']
    # user_experience = 2

    # Define the user's preferred job location
    user_job_location = 'Pune'

    # Filter the jobs dataset based on the user's years of experience and preferred job location
    filtered_jobs_df = jobs_df[(jobs_df['experience'].apply(lambda x: int(x.split('-')[0])) >= user_experience)]
    filtered_jobs_df = filtered_jobs_df.assign(location_similarity=np.where(filtered_jobs_df['location'].apply(lambda x: x[0]) == user_job_location, 1, 0))
    filtered_jobs_df = filtered_jobs_df.assign(location_similarity=filtered_jobs_df['location_similarity'] * 0.1) # reduce the weight of location similarity
    filtered_jobs_df = filtered_jobs_df.drop(columns=['job_title']) # remove the job title column

    # Convert the skills attribute into a bag-of-words representation
    count_vect = CountVectorizer()
    skills_bow = count_vect.fit_transform(filtered_jobs_df['skills'].apply(lambda x: ' '.join(eval(x))))
    skills_dense = skills_bow.toarray()

    # Convert the user's skills into a bag-of-words representation
    user_skills_bow = count_vect.transform([' '.join(user_skills)])
    user_skills_dense = user_skills_bow.toarray()

    # Calculate the Jaccard similarity between the user's skills and the job skills
    jaccard_sim = 1 - pairwise_distances(skills_dense, user_skills_dense, metric='jaccard')

    # Add the similarity score to the DataFrame
    filtered_jobs_df = filtered_jobs_df.assign(similarity=jaccard_sim.flatten())

    # Sort the jobs by similarity, location similarity, and experience difference
    filtered_jobs_df = filtered_jobs_df.sort_values(['similarity', 'location_similarity', 'experience'], ascending=[False, False, True])
    
    recommended_jobs = filtered_jobs_df.head(5)
    table_html = recommended_jobs.to_html(index=False)
    return table_html