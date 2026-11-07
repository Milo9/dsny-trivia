"""Serialize the research and final option challenges performed by Codex."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'audit/runs/next-shard-0003-reviews'
OUT.mkdir(exist_ok=True)
packet = json.loads((ROOT / 'artifacts/question-audit/current.json').read_text(encoding='utf-8'))

S = {
 'epcot': ('https://d23.com/a-to-z/epcot/', 'Opening paragraph: acronym coined in 1966 and its exact expansion.'),
 'slinky': ('https://d23.com/a-to-z/slinky-dog-dash/', 'Opening paragraph: named family coaster, Toy Story Land, Hollywood Studios.'),
 'shanghai': ('https://d23.com/a-to-z/shanghai-disneyland/', 'Opening paragraph: park name and June 16, 2016 opening.'),
 'shanghai2': ('https://thewaltdisneycompany.com/news/shanghai-disney-resort-opens-in-mainland-china/', 'June 16, 2016 publication; opening ceremony and park dedication naming Shanghai Disneyland.'),
 'six': ('https://disneyexperiences.com/press-room/', 'Opening overview: six resort destinations; International Parks section calls Shanghai sixth and Abu Dhabi a future seventh.'),
 'ticket': ('https://d23.com/e-ticket-memories-five-favorite-facts-about-ticket-books/', 'Section 1: public opening July 18, 1955, $1 gate admission, separate ride tickets; October adult coupon book was $2.50.'),
 'ticket2': ('https://mickeyblog.com/2023/07/17/heres-how-much-disneyland-cost-on-opening-day/', 'Adult admission $1 versus 50 cents for children; used to disambiguate the adult price.'),
 'castle': ('https://d23.com/a-to-z/sleeping-beauty-castle/', 'Opening paragraph identifies Sleeping Beauty Castle as the Fantasyland landmark at Disneyland.'),
 'rail': ('https://d23.com/a-to-z/walt-disney-world-railroad/', 'Opening two paragraphs: named Magic Kingdom attraction; tracks circle the park.'),
 'orleans': ('https://d23.com/a-to-z/new-orleans-square/', 'Opening paragraph: land dedicated July 24, 1966 by Walt Disney and the mayor of New Orleans.'),
 'orleans2': ('https://disneyvacationclub.disney.go.com/media/dvc/languagespecific/eng/member/justformembers/disneyfilesmagazine/2009/DisneyFilesMagazine_Winter2009.pdf', 'PDF page 29, opening New Orleans history: July 24, 1966 opening ceremony with Mayor Victor Schiro and Walt\'s speech.'),
 'paris': ('https://d23.com/a-to-z/disneyland-paris/', 'Opening paragraph: original Euro Disney name; Disneyland Paris became official October 1, 1994.'),
 'walt': ('https://d23.com/about-walt-disney/', 'Biography paragraphs: Chicago birth, McKinley school and evening art classes; Hollywood arrival/office; daughters Diane and Sharon.'),
 'walt2': ('https://www.televisionacademy.com/bios/walt-disney', 'Birthplace field: Chicago, Illinois; biography states 22 Oscar wins.'),
 'films': ('https://www.disneyanimation.com/films/', 'Intro identifies first fully animated feature in 1937; filmography lists Snow White 1937, Pinocchio/Fantasia 1940, Bambi 1942; Aladdin 1992 and other film release years.'),
 'mickey': ('https://d23.com/a-to-z/mickey-mouse/', 'Opening paragraphs: Walt\'s primary cartoon character; naming legend about Mortimer, Lillian and Mickey; collaboration with Ub Iwerks.'),
 'stuart': ('https://search.worldcat.org/title/305785', 'First-edition 1945 Stuart Little catalog record: E. B. White author, Garth Williams illustrator, Harper & Brothers publisher.'),
 'danger': ('https://www.cosgrovehallfilmsarchive.co.uk/aboutcosgrovehall', 'Studio origins and Danger Mouse paragraphs: Cosgrove/Hall founders and their studio\'s creation.'),
 'danger2': ('https://www.televisionacademy.com/features/news/news/mark-hall-acclaimed-british-animator', 'Opening and career paragraphs attribute Danger Mouse to Mark Hall and Brian Cosgrove.'),
 'jerry': ('https://interviews.televisionacademy.com/shows/tom-and-jerry', 'Joseph Barbera interview catalog, 09:36 segment: partnership with William Hanna and creation of Tom and Jerry.'),
 'oswald': ('https://d23.com/a-to-z/oswald-the-lucky-rabbit/', 'Opening paragraph: 26 Disney silent Oswald cartoons made between 1927 and 1928 for Mintz/Universal; complete series list follows.'),
 'oscars': ('https://www.disneyplus.com/en-nz/explore/articles/oscars-academy-awards-guide-2026', 'Everything Else / Who has won the most Oscars: 22 competitive and four honorary.'),
 'pooh': ('https://www.oscars.org/oscars/ceremonies/1969', 'Short Subject (Cartoon), Winner: Winnie the Pooh and the Blustery Day; Walt Disney, Producer.'),
 'carol': ('https://d23.com/a-to-z/carolwood-pacific-railroad/', 'Opening paragraph: named backyard miniature railroad, Holmby Hills, early 1950s.'),
 'lilly': ('https://d23.com/a-to-z/lilly-belle/', 'Opening paragraph distinguishes the Lilly Belle locomotive from its railroad, the Carolwood Pacific.'),
 'laugh': ('https://d23.com/a-to-z/laugh-o-gram-films/', 'Opening paragraph: Kansas City company and its seven modernized fairy-tale shorts in 1922.'),
 'alice': ('https://d23.com/a-to-z/alice-comedies/', 'Opening paragraphs: Kansas City pilot versus 56 Hollywood series shorts made 1924–1927.'),
 'school': ('https://mouseplanet.com/chicago-walt/4040/', 'McKinley High School section, paragraph beginning The same year: evening cartooning at Chicago Academy of Fine Arts, 81 East Monroe Street.'),
 'poppins': ('https://d23.com/a-to-z/mary-poppins-film/', 'Release/cast paragraphs: 1964, Julie Andrews as Mary Poppins; effects paragraph explains live-action/animation combination.'),
 'jungle': ('https://d23.com/a-to-z/jungle-book-the-film/', 'Release and voice-cast paragraphs: 1967 animated film; last animated feature supervised by Walt.'),
 'sword': ('https://d23.com/a-to-z/sword-in-the-stone-the-film/', 'Animated feature description; December 25, 1963 release and voice cast.'),
 'bed': ('https://d23.com/a-to-z/bedknobs-and-broomsticks-film/', 'Release/cast paragraph: 1971, Angela Lansbury; animation sequences described later.'),
 'dcl': ('https://d23.com/a-to-z/disney-cruise-line/', 'Opening paragraph: first Disney Magic voyage July 30, 1998, Port Canaveral; Wonder 1999. Final paragraph: Dream 2011 and Fantasy March 31, 2012.'),
 'magic': ('https://d23.com/a-to-z/disney-magic/', 'Opening paragraph: first fleet ship; maiden voyage July 30, 1998 from Port Canaveral.'),
 'fleet': ('https://disneyexperiences.com/app/uploads/2025/02/Final-DCL-Disney-Connect-Fact-SheetQ2.pdf', 'PDF page 1: launch in 1998 and fleet debut years Magic 1998, Wonder 1999, Dream 2011, Fantasy 2012; page 2 Lookout Cay opening month.'),
 'horn': ('https://touringplans.com/blog/disney-cruise-line-what-is-a-ship-horn-battle-dcl-in-a-jiffy/', 'Paragraph beginning Any historian: Magic and Wonder have one tune, When You Wish Upon a Star; Dream/Fantasy have multiple.'),
 'horn2': ('https://mouseplanet.com/seacret-stuff-on-the-disney-cruise-line/8326/', 'The Ship\'s Horn section: classic tune, Dream-expanded repertoire, and distinction between Magic/Wonder air horns and later ships.'),
 'club': ('https://disneycruise.disney.go.com/en-as/onboard-activities/oceaneer-youth-club/', 'Disney\'s Oceaneer Club heading, Ship Locations and On the Disney Magic section explicitly including Marvel Super Hero Academy.'),
 'cay': ('https://d23.com/a-to-z/disney-cruise-line/', 'Second paragraph: Gorda Cay renamed Disney\'s Castaway Cay, Bahamas private island cruise stop.'),
 'flag': ('https://www.bahamasmaritime.com/bma-news/bma-welcomes-disney-destiny/', 'December 5, 2025 article, opening paragraph: newest Disney Destiny proudly registered under The Bahamas flag.'),
 'lookout': ('https://disneyparksblog.com/dcl/first-look-at-disney-lookout-cay-at-lighthouse-point/', 'June 7, 2024 date and opening paragraph: welcoming guests for previews today on Eleuthera, ahead of debut.'),
 'remy': ('https://disneycruise.disney.go.com/en-as/onboard-activities/remy-restaurant/', 'Ship Locations lists Fantasy and Dream; opening and Bon Appetit sections identify adult-exclusive French cuisine.'),
 'palo': ('https://disneycruise.disney.go.com/en-as/onboard-activities/palo-restaurant/', 'Opening and Exquisite Italian Cuisine sections: adult-exclusive Northern Italian dining.'),
 'lumiere': ('https://disneycruise.disney.go.com/en-as/onboard-activities/lumieres-restaurant/', 'Ship Locations: Magic; Rotational Dining identifies main dining room rather than adult-exclusive Remy specialty venue.'),
 'triton': ('https://disneycruise.disney.go.com/en-as/onboard-activities/tritons-restaurant/', 'Ship Locations: Wonder; Rotational Dining identifies main dining room rather than adult-exclusive Remy specialty venue.'),
 'fantasy': ('https://d23.com/a-to-z/disney-fantasy/', 'Opening paragraph: christening March 1, 2012 and maiden voyage March 31.'),
 'aladdin': ('https://d23.com/a-to-z/aladdin-film/', '1992 release paragraph; songwriting paragraph states Tim Rice wrote A Whole New World for the production.'),
 'let': ('https://www.mtishows.com/sites/default/files/let_it_go_lyric_sheet.pdf', 'PDF page 1, first chorus, second line; licensed Frozen JR lyric sheet. Film wording corroborated separately, not inferred from the stage adaptation alone.'),
 'let2': ('https://www.disneyclips.com/lyrics/frozenlyrics5.html', 'Frozen / Let It Go, first chorus immediately after Well now they know; identifies Idina Menzel as Elsa. Secondary film transcription agrees with licensed sheet.'),
 'hakuna': ('https://www.mtishows.com/sites/default/files/tlkexperience_kids_actors_script.pdf', 'PDF page 3 (printed script pages 4–5), Hakuna Matata opening, measures 1–4; licensed musical excerpt.'),
 'hakuna2': ('https://www.youtube.com/watch?v=1djExjes5G4', 'Official Disney Sing-Alongs lyric-video search-index description reproduces the opening completion; corroboration only, full video was not available to inspect.'),
 'hakuna3': ('https://www.disneyclips.com/lyrics/lyrics66.html', 'The Lion King / Hakuna Matata film transcription, opening two lines; corroborates licensed stage score wording independently of the unavailable video playback.'),
}

# Each tuple supplies sources and a separate final-wording rationale for each option.
D = {
101: (['epcot'], ['Exact expansion of the acronym.', 'Park replaces Prototype and is not the expansion.', 'Enhanced Park for is not the expansion.', 'Expanding Park Center is not the expansion.']),
104: (['slinky'], ['Named Toy Story Land family coaster.', 'Not the documented name of that coaster.', 'Not the documented name of that coaster.', 'Not the documented name of that coaster.']),
105: (['shanghai','shanghai2'], ['Official park name in Shanghai.', 'Not its official park name.', 'Reverses the words; not its official name.', 'Magic Kingdom is not the Shanghai park\'s name.']),
106: (['six'], ['Six operating resort destinations at the stated date.', 'Undercounts the six destinations.', 'Counts the announced future seventh resort as if open.', 'Exceeds the six operating destinations.']),
109: (['ticket','ticket2'], ['Adult entry was one dollar; rides were separate.', 'Child entry price, not adult entry.', 'October adult ticket-book bundle price, not July gate-only admission.', 'Not the documented adult admission price.']),
110: (['castle'], ['Exact official Disneyland landmark name.', 'A different castle name, not this Disneyland landmark.', 'Character-based paraphrase is not the official landmark name.', 'Descriptive location label is not the official name.']),
111: (['shanghai','shanghai2'], ['The opening was in June 2016.', 'Two years before the documented opening.', 'Two years after the documented opening.', 'Four years before the documented opening.']),
112: (['rail'], ['Documented name of the railroad circling Magic Kingdom.', 'Not that attraction\'s documented name.', 'Not that attraction\'s documented name.', 'Not that attraction\'s documented name.']),
113: (['orleans','orleans2'], ['D23 records this land\'s 1966 dedication with Walt and the New Orleans mayor.', 'Not the land identified in that dedication record.', 'Not the land identified in that dedication record.', 'Not the Disneyland land in the recorded event.']),
114: (['paris'], ['The official name adopted on the specified date.', 'Original name superseded by that naming event.', 'Not the adopted official name.', 'Not the adopted official name.']),
118: (['walt','walt2'], ['Both biographies identify Chicago as birthplace.', 'Not the documented birthplace.', 'Not the documented birthplace.', 'Not the documented birthplace.']),
119: (['films','walt'], ['Studio explicitly identifies Snow White as its first fully animated feature, in 1937.', 'Filmography dates it to 1940, after Snow White.', 'Filmography dates it to 1940, after Snow White.', 'Filmography dates it to 1942, after Snow White.']),
120: (['mickey','stuart','danger','danger2','jerry'], ['Disney\'s primary mouse character; Walt and Ub Iwerks collaborated on his creation.', 'E. B. White\'s literary character, not Walt\'s creation.', 'Cosgrove and Hall creation from a different studio.', 'Hanna and Barbera creation, not Walt Disney\'s mouse.']),
122: (['oswald'], ['The named star of the 1927–1928 Oswald theatrical shorts.', 'Not the star named by the complete Oswald series record.', 'Not the star named by the complete Oswald series record.', 'Not the star named by the complete Oswald series record.']),
123: (['oscars','walt2','pooh'], ['22 competitive wins; the 1969 Academy record confirms the posthumous winner.', 'Below the expressly stated competitive total.', 'Below the expressly stated competitive total.', 'Above the competitive total; honorary/technical totals are outside the question.']),
127: (['walt'], ['Biography names both daughters Diane and Sharon.', 'Not the named pair of daughters.', 'Not the named pair of daughters.', 'Lillian was Walt\'s wife; this is not the named daughter pair.']),
128: (['mickey'], ['Mortimer is the proposal in the explicitly attributed naming legend.', 'Not the proposed name in that account.', 'Not the proposed name in that account.', 'Not the proposed name in that account.']),
129: (['carol','lilly'], ['Name of the whole backyard railway in Holmby Hills.', 'Not its documented proper name.', 'Confuses the Lilly Belle locomotive with the railroad; Express is not the documented railroad name.', 'Not its documented proper name.']),
130: (['laugh','alice','mickey'], ['Named series of 1922 Kansas City fairy-tale shorts.', 'Mickey\'s shorts began later, not the 1922 series.', 'Not the named 1922 fairy-tale series.', 'The Kansas City pilot does not make Alice Comedies the named 1922 fairy-tale series; later series shorts were made in Hollywood.']),
131: (['walt','alice'], ['The California production began in a Hollywood real estate office, within Los Angeles.', 'The later Burbank studio is not the first Hollywood office.', 'Not the documented first California studio city.', 'Not the documented first California studio city.']),
134: (['walt','school'], ['Academy identified in the primary biography; Korkis corroborates full Chicago name and evening classes.', 'A different institution from the named academy.', 'A different institution from the named academy.', 'A different institution and city from the named Chicago academy.']),
135: (['poppins','jungle','sword','bed'], ['1964 release, Andrews lead and live-action/animation all match.', '1967 animated feature with a different voice cast.', '1963 animated feature with a different voice cast.', 'Does combine media, but was released in 1971 and starred Angela Lansbury.']),
136: (['dcl','magic','fleet'], ['Magic was the first; fleet chronology starts with it in 1998.', 'Wonder followed in 1999.', 'Dream followed in 2011.', 'Fantasy followed in 2012.']),
137: (['dcl','fleet'], ['Both chronology and fact sheet place operating debut in 1998.', 'Before the operating debut; no confusion with planning/founding.', 'After the operating debut.', 'After the operating debut.']),
138: (['horn','horn2'], ['Classic Magic/Wonder melody, distinguished from the later ships\' larger repertoires.', 'Documented in the expanded Dream repertoire, not the original Magic-class classic tune.', 'Documented in the expanded Dream repertoire, not the original Magic-class classic tune.', 'Not the sole classic Magic/Wonder melody in the explicit repertoire account.']),
139: (['dcl','magic'], ['Both historical entries identify Port Canaveral as departure homeport.', 'Not the recorded port for this 1998 voyage.', 'Not the recorded port for this 1998 voyage.', 'Not the recorded port for this 1998 voyage.']),
140: (['club'], ['Official Oceaneer Club page locates Marvel Super Hero Academy in its Disney Magic section.', 'Not the named space in that ship-specific section.', 'Not the named space in that ship-specific section.', 'Not the named space in that ship-specific section.']),
141: (['cay','fleet'], ['The documented private Bahamian island is Castaway Cay.', 'Not the Disney private island named in the record.', 'Not the Disney private island named in the record.', 'Not the Disney private island named in the record.']),
146: (['flag'], ['The national registry authority explicitly states Bahamian registration for Destiny in 2025.', 'Not the flag recorded by its registry authority.', 'Not the flag recorded by its registry authority.', 'Not the flag recorded by its registry authority.']),
147: (['lookout','fleet'], ['Dated June 7 article states previews welcome guests today; fact sheet confirms opening month.', 'One month before the documented first previews.', 'One month after the documented first previews.', 'Two months after the documented first previews.']),
148: (['remy','palo','lumiere','triton'], ['Remy is adult-exclusive French dining on both named ships.', 'Palo is Italian, so fails the French qualifier.', 'Lumiere\'s is a Magic main dining venue, not the adult-exclusive restaurant on these two ships.', 'Triton\'s is a Wonder main dining venue, not the adult-exclusive restaurant on these two ships.']),
149: (['fantasy','dcl','fleet'], ['Documented maiden voyage March 31, 2012; distinct from float-out or christening.', 'One year before the recorded maiden voyage.', 'Two years after the recorded maiden voyage.', 'Two years before the recorded maiden voyage.']),
151: (['aladdin','films'], ['Aladdin introduced the song in its 1992 production.', '1991 film; not the production that introduced the 1992 song.', '1989 film; not the production that introduced the 1992 song.', '1995 film; not the production that introduced the 1992 song.']),
154: (['let','let2'], ['The exact missing word is anymore in both licensed sheet and film transcription.', 'Not the word at that position.', 'Not the word at that position.', 'A different two-word phrase, not the exact lyric completion.']),
155: (['hakuna','hakuna3'], ['Phrase completes the opening line in the licensed score and the film transcription.', 'Not the word completing that line.', 'Not the word completing that line.', 'Not the word completing that line.']),
}

SPECIAL = {
109: 'Challenged adult versus child prices, admission versus October coupon bundles, and public opening versus the invitation-only ceremony. Both price and scope are now explicit.',
119: 'Challenged whether any listed film predates Snow White; the complete official filmography gives later years for all three. Official-title length is unavoidable rather than an explanatory clue.',
120: 'Challenged attribution rather than merely mouse identity: all four are mice, but the alternative creators are White, Cosgrove/Hall and Hanna/Barbera. No TV-show facts are being tested.',
122: 'Challenged earlier Disney animals and the original cat distractor giveaway. Final options are four rabbits, and the premise now pins theatrical shorts to 1927–1928. The Oswald series record excludes the three other rabbit names.',
123: 'Challenged lifetime versus posthumous and competitive versus honorary/technical totals. Academy confirms the 1969 posthumous credit; the explicitly competitive count is corroborated independently by the Television Academy.',
128: 'Challenged legend versus established production history; wording now attributes the traditional story rather than presenting an uncertain private conversation as independently proven.',
129: 'Challenged Lilly Belle as an alternative name: it is the locomotive, not the Carolwood Pacific railroad. Source explicitly distinguishes them.',
130: 'Challenged Alice: its pilot was made in Kansas City, but the prompt now asks specifically for the 1922 modernized fairy-tale series, not everything made by the company.',
134: 'Challenged Art Institute confusion and duplicate distractors. Primary biography identifies the academy; the historian supplies its full name. Final four institutions are different.',
135: 'Challenged Bedknobs because it also mixes live action and animation; its year and lead actress fail. Removed the unsupported last-major-production assertion, since Walt later supervised The Jungle Book.',
138: 'Challenged the player-reported multi-answer problem: Dream can play the first three listed songs. Final scope is the original Magic-class classic melody; TouringPlans explicitly limits Magic/Wonder to one tune and Korkis corroborates the classic/expanded distinction. Original Disney blog failed to load; these independent specialist accounts are the evidence limitation, not an inspected video. Recheck scheduled.',
140: 'Challenged generic kids-space wording against nursery, Lab, Edge and Vibe. Final question tests the Marvel Academy association on Disney Magic, which the official club page states, rather than generic youth-club age/name recall. Historical month anchors the space configuration.',
147: 'Challenged whether Lookout Cay is itself a separate private island: it is on Eleuthera. Final question instead tests the specific first-preview date, which the June 7 announcement establishes, rather than duplicating the destination-name question 1512.',
148: 'Challenged Lumiere\'s and Triton\'s because both serve French-influenced meals. Their ship locations and main-dining status fail the full premise; Palo is Italian.',
154: 'Challenged semantic substitutes and the later chorus. This asks exact English wording at the quoted first-chorus position. Licensed stage sheet is corroborated by the film transcription; it is not assumed to prove every film lyric by itself.',
155: 'Challenged plausible rhyming/semantic substitutions; the opening phrase has a fixed last noun. Licensed score directly prints it and the film transcription independently agrees. Full official video playback was unavailable, so an uninspected video is not treated as proof.',
}

for item in packet['questions']:
    qid = item['question']['id']
    keys, reasons = D[qid]
    review = copy.deepcopy(item['reviewTemplate'])
    review['reviewer'] = 'Codex'
    review['manual'] = {k: True for k in review['manual']}
    review['notes'] = 'Read all four options, relevant full topic digests and cross-bank comparisons. Category and editorial difficulty checked on final wording. ' + SPECIAL.get(qid, 'Final challenge checks the exact named entity/event against each listed alternative, not merely a matching answer keyword.')
    v = review['verification']
    v['context'] = item['question']['question']
    v['timeSensitive'] = qid == 138
    v['nextReviewAt'] = '2027-02-04' if qid == 138 else None
    sources = [{'url': S[k][0], 'locator': S[k][1]} for k in keys]
    v['premise'] = {'reason': reasons[0], 'sources': sources}
    v['challenge'] = {'reviewer': 'Codex', 'at': review['at'], 'premiseChecked': True, 'alternativesExcluded': True, 'notes': SPECIAL.get(qid, 'Tried each alternative against the literal final scope: ' + ' '.join(f'{item["question"]["answers"][i]}: {reasons[i]}' for i in range(1,4)))}
    for i, opt in enumerate(v['options']):
        opt['reason'] = reasons[i]
        opt['basis'] = 'direct' if i == 0 else 'exclusive-inference'
        opt['sources'] = sources
    # These exclusions use explicit distinct attribution/roles rather than identity inference.
    for i in range(1,4):
        if qid in {119,120,135,148,151}:
            v['options'][i]['basis'] = 'contradiction'
    if qid in {154,155}:
        for i in range(1,4):
            v['options'][i]['basis'] = 'contradiction'
    (OUT / f'{qid}.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

assert set(D) == {x['question']['id'] for x in packet['questions']}
print(f'Saved {len(D)} final-wording schema-2 reviews to {OUT}')
