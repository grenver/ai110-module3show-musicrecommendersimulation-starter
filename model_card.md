# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The system over-prioritizes the small set of signals it does use, especially energy, so songs with a similar energy level can outrank songs that are a better genre or mood match. Because the catalog only has 10 songs and some styles appear more than once, the recommender can repeat the same artists or genres across different profiles instead of showing much variety. It also ignores important parts of musical taste like lyrics, instrumentation, and context, so it may miss what a real listener would actually want. Users whose preferences do not fit the dataset, such as niche genres or unusual combinations of mood and energy, are likely to get weaker results. In practice, that means the system can create a mild filter bubble around the songs that best match the most common patterns in the tiny dataset.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an Adversarial Conflicted profile with a fake genre and mixed signals. I looked at whether the top songs matched the mood of each profile and whether the same songs kept repeating across different users. The clearest result was that the high-energy songs kept rising to the top, even when genre and mood did not match very well. That surprised me because it showed the energy score was stronger than I expected for a tiny catalog. The Chill Lofi profile made the most sense, while the adversarial profile showed that the system can still be pulled toward similar high-energy songs even when the rest of the profile is conflicting.

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
