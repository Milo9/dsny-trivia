"""Backlog #6 rewords, researched and challenged by Claude on 2026-11-12."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def write(p, v): (ROOT / p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
AT = '2026-11-12'
NEXT = '2027-02-09'
LIM_OFFICIAL = 'Official Disney/Pixar page text inspected via fetch; no film viewing or in-person visit claimed.'
LIM_WIKI = 'Encyclopedia lead inspected; corroborates widely documented production facts. No film viewing claimed.'
LIM_FAN = 'Official Disney planning-forum answer (planDisney panelist), dated; not a formal policy page.'
S = {
 'r152-a113': ('https://en.wikipedia.org/wiki/A113', 'Lead paragraph', 'A113 is an inside joke referring to a CalArts animation classroom; it appears in almost every Pixar film. The code is written A113.', LIM_WIKI, False, ['pixar']),
 'r152-hall-presidents': ('https://disneyworld.disney.go.com/attractions/magic-kingdom/hall-of-presidents/', 'Location line: Located in Liberty Square at Magic Kingdom Park', 'The Hall of Presidents is in Liberty Square at Magic Kingdom and features Audio-Animatronics figures of all U.S. presidents.', LIM_OFFICIAL, True, ['parks']),
 'r152-fantasy-springs-names': ('https://disneyparksblog.com/disney-experiences/tokyo-disney-resort-announces-names-of-eighth-port-inspired-by-frozen-tangled-and-peter-pan', 'Oct 27, 2022 announcement; area name list', "Fantasy Springs has three areas: Frozen Kingdom, Rapunzel's Forest and Peter Pan's Never Land.", LIM_OFFICIAL, True, ['parks']),
 'r152-pixar-pier-neighborhoods': ('https://wdwnt.com/2018/05/four-neighborhoods-will-welcome-you-into-pixar-pier-at-disney-california-adventure/', 'May 2018 neighborhood rundown; Pixar Promenade section', 'Four neighborhoods: Incredibles Park, Toy Story Boardwalk, Pixar Promenade and Inside Out Headquarters; the Pixar Pal-A-Round Ferris wheel is the focal point of Pixar Promenade.', 'Specialist news report of the Disneyland Resort announcement at opening; corroborated by the D23 neighborhood list.', False, ['parks']),
 'r152-d23-inside-out': ('https://d23.com/inside-out-attraction-pixar-pier/', 'June 22, 2018 article; neighborhood list', 'D23 lists the Pixar Pier neighborhoods, including Inside Out Headquarters and Pixar Promenade.', LIM_OFFICIAL, False, ['parks']),
 'r152-hidden-mickeys-d23': ('https://d23.com/a-to-z/hidden-mickeys/', 'Complete entry', 'Hidden Mickeys are subtle silhouettes of Mickey Mouse, commonly the three-circle head form, worked into Disney designs.', LIM_OFFICIAL, False, ['cruise']),
 'r152-hidden-mickeys-ship': ('https://www.kennythepirate.com/2019/12/06/hidden-mickeys-how-many-can-you-find/', 'Dec 6, 2019 article; Disney Cruise Line paragraph', 'Hidden Mickeys can also be found at sea on Disney Cruise Line ships and on Castaway Cay.', 'Fan/specialist site; establishes the term is used for cruise ship decor. (An AllEars ship article returned HTTP 403 and was not used.)', False, ['cruise']),
 'r152-castaway-5k': ('https://plandisney.disney.go.com/question/register-castaway-cay-run-628629/', 'January 1, 2026 panelist answer', 'The Castaway Cay 5K is self-paced with no pre-registration; it is two laps and finishers collect a 5K medal at the bike rental stand.', LIM_FAN, True, ['cruise']),
 'r152-elemental': ('https://www.pixar.com/elemental', 'Opening synopsis', 'Elemental is set in Element City, where Fire-, Water-, Earth- and Air-residents live together.', LIM_OFFICIAL, False, ['pixar']),
 'r152-oliver-d23': ('https://d23.com/a-to-z/oliver-company-film/', 'Complete entry, first sentence', 'Oliver & Company is the Oliver Twist story animated with a twist.', LIM_OFFICIAL, False, ['movies']),
 'r152-oliver-wiki': ('https://en.wikipedia.org/wiki/Oliver_%26_Company', 'Lead paragraph', 'Oliver & Company is inspired by the Charles Dickens novel Oliver Twist.', LIM_WIKI, False, ['movies']),
 'r152-gmd-wiki': ('https://en.wikipedia.org/wiki/The_Great_Mouse_Detective', 'Lead paragraph', 'The Great Mouse Detective is based on the Basil of Baker Street books by Eve Titus and Paul Galdone.', LIM_WIKI, False, ['movies']),
 'r152-aristocats-wiki': ('https://en.wikipedia.org/wiki/The_Aristocats', 'Lead paragraphs', 'The Aristocats is based on a story by Tom McGowan and Tom Rowe, begun as a live-action TV script.', LIM_WIKI, False, ['movies']),
 'r152-lady-wiki': ('https://en.wikipedia.org/wiki/Lady_and_the_Tramp', 'Lead paragraph', "Lady and the Tramp is based on Ward Greene's 1945 Cosmopolitan story Happy Dan, the Cynical Dog.", LIM_WIKI, False, ['movies']),
 'r152-treasure-d23': ('https://d23.com/a-to-z/treasure-planet-film/', 'Complete entry, first sentence', "Treasure Planet is made with a nod to Robert Louis Stevenson's Treasure Island.", LIM_OFFICIAL, False, ['movies']),
 'r152-jungle-wiki': ('https://en.wikipedia.org/wiki/The_Jungle_Book_(1967_film)', 'Lead paragraph', "The Jungle Book (1967) is based on the Mowgli stories from Rudyard Kipling's 1894 book.", LIM_WIKI, False, ['movies']),
 'r152-pinocchio-wiki': ('https://en.wikipedia.org/wiki/Pinocchio_(1940_film)', 'Lead paragraph', "Pinocchio (1940) is loosely based on Carlo Collodi's 1883 novel The Adventures of Pinocchio.", LIM_WIKI, False, ['movies']),
 'r152-hunchback-wiki': ('https://en.wikipedia.org/wiki/The_Hunchback_of_Notre_Dame_(1996_film)', 'Lead paragraph', 'The Hunchback of Notre Dame (1996) is loosely based on the 1831 novel by Victor Hugo.', LIM_WIKI, False, ['movies']),
 'r152-mark-twain': ('https://disneyland.disney.go.com/attractions/disneyland/mark-twain-riverboat/', 'Along the Mississippi; Alternate Adventures', "The Mark Twain Riverboat is a steam-powered 19th-century-style paddle boat on Disneyland's Rivers of America; it shares the route with the Sailing Ship Columbia.", LIM_OFFICIAL, True, ['parks']),
 'r152-fowler': ('https://d23.com/a-to-z/admiral-joe-fowler-riverboat/', 'Complete entry', 'The Admiral Joe Fowler riverboat ran in Frontierland at Magic Kingdom from 1971 until fall 1980.', LIM_OFFICIAL, False, ['parks']),
 'r152-irvine': ('https://d23.com/walt-disney-legend/richard-irvine/', 'Final paragraph', "Walt Disney World's second paddle-wheel steamship, the Richard F. Irvine, was renamed Liberty Belle in 1996.", LIM_OFFICIAL, False, ['parks']),
}
lib = read('audit/source-notes.json')
for k, (url, loc, ev, lim, ts, topics) in S.items():
    lib['sources'][k] = dict(url=url, locator=loc, evidence=ev, checkedBy='Claude', checkedAt=AT,
                             timeSensitive=ts, nextReviewAt=NEXT if ts else None, limitations=lim, topics=topics)
write('audit/source-notes.json', lib)

ALL = ['singleAnswer', 'context', 'wording', 'noGiveaway', 'distinctFact', 'category', 'difficulty', 'scope']
D, X, C, E = 'direct', 'exclusive-inference', 'contradiction', 'exhaustive-list'
R = {
 2432: dict(ctx='Onward (2020) final police radio dispatch; recurring CalArts code.', ts=False,
   notes='Pixar topic and A113 cross-bank search read; no other A113 question. Distractors replaced with near-miss codes after the player flag said the old ones made no sense.',
   premise=('The Onward screenplay has a police radio call "a 113 in progress"; A113 is the recurring CalArts classroom code in Pixar films.', ['b38-onscript', 'r152-a113']),
   opts=[(D, 'The radio call echoes A113, the recurring Pixar code.', ['b38-onscript', 'r152-a113']),
         (X, 'A131 transposes the digits; the recurring code is A113 and the dispatch says 113.', ['b38-onscript', 'r152-a113']),
         (X, 'B113 changes the letter; the CalArts classroom code is A113.', ['r152-a113']),
         (X, 'A311 reverses the digits; neither the dispatch nor the recurring code uses 311.', ['b38-onscript', 'r152-a113'])],
   ch='Tried each near-miss as a variant: the source says A113 "and its variants" exist across media, but none of A131/B113/A311 is the classroom number or the spoken 113. Exactly one option matches.'),
 1355: dict(ctx='Walt Disney World Magic Kingdom land placement, November 2026.', ts=True,
   notes='Reframed from the attraction name (which repeated "presidents") to its land. Read Magic Kingdom land questions #94, #100, #599, #779, #1138: other attractions; #599 shares the Liberty Square answer but asks Haunted Mansion, a different fact.',
   premise=("Disney's official page places The Hall of Presidents in Liberty Square at Magic Kingdom.", ['r152-hall-presidents']),
   opts=[(D, 'Official page: located in Liberty Square.', ['r152-hall-presidents']),
         (X, 'Frontierland is a different land; the official location is Liberty Square.', ['r152-hall-presidents']),
         (X, 'Main Street, U.S.A. is a different land; the official location is Liberty Square.', ['r152-hall-presidents']),
         (X, 'Tomorrowland is a different land; the official location is Liberty Square.', ['r152-hall-presidents'])],
   ch='Checked that this is Magic Kingdom, not Disneyland (no Hall of Presidents there) and that the attraction is listed as current. Single location; no land boundary ambiguity.'),
 2243: dict(ctx='Tokyo DisneySea Fantasy Springs area names (opened June 2024).', ts=True,
   notes='Replaced distractors with Frozen-prefixed names so the stem\'s "Frozen-themed" no longer singles out the answer. Fantasy Springs digest read: #2241 year, #2242 third film, #2244/#2245 ride names; #2532 is Hong Kong.',
   premise=('Disney\'s naming announcement lists exactly three areas, one named Frozen Kingdom.', ['r152-fantasy-springs-names']),
   opts=[(D, 'Frozen Kingdom is the announced Frozen area.', ['r152-fantasy-springs-names']),
         (E, 'Frozen Fjord is not among the three announced area names.', ['r152-fantasy-springs-names']),
         (E, 'Frozen Village is not among the three announced area names.', ['r152-fantasy-springs-names']),
         (E, 'Frozen Harbor is not among the three announced area names.', ['r152-fantasy-springs-names'])],
   ch="Exhaustive three-name list excludes all distractors. Checked Hong Kong's World of Frozen is not Fantasy Springs; the stem pins Tokyo DisneySea."),
 2642: dict(ctx='Disney California Adventure Pixar Pier at its June 2018 opening.', ts=False,
   notes='Removed the wheel\'s "Pixar Pal-A-Round" name, which paired with the Pixar Promenade answer. Remaining "Pixar" token is the land name shared by all four real neighborhoods (decision recorded). Pixar Pier digest read: #623, #2239 ask other facts.',
   premise=('At opening the Pixar Pal-A-Round Ferris wheel was the focal point of Pixar Promenade.', ['r152-pixar-pier-neighborhoods', 'r152-d23-inside-out']),
   opts=[(D, 'The Ferris wheel is the focal point of Pixar Promenade.', ['r152-pixar-pier-neighborhoods']),
         (X, 'Incredibles Park holds the Incredicoaster, not the wheel.', ['r152-pixar-pier-neighborhoods']),
         (X, 'Toy Story Boardwalk holds Toy Story Midway Mania! and the carousel, not the wheel.', ['r152-pixar-pier-neighborhoods']),
         (X, 'Inside Out Headquarters is the western-end neighborhood with the Inside Out attraction, not the wheel.', ['r152-pixar-pier-neighborhoods', 'r152-d23-inside-out'])],
   ch='Checked that the wheel is the only giant Ferris wheel on the pier and is assigned to one neighborhood, Pixar Promenade. Historical 2018 anchor avoids later re-theming.'),
 1236: dict(ctx='Fan term used across Disney parks and ships.', ts=False,
   notes='Removed "Mickey Mouse" from the stem; the answer is still easy by design. No other Hidden Mickey question in the bank.',
   premise=('D23 defines Hidden Mickeys as subtle three-circle Mickey silhouettes; fans hunt them aboard Disney ships.', ['r152-hidden-mickeys-d23', 'r152-hidden-mickeys-ship']),
   opts=[(D, 'Hidden Mickeys is the documented term.', ['r152-hidden-mickeys-d23', 'r152-hidden-mickeys-ship']),
         (X, 'Magic Marks is not the term; D23 names these Hidden Mickeys.', ['r152-hidden-mickeys-d23']),
         (X, 'Castaway Icons is not the term; D23 names these Hidden Mickeys.', ['r152-hidden-mickeys-d23']),
         (X, 'Pixie Prints is not the term; D23 names these Hidden Mickeys.', ['r152-hidden-mickeys-d23'])],
   ch='"Mouse-head silhouettes" still points at Mickey but no longer contains the answer word. Checked none of the distractors is an established fan term.'),
 427: dict(ctx='Castaway Cay self-paced run/walk, as of November 2026.', ts=True,
   notes='Answers are now distances, so "Castaway Cay" in the stem no longer matches the answer text. No other Castaway Cay run question.',
   premise=('A January 2026 planDisney answer describes the self-paced Castaway Cay 5K (two laps, medal at the bike stand).', ['r152-castaway-5k']),
   opts=[(D, 'The self-paced event is the 5K.', ['r152-castaway-5k']),
         (C, '10K contradicts the documented 5K distance.', ['r152-castaway-5k']),
         (C, 'A half marathon contradicts the documented 5K distance.', ['r152-castaway-5k']),
         (C, 'One mile contradicts the documented 5K distance.', ['r152-castaway-5k'])],
   ch='Two laps make up the 5K, not a 10K. The January 2026 answer describes a single self-paced 5K and names no other distance; the stem asks about that one event. Changeable: recheck scheduled.'),
 2589: dict(ctx="Pixar's Elemental (2023) setting.", ts=False,
   notes='Distractors now all share the Element- stem, so "Elemental" in the stem no longer singles out the answer. Elemental digest read: #1411 asks Firetown (a borough), a different fact.',
   premise=("Pixar's synopsis: set in Element City, where Fire, Water, Earth and Air residents live together.", ['r152-elemental']),
   opts=[(D, 'Element City is named in the synopsis.', ['r152-elemental']),
         (X, 'Elementia is not the city named by Pixar.', ['r152-elemental']),
         (X, 'Element Bay is not the city named by Pixar.', ['r152-elemental']),
         (X, 'Elemental Heights is not the city named by Pixar.', ['r152-elemental'])],
   ch='Checked Firetown (a district) is not among the options, so the city/district distinction cannot create a second answer.'),
 518: dict(ctx='Source novels of Disney animated features.', ts=False,
   notes='Inverted: the stem names Dickens, the answer is the film, so the film title no longer echoes "Oliver Twist". Read the Oliver & Company digest and adaptation questions (#2499, #2787 etc.); none asks the Dickens source.',
   premise=("Oliver & Company is inspired by Dickens's Oliver Twist.", ['r152-oliver-d23', 'r152-oliver-wiki']),
   opts=[(D, "Inspired by Dickens's Oliver Twist.", ['r152-oliver-d23', 'r152-oliver-wiki']),
         (C, "Based on Eve Titus's Basil of Baker Street books, not Dickens.", ['r152-gmd-wiki']),
         (C, 'Based on a story by Tom McGowan and Tom Rowe, not Dickens.', ['r152-aristocats-wiki']),
         (C, "Based on Ward Greene's story, not Dickens.", ['r152-lady-wiki'])],
   ch="The Great Mouse Detective's Victorian London setting is a plausible Dickens confusion, but its source is Eve Titus. Disney's A Christmas Carol (2009) would also qualify but is not an option."),
 521: dict(ctx='Source novels of Disney animated features.', ts=False,
   notes='Inverted: the stem names Stevenson, so the film title no longer echoes "Treasure Island". Treasure Planet digest read; #404/#2861-2865 concern the live-action 1950 Treasure Island, excluded by "animated".',
   premise=("Treasure Planet is built on Stevenson's Treasure Island.", ['r152-treasure-d23']),
   opts=[(D, "D23: a nod to Stevenson's Treasure Island.", ['r152-treasure-d23']),
         (C, "Based on Kipling's Jungle Book stories.", ['r152-jungle-wiki']),
         (C, "Based on Collodi's novel.", ['r152-pinocchio-wiki']),
         (C, "Based on Victor Hugo's novel.", ['r152-hunchback-wiki'])],
   ch='Checked the live-action Treasure Island (1950) is excluded by "animated feature" and is not an option. Each distractor has a different, named literary source.'),
 925: dict(ctx='Disneyland Rivers of America vessels, November 2026.', ts=True,
   notes='Removed "Riverboat"/"Sailing Ship" from the options so the answer text no longer matches the stem. Read #909, #918, #1148, #2082 river questions; #918 asks the Liberty Belle renaming, a different fact.',
   premise=("Disneyland's Mark Twain is a steam paddle boat on the Rivers of America.", ['r152-mark-twain']),
   opts=[(D, "Mark Twain is Disneyland's paddle boat on the Rivers of America.", ['r152-mark-twain']),
         (X, "Liberty Belle is the renamed Walt Disney World paddle-wheeler, not Disneyland's.", ['r152-irvine']),
         (C, 'Columbia shares the route but is a sailing ship, not a paddle-wheel riverboat.', ['r152-mark-twain']),
         (X, 'Admiral Joe Fowler ran at Magic Kingdom (1971-1980), not Disneyland.', ['r152-fowler'])],
   ch="Columbia circles the same river, so the paddle-wheel qualifier is what excludes it; the official page names it the Sailing Ship Columbia. #2082's stem also names the Mark Twain Riverboat; accepted as incidental context."),
}
n = read('audit/runs/release-1.52-flag-followup-template.json')
used = set()
for r in n['reviews']:
    d = R[r['questionId']]
    r.update(checks=ALL, notes=d['notes'], context=d['ctx'], timeSensitive=d['ts'], nextReviewAt=NEXT if d['ts'] else None)
    r['premise'] = dict(reason=d['premise'][0], sources=d['premise'][1]); used.update(d['premise'][1])
    r['options'] = [dict(basis=b, reason=t, sources=s) for b, t, s in d['opts']]
    for _, _, s in d['opts']: used.update(s)
    r['challenge'] = dict(reviewer='Claude', at=AT, premiseChecked=True, alternativesExcluded=True, notes=d['ch'])
n['sourcesChecked'] = sorted(used)
write('audit/runs/release-1.52-flag-followup-evidence-notes.json', n)
n2 = dict(n, reviews=[r for r in n['reviews'] if r['questionId'] in (1236, 427)])
n2['sourcesChecked'] = sorted({s for r in n2['reviews'] for s in r['premise']['sources'] + [x for o in r['options'] for x in o['sources']]})
write('audit/runs/release-1.52-flag-followup-renewal-notes.json', n2)
print('ok', len(n['reviews']))
