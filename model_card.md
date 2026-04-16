# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests the top 5 songs from a small curated catalog that best match
a listener's stated taste profile — their preferred genre, mood, energy level, and
whether they enjoy acoustic sounds.

It is designed for **classroom exploration** of how content-based recommender systems
work. It assumes the user can accurately describe their own taste upfront; it cannot
learn from listening history or adapt over time.

**Intended use:**
- Demonstrating and explaining the mechanics of a content-based recommender
- Comparing how different user profiles produce different ranked outputs
- Identifying bias and limitations in simple weighted scoring systems

**Not intended for:**
- Real users choosing what to listen to — the catalog is too small and the scoring
  too rigid to serve genuine musical discovery
- Any commercial or production music application
- Representing the preferences of any demographic group — the catalog and profiles
  were created for testing purposes only, not to reflect real listening populations

---

## 3. How the Model Works

Imagine you walk into a record store and hand the clerk a card that says: "I like
pop music, happy songs, and high-energy tracks." The clerk then goes through every
album in the store and gives each one a score based on how well it matches your card.

That is exactly what VibeFinder does. For every song in the catalog it adds up points:

- **+2 points** if the song's genre matches your favorite genre — the biggest signal.
- **+1 point** if the song's mood matches your preferred mood.
- **Up to +1 point** based on how close the song's energy is to your target. A perfect
  match gives the full point; a song far from your target gets close to zero. This
  "closeness" scoring means the system rewards the right *level* of energy, not just
  "more is better."
- **+0.5 bonus** if you enjoy acoustic music and the song is mostly acoustic.

After scoring every song, it sorts the list from highest to lowest and returns the
top 5. The score for each recommendation is shown alongside a plain-English explanation
of what contributed to it.

---

## 4. Data

The catalog contains **20 songs** stored in `data/songs.csv`. The starter dataset had
10 songs (pop, lofi, rock, ambient, jazz, synthwave, indie pop); 10 more were added
to improve diversity:

| New genres added | New moods added |
|---|---|
| hip-hop, r&b, metal, classical | confident, romantic, angry |
| country, edm, folk, blues | melancholic, euphoric, sad |
| reggae, k-pop | calm, energetic |

Each song is described by 7 features: genre, mood, energy (0–1), valence (0–1),
danceability (0–1), acousticness (0–1), and tempo in BPM.

**Gaps in the data:** There is only one song per genre for most genres. This means
a rock fan gets one great match and then falls back to energy-only scoring. The
catalog also has no songs in genres like soul, gospel, trap, bossa nova, or
anything from non-English-speaking music scenes, which limits its coverage of global
listening tastes.

---

## 5. Strengths

- **Works well for common profiles.** The HAPPY_POP profile found a perfect 4.0
  match (Sunrise City: genre + mood + energy all aligned), which intuitively feels
  right.
- **Acoustic listeners are well served.** The CHILL_LOFI profile scored 4.47 —
  the highest of any tested profile — because the acoustic bonus stacked on top of
  genre and mood matches.
- **Niche profiles still get a winner.** The ADVERSARIAL Acoustic Classical profile
  found Autumn Sonata at a perfect 4.50 score. Even with only one song in that genre,
  the system correctly identified it and explained why.
- **Transparent explanations.** Every recommendation comes with a plain list of
  reasons, so users can immediately understand and critique the output.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** The genre component is worth +2.0 —
more than the mood, energy, and acoustic bonus combined. This means a mediocre song
in the right genre will almost always outrank an excellent song in a related genre.
For example, the INTENSE_ROCK profile ranked Gym Hero (a pop/intense song) second —
above Iron Cathedral (metal/angry, score 0.93) — solely because metal is not spelled
"rock." A human listener would consider metal closer to rock than pop is, but the
system treats them as completely unrelated.

**Sparse catalog amplifies the bottleneck.** With only one rock song in 20 tracks,
the INTENSE_ROCK profile gets a single strong match and then falls back to pure
energy scoring. In a real catalog of millions, this dilution would not happen.

**Conflicting preferences expose the genre-first bias.** The adversarial profile
"EDM fan who wants sad music" revealed that when genre and mood conflict, genre
always wins. Pulse Wave (EDM/euphoric) ranked first despite its mood being the
opposite of what the user asked for, simply because its genre matched.

**Binary categorical matching ignores musical similarity.** Rock and metal are
closely related genres, just as "happy" and "euphoric" are closely related moods.
The current scoring gives zero partial credit for near-matches, which produces
counterintuitive rankings.

**The profile is static.** A real listener's mood and energy preference shifts by
time of day, season, and activity. VibeFinder has no way to adapt.

---

## 7. Evaluation

**Profiles tested:**

