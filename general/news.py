import streamlit as st
from gnews import GNews
import pandas as pd
import requests
from newspaper import Article

def fetch_full_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article

st.title("Latest News on Heart Health")

if 'news' not in st.session_state:
    st.session_state.news = None

google_news = GNews(language="en", country="US", period="7d", max_results=10)

keyword = "heart health"

google_news.language = 'english'

google_news.country = 'United States'

if st.button("Search News", use_container_width=True):
    with st.spinner("Fetching news..."):
        st.session_state.news = google_news.get_news(keyword)

if st.session_state.news:
    df = pd.DataFrame(st.session_state.news)
    df = df.rename(columns={
        "title": "Title",
        "description": "Description",
        "published date": "Published Date",
        "publisher": "Publisher",
        "url": "URL",
        "image": "Image"
    })

    # Display news
    st.subheader(f"Top News for '{keyword}'")
    for _, article in df.iterrows():
        st.markdown(f"### [{article['Title']}]({article['URL']})")
        st.write(f"**Publisher:** {article['Publisher']['title']}")
        st.write(f"**Published Date:** {article['Published Date']}")
        st.write(article['Description'])
        st.markdown("---")

elif st.session_state.news is not None:
    st.warning("No news found for the given keyword.")

st.markdown("""
<style>
.stContainer {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin-bottom: 20px;
}
.stButton>button {
    float: right;
}
</style>
""", unsafe_allow_html=True)
