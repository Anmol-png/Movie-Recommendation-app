import streamlit as st

st.set_page_config(page_title="Movie Recommendation App 🎥", page_icon="🎬", layout="centered")

st.title("🎬 Movie Recommendation App")

st.markdown("Find movies you’ll love — and build your personal playlist!")

# -----------------------------
# Movie Database (simple demo)
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
# User selections
# -----------------------------
genre = st.selectbox("Choose movie type 🎭", list(movies.keys()))
region = st.selectbox("Choose region 🌍", ["Bollywood", "Hollywood"])

if st.button("Get Recommendations"):
    st.subheader(f"🎥 Top 10 {region} {genre} Movies:")
    recommended = movies[genre][region]
    for i, movie in enumerate(recommended, start=1):
        st.write(f"{i}. {movie}")

# -----------------------------
# Personal Playlist Section
# -----------------------------
st.markdown("---")
st.header("🎵 Your Personal Playlist")

if "playlist" not in st.session_state:
    st.session_state.playlist = []

movie_to_add = st.text_input("Add a movie to your playlist:")
if st.button("Add Movie"):
    if movie_to_add:
        st.session_state.playlist.append(movie_to_add)
        st.success(f"✅ '{movie_to_add}' added to your playlist!")
    else:
        st.warning("⚠️ Please enter a movie name first.")

if st.session_state.playlist:
    st.subheader("Your Playlist:")
    for idx, movie in enumerate(st.session_state.playlist, start=1):
        st.write(f"{idx}. {movie}")

    if st.button("Clear Playlist"):
        st.session_state.playlist = []
        st.info("🗑️ Playlist cleared.")
else:
    st.caption("Your playlist is empty. Add some movies you like!")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
