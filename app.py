import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="🎬 Movie Recommendation App", page_icon="🎥", layout="centered")

# -----------------------------
# Mode Selection (Dark / Light)
# -----------------------------
mode = st.radio("🌗 Choose Theme Mode:", ["Dark Mode", "Light Mode"])

if mode == "Dark Mode":
    bg_url = "https://images.unsplash.com/photo-1502136969935-8d0710f237f7?auto=format&fit=crop&w=1650&q=80"
    text_color = "white"
    box_color = "rgba(0, 0, 0, 0.65)"
else:
    bg_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1650&q=80"
    text_color = "black"
    box_color = "rgba(255, 255, 255, 0.75)"

# -----------------------------
# Background Styling
# -----------------------------
def set_bg_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .block-container {{
            backdrop-filter: blur(6px);
            background-color: {box_color};
            border-radius: 20px;
            padding: 25px;
        }}
        h1, h2, h3, h4, h5, h6, label, p, span, div {{
            color: {text_color} !important;
        }}
        .stButton button {{
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
        }}
        .stButton button:hover {{
            background-color: #ff7777;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_style()

# -----------------------------
# App Title
# -----------------------------
st.title("🎬 Movie Recommendation App")
st.markdown("Find movies you’ll love — and build your own playlist! 🍿")

# -----------------------------
# Movie Data
# -----------------------------
movies = {
    "Funny": {
        "Bollywood": [
            "Hera Pheri", "Dhamaal", "3 Idiots", "Welcome", "Chupke Chupke",
            "Golmaal", "Munna Bhai M.B.B.S.", "Fukrey", "Total Dhamaal", "Housefull"
        ],
        "Hollywood": [
            "The Hangover", "Superbad", "21 Jump Street", "Johnny English", "Ted",
            "Dumb and Dumber", "Central Intelligence", "Deadpool", "Yes Man", "The Mask"
        ]
    },
    "Action": {
        "Bollywood": [
            "War", "Pathaan", "Singham", "Dhoom 3", "Tiger Zinda Hai",
            "Baaghi", "Ghajini", "Don 2", "Kick", "Holiday"
        ],
        "Hollywood": [
            "John Wick", "Mad Max: Fury Road", "The Dark Knight", "Inception", "Avengers: Endgame",
            "Mission Impossible", "Gladiator", "Die Hard", "Fast & Furious 7", "The Matrix"
        ]
    },
    "Romance": {
        "Bollywood": [
            "Dilwale Dulhania Le Jayenge", "Jab We Met", "Ae Dil Hai Mushkil", "Mohabbatein", "Veer-Zaara",
            "Yeh Jawaani Hai Deewani", "Kal Ho Naa Ho", "Tamasha", "Kabir Singh", "Barfi!"
        ],
        "Hollywood": [
            "The Notebook", "La La Land", "Titanic", "Me Before You", "Crazy Rich Asians",
            "To All the Boys I’ve Loved Before", "About Time", "P.S. I Love You", "Notting Hill", "500 Days of Summer"
        ]
    }
}

# -----------------------------
# Movie Selection
# -----------------------------
genre = st.selectbox("🎭 Choose movie type", list(movies.keys()))
region = st.selectbox("🌍 Choose region", ["Bollywood", "Hollywood"])

if st.button("🎬 Get Recommendations"):
    st.subheader(f"Top 10 {region} {genre} Movies:")
    for i, movie in enumerate(movies[genre][region], start=1):
        st.markdown(f"**{i}. {movie}**")

# -----------------------------
# Playlist Section
# -----------------------------
st.markdown("---")
st.header("🎵 Your Personal Playlist")

if "playlist" not in st.session_state:
    st.session_state.playlist = []

movie_to_add = st.text_input("🎞️ Add a movie to your playlist:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Add Movie"):
        if movie_to_add:
            st.session_state.playlist.append(movie_to_add)
            st.success(f"✅ '{movie_to_add}' added to your playlist!")
        else:
            st.warning("⚠️ Please enter a movie name first.")
with col2:
    if st.button("🗑️ Clear Playlist"):
        st.session_state.playlist = []
        st.info("Playlist cleared.")

if st.session_state.playlist:
    st.subheader("🎬 Your Playlist:")
    for idx, movie in enumerate(st.session_state.playlist, start=1):
        st.markdown(f"**{idx}. {movie}**")
else:
    st.caption("Your playlist is empty. Add your favorite movies!")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
