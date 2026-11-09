"""Expand explicit Batch 27 evidence notes after source and final-wording review.

Does not edit shards or attest from mechanical success. The rows below are the
reviewer's individual premise, option and separate challenge assessments.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))
def write(p, value):
    (ROOT / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

library = read('audit/source-notes.json')
def source(key, url, locator, evidence, limitation='Institutional text inspected; no original film, audio or video playback claimed.', changing=False):
    library['sources']['b27-' + key] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt='2026-11-08', timeSensitive=changing,
        nextReviewAt='2027-02-05' if changing else None, limitations=limitation, topics=['Batch 27', key])

SS = 'https://www.springfieldspringfield.co.uk/movie_script.php?movie='
WIKI = 'https://en.wikipedia.org/wiki/'
source('corey','https://www.pixar.com/onward','The Manticore (Corey), lines 118-119',
       'Corey is the Manticore. Modern conveniences replaced magic and quests; she converted her tavern to a family restaurant.')
source('soul','https://www.pixar.com/soul','Synopsis; Joe Gardner; Moonwind; Counselors; Terry profiles',
       'Joe is a jazz pianist. Terry counts entrants to the Great Beyond and pursues the discrepancy. Counselors use Jerry; 22 is a new soul and Moonwind a living mystic.')
source('zone',SS+'soul','22 explains the zone, lines 682-694; Moonwind introduction 716-729',
       '22 explicitly calls the space between physical and spiritual the zone; musicians and other absorbed people enter it. Moonwind is met there.',
       'Third-party dialogue transcription; Pixar Moonwind profile corroborates the zone/astral-plane setting. No playback claimed.')
source('luca','https://www.pixar.com/luca','Massimo Marcovaldo profile; The World: Island',
       'Massimo is Giulia’s one-armed fisherman father. Alberto’s island hideout is a reclaimed, long-abandoned Roman tower with broken stairs.')
source('cup',SS+'luca','Giulia explains the triathlon, lines 957-960; race rules 1324-1330',
       'The three events are swimming, cycling and eating pasta; official rules require the bay, a bowl of pasta and a ride up Mount Portorosso and back.',
       'Third-party dialogue transcription; Disney Latino food article corroborates pasta and Vespa purchase as prize motivation; independent contemporary reviews corroborate the full triad.')
source('cup-food','https://www.disneylatino.com/novedades/luca-3-indicios-que-nos-permiten-descubrir-las-tradiciones-italianas-que-se-plasmaron-en-la-pelicula',
       'Gelato y pastas section; Vespa section', 'Pasta eating is a Cup event. Winning money would let the boys buy a Vespa; the scooter is their goal, not a race vehicle.')
source('cup-review','https://www.kinemalogue.net/2021/06/the-shadow-over-portorosso.html','Portorosso Cup plot paragraph',
       'The contemporary review lists swimming, cycling and pasta eating as the triathlon events.', 'Independent secondary film review corroborating the inspected dialogue.')
source('atlantis',SS+'atlantis-the-lost-empire','Milo’s proposal 67-78; Whitmore’s financing promise 369-391; crew briefing 417-437',
       'The Shepherd’s Journal gives Atlantis’s whereabouts. Preston Whitmore explicitly promised to finance the expedition if Thatch found it, and has arranged the crew.',
       'Third-party dialogue transcription, corroborated by detailed film plot and named cast; primary film playback unavailable.')
source('atlantis-plot',WIKI+'Atlantis:_The_Lost_Empire','Plot, Whitmore’s recruitment and journal; cast Rourke',
       'Millionaire Preston B. Whitmore recruits Milo, using the Shepherd’s Journal. Rourke is the expedition’s commander, not the financier.',
       'Secondary plot/cast corroboration of dialogue, not a primary film viewing.')
source('treasure',WIKI+'Treasure_Planet','Plot, galley assignment and black-hole incident; Voice cast Morph/Scroop',
       'Morph is Silver’s small shapeshifting pet. Scroop is the arachnid pirate who cuts Arrow’s lifeline; Hands is another crew member.',
       'Detailed secondary plot and cast inspected; Silver/Morph names corroborated by film dialogue. No original playback claimed.')
source('surfer',SS+'treasure-planet','Sarah and Doppler discuss Jim, lines 235-248; Silver/Morph cabin scene 1192-1226',
       'Sarah says Jim built his first solar surfer at eight. Silver addresses his pet as Morphy; Jim calls it Morph.',
       'Third-party film transcription, corroborated by film plot/cast for Morph; the solar-surfer term is explicit dialogue. No claim that Jim invented the device type.')
source('bear',WIKI+'Brother_Bear','Plot, Denahi misidentifies transformed Kenai; mountain resolution; cast brothers/moose',
       'Denahi mistakes Kenai’s bear form for his killer. Sitka restores Kenai’s humanity; Kenai chooses to become a bear again for Koda. Rutt and Tuke are moose.',
       'Secondary plot with ending dialogue corroboration; no original film playback.')
source('bear-end',SS+'brother-bear','Mountain resolution, lines 1274-1306',
       'After human restoration Kenai says Koda needs him. Denahi supports his choice; the narration says Kenai lived with Koda and the bears.',
       'Third-party film transcription corroborating the detailed plot, including temporary restoration before final choice.')
source('john',WIKI+'Robin_Hood_(1973_film)','Voice cast Prince John; Production, quoted Ken Anderson design account',
       'Prince John is a scrawny lion without a mane. The quoted production artist explains choosing a lion for John; Little John is a bear.',
       'Secondary cast account plus reproduced animator design testimony; primary film playback unavailable. These independently described roles corroborate the species assignment.')
source('jungle-profile','https://skgaleana.com/wp-content/uploads/2020/10/Meet-the-characters-feature-profiles-Jungle-Book.pdf',
       'Disney 2013 character profiles, printed KAA page / PDF page 6',
       'The Kaa profile repeatedly calls him a python but also calls him a boa constrictor once; all descriptions identify a snake.',
       'Disney-copyrighted promotional PDF on a third-party host. Its internal species contradiction prevents approving python versus boa; final question asks the uncontested broad animal type.')
source('jungle',WIKI+'The_Jungle_Book_(1967_film)','Plot, final Shere Khan fight; Voice cast Kaa',
       'Kaa is a snake. Shere Khan fears both guns and fire. Mowgli ties a burning branch to his tail during the climax and drives him away.',
       'Secondary detailed climax summary; Kaa’s broad type corroborated by Disney’s character PDF. The revised climax question does not assert fire is Khan’s only fear.')
source('bolt',WIKI+'Bolt_(2008_film)','Opening premise and Plot, director’s staging and eventual discovery',
       'Bolt believes the effects and powers on his show are real because the director conceals the staging. Later he discovers he is an ordinary dog.',
       'Secondary detailed plot; original film playback unavailable. Official theatrical synopsis independently corroborates initial superpower belief.')
source('bolt-primary','https://movies.disney.com/bolt','Theatrical synopsis, line 70',
       'Disney says Bolt thinks his Hollywood show is real and describes his supposed superpowers.')
source('raya','https://d23.com/meet-the-characters-of-raya-and-the-last-dragon/',
       'Raya; Sisu; Boun; Ongis; Tuk Tuk profiles, lines 65-103',
       'Druun are destructive spirits that petrify people. Tuk Tuk is Raya’s gigantic steed; Sisu is a dragon, Ongis con artists, and Boun a boat captain.')
source('rise','https://disneyworld.disney.go.com/attractions/hollywood-studios/star-wars-rise-of-the-resistance/',
       'Accept a Mission from the Resistance, lines 23-27',
       'A First Order Star Destroyer captures the guests’ transport and Resistance allies help them escape; the Star Destroyer itself is not captured.',changing=True)
source('remy','https://disneyworld.disney.go.com/attractions/epcot/remys-ratatouille-adventure/',
       'Opening and A Recipe for Excitement, lines 0-22',
       'Remy’s Ratatouille Adventure shrinks guests for a chase through Gusteau’s restaurant.',changing=True)
source('blizzard','https://disneyworld.disney.go.com/destinations/blizzard-beach/',
       'Opening melted-ski-resort description; attraction lists Summit Plummet and Chairlift',
       'Blizzard Beach has the melted ski-resort theme, Summit Plummet and Chairlift.',changing=True)
source('tiki','https://disneyland.disney.go.com/attractions/disneyland/enchanted-tiki-room/',
       'An Animation First, lines 30-34',
       'Disneyland’s Enchanted Tiki Room introduced Audio-Animatronics technology to the world in 1963.')
source('tiki-history','https://sites.disney.com/waltdisneyimagineering/our-story/',
       '1963, June timeline entry, lines 56-58',
       'Imagineering’s separate historical timeline dates the introduction of Audio-Animatronics at the Enchanted Tiki Room to June 1963.')
source('pooh','https://disneyworld.disney.go.com/attractions/magic-kingdom/many-adventures-of-winnie-the-pooh/',
       'Opening, lines 0-2; story scenes 24-30',
       'The Many Adventures of Winnie the Pooh takes Magic Kingdom guests through the Hundred Acre Wood in oversized Hunny Pots.',changing=True)
source('epcot-old',WIKI+'Epcot','Park layout, original Future World, lines 254-256',
       'World Celebration, World Discovery and World Nature were grouped as Future World. Innoventions was a smaller pavilion, not the whole half.',
       'Secondary historical layout corroborated against official four-neighborhood press description; no disputed exact completion date retained.')
source('epcot-new','https://disneyexperiences.com/disneyworld-press/release/historic-transformation-of-epcot-underway-at-walt-disney-world-resort/',
       'Opening four-neighborhood description and neighborhood headings',
       'The four neighborhoods are World Showcase, World Celebration, World Discovery and World Nature.')
source('table','https://disneyworld.disney.go.com/dining/magic-kingdom/cinderella-royal-table/',
       'Fairytale Dining; A Feast Fit for Royalty, lines 35-49',
       'Cinderella’s Royal Table offers character dining with princesses inside Cinderella Castle at breakfast, lunch and dinner.',changing=True)
source('frozen-history',WIKI+'Frozen_Ever_After','EPCOT infobox and History: June 21, 2016; replaced Maelstrom',
       'Frozen Ever After opened June 21, 2016 in EPCOT’s Norway pavilion, replacing Maelstrom.',
       'Secondary dated attraction record; the inspected official attraction page corroborates ride identity. An attempted opening-day blog route was inaccessible and is not claimed as inspected.')
source('walt-france','https://www.waltdisney.org/blog/over-there-walt-disneys-world-war-i-adventure',
       'Armistice, November 18 dispatch and December 4 arrival paragraphs',
       'Walt joined the Red Cross Ambulance Corps and was sent to France after the November 11, 1918 armistice.')
source('roy','https://www.waltdisney.org/blog/roy-disney-made-walt%E2%80%99s-dream-come-true-after-walt%E2%80%99s-passing',
       'Roy’s Walt Disney World construction and financing account; 1971 naming memo',
       'Roy O. Disney led financing and completion of his brother’s Florida dream and named the resort Walt Disney World.')
source('imagineers','https://sites.disney.com/waltdisneyimagineering/',
       'Inspiring Humanity, lines 20-21',
       'Imagineers are the creative professionals behind Disney’s designed worlds and attractions; the organization combines design, engineering, development and storytelling.')
source('alcoa','https://devfiuonline.fiu.edu/about-us/story-hub/fiu-online-news/stem-women-and-minorities-whats-the-big-deal.php',
       'Opening Imagineering origin paragraph',
       'The university account attributes Imagineering to Alcoa around 1940, preceding Disney’s use.',
       'Institutional secondary etymology, corroborated by reproduced 1942 Alcoa advertisement on Imagineering Ezine. Used to remove unsupported Walt-coined wording, not to introduce a new first-use claim.')
source('depth','https://www.waltdisney.org/multiplane-classroom-kit','Opening technology paragraph',
       'Photographing separate levels of artwork with a multiplane camera gives depth to two-dimensional animation; The Old Mill used it in 1937.')
source('snow-award','https://www.oscars.org/oscars/ceremonies/1939',
       'Memorable Moments: Walt Disney, lines 144-146',
       'Shirley Temple presented Disney one statuette and seven miniature statuettes for Snow White at the 1939 ceremony.')
source('snow-museum','https://www.waltdisney.org/blog/artifactual-cinderella-slipper',
       'Awards Lobby, second paragraph',
       'The museum describes the Snow White special award as one standard Oscar alongside seven miniature Oscars.')
source('encanto-lament',SS+'encanto','Mirabel’s private lament, lines 588-645; Isabela’s plant song 1747-1843; river flashback 1950-2056',
       'Waiting on a Miracle is Mirabel’s private lament; What Else Can I Do is Isabela’s new-plant song; Dos Oruguitas accompanies Alma’s river backstory after the collapse.',
       'Third-party film transcription; song/scene roles corroborated by saved b19-1019 and the Yatra interview account. No original playback claimed.')
source('yatra','https://ktvz.com/entertainment/cnn-entertainment/2022/02/24/sebastian-yatra-singer-of-dos-oruguitas-explains-why-encanto-moved-him-to-tears/',
       'Song/flashback description and interview',
       'Yatra’s Dos Oruguitas accompanies the flashback to Alma’s life with Pedro.',
       'CNN interview report independently corroborating the scene; original film playback unavailable.')
source('up-score','https://michaelgiacchino.com/projects/up/',
       'Up (2009), Married Life track list and What Michael Says, lines 27-43',
       'Giacchino describes composing the Married Life sequence and Ellie’s theme.')
source('up-oscar','https://www.oscars.org/oscars/ceremonies/2010',
       'Music (Original Score), winner, lines 609-615',
       'Michael Giacchino won Original Score for Up at the 2010 Academy Awards.')
source('coco-oscar','https://www.oscars.org/oscars/ceremonies/2018',
       'Music (Original Song), winner, lines 597-603',
       'Remember Me from Coco won; music and lyric are credited to Kristen Anderson-Lopez and Robert Lopez.')
source('lantern',SS+'tangled','Boat and lantern duet, lines 1131-1204',
       'Rapunzel and Flynn sing I See the Light together during the lantern boat scene.',
       'Third-party dialogue transcription; composer catalog and saved b19-1015 independently identify the track and other scene assignments.')
source('ray',SS+'the-princess-and-the-frog','Evangeline evening-star scene, lines 1496-1545; Facilier’s number 467-554',
       'Ray sings Ma Belle Evangeline to the star. Friends on the Other Side is Facilier’s number; Almost There belongs to Tiana’s restaurant dream.',
       'Third-party transcription corroborated by saved song/scene note b19-1014 and original soundtrack metadata. No playback claimed.')
source('frog-track','https://music.apple.com/us/song/ma-belle-evangeline-feat-terence-blanchard/1417397893',
       'Song title, Jim Cummings performer and original-motion-picture soundtrack attribution',
       'The track is titled Ma Belle Evangeline, performed by Jim Cummings, on the 2009 Princess and the Frog soundtrack.',
       'Label-distributed original soundtrack metadata; no audio playback claimed.')
source('frog-album','https://music.apple.com/us/album/the-princess-and-the-frog-original/1417397114',
       'Original soundtrack heading, opening editorial track descriptions and Walt Disney Records copyright',
       'The original album attributes Friends on the Other Side to Keith David and Almost There to Anika Noni Rose.',
       'Label-distributed original soundtrack metadata, with film dialogue establishing the characters and scenes.')
source('lookout','https://disneyparksblog.com/dcl/first-look-at-disney-lookout-cay-at-lighthouse-point/',
       'June 7, 2024, first paragraph',
       'Disney Lookout Cay at Lighthouse Point on Eleuthera welcomed preview guests in June 2024; it is a destination on Eleuthera, not a separate private island.')
source('midship','https://disneycruise.disney.go.com/en-sg/onboard-activities/midship-detective-agency/',
       'Title, ship locations and enchanted-art game-card descriptions, lines 0-27',
       'Midship Detective Agency is an interactive mystery caper aboard Dream and Fantasy using clues from enchanted art.',changing=True)
source('lotso','https://www.pixar.com/toy-story-3','Lotso, Big Baby and Ken character profiles',
       'Lotso is the strawberry-scented plush bear; Big Baby is a baby doll and Ken a fashion doll.')
source('lotso-plot',WIKI+'Toy_Story_3','Plot, Sunnyside assignment, Buzz reset and prison hierarchy',
       'Lotso rules Sunnyside, keeps newcomers with destructive toddlers and uses Big Baby and the monitoring monkey to enforce his control. Ken is an ally, not the ruler.',
       'Secondary plot identifies command roles; Pixar independently corroborates toy identities. No original film playback.')
source('hall',WIKI+'One_Hundred_and_One_Dalmatians','Plot, Colonel and Tibbs investigate Hell Hall, line 268',
       'Hell Hall is Cruella’s Suffolk manor where the Baduns keep the stolen puppies.',
       'Detailed secondary plot and saved b16-858 passage. D23 place entry and attempted 1961 transcription could not be accessed; no claim of primary playback. The Take’s independent film criticism corroborates the named manor.')
source('hall-critic','https://the-take.com/watch/the-evolution-of-cruella-from-spinster-villain-to-punk-icon',
       'Transcript, Cruella 1.0: The Pure Evil Spinster, lines 53-55',
       'The account of the 1961 film explicitly identifies Cruella’s manor as Hell Hall.',
       'Independent secondary film criticism; used for the place name only, not its social interpretations.')
source('renaissance',WIKI+'Disney_Renaissance','Lead and Timeline: 1989 The Little Mermaid, lines 151-154',
       'The standard Disney Renaissance period begins in 1989 with The Little Mermaid. Beauty and the Beast is 1991, Aladdin 1992, and Oliver & Company a 1988 precursor.',
       'Secondary historical periodization, with release chronology independently checked against the studio catalog saved as b26-order.')

rows = {}
def row(i, sources, premise, reasons, challenge, context):
    assert len(reasons) == 4
    rows[i] = (sources.split(), premise, reasons, challenge, context)

row(1435,'b27-corey','Pixar names the restaurant-owning Manticore Corey.',[
    'Corey is the named Manticore.','Lyria is a different name, not the named proprietor.','Blaze does not match her established name.','Fiara does not match her established name.'],
    'Rechecked whether restaurant and warrior refer to different characters: Pixar explicitly identifies the same Corey in both roles. Other names are not aliases.', 'Onward (2020), Manticore’s restaurant.')
row(1436,'b27-corey','Pixar explains that modern conveniences replaced magic and questing.',[
    'Convenient technology displaced difficult magic.','A legal ban is not the stated replacement mechanism.','A knowledge-erasing curse conflicts with surviving spells and Corey’s history.','Underground sealing is not the described social change.'],
    'Magic remains usable; loss of everyday use is different from its eradication. The final question asks the reason for that change, not why a specific spell failed.', 'Onward’s modernization premise.')
row(1437,'b27-soul b25-dorothea','Joe is the auditioning pianist; Dorothea plays saxophone and Curley drums.',[
    'Joe auditions at the piano.','Trumpet is not Joe’s audition instrument.','Saxophone belongs to Dorothea at this audition.','Drums belong to Curley in her band.'],
    'Restricted to the audition so a music teacher’s ability to demonstrate other instruments cannot create a second answer.', 'Soul (2020), Dorothea Williams audition.')
row(1438,'b27-zone b27-soul','22 names the space the zone and Moonwind is encountered there.',[
    'The Zone is the explicit term.','Flow describes absorption but is not the named space.','The Ether is not 22’s term.','The Great Between is not 22’s term.'],
    'Pixar also uses Astral Plane for this broader setting, but that is not a listed distractor. The film dialogue directly calls the specified space the zone.', 'Soul, 22 and Joe’s visit to Moonwind.')
row(1439,'b27-soul','Pixar assigns the soul-count discrepancy to Terry.',[
    'Terry is responsible for the count.','Jerry names the counselors, not the counter.','22 is the soul Joe mentors.','Moonwind is a living mystic who helps Joe.'],
    'Checked Terry versus Jerry despite the similar names. The earlier counselor-name question #1042 concerns a distinct role, not the same identity.', 'Soul, count discrepancy after Joe’s detour.')
row(1440,'b27-cup b27-cup-food b27-cup-review','Giulia’s complete event list establishes all three components.',[
    'Swimming, pasta and cycling are the three events.','Running replaces pasta in this conventional triathlon list.','Rowing and running replace two of the required events.','Pizza replaces the required pasta.'],
    'Tested partial overlap in every list. A Vespa is the hoped-for purchase, not the vehicle ridden in the race. Race name #1043 tests a different fact.', 'Luca (2021), Portorosso Cup rules.')
row(1441,'b27-luca','Pixar’s Island section identifies the abandoned Roman tower.',[
    'The reclaimed Roman tower is Alberto’s hideout.','A harbor cave is a different structure.','A sunken boat is underwater, unlike the tower.','A beach shack is not the described structure.'],
    'Removed the unsupported lighthouse designation. #1564 asks why Alberto lives alone, not the structure’s identity.', 'Luca, Alberto’s island home at first meeting.')
row(1442,'b27-luca','Pixar directly identifies Giulia’s father as Massimo.',[
    'Massimo is Giulia’s fisherman father.','Ercole is the town bully, not her father.','Marco is not the character’s name; actor Marco Barricelli is different.','Stefano is not her father’s name.'],
    'Distinguished the character from voice actor Marco Barricelli; Ercole’s separate bully identity cannot satisfy the father relationship.', 'Luca, Giulia Marcovaldo’s family.')
row(1443,'b27-atlantis b27-atlantis-plot','Whitmore explicitly promises to finance the expedition and supplies the crew.',[
    'Preston B. Whitmore is the financier.','Rourke commands the expedition rather than underwriting it.','Cornelius Aldrich is not the named financier.','Bennett Calloway is not the named financier.'],
    'Command and financing are separate roles. The exact financing promise supports the premise, beyond the generic description of a wealthy friend.', 'Atlantis: The Lost Empire (2001), Whitmore’s recruitment.')
row(1444,'b27-atlantis b27-atlantis-plot','Milo describes the Shepherd’s Journal as the route source.',[
    'The Shepherd’s Journal contains the whereabouts.','Atlantean Codex is not this artifact’s title.','Book of Kida is not this artifact’s title.','Lost Meridian is not this artifact’s title.'],
    'Kida’s royal identity and the power crystal are different facts. Confirmed the journal directs the expedition rather than merely recording unrelated lore.', 'Atlantis (2001), expedition route text.')
row(1445,'b27-treasure b27-surfer','Silver’s shapeshifting companion is named Morph.',[
    'Morph is the named shapeshifting pet.','Splat is not Silver’s pet’s name.','Glop is not Silver’s pet’s name.','Blobby is not Silver’s pet’s name.'],
    'A descriptive blob nickname is not an alternative proper name. The map sphere in #835 and B.E.N. in #875 are separate objects/characters.', 'Treasure Planet (2002), Silver’s galley companion.')
row(1446,'b27-surfer','Sarah explicitly calls Jim’s board a solar surfer.',[
    'Solar surfer is the device’s name.','Comet board is not the named board.','Gravity glider is not the named board.','Rocket board is not the named board.'],
    'Building a device does not establish inventing the technology; final wording asks what he rides and avoids that claim.', 'Treasure Planet, Jim’s early solar-surfing activity.')
row(1447,'b27-treasure','The black-hole incident identifies Scroop as the lifeline cutter.',[
    'Scroop cuts Mr. Arrow’s line.','Hands is a different crew member.','Grinder is not the identified attacker.','Slaughter is not the identified attacker.'],
    'Replaced subjective most-dangerous ranking with a concrete action, and checked Jim’s apparent guilt against the actual perpetrator.', 'Treasure Planet, black-hole encounter.')
row(1448,'b27-bear','Denahi misreads Kenai’s transformation as his death.',[
    'Denahi hunts the transformed Kenai.','Sitka has already died and is the transforming spirit.','Tuke is a moose, not Kenai’s human brother.','Rutt is a moose, not Kenai’s human brother.'],
    'The original conflated Sitka’s death with Denahi’s belief about Kenai. Final wording specifies the latter and leaves the two moose excluded.', 'Brother Bear (2003), Denahi’s pursuit.')
row(1449,'b27-bear b27-bear-end','The ending restores humanity briefly before Kenai chooses bear life.',[
    'Kenai returns to bear form to care for Koda.','He does not remain human to rule the tribe.','He does not leave life to become Sitka’s fellow spirit.','Koda is not transformed into a human.'],
    'Temporary human restoration cannot make the human-life option correct: the question expressly asks his subsequent final choice.', 'Brother Bear, mountain resolution and ending narration.')
row(1453,'b27-john','Prince John’s species is explicitly described and explained by the character designer.',[
    'Prince John is a lion.','Little John, not Prince John, is a bear.','A wolf is not Prince John’s species.','A weasel is not Prince John’s species.'],
    'A missing mane does not change the species. Mayor Lionheart #2653 is another character in another film, requiring an independent animal identity.', 'Robin Hood (1973), Prince John design.')
row(1458,'b27-jungle-profile b27-jungle','All inspected descriptions agree Kaa is a snake.',[
    'Kaa is a snake.','He is not a crocodile.','He is not a lizard.','He is not a turtle.'],
    'Disney’s PDF inconsistently uses python and boa constrictor. The final broad-type question removes that disputed distinction and excludes all three other reptiles.', 'Disney’s animated The Jungle Book (1967), Kaa.')
row(1459,'b27-jungle','The bounded final fight ends with a burning branch tied to the tiger’s tail.',[
    'The burning branch uses fire to drive him away.','Water is not the repelling weapon in this fight.','Drums are not the repelling weapon in this fight.','A hunter’s trap is not used to drive him away.'],
    'Khan also fears guns, so only-fear wording was false. The final scene-specific question excludes guns and the three listed alternatives by the actual action.', 'The Jungle Book (1967), final Shere Khan fight.')
row(1464,'b27-bolt b27-bolt-primary','The concealed staging leads Bolt to mistake fictional abilities for real powers.',[
    'Bolt believes his powers are real.','He does not understand them as a remote-controlled trick.','He does not believe they require recording cameras.','Special effects are the actual explanation, not his initial belief.'],
    'The original also allowed belief that Penny was in danger. All final options concern the abilities, and start-of-film timing avoids his later realization. This is theatrical-film trivia about an in-universe show.', 'Bolt (2008), initial belief before leaving the set.')
row(1465,'b27-raya','Disney’s Tuk Tuk profile identifies Raya’s gigantic steed.',[
    'Tuk Tuk is Raya’s mount.','Sisu is the dragon they seek.','Ongis are the small con artists who accompany Noi.','Boun is a human boat captain.'],
    'Armadillo-like is visual comparison, not a pure-species assertion. The separate roles exclude all three names without assuming none ever travels with Raya.', 'Raya and the Last Dragon (2021), Raya’s steed.')
row(1466,'b27-raya','The Raya profile names the petrifying destructive spirits Druun.',[
    'The Druun are the named spirits.','Mist Spirits is not their proper name.','Stone Shadows is not their proper name.','Kakamora are not the named Kumandra spirits.'],
    'Final wording asks the proper name, so a descriptive phrase such as mist spirits cannot become a second answer.', 'Raya and the Last Dragon, petrification threat.')
row(1467,'b27-rise','The official ride story has a captured transport and Resistance-assisted escape.',[
    'Rise of the Resistance has this storyline.','Smugglers Run is the Falcon flight experience, not this named escape.','Star Tours is not the attraction described in this official story.','Force Encounter is not the named ride.'],
    'Corrected which vessel is captured. Separate questions cover Galaxy’s Edge, Falcon roles, ride technology and opening year; none establishes this particular plot/name association.', 'Hollywood Studios attraction as of November 2026.')
row(1468,'b27-remy','The attraction page names the rat-size Gusteau’s chase.',[
    'Remy’s Ratatouille Adventure is the official title.','Remy’s Kitchen Chase is not the official title.','Gusteau’s Little Adventure is not the official title.','Rat Race Paris is not the official title.'],
    'Removed the film title from the stem. #2220 asks trackless technology and #2256 another park’s version, not this EPCOT attraction title.', 'EPCOT attraction as of November 2026.')
row(1474,'b27-blizzard','The official page combines the ski-resort theme with both named attractions.',[
    'Blizzard Beach has all these features.','Typhoon Lagoon uses a different storm setting.','River Country is not the ski-themed park.','Snow Peak is not the park’s name.'],
    'Mount Gushmore #1157 is a mountain name, not this water park’s identity; Typhoon Lagoon #775 asks the other park’s distinct theme.', 'Walt Disney World water park as of November 2026.')
row(1475,'b27-tiki b27-tiki-history','Disney explicitly dates the public Audio-Animatronics introduction to the Tiki Room in 1963.',[
    'The Enchanted Tiki Room is the documented introduction.','Jungle Cruise is not the attraction named in this 1963 technology debut.','Indiana Jones Adventure is not the 1963 debut.','Swiss Family Treehouse is not the documented debut.'],
    'Removed singing-birds clues so #910 cannot solve this historical technology question merely by recognizing the musical attraction.', 'Disneyland, original 1963 technology debut.')
row(1479,'b27-pooh','The Magic Kingdom attraction page names the Hunny Pot journey.',[
    'The Many Adventures of Winnie the Pooh is the Magic Kingdom ride.','Winnie the Pooh and Friends is not this title.','Pooh’s Honey Hunt is not the Magic Kingdom attraction.','Hundred Acre Coaster is not this title.'],
    'Tokyo’s trackless ride #2643/#2644 is a distinct version; the explicit Magic Kingdom location prevents Honey Hunt also fitting.', 'Magic Kingdom attraction as of November 2026.')
row(1482,'b27-epcot-old b27-epcot-new','The old layout grouped the three present neighborhoods under Future World.',[
    'Future World named the whole half.','Innoventions was a smaller pavilion within it.','Tomorrow’s World was not the area’s name.','Vision Center was not the area’s name.'],
    'Separated the half-park name from a pavilion and removed misleading implication that all physical redesign occurred in one year.', 'EPCOT historical layout before the four-neighborhood arrangement.')
row(1485,'b27-table','The named restaurant offers princess dining inside the castle.',[
    'Cinderella’s Royal Table is the restaurant.','Bibbidi Bobbidi Boutique is not this dining restaurant.','Princess Banquet is not this official title.','Royal Family Table is not this official title.'],
    'Removed Cinderella from the stem to avoid title echo. Current character appearances can change, so the dated offering has a scheduled recheck.', 'Magic Kingdom dining as of November 2026.')
row(1486,'b27-frozen-history','The EPCOT opening record places Frozen Ever After in Maelstrom’s site in 2016.',[
    'Frozen Ever After replaced Maelstrom in 2016.','Gran Fiesta Tour is a different pavilion’s ride.','Na’vi River Journey is not in Norway or this replacement.','Living with the Land is not the Norway replacement.'],
    'The original phrasing could invite Maelstrom as the ride that was reimagined. Final wording asks what opened afterward, with four distinct attraction names.', 'EPCOT Norway pavilion, 2016 opening event.')
row(1487,'b27-walt-france','The museum dates Walt’s Red Cross dispatch after the armistice.',[
    'Red Cross ambulance driving brought him to France.','Aircraft construction was not the documented volunteer service.','Army Signal Corps service was not his organization.','Cavalry horse training was not the documented service.'],
    'Post-armistice timing corrects the implication of wartime driving in France. Removed poster drawing as a distractor because he did draw during the service.', 'Walt’s 1918-1919 Red Cross service in France.')
row(1490,'b27-roy disney-family roy-death','The museum attributes completion of the Florida project to Roy O. Disney.',[
    'Roy O., Walt’s older brother, led completion.','Roy E. was the nephew, not the project leader.','Lillian was Walt’s wife, not the leader of this completion.','Diane was Walt’s daughter, not the project leader.'],
    'Avoided saying Roy first took over the company in 1966, since he had long held leadership. Resort completion is separate from his death year and later naming lore.', 'Walt Disney World completion and 1971 opening.')
row(1494,'b27-imagineers b27-alcoa','Disney’s own organization calls its designers Imagineers.',[
    'Imagineers is Disney’s established name.','Theme Builders is not that formal name.','Dream Makers is not that formal name.','Park Designers is a description rather than that formal name.'],
    'Removed unsupported claim that Walt coined the word. Final question tests Disney terminology without introducing a contested first-use date.', 'Disney theme-park design profession terminology.')
row(1495,'b27-depth','The museum explains the depth effect of separately photographed artwork levels.',[
    'Separate layers create apparent depth.','The camera does not turn monochrome artwork into color.','It does not automatically synchronize mouth shapes.','Tracing actors describes rotoscoping, not multiplane photography.'],
    'All four are parallel effects/processes. No first-ever-camera claim remains; #405 tests rotoscoping itself, a different technique.', 'Traditional Disney multiplane animation technique.')
row(1496,'b27-snow-award b27-snow-museum','Academy and museum agree on one standard statuette plus seven miniatures.',[
    'One full-size and seven miniature statuettes matches both records.','Three miniatures is the wrong count.','Seven full-size statuettes reverses the sizes.','Three full-size and one miniature matches neither count.'],
    'Independently corroborated the exact quantities and sizes. Shortened stem to avoid the Seven Dwarfs title hint; the 1939 ceremony is distinct from 1937 film release.', '1939 special Academy Award for Snow White.')
row(1497,'b27-encanto-lament b19-1019','Mirabel’s private lament is Waiting on a Miracle.',[
    'Waiting on a Miracle is the solo lament.','Family Madrigal is the opening family introduction.','What Else Can I Do is Isabela’s plant-discovery number.','Dos Oruguitas accompanies Alma’s backstory.'],
    'Removed the claim that Mirabel is the only ungifted Madrigal; in-laws also lack powers. The song scene, not universal family status, determines the answer.', 'Encanto (2021), Mirabel’s post-ceremony private lament.')
row(1498,'b27-encanto-lament b19-1019','Isabela’s new-plant number is What Else Can I Do.',[
    'What Else Can I Do is Isabela’s number.','Waiting on a Miracle is Mirabel’s lament.','Surface Pressure concerns Luisa.','All of You is the rebuilding finale.'],
    'Mirabel joins Isabela, but that does not make Mirabel’s separate solo correct. Each option names a different bounded number.', 'Encanto, Isabela’s plant-discovery scene.')
row(1499,'b27-encanto-lament b27-yatra b19-1019','Dos Oruguitas accompanies Alma and Pedro’s backstory.',[
    'Dos Oruguitas is the flashback song.','Colombia, Mi Encanto is the celebration number.','Surface Pressure is Luisa’s burden number.','All of You accompanies rebuilding.'],
    'Corrected collapse timing: the river flashback follows Casita’s fall. The scene and Spanish-language wording exclude the three other numbers.', 'Encanto, Alma/Pedro river flashback.')
row(1502,'b27-up-score b27-up-oscar','Giacchino’s own composition account and Academy credit agree.',[
    'Michael Giacchino composed the score and Married Life.','Hans Zimmer is not the credited Up composer.','Alan Menken is not the credited Up composer.','John Williams is not the credited Up composer.'],
    'Checked film-score authorship rather than a later performer/arranger; his Zootopia credit #1269 does not independently answer who scored Up.', 'Up (2009), original orchestral score.')
row(1504,'b27-coco-oscar','The Academy identifies the Lopez team’s winning song in Coco.',[
    'Coco features their Oscar-winning Remember Me.','Inside Out is not the film credited for that song.','Soul is not the film credited for that song.','Onward is not the film credited for that song.'],
    'A composer’s involvement elsewhere does not satisfy the precise Oscar-winning original-song condition; the award record assigns this song to Coco.', 'Original song award for Coco, following Frozen.')
row(1509,'b27-lantern b19-1015 b13-tangledcatalog','The lantern duet is I See the Light.',[
    'I See the Light is the boat duet.','When Will My Life Begin is Rapunzel’s routine song.','I’ve Got a Dream is the tavern ensemble.','Something That I Want is not the specified duet.'],
    'Separated lantern subject #842 from the duet title. Other songs express dreams but do not occupy this bounded boat scene.', 'Tangled (2010), lantern boat duet.')
row(1510,'b27-ray b27-frog-track b19-1014','Ray sings Ma Belle Evangeline while addressing the star.',[
    'Ma Belle Evangeline is the named ballad.','Almost There is Tiana’s restaurant number.','Friends on the Other Side is Facilier’s number.','Ray’s Song is not the established track title.'],
    'Ray’s relationship to the star #245 is different from naming this number. A descriptive Ray’s Song label cannot replace the actual soundtrack title.', 'The Princess and the Frog (2009), Ray’s evening-star ballad.')
row(1511,'b27-ray b27-frog-album b19-1014','The exact number appears in The Princess and the Frog.',[
    'The Princess and the Frog contains this number.','Moana is not its originating film.','Encanto is not its originating film.','Coco is not its originating film.'],
    'Removed Dr. Facilier from the stem so memorizing #27’s villain name no longer solves the question; the actual song/film attribution is required.', 'Original theatrical song attribution.')
row(1512,'b27-lookout','The dated Disney announcement names Lookout Cay on Eleuthera.',[
    'Disney Lookout Cay opened on Eleuthera in 2024.','Castaway Cay is the older destination on a different island.','Discovery Island is not this Bahamian cruise destination.','River Country is not this Bahamian cruise destination.'],
    'Used the destination’s proper name, rather than Lighthouse Point alone, and distinguished a destination on an island from a whole private island. #147 asks the preview date, a separate fact.', 'Disney Lookout Cay’s historical 2024 opening.')
row(1517,'b27-midship','DCL names the enchanted-art mystery game on Dream and Fantasy.',[
    'Midship Detective Agency is the advertised game.','Cruise Case Files is not the advertised title.','Villain Hunt is not the advertised title.','The Magic Mystery is not the advertised title.'],
    'Avoided calling the game card a generic electronic device and avoided implying every case involves Disney villains; Muppet cases also exist.', 'Dream/Fantasy offering as of November 2026.')
row(1530,'b27-lotso b27-lotso-plot','Lotso controls Sunnyside’s harsh hierarchy; others carry out subordinate roles.',[
    'Lots-o’-Huggin’ Bear, or Lotso, is the ruler.','Big Baby is his enforcer, not the ruler.','Ken cooperates but does not control assignment policy.','The Monkey monitors security rather than directing the system.'],
    'Removed teddy-bear words that revealed the only Bear answer. Helpers’ participation in enforcement does not make them the authority who assigns arrivals.', 'Toy Story 3 (2010), Sunnyside hierarchy.')
row(1535,'b27-hall b27-hall-critic','The stolen puppies are held at Hell Hall in Suffolk.',[
    'Hell Hall is the named captive-puppy location.','Toad Hall belongs to another Disney story.','Devil’s Bayou is not this English house.','Sleepy Hollow is not this English house.'],
    'Specified 1961 animation, excluded loosely descriptive De Vil Estate alias, and separated naming the location from #858’s rescue-cat identity.', '101 Dalmatians (1961), country-house captivity.')
row(1537,'b27-renaissance b26-order','The standard Renaissance timeline starts with the 1989 Little Mermaid.',[
    'The Little Mermaid is the 1989 starting film.','Beauty and the Beast came in 1991.','Aladdin came in 1992.','Oliver & Company came in 1988 and is a precursor.'],
    'Some histories include precursors, but explicit 1989 wording and verified release chronology exclude Oliver. The Under the Sea award #158 and preceding-feature #1389 test other facts.', 'Conventional Disney Renaissance periodization and theatrical years.')

notes = read('audit/runs/next-shard-0027-reviewed-notes.json')
assert {r['questionId'] for r in notes['reviews']} == set(rows)
checked = set()
for review in notes['reviews']:
    i = review['questionId']
    sources, premise, reasons, challenge, context = rows[i]
    checked.update(sources)
    changing = any(library['sources'][s]['timeSensitive'] for s in sources)
    review.update(checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],
                  notes='Codex read final stem and all four options; complete packet topic catalog and additional cross-shard matches reviewed. ' + challenge,
                  context=context, timeSensitive=changing, nextReviewAt='2027-02-05' if changing else None,
                  premise=dict(reason=premise,sources=sources))
    review['options'] = [dict(basis='direct' if n == 0 else 'exclusive-inference',reason=reason,sources=sources)
                         for n,reason in enumerate(reasons)]
    review['challenge'] = dict(reviewer='Codex',at='2026-11-08',premiseChecked=True,
                               alternativesExcluded=True,notes=challenge)
notes['sourcesChecked'] = sorted(checked)
write('audit/source-notes.json',library)
write('audit/runs/next-shard-0027-reviewed-notes.json',notes)
print(f'Authored {len(rows)} explicit final-wording reviews; no ledger import performed.')
