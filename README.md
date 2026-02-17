# 🎬 Movie Recommendation System with FastAPI & Streamlit

A full-stack, end-to-end movie recommender application. This project features a **hybrid recommendation strategy** by combining a local Content-Based Machine Learning model with real-time metadata discovery from the TMDB API.

---

## 🚀 Features

* 🏠 **Live Home Feed**: Dynamic categories (Trending, Popular, Top Rated, Upcoming) powered by TMDB's 2026 data.
* 🔍 **Smart Search**: Keyword-based search with real-time posters and movie details.
* 🤖 **Hybrid Recommendations**:
    * **Content-Based (TF-IDF)**: Uses NLP and Cosine Similarity on a 45k+ dataset to find plot-similar films.
    * **Genre Discovery**: Live TMDB "More Like This" results based on movie categories.
* 📱 **Responsive UI**: Modern grid layout with adjustable column counts and a dedicated "Detail View" for every movie.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI (Python)
* **Frontend**: Streamlit
* **Machine Learning**: Scikit-learn (TF-IDF Vectorizer, Cosine Similarity), Pandas, NumPy
* **API**: The Movie Database (TMDB)

---

## 💻 How to Run

1. **Start Backend**: `uvicorn main:app --reload`
2. **Start Frontend**: `streamlit run app.py`



--
## 📂 Project Structure

* `main.py`: FastAPI backend containing the recommendation logic and API routes.
* `app.py`: Streamlit frontend for the user interface.
* `model.ipynb`: Data processing and TF-IDF model generation notebook.
* `df.pkl`, `tfidf_matrix.pkl`, `indices.pkl`: Exported ML components.
* `requirements.txt`: List of required Python libraries.
--

### 🎨 Why this format works:

* **Main Title (`#`)**: This creates the large top header with the movie clapboard icon.
* **Dividers (`---`)**: These create the thin gray lines that give the page a clean "sectioned" look.
* **Icon List (`* 🏠`)**: Combining bullet points with emojis makes the features section easy to scan visually.
* **Code Blocks (Backticks)**: Wrapping your commands in triple backticks (```) puts them in a dark box, making them look like a real terminal.
* **Bold & Links**: Highlighting key tech like **FastAPI** and providing clickable links for the docs adds a professional touch.



**Would you like me to help you add a "Demo Video" or "Screenshots" section to show off the UI in the README?**
