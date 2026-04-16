# Reflection: Music Recommender Evaluation

## Profile Comparison Notes

### HAPPY_POP vs CHILL_LOFI

The HAPPY_POP profile returned a wide spread of genres in its top 5 — pop, indie pop,
country, hip-hop — all pulled in by mood and energy matches after the two pop songs
were exhausted. The CHILL_LOFI profile, by contrast, clustered tightly: three lofi
songs in a row, then ambient and jazz. The difference is the acoustic bonus: CHILL_LOFI
users get +0.5 on every highly acoustic track, which consistently favors the slow,
instrumental catalog entries. This makes sense musically — lofi listeners really do
want a specific texture — but it also means the top 5 for a lofi user lacks variety.

### CHILL_LOFI vs INTENSE_ROCK

Both profiles found their strongest match immediately (Library Rain at 4.47, Storm
Runner at 3.99). After that, the two profiles diverged sharply. CHILL_LOFI had three
more lofi songs to draw from, keeping scores high (4.46, 3.48). INTENSE_ROCK had
zero other rock songs, so positions 2–5 were decided entirely by energy proximity —
a pop song (Gym Hero) ranked above a metal song (Iron Cathedral) because the system
cannot recognize that metal and rock are musically adjacent. This is the clearest
example of the system's binary genre matching failing a real listener.

### INTENSE_ROCK vs ADVERSARIAL EDM/Sad

Both profiles wanted high energy, but the EDM/sad profile added a conflicting mood
preference. The result shows that when genre and mood disagree, genre wins every time.
Pulse Wave (EDM/euphoric) ranked first for the EDM/sad profile despite its mood being
the opposite of "sad." An INTENSE_ROCK user at least got a first result that matched
on all three dimensions; the EDM/sad user got a result that matched genre but actively
contradicted their mood preference. This tells us the system is not capable of
balancing trade-offs — it simply adds up points regardless of whether the combination
makes sense.

### ADVERSARIAL EDM/Sad vs ADVERSARIAL Classical

These two edge cases produced opposite outcomes. The Classical profile was the
*most successful* test of the system: Autumn Sonata scored a perfect 4.50, and every
field matched (genre, mood, energy, acousticness). The EDM/sad profile was the *least
successful*: its top result contradicted the mood preference. The key difference is
conflict — the Classical profile had internally consistent preferences that the catalog
could satisfy, while the EDM/sad profile had preferences that no single song could
fully honor (no songs are tagged EDM and sad). This reveals that the system performs
well when preferences are consistent and realistic, but breaks down when given inputs
that do not match patterns in the catalog.

---

## Weight-Shift Experiment Notes

Halving genre weight (+2.0 → +1.0) and doubling energy weight (+1.0 proximity →
+2.0 proximity) caused modest ranking shifts but did not fix the core problems.

For HAPPY_POP, Rooftop Lights moved above Gym Hero because its energy (0.76) is
slightly closer to the target (0.82) than Gym Hero's (0.93). Doubling energy weight
magnified that small difference enough to flip the order. This suggests the original
weights were keeping genre in charge even when energy differences were meaningful.

For INTENSE_ROCK, the experiment showed that halving genre weight alone is not enough
to surface Iron Cathedral above high-energy non-rock songs. Metal still earned zero
genre points; it can only compete on energy. The real fix would be a similarity matrix
that gives metal partial genre credit when the user prefers rock.

---

## Personal Reflection

Building VibeFinder forced me to confront how much human judgment is hidden inside
even a "simple" algorithm. Choosing the weight of +2.0 for genre was not a
mathematically derived decision — it was a guess based on intuition that genre is the
strongest vibe signal. Testing that guess against the rock profile showed it was
partially wrong: the weight was so dominant that it created a cliff after the first
result, collapsing the remaining recommendations into pure energy-matching. That is
not a bug in the code; it is a bias baked into the design. The code worked exactly as
written. The design just did not match what a real listener would want.

The most interesting thing about this project is how it reframes the way I think about
Spotify or YouTube recommendations. Before building this, I assumed those platforms
were doing something fundamentally different — some kind of deep understanding of music.
Now I suspect the core is the same idea: score, rank, return the top items. The
difference is scale (millions of songs), more features (audio fingerprinting, lyric
analysis), and collaborative signals (what similar users skipped). The magic is not
in the algorithm; it is in the data and the feedback loops.

One thing AI tools helped clarify was the distinction between a scoring rule and a
ranking rule. I originally thought of them as one thing — "recommend songs" — but
separating them into `score_song` and `recommend_songs` made the logic much cleaner
and easier to debug. When the output looked wrong, I could test each function
independently instead of guessing where the problem was. That modular structure was
a direct result of working through the design before writing any code.
