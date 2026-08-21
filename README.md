# Movie Recommendation Model 

A Machine Learning based movie recommendation system that recommends similar movies based on movie features.

# Features

* Recommends movies similar to the selected movie
* Uses movie similarity scores for recommendations
* Simple Streamlit web interface
* Machine Learning based recommendation approach

# Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Jupyter Notebook

# Project Files

* `app.py` — Streamlit application
* `Movie_Recommendation.ipynb` — Model development notebook
* `similarity.pkl` — Movie similarity data used for recommendations
* `movies.csv` — Movie dataset

> **Note:** `similarity.pkl` is a large file and is not included directly in this GitHub repository because it exceeds GitHub's 100 MB file size limit.

# How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

# Project Goal

The goal of this project is to build a simple movie recommendation system that helps users discover movies similar to their selected movie.


