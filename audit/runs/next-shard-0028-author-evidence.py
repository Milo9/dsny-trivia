"""Expand Codex's inspected batch-28 evidence; does not edit question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'audit/source-notes.json'
OUT = ROOT / 'audit/runs/next-shard-0028-reviewed-notes.json'
library = json.loads(LIB.read_text(encoding='utf-8'))
notes = json.loads(OUT.read_text(encoding='utf-8'))

def source(key, url, locator, evidence, limitation='Institutional text inspected; no film, audio or video playback claimed.'):
    library['sources']['b28-' + key] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt='2026-11-08', timeSensitive=False,
        nextReviewAt=None, topics=['Batch 28', key], limitations=limitation)

source('corona', 'https://princess.disney.com/rapunzel?intoverride=true',
       'Opening Rapunzel biography, line 49', 'Disney identifies Rapunzel as Princess of Corona.')
source('wayfinding', 'https://news.disney.com/moana-quotes',
       'Maui section, line 76, navigation explanation',
       'Maui names the navigation skill wayfinding and describes mentally knowing position and direction.')
source('death', 'https://d23.com/a-to-z/disney-walter-elias/',
       'Final biographical paragraphs, line 96', 'Walt died December 15, 1966 while planning EPCOT.')
source('roy', 'https://www.waltdisney.org/blog/roy-disney-made-walt%E2%80%99s-dream-come-true-after-walt%E2%80%99s-passing',
       'Finishing Walt Disney World, Card Walker naming account, lines 23-25',
       'Roy insisted on Walt Disney World rather than Disney World to honor Walt, despite a marketing preference for the shorter name.')
source('slogan', 'https://disneyexperiences.com/disneyland-press/fact/disneyland-park-fact-sheet-2/',
       'Dedication and Location, lines 10-14',
       'Disneyland is called The Happiest Place on Earth. The reproduced dedication does not contain that slogan.')
source('cars', 'https://www.pixar.com/cars', 'Lightning McQueen profile, line 67',
       'McQueen gets lost in the town of Radiator Springs.')
source('auto', 'https://www.pixar.com/wall-e', 'Auto profile, lines 89-91',
       'Auto is the Axiom autopilot, a steering-wheel robot following a hidden mandate.')
source('wall700', 'https://www.pixar.com/wall-e', 'Opening heading and WALL-E profile, lines 51 and 67',
       'WALL-E has been cleaning Earth for about 700 years.')
source('wallplot', 'https://en.wikipedia.org/wiki/WALL-E', 'Plot and Captain voice-cast entry, lines 268-286',
       'Evacuation was 700 years earlier. Captain B. McCrea overrides AUTO, whose directive forbids returning to Earth.',
       'Secondary plot and cast account, corroborating Pixar chronology and character roles. McCrea name is printed in the film rather than spoken; no film viewing claimed.')
source('captain', 'https://www.pixar.com/wall-e', 'Captain profile, lines 101-103',
       'The human Captain commands the Axiom and chooses a new course for humanity after the probe discovery; the profile labels him Captain without a surname.')
source('bugcast', 'https://www.pixar.com/a-bugs-life', 'Francis, Dim, Manny and Gypsy, Slim and P.T. Flea profiles, lines 117-197',
       'Francis is the male ladybug; Manny a mantis, Dim a beetle, Slim a walking stick. P.T. Flea owns the circus.')
source('butterfly', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=a-bugs-life',
       'Troupe breakup speech, lines 784-789; Heimlich departure, lines 2372-2381',
       'Heimlich explicitly dreams of being a beautiful butterfly and calls himself one when he has wings.',
       'Third-party dialogue transcription; Pixar Heimlich profile corroborates the caterpillar-to-winged transformation. No playback claimed.')
source('heimlich', 'https://www.pixar.com/a-bugs-life', 'Heimlich profile, lines 130-132',
       'Heimlich is the caterpillar whose resulting wings are small.')
source('onward', 'https://www.pixar.com/onward', 'Barley, Laurel, Officer Colt Bronco and Guinevere profiles, lines 81-143',
       'Laurel is Ian and Barley mother. Colt Bronco is her centaur police-officer partner. Barley plays Quests of Yore; Guinevere is his van.')
source('lucaparents', 'https://www.pixar.com/luca', 'Daniela Paguro and Lorenzo Paguro profiles, lines 135-149',
       'Daniela is Luca mother and Lorenzo his father; Massimo is Giulia father and Alberto Luca friend.')
source('lucastars', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=luca',
       'Giulia telescope lesson, lines 1598-1609',
       'Giulia identifies the supposed sky fish as stars and shows Saturn, discussing planets rather than marine life.',
       'Secondary dialogue transcript; specific lesson inspected, with Pixar Giulia learning profile as contextual corroboration. No playback claimed.')
source('lucaabandon', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=luca',
       'Tower reconciliation, lines 2001-2015',
       'Alberto says he marked days when his father left, stopped counting and hoped his father would change his mind.',
       'Secondary dialogue transcription; corroborated by independent plot account, b28-lucaplot. No original viewing claimed.')
source('lucaplot', 'https://en.wikipedia.org/wiki/Luca_(2021_film)',
       'Plot, tower reconciliation, line 230', 'Luca learns Alberto was abandoned by his father long ago.',
       'Secondary plot account corroborates the separately inspected abandonment dialogue.')
source('wade', 'https://www.pixar.com/elemental', 'Wade Ripple profile, lines 78-80',
       'Wade is emotionally open, empathetic and compassionate.')
source('pipes', 'https://imsdb.com/scripts/Elemental.html',
       'Printed screenplay pp.25-28, pipe burst and Wade arrival, lines 1445-1615',
       'Ember anger cracks a water pipe and floods the basement; Wade emerges through the pipe, identifies himself as inspector, and cries while writing citations.',
       'Disney/Pixar screenplay mirrored on IMSDb; copyright and scene text inspected. No playback claimed.')
source('glass', 'https://imsdb.com/scripts/Elemental.html',
       'Culvert repair before Ripple dinner, printed pp.74-75, lines 4277-4323; inspection pp.86-87, lines 4993-5022',
       'Ember melts sandbags into glass to seal culvert doors. Water then holds behind the glass; Gale later approves tempered glass.',
       'Studio screenplay on third-party mirror. Original claim that this saves the whole city in the climax was removed; glass later fails during the flood.')
source('io2', 'https://assets.debut.disney.com/documents/Inside_Out_2_Script.pdf',
       'Printed pp.1,23-28,50,95-97',
       'Riley is 13; a puberty alarm precedes renovation and new emotions. Anxiety tells Nostalgia to wait about ten years. A worker calls the sarcastic-echo gap a Sar-chasm.')
source('nostalgia-corroboration', 'https://www.ottplay.com/news/inside-out-2-pixars-finest-franchise-gets-freckles-braces/dc7ef20ae1459',
       'Review paragraph describing Nostalgia gag',
       'Contemporary review independently describes the gag as making Nostalgia wait at least ten years.',
       'Secondary review corroborates the exact numerical joke; canonical attribution and wording come from the studio screenplay.')
source('voyd', 'https://graphics.pixar.com/library/PortalsIncredibles2/paper.pdf',
       'Abstract and Introduction, Into the Voyd (DigiPro 2018)',
       'Pixar authors describe Voyd creating portals connecting two locations, through which characters and objects pass.',
       'Full indexed primary paper text inspected in search retrieval. Live open redirected to technology library; that generic page is not scene evidence. Roster corroboration is b28-i2plot.')
source('i2assets', 'https://www.pixar.com/incredibles-2',
       'Raccoon, Elasticycle and Hydroliner sections, lines 205-207,253-255,279-281',
       'Jack-Jack battles a backyard raccoon. Elastigirl motorcycle is the Elasticycle. The climax boat design is a super yacht.')
source('i2dialogue', 'https://transcripts.simpleremix.com/script.php/the-incredibles-2-2018-F8HU',
       'Opening Tony interview lines 3-115; Bob/Dicker mind-wipe call 2001-2011; Everjust announcement 2578-2582; goggles discussion 3155-3163',
       'Tony saw Violet unmasked and Dicker erased his memory. The Deavors name their signing-ceremony boat Everjust. The children identify goggles controlling the adults.',
       'Secondary dialogue transcript; corroborated by Pixar character/design text and a separate plot/cast account. No original viewing claimed.')
source('i2plot', 'https://en.wikipedia.org/wiki/Incredibles_2',
       'Plot lines 227,231-236; Voyd and He-Lectrix cast lines 255-258',
       'Tony forgets Violet. Evelyn controls Helen with goggles. The yacht is Everjust. Voyd creates portals; He-Lectrix controls electricity.',
       'Secondary scene/roster account corroborates dialogue and primary production paper. Promotional Pixar synopsis does not establish the twist.')
source('soulbody', 'https://assets.scriptslug.com/live/pdf/scripts/soul-2020.pdf?v=1729114993',
       'Academy screenplay printed pp.51-54, hospital awakening',
       'Joe sees cat paws and his human body in front of him; 22 is speaking from Joe body. They occupy separate adult-human and cat bodies.',
       'Disney/Pixar Academy screenplay on Script Slug mirror; specific passage read, no film playback.')
source('dez', 'https://assets.scriptslug.com/live/pdf/scripts/soul-2020.pdf?v=1729114993',
       'Academy screenplay printed pp.80-82, Dez conversation',
       'Dez says he wanted to be a veterinarian but chose cheaper barber school after his daughter became sick. He is happy with barbering.',
       'Studio-authored screenplay mirrored by Script Slug, corroborated with film dialogue transcript and Pixar barber profile.')
source('soulcast', 'https://www.pixar.com/soul', 'Dez profile, lines 110-112',
       'Dez is Joe longtime barber, rather than merely a customer.')
source('roz', 'https://www.pixar.com/monsters-inc', 'Roz and Celia profiles, lines 137-152',
       'Roz is dispatch manager; Celia is the receptionist.')
source('rozreveal', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=monsters-inc',
       'CDA reveal, lines 2875-2886',
       'An agent says Number One wants to speak, Roz appears, and she explains her undercover work.',
       'Secondary dialogue transcription corroborates the primary Roz profile hint of a No.1 boss. No film viewing claimed.')
source('cda', 'https://www.pixar.com/monsters-inc', 'Child Detection Agency profile, lines 202-204',
       'The CDA teams wear yellow suits and remove human goods and disinfect monsters.')
source('ratcast', 'https://www.pixar.com/ratatouille',
       'Linguini, Colette, Auguste, Skinner, Emile and Django profiles, lines 77-164',
       'Linguini secretly cooks with Remy; Colette trains him. Django is Remy father and clan patriarch; Emile his brother; Gusteau the late chef and Skinner the boss.')
source('hair', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=ratatouille',
       'Linguini argument with Remy after press attention, lines 1636-1640',
       'Linguini complains of Remy yanking his hair while he tries to concentrate.',
       'Secondary film dialogue corroborated by the specific hair-control plot description in b28-ratplot; not inferred solely from a generic homepage.')
source('ratplot', 'https://en.wikipedia.org/wiki/Ratatouille_(film)',
       'Plot, formation of the secret cooking partnership',
       'Remy controls Linguini movements by pulling his hair from beneath his toque.',
       'Secondary plot account; corroborates independently hosted dialogue referring to hair-yanking. No playback claimed.')
source('frozencharacters', 'https://d23.com/meet-the-enchanting-new-characters-of-frozen-2/',
       'Bruni and Gale sections, lines 85-105',
       'Bruni is the salamander drawn to Elsa snowflakes; Gale is the wind spirit.')
source('brunifire', 'https://news.disney.com/how-to-draw-bruni-frozen-2',
       'Opening description of animation supervisor Trent Correy lesson',
       'Disney identifies Bruni as the fire spirit from Frozen 2.')
source('frozendialogue', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=frozen-ii',
       'Runeard memory 1169-1179; Olaf farewell 1202-1227; fifth-spirit reveal 1335-1342; Queen Anna introduction 1379-1387',
       'Runeard intended the dam to weaken Northuldra land. Elsa is called fifth spirit; Anna is introduced as Queen. Olaf says his magic is fading and he is flurrying away.',
       'Secondary transcription with spelling/grammar errors. Used only where meaning is clear and corroborated by b28-frozenplot and b28-olafvisual; no original viewing claimed.')
source('frozenplot', 'https://en.wikipedia.org/wiki/Frozen_2', 'Plot, lines 248-251 and cast lines 258-266',
       'Runeard used the dam against the Northuldra. Elsa freezes, Olaf fades away, then returns. Elsa is fifth spirit and Anna becomes queen.',
       'Secondary plot/cast account corroborates separately inspected dialogue; no film playback or primary screenplay access claimed.')
source('olafvisual', 'https://www.looper.com/879290/questions-from-the-frozen-movies-we-still-need-answers-to/',
       'Do any other connections exist between Elsa and Olaf? section, line 140',
       'Olaf snowman form disintegrates into snowflakes after Elsa freezes.',
       'Secondary visual-scene description corroborates farewell dialogue and separate plot account. No original viewing claimed.')
source('wish', 'https://thewaltdisneycompany.com/news/walt-disney-animation-studios-debuts-wish-trailer/',
       'Opening trailer introduction and Chris Buck kingdom quotation, lines 65-67',
       'Asha wish calls Star from the sky. Magnifico rules Rosas, the kingdom of wishes.')
source('dallben', 'https://d23.com/a-to-z/dallben/', 'Complete character entry, line 87',
       'Dallben is the wizard and Taran mentor in The Black Cauldron.')
source('witches', 'https://d23.com/a-to-z/orddu-orgoch-and-orwen/', 'Complete character entry, line 88',
       'Orddu, Orgoch and Orwen are the Witches of Morva in The Black Cauldron.')
source('friar', 'https://d23.com/a-to-z/friar-tuck/', 'Complete character entry, line 89',
       'Friar Tuck is the badger holy man in Disney Robin Hood.')
source('cornelius', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=meet-the-robinsons',
       'Family-tree recap lines 887-905; Bowler Hat Guy future history 1516-1549; adoption naming after 1834',
       'Cornelius is Wilbur father and Lewis grown-up inventor identity. Bud, Fritz and Joe are brothers in the older generation.',
       'Secondary dialogue transcript corroborated by b28-robinsonsplot; replaces the original two synonymous correct answers.')
source('robinsonsplot', 'https://en.wikipedia.org/wiki/Meet_the_Robinsons',
       'Plot lines 238-242; cast lines 248-264',
       'Lewis adult self is Cornelius. Bud is his adoptive father, while Fritz and Joe are Bud brothers.',
       'Secondary plot and cast account, corroborated by the family-tree and adoption dialogue; no film viewing claimed.')

# Each tuple supplies a premise, four separate final-option assessments and the
# actual adversarial check, rather than inferring exclusions from answer order.
reviews = {}
def review(qid, refs, premise, reasons, challenge, distinct):
    reviews[qid] = (refs.split(), premise, reasons, challenge, distinct)

review(1538, 'corona', 'Rapunzel royal identity is explicitly tied to Corona.',
 ['Corona is her named kingdom.', 'Arendelle is a different named kingdom, not Corona.', 'DunBroch is not the kingdom named for Rapunzel.', 'Agrabah is not her named kingdom.'],
 'Removed lantern timing and parental-rule clauses; the character biography establishes the one proper kingdom name without relying on TV plot trivia.',
 'Different from #842 birthday lantern purpose and #43 Frozen kingdom.')
review(1540, 'ratcast', 'The secret ghost-cooking partnership is Linguini and Remy.',
 ['Linguini supplies the human movements for Remy cooking.', 'Colette is Linguini trainer, not the secret human partner.', 'Gusteau is already dead and appears in Remy imagination.', 'Skinner is the restaurant boss opposing the partnership.'],
 'Colette later helps in the kitchen, so checked the word secretly: this asks the established concealed partnership, not everyone who ever cooks with Remy.',
 'Different from #1027 initial job, #1278 Skinner role and #263 parentage.')
review(1541, 'wayfinding', 'Maui explicitly calls the skill he explains wayfinding.',
 ['Wayfinding is the named traditional navigation skill.', 'The lesson is not making maps.', 'The named skill does not require a magnetic compass.', 'The named lesson is not navigation by clock-based dead reckoning.'],
 'Replaced Star-reading and Sky navigation because they could describe parts of wayfinding. The question now asks Maui named skill, not every generic synonym for navigation.',
 'Different from #1018 ancestral song, #544 shapeshifting and Moana geographic questions.')
review(1544, 'death', 'Walt death is dated December 15, 1966.',
 ['1966 matches the dated death.', '1967 is a year after the recorded death.', '1968 is two years after the recorded death.', '1964 is two years before the recorded death.'],
 'Checked death year versus resort opening and posthumous film releases; only 1966 matches the dated event. Cached b17-death and b12-death also agree.',
 'Asks the year, unlike #693 illness, #688 first posthumous feature, #687 opening date.')
review(1545, 'roy', 'Roy insisted that the resort name honor Walt, despite marketing advice.',
 ['Honoring Walt explains Roy insistence in the naming account.', 'The account describes a personal naming decision, not an Oscar condition.', 'Roy insistence and its stated tribute motive are not a state-charter requirement.', 'The account concerns completion of one Florida project after Walt death, not two Florida resorts built by Walt.'],
 'Removed the invented award premise and the giveaway None answer. Checked whether a legal or award requirement could explain the stated insistence; the historical account identifies the tribute and marketing disagreement.',
 'Distinct from #1490 who completed the resort and #695 Florida Project announcement name.')
review(1546, 'slogan', 'Disney own fact sheet labels Disneyland The Happiest Place on Earth.',
 ['This is the classic Disneyland slogan printed in the location heading.', 'Most Magical is not the classic slogan the Disneyland fact sheet identifies.', 'Vacation Kingdom is not the Disneyland slogan in this record.', 'Place Where Dreams Begin is not the identified classic slogan.'],
 'Removed both original-slogan chronology and false dedication-plaque claim. Replaced the shared Where Dreams Come True campaign so another genuine Disney campaign would not fit.',
 'Different from #1380 dedication opening words and park opening-date questions.')
review(1550, 'cars', 'McQueen gets lost in Radiator Springs in the original Cars.',
 ['Radiator Springs is the named town.', 'Carburetor County is not that town name.', 'Piston Peak is not the town named in McQueen profile.', 'Ornament Valley is not the town name in the profile.'],
 'Kept the question specifically about a town: regional names do not become town aliases. Removed an unnecessary claim that community service itself transforms the town.',
 'Different from #293 Mater, #488 tire shop, #1277 motel and the Cars Land attraction names.')
review(1553, 'auto wallplot', 'AUTO is the Axiom autopilot following the hidden no-return directive.',
 ['AUTO is the named autopilot enforcing the mandate.', 'OTTO is not the autopilot name.', 'NAVI-9 is not the named Axiom autopilot.', 'PILOT PRIME is not the named Axiom autopilot.'],
 'Confirmed that the hidden order concerns remaining away from Earth, rather than confusing AUTO with captain or GO-4. Alternate spellings are not accepted character names.',
 'Different from #495 spaceship name and #1305 cleaning robot.')
review(1554, 'wall700 wallplot', 'The opening robot chronology is approximately 700 years.',
 ['700 years matches Pixar heading and evacuation chronology.', '300 is not the stated interval.', '1,000 is not the stated interval.', '50 is not the stated interval.'],
 'Removed alone: the 700-year work interval does not prove he was the sole robot for every one of those years. Pixar and the independent plot chronology agree on the approximate figure.',
 'Different from acronym #28, ship #495 and plant #1304.')
review(1555, 'captain wallplot', 'The human commander who defies AUTO is Captain McCrea.',
 ['McCrea is the recorded captain name.', 'Turnbuckle is not the identified captain.', 'Holbrook is not the identified captain.', 'Sorrenson is not the identified captain.'],
 'Checked human captain versus autopilot. Pixar verifies the role and return-home decision; the secondary cast account supplies the surname and notes it is seen on a portrait rather than spoken.',
 'Different from #1553 AUTO identity and #495 ship name.')
review(1556, 'butterfly heimlich', 'Heimlich explicitly says he wants to be a beautiful butterfly.',
 ['Butterfly is his stated dream.', 'A moth is not the creature he says he wants to become.', 'A dragonfly is not his stated dream.', 'A queen ant is not his stated dream.'],
 'This asks what he dreams, not real-world caterpillar taxonomy; the explicit statement excludes the moth distractor even though real caterpillars can become moths.',
 'Different from #1022 circus occupation and other A Bug Life character identities.')
review(1557, 'bugcast', 'Francis is specifically the male ladybug mistaken for female.',
 ['Francis is the male ladybug.', 'Manny is a mantis magician.', 'Slim is a walking stick.', 'Dim is a rhinoceros beetle.'],
 'Read each named performer role rather than excluding them by absence from a synopsis; only Francis has the ladybug identity.',
 'Different from #1558 circus proprietor and #2583 pill-bug twins.')
review(1558, 'bugcast', 'P.T. Flea is the circus proprietor.',
 ['P.T. Flea owns the troupe.', 'Ringmaster Bob is not its named proprietor.', 'Big Top Pete is not its named proprietor.', 'Colonel Buzz is not its named proprietor.'],
 'Removed flea from the stem so species no longer singles out the correct option. Checked that this asks who runs the troupe, unlike what occupation it has.',
 'Different from #1022 circus performers and #1557 Francis species.')
review(1559, 'onward', 'Laurel Lightfoot is Ian and Barley mother and Colt partner.',
 ['Laurel is the named mother.', 'Guinevere is the van, not their mother.', 'Fawn is not their mother name.', 'Willow is not their mother name.'],
 'Compared all four options and #1560: knowing the mother name does not supply Colt name. The shared relationship is context, not the tested fact.',
 'Different from #1560 boyfriend name and #2170 mother voice actor.')
review(1560, 'onward', 'Officer Colt Bronco is the centaur partner of Laurel.',
 ['Colt Bronco is explicitly named as the centaur cop.', 'Deputy Hoofington is not his name.', 'Sergeant Mane is not his name.', 'Officer Trot is not his name.'],
 'Compared the full mother question: Colt identity is a second fact, not an inverse question asking for Laurel again. Exact official proper name excludes the invented alternatives.',
 'Different from #1559 mother identity and #1561 game name.')
review(1561, 'onward', 'Pixar names Barley role-playing game Quests of Yore.',
 ['Quests of Yore is the named game.', 'Realm of Wizards is not the named game.', 'Legends of Old is not the named game.', 'Path of the Phoenix is not the named game.'],
 'Removed the extra real-clues assertion because the direct profile establishes the title without requiring that additional plot claim.',
 'Different from #558 Guinevere and #1434 visitation items.')
review(1562, 'lucastars', 'Giulia telescope lesson addresses stars and Saturn.',
 ['Astronomy studies the stars and planets being explained.', 'Marine biology does not describe this celestial lesson; fish was the mistaken interpretation.', 'History is not the subject of this telescope lesson.', 'Mathematics is related to astronomy but is not what the identified stars-and-planets explanation is about.'],
 'Removed a broad favorite-school-subject claim; asked the specific lesson subject and moved scene trivia to pixar. A topic using mathematics does not make mathematics an equally precise answer.',
 'Different from #1440 race events and #1442 Giulia father.')
review(1563, 'lucaparents', 'Daniela and Lorenzo are Luca sea-monster parents.',
 ['This pair is explicitly his mother and father.', 'Alberto is Luca friend, so Marina and Alberto cannot be the parent pair.', 'Giulia and Massimo are a daughter and her human father.', 'Ercole is the town bully, not Luca father; Sofia and Ercole is not the parent pair.'],
 'Checked both names in every pair rather than validating only Daniela; the explicit parental pair excludes all alternatives.',
 'Different from #2444 Daniela voice actor and #1293 Alberto surname.')
review(1564, 'lucaabandon lucaplot', 'Alberto explains his father left him alone and he waited for a change of mind.',
 ['Abandonment by his father is the explicit explanation.', 'He describes his father choosing to leave, not parents lost at sea.', 'He waited for his father rather than running away from family.', 'His account describes paternal abandonment, not a sea-monster banishment.'],
 'The wall marks count days since father left, not a known death or legal exile. Both transcript and independent plot account establish abandonment.',
 'Different from #1441 tower structure: cause of living alone is a separate fact.')
review(1565, 'wade pipes', 'Wade openly expresses emotion and cries during the inspection scene.',
 ['His tears express the strong emotion.', 'His emotional reaction is not petrification.', 'His emotional reaction is not invisibility.', 'His emotional reaction is not emitting sparks.'],
 'Removed subjective most-defining ranking; checked the observed expressive behavior, not an assertion that his only trait is crying. Scene text explicitly records tears.',
 'Different from #1046 Wade name and #1410 inspector occupation.')
review(1566, 'glass', 'Ember seals the culvert with melted sand before the family dinner.',
 ['The scene explicitly melts sandbags into glass.', 'The repair is glass, not frozen water.', 'The scene uses no growing roots as the repair.', 'It seals with glass rather than steel plates.'],
 'Replaced the false city-saving climax premise with the earlier repair scene. Glass can later fail without contradicting what material sealed the doors in this scene.',
 'Different from #1413 fear before touching Wade and family-shop identity.')
review(1567, 'pipes', 'A pipe cracks after Ember loses her temper and Wade emerges into the flooded basement.',
 ['A water pipe bursts and sprays the room.', 'The depicted break is not a gas valve leak.', 'No ceiling-beam collapse is the event bringing Wade in.', 'A blocked chimney flue is not his route into the shop.'],
 'Removed unneeded corroded descriptor; checked the immediate pipe burst rather than confusing it with the later citywide culvert flood.',
 'Different from #1410 Wade job and #1566 culvert repair.')
review(1568, 'io2', 'Riley is 13 and the puberty alarm initiates the HQ change before new emotions arrive.',
 ['Puberty is the depicted developmental change.', 'The arrival is not caused by a new-city move; that belongs to the original film.', 'Her parents divorce is not the depicted trigger.', 'Friends school plans matter at camp, but loss of a best friend is not the biological trigger for new emotions.'],
 'Checked cause versus later camp stressors: puberty precedes the new arrivals and is not merely inferred from Anxiety behavior.',
 'Different from #471 Anxiety planning, #1414 sport and #1417 original emotions imprisonment.')
review(1569, 'io2', 'A worker explicitly names the sarcastic-echo gap Sar-chasm.',
 ['Sar-Chasm is the spoken pun name.', 'Snark Pit is not the spoken name.', 'Irony Gap is not the spoken name.', 'Wit End is not the spoken name.'],
 'Removed chasm from the stem to avoid giving away its unique name component. Confirmed it changes how listeners hear an echo rather than literally changing every thought or all speech.',
 'Different from #1416 Sense of Self and other original-film memory locations.')
review(1570, 'io2 nostalgia-corroboration', 'Anxiety tells Nostalgia she has about ten years before she is invited.',
 ['About ten matches the explicit line.', 'Two years does not match Anxiety line.', 'Twenty years does not match Anxiety line.', 'Six months does not match Anxiety line.'],
 'Checked that this asks the fictional joke as attributed to Anxiety, not a real claim about when humans can feel nostalgia. Contemporary review independently corroborates ten.',
 'Different from #480 Ennui and #1047 Envy identity.')
review(1571, 'voyd i2plot', 'Voyd signature ability connects two locations using portals.',
 ['Creating portals is the power described by Pixar production authors.', 'Invisibility is Violet established ability, not the described Voyd effect.', 'Electricity belongs to He-Lectrix in the roster, not Voyd portal power.', 'Super speed belongs to Dash, not the described spatial portal effect.'],
 'Checked the specific depicted spatial effect rather than treating one visual glow as proof of another power. Primary paper explicitly says her power creates openings connecting locations; roster distinguishes the competing hero abilities.',
 'Different from #489 Violet two powers and #1039 Jack-Jack unpredictable powers.')
review(1572, 'i2assets', 'Pixar describes Jack-Jack backyard fight with a raccoon.',
 ['A raccoon is explicitly the opponent.', 'A possum is not the identified animal.', 'A skunk is not the identified animal.', 'A coyote is not the identified animal.'],
 'The production character heading identifies the specific scene animal; the mask-like face is not used to guess among species.',
 'Different from #1039 Jack-Jack powers and #1276 baby name.')
review(1573, 'i2plot i2dialogue', 'Evelyn holds Helen under hypnosis with goggles.',
 ['Goggles are the device applied to her eyes.', 'A cloth blindfold blocks sight but is not the device in this scene.', 'A mirrored helmet is not the hypnosis device.', 'A sleep mask is not the hypnosis device.'],
 'Separated screen broadcasts from goggles worn by controlled victims; removed unsupported spiral-pattern specificity. Plot and dialogue both identify goggles controlling the adults.',
 'Different from #483 who masterminds Screenslaver; this asks the control device.')
review(1574, 'i2dialogue i2plot', 'Dicker wipes Tony memory after he recognizes unmasked Violet.',
 ['Tony Rydinger is the interviewed witness.', 'Dash is Violet brother, not this witness.', 'Buddy Pine is not the boy Dicker interviews.', 'Winston is not the classmate whose memory is wiped.'],
 'Removed later restored: Bob arranges a renewed meeting, not recovery of Tony erased memory. The opening interview names Tony and the later call confirms the wipe.',
 'Different from #71 Syndrome civilian identity and other Violet power questions.')
review(1575, 'i2assets', 'Elastigirl new motorcycle is called the Elasticycle.',
 ['Elasticycle is Pixar heading for the motorcycle.', 'The Incredimobile is not the motorcycle name.', 'Parr Racer is not its name.', 'Stretch Cycle is not its official name.'],
 'Checked motorcycle versus the family supercar; the similar invented Stretch Cycle is not the documented proper name.',
 'Different from #1576 yacht and #1159 park coaster name.')
review(1576, 'i2dialogue i2assets i2plot', 'Winston announces the televised signing ceremony aboard the Everjust.',
 ['Everjust is the name spoken in the announcement.', 'Incredible Voyager is not the announced boat name.', 'Deavor Star is not the announced boat name.', 'Municiberg Pearl is not the announced boat name.'],
 'Removed the conflation of the earlier world summit with the signing ceremony at sea. Confirmed proper name in dialogue, not merely Hydroliner production design label.',
 'Different from #1289 DevTech public leader and #1575 motorcycle.')
review(1577, 'soulbody', 'Joe and 22 arrive in separate wrong bodies at the hospital.',
 ['The script explicitly places 22 in Joe body and Joe in the cat.', 'The two occupy different bodies, not one body.', 'Joe is in a cat and 22 in his adult body; becoming a ghost and human is not the described pairing.', 'Joe adult body and a cat are present; neither becomes a child.'],
 'Checked both sides of the swap. Soul in the film title supplies no clue as to which body contains which character; this is not a character-number or afterlife-location duplicate.',
 'Different from #661 22 identity, #1438 Zone and #1439 Terry.')
review(1578, 'dez soulcast', 'Dez, Joe barber, explicitly identifies his former veterinary ambition.',
 ['Veterinarian is his stated planned career.', 'Jazz is Joe ambition, not Dez stated career plan.', 'Physician means a human medical doctor, not the veterinary career he names.', 'Pilot is not his stated career plan.'],
 'Replaced doctor with physician because veterinarian is also a doctor. Corrected barbershop regular to barber; the specific dialogue establishes the ambition.',
 'Different from #1316 jazz bandleader and #1437 Joe instrument.')
review(1579, 'roz rozreveal', 'Roz the dispatch manager appears as CDA Number One.',
 ['Roz is the revealed undercover leader.', 'Celia is the receptionist, which the original stem incorrectly attributed to Roz.', 'Needleman is not the Number One revealed in this scene.', 'Smitty is not the Number One revealed in this scene.'],
 'Corrected the job rather than accepting Roz under a false receptionist premise. The reveal names Roz, excluding all three other workers.',
 'Different from #1580 organization name and #657 company chief.')
review(1580, 'cda', 'Pixar names the yellow-suited human-contamination response teams CDA.',
 ['Child Detection Agency is the official organization name.', 'Human Containment Bureau is not the identified team.', 'Scare Safety Board is not its name.', 'Monster Homeland Security is not its name.'],
 'Read the actual team description, not just a generic Monsters synopsis. Human contamination is the monsters in-universe belief; no real-world toxicity claim is being made.',
 'Different from #1579 individual undercover leader and #640 scream energy.')
review(1581, 'ratcast', 'Django is explicitly Remy father and rat-clan patriarch.',
 ['Django is the father and colony leader.', 'Emile is Remy brother.', 'Auguste is the human chef Gusteau, not Remy father.', 'Horst is not the rat-clan father named Django.'],
 'Removed food-loving characterization that is more prominently associated with Emile. Explicit parentage supplies the discriminator, not food preferences.',
 'Different from #1300 brother identity and #263 Linguini human father.')
review(1582, 'ratcast', 'Colette is assigned to train Linguini in the kitchen.',
 ['Colette is explicitly the assigned trainer.', 'Danielle is not the trainer named in the profile.', 'Solange is not the trainer named in the profile.', 'Brigitte is not the trainer named in the profile.'],
 'Removed fiery stereotype and unnecessary romance clause; checked the specific work assignment, not any female name appearing in wider adaptations.',
 'Different from #1540 secret Remy partnership and #1278 head-chef identity.')
review(1583, 'hair ratplot', 'Remy steers Linguini physically by pulling his hair beneath the toque.',
 ['Hair pulling is the control mechanism.', 'He does not direct this secret movement mechanism by whispered words.', 'Glove hand signals are not how Remy controls his movements.', 'A hidden earpiece is not the mechanism.'],
 'Hair-yanking dialogue alone could describe annoyance, so corroborated the specific control mechanism with the plot account. The scene is physical steering, not translation of rat speech.',
 'Different from #1540 partner identity and #1050 rescued soup.')
review(1584, 'frozencharacters brunifire', 'Bruni is the salamander and Disney identifies him as the fire spirit.',
 ['Bruni is the named salamander.', 'Ember is not this Frozen spirit name.', 'Flicker is not the salamander name.', 'Spark is not the salamander name.'],
 'Used two primary passages to join species and elemental role rather than assuming that any salamander is the fire spirit.',
 'Different from #540 earth giants and #783 Elemental protagonist Ember.')
review(1585, 'frozendialogue frozenplot', 'Runeard built the dam to weaken Northuldra land.',
 ['Runeard is explicitly responsible in the memory.', 'The Duke is not the king in that historical memory.', 'Hans is not the king in that historical memory.', 'Pabbie is not the dam-building king.'],
 'Removed long unequal answer and broad central-mystery wording. The flashback specifically identifies intent and actor; the later dam destruction is a separate action.',
 'Different from #1097 Ahtohallan and #758 Northuldra people identity.')
review(1586, 'frozendialogue frozenplot', 'Elsa is explicitly identified as the fifth spirit.',
 ['Fifth is the number used in the reveal.', 'Third is not the number used for Elsa.', 'Fourth is not the number used for Elsa.', 'Sixth is not the number used for Elsa.'],
 'Replaced Snow Queen because it can also describe Elsa. Asked for the numbered spirit and checked the explicit fifth-spirit reveal, without denying Anna role as the other side of the bridge.',
 'Different from #1587 new monarch and #1600 Show Yourself song.')
review(1587, 'frozendialogue frozenplot', 'At the ending, Anna is introduced as Queen of Arendelle.',
 ['Anna is the new queen.', 'Kristoff becomes Anna fiance, not queen.', 'Iduna is their deceased mother, not the new queen.', 'Honeymaren remains a Northuldra character, not the crowned queen.'],
 'Checked the final succession and Elsa move rather than assuming the initial queen continues ruling; final introduction explicitly names Anna.',
 'Different from #14 sister relationship and #1586 spirit identity.')
review(1588, 'frozencharacters', 'Gale is explicitly the wind spirit.',
 ['Gale is the documented name.', 'Zephyr is not the spirit name.', 'Breeze is not the spirit name.', 'Squall is not the spirit name.'],
 'Removed specific hats-and-papers behavior so the primary character description fully establishes the remaining premise and name.',
 'Different from #1584 salamander and #1412 Elemental Gale air element; same name in different films is not the same character fact.')
review(1589, 'frozendialogue frozenplot olafvisual', 'After Elsa freezes, Olaf physical form breaks into snowflakes.',
 ['His form disintegrates into snowflakes.', 'He does not become a solid ice block; Elsa freezing is a different event.', 'He does not simply become a small intact snowball.', 'The described event is snowflake disintegration, not melting into liquid.'],
 'Replaced losing speech, which could also follow disappearance, with mutually exclusive physical-form alternatives. Corroborated transcript fading language with a visual-scene account.',
 'Different from #202 Olaf identity and #1602 Anna song timing; the latter has a separately recorded next-batch concern.')
review(1590, 'wish', 'Asha wish calls a celestial being named Star from the sky.',
 ['Star is the official character name.', 'Spark is not the named celestial helper.', 'Wisp is not the named helper.', 'Glimmer is not the named helper.'],
 'The official trailer text explicitly names the being, not just an unnamed star-shaped object. Other luminous names are not aliases in the stated film.',
 'Different from #850 goat name and #528 Magnifico identity.')
review(1591, 'wish', 'Disney names the kingdom ruled by Magnifico Rosas.',
 ['Rosas is the named kingdom.', 'Auradon is not the kingdom named in Wish.', 'Coronado is not the kingdom name.', 'Valoria is not the kingdom name.'],
 'Checked the ruler and kingdom association in the same source passage; the names are not competing translations of Rosas.',
 'Different from #528 ruler identity and #1590 celestial helper identity.')
review(1592, 'dallben', 'Dallben is the wizard and Taran mentor in the 1985 film.',
 ['Dallben is explicitly identified as mentor.', 'Fflewddur is not the wizard mentor named Dallben.', 'Gurgi is not the wizard mentor named Dallben.', 'Coll is not the film mentor named by Disney.'],
 'Specified Disney film and removed novel-derived farm/ownership details; Coll role in the source novels cannot create a second answer to the film-specific wizard question.',
 'Different from #863 Taran occupation and #1114 wandering minstrel.')
review(1593, 'witches', 'D23 supplies the complete trio of Morva witches.',
 ['These are all three listed Morva witches, in a different harmless order.', 'The Sleeping Beauty fairy trio is not the Morva witches.', 'These three Disney villains are not the named Morva trio.', 'These mythological names are not the film trio.'],
 'Removed ancient, shape-shifting and sword-trade clauses; matched all three proper names to the exhaustive character entry rather than approving a group from one shared name.',
 'Different from #47 Horned King and #2476 source-book series.')
review(1594, 'friar', 'D23 explicitly identifies Friar Tuck as a badger.',
 ['Badger is his identified species.', 'Bear is not Friar Tuck species.', 'Mouse is not Friar Tuck species.', 'Donkey is not Friar Tuck species.'],
 'Checked Disney animated portrayal rather than the human character in other Robin Hood adaptations; Little John being a bear does not transfer to Friar Tuck.',
 'Different from #859 Little John bear, #510 Robin fox and #2484 narrator bird.')
review(1595, 'cornelius robinsonsplot', 'Lewis grown-up identity is Cornelius Robinson.',
 ['Cornelius is the adult Lewis name.', 'Bud is Lewis adoptive father, not his future self.', 'Fritz is Bud brother, not Lewis future self.', 'Joe is another of Bud brothers, not Lewis future self.'],
 'Removed Wilbur father as a competing option because it is also Cornelius. All final choices are parallel names of distinct relatives, verified by the family-tree dialogue and cast account.',
 'Different from #1327 adult Goob villain identity, #1130 Franny mother identity and #839 motto.')

checks = ['singleAnswer', 'context', 'wording', 'noGiveaway', 'distinctFact', 'category', 'difficulty', 'scope']
assert set(reviews) == {r['questionId'] for r in notes['reviews']}
for record in notes['reviews']:
    qid = record['questionId']
    refs, premise, reasons, challenge, distinct = reviews[qid]
    refs = ['b28-' + s for s in refs]
    assert len(reasons) == 4
    record.update(checks=checks, notes=distinct + ' Complete category/topic context and all four final options reviewed. Static theatrical-film/history fact; difficulty calibrated editorially.',
                  context=premise, timeSensitive=False, nextReviewAt=None)
    record['premise'] = dict(reason=premise, sources=refs)
    record['options'] = [dict(basis='direct' if i == 0 else 'exclusive-inference', reason=reason, sources=refs)
                         for i, reason in enumerate(reasons)]
    record['challenge'] = dict(reviewer='Codex', at='2026-11-08', premiseChecked=True,
                              alternativesExcluded=True, notes=challenge)
notes['sourcesChecked'] = sorted({s for r in notes['reviews'] for s in r['premise']['sources']})
LIB.write_text(json.dumps(library, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
OUT.write_text(json.dumps(notes, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Authored {len(reviews)} explicit reviews using {len(notes["sourcesChecked"])} inspected source notes.')
