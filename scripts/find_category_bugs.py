"""
Whole-corpus check for CLAUDE.md rule #9: Pixar films must be tagged
`pixar`, not `movies` (Zootopia-style non-film-identity categories like
`characters` are unaffected -- this only checks the movies/pixar boundary).

Matches question text + answers[0] (same haystack convention as
count_topics.py) against a small allowlist of Pixar-vs-Disney film
identity patterns, then flags any `movies`-tagged question matching a
Pixar film or any `pixar`-tagged question matching a non-Pixar Disney
film. This is the exact check that was run as a one-off scratch script
during the 2026-07-29 quality audit and then lapsed (nothing re-ran it
since) -- checked in here so it doesn't lapse again, same rationale as
find_leaks.py for rule #2.

Advisory/lexical only: a question whose film identity isn't captured by
these patterns (e.g. it only names a character shared across films, or
uses phrasing these patterns don't cover) won't be flagged. Always
eyeball hits before recategorizing -- a pattern match isn't proof, just
a candidate.

Run from the project root: python scripts/find_category_bugs.py
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_corpus

# (film name, pattern, is_pixar). Kept intentionally small -- just the
# titles/characters specific enough to identify the film unambiguously,
# reused loosely from count_topics.py's film_keywords.
FILM_IDENTITY = [
    ("Toy Story", r"toy story|woody\b.*sheriff|buzz lightyear|stinky pete\b|lotso\b|bullseye\b.*horse|gabby gabby\b|\bforky\b", True),
    ("A Bug's Life", r"bug.?s life\b|\bflik\b.*ant\b|princess atta\b|\bmolt\b.*grasshopper\b|circus bugs\b", True),
    ("Monsters Inc/University", r"monsters,? inc\b|monsters university\b|\bsulley\b|mike wazowski\b|randall\b.*monster|dean hardscrabble\b|oozma kappa\b", True),
    ("Finding Nemo/Dory", r"finding nemo\b|finding dory\b|marlin\b.*clown|marine life institute\b|hank\b.*octopus", True),
    ("The Incredibles", r"incredibles\b|mr\.? incredible\b|elastigirl\b|edna mode\b|frozone\b|syndrome\b.*omnidroid|jack.?jack\b", True),
    ("Cars", r"lightning mcqueen|mater\b.*tow truck|radiator springs\b|chick hicks\b|doc hudson\b|piston cup\b|francesco bernoulli\b", True),
    ("Ratatouille", r"ratatouille\b|\bremy\b.*rat|linguini\b|gusteau\b|anton ego\b", True),
    ("WALL-E", r"wall.?e\b|buy n large\b|\baxiom\b.*ship", True),
    ("Up", r"carl fredricksen\b|ellie fredricksen\b|russell\b.*wilderness\b|\bdug\b.*talking dog\b|paradise falls\b", True),
    ("Brave", r"\bmerida\b|king fergus\b|queen elinor\b|mor.?du\b|dingwall\b.*clan", True),
    ("Inside Out", r"inside out\b|bing bong\b|core memories\b|hockey island\b|\briley\b.*emotions", True),
    ("Coco", r"\bcoco\b.*pixar|miguel\b.*guitar|hector\b.*rivera|ernesto.*de la cruz|land of the dead\b", True),
    ("Soul", r"\bsoul\b.*pixar|joe gardner\b|great before\b", True),
    ("Onward", r"ian lightfoot\b|barley lightfoot\b|phoenix gem\b|manticore\b.*tavern", True),
    ("Luca", r"\bluca\b.*sea monster|alberto\b.*sea monster|portorosso\b|ercole\b.*visconti", True),
    ("Turning Red", r"turning red\b|meilin lee\b|4.?town\b", True),
    ("Elemental", r"\belemental\b|ember\b.*fire element|ember\b.*lumen|element city\b", True),
    ("Lightyear", r"\blightyear\b.*(movie|film|2022)|zurg\b.*lightyear|sox\b.*cat robot", True),
    ("Elio", r"\belio\b.*(pixar|alien|communiverse)", True),
    ("The Good Dinosaur", r"good dinosaur\b|\barlo\b.*dinosaur|\bspot\b.*good dinosaur", True),
    ("Beauty and the Beast", r"beauty.*beast|\blumiere\b|cogsworth\b|mrs\.? potts\b", False),
    ("The Little Mermaid", r"little mermaid\b|\bariel\b|\bursula\b|prince eric\b|king triton\b|scuttle\b", False),
    ("Frozen", r"\bfrozen\b|\belsa\b|arendelle\b|\bkristoff\b|\bolaf\b|let it go\b", False),
    ("The Lion King", r"lion king\b|\bsimba\b|\bmufasa\b|\btimon\b|\bpumbaa\b|\brafiki\b|pride rock\b", False),
    ("Moana", r"\bmoana\b|\bmaui\b.*demigod|te fiti\b|te ka\b|\btamatoa\b|\bheihei\b|motunui\b", False),
    ("Aladdin", r"\baladdin\b|\bgenie\b.*lamp|\bjafar\b|\bjasmine\b.*agrabah|\bagrabah\b|cave of wonders\b", False),
    ("Pocahontas", r"\bpocahontas\b|governor ratcliffe\b|grandmother willow\b|\bnakoma\b", False),
    ("Encanto", r"\bencanto\b|madrigal\b|\bmirabel\b|\bcasita\b", False),
    ("Mulan", r"\bmulan\b|\bmushu\b.*dragon|shan yu\b|li shang\b|fa zhou\b", False),
    ("Tangled", r"\btangled\b|\brapunzel\b|flynn rider\b|mother gothel\b|snuggly duckling\b", False),
    ("The Hunchback of Notre Dame", r"hunchback\b|quasimodo\b|esmeralda\b|\bfrollo\b|\bclopin\b", False),
    ("Tarzan", r"\btarzan\b|\bkerchak\b|\bterk\b.*gorilla|clayton\b.*hunter", False),
    ("Zootopia", r"zootopia\b|judy hopps\b|nick wilde\b|bellwether\b|night howlers\b", False),
    ("The Emperor's New Groove", r"emperor.*groove\b|\bkuzco\b|\byzma\b|\bkronk\b", False),
    ("Big Hero 6", r"big hero 6\b|\bbaymax\b|san fransokyo\b", False),
    ("Wreck-It Ralph", r"wreck.?it ralph\b|vanellope\b|fix.?it felix\b|sugar rush\b.*game", False),
    ("Atlantis: The Lost Empire", r"atlantis.*lost empire\b|milo thatch\b|commander rourke\b|vinny santorini\b", False),
    ("Hercules", r"\bhercules\b.*disney|hades\b.*underworld|\bmegara\b|philoctetes\b", False),
    ("Cinderella", r"\bcinderella\b|lady tremaine\b|anastasia\b.*tremaine|\bdrizella\b|glass slipper\b", False),
    ("Bambi", r"\bbambi\b|\bthumper\b.*rabbit|great prince\b.*forest", False),
    ("101 Dalmatians", r"101 dalmatians|cruella de vil\b|\bpongo\b.*dalmatian|\bperdita\b.*dalmatian", False),
    ("The Jungle Book", r"jungle book\b|\bmowgli\b|\bbaloo\b|\bbagheera\b|shere khan\b", False),
    ("The Fox and the Hound", r"fox and the hound\b|\btod\b.*fox|\bcopper\b.*hound", False),
    ("Brother Bear", r"brother bear\b|\bkenai\b.*bear|\bkoda\b.*bear", False),
]


def check_category(q):
    """Returns a list of (film, wrong_category, right_category) mismatches
    for a single question dict -- used by validate_batch.py so this same
    check runs on new drafts, not just the whole-corpus pass below."""
    cat = q.get("category")
    if cat not in ("movies", "pixar"):
        return []
    haystack = q.get("question", "") + " " + (q.get("answers") or [""])[0]
    hits = []
    for film, pattern, is_pixar in FILM_IDENTITY:
        if re.search(pattern, haystack, re.IGNORECASE):
            if is_pixar and cat == "movies":
                hits.append((film, "movies", "pixar"))
            elif not is_pixar and cat == "pixar":
                hits.append((film, "pixar", "movies"))
    return hits


def main():
    corpus = load_corpus()
    bugs = []
    for q in corpus:
        for film, wrong, right in check_category(q):
            bugs.append((q, film, wrong, right))

    print(f"Scanned {len(corpus)} questions ({sum(1 for q in corpus if q.get('category') in ('movies','pixar'))} tagged movies/pixar).")
    print(f"\n--- Category mismatches (advisory, eyeball these): {len(bugs)} ---")
    for q, film, wrong, right in bugs:
        print(f"  id={q.get('id')}: tagged '{wrong}' but matches {film} (should be '{right}')")
        print(f"      {q.get('question')!r}  answers[0]={q.get('answers', [''])[0]!r}")
    # Advisory only -- a pattern match on an incidental mention (e.g. an actor's
    # other role named in passing) is common and not itself an error. Always 0.
    return 0


if __name__ == "__main__":
    sys.exit(main())
