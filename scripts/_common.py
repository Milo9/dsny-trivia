"""
Shared helpers for scripts/ tools: corpus loading, text normalization,
and the direct-to-video sequel / short registry used by both
count_topics.py and find_gaps.py.
"""
import json
import os
import re

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


def tokenize(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


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
