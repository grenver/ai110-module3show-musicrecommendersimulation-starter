# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Retro Resonance 1.0

---

## 2. Intended Use  

This recommender suggests a small set of songs from a classroom-sized catalog based on a user's preferred genre, mood, energy, and a few optional taste signals. It is designed for classroom exploration only, not for real users.

The system assumes a user can describe taste with simple labels and a handful of numeric preferences. That makes it useful for showing how ranking works, but it also means it cannot represent the full complexity of real music taste.

---

## 3. How the Model Works  

The model starts with genre, mood, and energy. Genre and mood add direct match bonuses, while energy adds a smooth similarity score so songs closer to the target feel rank higher. It then layers on extra signals from the dataset: popularity, release decade, mood tags, aggressiveness, synthiness, and nostalgia score.

The user can also provide optional preferences such as a preferred decade, a more specific mood tag, a target popularity range, target aggressiveness, and whether they like synth-heavy or nostalgic songs. The final score is the sum of these little signals, and the explanation text lists the reasons the song moved up. Compared with the starter version, this adds more nuanced attributes and makes the Retro Nostalgia profile possible.

---

## 4. Data  

The catalog contains 10 songs in `data/songs.csv`. It includes pop, lofi, rock, ambient, jazz, synthwave, and indie pop, with moods such as happy, chill, intense, relaxed, moody, and focused.

Each row includes more than the starter features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`, plus `popularity`, `release_decade`, `mood_tag`, `aggressiveness`, `synthiness`, and `nostalgia_score`. Those added fields make it possible to run more specific experiments, including the Retro Nostalgia test profile.

The data still leaves out a lot of real musical taste, especially lyrics, context, and cultural meaning. The dataset also reflects the small hand-built catalog rather than broad listener behavior.

---

## 5. Strengths  

The system works well when the user profile is clear and the target song traits are represented in the catalog. The scoring is transparent, so it is easy to see why a song ranked highly, and the extra attributes make it better at separating similar songs than a genre-only recommender would be.

The Retro Nostalgia experiment is a strength because it shows the system can use the newer fields in a meaningful way instead of treating every song as just genre plus energy.

---

## 6. Limitations and Bias 

The system still over-prioritizes the small set of signals it does use, especially energy, so songs with a similar energy level can outrank songs that are a better genre or mood match. Because the catalog only has 10 songs and some styles appear more than once, the recommender can repeat the same artists or genres across different profiles instead of showing much variety. It also ignores important parts of musical taste like lyrics, instrumentation, and context, so it may miss what a real listener would actually want. Users whose preferences do not fit the dataset, such as niche genres or unusual combinations of mood and energy, are likely to get weaker results. In practice, that means the system can create a mild filter bubble around the songs that best match the most common patterns in the tiny dataset.

---

## 7. Evaluation  

I tested five profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, Adversarial Conflicted, and Retro Nostalgia. I looked at whether the top songs matched the mood of each profile and whether the same songs kept repeating across different users. The clearest result was that the high-energy songs kept rising to the top, even when genre and mood did not match very well. That surprised me because it showed the energy score was stronger than I expected for a tiny catalog.

The Retro Nostalgia profile was the main check for the new attributes. It made it easy to see whether the recommender could respond to decade, mood tag, synthiness, and nostalgia instead of relying only on the basic profile fields. The Chill Lofi profile made the most sense, while the adversarial profile showed that the system can still be pulled toward similar high-energy songs even when the rest of the profile is conflicting.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
