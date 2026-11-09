"""Explicit evidence notes from Codex's batch 31 source and option review.

Does not edit question shards or infer evidence from URLs/check results.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = '2026-11-08'
library_path = ROOT / 'audit/source-notes.json'
library = json.loads(library_path.read_text(encoding='utf-8'))
sources = library['sources']

def source(key, url, locator, evidence, limitation='Institutional text inspected; no original film, audio or video playback claimed.'):
    key = 'b31-' + key
    sources[key] = dict(url=url, locator=locator, evidence=evidence, checkedBy='Codex', checkedAt=DATE,
                        timeSensitive=False, nextReviewAt=None, limitations=limitation, topics=['Batch 31'])
    return key

SECONDARY = 'Secondary text account inspected, not original film playback. Specific passage is paired with the independently identified corroboration in the review; no studio-certified screenplay is claimed.'
source('alice-transform','https://en.wikipedia.org/wiki/Caterpillar_(Alice%27s_Adventures_in_Wonderland)',
       'In other media > Disney film, paragraph ending with Richard Haydn credit',
       'The 1951 Caterpillar becomes a butterfly in Alice\'s presence.', SECONDARY)
source('alice-scene','https://thedisneypurist.com/2023/09/29/13-alice-in-wonderland-1951/',
       'Plot: three-inch height disagreement, lines 38-39',
       'The offended Caterpillar becomes a butterfly and then explains the mushroom.', SECONDARY)
source('alice-tale','https://d23.com/a-to-z/alice-in-wonderland-film/',
       'Opening synopsis, lines 89-90',
       'Tweedledum and Tweedledee tell The Walrus and the Carpenter; the tea party and Queen confrontation are separate encounters.')
source('aristo-band','https://en.wikipedia.org/wiki/The_Aristocats',
       'Voice cast: Scat Cat through Billy Boss, lines 280-284',
       'Scat Cat plays trumpet; Shun Gon piano and pot drums; Hit Cat acoustic guitar; Peppo concertina; Billy Boss double bass.', SECONDARY)
source('hit-cat','https://whatthemovie.com/movie/the_aristocats/character/144933-hit-cat',
       'Hit Cat character description, lines 31-35',
       'Hit Cat is the English band member and plays acoustic guitar.',
       'Secondary character listing corroborates the complete band-role listing; primary detailed instrument documentation was not located.')
source('band-corroboration','https://www.fakebands.com/wiki/index.php?title=The_Alley_Cats_(Aristocats)',
       'Members table, lines 16-23',
       'The table independently lists Scat Cat as trumpet, Shun Gon piano/drums, Billy Boss double bass, Peppo concertina and Hit Cat guitar.',
       'Secondary specialist fictional-band catalog, compared with Wikipedia and the Hit Cat character listing. Primary detailed instrument documentation was sought but not accessible; no original playback claimed.')
source('frozen-scenes','https://www.springfieldspringfield.co.uk/movie_script.php?movie=frozen-2013',
       'Coronation 230-307; Anna/Hans duet 448-518; Kristoff/Sven 805-832; Olaf 1075-1126; trolls 1627-1714; childhood door song near opening',
       'Kristoff supplies Sven\'s replies in his solo. Olaf imagines a warm beach. Trolls try pairing Anna and Kristoff despite her engagement. Other numbers belong to Anna\'s childhood door appeal, coronation anticipation, and the Anna/Hans courtship.',
       'Third-party dialogue transcription inspected and compared with the existing film-song notes, including b29-frozen-music. No lyrics reproduced in these notes and no original playback claimed.')
source('frozen-album','https://christophebeck.com/projects/frozen/',
       'Frozen soundtrack > Disc 1 tracks 2-9, lines 43-50',
       'The film composer\'s album listing credits the Kristoff solo to Jonathan Groff, the Olaf solo to Josh Gad, Fixer Upper to cast and Maia Wilson, and the Anna/Hans duet to Kristen Bell and Santino Fontana.',
       'Primary soundtrack-credit listing from the film composer; used to corroborate song titles/performers, with scene context established by the separately inspected transcription. No audio playback claimed.')
source('fever','https://d23.com/catching-frozen-fever/',
       'Filmmaker interview: Anna birthday and Snowgies paragraph, line 75',
       'Elsa has a cold while organizing Anna\'s birthday; her sneezes produce tiny snowmen called Snowgies. Kristoff, Sven and Olaf help with Anna\'s celebration.')
source('geri','https://www.pixar.com/geris-game', 'Synopsis, line 59',
       'Geri plays himself at chess in a park.')
source('bao','https://www.pixar.com/bao', 'Synopsis, line 62',
       'A mother gets another chance at motherhood when a dumpling comes to life as a boy.')
source('opening','https://en.wikipedia.org/wiki/Disneyland', 'Opening day: crowd and ride problems, lines 265-266',
       'July 17, 1955 is the commemorated opening; crowd problems included an overloaded Mark Twain. The day became known as Black Sunday.', SECONDARY)
source('opening-corroboration','https://www.wired.com/2010/09/disneyland/',
       'Opening historical introduction, lines 56-64', 'Disneyland\'s 1955 opening was called Black Sunday by insiders.',
       'Journalistic historical introduction read; used for nickname only, not as evidence of any sinking or mechanical failure.')
source('riverboat','https://www.disneyhistory101.com/new-index-32',
       'Opening-day Mark Twain account, lines 1317-1321',
       'An opening-day crowd boarded without a set limit; the deck approached the waterline. Account includes Nunis\'s recollection of overloading and Koenig\'s capacity description.',
       'Historical compilation reproduces attributed recollections; corroborated by the separate Disneyland opening account. Wording reduced to low riding, not a literal sinking or claimed exact capacity.')
source('gas','https://www.dix-project.net/index.php/document/smithsonian-studies-in-american-art_1991-08-22_disneyland-1955',
       'Karal Ann Marling, Smithsonian Studies in American Art, opening-day paragraph, line 48',
       'A gas leak temporarily shut Fantasyland on opening day; OCR misspells the land name in the reproduced text.',
       'Scholarly historical article reproduced by an archive. Does not establish an evacuation count; that extra claim was removed.')
source('spaceship','https://d23.com/a-to-z/spaceship-earth/', 'Opening history and 1994 concepts paragraphs, lines 88-89',
       'Disney identifies AT&T as the 1982 sponsor and Ray Bradbury as a source of attraction concepts; Siemens sponsorship began in 2005.')
source('spaceship-history','https://en.wikipedia.org/wiki/Spaceship_Earth_(Epcot)',
       'Sponsor list 168-171; Design and construction 197-202; Timeline 313-314',
       'Bradbury helped the original storyline. Bell System was the initial sponsor; AT&T took the sponsor name after its 1984 breakup. The AT&T president dedicated the 1982 attraction.',
       'Secondary history compared with Disney\'s entry. Both Bell System and AT&T names belong to the opening sponsor lineage, so they are combined into a single option.')
source('district','https://www.oversightdistrict.org/history/the-reedy-creek-improvement-district/',
       'RCID Created, line 80', 'The May 12, 1967 legislation created the Reedy Creek Improvement District and two municipalities.')
source('district-functions','https://www.oversightdistrict.org/about_cftod/',
       'About the District: 1967 creation and county authority',
       'The 1967 district was called Reedy Creek Improvement District and was given county-like governmental responsibilities.')
source('strike','https://animationguild.org/about-the-guild/disney-strike-1941/',
       'Babbitt firing and strike opening, lines 20-25',
       'Guild history links Babbitt\'s firing to the strike beginning May 29, 1941.',
       'Union institutional history; only year and firing trigger used. Its duration differs from other histories and is not adopted.')
source('strike-corroboration','https://www.pbs.org/wgbh/americanexperience/features/walt-disneys-empire/',
       'May 1941 strike photograph description, lines 82-86',
       'Animators struck in May 1941 for wages, overtime and credit practices. Ward Kimball continued working.',
       'Public broadcaster historical exhibit corroborates year and working-condition context.')
source('babbitt-letters','https://babbittblog.com/2016/05/27/letters-of-termination/',
       'Introductory account of the May 27, 1941 termination letters',
       'Babbitt\'s archive describes his dismissal and reproduces two termination letters.',
       'Archival introductory text inspected; no independent transcription of the scanned letter images is claimed.')
source('dca','https://disneyexperiences.com/disneyland-press/fact/disney-california-adventure-park-fact-sheet-2/',
       'Opening paragraph, line 10', 'Disney California Adventure opened February 8, 2001.')
source('rose','https://disneycruise.disney.go.com/en-ca/onboard-activities/rose-lounge/',
       'Title, Ship Locations, introduction and Step Into a Fairy Tale, lines 0-21',
       'The Rose is on Disney Wish at the entrance to Palo Steakhouse and Enchanté, themed to Beauty and the Beast.')
sources['b31-rose']['timeSensitive']=True
sources['b31-rose']['nextReviewAt']='2027-02-05'
sources.pop('b31-wish-guide', None)
source('wish-goodnight','https://disneyparksblog.com/dcl/live-shows-on-the-disney-wish/',
       'May 30, 2025 article > Say Goodnight Together in the Grand Hall, lines 89-92',
       'The described goodnight show uses the Cinderella song So This Is Love with the twinkling chandelier. Question now states 2025 rather than promising a current nightly schedule.')
source('jungle2','https://d23.com/a-to-z/jungle-book-2-the-film/',
       'Opening synopsis and cast, lines 89-91',
       'Shanti is the girl who drew Mowgli out of the jungle; Ranjan is his little stepbrother. Shere Khan seeks revenge. Kaa and Baloo are separately named characters.')
source('jungle2-official','https://movies.disney.com/the-jungle-book-2',
       'Synopsis', 'Ranjan is Mowgli\'s little stepbrother, Shanti his friend, and Shere Khan the tiger planning revenge.')
source('tarzan2','https://d23.com/a-to-z/tarzan-ii-film/',
       'Synopsis and cast, lines 87-89',
       'Young Tarzan feels unlike the apes. The feared Zugor is an old hermit ape; Kerchak and Kala are separate members of Tarzan\'s family.')
source('tarzan2-detail','https://en.wikipedia.org/wiki/Tarzan_II',
       'Plot, lines 196-199', 'Tarzan cannot run as fast as the young gorillas. Zugor amplifies his voice with hollow trees; Sabor is a leopard.', SECONDARY)
source('tarzan2-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=tarzan-ii',
       'Opening imitation of Kerchak, lines 93-107; Zugor discovery, lines 396-408',
       'Opening dialogue describes Tarzan\'s difficulty running and climbing. Tarzan identifies the ape as Zugor after seeing him frighten another animal.', SECONDARY)
source('fantasia','https://en.wikipedia.org/wiki/Fantasia_(1940_film)',
       'Program > Night on Bald Mountain/Ave Maria, lines 286-287',
       'The spirits are driven back by an Angelus bell at dawn, followed by the Ave Maria procession.', SECONDARY)
source('fantasia-corroboration','https://mouseplanet.com/the-fantasia-mountains/4606/',
       'Jim Korkis, Bald Mountain description, lines 24-28 and image caption 43',
       'Church bells and the dawn choir end the evil revelry.',
       'Specialist Disney historian\'s scene discussion corroborates the separate program synopsis, not original playback.')
source('kronk','https://en.wikipedia.org/wiki/Kronk%27s_New_Groove',
       'Plot, lines 181-185',
       'Kronk\'s father wants a wife and large home for him; friends pose as wife and children when he arrives. Kronk already works as a chef. Yzma\'s youth-potion scheme is a preceding flashback.', SECONDARY)
source('kronk-official','https://d23.com/a-to-z/kronks-new-groove-film/',
       'Synopsis, line 89', 'Kronk is already a head chef; his father\'s visit makes him plot to appear successful.')
source('bambi2','https://en.wikipedia.org/wiki/Bambi_II',
       'Plot 221-229 and voice cast 230-241',
       'Ronno is the rival fawn who tries to impress Faline. Flower is Bambi\'s friend, Friend Owl helps his father find a doe. Bambi and his father develop their relationship after his mother dies.', SECONDARY)
source('bambi2-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=bambi-ii',
       'Groundhog introduction 240-288 and Ronno/Faline confrontation 503-525',
       'Ronno names himself, challenges Bambi and later orders Faline to go with him; she objects and Bambi intervenes.', SECONDARY)
source('bambi2-official','https://d23.com/a-to-z/bambi-ii-film/',
       'Synopsis, line 87', 'The bereaved Bambi and his father the Great Prince learn to become a family.')
source('hk','https://thewaltdisneycompany.com/press-releases/hong-kong-welcomes-a-new-era-of-family-entertainment-with-grand-opening-of-hong-kong-disneyland-resort/',
       'September 12, 2005 date and grand opening lead, lines 60-64', 'Hong Kong Disneyland held its grand opening September 12, 2005.')
source('snow-cost','https://catalog.afi.com/Film/5865-SNOW-WHITEANDTHESEVENDWARFS',
       'History, contemporary negative-cost estimate, line 84',
       'Contemporary sources estimated production cost at $1,488,423; AFI distinguishes it from the much lower original budget.')
source('snow-cost-corroboration','https://en.wikipedia.org/wiki/Snow_White_and_the_Seven_Dwarfs_(film)',
       'Infobox budget and introductory production-cost account, lines 287-292', 'The production cost is rounded to $1.5 million.', SECONDARY)
source('cars3','https://en.wikipedia.org/wiki/Cars_3',
       'Plot, Florida 500 final lap, lines 224-226', 'After Storm pushes Cruz against the wall, she flips over him and wins.', SECONDARY)
source('cars3-corroboration','https://geekytalksite.wordpress.com/2017/06/22/disney-pixars-cars-3-surprisingly-mature-story/',
       'Plot discussion, lines 49-50', 'Contemporary review describes Storm pinning Cruz and her flipping over him.',
       'Contemporary secondary scene account corroborates the plot synopsis; Pixar\'s generic page did not describe the final pass.')
source('mu','https://www.pixar.com/monsters-university',
       'Randy Boggs 102-104; Dean Hardscrabble 114-116; Roar Omega Roar 210-212',
       'Johnny Worthington is ROR president. Randy is a freshman scaring student, Hardscrabble the dean. Sulley\'s profile describes him as a student.')
source('mu-room','https://www.springfieldspringfield.co.uk/movie_script.php?movie=monsters-university',
       'Room 319 assignment and Randy introduction, lines 247-265',
       'Mike is assigned a room; Randy introduces himself as Mike\'s roommate and fellow scaring major.', SECONDARY)
source('mu-roles','https://en.wikipedia.org/wiki/Monsters_University',
       'Plot 235; Voice cast 257-262',
       'Randall is Mike\'s assigned roommate; Johnny J. Worthington III is ROR president, distinct from the dean and other students.', SECONDARY)
source('fox2','https://en.wikipedia.org/wiki/The_Fox_and_the_Hound_2',
       'Plot, lines 202-206',
       'Copper joins Cash\'s Singin\' Strays at the fair after Tod falsely calls him a stray. The expected talent scout represents the Grand Ole Opry.', SECONDARY)
source('fox2-official','https://d23.com/a-to-z/fox-and-the-hound-2-the-film/',
       'Synopsis: novelty dog act and Cash\'s ambition',
       'Copper joins the singing dog act led by Cash, whose ambition is the Grand Ole Opry. Dixie tries to regain her place.')
source('poppins','https://www.springfieldspringfield.co.uk/movie_script.php?movie=mary-poppins',
       'Uncle Albert visit: floating-laughter dialogue 1251-1283; tea service 1376-1409',
       'Albert\'s laughter causes floating. Mary pours tea with Bert, Jane and Michael present; she scolds their laughter rather than laughing herself into the air.', SECONDARY)
source('poppins-corroboration','https://en.wikipedia.org/wiki/Mary_Poppins_(film)',
       'Plot, line 239; Uncle Albert cast description, line 263',
       'Mary, the children and Bert visit Albert, whose uncontrollable laughter causes him to float.', SECONDARY)
source('bed','https://d23.com/a-to-z/bedknobs-and-broomsticks-film/',
       'Synopsis and cast, lines 89-92',
       'Eglantine Price, played by Angela Lansbury, shelters three London children and seeks magic to help England defeat Germany; travel is enabled by a bedknob.')
source('bed-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=bedknobs-and-broomsticks',
       'War effort 350-361; traveling gift 424-445; missing final lesson 451-485',
       'Price says her work supports the war effort. She enchants Paul\'s knob: turning it and naming the destination moves the bed. Paul alone can operate the spell.', SECONDARY)
source('nemo','https://d23.com/a-to-z/20000-leagues-under-the-sea-film/',
       'Synopsis and cast, lines 89-94', 'Nemo commands the Nautilus in the 1954 film; his island and inventions are ultimately destroyed.')
source('nemo-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=20000-leagues-under-the-sea',
       'Vulcania approach, boarding parties and destruction order 1563-1636; final explosion warning 1659-1663',
       'With hostile boarding parties approaching, Nemo orders destruction before they reach his lagoon. His knowledge is the prize at stake.', SECONDARY)
source('nemo-plot','https://en.wikipedia.org/wiki/20,000_Leagues_Under_the_Sea_(1954_film)',
       'Plot, line 201', 'Nemo sets a time bomb to destroy evidence of his discoveries on Vulcania.', SECONDARY)
source('swiss','https://en.wikipedia.org/wiki/Swiss_Family_Robinson_(1960_film)',
       'Plot opening, lines 177-178', 'The abandoned ship grounds on rocks off an island; the family salvages it and goes ashore.', SECONDARY)
source('swiss-official','https://d23.com/a-to-z/swiss-family-robinson-film/',
       'Opening synopsis, lines 87-88', 'A shipwreck strands the family, who salvage supplies and build an island home.')

template = json.loads((ROOT/'audit/runs/next-shard-0031-final-template-v2.json').read_text(encoding='utf-8'))
reviews = {r['questionId']:r for r in template['reviews']}
CHECKS = ['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']

def review(qid, keys, premise, reasons, challenge, distinct, context, bases=None):
    r = reviews[qid]
    ids = [s if s.startswith('b30-') or s.startswith('b29-') else 'b31-'+s for s in keys]
    assert len(reasons)==4
    r.update(checks=CHECKS, notes=distinct, context=context, timeSensitive=False, nextReviewAt=None)
    r['premise'] = dict(reason=premise, sources=ids)
    r['options'] = [dict(basis=b, reason=reason, sources=ids) for b,reason in zip(bases or ['direct']+['exclusive-inference']*3,reasons)]
    r['challenge'] = dict(reviewer='Codex',at=DATE,premiseChecked=True,alternativesExcluded=True,notes=challenge)

review(2068,['b30-aladdin'], 'The question asks a stated rule, not every conceivable limit on Genie.',
 ['Resurrection is one of his three stated prohibitions.','Immortality is not in that three-rule list.','A ban on healing any injury is not in that list.','A ban on backward aging is not in that list.'],
 'Read the complete rule list separately: killing, forced love and resurrection. Changed cannot to will not because his resurrection wording is a refusal; no unsupported claim about immortality is needed.',
 'Different rule from #2067, which tests forced love. No new TV or sequel scope.', 'Aladdin, original 1992 film; initial lamp explanation.', ['direct','exhaustive-list','exhaustive-list','exhaustive-list'])
review(2069,['alice-transform','alice-scene'], 'The 1951 film actually shows this transformation during the mushroom encounter.',
 ['Both accounts identify a butterfly.','The described new insect is a butterfly, not a moth.','The same transformation is not into a dragonfly.','It is not a ladybug transformation.'],
 'Compared moth versus butterfly explicitly; the evidence names butterfly. Specified 1951 to avoid adaptation confusion.',
 'Distinct from #1057, which asks where the Caterpillar sits.', 'Alice in Wonderland, 1951 animated film; mushroom conversation.')
review(2070,['alice-tale'], 'Disney identifies the tale told by the twins in the animated film.',
 ['Disney names this exact tale.','The twins\' named tale is not The Lobster Quadrille.','The named tale is not the Mock Turtle story.','The Queen encounter is separate from the twins\' tale.'],
 'Book material is not substituted for the film: the twin narration has one named title. Oysters supply scene context, not an answer title repeated in the stem.',
 'No other question asks which tale the twins narrate.', 'Alice in Wonderland, 1951 animated film; Tweedledee/Tweedledum encounter.')
review(2071,['aristo-band','hit-cat','band-corroboration'], 'The question identifies Hit Cat\'s instrument in Scat Cat\'s band.',
 ['Hit Cat is explicitly the acoustic guitarist.','The trumpet belongs to Scat Cat\'s band role.','Billy Boss is the double-bass player.','Peppo plays the concertina.'],
 'Checked every band member assignment, rather than inferring absence from a plot summary. This asks the band instrument, not whether Hit Cat could ever learn another instrument.',
 'Distinct from #2072 trumpet assignment, #1110 band leader, and #1250 song title.', 'The Aristocats (1970); alley-cat band instrument roles.', ['direct','contradiction','contradiction','contradiction'])
review(2072,['aristo-band','band-corroboration'], 'Scat Cat is the band leader and its named trumpet player.',
 ['The band-role list assigns him trumpet.','Shun Gon has the band\'s piano role.','Billy Boss has the double-bass role.','Shun Gon has the pot-drums role.'],
 'The instrument list expressly distinguishes piano/drums, bass and trumpet. No claim about every instrument Scat Cat is capable of playing is necessary.',
 'His instrument adds a fact beyond the leader identity in #1110; #2071 asks another member\'s instrument.', 'The Aristocats (1970), named band roles.', ['direct','contradiction','contradiction','contradiction'])
review(2073,['frozen-scenes','frozen-album','b29-frozen-music'], 'The trolls\' matchmaking number occurs despite Anna\'s engagement.',
 ['The troll sequence is Fixer Upper.','That is Kristoff\'s earlier Sven-voice solo.','That is Olaf\'s beach fantasy.','That is Anna and Hans\'s courtship duet.'],
 'Checked the competing song scenes, including the engagement interruption during the trolls\' number. Different songs are not inferred solely from one correct title.',
 'Distinct song performance from #2074/#2075 and the other Frozen music questions.', 'Frozen (2013), trolls\' attempted matchmaking.', ['direct','contradiction','contradiction','contradiction'])
review(2074,['frozen-scenes','frozen-album'], 'Olaf sings while imagining a warm beach without understanding melting.',
 ['Olaf\'s warm-weather fantasy uses this song.','That is the later trolls\' number.','That is Anna\'s childhood appeal at Elsa\'s door.','That is coronation anticipation and a palace reprise.'],
 'Removed summer from the stem to stop repeating the title. Compared the door, coronation and troll sequences against Olaf\'s specific fantasy.',
 'No equivalent Olaf-solo question elsewhere in the complete Frozen digest.', 'Frozen (2013); Olaf\'s beach fantasy.', ['direct','contradiction','contradiction','contradiction'])
review(2075,['frozen-scenes','frozen-album','b29-frozen-music'], 'Kristoff performs a solo with imitated replies from Sven after the shop encounter.',
 ['The short Kristoff/Sven solo has this title.','In Summer is Olaf\'s performance.','Fixer Upper is the trolls\' performance.','Love Is an Open Door is Anna and Hans\'s duet.'],
 'Removed unsupported duration and title-paraphrase clues. Kristoff supplies both voices: Sven does not literally sing. The later Frozen 2 rock ballad is a separate scene.',
 'Distinct from #1601 Lost in the Woods and the other two batch song scenes; difficulty set to medium.', 'Frozen (2013); nighttime scene after Oaken\'s shop.', ['direct','contradiction','contradiction','contradiction'])
review(2076,['fever'], 'Elsa\'s illness makes her create Snowgies while preparing Anna\'s birthday.',
 ['The filmmaker describes tiny snowmen called Snowgies.','The sneeze creations are snowmen, not castles.','The described creatures are not mere confetti-like bursts.','The recurring sneeze creations are not flower bouquets.'],
 'A sneeze later produces a giant snowball, so changed each sneeze to repeatedly. The final question asks the recurring party complication, not an exhaustive inventory of every sneeze effect. The correct tiny creatures are explicitly identified.',
 'Distinct from the birthday recipient #2077 and party-guard #2204. The short\'s coverage remains a small secondary-title group.', 'Frozen Fever (2015), recurring sneezes during party preparations.')
review(2077,['fever'], 'The celebration is explicitly Anna\'s birthday.',
 ['Anna is the birthday recipient.','Kristoff helps organize it, rather than being the birthday recipient.','Olaf helps with the party, rather than receiving it.','Sven helps, rather than being the birthday recipient.'],
 'Distinguished birthday recipient from the named helpers and Elsa, who is organizing. One named recipient excludes the other three.',
 'Recipient is a separate fact from Snowgies, party guard and theatrical pairing.', 'Frozen Fever (2015), Anna\'s party.')
review(2078,['geri'], 'Pixar identifies the park game against himself.',
 ['Pixar names chess.','Chess and checkers are different games; Pixar names chess.','Pixar\'s identified game is not dominoes.','The named game is not cards.'],
 'Compared checkers rather than relying on generic board-game wording; Pixar explicitly calls it chess.',
 'Different fact from prize #2208, trick #2324 and human-character production claim #2326.', 'Geri\'s Game (1997); park match.')
review(2080,['bao'], 'Pixar identifies the food that becomes the mother\'s new child.',
 ['The living child begins as a dumpling.','The living food-child is not an appliance.','It is not a lantern.','It is not a bracelet.'],
 'Checked object identity, not the mother\'s dream versus reality interpretation. Removed unnecessary award and nationality claims and the answer\'s parenthetical title repetition.',
 'Distinct from #2210 ending action, #2211 city and #2460 director. Basic visual identity is easy.', 'Bao (2018), living dumpling premise.')
review(2081,['opening','opening-corroboration'], 'The nickname is attached to the July 17, 1955 chaotic preview/opening.',
 ['Both histories identify Black Sunday.','This is a descriptive phrase, not the nickname they identify.','Neither account names The Great Meltdown as that nickname.','Neither account identifies Chaos Day as that nickname.'],
 'Nickname evidence is explicit; the other labels are not competing documented aliases in these accounts. Kept the date separate from public admission on July 18.',
 'Different from #683 ceremony date and #109 admission price.', 'Disneyland\'s commemorated July 17, 1955 opening.')
review(2082,['riverboat','opening'], 'The overloaded opening-day riverboat rode low; literal sinking wording was removed.',
 ['Accounts identify excessive passenger loading.','The low-riding problem is attributed to passenger loading, not a boiler fault.','The described loading incident is not a dock collision.','The account explains low freeboard by crowds, not a construction leak.'],
 'No claim that the guided boat literally sank or had a known numerical capacity. Compared the specific overloading account against all three mechanical explanations.',
 'Different fact from #925 riverboat identity and opening nickname #2081.', 'Mark Twain, Disneyland, July 17, 1955; historical loading account.')
review(2083,['gas','opening'], 'The historical article identifies the cause of Fantasyland\'s temporary closure.',
 ['The specified utility emergency is a gas leak.','It is not attributed to an electricity outage.','It is not attributed to a water-main break.','It is not attributed to an electrical fire.'],
 'Removed the unsupported claim about several evacuated lands. The evidence names the utility fault; the other opening-day mishaps do not change it.',
 'Separate opening-day utility incident from the boat-loading and nickname facts.', 'Fantasyland, Disneyland, opening day in 1955.')
review(2084,['spaceship','spaceship-history'], 'Bradbury helped develop the attraction\'s original storyline.',
 ['The histories identify Ray Bradbury.','The original-story contribution is attributed to Bradbury, not Asimov.','The identified contributor is Bradbury, not Sagan.','The identified contributor is Bradbury, not Spielberg.'],
 'Question now asks the documented storyline contribution rather than implying he alone designed or scripted the entire attraction. All names are presented in parallel.',
 'Different fact from sponsor #2085 and narrator #2221.', 'Spaceship Earth original development, opened 1982.')
review(2085,['spaceship','spaceship-history'], 'Both Bell System and AT&T are names used for the opening sponsor lineage.',
 ['Combines the Bell System opening brand and AT&T parent identity.','General Electric is not the original sponsor in the sponsor histories.','Siemens belongs to the much later 2005 sponsorship.','RCA is not the original sponsor in those histories.'],
 'Original AT&T distractor could also be defended; combined it with Bell System. Siemens is excluded chronologically, not just by failing to appear in a short synopsis.',
 'Sponsor identity differs from author and narrator facts.', 'Spaceship Earth, EPCOT opening in 1982.', ['direct','exhaustive-list','contradiction','exhaustive-list'])
review(2086,['district','district-functions'], 'The historical district name and 1967 governmental role are documented by its successor.',
 ['The legislation created RCID.','This is not the district\'s enacted name.','This is not the district\'s enacted name.','This is not the district\'s enacted name.'],
 'Historical wording avoids claiming Disney retains the same current governing powers. The law\'s specific district identity excludes the three invented titles.',
 'Different from EPCOT city vision #392 and Florida Project announcement #695.', 'Florida special district establishment in 1967, not current governance.')
review(2087,['strike','strike-corroboration'], 'Guild and PBS histories put the labor dispute in 1941.',
 ['Both sources identify 1941.','1937 precedes the documented strike.','1955 is later than the documented strike.','1966 is later than the documented strike.'],
 'Sources disagree on duration, which is not asked. Year is independently corroborated; no conflicting chronology among the four years.',
 '#2262 asks a production-film association; that different fact is not the strike year itself.', 'Walt Disney studio labor strike, 1941.')
review(2088,['strike','babbitt-letters','strike-corroboration'], 'The Guild links Babbitt\'s dismissal to the strike\'s onset.',
 ['Babbitt is the dismissed union advocate in the source.','The stated trigger is Babbitt\'s dismissal, not Iwerks\'s.','Kimball continued working, rather than being this dismissed organizer.','The identified dismissed organizer is Babbitt, not Thomas.'],
 'Checked the causal dismissal rather than conflating an animator\'s later departure with the strike trigger. Avoided an exact dismissal day because accounts differ.',
 'The trigger identity adds a different fact from the date and production-film questions.', 'Disney strike trigger in 1941.')
review(2089,['dca'], 'The park\'s official fact sheet supplies its opening date.',
 ['The official date is February 8, 2001.','July 17 is a different day and month.','October 1 is a different day and month.','May 5 is a different day and month.'],
 'This is the park\'s opening, not Disneyland\'s anniversary or a reimagining. All four options use the same date form.',
 'Distinct from #622 park identity and #2122 Soarin\' original title.', 'Disney California Adventure, original opening.')
review(2090,['rose'], 'The named Wish lounge is located beside the two adult restaurants.',
 ['The live page names The Rose at those restaurants.','The Bayou is another named Wish lounge, not this named location/theme.','Nightingale\'s is another Wish lounge, not this named location/theme.','Keg & Compass is another Wish lounge, not this named location/theme.'],
 'Removed the word rose from the stem and used real onboard lounge names. Both location and film theme are needed; the official page establishes one venue.',
 'Distinct from #1231/#1232/#970, which test other lounges.', 'Disney Wish lounge location/theme as of November 2026.')
reviews[2090]['timeSensitive']=True
reviews[2090]['nextReviewAt']='2027-02-05'
review(2091,['wish-goodnight'], 'Disney\'s 2025 description names the song accompanying the Grand Hall lighting.',
 ['The 2025 article names So This Is Love.','The named song is not A Whole New World.','The named song is not Once Upon a Dream.','The named song is not Beauty and the Beast.'],
 'The question is now historical to 2025, avoiding a current nightly schedule promise. Source names the exact music cue, rather than inferring from a Cinderella statue.',
 'Distinct from #1223 statue identity and other cruise musical shows.', 'Wish Grand Hall goodnight show described May 30, 2025.')
review(2092,['jungle2','jungle2-official'], 'Shanti is the named girl who originally drew Mowgli toward the village.',
 ['Disney identifies Shanti in this role.','Ranjan is Mowgli\'s younger adoptive brother.','Messua is not the named village girl in that role.','Kaa is a different jungle character, not the village girl.'],
 'Used the sequel\'s named character, not an invented name for the unnamed first-film girl. The village-girl role excludes the two boys/adults and the snake.',
 'Distinct from #1062 destination and #2093 adoptive brother.', 'The Jungle Book 2, Shanti identification and original-film continuity.')
review(2093,['jungle2','jungle2-official'], 'Disney identifies Ranjan as Mowgli\'s little step/adoptive brother.',
 ['Ranjan is the named younger brother.','Shanti is Mowgli\'s friend, not his adoptive brother.','Baloo is his bear friend, not his human adoptive brother.','Akela is not the village family\'s little boy.'],
 'Corrected the premise: the old question wrongly called him Shanti\'s brother. Both official synopses explicitly connect Ranjan to Mowgli.',
 'Different role fact from Shanti and Baloo\'s return; set medium difficulty.', 'The Jungle Book 2, Mowgli\'s village adoptive family.')
review(2094,['jungle2','jungle2-official'], 'The official sequel synopsis says Shere Khan plans revenge on Mowgli.',
 ['Shere Khan is explicitly the revenge-seeking returning tiger.','Kaa returns, but is not the synopsis\'s revenge-seeking tiger.','King Louie is not the returning revenge pursuer described here.','Buldeo is not that returning film villain.'],
 'Kaa is a returning antagonist, so simply returning would be ambiguous; the revenge-on-Mowgli clause is essential and supported.',
 '#42 tests the original tiger\'s name; this item additionally tests the sequel\'s revenge motive, not just a shared name.', 'The Jungle Book 2, main revenge pursuit.')
review(2095,['tarzan2','tarzan2-detail','tarzan2-dialogue'], 'Zugor\'s monster identity is an old ape\'s vocal deception.',
 ['Zugor is the ape behind the amplified monster calls.','Sabor is a leopard, not this ape.','Kerchak is a separate troop leader.','The revealed hermit is Zugor, not Tublat.'],
 'Removed in-disguise wording: he uses hollow-tree amplification, not a monster costume. Original 1999 Sabor and Kerchak roles do not establish the hermit reveal.',
 'Distinct from #2196 brothers and #2197 predator; film coverage remains within the secondary-title guideline.', 'Tarzan II, Dark Mountain monster reveal.')
review(2096,['tarzan2-detail','tarzan2','tarzan2-dialogue'], 'Tarzan\'s initial inability to keep up running creates his self-doubt.',
 ['The plot explicitly says he cannot run as fast as the young gorillas.','His difficulty is not inability to hear warning calls.','It is not inability to see in daylight.','He can move his arms; the stated limitation is comparative running speed.'],
 'Narrowed broad weaker to the specific sourced running comparison. The final options ask physical limitations, not unrelated personality traits.',
 'A different fact from Zugor reveal and the other Tarzan II characters.', 'Tarzan II opening childhood frustration.')
review(2097,['fantasia','fantasia-corroboration'], 'A dawn bell ends the evil gathering before the Ave Maria procession.',
 ['The Angelus/church bell drives the spirits back.','The account does not describe sunlight turning them into stone; the bell drives them back.','The finale shows a procession, not descending angels.','The bell interrupts him; it is not merely spontaneous sleep.'],
 'Distinguished simultaneous dawn from the specific bell cue; a choir is heard, but that does not make visible descending angels defensible.',
 'Distinct from Chernabog name #564 and soundtrack/other segments.', 'Fantasia (1940), transition from Bald Mountain to Ave Maria.')
review(2098,['kronk','kronk-official'], 'Kronk wants his visiting father to believe he has an impressive settled domestic life.',
 ['The plot specifies a house and family, with friends pretending to be wife and children.','He is not fabricating royal status for this visit.','He already is a chef; the domestic claim is what he fakes.','The father-visit deception is not a championship trophy.'],
 'The chef distractor could describe a real occupation but not the false claim in this visit. The source separates the domestic deception from earlier Yzma and camp flashbacks.',
 'Different from Papi name #2199, youth product #2200 and camp rivalry #2201.', 'Kronk\'s New Groove, father-visit framing story.')
review(2100,['bambi2','bambi2-dialogue'], 'Ronno is the older fawn and romantic rival.',
 ['The cast and plot identify Ronno as Faline\'s other suitor and Bambi\'s rival.','The film\'s named rival is Ronno, not Gobo.','Friend Owl is the owl helping Bambi\'s father, not a rival fawn.','Flower is Bambi\'s skunk friend, not the rival fawn.'],
 'Did not import Gobo from Salten\'s book. Compared roles and species; Ronno\'s challenges and pursuit of Faline are explicit.',
 'Distinct from original-film Faline #1055 and the father-son premise.', 'Bambi II, Ronno/Faline rivalry.')
review(2101,['bambi2-official','bambi2'], 'The bereaved fawn and his father form the film\'s central bond.',
 ['Disney\'s synopsis identifies father and son learning to become family.','His mother is dead, so this is not mother and son raising another fawn.','A planned wedding is not the documented central relationship.','Bambi and Ronno are rivals, not joint forest rulers.'],
 'All answers now describe relationships. The father-son plot excludes mother-return, wedding and joint-rule premises.',
 'Different from #2468 father voice actor and #2469 substitute-doe request.', 'Bambi II, interval following his mother\'s death.')
review(2102,['hk'], 'Disney\'s opening-day release dates the Hong Kong park to 2005.',
 ['The official opening is September 12, 2005.','2001 is not the dated opening year.','2008 is not the dated opening year.','2016 is not the dated opening year.'],
 'Original opening is distinct from later expansions and Shanghai\'s debut. The dated contemporary release fixes one year.',
 'No other question in the complete park digest asks HKDL\'s original opening year.', 'Hong Kong Disneyland original opening, 2005.')
review(2103,['snow-cost','snow-cost-corroboration'], 'AFI distinguishes final production cost from the original budget.',
 ['$1,488,423 rounds to $1.5 million.','$0.5 million is far below the cited final cost.','$3 million is roughly double the cited final cost.','$0.75 million is about half the cited final cost.'],
 'Removed the disputed precision of the initial budget and specified nominal dollars. The rounded final amount is corroborated independently.',
 'Different from #2356 financing method and #1198 production nickname.', 'Snow White and the Seven Dwarfs, 1937 final production cost.')
review(2104,['cars3','cars3-corroboration'], 'The final-lap wall pin ends with Cruz passing over Storm.',
 ['She flips over Storm.','She passes over him rather than spinning him backward.','The pass is a physical flip, not a nitro activation.','She goes over him, not under the track.'],
 'Removed the unsupported claim that she learned it from footage. Scope is the particular wall-pin escape, not every tactic used during the whole race.',
 'Separate from #1037 trainer identity and #1287 rival identity.', 'Cars 3, Florida 500 final-lap pass.')
review(2105,['mu-room','mu-roles','mu'], 'Randy/ Randall introduces himself as Mike\'s assigned college roommate.',
 ['Assignment and introduction identify him as the roommate.','They meet as students; he is not introduced as a brother.','He is a fellow scaring major, not the professor.','He is a fellow assigned resident, not the supervisor.'],
 'Limited to college arrival and removed the unneeded study-partner/rivalry generalization. Randy is the younger Randall, not a separate monster.',
 'Distinct from #192 fraternity and #1283 dean facts.', 'Monsters University, Mike\'s Room 319 arrival.')
review(2106,['mu','mu-roles'], 'Pixar explicitly identifies the ROR president.',
 ['Johnny Worthington is named president.','Randall is a student/member, not the named president.','Sulley is a student and temporary member, not president.','Hardscrabble is the dean, not a fraternity president.'],
 'Removed top-student superlative. A single named presidency excludes the other members without claiming they lack scaring skill.',
 'Different from the fraternity Mike joins and the dean identity.', 'Monsters University, Roar Omega Roar leadership.')
review(2107,['fox2','fox2-official'], 'Copper joins the named musical group led by Cash.',
 ['The group is the Singin\' Strays.','The named group is not The Barking Brigade.','The named group is not The Howling Harmonizers.','The named group is not The Mutt Chorus.'],
 'Removed singing stray dogs from the stem because it paraphrased the correct name. D23 spells the group Singing Strays, while the detailed plot records Singin\' Strays; these denote the same act.',
 'Group identity differs from cast voices, scout destination and membership lie.', 'The Fox and the Hound 2, Cash\'s county-fair act.')
review(2108,['fox2','fox2-official'], 'The anticipated scout is linked to the Grand Ole Opry.',
 ['The plot explicitly names the Grand Ole Opry scout.','The scout is not described as representing Carnegie Hall.','The named venue is not the Royal Albert Hall.','The named venue is not the Hollywood Bowl.'],
 'Changed event-versus-person options into four parallel venues. The precise affiliation, not merely a generic audition, is asked.',
 'Venue affiliation adds a fact beyond the group or voice actors.', 'The Fox and the Hound 2, county-fair talent scout.')
review(2109,['fox2','fox2-official'], 'Tod falsely presents the owned Copper as a stray so he can join.',
 ['Calling Copper a stray means claiming he has no owner.','Tod promotes Copper\'s membership; denying his singing is not the recorded claim.','The lie concerns Copper\'s ownership status, not ownership of the fair.','The recorded lie is stray status, not an injured leg.'],
 'The original why stem had what answers. Final wording asks the false claim; Copper really belongs to Amos Slade, making no owner a lie.',
 'Separate membership deception from group name and scout affiliation.', 'The Fox and the Hound 2, Cash recruits Copper after Tod\'s lie.')
review(2110,['poppins','poppins-corroboration'], 'Albert\'s laughter is the explicit trigger for floating.',
 ['Uncontrollable laughter causes his floating.','Eating cake is not the identified trigger.','A midnight clock is not the identified trigger.','Removing his hat is not the identified trigger.'],
 'Replaced speculative laughing-gas diagnosis with observable cause. Thinking sad thoughts brings people down rather than causing this ascent.',
 'Cause differs from #2111 guest group; canonical theatrical film, not later book/TV material.', 'Mary Poppins (1964), Uncle Albert visit.')
review(2111,['poppins','poppins-corroboration'], 'The tea-service dialogue identifies Mary, Bert and both Banks children.',
 ['Mary pours for Albert, Bert, Jane and Michael.','George and Winifred are not among these tea guests.','Ellen, Mrs. Brill and George are not this tea group.','The servants and Winifred do not replace Bert and the children.'],
 'Removed after laughing too hard: Mary ascends deliberately while disapproving of the laughter. Compared complete four-person groups, not overlapping only-children alternatives.',
 'Guest list is distinct from Albert\'s floating trigger.', 'Mary Poppins (1964), floating tea party.', ['direct','exhaustive-list','exhaustive-list','exhaustive-list'])
review(2112,['bed'], 'Disney identifies the apprentice witch who shelters the London children.',
 ['Eglantine Price is the named host/apprentice.','Mary Poppins is not the named witch in this film.','Agatha Fritton is not the named host.','Millicent Bloom is not the named host.'],
 'The wartime-evacuee premise belongs to the 1971 film; Disney\'s synopsis and Lansbury credit identify one character.',
 'Different from study motive #2113 and travel object #2114.', 'Bedknobs and Broomsticks (1971), evacuees arriving at Miss Price\'s home.')
review(2113,['bed','bed-dialogue'], 'She seeks useful magic for England\'s war effort through her course.',
 ['Disney identifies a spell to help England win against Nazi Germany.','Her goal is war aid, not an entertainment career.','The documented purpose is not a family curse.','The documented purpose is not a wager with a sister.'],
 'Distinguished Price\'s sincere wartime goal from Browne\'s street-performer occupation. The desired final lesson is linked to ending the war.',
 'Motivation is a separate fact from identity and object.', 'Bedknobs and Broomsticks (1971), correspondence study and missing final lesson.')
review(2114,['bed','bed-dialogue'], 'Price enchants Paul\'s bedknob with the traveling spell.',
 ['The knob operates the bed\'s travel spell.','Her broomstick is a separate attempted flying method, not Paul\'s gift.','The gift is not a carpet.','The gift is not a clock.'],
 'Removed title giveaway and unqualified anywhere/instantly claim. Paul alone operates this particular spell; broom flight does not make the broom a second correct gift.',
 'Distinct from #2113 spell\'s war purpose; 1971/Lansbury identifies film without naming the answer in the title.', 'Bedknobs and Broomsticks (1971), enchanted gift to Paul.')
review(2115,['nemo','nemo-plot'], 'The official synopsis names the submarine\'s captain.',
 ['Nemo commands Nautilus.','Flint is not the named Nautilus captain.','Amelia is not the named Nautilus captain.','Hook is not the named Nautilus captain.'],
 'Specified the 1954 Disney version. A unique named commander excludes other Disney captains without relying on what kind of vessel they could theoretically command.',
 'Distinct from #1205 source novel author and #2116 destruction motive.', '20,000 Leagues Under the Sea (1954), Nautilus commander.')
review(2116,['nemo-dialogue','nemo-plot','nemo'], 'Nemo destroys the discoveries before hostile boarding parties can obtain them.',
 ['Dialogue orders destruction before the parties reach the lagoon; plot confirms concealment of discoveries.','The triggering danger is hostile boarding parties, not diverting lava.','He destroys the base rather than building an exit channel.','The crew agrees to follow Nemo; he is not punishing a mutiny when planting the bomb.'],
 'Replaced trap-on-pursuing-ships, which could overlap the defensive explosion, with a distinct channel claim. The motive is denial of knowledge to enemies, not a naturally erupting volcano.',
 'Motive differs from Nemo identity and film production trivia.', '20,000 Leagues Under the Sea (1954), Vulcania destruction order.')
review(2117,['swiss','swiss-official'], 'The family\'s vessel grounds on rocks and becomes a salvageable wreck.',
 ['The plot explicitly describes grounding on rocks.','Pirates later approach; they do not capture the ship intact in this event.','The family goes ashore after wrecking, rather than sailing away.','The event is a wreck, not a ship sale.'],
 'Removed competing chain-of-causation answers about pirates and storm. Final wording asks the immediate physical fate at the island, not the cause of the whole voyage disruption.',
 'Distinct from #2118 defensive weapons, #2119 treehouse and park adaptations.', 'Swiss Family Robinson (1960), opening shipwreck.')

template['at']=DATE
template['sourcesChecked']=sorted({s for r in reviews.values() for s in r['premise']['sources']})
template['reviews']=list(reviews.values())
library_path.write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'audit/runs/next-shard-0031-reviewed-notes.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Authored {len(reviews)} retained-question reviews; retirement comparisons are separate.')
