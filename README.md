# 🎬 Movie Recommender System

A visually dynamic, **Streamlit-based** web app that recommends five similar movies based on your selection, powered by content-based filtering and enriched with real-time movie posters from the **TMDb API**. Built for scalability, portability, and style — with Docker, Google Drive integration, and an engaging neon-themed UI.

---

## 🚀 Features

- 🔍 **Content-Based Recommendations**: Suggests 5 similar movies using a precomputed **cosine similarity matrix** based on metadata like genres, cast, crew, and keywords.
- 🎨 **Stylish UI**: 
  - Neon-gradient animated background
  - **Orbitron** font styling
  - Custom buttons and cards styled via injected CSS
- 📦 **Efficient Model Management**:
  - `movies_dict.pkl` committed to GitHub (<3 MB)
  - `similarity.pkl` (>100 MB) hosted on **Google Drive**, downloaded dynamically at runtime via `gdown`
- 🖼️ **Poster Integration**: High-quality movie posters fetched live using **TMDb API**
- 🐳 **Dockerized Deployment**: Full containerization with a `Dockerfile` for consistent builds across environments
- ☁️ **Cloud Hosting with Render**:
  - Uses `render.yaml` to configure and trigger builds
  - Compatible with manual and automatic deployments via Git push

---

## 🧠 How It Works

1. **Preprocessing (Offline)**:
   - Movie metadata is processed and vectorized.
   - A cosine similarity matrix is computed and saved as `similarity.pkl`.

2. **Runtime (Online)**:
   - When a user selects a movie, the app fetches its index, looks up the top 5 similar entries using the preloaded similarity matrix.
   - Movie posters are retrieved in real-time via TMDb API.
   - The app displays recommendations with titles, images, and styled cards.

---

## 📁 Project Structure

├── app.py # Main Streamlit app
├── movies_dict.pkl # Lightweight movie metadata (stored in repo)
├── similarity.pkl # Large similarity matrix (loaded via Google Drive)
├── Dockerfile # Container setup
├── render.yaml # Render deployment config
├── requirements.txt # Python dependencies
└── .streamlit/
└── config.toml # Custom Streamlit settings

## 🧪 Local Setup

```bash
# Clone the repo
git clone https://github.com/sarvesh-112/movie-recommender-system.git
cd movie-recommender-system

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

Make sure you have a valid TMDb API key and a similarity.pkl file accessible via Google Drive. The app will automatically download it using gdown.
```

```🐳 Docker Build & Run
# Build Docker image
docker build -t movie-recommender .

# Run container
docker run -p 8501:8501 movie-recommender
```
☁️ Deploying on Render
Push your code to GitHub.

In Render, link the repo and select “Docker” as the environment.

Render automatically uses render.yaml and your Dockerfile to build and deploy.

Enable auto-deploy or trigger manual rebuilds on every commit.

🔐 API Key Setup
Create a .env file or securely store your TMDb API key. If not, ensure it is hardcoded only for demo/testing purposes and never exposed in public repos.

📌 Notes
This project avoids the setuptools.build_meta error on Render by relying on a custom Docker build.

It provides an engaging user experience while remaining scalable and lightweight.

You can easily extend it to include collaborative filtering or hybrid models.

🧑‍💻 Authors
Sarvesh Ganesan – GitHub

Project #1 | Streamlit + Jupyter + Docker + TMDb

🪄 Future Enhancements
Add collaborative filtering (Matrix Factorization, SVD)

Deploy API backend using FastAPI

Enable user-based recommendations and authentication

Cache API requests for speed optimization

📜 License
MIT License — Feel free to fork, customize, and deploy.
Let me know if you want this saved as a file (`README.md`) or automatically committed to your repo if you're working via GitHub.
