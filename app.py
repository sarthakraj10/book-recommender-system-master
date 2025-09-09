import streamlit as st
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Page configuration
st.set_page_config(page_title="📚 Book Recommender", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #00a65a;'>📚 Book Recommender System</h1>", unsafe_allow_html=True)
st.markdown("---")

# Tabs for navigation (only Home and Recommend)
tabs = st.tabs(["🏠 Home", "🔍 Recommend"])

# --- Tab 1: Home ---
with tabs[0]:
    st.subheader("🔥 Top 50 Popular Books")
    cols = st.columns(4)

    for idx in range(len(popular_df)):
        with cols[idx % 4]:
            st.image(popular_df['Image-URL-M'].values[idx], use_container_width=True)
            st.markdown(f"**{popular_df['Book-Title'].values[idx]}**")
            st.markdown(f"*by {popular_df['Book-Author'].values[idx]}*")
            st.markdown(f"⭐ {popular_df['avg_rating'].values[idx]} | 🗳️ {popular_df['num_ratings'].values[idx]}")

# --- Tab 2: Recommend ---
with tabs[1]:
    st.subheader("🔍 Get Book Recommendations")

    # Autocomplete book name input using selectbox
    book_list = pt.index.values
    user_input = st.selectbox("Search and select a book:", book_list)

    if st.button("Recommend"):
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        st.markdown("### 📖 Recommended Books")
        rec_cols = st.columns(4)

        for i, col in zip(similar_items, rec_cols):
            temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
            title = temp_df['Book-Title'].values[0]
            author = temp_df['Book-Author'].values[0]
            image_url = temp_df['Image-URL-M'].values[0]

            with col:
                st.image(image_url, use_container_width=True)
                st.markdown(f"**{title}**")
                st.markdown(f"*{author}*")
