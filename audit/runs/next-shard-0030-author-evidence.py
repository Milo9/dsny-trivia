"""Explicit evidence notes from the batch-30 source and final-wording review.

Only writes evidence artifacts; content edits use patches and retirements use the
supported audit command. Does not infer source support or mark ledger approvals.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = '2026-11-08'
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))
def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

library = read('audit/source-notes.json')
S = library['sources']
def source(key, url, locator, evidence, secondary=False):
    key = 'b30-' + key
    S[key] = dict(url=url, locator=locator, evidence=evidence, checkedBy='Codex',
        checkedAt=DATE, timeSensitive=False, nextReviewAt=None, topics=['Batch 30'],
        limitations=('Secondary text or third-party dialogue transcription inspected; no film playback claimed. '
                    'Detailed passages and identified corroboration support the stated fact; the mirror is not studio-certified.'
                    if secondary else 'Institutional text inspected; no film or video playback claimed.'))
    return key

mermaid = source('mermaid', 'https://d23.com/a-to-z/little-mermaid-ii-the-return-to-the-sea-film/',
    'Synopsis and voices, lines 87-88', 'Melody is Ariel and Eric’s daughter. Morgana is Ursula’s sibling and plots against Triton.')
mermaidplot = source('mermaidplot', 'https://en.wikipedia.org/wiki/The_Little_Mermaid_II:_Return_to_the_Sea',
    'Plot: christening threat, lines 200-202', 'Morgana threatens Melody with her tiger-shark henchman Undertow; Triton shrinks him.', True)
mermaidscript = source('mermaidscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=little-mermaid-ii-return-to-the-sea-the',
    'Christening confrontation, lines 107-146', 'Morgana is identified as Ursula’s sister, calls Undertow, and threatens that Melody will be shark food.', True)
mulan = source('mulan', 'https://d23.com/a-to-z/mulan-ii-film/', 'Synopsis and cast, lines 87-89',
    'The Emperor sends his daughters to arranged marriages for alliances. The princesses fall for Yao, Ling and Chien-Po; cast names are Mei, Ting Ting and Su.')
mulanplot = source('mulanplot', 'https://en.wikipedia.org/wiki/Mulan_II', 'Plot, lines 198-201',
    'The mission is an alliance through marriages in Qui Gong. Daughters are Ting-Ting, Mei and Su; each falls in love with one of the three soldiers.', True)
cars = source('cars', 'https://www.pixar.com/cars-2', 'Characters: Holley Shiftwell; Professor Z; Miles Axlerod; Finn; Francesco',
    'Holley’s equipment includes a telescoping utility arm and holographic display. Professor Z designs weapons; Finn is a spy, Francesco a racer and Axlerod organizes the Grand Prix.')
carsplot = source('carsplot', 'https://en.wikipedia.org/wiki/Cars_2', 'Plot, lines 225-234',
    'Professor Zündapp leads the visible sabotage, but Mater exposes Sir Miles Axlerod as the hidden mastermind seeking to discredit alternative fuel.', True)
carsscript = source('carsscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=cars-2',
    'Opening lines 56-67; bomb reveal 2115-2130, 2245-2260; fuel explanation 2336-2339',
    'Professor Z is addressed as Zündapp (mirror loses the umlaut). Zündapp’s voice cannot disarm the bomb; Axlerod’s can. Axlerod engineered the fuel sabotage.', True)
patch = source('patch', 'https://d23.com/a-to-z/101-dalmatians-ii-patchs-london-adventure-film/',
    'Complete synopsis and cast, lines 87-88', 'In the 2003 sequel, Patch is left behind during the move and seeks his hero Thunderbolt. Lightning is a separate character.')
patchscript = source('patchscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=101-dalmatians-ii-patchs-london-adventure',
    'Fur shop 187-195; heiress 223-224; sidekick 299-314; henchmen 666-670',
    'The shopkeeper refuses furs because of Cruella’s probation. She calls herself overfinanced, and remains obsessed with furs. Thunderbolt’s sidekick is Little Lightning.', True)
never = source('never', 'https://d23.com/a-to-z/return-to-never-land-film/', 'Synopsis, lines 89-90',
    'During World War II, Hook kidnaps Wendy’s daughter Jane, mistaking her for Wendy, to bait Peter Pan.')
neverplot = source('neverplot', 'https://en.wikipedia.org/wiki/Return_to_Never_Land', 'Voice cast: Jane and Daniel, lines 203-209',
    'Jane initially refuses to believe the stories; Danny is her younger brother and Wendy’s son.', True)
cab = source('cab', 'https://en.wikipedia.org/wiki/The_Three_Caballeros', 'Plot: second gift, lines 253-254',
    'The second present is a Brazilian pop-up book. José shrinks himself and Donald to enter it; Panchito later gives the piñata.', True)
cabdetail = source('cabdetail', 'https://www.skywaytowonderland.com/the-three-caballeros/', 'Film plot: Brasil book, lines 105-107',
    'Donald opens a pop-up book labeled Brasil; José shrinks Donald and they enter its train scene for Bahia.', True)
bongo = source('bongo', 'https://d23.com/a-to-z/bongo-film/', 'Complete entry, line 88', 'Bongo is a young circus bear in Fun and Fancy Free.')
lulu = source('lulu', 'https://d23.com/a-to-z/lulubelle/', 'Complete entry, line 88', 'Lulubelle is Bongo’s girlfriend in Fun and Fancy Free.')
fantasia = source('fantasia', 'https://d23.com/a-to-z/fantasia2000-film/', 'Program synopsis, lines 89-90',
    'Pines of Rome accompanies flying whales; Firebird Suite a sprite restoring a ravaged forest; Rhapsody in Blue Manhattan; Symphony No. 5 abstract shapes; Carnival of the Animals flamingos.')
xmas = source('xmas', 'https://d23.com/a-to-z/beauty-and-the-beast-the-enchanted-christmas-film/',
    'Synopsis, lines 87-89', 'Forte is the malevolent pipe organ who opposes Belle and Beast’s romance.')
xmasplot = source('xmasplot', 'https://en.wikipedia.org/wiki/Beauty_and_the_Beast:_The_Enchanted_Christmas',
    'Plot, lines 181-187', 'The Beast dislikes Christmas because the curse was cast then. Forte prefers his enchanted status because the Beast appreciates his music.', True)
xmasscript = source('xmasscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=beauty-and-the-beast-the-enchanted-christmas',
    'Forte explains his motivation 244-267; Beast’s response 333-343; Christmas curse flashback 735-785',
    'Forte says his music was unneeded before the curse but the Beast now needs him as confidant; he orders Fife to stop the romance. The Beast recalls being cursed at Christmas.', True)
poca = source('poca', 'https://d23.com/a-to-z/pocahontas-ii-journey-to-a-new-world-film/', 'Synopsis, lines 89-90',
    'Pocahontas travels to England on a peace mission with diplomat John Rolfe. Rolfe and John Smith help save her.')
pocaplot = source('pocaplot', 'https://en.wikipedia.org/wiki/Pocahontas_II:_Journey_to_a_New_World',
    'Plot, lines 184-194', 'Smith is presumed dead, then returns hooded to rescue Pocahontas. At the end she chooses Rolfe, who sails with her; the film ends with a kiss, not a wedding.', True)
hunch = source('hunch', 'https://d23.com/a-to-z/hunchback-of-notre-dame-ii-the-film/', 'Synopsis, lines 87-88',
    'Esmeralda and Phoebus have a son, Zephyr. Circus master Sarousch coerces Madellaine to distract Quasimodo so he can steal a bell.')
hunchplot = source('hunchplot', 'https://en.wikipedia.org/wiki/The_Hunchback_of_Notre_Dame_II', 'Plot, lines 190-196',
    'Zephyr is Quasimodo’s friend, not his ward. Sarousch wants La Fidèle, whose interior holds precious decoration.', True)
hunchscript = source('hunchscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=hunchback-of-notre-dame-ii-the',
    'Bell polishing 94-120; Quasimodo shows La Fidèle’s interior 656-667',
    'Characters call the bell La Fidèle; Quasimodo shows its valuable interior to Madellaine. Zephyr calls Esmeralda and Phoebus his parents.', True)
cinder3 = source('cinder3', 'https://en.wikipedia.org/wiki/Cinderella_III:_A_Twist_in_Time',
    'Plot, lines 188-190', 'Anastasia takes the dropped wand and shows it to Tremaine. Tremaine rewinds to the Grand Duke’s slipper fitting, then enlarges the slipper for Anastasia.', True)
cinder3script = source('cinder3script', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=cinderella-3-a-twist-in-time',
    'Wand and reversal sequence, lines 34-143', 'Anastasia brings home the wand. Tremaine reverses time and the Grand Duke arrives for the slipper fitting.', True)
cinder2 = source('cinder2', 'https://d23.com/a-to-z/cinderella-ii-dreams-come-true-film/', 'Synopsis, line 89',
    'Anastasia falls in love with the town baker in Cinderella II: Dreams Come True.')
bear = source('bear', 'https://movies.disney.com/brother-bear-2', 'Film synopsis',
    'Kenai reunites with his childhood human friend Nita and they journey to burn the amulet he gave her.')
bear2 = source('bear2', 'https://d23.com/a-to-z/brother-bear-2-film/', 'Synopsis: carved amulet and Hokani Falls',
    'Nita cannot marry until she and Kenai burn the carved amulet together at Hokani Falls; their childhood friendship renews.')
rescuers = source('rescuers', 'https://d23.com/a-to-z/rescuers-down-under-the-film/', 'Synopsis and Orville/Wilbur production note, lines 88-91',
    'Wilbur flies Bernard and Bianca to Australia. Frank is a frill-necked lizard; Jake is their Australian ally. Wilbur replaces his brother Orville from the original film.')
rescuersplot = source('rescuersplot', 'https://en.wikipedia.org/wiki/The_Rescuers_Down_Under',
    'Plot and Voice cast, lines 234-254', 'Wilbur flies the mice, Jake is their local hopping-mouse guide, and Frank is McLeach’s captive lizard. Cody is the boy and Marahute the eagle.', True)
coco = source('coco', 'https://www.pixar.com/coco', 'Characters: Pepita, lines 129-131; Frida, lines 164-166',
    'Pepita is an alebrije spirit guide inspired by colorful Mexican folk art. Frida is an artist ally in the Land of the Dead.')
cocolatino = source('cocolatino', 'https://www.disneylatino.com/novedades/dia-de-muertos-que-son-los-alebrijes-y-como-aparecen-en-coco',
    'Frida and Dante paragraphs, lines 43-46', 'Frida Kahlo appears with a monkey alebrije. Dante becomes a winged alebrije and is recognized as Miguel’s spirit guide.')
light = source('light', 'https://en.wikipedia.org/wiki/Lightyear_(film)', 'Plot, lines 227 and 231-233',
    'Buzz’s flights cause relativistic time dilation. Zurg is an older Buzz from an alternate timeline, not Buzz’s father or commander.', True)
lightscript = source('lightscript', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=lightyear',
    'Hawthorne explanation 359-376; Zurg reveal 1577-1619', 'Hawthorne identifies time dilation: Buzz ages minutes while the colony ages years. Zurg rejects the father guess and identifies himself as an older Buzz.', True)
princess = source('princess', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=ralph-breaks-the-internet',
    'Princess interrogation, lines 1454-1486', 'Vanellope denies magic/animal/witch tropes but agrees that people assume a strong man solved her problems; the others then accept her as a princess.', True)
princessnews = source('princessnews', 'https://www.thejournal.ie/disney-ralph-breaks-the-internet-princesses-4354484-Nov2018/',
    'Opening description of princess scene', 'The scene criticizes outsiders’ assumption that a princess’s problems were solved by a strong man.', True)
ralph = source('ralph', 'https://www.museumofplay.org/blog/wreck-it-ralph-and-video-game-villainy/',
    'Opening-scene discussion, lines 197-199', 'Ralph attends the villain group with Clyde, Bowser and Zangief; Clyde directs him to accept who he is.', True)
ralphscript = source('ralphscript', 'https://giveadaygetadisneyday.blogspot.com/2014/08/wreck-it-ralph-2012-full-script.html',
    'Opening group sequence 93-129; station 149-161',
    'Bowser attends the group; its leader conducts questions and the affirmation. The camera pulls back to the central room of Pac-Man, then the group travels to Game Central Station. Sonic appears on a station PSA and Pac-Man at Felix’s party.', True)
S[ralphscript]['limitations'] += ' This fan mirror mislabels the ghost Blinky; do not use it to identify Clyde. Character identity is corroborated separately.'
aladdin = source('aladdin', 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=aladdin',
    'Genie’s three rules, lines 725-734; cave escape 740-757',
    'The three stated rules are no killing, no forcing love and no resurrecting the dead. Genie subsequently leaves the cave with Aladdin.', True)
aladdin2 = source('aladdin2', 'https://en.wikipedia.org/wiki/Genie_(Disney)',
    'Involvement, line 175', 'Genie’s limitations include killing, forcing love and reviving the dead.', True)
ralphproduction = source('ralphproduction', 'https://www.cinemovie.tv/index.php/behind-the-scenes/wreck-it-ralph-movie-production-notes?highlight=WyJlcGljIl0%3D',
    'WHO’S WHO AT BAD-ANON, lines 290-305', 'Disney production notes identify Clyde as Bad-Anon’s leader, Zangief as a regular attendee, and the venue as Pac-Man’s digs.')
S[ralphproduction]['limitations'] = 'Studio production notes reproduced by a third-party publication; corroborated with contemporary museum discussion and scene transcription. No film playback claimed.'

R = {}
def review(qid, sources, premise, reasons, challenge, distinct):
    R[qid] = dict(sources=sources, premise=premise, reasons=reasons, challenge=challenge, distinct=distinct)
review(2018,[mermaid], 'The sequel explicitly identifies Ariel and Eric’s daughter as Melody.',
    ['Melody is the named daughter.', 'Marina is not the daughter identified in this family.', 'Coral is not the daughter identified in this family.', 'Pearl is not the daughter identified in this family.'],
    'Checked the specific sequel family rather than any mermaid character: only Melody is Ariel and Eric’s daughter.', 'Different from Melody’s helpers #2319 and her locket/wall #2320–2321.')
review(2019,[mermaid,mermaidscript], 'The villain Morgana is Ursula’s sister and threatens Triton’s family.',
    ['Morgana is the named sibling.', 'Vanessa is not the sibling identified in this sequel.', 'Marina del Rey is not the sibling identified here.', 'Ursulina is not the sibling identified here.'],
    'Sibling identity is unique; removed unnecessary age comparison. Vanessa’s original-film disguise cannot meet this sequel relationship.', 'Different from original Ursula identity and Vanessa disguise #822.')
review(2020,[mermaidplot,mermaidscript], 'Morgana’s named shark henchman is Undertow, correcting the eel premise.',
    ['Undertow is summoned as the shark threat.', 'Flotsam is not Morgana’s named shark.', 'Jetsam is not Morgana’s named shark.', 'Glut is not the named sequel henchman.'],
    'Challenged the shark/piranha transformation: Undertow is originally a shark despite being shrunk for much of the film; neither original-film eel nor Glut is him.', 'Original-film eel pair #68 tests a different employer and identity.')
review(2021,[mulan,mulanplot], 'The assigned mission is arranged royal marriages to secure an alliance with Qui Gong.',
    ['The Emperor arranges the marriages for an alliance.', 'Seeking refuge is not his stated purpose.', 'A trade agreement is not the stated marriage mission.', 'Warrior training is not the daughters’ assigned mission.'],
    'Separated the Emperor’s original order from the later romance and cancelled marriages; only the alliance answer describes the assignment.', 'Different from daughters’ names, their new romances, and Mushu’s own motive #2330.')
review(2022,[mulan,mulanplot], 'The complete daughter roster is Ting-Ting, Mei and Su.',
    ['This is the complete named trio.', 'Lin replaces Mei and is not in the roster.', 'Fa replaces Ting-Ting and is not in the roster.', 'Xiu and Ting do not give the complete named roster.'],
    'Checked complete sets, not just shared Mei/Su names. Only the first option contains all three daughters.', 'Names differ from the marriage mission and love-count facts.')
review(2023,[mulan,mulanplot], 'Each princess pairs romantically with one of the three escorting soldiers.',
    ['All three soldiers fall in love, one per princess.', 'Only one contradicts the three pairings.', 'Only two omits one pairing.', 'None contradicts every pairing.'],
    'All is a count of the named soldiers, not all men in the film; the sources enumerate a romance for each soldier.', 'Different from identifying the princesses or their intended spouses.')
review(2024,[carsplot,carsscript,cars], 'The final reveal exposes Axlerod as the hidden architect of the fuel-sabotage plot.',
    ['Axlerod is exposed and his voice disarms the bomb.', 'Zündapp serves the hidden mastermind and cannot disarm it.', 'Finn investigates the sabotage as a British spy.', 'Francesco is a racing competitor, not the revealed mastermind.'],
    'Zündapp also directs villains, but the final hidden-mastermind reveal and bomb test identify Axlerod alone.', 'Separate from fuel name #1282 and veteran spy identity #1031.')
review(2025,[cars], 'Pixar’s Holley biography explicitly lists a telescoping utility arm in her equipment.',
    ['Pixar names the telescoping utility arm.', 'A folding crane boom is a different arm mechanism.', 'An inflatable lifting arm is not the identified telescoping device.', 'A scissor-lift platform is not the identified arm.'],
    'Asks the named kind of extendable arm, not which of several weapons she might also possess. Removed the unestablished primary-weapon ranking.', 'Equipment type adds a fact beyond the spy-role comparison #1031.')
review(2026,[carsplot,carsscript], 'Professor Z is the abbreviated form of Professor Zündapp in Cars 2.',
    ['Zündapp is the character’s full name.', 'Zweig is not his stated surname.', 'Zeller is not his stated surname.', 'Zorn is not his stated surname.'],
    'All options now share Professor and Z; neither title nor initial picks the answer. Transcript and cast/plot establish the full surname.', 'Different from the hidden-mastermind reveal.')
review(2027,[patch], 'Patch is the puppy left behind during the family move in the 2003 sequel.',
    ['Disney identifies Patch as left behind.', 'Rolly is not the puppy identified in this moving-day event.', 'Lucky is not the puppy identified here.', 'Pepper is not the puppy identified here.'],
    'The question omits the sequel subtitle, avoiding a Patch giveaway; only Patch is the accidentally forgotten puppy.', 'Distinct from his hero’s name and Lucky’s later reminder #2464.')
review(2028,[patch,patchscript], 'Patch idolizes the fictional television dog Thunderbolt within the film.',
    ['Thunderbolt is the heroic star Patch seeks.', 'Lightning is Thunderbolt’s sidekick, not the hero asked for.', 'Ace is not Patch’s named TV hero.', 'Blaze is not Patch’s named TV hero.'],
    'Lightning is a genuine show character but is explicitly the sidekick. This is an in-universe plot reference, not real TV trivia.', 'Separate from Lightning’s sidekick identity #2339; the two questions assign distinct roles.')
review(2029,[patchscript], 'The fur seller explicitly cites Cruella’s probation as the reason he cannot sell her furs.',
    ['Her probation bars the sale.', 'She describes herself as overfinanced, not penniless.', 'She begs for furs, disproving reformation or lost interest.', 'The exchange occurs in London and cites probation, not total city banishment.'],
    'A restraining order also exists, but the shopkeeper expressly gives probation as the purchase restriction; no other listed motive fits.', 'Different from Lars’s identity and art commission #2463.')
review(2030,[never,neverplot], 'Jane is Wendy’s skeptical daughter in the 2002 sequel.',
    ['Jane is the daughter named in the film.', 'Danny is her younger brother, not Wendy’s daughter.', 'Molly is not the daughter identified in this sequel.', 'Alice is not the daughter identified here.'],
    'Initial skepticism is scene context, not an assertion that she never changes; Danny’s different family role excludes him.', 'Different from the wartime setting and Hook’s mistaken identity motive.')
review(2031,[never], 'Disney places this sequel’s London story during World War II.',
    ['World War II is the stated setting.', 'World War I is a different conflict.', 'The Napoleonic Wars are a different period.', 'The Crimean War is a different period.'],
    'Checked the sequel rather than the original Edwardian Peter Pan; only WWII is its setting. All options are wars.', 'Sharing WWII with studio revenue question #1204 does not establish this film’s setting.')
review(2032,[never], 'Hook mistakes Jane for Wendy and takes her as bait for Peter Pan.',
    ['Mistaking Jane for Wendy is the stated cause.', 'A need for a cook is not the stated kidnapping motive.', 'A stolen treasure map is not the stated cause.', 'An insult to Hook’s mustache is not the stated cause.'],
    'Hook’s ultimate target is Peter, but the question asks why Jane was selected: his mistaken identification is explicit.', 'Different from naming Jane; knowing Wendy’s daughter does not explain Hook’s mistake.')
review(2033,[cab,cabdetail], 'The Brazilian pop-up book is the gift Donald and José enter after José’s shrinking magic.',
    ['The Brasil pop-up book carries them into Bahia.', 'They do not enter a miniature theater in this gift scene.', 'Mexico is explored later via Panchito’s flying serape, not this map.', 'The piñata is a separate gift, not the entered book.'],
    'Fixed agency: José shrinks them; the book does not itself shrink them. Both detailed accounts identify the entered gift as a book.', 'Different from Caballeros character introductions in Saludos Amigos.')
review(2034,[lulu], 'Disney identifies Lulubelle as Bongo’s girlfriend.',
    ['Lulubelle is the named girlfriend.', 'Lumpjaw is not the girlfriend identified by Disney.', 'Daisy is not the named girlfriend in Bongo.', 'Bearbelle is not the named girlfriend in Bongo.'],
    'Removed the unsupported cub age. The relationship identifies Lulubelle uniquely among all four names.', 'Character relationship differs from Bongo’s occupation.')
review(2035,[bongo], 'Bongo is a circus bear before his escape.',
    ['He performs in the circus.', 'He is not employed as a lumberjack’s helper in this setup.', 'A zoo exhibit is a different captivity setting from his circus job.', 'A logging-camp mascot is a different occupation.'],
    'Asked his occupation before escape, not any act he can perform. Circus context excludes the other workplaces without relying on the unicycle detail.', 'Different from naming Lulubelle and the film’s other giant/harp story.')
review(2036,[fantasia], 'Pines of Rome is the Fantasia 2000 composition paired with flying whales.',
    ['Respighi’s Pines of Rome accompanies the whales.', 'Firebird Suite accompanies forest destruction and renewal.', 'Rhapsody in Blue accompanies Manhattan stories.', 'Symphony No. 5 accompanies abstract forms.'],
    'Checked all four segment pairings, not merely the composer; only Pines of Rome is the whale sequence.', 'Different from Rhapsody city #539, original Rite of Spring #389 and Firebird forest sequence.')
review(2037,[fantasia], 'Firebird Suite is the forest destruction-and-regeneration segment.',
    ['Firebird Suite follows the sprite and ravaged forest.', 'Pines of Rome follows flying whales.', 'Rhapsody in Blue follows city residents.', 'Carnival of the Animals follows flamingos and a yo-yo.'],
    'Only Firebird has the nature-spirit forest renewal plot; other segment settings are explicitly different.', 'Separate from whales, Manhattan, and flamingo hobby #2387.')
review(2038,[xmas], 'Forte is the pipe-organ antagonist in The Enchanted Christmas.',
    ['Forte is the named villain.', 'Maestro is a title, not his name.', 'Cadenza belongs to the separate 2017 film, not this villain.', 'Crescendo is not the villain identified in this film.'],
    'The film version excludes Cadenza, another genuine musical character. Forte’s proper name differs from a musical title.', 'Different from Forte’s motivation and Cadenza’s transformation in #2065.')
review(2039,[xmasscript,xmasplot], 'Forte wants his valued place as the Beast’s musical confidant to continue.',
    ['The cursed Beast now depends on his music and counsel.', 'Forte does not cite a theft of treasure as his motive.', 'He does not cite an Enchantress promise of a throne.', 'He does not claim a romance with Belle as his goal.'],
    'Replaced the false loss-of-talent premise. His own explanation contrasts former neglect with present influence, excluding the three alternate motives.', 'A motive fact, not the pipe organ’s name or Beast’s reason for hating Christmas.')
review(2040,[xmasplot,xmasscript], 'The Beast associates Christmas with the day he was cursed.',
    ['The spell was cast at Christmas.', 'Christmas itself is not the mechanism that can break the spell.', 'His late father is not the stated holiday association.', 'He was transformed by the curse, rather than specifically enchanted to hate Christmas.'],
    'Separated the curse’s timing from an invented instruction to hate a holiday; only the transformation date explains the stated aversion.', 'Different from Forte’s preference for the curse and the original rose deadline.')
review(2041,[pocaplot,poca], 'The sequel ends with Pocahontas choosing Rolfe and sailing with him.',
    ['John Rolfe is the partner she chooses.', 'She parts from John Smith as a friend.', 'Ratcliffe is the antagonist, not her chosen partner.', 'Thomas is not the partner in the ending.'],
    'The first-film romance would make Smith plausible, so anchored the question to the sequel’s ending; removed the marriage/history conflation.', 'Different from original-film love interest #33 and Smith’s hooded rescue.')
review(2042,[poca,pocaplot], 'Pocahontas travels in Powhatan’s stead for diplomatic peace negotiations.',
    ['Seeking peace is the mission Disney describes.', 'Smith is believed dead; finding him is not her mission.', 'She travels as an envoy, not to take a royal household post.', 'No stolen artifact is the diplomatic mission described.'],
    'Distinguished her eventual reunion with Smith from her original purpose; the named peace mission excludes the other proposed goals.', 'Different from King James’s identity and the bear-baiting provocation.')
review(2043,[pocaplot,poca], 'The hooded rescuer reveals himself as John Smith, who was presumed dead.',
    ['Smith is the disguised returning rescuer.', 'Ratcliffe is the opponent who framed Smith.', 'Kocoum is not the hooded rescuer in this sequel.', 'Thomas is not the hooded rescuer.'],
    'Used presumed dead rather than requiring deliberate death-faking. The specific hooded rescue identifies Smith independently of the first-film romance.', 'Shared Smith answer with #33 tests a different scene and relationship.')
review(2044,[hunch,hunchscript], 'Zephyr is the son of Esmeralda and Phoebus.',
    ['Zephyr is the named son.', 'Zephyrus is not his stated name.', 'Django is not the son’s stated name.', 'Marcel is not the son’s stated name.'],
    'Removed ward: both parents are alive and parent him. Checked the exact name Zephyr rather than a similar Greek-derived variant.', 'Distinct from the ending kiss #2338 and seven-year chronology #2337.')
review(2045,[hunchplot,hunchscript], 'Sarousch targets the treasured bell La Fidèle, decorated inside.',
    ['La Fidèle is the named target bell.', 'La Cloche d’Or is not the bell’s stated name.', 'Le Grand Bourdon is not the target name in this film.', 'L’Esprit Sacré is not the target name in this film.'],
    'Checked the fictional film bell rather than names of real Notre-Dame bells. Its decoration is inside; the proper name remains unique.', 'Different from the villain’s identity and the ending action when Zephyr rings it.')
review(2046,[hunch], 'Sarousch is the circus master coercing Madellaine to distract Quasimodo.',
    ['Sarousch is the named circus villain.', 'Frollo is not this sequel’s circus master.', 'Clopin is not the coercing circus master.', 'Phoebus is not the coercing circus master.'],
    'Specified the sequel’s circus and coercion; the earlier villain and returning Parisian characters cannot replace Sarousch.', 'Different from Madellaine’s performance aspiration #2336 and the stolen bell’s name.')
review(2047,[cinder3,cinder3script], 'Anastasia first takes the dropped wand before giving it to her mother.',
    ['Anastasia takes and brings home the wand.', 'Drizella is at home and does not first take it.', 'Cinderella does not first take the dropped wand.', 'Tremaine acquires it from Anastasia later.'],
    'Later possession would make Tremaine arguable under broad steals wording, so final wording asks the first pickup after the drop.', 'Different from #2446’s slipper recipient and #2049’s baker romance.')
review(2048,[cinder3,cinder3script], 'Tremaine rewinds the story to the Grand Duke’s slipper fitting.',
    ['The Grand Duke’s visit is where time resumes.', 'It does not resume at Cinderella meeting the mice.', 'It does not resume during the Prince’s childhood.', 'The Fairy Godmother’s earlier visit is not the return point.'],
    'Checked the exact destination of the reversal, distinct from the later enlargement spell and altered slipper result.', 'Different from #2446: reversal destination versus whose foot the slipper fits.')
review(2049,[cinder2], 'The baker romance belongs to Cinderella II and features Anastasia.',
    ['Anastasia is the stepsister in the baker romance.', 'Drizella is not the stepsister in that romance.', 'Only Anastasia, not both sisters, has this storyline.', 'Neither is false because Anastasia does.'],
    'Corrected the movie from III to II. Only Anastasia is identified in the baker relationship; the third film’s prince subplot is separate.', 'Different from the baker’s gesture #2322, Cinderella’s line #2323, and wand/slipper facts.')
review(2050,[bear,bear2], 'Kenai gave Nita an amulet whose spiritual bond requires their joint burning ritual.',
    ['The object is explicitly an amulet.', 'The ritual object is not a painted mask.', 'The ritual object is not a woven bracelet.', 'The ritual object is not a feather headdress.'],
    'An amulet can also be a carved necklace, so removed that overlapping distractor. The surviving alternatives are different objects.', 'Different from shaman identity #2194 and the site’s participants/romantic history.')
review(2051,[bear], 'Nita knew Kenai as his childhood human friend.',
    ['She is his childhood friend.', 'The described relationship is not adoptive motherhood.', 'The described relationship is not rival chief.', 'The described relationship is friendship, not siblinghood.'],
    'Removed childhood from the stem and shortened parallel answers. The friend relationship excludes parental, political and sibling relationships.', 'Different from Atka’s betrothal #2193 and amulet object #2050.')
review(2052,[rescuers,rescuersplot], 'Wilbur is the albatross transport for the Australian rescue.',
    ['Wilbur is the sequel’s albatross pilot.', 'Orville is the original film’s pilot, replaced by his brother.', 'Marahute is the eagle, not the albatross pilot.', 'Frank is the captive lizard, not the pilot.'],
    'The two albatross brothers make the sequel version essential; only Wilbur handles this Australian flight.', 'Different from original pilot #861 and country setting #523.')
review(2053,[rescuers,rescuersplot], 'Frank is the captive lizard and Jake the local guide, in that order.',
    ['Frank and Jake match the two stated roles respectively.', 'Wilbur is an albatross and Cody a human boy, not this pair.', 'Rex and Sydney do not name the stated lizard/guide pair.', 'Bruce and Digger do not name the stated lizard/guide pair.'],
    'Removed the false joint-guide description. Captive Frank and guide Jake have separate roles; order is explicit.', 'Different from the albatross pilot and the eagle species #254.')
review(2054,[coco,cocolatino], 'Coco uses alebrijes as the specific name for its folk-art spirit-guide creatures.',
    ['Alebrijes is the explicit creature name.', 'Ofrendas is not the specific creature name given by Pixar.', 'Cempasúchiles is not the specific creature name given by Pixar.', 'Calaveras is not the specific creature name given by Pixar.'],
    'Generic spirits or guardians could describe their function, so replaced those options. Asked the specific named creature class, not a broad description.', 'Different from Pepita’s individual name #771 or animal components #2438.')
review(2055,[coco,cocolatino], 'Frida Kahlo is the real artist depicted as Miguel’s Land-of-the-Dead artistic ally.',
    ['Frida Kahlo is the artist identified by Disney.', 'Diego Rivera is not the artist identified in this scene.', 'Dolores del Río is not the artist staging this scene.', 'Cantinflas is not the artist staging this scene.'],
    'Other cultural figures may appear elsewhere; the specific artistic ally/performance scene identifies Kahlo alone.', 'Different from #2178, which asks whose disguise Héctor wears, not who creates the performance.')
review(2058,[light,lightscript], 'Lightyear reveals Zurg as an older alternate-timeline Buzz.',
    ['He is the older alternate Buzz.', 'Buzz guesses father and is explicitly corrected.', 'The armor hides Buzz, not an alien-built robot identity.', 'Buzz’s former commander is Alisha, not Zurg’s revealed identity.'],
    'Kept Lightyear separate from Toy Story 2’s father joke; a robotic suit is not the identity of its wearer.', 'Different from fuel crystal #1295 and time dilation cause #2059.')
review(2059,[light,lightscript], 'Hawthorne explicitly explains the elapsed years as time dilation near hyperspeed.',
    ['Relative travel speed causes time dilation.', 'Hawthorne explains travel speed, not a broken stasis pod.', 'The returning flights advance relative time, not repeat a time loop.', 'The explanation is speed-dependent, not an unusual planetary orbit.'],
    'The colony does age while he flies; the later time-travel plot does not change Hawthorne’s explicit explanation of this effect.', 'Different from Zurg’s identity and the tested fuel source.')
review(2060,[princess,princessnews], 'Rapunzel’s final question is about outsiders assuming a strong man solved their problems.',
    ['Vanellope agrees with this assumption being made about her.', 'A lost glass slipper is not Rapunzel’s final question.', 'Singing instruction from pets is not the agreed assumption.', 'A universal wicked-stepmother history is not the agreed assumption.'],
    'Corrected the distinction between what actually solves their problems and what people assume; no claim every princess shares Cinderella’s biography.', 'Different from Vanellope’s chosen racing career #1422 and Yesss’s role #848.')
review(2061,[ralphproduction,ralph,ralphscript], 'Clyde directs the Bad-Anon meeting and its closing affirmation.',
    ['Clyde is the directing ghost identified in the scene discussion.', 'Zangief shares advice as a member, not the leader.', 'King Candy is not the meeting leader.', 'Bowser attends as a member, not the leader.'],
    'Speaking advice does not imply leadership: Zangief and Bowser are fellow members; the source describing Clyde’s directing role supplies the identification. Fan transcript’s Blinky label is not used for his name.', 'Location removed from the stem so #2063 retains its independent setting fact.')
review(2062,[ralph,ralphscript], 'Bowser is one of the opening Bad-Anon attendees.',
    ['Bowser reacts in the meeting and is listed by the museum.', 'Sonic’s station PSA is a different scene, not meeting attendance.', 'Mario is not among the attendees in this opening scene.', 'Pac-Man appears at Felix’s party, not as a Bad-Anon attendee.'],
    'A cameo somewhere in the film is insufficient; only Bowser attends this meeting among these four. Its location in Pac-Man does not make Pac-Man a participant.', 'Separate from meeting leader #2061 and venue #2063.')
review(2063,[ralphscript,ralphproduction], 'The opening pullback places Bad-Anon in Pac-Man’s central ghost room.',
    ['The pullback reveals Pac-Man’s ghost pen.', 'They ride from Pac-Man to the station afterward.', 'Sugar Rush’s castle is not the room revealed by the pullback.', 'Hero’s Duty is not the game housing the opening group.'],
    'Distinguished a game’s room from the later station concourse; the explicit journey between them excludes the station answer.', 'Independent venue fact now absent from #2061’s stem; #1420 asks group name.')
objects = source('objects', 'https://d23.com/then-and-now-the-enchanting-cast-of-magical-objects-in-beauty-and-the-beast/',
    'The Wardrobe/Madame Garderobe: 2017 paragraph, line 90', 'In the 2017 film, Garderobe is a wardrobe and her husband Cadenza a harpsichord.')
dogscript = source('dogscript', 'https://assets.scriptslug.com/live/pdf/scripts/beauty-and-the-beast-2017.pdf',
    'Screenplay dated August 10, 2016, printed page 30: Froufrou entrance; page 31: Garderobe’s pet',
    'Froufrou is a small animated piano stool that barks and helps Garderobe; she addresses him as her dog.')
S[dogscript]['limitations'] = 'Original screenplay hosted by a third party; development script can differ from final film. Final-film cast account independently confirms stool transformation; no playback claimed.'
dogplot = source('dogplot', 'https://en.wikipedia.org/wiki/Beauty_and_the_Beast_(2017_film)', 'Cast: Gizmo/Frou-Frou, line 270',
    'Frou-Frou, Cadenza and Garderobe’s pet dog, is transformed into a footstool.', True)
review(2064,[objects], 'Garderobe’s cursed form in the 2017 film is a wardrobe.',
    ['She becomes a wardrobe.', 'Cadenza, not Garderobe, becomes a harpsichord.', 'A footstool is not her described enchanted form.', 'A music box is not her described enchanted form.'],
    'Specified the 2017 version rather than assuming the animated wardrobe’s name. Garderobe and Cadenza have different cursed forms.', 'Different from the animated clock/candelabra questions and Cadenza/dog transformations.')
review(2065,[objects], 'Cadenza’s cursed form in the 2017 film is a harpsichord.',
    ['He becomes a harpsichord.', 'A grand piano is not the named instrument.', 'A pipe organ belongs to Forte’s separate film, not Cadenza.', 'A spinet piano is not the named instrument.'],
    'Replaced non-instrument distractors; all four are keyboard instruments but only harpsichord matches Cadenza. Forte is a plausible different-film confusion.', 'Different from Garderobe, dog and Forte’s identity/motivation.')
review(2066,[dogscript,dogplot], 'The 2017 film turns the couple’s dog into a stool.',
    ['A stool matches both the screenplay and final-film account.', 'A rug is not the dog’s enchanted form.', 'A lamp is not the dog’s enchanted form.', 'A cushion is not the dog’s enchanted form.'],
    'The screenplay calls it a piano stool while the final-film account calls it a footstool. Broader stool is supported by both and cannot mean any other listed object.', 'Different from the two owners’ transformations; each maps a different character to an object.')
review(2067,[aladdin,aladdin2], 'Genie’s initial list of three wish limitations includes an inability to force love.',
    ['Forcing love is explicitly rule two.', 'Leaving the cave is not in the three rules; he soon does so.', 'Two simultaneous masters is not one of this enumerated three-rule list.', 'Invisibility is not one of this enumerated three-rule list.'],
    'The question asks membership in the explicit three-rule list, not all imaginable constraints on a genie. The list is exhaustive for that wording.', 'Different from #2068’s no-resurrection rule; knowing one prohibition does not establish the other.')

template = read('audit/runs/next-shard-0030-final-template.json')
template['at'] = DATE
template['reviews'] = [r for r in template['reviews'] if r['questionId'] in R]
for item in template['reviews']:
    data = R[item['questionId']]
    item.update(checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],
        notes='Full topic/category digests and cross-bank comparisons read. ' + data['distinct'] + ' Category and recall difficulty fit; sequel/in-universe scope checked.',
        context='Released film/version named in the final question; English-language character names and story. Historical fictional fact.',
        timeSensitive=False, nextReviewAt=None)
    item['premise'] = dict(reason=data['premise'], sources=data['sources'])
    item['options'] = [dict(basis=('direct' if n == 0 else 'exhaustive-list' if item['questionId']==2067 else 'exclusive-inference'),
        reason=reason, sources=data['sources']) for n,reason in enumerate(data['reasons'])]
    item['challenge'] = dict(reviewer='Codex',at=DATE,premiseChecked=True,alternativesExcluded=True,notes=data['challenge'])
template['sourcesChecked'] = sorted({s for d in R.values() for s in d['sources']})
write('audit/runs/next-shard-0030-reviewed-notes.json',template)
write('audit/source-notes.json',library)

initial = read('artifacts/question-audit/current-compact.json')['catalog']
for qid, replacement, reason, url, locator in [
    (2056,2415,'Both ask the identity of the same coconut-armored pirates. Retain the sequel-context question; the retired original also wrongly says they seek Maui’s fishhook, whereas they seek Te Fiti’s heart.', 'https://www.disney.co.jp/movie/moana', 'Character: Kakamora (Japanese official character description; target is Te Fiti’s heart)'),
    (2057,2580,'Exact same reveal that Kevin is female. Retain 2580 with more coherent alternative discoveries; the retired question’s gender stem makes its robot/two-birds alternatives conspicuous.', 'https://en.wikipedia.org/wiki/Up_(2009_film)', 'Plot, line 260: Kevin revealed female'),
]:
    if str(replacement) not in initial:
        for path in (ROOT/'questions').glob('q-*.json'):
            for q in json.loads(path.read_text(encoding='utf-8')):
                if q['id']==replacement:
                    initial[str(replacement)]=q
    write(f'audit/runs/next-shard-0030-comparison-{qid}-{replacement}.json',dict(
        reviewer='Codex',at=DATE,questions=[initial[str(qid)],initial[str(replacement)]],
        decision='retire',retiredId=qid,replacedBy=replacement,reason=reason,
        sources=[dict(url=url,locator=locator)],challenge='Read both complete questions and all options: the same identity/reveal answers both without learning an independent fact.'))
print(f'Authored {len(template["reviews"])} final-wording reviews; sources and two retirement comparisons saved.')
