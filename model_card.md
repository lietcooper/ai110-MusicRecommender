# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch is designed to suggest songs from a small catalog that best match a listener's current taste profile — their preferred mood, genre, and the feel of music they want to hear right now. It takes in a set of preferences (like "I want something energetic, hip-hop, high danceability") and returns the five songs from the catalog that most closely fit that description.

The system assumes that a user can describe their preferences as a set of target values — one mood label, one genre label, and numeric sliders for energy, acousticness, danceability, and valence. This is a simplified model of real taste: it treats preferences as fixed and independent, and assumes the user knows what they want before they start listening. It is built for classroom exploration and does not reflect the complexity of a production music app.

---

## 3. How the Model Works  

Imagine you tell the system: "I want something energetic, hip-hop, and very danceable." The system then looks at every song in the catalog and asks: how close is this song to what you described?

For labels like mood and genre, it's a simple yes/no: if the song's mood matches yours, it earns bonus points (mood is worth more than genre, because how a song makes you feel tends to matter more than its style category). For numbers like energy and danceability, the system uses a proximity rule — a song that is almost exactly at your target earns nearly full points, while a song far from your target earns fewer. All the points add up to a total score, and the five songs with the highest scores become your recommendations.

The maximum possible score is 8.5 points: 2.0 for a mood match, 1.5 for a genre match, and up to 5.0 spread across the four numeric features. Songs are ranked purely by this score — no randomness, no popularity weighting, no history.

---

## 4. Data  

The catalog contains 20 songs stored in a CSV file. Each song has six meaningful features: mood, genre, energy, acousticness, danceability, and valence. The catalog was expanded from 10 songs to 20 during development to cover a wider range of styles.

Genres represented include hip-hop, lofi, rock, pop, synthwave, indie pop, r&b, classical, metal, country, funk, electronic, soul, blues, and folk. Moods include energetic, focused, intense, happy, moody, peaceful, romantic, aggressive, nostalgic, uplifting, melancholic, tender, sad, and dreamy.

Despite this variety, the catalog skews toward Western popular music styles and contains no entries for genres like jazz, reggae, Latin, or K-pop. Some moods appear only once (e.g., "dreamy," "tender," "romantic"), which means users with those preferences have almost no real choice — there is only one possible top match regardless of numeric features. The dataset reflects the taste of whoever designed it, not a broad or culturally representative sample.

---

## 5. Strengths  

The system works best when the user has a clear, strong preference that the catalog can actually satisfy. A listener who wants energetic hip-hop gets an excellent result: one song dominates the ranking because it matches every single feature the user cares about. The scoring is transparent — every point awarded is explained in plain language alongside each recommendation, so a user can see exactly why a song was chosen.

The separation between scoring and ranking also means the system is easy to inspect and adjust. Changing how much weight energy carries versus genre is a one-line edit, and the effect on rankings is immediately observable. This transparency is something real streaming apps rarely offer, and it makes the system useful as a learning tool for understanding how feature-weighted similarity works in practice.

---

## 6. Limitations and Bias 

The most significant structural weakness discovered through experimentation is **energy dominance**. When the energy weight was doubled (2.0 → 4.0), the top recommendations barely changed for well-matched profiles — but for adversarial profiles like "High-Energy Sad," songs with mismatched moods shot up the rankings purely because their energy value was close to 0.9, burying the only truly sad songs in the catalog. This means a user who wants sad, introspective music but happens to phrase their energy preference highly will systematically receive energetic songs that contradict their intent.

A related bias is **categorical lock-in amplified by a small catalog**. Mood and genre together contribute up to 3.5 of 8.5 points, and with only 20 songs some labels appear just once (e.g., "aggressive," "romantic," "tender"). A user whose mood or genre has a single catalog match will always receive that one song in their top results regardless of how poorly its numeric features align — there is simply no competition.

