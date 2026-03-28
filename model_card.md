# 🎧 Model Card: Music Recommender Simulation
# [Model Card](model_card.md) | [ReadMe](ReadMe.md) | 

## 1. Model Name   <!-- [§Phase 5] -->

# ---- NB BEGIN ----

## Goal / Task
Suggest top‑K songs from a small catalog by matching a user’s preferred **genre**, **mood**, **energy**, and **tempo** using a transparent, content‑based score.
# ---- NB END ----
Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

# ---- NB BEGIN ----

## Intended Use / Non‑Intended Use
Intended for **education/demo** to illustrate explainable content‑based recommenders. Not intended for production, personalization at scale, or sensitive decision contexts.

# ---- NB END ----
Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

# ---- NB BEGIN ----

## Algorithm Summary (plain language)
We award points for **exact genre/mood matches** and add similarity points for **energy** and **tempo** (closer to target gets more). Optional features lightly adjust scores: **mood tag overlaps** and a **popularity** boost. I then **rank** songs and apply a **diversity penalty** so the top results aren’t dominated by one artist/genre.

# ---- NB END ----
Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

# ---- NB BEGIN ----
## Data Used
20 songs with: title, artist, genre, mood, energy (0–1), tempo_bpm, plus optional: popularity (0–100), release_decade, mood_tags. Catalog is intentionally small and CodePath classroom‑oriented.
# ---- NB END ----

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

# ---- NB BEGIN ----

# ---- NB END ----

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

# ---- NB BEGIN ----

## Observed Behavior / Biases
Energy‑heavy profiles push up EDM/Rock. Mood‑first mode surfaces Lo‑fi/Ambient for calm profiles. Popularity subtly favors radio‑friendly tracks. Because the catalog is small and skewed, some tastes (e.g., Jazz) get little representation.

# ---- NB END ----

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

# ---- NB BEGIN ----

## Evaluation Process
Tried three diverse profiles and compared top‑10 lists across four modes. Ran an experiment increasing energy importance and observed predictable shifts (EDM/Rock rose). Checked explanations (“reasons”) per song to confirm weight effects.

# ---- NB END ----

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

# ---- NB BEGIN ----

## Ideas for Improvement
- Add collaborative signals (e.g., co‑listening) beside attributes.  
- Learn weights from feedback, not fixed constants.  
- Expand dataset diversity and use multi‑label genre/mood taxonomy.

# ---- NB END ----

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

# ---- NB BEGIN ----

## Personal Reflection
Designing clear **scoring + ranking** rules made it easy to reason about behaviour. Even simple linear similarities “feel” like recommendations when combined with readable explanations, but small design choices (e.g., popularity) introduce bias quickly.

# ---- NB END ----

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
