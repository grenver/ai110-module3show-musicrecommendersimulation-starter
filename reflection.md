# Reflection

## What I Learned

The biggest thing I learned is that a recommender can look smart even when it is really using only a few signals. In this project, genre and mood were useful when they lined up with the user profile, but energy was strong enough to pull songs upward even when the rest of the profile was a bad match. That became obvious in the Adversarial Conflicted profile, where Storm Runner still ranked well because its energy was close to the target.

I also learned that adding more song attributes only helps if the data actually contains meaningful variation. The Retro Nostalgia experiment was useful because it proved that `release_decade`, `mood_tag`, `synthiness`, and `nostalgia_score` were not just extra columns. They changed which songs ranked higher and made the explanation text more specific.

## Profile Comparison Notes

High-Energy Pop vs. Chill Lofi: the High-Energy Pop profile leaned toward songs like Sunrise City and Gym Hero because genre, mood, and energy all lined up well. The Chill Lofi profile shifted toward Library Rain and Midnight Coding because it wanted lower energy and more acoustic sound. That makes sense because the recommender rewards songs that match the user's style and feel, not just the title or artist.

Deep Intense Rock vs. Adversarial Conflicted: Deep Intense Rock kept Storm Runner at the top because it matched rock, intense, and high energy all at once. The adversarial profile also kept Storm Runner near the top, but for a different reason: the energy score was doing most of the work even though the genre and mood did not fit. That shows the system can be pushed toward the same type of song when energy is strong enough.

High-Energy Pop vs. Deep Intense Rock: both profiles liked energetic songs, so there was overlap in the results, but the top song changed because the genre and mood changed. High-Energy Pop preferred Sunrise City, while Deep Intense Rock preferred Storm Runner. This makes sense because the recommender still uses genre and mood, but energy can push similar songs upward across different users.

## Bias And Limits

The main bias in this system is toward the small catalog itself. Because there are only 10 songs, the recommender repeats the same artists and keeps circling back to a few strong matches instead of exploring a wide range of music. That means the output is shaped more by what happens to be in the dataset than by any real understanding of music taste.

Another limitation is that the system does not understand lyrics, context, or why a person likes a song emotionally. It can also be unfair to users whose preferences do not match the catalog well, especially niche tastes or unusual combinations of mood and energy. In a real product, that could create a filter bubble where the system keeps showing the same narrow kind of music and ignores better choices outside the dataset.