Finally, the proximity formula assumes **symmetric, linear tolerance**: being 0.2 above the target energy costs the same as being 0.2 below. Real listeners are often asymmetric — they may tolerate slightly more intensity than they asked for, but strongly dislike songs that feel too quiet or too slow. The current scoring has no way to express that asymmetry, so it will occasionally recommend songs that feel subtly wrong even though their numeric score looks correct.

---

## 7. Evaluation  

Six user profiles were tested: three standard listeners and three adversarial edge cases.

**High-Energy Hip-Hop** — *Street Echoes* scored 8.32 and dominated by a wide margin. It was the only song that matched both mood ("energetic") and genre ("hip-hop"), and its numeric features (energy 0.85, danceability 0.90) were nearly identical to the user's targets. The result felt correct.

**Chill Lofi** — *Focus Flow* came out on top, matching both "focused" mood and "lofi" genre. The second and third results (*Library Rain*, *Midnight Coding*) also matched the lofi genre but not the mood — they still ranked highly because their energy and acousticness were close to the targets. This felt reasonable: a lofi listener probably doesn't mind slightly different moods as long as the texture is right.

**Deep Intense Rock** — *Storm Runner* won, matching mood ("intense") and genre ("rock"). *Gym Hero* came in second with only a mood match. What was surprising: *Iron Storm* — a metal song with energy 0.97 — placed third, not second, even though it feels like an intense rock song. The reason is danceability: *Gym Hero* has a danceability score closer to 0.5 (the rock profile target), while *Iron Storm* is more rigid rhythmically. The system penalized the more "metal" song for not being groovy enough.

**High-Energy Sad (adversarial)** — This was the most revealing test. *Delta Cross* (a blues song tagged "sad") won because it matched both mood and genre, even though its energy (0.45) was far from the user's stated target of 0.9. The system correctly honored the emotional intent — but the second-place result was *Storm Runner*, a hard rock track with no emotional match at all, boosted purely by its energy proximity. The top result felt right; the rest of the list felt like a different user entirely.

**All-Middle Neutral (adversarial)** — All numeric features set to 0.5. *Sunrise City* won because it matched mood ("happy") and genre ("pop") — the only two things that could differentiate songs when every numeric feature is equally close to the midpoint. This confirmed the hypothesis: neutral numeric preferences turn the recommender into a pure genre/mood lookup, not a nuanced finder.

**Missing Genre (adversarial)** — Genre set to "jazz," which has no exact catalog match. *Morning Sonata* (classical, "peaceful" mood) topped the list on mood match plus strong acousticness proximity. Surprisingly, *Coffee Shop Stories* appeared second — it turned out that song's genre in the CSV is "jazz," so there was a match after all. This revealed a hidden catalog entry that wasn't obvious from browsing the data.

---

## 8. Future Work  

The most important improvement would be **diversity enforcement**: the current system can return five songs that are nearly identical to each other if they all score close to the top. A real recommender should spread results across genres or moods so the user has genuine variety to choose from, not five copies of the same vibe.

A second improvement would be **asymmetric tolerance**: letting users express that they are okay with songs slightly above their energy target but not below, or vice versa. The current linear proximity formula treats over- and under-shooting as equally bad, which doesn't match how most people actually experience intensity preferences.

Longer term, the system could benefit from a **larger and more diverse catalog**, coverage of underrepresented genres (jazz, Latin, K-pop, classical sub-genres), and the ability to learn from listening history rather than requiring the user to specify all preferences upfront.

---

## 9. Personal Reflection  

**High-Energy Hip-Hop vs. Chill Lofi** — These two profiles produced the most opposite lists imaginable, and that makes complete sense. The hip-hop profile asked for energy 0.85, danceability 0.88, and very little acoustic texture. The lofi profile asked for the opposite: low energy, high acousticness, moderate danceability. So the songs that scored near the top for one profile scored near the bottom for the other. It's a good sign that the numeric proximity formula is doing its job — it genuinely rewards songs that are "close" to what you asked for, not just songs that are generically popular.

