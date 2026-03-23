# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

# ------------ BEGIN ------------

<img src="MusicRecommenderSimulation-Demo.gif" alt="MusicRecommenderSimulation-Demo">

# §Phase 1 – Steps 1–4
# <!-- [§Phase 1 – Steps 1–4] -->

Real platforms blend **collaborative filtering (CF)**—“people like you liked X”—with **content‑based filtering (CBF)**—“this song’s attributes match your taste.” Our simulation focuses on CBF for transparency: we compare a user’s **taste profile** (genre, mood, energy, tempo) against each song’s attributes, compute a **score per song**, then **rank** all songs to pick the top‑K. We also record **reasons** (e.g., “genre match”) so results are explainable.

**Objects/Features**
- **Song:** title, artist, genre, mood, energy (0–1), tempo_bpm (+ optional: popularity, release_decade, mood_tags)

- **UserProfile:** favorite_genre, favorite_mood, target_energy, target_tempo_bpm, desired_mood_tags (optional)

**Scoring (initial idea)**
- +2.0 for exact **genre** match
- +1.0 for exact **mood** match
- **Energy similarity**: higher when close to target (1 − |song.energy − target|)
- **Tempo similarity**: higher when close to target BPM

**Ranking**
- Compute score for every song (**scoring rule**) then sort descending (**ranking rule**) to get top‑K.

### Algorithm Recipe  <!-- [§Phase 2 – Steps 3–5] -->
# §Phase 2 – Steps 3–5

1) Start score at 0.  
2) If genre matches user’s favorite_genre, +2.0.  
3) If mood matches favorite_mood, +1.0.  
4) Add **energy similarity** = 1 − |energy − target_energy|, weighted 1.5.  
5) Add **tempo similarity** = 1 − min(|tempo−target|/200, 1), weighted 0.6.  
6) (Optional) Add **mood tag overlap** (cap at 3 tags), weighted 0.6.  
7) (Optional) Add **popularity boost** = popularity/100, weighted 0.5.

Will support multiple **modes** (Genre‑First, Mood‑First, Energy‑Focused, Balanced) via weight presets and add a **diversity penalty** in ranking to avoid many items from the same artist/genre at the very top.

### Mermaid data-flow {Optional}

flowchart LR
-  A[User Prefs] --> B[Score Song]
-  C[Songs CSV] --> B
-  B --> D[Scores + Reasons]
-  D --> E[Sort / Rank]
-  E --> F[Top-K Recommendations]

## Run to viw WebUI uvicorn app:app --reload --host 127.0.0.1 --port 8000

## Diversity penalty: When diversity=True, we pick songs greedily, but after we place each song into the top‑K list, we slightly penalize future candidates by how many times we’ve already used their artist and genre:
```
adjusted_score = base_score
                 - 0.15 * times_this_artist_already_selected
                 - 0.10 * times_this_genre_already_selected
```
# ------------ END ------------

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

