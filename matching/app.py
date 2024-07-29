import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import os

# File to store user data
DATA_FILE = 'users_data.csv'

# Load existing data or create a new DataFrame
if os.path.exists(DATA_FILE):
    users_df = pd.read_csv(DATA_FILE)
else:
    users_df = pd.DataFrame(columns=['username', 'age', 'interests'])

# Function to save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Function to display survey form
def display_survey():
    st.title("Interest Matching Form")
    
    username = st.text_input("Username")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    interests = st.text_area("Interests (comma-separated)")
    
    if st.button("Submit"):
        new_user = pd.DataFrame({
            'username': [username],
            'age': [age],
            'interests': [interests]
        })
        global users_df
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        save_data(users_df)
        st.success("Survey submitted successfully!")
        st.write(users_df)

# Function to display matching results
def display_matching():
    st.title("K-Nearest Neighbors Matching")
    
    username = st.text_input("Enter your username to find matches")
    
    if st.button("Find Matches"):
        user_data = users_df[users_df['username'] == username]
        if user_data.empty:
            st.error("User not found!")
        else:
            vectorizer = CountVectorizer()
            interests_matrix = vectorizer.fit_transform(users_df['interests'])
            
            knn = NearestNeighbors(n_neighbors=3, metric='cosine')
            knn.fit(interests_matrix)
            
            user_index = users_df[users_df['username'] == username].index[0]
            distances, indices = knn.kneighbors(interests_matrix[user_index], n_neighbors=4)
            
            match_indices = indices.flatten()[1:]
            matches = users_df.iloc[match_indices]
            
            st.write("Top Matches:")
            st.write(matches[['username', 'age', 'interests']])

# Streamlit main function
def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Go to", ["Survey", "Matching"])
    
    if option == "Survey":
        display_survey()
    elif option == "Matching":
        display_matching()

if __name__ == "__main__":
    main()