| Profile | Top result | Score | Felt right? |
|---|---|---|---|
| HAPPY_POP | Sunrise City (pop/happy) | 4.00 | Yes — perfect match |
| CHILL_LOFI | Library Rain (lofi/chill) | 4.47 | Yes — exactly the vibe |
| INTENSE_ROCK | Storm Runner (rock/intense) | 3.99 | Yes — but cliff after #1 |
| ADVERSARIAL EDM/sad | Pulse Wave (EDM/euphoric) | 2.99 | No — mood ignored |
| ADVERSARIAL Classical | Autumn Sonata (classical/melancholic) | 4.50 | Yes — perfect match |

**What surprised me:**
- Iron Cathedral (metal) ranked 5th for the rock profile, losing to a pop song and
  three purely energy-matched tracks. The binary genre check completely failed to
  recognize that metal is a close neighbor of rock.
- The EDM/sad adversarial profile showed that when genre and mood pull in opposite
  directions, the +2.0 genre weight always wins. The system cannot handle conflicting
  preferences gracefully.

**Weight-shift experiment (genre halved to +1.0, energy doubled to 2× proximity):**
- For HAPPY_POP: Rooftop Lights (indie pop) jumped over Gym Hero because doubling
  energy weight amplified the fact that Rooftop Lights' energy (0.76) is closer to
  the target (0.82) than Gym Hero's (0.93).
- For INTENSE_ROCK: Storm Runner still dominated. Iron Cathedral still ranked last
  of the top 5. Halving genre weight narrowed the gap but did not fix the categorical
  blind spot — metal still scored zero genre points.
- **Conclusion:** The weight shift made the system more energy-sensitive but did not
  fix the fundamental limitation of binary genre/mood matching.

---

## 8. Future Work

1. **Soft genre similarity.** Replace exact genre matching with a similarity matrix
   (e.g., rock ↔ metal = 0.8, rock ↔ jazz = 0.2) so related genres earn partial
   credit instead of zero.
2. **Expand the catalog.** With only 1–2 songs per genre, niche profiles are
   under-served after the top pick. A realistic catalog would have hundreds of songs
   per genre.
3. **Diversity penalty.** Add a rule that prevents the top 5 from being dominated by
   a single genre or artist. The CHILL_LOFI profile returned three lofi songs in a
   row — a real platform would inject variety.
4. **Dynamic profiles.** Allow the system to update `target_energy` based on time
   of day or recent skips, making recommendations more context-aware.
5. **Valence and danceability scoring.** These features are in the dataset but not
   yet used in scoring. Adding them would give the system more expressive power.

---

## 9. Personal Reflection

**Biggest learning moment:**
The most surprising moment was when Iron Cathedral — a metal song with angry mood and
0.97 energy — ranked below Gym Hero (a pop song) for a listener who explicitly asked
for rock and intense music. I expected the system to "know" that metal is closer to
rock than pop is. But it does not know anything like that. It only knows whether two
strings are equal. That one ranking failure made the limitation of binary categorical
matching click immediately: the system has no concept of musical relatedness,
only exact matches.

**How AI tools helped, and where I had to verify:**
Using an AI assistant to design the scoring formula saved a lot of time — particularly
the explanation of why proximity scoring (`1.0 - abs(a - b)`) is better than a flat
"higher is better" rule. That was a non-obvious mathematical choice that became clear
once explained. However, AI-generated suggestions always needed to be tested against
the actual data. The adversarial EDM/sad profile, for example, was suggested as an
edge case to try — and it exposed the genre-over-mood bias immediately. The insight
came from running the code, not from the suggestion alone.

**What surprised me about simple algorithms feeling like recommendations:**
Even with just four scoring components and a 20-song catalog, the results for
HAPPY_POP and CHILL_LOFI "felt right" intuitively. Sunrise City ranked first for a
pop/happy listener; Library Rain ranked first for a chill/lofi listener. That was
genuinely surprising — I expected a system this simple to produce obviously wrong
results. It made me realize that the reason real platforms feel magical is not
necessarily because their algorithms are incomprehensibly complex, but because they
have millions of songs to rank and millions of users whose patterns reinforce each
other. The core idea — score and sort — is the same.

**What I would try next:**
The most impactful improvement would be replacing binary genre matching with a
similarity table (rock ↔ metal = 0.8, pop ↔ indie pop = 0.7) so that related genres
earn partial credit instead of zero. After that, I would add the valence and
danceability features to the scoring function — they are already in the dataset but
not yet used, and they would help distinguish "happy and danceable" pop from "happy
but slow" pop. Finally, I would implement a diversity penalty to prevent the top 5
from stacking with songs from the same genre, which would make the recommendations
feel more like a real playlist and less like a filter.
