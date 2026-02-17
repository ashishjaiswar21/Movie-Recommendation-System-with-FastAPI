import streamlit as st
import httpx
import asyncio

# --- CONFIGURATION ---
API_BASE_URL = "https://movie-recommendation-system-with-fastapi.onrender.com" or "http://127.0.0.1:8000"

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize session state for the selected movie
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# --- API HELPERS ---
async def get_from_api(endpoint: str, params: dict = None):
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(f"{API_BASE_URL}{endpoint}", params=params)
            return response.json() if response.status_code == 200 else None
        except Exception:
            return None

# --- UI COMPONENTS ---
def movie_card(movie_data, idx, cols_count):
    """Renders an individual movie card with an 'Open' button."""
    # Handle different keys for Search Bundle vs Home Feed
    m = movie_data.get('tmdb') if 'tmdb' in movie_data else movie_data
    if not m: return

    poster = m.get('poster_url') or "https://via.placeholder.com/500x750?text=No+Poster"
    st.image(poster, use_container_width=True)
    st.markdown(f"**{m.get('title')}**")
    
    # Selecting a movie updates session state and re-runs the app
    if st.button("Open", key=f"btn_{m.get('tmdb_id')}_{idx}"):
        st.session_state.selected_movie = m.get('title')
        st.rerun()

def render_grid(movie_list, cols_count):
    if not movie_list:
        st.info("No movies found.")
        return
    
    rows = [movie_list[i:i + cols_count] for i in range(0, len(movie_list), cols_count)]
    for row in rows:
        cols = st.columns(cols_count)
        for i, movie in enumerate(row):
            with cols[i]:
                movie_card(movie, i, cols_count)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏠 Menu")
    if st.button("Home"):
        st.session_state.selected_movie = None
        st.rerun()
    
    st.divider()
    st.markdown("### 🎞️ Home Feed Settings")
    category = st.selectbox("Category", ["trending", "popular", "top_rated", "upcoming"])
    grid_cols = st.slider("Grid columns", 4, 8, 4)

# --- MAIN INTERFACE ---
st.title("🎬 Movie Recommender")
st.caption("Type keyword → dropdown suggestions → matching results → open → details + recommendations")

# Mode 1: Detailed Movie View (If a movie is selected)
if st.session_state.selected_movie:
    with st.spinner("Loading movie details..."):
        bundle = asyncio.run(get_from_api("/movie/search", {"query": st.session_state.selected_movie}))
        
        if bundle:
            details = bundle['movie_details']
            
            # Header: Poster and Metadata
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(details['poster_url'], use_container_width=True)
            with c2:
                st.header(details['title'])
                st.write(f"**Release:** {details['release_date']}")
                st.write(f"**Genres:** {', '.join([g['name'] for g in details['genres']])}")
                st.subheader("Overview")
                st.write(details['overview'])
            
            # Backdrop Image (Just like in your screenshot)
            if details.get('backdrop_url'):
                st.subheader("Backdrop")
                st.image(details['backdrop_url'], use_container_width=True)
            
            st.divider()
            st.subheader("✅ Recommendations")
            
            # TF-IDF Recommendations
            st.markdown("### 🔍 Similar Movies (Content-Based)")
            render_grid(bundle['tfidf_recommendations'], grid_cols)
            
            # Genre Recommendations
            st.markdown("### 🎭 More Like This (By Genre)")
            render_grid(bundle['genre_recommendations'], grid_cols)
        else:
            st.error("Movie not found.")
            if st.button("Back to Home"):
                st.session_state.selected_movie = None
                st.rerun()

# Mode 2: Home Feed (Default)
else:
    search_query = st.text_input("Search by movie title (keyword)", placeholder="Type: avenger, batman, love...")
    
    if search_query:
        if st.button("Search"):
            st.session_state.selected_movie = search_query
            st.rerun()
    
    st.divider()
    st.subheader(f"🏠 Home — {category.capitalize()}")
    with st.spinner("Fetching feed..."):
        home_feed = asyncio.run(get_from_api("/home", {"category": category, "limit": 24}))
        render_grid(home_feed, grid_cols)