**Deep Intense Rock vs. High-Energy Hip-Hop** — Both profiles want high energy, but they diverge on danceability and acousticness. The rock profile wanted less danceability (0.50) and near-zero acousticness, while the hip-hop profile wanted very high danceability (0.88). That's why *Street Echoes* (hip-hop, very danceable) appears in the hip-hop top 5 but not the rock top 5, and *Storm Runner* (rock, lower danceability) does the opposite. Energy alone doesn't determine the list — the combination of all features matters.

**High-Energy Sad vs. All-Middle Neutral** — Both are adversarial, but for different reasons. The High-Energy Sad profile has a real internal contradiction: asking for energy 0.9 but mood "sad." The system resolves this conflict by honoring the mood match at the top (Delta Cross) and then filling in the rest of the list with high-energy songs that ignore the mood entirely. The All-Middle Neutral profile has no contradiction — it just has no strong opinions. Because all numbers point toward the middle, the system has nothing to grab onto numerically, so it defaults to label-matching. A user with neutral preferences essentially gets whoever has the right genre and mood sticker, which may not feel personal at all.

**Chill Lofi vs. Missing Genre** — The lofi profile and the jazz-seeking profile both want quiet, acoustic, low-energy music. Their numeric targets are similar. Yet the lofi profile gets a much more cohesive top-5 list (all lofi or adjacent) because the genre label "lofi" exists in the catalog and earns bonus points. The jazz profile gets a scattered list because that genre bonus never fires for most songs. This shows that the system is only as good as the labels in the data — two users who would enjoy the same songs in real life can get very different recommendations just because one of them used a genre name the catalog doesn't recognize.

**Why does "Gym Hero" keep showing up for people who just want Happy Pop?** — *Gym Hero* is tagged "intense" and is not pop, so it doesn't match the happy pop profile's labels at all. But it shows up because its numeric features are close to average: moderate energy, moderate danceability, near-zero acousticness. When the system runs out of exact genre/mood matches to rank, it fills the remaining slots with whatever songs are numerically closest to the midpoint — and *Gym Hero* happens to live near the center of the feature space. It's not a bad song for that profile; it's just a consequence of the catalog being small and *Gym Hero* being numerically "average." In a real app with millions of songs, it would get crowded out by songs that match both the label and the numbers.

---

**What was your biggest learning moment during this project?**

The most clarifying moment came from running the adversarial profiles — specifically the High-Energy Sad case. Before testing, the assumption was that mood and genre bonuses were strong enough to anchor the results emotionally. But after the top match, the rest of the list filled with high-energy songs that had nothing to do with sadness. That revealed something fundamental: the scoring formula has no concept of *conflict*. It adds up points from independent features without noticing when those features are pulling in opposite directions. A song can earn maximum energy points and maximum mood points from different users at the same time, because the system never asks whether those two signals are compatible. Real recommenders have to solve this problem too — it just isn't visible until you deliberately try to break the system.

**How did using AI tools help you, and when did you need to double-check them?**

AI assistance proved valuable at nearly every stage of this project. It helped in understanding the existing codebase structure, planning how the scoring algorithm should be decomposed into functions, implementing the scoring and ranking logic directly from the written algorithm recipe, and reviewing the resulting code for correctness and clarity. Rather than spending time on syntax or boilerplate, it was possible to focus on the design decisions — which features to weight, how to handle categorical versus numeric comparisons, and what the edge cases should test. That said, the outputs required verification at each step: the experiment results needed to be read and interpreted manually, the adversarial profiles needed human judgment about what counted as a "surprising" or "wrong" result, and the bias analysis required reasoning about the domain rather than just the code. AI tools accelerated the implementation and surfaced possibilities quickly, but the decisions about what to test, what the results meant, and what to write about them remained a human responsibility throughout.
