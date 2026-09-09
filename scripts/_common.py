"""
Shared helpers for scripts/ tools: corpus loading, text normalization,
and the direct-to-video sequel / short registry used by both
count_topics.py and find_gaps.py.
"""
import json
import os
import re
import sys

# Windows' default console codepage (cp1252) can't encode some question text
# (accented names, smart quotes) -- this crashed find_near_dupes.py under
# output redirection (e.g. `> report.txt`) on a `ā` character. Every
# script here imports _common, so fixing it once here covers all of them.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALID_CATEGORIES = {"movies", "characters", "parks", "walt", "cruise", "music", "pixar"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "in", "on", "at", "of", "to", "for",
    "and", "or", "what", "which", "who", "whom", "whose", "how", "does", "did", "do",
    "this", "that", "these", "those", "from", "by", "with", "as", "name", "named",
    "called", "its", "his", "her", "their", "s", "it", "he", "she", "they", "film",
    "movie", "disney", "character",
}

HONORIFICS = {
    "mr", "mrs", "ms", "dr", "king", "queen", "prince", "princess", "captain",
    "lord", "lady", "sir", "madame", "aunt", "uncle",
}
ARTICLES = {"a", "an", "the"}


def load_corpus():
    """Returns the flat list of all question dicts across every shard."""
    with open(os.path.join(BASE, "questions", "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    questions = []
    for shard in manifest["shards"]:
        path = os.path.join(BASE, shard)
        with open(path, encoding="utf-8-sig") as f:
            questions.extend(json.load(f))
    return questions


def stem(word):
    """Cheap suffix-stripping, not a full Porter stemmer -- good enough to fold
    plurals/tense variants (kitten/kittens, sings/sang... well, not irregulars,
    but sing/singing/sung's shared prefix) into one token for near-dupe recall."""
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 5 and word.endswith("ing"):
        return word[:-3]
    if len(word) > 4 and word.endswith("ed") and not word.endswith("eed"):
        return word[:-2]
    if len(word) > 4 and word.endswith("es"):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us")):
        return word[:-1]
    return word


def tokenize(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {stem(w) for w in words if w not in STOPWORDS and len(w) > 1}


def normalize_answer(text):
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", "", t)
    words = [w for w in t.split() if w not in ARTICLES]
    if len(words) > 1:
        words = [w for w in words if w not in HONORIFICS]
    return " ".join(words)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def _tokens_overlap(a, b):
    """True if two already-stemmed tokens are the same word, or one is a
    length->=5 prefix of the other. The prefix branch exists because `stem()`
    only strips ies/ing/ed/es/s -- it does not strip -er, so "shoemaking" (->
    "shoemak") and "shoemaker" (unchanged) never land on the same stem. Adding
    -er-stripping to `stem()` itself would corrupt unrelated tokens ("water" ->
    "wat") for every other script that shares it, so the tolerance lives here
    instead, local to leak detection."""
    if a == b:
        return True
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    return len(shorter) >= 5 and longer.startswith(shorter)


def find_answer_leaks(q):
    """Detect the correct answer (answers[0]) leaking into the question's own
    text -- CLAUDE.md rule #2. Two tiers:

    Tier 1 (high precision): the full normalized answer string appears
    verbatim inside the question text. This is the original validate_batch.py
    check, now shared so both drafts and a whole-corpus pass use it.

    Tier 2 (advisory): a content word from the correct answer -- matched via
    _tokens_overlap, so morphological variants like shoemaker/shoemaking count
    -- also appears in the question, AND that same word does NOT appear (by
    the same matching rule) in any of the 3 distractors. The distractor check
    is what keeps this from flagging ordinary shared category vocabulary (a
    question and all 4 answers about the same film, say) -- it only fires when
    the overlap is specific to the correct answer.

    Both tiers are lexical/stem-based only. A pure-synonym leak (question says
    "canine," answer is "Dog") shares no stem and is NOT detectable this way --
    same residual class the find_near_dupes.py dedup tooling already accepts
    and leaves to a human read. Always eyeball hits; this is advisory, not
    proof of a violation (e.g. a title-answer that must legitimately contain
    a franchise word the question also mentions, like "Frozen Fever" answering
    a question that says "Frozen").

    Returns a list of {"tier": 1|2, "token": str} hits (empty if none, or if
    `q` doesn't have exactly 4 answers).
    """
    answers = q.get("answers") or []
    if len(answers) != 4 or not isinstance(q.get("question"), str):
        return []

    question_text = q["question"]
    norm_q = question_text.strip().lower()
    correct_raw = re.sub(r"[^\w\s]", "", answers[0]).strip().lower()

    hits = []

    if len(correct_raw) >= 4 and correct_raw in norm_q:
        hits.append({"tier": 1, "token": answers[0]})

    q_tokens = tokenize(question_text)
    correct_tokens = tokenize(answers[0])
    distractor_tokens = set()
    for a in answers[1:]:
        distractor_tokens |= tokenize(a)

    for tok in sorted(correct_tokens):
        if len(tok) < 4:
            continue
        if not any(_tokens_overlap(tok, qt) for qt in q_tokens):
            continue
        if any(_tokens_overlap(tok, dt) for dt in distractor_tokens):
            continue
        hits.append({"tier": 2, "token": tok})

    return hits


# Direct-to-video sequels and theatrical shorts historically under-mined
# relative to their parent film (see CLAUDE.md "richest under-mined veins").
# `parent` names a key in count_topics.py's film_keywords so its matches can
# be excluded from the parent's count -- None means no tracked parent.
SEQUELS_AND_SHORTS = [
    {"title": "The Lion King II: Simba's Pride", "parent": "The Lion King",
     "pattern": r"lion king ii|simba.?s pride|\bkiara\b|\bkovu\b|\bvitani\b|\bzira\b"},
    {"title": "The Return of Jafar", "parent": "Aladdin",
     "pattern": r"return of jafar"},
    {"title": "Aladdin and the King of Thieves", "parent": "Aladdin",
     "pattern": r"king of thieves|sa.?luk"},
    {"title": "The Little Mermaid II: Return to the Sea", "parent": "The Little Mermaid",
     "pattern": r"little mermaid ii|return to the sea|\bmelody\b.*ariel|morgana\b.*ursula"},
    {"title": "Mulan II", "parent": "Mulan",
     "pattern": r"\bmulan ii\b"},
    {"title": "Pocahontas II: Journey to a New World", "parent": "Pocahontas",
     "pattern": r"pocahontas ii|john rolfe"},
    {"title": "The Hunchback of Notre Dame II", "parent": "The Hunchback of Notre Dame",
     "pattern": r"hunchback.*\bii\b|\bzephyr\b|\bmadellaine\b|\bsarousch\b"},
    {"title": "Cinderella II: Dreams Come True", "parent": "Cinderella",
     "pattern": r"cinderella ii\b"},
    {"title": "Cinderella III: A Twist in Time", "parent": "Cinderella",
     "pattern": r"cinderella iii"},
    {"title": "Brother Bear 2", "parent": "Brother Bear",
     "pattern": r"brother bear 2"},
    {"title": "101 Dalmatians II: Patch's London Adventure", "parent": "101 Dalmatians",
     "pattern": r"dalmatians ii|patch.?s london adventure"},
    {"title": "The Jungle Book 2", "parent": "The Jungle Book",
     "pattern": r"jungle book 2|\branjan\b|\bshanti\b.*jungle"},
    {"title": "Tarzan II", "parent": "Tarzan",
     "pattern": r"tarzan ii\b"},
    {"title": "The Fox and the Hound 2", "parent": "The Fox and the Hound",
     "pattern": r"fox and the hound 2"},
    {"title": "Kronk's New Groove", "parent": "The Emperor's New Groove",
     "pattern": r"kronk.?s new groove"},
    {"title": "Bambi II", "parent": "Bambi",
     "pattern": r"bambi ii\b"},
    {"title": "Frozen Fever", "parent": "Frozen",
     "pattern": r"frozen fever"},
    {"title": "Olaf's Frozen Adventure", "parent": "Frozen",
     "pattern": r"olaf.?s frozen adventure"},
    {"title": "Geri's Game", "parent": None,
     "pattern": r"geri.?s game"},
    {"title": "Piper (Pixar short)", "parent": None,
     "pattern": r"\bpiper\b.*short|pixar short.*\bpiper\b"},
    {"title": "Bao (Pixar short)", "parent": None,
     "pattern": r"\bbao\b.*short|pixar short.*\bbao\b"},
]
