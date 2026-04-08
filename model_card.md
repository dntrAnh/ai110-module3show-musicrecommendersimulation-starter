# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder Classroom Prototype

---

## 2. Intended Use

This model suggests top songs from a small classroom dataset based on a user profile with genre, mood, and target energy. It is intended for learning how recommendation logic works, not for production users. It assumes users can describe their taste with a few simple preferences.

---

## 3. How the Model Works

The model gives each song a score by checking how well song features line up with user preferences. A song can gain points from matching genre and mood, and also from being close to the user's energy target. During experimentation, I shifted weights to make energy matter more and genre matter less so I could test sensitivity. The output is the top ranked songs plus short reason strings explaining why each song was picked.

---

## 4. Data

The catalog has 20 songs in `data/songs.csv`. The dataset includes many genres, but only a few repeated clusters (for example, 3 lofi songs and 2 pop songs while most genres appear once). Mood labels are similarly sparse, with a few repeated labels and many singletons. This means some user tastes have only one or two realistic matches in the catalog.

---

## 5. Strengths

The recommender works well for focused profiles like High-Energy Pop and Chill Lofi, where at least one major feature clearly matches. The explanations are easy to understand, so users can see exactly why a song ranked highly. It also reacts in a predictable way when the user profile changes, which is good for learning and debugging.

---

## 6. Limitations and Bias

One weakness is that the system can create an energy-driven filter bubble, especially after increasing energy weight. Songs with very similar energy values keep rising to the top even when mood is a poor match, so users can get repetitive results that feel “technically correct” but emotionally wrong. Because the dataset is small, many genres have only one example, so some users get low variety no matter what they ask for. The energy formula also drops to zero after a fixed gap, which can harshly remove songs that might still be good fits in real listening behavior. Finally, if a profile is missing keys (like mood or energy), recommendations can collapse into ties and lose personalization.

---

## 7. Evaluation

I tested six profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Conflicting Preferences (High Energy + Sad Mood), Sparse Profile (Genre Only), and Boundary Energy Tie Case. Before the experiment, genre contributed strongly; after the weight shift experiment (genre halved, energy doubled), high-energy songs became even more dominant across multiple profiles. One surprise was that in conflicting profiles, songs like Gym Hero kept ranking near the top because energy closeness could overpower mood mismatch. I also compared results to musical intuition: for Happy Pop, Sunrise City as #1 felt right, but repeated appearances of Gym Hero for non-pop moods felt less intuitive. This showed the model became more sensitive to energy than to emotional context.

Inline chat prompt used for result explanation:

"Using the weights in `src/recommender.py`, explain in plain language why Sunrise City ranked #1 for the High-Energy Pop profile. Break down genre points, mood points, and energy similarity points with the actual score math."

Chat-view prompt used for bias analysis:

"Using #file:src/recommender.py and #file:data/songs.csv, identify likely filter bubbles or user groups that may get weaker recommendations. Focus on genre sparsity, mood sparsity, and the energy-gap formula."

---

## 8. Future Work

I would add diversity logic so the top 5 are not all near-identical in energy. I would include additional preference controls (for example, acousticness and danceability) and allow “soft” mood matching. I would also add tie-breaking rules and normalization so missing profile fields do not collapse results to many zero-score ties.

---

## 9. Personal Reflection

My biggest learning moment was seeing how one small scoring change (higher energy weight) reshaped almost every top-5 list. It made me realize that recommendation quality is not just about writing code that runs, but about tuning tradeoffs between relevance and variety.

AI tools helped me move faster by generating adversarial profiles, suggesting experiment ideas, and explaining score behavior in plain language. I still had to double-check outputs by running the code and verifying the math myself, because AI suggestions can sound correct even when they need context-specific validation.

What surprised me most is that even a very simple weighted formula can feel like a "real" recommender once it gives ranked outputs and explanations. At the same time, those rankings can feel repetitive or biased if one feature dominates.

If I extended this project, I would add diversity constraints, soft mood matching, and more user controls (like danceability/acousticness sliders). I would also test with a larger and more balanced dataset to reduce filter bubbles and improve fairness across different listener types.
