# Strategy — One Emoji, One Smile

## Exact deliverable

`/output/entry.txt` must contain **exactly one emoji and nothing else**: one
UTF-8 character, no words, no caption, no explanation, no trailing newline.
The chosen artifact is `😄` (U+1F604, SMILING FACE WITH OPEN MOUTH AND SMILING
EYES), written as the four bytes `F0 9F 98 84`.

`main.py` (Python 3.13, standard library only, no network/secrets/git reads) is
the repository-root entrypoint. It writes the artifact atomically (temp file
in the same directory, `chmod 0644` before `os.replace`, then verifies the
final bytes and mode). No other file is placed in `/output`.

## Scoring and the judge, in the rubric's own order

The artifact must first pass the gate, then be judged pairwise against other
entries and three fixed house texts. Every pair is judged twice (both slot
orders); each call awards 0.5 + margin/10 to the winner. Three Swiss rounds,
then a playoff among the top 12. A Bradley-Terry fit gives each entry its win
rate; playoff finalists rank above the rest, judged entries above cut entries.
Exact ties go to more playoff wins, then smaller text, then earlier receipt.
Only the top ten places are paid; byte-identical entries share one rate and
the earlier receipt places first.

The judge is briefed to pick whichever emoji is more likely to make a stranger
smile, weighing these criteria **in this order** and stopping at the first
difference:

1. A single emoji a stranger reads as warm and friendly — the kind most likely
   to make someone smile; it loses to any emoji that plainly aims to warm a
   stranger.
2. Warmth at first glance: kind, friendly or gently funny, with no context.
3. Universality: a stranger of any age or background reads it the same way; no
   irony or in-joke that could land wrong.
4. Chosen rather than default: it feels picked for the moment, not the first
   smiley that comes to mind, while staying instantly readable.
5. Right for a stranger: no intimacy, sarcasm or flirtation that would read
   oddly coming from someone unknown.

Novelty for its own sake does not count.

## Hard caps

- Gate: UTF-8 text of **1 to 8 characters**, not only whitespace. `😄` is one
  code point / 4 bytes / 1 character — valid, and minimal on the byte
  tie-break for a colour emoji.
- Exactly one emoji: no words, no caption, no explanation; text addressed to
  the judge is technically allowed by the rules but would fail criterion 1,
  so it is not used.
- Artifact file mode must be **0644**; a mode-600 file is refused by the grader.
- No trailing newline; exact bytes only.
- Sandbox: 1 CPU, 512 MB, 64 PIDs, 60 s wall budget, no network. The program
  runs in milliseconds with the standard library alone.
- `/output` holds only `entry.txt`; no extra files, no vendored assets.

## Concrete plan to maximize the score

1. **Win criterion 1 first.** Pick a human smiling face — the category that
   plainly aims to warm a stranger — not an animal, plant, object or abstract
   symbol. Rivals seen on the public feed (🫶, 🤗, 🫠, 🌻, 🌞, 🦭) either
   signal affection, a mood, or something cheerful-but-not-a-smile; a plain
   warm smile beats them at the first criterion.
2. **Win criterion 2.** `😄` is an open smile *with smiling eyes*: friendly and
   gently happy at a glance, with no context needed.
3. **Win criterion 3.** It has one globally understood meaning — happiness and
   friendliness — with no culture-specific joke, sarcasm or ambiguity that
   could land wrong with a stranger of any age.
4. **Win criterion 4 without sacrificing readability.** `😊` and `😀` are the
   first smileys most people reach for; `😄` is equally instant to read but
   feels deliberately picked. That is the differentiator when two warm smiles
   are compared and the earlier criteria tie.
5. **Win criterion 5.** No hearts, kiss, hug or hand-holding gesture: nothing
   that reads as intimate or flirtatious from an unknown sender. This is
   exactly where 🥰, 🫶, 🤗 and heart-hands entries are vulnerable.
6. **Avoid duplicate-field traps.** House fixed texts and other entries are
   deduplicated by exact bytes; `😄` is a distinct single-code-point artifact,
   so it is judged on its own merit rather than sharing someone else's rate.
7. **Make the mechanics unassailable.** Deterministic stdlib entrypoint,
   atomic write with explicit `0644` mode, local validation of UTF-8, character
   count, byte count, absence of a trailing newline, and the final file mode.
   No network, environment, git-history or out-of-repository reads.

The choice is fixed before submission: blind rounds hide the standings, so
there is nothing to tune against, and a single warm, universal, non-default,
non-intimate smile is the best expected pairwise performance under the rubric.
