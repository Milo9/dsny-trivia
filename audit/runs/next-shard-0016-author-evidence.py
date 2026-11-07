"""Expand the explicit passage assessments below; never edit question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Question, inspected source, exact locator, premise, three exclusions, final challenge.
DATA = [
(852,'Pinocchio_(1940_film)','Plot: departure from Stromboli show and bird-cage imprisonment',
 'Stromboli imprisons Pinocchio in his wagon when the puppet wants to go home.',
 ['The Coachman organizes Pleasure Island, not this puppet show.','Honest John recruits Pinocchio for Stromboli; he is not the imprisoning showman.','Lampwick is a boy met on the later island journey.'],
 'The Coachman also confines transformed boys, so the final wording specifies the puppet master and original film; the cage incident identifies Stromboli.'),
(853,'Alice_in_Wonderland_(1951_film)','Voice cast: Sterling Holloway as the Cheshire Cat; other Wonderland roles',
 'The Cheshire Cat is described as a pink-and-purple-striped cat with a permanent grin.',
 ['The White Rabbit is a waistcoated rabbit and royal herald.','The Mad Hatter is the human tea-party host.','The Caterpillar is a hookah-smoking caterpillar, not the striped cat.'],
 'The original broad disappearing ability risks confusing magical effects and the Caterpillar\'s transformation. Final wording asks a concrete combined visual identity; none of the three other characters is that cat.'),
(854,'Peter_Pan_(1953_film)','Opening Darling nursery scene and Voice cast: George, John and Michael',
 'George Darling is Wendy\'s father; Mary is her mother, and John and Michael are her brothers.',
 ['John is Wendy\'s brother.','Michael is Wendy\'s youngest brother.','Edward is not the father\'s name in this family identification.'],
 'The mother question #1104 tests Mary, a separate parent. Do not confuse the Edwardian setting with an Edward Darling; the opening dialogue names George.'),
(855,'Lady_and_the_Tramp','Plot opening and Voice cast: Lady, Jock, Trusty and Tramp',
 'Lady is a cocker spaniel in the original 1955 animated film.',
 ['Scottish terrier identifies Jock, not Lady.','Bloodhound identifies Trusty, not Lady.','A schnauzer is not Lady\'s established breed.'],
 'Read #856 and #2480 too: Lady\'s breed, Tramp\'s mixed ancestry and Jock\'s breed are different character facts. Specified 1955 rather than reasoning from live-action casting.'),
(856,'Lady_and_the_Tramp','Lead, Plot opening and Voice cast: Tramp as mongrel',
 'Tramp is a mixed-breed street dog, described as a mutt or mongrel.',
 ['A dalmatian is a specific breed, not his mixed-breed classification.','A bulldog is not the classification given for Tramp.','A poodle is not the classification given for Tramp.'],
 'The question asks the animated dog\'s classification, not the breed of a live-action animal performer. Possible terrier or schnauzer ancestry does not make any listed pure breed correct.'),
(857,'Sleeping_Beauty_(1959_film)','Good-fairy cast descriptions; cottage dress color argument',
 'Merryweather argues for blue; Flora insists on pink, Fauna handles the cake, and Maleficent is the hostile fairy.',
 ['Flora argues for pink in this dispute.','Fauna is the peacemaker and cake maker, not the blue advocate.','Maleficent is absent from the cottage dress dispute.'],
 'Removed good fairy from the stem so Maleficent is not grammatically disqualified. The question asks who advocates blue, not whether Aurora\'s dress is ever blue or pink; both colors appear.'),
(858,'One_Hundred_and_One_Dalmatians','Plot: Colonel and Sergeant Tibbs discover and evacuate Hell Hall; Voice cast',
 'Sergeant Tibbs is the barn cat who discovers the captive puppies and helps them escape Hell Hall.',
 ['Figaro is not the named cat assisting this rescue.','Lucifer is not the named cat assisting this rescue.','Thomas O\'Malley is not the named cat assisting this rescue.'],
 'All options are cats, so species alone does not solve it. The identified rescuer is Tibbs; #1535 asks the estate name rather than the cat.'),
(859,'Robin_Hood_(1973_film)','Voice cast and Ken Anderson character-design account',
 'Little John is a brown bear; Robin Hood is a fox, Friar Tuck a badger, and Prince John a lion.',
 ['A fox describes Robin Hood, not Little John.','A badger describes Friar Tuck, not Little John.','A lion describes Prince John, not Little John.'],
 'Read #1594 and #510: animal casting for different characters is not one reversible fact. The character-design account explicitly separates all four species.'),
(860,'Piglet_(Winnie-the-Pooh)','Lead and species infobox; Disney interpretation section',
 'Piglet is Pooh\'s small, timid pig friend.',
 ['Roo is the young kangaroo, not the pig.','Rabbit is the rabbit, not the pig.','Gopher is the burrowing gopher, not the pig.'],
 'Close friendship could include all four, but the conjunction with pig selects Piglet. This is established theatrical Pooh character coverage, not TV-episode trivia.'),
(861,'The_Rescuers','Plot, Orville cast entry and sequel discussion',
 'Orville is the albatross who flies Bernard and Bianca to Devil\'s Bayou in the original film.',
 ['Wilbur is the albatross in the Australian sequel.','Evinrude propels their leaf boat as a dragonfly.','Dinky is not the albatross identified for this flight.'],
 'Separated the original flight from the sequel and the later swamp boat journey. The original dialogue names Orville and Devil\'s Bayou, excluding the other transport helper.'),
(862,'The_Fox_and_the_Hound','Opening Plot and Big Mama cast entry',
 'Big Mama is the owl who arranges Tod\'s adoption and later advises him.',
 ['Friend Owl is not the owl identified in this story.','Mama Odie is not the owl identified in this story.','Archimedes is not the owl identified in this story.'],
 'Widow Tweed actually adopts and raises Tod; Big Mama helps arrange it. The phrase helps raise does not claim the owl is the adoptive human owner asked about in #1113.'),
(863,'The_Black_Cauldron_(film)','Plot opening and cast; Taran\'s farm and dungeon self-identification',
 'Taran is the young assistant pig-keeper under Dallben.',
 ['Fflewddur Fflam is the bard.','Gurgi is the small creature accompanying Taran.','Dallben is Taran\'s elderly guardian and enchanter.'],
 'Taran repeatedly identifies his occupation; Dallben owns Hen Wen but is not the young assistant. #2479 tests voice actor Grant Bardsley, an additional production fact rather than the same answer.'),
(864,'The_Great_Mouse_Detective','Plot opening: Dawson meets Olivia; ending: investigative partnership',
 'David Q. Dawson is the retired army surgeon who becomes Basil\'s investigative partner.',
 ['Hiram Flaversham is Olivia\'s toymaker father.','Professor Ratigan is Basil\'s criminal adversary.','Delbert Doppler is not the surgeon partnered with Basil.'],
 'Removed invented Dr. titles from Flaversham and Ratigan. Flaversham accompanies the final pursuit, but is a toymaker rather than the doctor, so the conjunction still selects Dawson.'),
(865,'Oliver_%26_Company','Plot barge introduction and Voice cast: all four gang dogs',
 'Tito is the chihuahua; Dodger is a terrier, Francis a bulldog and Einstein a Great Dane.',
 ['Dodger is the terrier, not the chihuahua.','Francis is the bulldog, not the chihuahua.','Einstein is the Great Dane, not the chihuahua.'],
 'All four are gang members, so membership is not the discriminator. The source names the four different breeds; no competing gang member also fits chihuahua.'),
(866,'The_Little_Mermaid_(1989_film)','Voice cast: Chef Louis; palace kitchen pursuit',
 'Louis is Eric\'s cook who tries to prepare Sebastian as food.',
 ['Grimsby is Eric\'s adviser, not the pursuing cook.','Carlotta is the household maid, not the pursuing cook.','Max is Eric\'s dog, not the pursuing cook.'],
 'Removed the Chef title from the correct option, which alone previously repeated the stem\'s profession. The 1989 kitchen pursuit, not a remake or household job in general, fixes Louis.'),
(867,'The_Lion_King','Plot elephant-graveyard rescue and Voice cast: Zazu, Rafiki, Timon and Banzai',
 'Zazu is Mufasa\'s hornbill majordomo.',
 ['Rafiki is the mandrill shaman.','Timon is a meerkat.','Banzai is a spotted hyena.'],
 'Rafiki also advises the royal family, but the hornbill and majordomo conjunction excludes him. The other two named animals are not birds or palace officials.'),
(868,'Pocahontas_(1995_film)','Plot opening, Nakoma warning Kocoum, and cast descriptions',
 'Chief Powhatan wants Pocahontas to marry the warrior Kocoum.',
 ['Nakoma is Pocahontas\'s friend, not this prospective husband.','Thomas is the English settler who later shoots Kocoum.','Powhatan is Pocahontas\'s father, not her prospective husband.'],
 'This asks the Disney film\'s intended match, not historical marriage or the sequel romance. Kocoum\'s death does not change the initial expectation.'),
(869,'The_Hunchback_of_Notre_Dame_(1996_film)','Plot opening and Clopin cast entry',
 'Clopin is the puppeteer who tells Quasimodo\'s origin to children in the opening.',
 ['Phoebus is the captain, not the opening storyteller.','Quasimodo is the bell-ringer whose story is told.','Frollo appears in the story but is not its framing puppeteer.'],
 'Frollo sings within the opening number, but that does not make him the framing puppeteer. #548 asks the song title; this asks the storyteller\'s identity.'),
(870,'Hercules_(1997_film)','Plot ending and Voice cast: Megara and the Muses',
 'Megara is Hercules\'s romantic partner; he chooses a mortal life with her.',
 ['Thalia is a Muse, not the romantic partner in this story.','Calliope is a Muse, not the romantic partner in this story.','Atropos is not the woman for whom Hercules retrieves a soul and gives up Olympus.'],
 'The Disney romance is Megara\'s rather than any woman associated with mythological Heracles. The final choice to remain with Meg establishes the precise romantic relationship.'),
(871,'Mulan_(1998_film)','Plot training camp and cast: Captain Li Shang, Chi-Fu, Yao and Ling',
 'Captain Li Shang commands and trains the recruits; Chi-Fu is the imperial official, Yao and Ling recruits.',
 ['Chi-Fu is the imperial representative who criticizes the training.','Yao is a fellow recruit under Shang.','Ling is a fellow recruit under Shang.'],
 'Other soldiers may help one another learn, but the stem asks the army captain responsible for the unit; this fixes Shang rather than an assistant or recruit.'),
(872,'Tarzan_(1999_film)','Childhood Plot and Voice cast: Tantor, Kerchak, Terk and Sabor',
 'Tantor is the elephant who befriends Tarzan as a child.',
 ['Kerchak is the gorilla troop leader.','Terk is the gorilla childhood friend.','Sabor is the leopard.'],
 'Terk also satisfies childhood friend but fails elephant. Kerchak and Sabor fail both the species and the stated friendship.'),
(873,'Atlantis:_The_Lost_Empire','Expedition roster and cast; campfire dialogue about teenager chief mechanic',
 'Audrey Ramirez is the expedition\'s teenage chief mechanic.',
 ['Helga Sinclair is Rourke\'s second-in-command.','Moliere is the geologist and tunneling expert.','Packard is the radio operator.'],
 'The role and age are explicitly stated in Milo\'s question to Audrey. Repair-adjacent technical jobs do not make the geologist or radio operator the chief mechanic.'),
(874,'Lilo_%26_Stitch','Plot: Councilwoman assigns Jumba and Earth expert Pleakley; Voice cast',
 'Pleakley is the council\'s Earth expert assigned to assist Jumba in retrieving Stitch.',
 ['Jumba is the scientist being assisted and Stitch\'s creator.','Gantu is the captain, not this assigned Earth expert.','Reuben is not the agent assigned as Jumba\'s Earth expert in the 2002 film.'],
 'Replaced poses as with the actual official assignment and specified 2002. This tests the theatrical mission, not sequel or TV stories involving Reuben.'),
(875,'Treasure_Planet','Plot: treasure chamber, Flint\'s skeleton and memory-circuit restoration',
 'Jim finds B.E.N.\'s missing primary memory circuit with Flint\'s skeleton and reinstalls it, restoring knowledge of the trap.',
 ['M.O. is not the robot whose circuit Jim restores here.','Auto is not the robot whose circuit Jim restores here.','DOR-15 is not the robot whose circuit Jim restores here.'],
 'Challenged the premise separately: the map is a distinct object, not a piece stored in B.E.N. Final wording asks the recovered memory circuit and its owner. #2613 asks Martin Short\'s voice performance, an additional fact.'),
(876,'Brother_Bear','Plot journey and Voice cast: Rutt and Tuke',
 'Rutt and Tuke are the moose brothers encountered by Kenai and Koda.',
 ['Timon and Pumbaa are not the named moose brothers.','Jock and Trusty are not the named moose brothers.','Pain and Panic are not the named moose brothers.'],
 'All options are paired character names of comparable form. The source explicitly names the two moose; the other pairs do not denote that duo.'),
(877,'Chicken_Little_(2005_film)','Plot final paragraph, Voice cast: Adam West as Ace, and video-game section',
 'Ace is the action-hero movie version of Chicken Little shown in the film-within-the-film ending.',
 ['Buck is Chicken Little\'s father, not his Hollywood counterpart\'s name.','Kirby is the alien child, not the action-hero counterpart.','Runt is the pig friend, with his own movie counterpart.'],
 'The father is also nicknamed Ace in some accounts, so final wording fixes the action-hero counterpart rather than a real first name. This is an in-universe movie sequence in a theatrical film, not real TV trivia.'),
(878,'Meet_the_Robinsons','Plot science-fair sabotage and Helping Hat reveal; Voice cast',
 'Doris is the rogue robotic bowler hat helping Goob sabotage Lewis.',
 ['Carl is the Robinsons\' friendly robot.','Lefty is not the bowler hat\'s given identity.','Goob is the man wearing the hat, not the hat itself.'],
 'Bowler Hat Guy and his hat are separate entities. Goob identifies the human in #1087; Doris names the sentient invention here.'),
(879,'Bolt_(2008_film)','Plot New York meeting, cross-country journey and Voice cast',
 'Mittens is the stray tuxedo cat who guides Bolt and later helps him reunite with Penny.',
 ['Rhino is the hamster traveling with them.','Whiskers is not the cat named in this journey.','Penny is the human Bolt is trying to find.'],
 'Changed black cat to stray cat to avoid inaccurately implying an all-black coat: Mittens has white tuxedo markings. This is the film\'s real journey, not a fictional TV-episode claim.'),
(880,'The_Princess_and_the_Frog','Bayou Plot and cast: Mama Odie, Eudora, Charlotte and Juju',
 'Mama Odie is the blind bayou priestess who advises Tiana and Naveen; Juju is her snake.',
 ['Eudora is Tiana\'s mother.','Charlotte is Tiana\'s childhood friend.','Juju is Mama Odie\'s snake, not the priestess.'],
 'Eudora and Charlotte also guide or help Tiana, but neither is the blind bayou priestess. Juju lives there but is a snake; role and blindness jointly fix Mama Odie.'),
(881,'Frozen_(2013_film)','Voice cast: Paul Briggs as Marshmallow; palace confrontation',
 'Marshmallow is the giant snow monster guarding Elsa\'s palace.',
 ['Olaf is the smaller snowman accompanying Anna and Kristoff.','Sven is the reindeer, not a snow guardian.','Snowgies belong to Frozen Fever, not the giant guard in the 2013 film.'],
 'Specified 2013 to exclude the small snow creatures in Frozen Fever. Olaf is also made of snow but does not satisfy giant palace guard.'),
(882,'Big_Hero_6_(film)','Voice cast and laboratory introduction; Wasabi armor description',
 'Wasabi specializes in laser-induced plasma and his battle armor deploys plasma blades.',
 ['Go Go uses electromagnetic wheels/discs, not Wasabi\'s forearm plasma-blade system.','Honey Lemon uses chemistry spheres, not the forearm plasma-blade system.','Fred wears the monster suit with jumping and fire effects, not the plasma-blade system.'],
 'Did not infer exclusive abilities merely from Wasabi\'s laser expertise. Cross-checked the described equipment: discs, chemistry spheres and monster suit differ from his retractable forearm blades. #1134 tests another member\'s equipment.'),
(884,'Moana_(2016_film)','Plot cavern revelation and Tala\'s spirit; Voice cast family relationships',
 'Gramma Tala is Moana\'s ocean-loving grandmother and guide.',
 ['Sina is Moana\'s mother.','Te Fiti is the island goddess, not her grandmother.','Chief Tui is Moana\'s father.'],
 'Several characters guide Moana, but only Tala has the stated grandmother relationship. This does not duplicate the Sina or Chief Tui parent questions.'),
(885,'Encanto','Voice cast family relationships and gifts; The Family Madrigal cousin roll call',
 'Camilo is Mirabel\'s cousin with the shapeshifting gift; Dolores hears extraordinarily, Antonio speaks with animals, Bruno sees the future.',
 ['Dolores has exceptional hearing.','Antonio communicates with animals.','Bruno has prophetic visions and is Mirabel\'s uncle rather than cousin.'],
 'Camilo can imitate Bruno or Dolores without transferring his gift to them. Rechecked the explicit gift roster and clarified whose cousins are meant; #1135 and #1099 test different gifts.'),
]

PARKS = [
(886,'https://www.disneyparksblog.com/disney-experiences/top-ways-to-celebrate-indiana-jones-at-disney-parks/','Disneyland attraction location; Forbidden Eye listing',
 'Disneyland\'s Indiana Jones Adventure is in Adventureland.',
 ['Frontierland is not the assigned land for this Disneyland attraction.','Fantasyland is not the assigned land.','Tomorrowland is not the assigned land.'],
 'The word Adventure in the ride title is a thematic clue but does not state Adventureland. #100 concerns Pirates at Magic Kingdom, #2525 Skull Rock in Paris, and #887 the temple subtitle, all separate location or naming facts.'),
(887,'https://disneyparksblog.com/disney-experiences/top-ways-to-celebrate-indiana-jones-at-disney-parks/','Opening list of Indiana Jones experiences by resort',
 'Disneyland\'s ride is Indiana Jones Adventure: Temple of the Forbidden Eye; Tokyo uses Crystal Skull and Paris has Temple of Peril.',
 ['Temple of the Crystal Skull is the Tokyo version.','Temple of Peril is the Paris attraction.','Temple of Doom is not the Disneyland subtitle in the official list.'],
 'Used parallel real Indiana Jones temple names as distractors. Resort context is essential: do not import Tokyo\'s subtitle or confuse a movie title with this ride.'),
(888,'https://disneyworld.disney.go.com/attractions/epcot/living-with-the-land/','Opening description: gentle boat tour past greenhouses',
 'Living with the Land takes its boats through agricultural greenhouses.',
 ['Space capsules are not the agricultural growing spaces described.','Underwater tunnels are not the plant-growing spaces described.','Movie sets are not the working growing spaces described.'],
 'The ride also has staged environments, but its actual working greenhouses make only the first offered kind of space correct. #920 asks the farming ride\'s name and #1139 its pavilion; this greenhouse feature is related but a distinct requested attribute.'),
(889,'https://www.disneyworld.eu/attractions/epcot/seas-with-nemo-and-friends/','A Fin-tastic Adventure and Explore the Aquarium; Seas exit',
 'The Nemo clamobile ride occupies The Seas pavilion and exits into its SeaBase aquarium.',
 ['The Land is the agricultural pavilion, not the Nemo aquarium site.','Imagination is not the pavilion identified by the Seas ride and aquarium.','The Odyssey is not the pavilion identified by the Seas ride and aquarium.'],
 'Separated ride identity from film category: this is park-location trivia, so parks remains correct even though Nemo is Pixar. The pavilion is identified through the ride and SeaBase connection.'),
(890,'https://disneyworld.disney.go.com/attractions/animal-kingdom/kilimanjaro-safaris/','Opening and A Truly Wild Adventure',
 'Kilimanjaro Safaris is the guided open-air safari-vehicle ride through Harambe Wildlife Reserve.',
 ['Kali River Rapids is a river raft attraction, not this truck ride.','Wildlife Express Train travels by locomotive to Conservation Station.','Maharajah Jungle Trek is a walking trail through Asian animal habitats.'],
 'Wild Africa Trek genuinely includes a safari-vehicle portion in Harambe Reserve, so it was removed rather than dismissed. Final options distinguish truck, raft, train and walking trail. #1484 asks the village/area name Harambe, not the safari ride.'),
(891,'https://disneyparksblog.com/wdw/dinoland-closing-animal-kingdom/','When is DinoLand closing; Time Rover references',
 'DINOSAUR used vehicles called Time Rovers; the attraction\'s final operating day was February 1, 2026.',
 ['Dino Runners is not the established vehicle name.','Chrono Cruisers is not the established vehicle name.','Primeval Rovers is not the established vehicle name.'],
 'Changed to before-closure wording. Time-traveling is necessary context and also appears in other invented choices; it does not uniquely give Time Rovers. Rechecked the name separately from the closure date.'),
(892,'https://disneyworld.disney.go.com/attractions/magic-kingdom/mad-tea-party/','Opening, A Very Merry UnBirthday and Control Your Spin',
 'Mad Tea Party spins guests in giant teacups.',
 ['Prince Charming Regal Carrousel uses carousel horses, not teacups.','Dumbo uses flying elephant vehicles, not teacups.','The Pooh dark ride is not the spinning-teacup attraction.'],
 'Movement alone could fit multiple rides; the giant teacup vehicles select Mad Tea Party. No title words are copied into the question.'),
(893,'https://disneyworld.disney.go.com/attractions/magic-kingdom/peter-pan-flight/','Set Sail Across the Sky: pirate galleon and London',
 'Peter Pan\'s Flight boards a pirate galleon and flies over London, including Big Ben and Tower Bridge.',
 ['It\'s a Small World uses boats past international doll scenes, not flying pirate ships over London.','The Barnstormer is a coaster, not this London dark ride.','Under the Sea is the Mermaid dark ride, not this pirate-galleon flight.'],
 'The selected conjunction is flying pirate ships over London, not any attraction containing a boat. The presence of British scenes elsewhere would not satisfy the ride vehicle and scene together.'),
(894,'https://disneyworld.disney.go.com/attractions/magic-kingdom/jungle-cruise/','Adventure Around Every Corner: dry wit and trusty skipper',
 'Jungle Cruise is the comedic river tour with a live skipper and dry jokes.',
 ['Swiss Family Treehouse is a walk-through treehouse, not a skippered tour.','Pirates of the Caribbean is a pirate dark boat ride, not the live-skipper comedy tour.','Magic Carpets of Aladdin is a flying-carpet spinner, not a skippered river tour.'],
 'Other attractions contain humor, but the live skipper\'s intentionally corny narration selects Jungle Cruise. Historical snapshot describes the base attraction rather than promising holiday operation.'),
(895,'https://disneyworld.disney.go.com/attractions/epcot/gran-fiesta-tour-starring-three-caballeros/','Opening description: gentle boat ride through Mexico Pavilion',
 'Gran Fiesta Tour Starring The Three Caballeros is inside the Mexico Pavilion.',
 ['Norway is not the pavilion assigned to Gran Fiesta Tour.','Germany is not the pavilion assigned to Gran Fiesta Tour.','Italy is not the pavilion assigned to Gran Fiesta Tour.'],
 'The official description explicitly names Mexico. #1171 asks pyramid architecture, requiring another fact rather than knowing which ride Mexico houses.'),
(897,'https://disneyworld.disney.go.com/attractions/hollywood-studios/toy-story-mania/','It\'s Playtime, Fun & Games and related attractions',
 'Toy Story Mania uses 3D glasses, carnival trams and spring-action shooters aimed at moving targets.',
 ['Alien Swirling Saucers is a spinning rocket ride, not the target-shooting game.','Slinky Dog Dash is a coaster, not the target-shooting game.','Runaway Railway is a cartoon adventure, not this interactive target game.'],
 'Other rides can display dimensional projections, but the combination of carnival targets and guest-operated shooters uniquely identifies Mania among the four.'),
(898,'https://disneyparks.disney.go.com/mickey-minnies-runaway-railway/','Engineer Goofy opening and Hollywood Studios section',
 'Mickey & Minnie\'s Runaway Railway carries guests on Engineer Goofy\'s train into the cartoon world at Hollywood Studios.',
 ['Toy Story Mania is a carnival shooting game, not Engineer Goofy\'s train.','Slinky Dog Dash is a Toy Story coaster, not Goofy\'s cartoon train adventure.','Star Tours is a Star Wars simulator, not Goofy\'s train adventure.'],
 'Removed Mickey, Minnie and railway from the stem and replaced invented near-titles with real rides. Engineer Goofy supplies a scene fact rather than copying the answer title; #1173 instead asks the theater building.'),
(899,'https://en.wikipedia.org/wiki/Disney%27s_Pop_Century_Resort','Theming: 1950s list; Gallery: bowling-pin-shaped pool',
 'Pop Century\'s 1950s area contains the bowling-pin-shaped Bowling Pool.',
 ['Art of Animation lists Big Blue, Cozy Cone and Flippin\' Fins pools, not this 1950s section.','All-Star Music has guitar and piano pools, not the bowling-pin pool.','Caribbean Beach has Caribbean island villages and a colonial-fort-themed main pool, not the 1950s bowling area.'],
 'Do not confuse nearby Art of Animation across the bridge with Pop Century. Confirmed the pool shape separately from the bowling-pin staircases and the decade setting.'),
(900,'https://disneyworld.disney.go.com/resorts/wilderness-lodge-resort/','What Makes This Resort Hotel Unique: Great Northwest and National Park lodges',
 'Wilderness Lodge draws on turn-of-the-century national park lodges of America\'s Great Northwest, with a rustic interior.',
 ['Grand Floridian evokes Victorian Palm Beach, not Northwest park lodges.','Contemporary is an ultra-modern A-frame resort, not a rustic park lodge.','Port Orleans evokes Louisiana and New Orleans, not Northwest park lodges.'],
 'A grand lobby alone is insufficient. The specific Northwest national-park-lodge design selects Wilderness Lodge; related hotel location and pool questions ask other attributes.'),
(901,'https://disneyworld.disney.go.com/resorts/polynesian-resort/','What Makes This Resort Hotel Unique and Resort Monorail',
 'Polynesian Village celebrates South Pacific islands and has Resort Monorail service.',
 ['Contemporary has monorail service but an ultra-modern theme.','Grand Floridian has monorail service but a Victorian Palm Beach theme.','Wilderness Lodge has a Northwest park-lodge theme, not the South Pacific.'],
 'Monorail service alone leaves two competing choices, so checked South Pacific theming explicitly. Knowing the list of monorail hotels in #626 does not identify which has this theme.'),
]

base=read('audit/runs/next-shard-0016-final-evidence-notes.json')
library=read('audit/source-notes.json')
templates={r['questionId']:r for r in base['reviews']}
CHECKS=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
reviews=[]
for i,topic,locator,premise,wrong,challenge in DATA+PARKS:
    url=topic if topic.startswith('https:') else 'https://en.wikipedia.org/wiki/'+topic
    sid=f'b16-{i}'
    limitations=('Text synopsis and named cast/character descriptions inspected; no original film playback claimed. D23 A-to-Z yielded a sign-in shell. Where available, corroborating dialogue, official material or prior passage notes are linked separately.' if i<886 else 'Text descriptions inspected. Park experience/location frozen to November 2026, or the stated past closure, rather than an unbounded operating promise.')
    library['sources'][sid]={'url':url,'locator':locator,'evidence':premise,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':False,'nextReviewAt':None,'limitations':limitations,'topics':['Batch 16',topic]}
    r=templates[i]
    r.update(checks=CHECKS,notes='Complete question, four options, full deduplicated topic digests and cross-bank context reviewed. Category/difficulty retained; no new sequel/TV scope introduced. '+challenge,context=locator,timeSensitive=False,nextReviewAt=None)
    r['premise']={'reason':premise,'sources':[sid]}
    r['options']=[{'basis':'direct','reason':premise,'sources':[sid]}]+[{'basis':'exclusive-inference','reason':v,'sources':[sid]} for v in wrong]
    r['challenge']={'reviewer':'Codex','at':'2026-11-07','premiseChecked':True,'alternativesExcluded':True,'notes':challenge}
    reviews.append(r)

# Only passages actually inspected in this run, or evaluated reusable source notes.
EXTRA={
852:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=pinocchio','Pinocchio tells Honest John after leaving Stromboli: bird-cage account','Pinocchio identifies Stromboli as the person who locked him in a bird cage.')],
854:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=peter-pan','Opening nursery argument: Mary addresses George and Wendy calls him Father','George is the father addressed by Mary and Wendy during preparations to leave the nursery.')],
857:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=sleeping-beauty-1959','Cottage dress preparation: blue/pink exchange, Merryweather named at the blue spell','Merryweather demands blue while Flora demands pink; Fauna works on the cake.')],
860:[('https://characters.disney.com/winnie-the-pooh/piglet','Piglet character introduction','Disney describes Piglet as a small, timid friend in the Hundred Acre Wood.')],
861:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=the-rescuers','Albatross Flight 13 landing, introduction and Devil\'s Bayou arrival','Orville introduces himself to Bernard and Bianca as the captain and flies them to Devil\'s Bayou.')],
862:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=fox-and-the-hound-the','Opening: Big Mama comforts orphaned Tod and seeks help','Big Mama finds the little fox, recognizes he needs care, and recruits the other birds to help.')],
864:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=great-mouse-detective-the','Basil calls his companion Doctor; final farewells identify Dr. Dawson','Dawson accompanies Basil and Olivia repeatedly addresses him as Dr. Dawson.')],
863:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=the-black-cauldron','Opening bath for Hen Wen; Taran asks Dallben about being an assistant pig keeper','Taran explicitly calls himself the assistant pig keeper while Dallben directs his care for Hen Wen.')],
873:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=atlantis-the-lost-empire','Campfire conversation: Milo asks Audrey how a teenager became chief mechanic','Milo explicitly calls Audrey a teenager and the expedition\'s chief mechanic.')],
875:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=treasure-planet','B.E.N. introduction and memory restoration after Flint\'s trove','B.E.N. lacks his primary memory circuit; restoring it brings back the memory of Flint removing it to hide the trap.'),('https://www.skywaytowonderland.com/treasure-planet/','Treasure chamber, Jim and B.E.N. board the old ship','Jim sees Flint\'s skeleton holding B.E.N.\'s chip and returns it to the robot.')],
877:[('https://www.nintendoworldreport.com/pr/12593/buena-vista-ships-chicken-little-ace-in-action-for-wii','Buena Vista press release: movie-within-movie inspiration and reprised film roles','Disney\'s press release distinguishes the superhero alter egos from the original Chicken Little and names Adam West as Ace.')],
882:[('https://disney.fandom.com/wiki/Wasabi','Powers and abilities; original Big Hero 6 appearance','Wasabi\'s suit houses retractable plasma blades in the forearms.'),('https://www.springfieldspringfield.co.uk/movie_script.php?movie=big-hero-6','Nerd lab introductions: Go Go bike; Wasabi laser-induced plasma; Honey Lemon chemistry','Hiro meets Go Go at the electromagnetic bike, Wasabi at the plasma demonstration and Honey Lemon at her chemistry experiment.')],
885:[('https://news.disney.com/introducing-encanto','Pepa and Felix branch: Dolores, Camilo and Antonio','Disney assigns hearing to Dolores, appearance transformation to Camilo, and animal communication to Antonio.'),('https://news.disney.com/cast-of-encanto','Bruno and Camilo cast interviews','Bruno has foresight; Camilo shapeshifts to look like other people.')],
886:[('https://wdwnt.com/2026/09/indiana-jones-adventure-now-closed-for-refurbishment-at-disneyland/','Opening refurbishment report: Adventureland location','Indiana Jones Adventure: Temple of the Forbidden Eye is located in Adventureland at Disneyland.')],
890:[('https://disneyworld.disney.go.com/events-tours/animal-kingdom/wild-africa-trek/','The Journey; Complimentary Photo Services','Wild Africa Trek includes a rugged safari vehicle and encounters with animals in Harambe Reserve, so it fit the original broad wording.'),('https://disneyworld.disney.go.com/attractions/animal-kingdom/wildlife-express-train/','All About Animals','Wildlife Express is a locomotive journey to Conservation Station.'),('https://disneyworld.disney.go.com/attractions/animal-kingdom/maharajah-jungle-trek/','Explore a Mystical Forest','Maharajah Jungle Trek is a self-guided walking trail through the Anandapur Royal Forest.')],
891:[('https://en.wikipedia.org/wiki/Dinosaur_(Disney%27s_Animal_Kingdom)','Ride statistics vehicle list and closed status','DINOSAUR\'s named vehicles were Time Rovers; the attraction is closed.')],
899:[('https://plandisney.disney.go.com/question/know-lifeguards-hippy-dippy-pool-pop-century-lifeguards-366175/','Resort\'s three pools by decade','Pop Century places the Bowling Pool in the 1950s area.'),('https://disneyworld.disney.go.com/resorts/art-of-animation-resort/','Pool descriptions','Art of Animation\'s pools are Big Blue, Cozy Cone and Flippin\' Fins.'),('https://disneyworld.disney.go.com/resorts/all-star-music-resort/','Guitar-Shaped Pool and Piano Pool','All-Star Music has guitar and grand-piano pools.')],
900:[('https://disneyworld.disney.go.com/resorts/grand-floridian-resort-and-spa/','What Makes This Resort Hotel Unique','Grand Floridian evokes Victorian Palm Beach.'),('https://disneyworld.disney.go.com/resorts/contemporary-resort/','What Makes This Resort Hotel Unique','Contemporary is ultra-modern, with an A-frame tower and Southwest mural.'),('https://disneyworld.disney.go.com/resorts/port-orleans-resort-riverside/','What Makes This Resort Hotel Unique','Port Orleans Riverside evokes rural Louisiana; French Quarter evokes New Orleans.')],
901:[('https://disneyworld.disney.go.com/resorts/grand-floridian-resort-and-spa/','Victorian introduction and Resort Monorail','Grand Floridian combines a Victorian Palm Beach theme with monorail service.'),('https://disneyworld.disney.go.com/resorts/contemporary-resort/','Ultra-modern introduction and monorail tower','Contemporary is a modern A-frame resort served by monorail.'),('https://disneyworld.disney.go.com/resorts/wilderness-lodge-resort/','What Makes This Resort Hotel Unique','Wilderness Lodge has a Northwest national-park-lodge theme.')],
}
for r in reviews:
    i=r['questionId']
    for n,(url,loc,evidence) in enumerate(EXTRA.get(i,[]),1):
        sid=f'b16-{i}-extra-{n}'
        library['sources'][sid]={'url':url,'locator':loc,'evidence':evidence,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':False,'nextReviewAt':None,'topics':['Batch 16'],'limitations':'Inspected text; mirrored screenplay dialogue and secondary accounts are identified by their URLs, not claimed as film playback.'}
        # Each source supports only its explicit passage, not an invented copy of the whole premise.
        r['premise']['sources'].append(sid)
    if i in EXTRA:
        r['challenge']['notes']+=' Corroborating passages evaluated as listed; each source note states its own limited claim.'

# Reuse narrowly matching inspected prior passages without broadening their claims.
for r in reviews:
    for sid in {859:['b11-robin'],864:['b10-bigben'],869:['b14-bells'],884:['b10-sina']}.get(r['questionId'],[]):
        r['premise']['sources'].append(sid)
SUPPORT={
 'b16-882-gogo':('https://en.wikipedia.org/wiki/Go_Go_Tomago','Disney version, Film','The 2014 film version wears Hiro-built armor with electromagnetic skating and projectile discs.'),
 'b16-882-honey':('https://en.wikipedia.org/wiki/Honey_Lemon','Disney version, mechanical purse','The Disney film version uses a mechanical purse that mixes chemical elements into balls.'),
 'b16-882-fred':('https://disney.fandom.com/wiki/Fred_(Big_Hero_6)','Powers and abilities; original film suit','Fred\'s monster suit provides high jumps and a flamethrower below the chest.'),
 'b16-899-caribbean':('https://www.disneyworld.eu/resorts/caribbean-beach-resort/','What Makes This Resort Hotel Unique and Pool with Waterslide','Caribbean Beach evokes five named Caribbean islands and an old Spanish citadel pool.'),
 'b16-890-kali':('https://disneyworld.disney.go.com/attractions/animal-kingdom/kali-river-rapids/','Attraction description','Kali River Rapids is a whitewater raft ride, not a truck safari.'),
}
for sid,(url,loc,evidence) in SUPPORT.items():
    library['sources'][sid]={'url':url,'locator':loc,'evidence':evidence,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':False,'nextReviewAt':None,'topics':['Batch 16'],'limitations':'Text passage inspected; film-character pages restricted to Disney film sections, not comic or television powers.'}
library['sources']['b16-882']['evidence']='Wasabi is the team member specializing in lasers; Go Go, Honey Lemon and Fred are separately named colleagues.'
library['sources']['b16-886']['evidence']='Disney lists the Forbidden Eye attraction at Disneyland separately from the Crystal Skull at Tokyo and Temple of Peril in Paris.'
for r in reviews:
    i=r['questionId']
    if i==882:
        r['options'][0]['sources']=['b16-882','b16-882-extra-1','b16-882-extra-2']
        for j,sid in enumerate(['b16-882-gogo','b16-882-honey','b16-882-fred'],1): r['options'][j]['sources']=[sid]
    elif i==899:
        r['options'][0]['sources']+=['b16-899-extra-1']
        r['options'][1]['sources']=['b16-899-extra-2']
        r['options'][2]['sources']=['b16-899-extra-3']
        r['options'][3]['sources']=['b16-899-caribbean']
    elif i in (900,901):
        for j in range(1,4): r['options'][j]['sources']=[f'b16-{i}-extra-{j}']
    elif i==890:
        r['options'][1]['sources']=['b16-890-kali']
        r['options'][2]['sources']=['b16-890-extra-2']
        r['options'][3]['sources']=['b16-890-extra-3']
    elif i==886:
        for option in r['options']: option['sources']=['b16-886-extra-1']
    elif i==885:
        for option in r['options']: option['sources']+=['b16-885-extra-1','b16-885-extra-2']
base['reviews']=reviews
base['sourcesChecked']=list(dict.fromkeys(s for r in reviews for part in [r['premise']]+r['options'] for s in part['sources']))
write('audit/source-notes.json',library)
write('audit/runs/next-shard-0016-reviewed-notes.json',base)
print('Authored',len(reviews),'explicit four-option reviews.')
