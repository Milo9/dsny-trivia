"""Explicit Batch 21 evidence authoring. Does not edit question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def save(p, value):
    (ROOT / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def wiki(page):
    return 'https://en.wikipedia.org/wiki/' + page
def script(page):
    return 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=' + page

# Main inspected passage, specific locator, premise, four assessments in final
# stored order, and the separately performed challenge of literal alternatives.
rows = {
1102: (wiki('Pinocchio_(1940_film)'), 'Plot, Blue Fairy workshop visit; Voice cast',
 'The Blue Fairy appoints Jiminy Cricket as Pinocchio\'s conscience; Geppetto creates the puppet and Figaro is his kitten.',
 ['Jiminy is explicitly assigned this office.', 'The Blue Fairy appoints the conscience; she is not the appointee.', 'Geppetto is the creator and father figure, not the appointed conscience.', 'Figaro is Geppetto\'s kitten, not the appointee.'],
 'Helping guide Pinocchio does not by itself confer the specific office. The appointment exchange names Jiminy, excluding the fairy who performs it and the two workshop residents. The final badge in #556 is a different reward fact.'),
1103: (wiki('Alice_in_Wonderland_(1951_film)'), 'Plot, Cheshire Cat directions and unbirthday tea party',
 'The Mad Hatter, March Hare and Dormouse host the party; the White Rabbit arrives later and loses his watch.',
 ['The Hatter is one of the hosts alongside the March Hare.', 'The White Rabbit is a later visitor whose watch the hosts destroy.', 'The Caterpillar belongs to the earlier mushroom encounter, not the tea hosts.', 'The King belongs to the later royal court, not the tea hosts.'],
 'The Rabbit does appear at the table, but being a visitor is different from hosting it. Dormouse could also fit the role but is not an option; exactly one of the four choices is a host.'),
1104: (wiki('Peter_Pan_(1953_film)'), 'Opening Plot and Voice cast, Heather Angel as Mary Darling',
 'George and Mary Darling are the parents of Wendy, John and Michael.',
 ['Mary Darling is explicitly the children\'s mother.', 'Jane is not the mother\'s name in the 1953 parent roster.', 'Elizabeth is not the name assigned to Wendy\'s mother.', 'Margaret is not the name assigned to Wendy\'s mother.'],
 'The opening dialogue addresses the mother as Mary and Wendy calls her Mother. The alternatives are competing names for one identified parent, not other maternal roles; the date excludes adaptations.'),
1105: ('https://catalog.afi.com/Film/51552-LADY-AND-THE-TRAMP', 'Synopsis, Jim Dear and Darling leave Aunt Sarah to babysit; credited voices',
 'Aunt Sarah brings her two Siamese cats, Si and Am, into Lady\'s household.',
 ['AFI explicitly identifies Si and Am as Aunt Sarah\'s cats.', 'Jock and Trusty are Lady\'s neighborhood dog friends.', 'Tibbs and Rufus is not the pair AFI identifies as Aunt Sarah\'s cats.', 'Tito and Rita is not the pair identified as her cats.'],
 'Tibbs and Rufus are feline names elsewhere, so species alone would not exclude them. The named owner-pair relationship does: the inspected synopsis gives Si and Am. The 1955 version avoids remake changes.'),
1106: (wiki('Sleeping_Beauty_(1959_film)'), 'Opening Plot, royal christening; cast Stefan, Hubert and Phillip',
 'Aurora is Stefan\'s daughter; Hubert is Phillip\'s father and Phillip is Aurora\'s betrothed.',
 ['Stefan is explicitly Aurora\'s father.', 'Hubert fathers Phillip, not Aurora.', 'Phillip is Aurora\'s betrothed, not her father.', 'Triton is not the father identified in this 1959 family.'],
 'The two kings are distinct fathers. A later father-in-law relationship cannot make Hubert Aurora\'s father under the opening royal family; the film date excludes Maleficent adaptations.'),
1107: (wiki('One_Hundred_and_One_Dalmatians'), 'Voice cast, Martha Wentworth as Nanny; Perdita and Sergeant Tibbs entries',
 'Nanny is the Radcliffes\' human cook and housekeeper; Perdita is a Dalmatian mother and Tibbs a cat.',
 ['Nanny is expressly the household cook and housekeeper.', 'Sergeant Tibbs is a cat helping the countryside rescue, not a human housekeeper.', 'Perdita is the puppies\' canine mother, not the human housekeeper.', 'Miss Birdwell is not the housekeeper identified by the film\'s cast and Pongo\'s introduction.'],
 'The old puppy-care wording admitted Perdita as well as Nanny. Final wording requires the human household job; the narration specifically identifies Nanny. Easy difficulty acknowledges that two alternatives are animals.'),
1108: (wiki('The_Sword_in_the_Stone_(1963_film)'), 'Plot, Merlin returns Wart to Ector\'s castle; Voice cast Ector/Kay/Merlin/Pelinore',
 'Ector is Arthur\'s foster father, Kay his foster brother, Merlin his tutor and Pellinore Ector\'s friend.',
 ['Ector is explicitly the foster father.', 'Kay is the foster brother and Ector\'s son.', 'Merlin is the tutor, not the foster father.', 'Pellinore is Ector\'s friend who announces the tournament.'],
 'Merlin\'s paternal guidance does not make him the named foster parent. Kay\'s relationship in #1061 is separate from Ector\'s; the two answers cannot be swapped.'),
1109: (wiki('The_Jungle_Book_(1967_film)'), 'Voice cast, vulture quartet and Hathi/King Louie/Kaa entries',
 'The four vultures are Buzzie, Dizzy, Flaps and Ziggy; Hathi is an elephant, Louie an orangutan and Kaa a python.',
 ['This is the complete four-vulture roster.', 'Hathi replaces Ziggy but is an elephant.', 'Louie replaces Flaps but is an orangutan.', 'Kaa replaces Dizzy but is a snake.'],
 'Each wrong set shares three genuine vultures, so familiarity with one name cannot solve it. The fourth member must also fit. The artifact catalogue independently names the same complete quartet.'),
1110: (wiki('The_Aristocats'), 'Voice cast, Scat Cat, O\'Malley, Roquefort and Edgar',
 'Scat Cat leads the jazz-playing alley cats; O\'Malley is his friend, Roquefort a mouse and Edgar the butler.',
 ['Scat Cat is expressly the band leader.', 'O\'Malley introduces his friends Scat Cat and his gang, rather than leading them.', 'Roquefort is the household mouse.', 'Edgar is the human butler and antagonist.'],
 'O\'Malley participates musically but is not the identified leader. #2072 asks which instrument Scat Cat plays, requiring trumpet knowledge beyond this role; #2071 asks Hit Cat\'s instrument.'),
1111: (wiki('Robin_Hood_(1973_film)'), 'Voice cast, Sir Hiss, Little John, Nutsy and Trigger',
 'Sir Hiss is Prince John\'s snake advisor; Little John is a bear and Nutsy/Trigger are vulture guards.',
 ['Sir Hiss is explicitly the snake counselor.', 'Little John is Robin\'s bear companion.', 'Nutsy is a vulture guard, not the snake advisor.', 'Trigger is another vulture guard, not the snake advisor.'],
 'All characters can interact with Prince John, but only Hiss combines the advisory role and snake identity. #1251 asks a song title and is distinct.'),
1112: (wiki('The_Rescuers'), 'Cast, Evinrude and Orville; Plot bayou boat trip',
 'Evinrude is the dragonfly propelling the leaf boat across Devil\'s Bayou; Orville provides air transport.',
 ['Evinrude mans the leaf boat and is called on to start his engine.', 'Orville is the albatross pilot, not the dragonfly.', 'Wilbur is not the named dragonfly in the 1977 boat scene.', 'Rufus is the orphanage cat, not its motor.'],
 'The motor wording is figurative propulsion, not a mechanical engine. Evinrude is called by name as the boat starts; the albatross choices concern flight instead.'),
1113: (wiki('The_Fox_and_the_Hound'), 'Opening Plot, Big Mama arranges Tod\'s adoption; Voice cast',
 'Big Mama arranges for Widow Tweed to adopt the orphaned Tod; Amos raises Copper and Vixey later becomes Tod\'s mate.',
 ['Widow Tweed is the adopting farmer who names him Tod.', 'Big Mama helps arrange adoption and advises him, but is not the adopting farmer.', 'Amos Slade owns Copper and opposes Tod.', 'Vixey is his later fox love interest.'],
 'Big Mama helps raise and protect Tod, making her a plausible broad caregiver answer. The specific adoption belongs to Tweed; #862 asks the owl\'s identity rather than the adopter.'),
1114: ('https://www.disneyanimation.com/films/the-black-cauldron/', 'Synopsis, motley team joins Taran; corroborating film cast roles',
 'Disney Animation names Fflewddur Fflam as the minstrel accompanying Taran.',
 ['Disney explicitly names Fflewddur as the minstrel.', 'Taran is the assistant pig keeper whose quest this is.', 'Dallben is Taran\'s wizard guardian, not this minstrel.', 'Eidilleg is the fairy king, not the minstrel.'],
 'Final wording isolates the named minstrel; it does not depend on whether the instrument should be called a harp or lyre. #1068 names the princess, a different companion and role.'),
1115: (wiki('The_Great_Mouse_Detective'), 'Plot Olivia\'s account of bat kidnapper; cast and Ratigan\'s lair',
 'Fidget is Ratigan\'s bat henchman, Felicia his cat, Bartholomew a mouse lackey and Dawson Basil\'s partner.',
 ['Fidget is the bat assistant who kidnaps Olivia\'s father.', 'Felicia is Ratigan\'s pet cat.', 'Bartholomew is a mouse lackey, not the bat.', 'Dawson is Basil\'s doctor companion, not Ratigan\'s bat.'],
 'Bartholomew also works for Ratigan, but the bat qualification excludes him. #2500 asks Fidget\'s peg leg, a separate physical trait; knowing that trait and knowing his name are different recall facts.'),
1116: (wiki('Oliver_%26_Company'), 'Plot Jenny adopts Oliver; Voice cast Georgette/Rita/Francis/Einstein',
 'Georgette is the Foxworth family\'s poodle; Rita, Francis and Einstein belong to Fagin\'s gang.',
 ['Georgette is explicitly the family poodle.', 'Rita is a gang dog, not Jenny\'s family poodle.', 'Francis is the gang\'s bulldog.', 'Einstein is the gang\'s Great Dane.'],
 'All four choices are dogs from the film. Attending Jenny\'s birthday later does not establish household ownership; Georgette is the dog already living with the family.'),
1117: (wiki('The_Little_Mermaid_(1989_film)'), 'Voice cast, Frank Welker as Max; ship/fire and beach scenes',
 'Max is Eric\'s pet sheepdog, addressed by name on the ship and at the beach.',
 ['Max is explicitly Eric\'s named dog.', 'Bruno is not the name Eric uses for his dog.', 'Major is not the name assigned to Eric\'s dog.', 'Sultan is not the name Eric uses for this pet.'],
 'The identity is a single named dog, not any animal owned by royalty. Other Disney pet names remain wrong. Max in #563 is Goofy\'s son, an unrelated character.'),
1118: (wiki('Aladdin_(1992_Disney_film)'), 'Voice cast, Sultan and Jafar; royal succession Plot',
 'Jasmine\'s father is addressed as Sultan; Jafar serves as grand vizier before usurping him.',
 ['Sultan is his specific in-film title.', 'King is a broader translation of a monarch, not the specific title used.', 'Vizier is Jafar\'s office.', 'Emir is not the specific title used for Jasmine\'s father.'],
 'A sultan can broadly be called a king. Final wording asks the specific address used in the film, so the translation does not create two correct choices.'),
1119: (wiki('The_Lion_King'), 'Voice cast, Zoe Leader as Sarafina and Madge Sinclair as Sarabi',
 'Sarafina is Nala\'s mother; Sarabi is Simba\'s mother. Sarafina\'s name is a credit identity, not spoken dialogue.',
 ['The cast identifies Sarafina as Nala\'s mother.', 'Sarabi is Simba\'s mother, not Nala\'s.', 'Zira is not the mother named for Nala in the 1994 credits.', 'Kiara is not the mother named for Nala in the 1994 credits.'],
 'Similar names Sarabi and Sarafina are deliberately plausible. The exact relationship and credited name distinguish them; no in-film spoken naming is claimed. #282 asks the other mother.'),
1120: (wiki('Pocahontas_(1995_film)'), 'Voice cast, Percy, Meeko, Flit and Wiggins',
 'Percy is Ratcliffe\'s pug; Meeko is a raccoon, Flit a hummingbird and Wiggins the human manservant.',
 ['Percy is explicitly Ratcliffe\'s pet pug.', 'Meeko is Pocahontas\'s raccoon companion.', 'Flit is her hummingbird companion.', 'Wiggins is a human servant, not the pug.'],
 'Percy eventually befriends the other animals and leaves his owner, so the question refers to his established introductory relationship rather than an assertion of permanent ownership.'),
1121: ('https://kids-in-mind.com/h/hercules_1997__131.htm', 'Violence/Gore, Fates share an eyeball sentence; corroborating UW scene analysis',
 'The three Fates pass a shared eyeball between them to see.',
 ['The review specifically identifies their shared eyeball.', 'An ear is not the sight organ passed between them.', 'A hand is not the sight organ in this exchange.', 'A nose is not the shared sight organ.'],
 'The old thread distractor was also something the Fates handle together. Final wording asks a sight-enabling body part. The eye is shared by the trio, not one separate eye per Fate.'),
1122: ('https://repository.unissula.ac.id/16098/6/LAMPIRAN.pdf', 'Printed page 74 / PDF page 19, tea test and Matchmaker\'s final declaration',
 'After the tea-serving mishap, the Matchmaker declares that Mulan will never bring her family honor.',
 ['The transcribed speaker of the declaration is the Matchmaker.', 'Grandmother Fa accompanies preparations but does not deliver this verdict.', 'Chi-Fu is the imperial official in the later conscription scene, not the tea examiner.', 'Fa Li is her mother, not the speaker of this verdict.'],
 'Chi-Fu also disparages Mulan later, so a generic insult question could admit him. The final tea-test scene and declaration exclude that later context, and the stem no longer repeats matchmaking.'),
1124: (script('emperors-new-groove-the'), 'Jungle Bucky encounter, lines 1789–1840; Yzma asks which way the llama went',
 'Kronk converses with the squirrel and asks it for directions to the talking llama.',
 ['Yzma identifies the animal as a squirrel during Kronk\'s conversation.', 'Llama describes Kuzco, the subject of the directions, not Bucky\'s language.', 'Jaguars are mentioned in Bucky\'s story, not the speaker\'s species.', 'A parrot is not the animal Kronk questions in this scene.'],
 'Kronk says he learned all woodland creatures, so merely proving squirrel competence cannot exclude other competence. Final wording asks the particular Bucky conversation; the llama and jaguars are subjects of that conversation.'),
1125: (wiki('Atlantis:_The_Lost_Empire'), 'Expedition roster in Plot; Voice cast Santorini/Moliere/Sweet/Cookie',
 'Vinny Santorini is the demolitions expert; Mole handles geology, Sweet medicine and Cookie food.',
 ['Vinny is explicitly assigned demolitions.', 'Moliere is the geologist and excavator.', 'Dr. Sweet is the medical officer.', 'Cookie is the expedition cook.'],
 'Other crew can handle explosives incidentally, but the roster\'s designated specialty is unique. Whitmore\'s briefing separately assigns Santorini to demolitions; #522 asks the excavator.'),
1126: (wiki('Lilo_%26_Stitch'), 'Plot, Grand Councilwoman dismisses Jumba/Pleakley and assigns Gantu',
 'After Jumba and Pleakley fail, the Grand Councilwoman assigns Gantu to capture Stitch.',
 ['Gantu is the replacement retrieval officer.', 'Bubbles is the social worker, not the assigned replacement.', 'David is Nani\'s human friend, not the replacement officer.', 'The Grand Councilwoman assigns the mission instead of taking it herself.'],
 'The old Captain Gantu answer repeated the captain clue. Final wording instead distinguishes the replacement from the first team and the assigning leader. The 2002 date is essential because the remake changes this plot.'),
1128: (wiki('Brother_Bear'), 'Opening Plot and cast, Tanana/Denahi/Sitka/Tug',
 'Tanana is the tribe\'s shaman who gives Kenai his totem and guides him after the transformation.',
 ['Tanana is explicitly the shaman-woman.', 'Denahi is Kenai\'s surviving brother.', 'Sitka is his eldest brother and later spirit guide.', 'Tug is a bear at the salmon run, not the tribal shaman.'],
 'Sitka provides spiritual guidance but is not the human shaman officiating the totem ceremony. The final four choices all occur in the original film, avoiding sequel-only names.'),
1129: (wiki('Chicken_Little_(2005_film)'), 'Opening Plot and Voice cast, Runt/Foxy/Fish/Goosey',
 'Runt of the Litter is the large pig in Chicken Little\'s outcast friend group.',
 ['The cast explicitly identifies Runt as the pig.', 'Foxy Loxy is a fox and school bully.', 'Fish Out of Water is a goldfish.', 'Goosey Loosey is a goose and Foxy\'s friend.'],
 'The 2005 date excludes the earlier wartime short. Species words in the wrong names make elimination easy, so difficulty is lowered; no second pig is among the choices.'),
1130: (wiki('Meet_the_Robinsons'), 'Voice cast, Franny, Lucille, Mildred and Doris; family tree dialogue',
 'Franny is Wilbur\'s mother; Lucille is his grandmother, Mildred the orphanage head and Doris a robotic hat.',
 ['Franny is expressly Wilbur\'s mother.', 'Lucille adopts Lewis and is Wilbur\'s grandmother.', 'Mildred runs the orphanage, not Wilbur\'s future household.', 'Doris is the robotic bowler hat, not his mother.'],
 'Time travel creates two generations of mothers in the story. The family tree states Wilbur is Franny and Cornelius\'s son, excluding Lucille\'s earlier adoption relationship.'),
1131: (wiki('Bolt_(2008_film)'), 'Opening Plot, Penny adopts the puppy; Voice cast',
 'Penny adopts Bolt and remains his owner outside the fictional television series; Mittens and Rhino are animal companions.',
 ['Penny is the girl who adopts and owns Bolt.', 'Mittens is the cat companion.', 'Rhino is the hamster companion.', 'Molly is not the owner named by the plot or cast.'],
 'This is the movie\'s real owner relationship rather than a plot question about the in-universe television show, preserving scope. Penny in #275 is a different film\'s orphan.'),
1132: (wiki('The_Princess_and_the_Frog'), 'Voice cast, Eudora, Charlotte and Mama Odie; opening family scene',
 'Eudora is Tiana\'s mother; Charlotte is her friend and Mama Odie the bayou priestess.',
 ['The cast explicitly names Eudora as Tiana\'s mother.', 'Charlotte is the wealthy childhood friend.', 'Mama Odie is the bayou guide, not her birth mother.', 'Georgia is not the mother\'s name assigned by the cast.'],
 'Mama Odie uses maternal language, but the opening household identifies Eudora and James as Tiana\'s parents. A maternal guide does not replace that explicit family relationship.'),
1133: (script('frozen-2013'), 'Search-party volunteers, lines 1165–1176; coronation Duke introduction lines 378–384',
 'The Duke volunteers two men to accompany Hans\'s search party after Anna disappears.',
 ['The Duke is the visitor who volunteers his two men.', 'Hans leads and requests volunteers; he is not the visiting donor of the two bodyguards.', 'Oaken is the trading-post proprietor, not a coronation dignitary supplying men.', 'Runeard does not appear in this 2013 search-party exchange.'],
 'Hans also threatens Elsa later, so the final question avoids a broad villainous motive. It asks who supplies the two men to Hans, differentiating supplier from party leader and removing the Weselton giveaway.'),
1134: (wiki('Honey_Lemon'), 'Disney version, 2014 film armor and chemical purse paragraph; film cast specialties',
 'Honey Lemon\'s purse mixes chemicals into spheres; Go Go specializes in electromagnetics, Wasabi in lasers, and Fred is the mascot.',
 ['Honey Lemon produces the chemical balls with her purse.', 'Go Go specializes in electromagnetics, not this chemical purse.', 'Wasabi specializes in laser/plasma equipment.', 'Fred is the mascot, not the chemistry specialist identified with this purse.'],
 'Other team members can hold or be affected by the spheres, but this asks their equipment user. The Disney-film section is used rather than the different Marvel-comics power set; #882 asks Wasabi\'s equipment.'),
1135: ('https://news.disney.com/introducing-encanto', 'Family profiles, Pepa/Felix children and Isabela paragraphs',
 'Disney assigns extraordinary hearing to Dolores, shapeshifting to Camilo, animal speech to Antonio and plant growth to Isabela.',
 ['Dolores is explicitly assigned extraordinary hearing.', 'Camilo transforms his appearance.', 'Antonio communicates with animals.', 'Isabela grows flowers and plants.'],
 'Understanding animal speech differs from supernatural hearing. Isabela is Mirabel\'s sister rather than cousin, so the final stem uses relatives; each gift has its own named recipient.'),
1136: ('https://disneyexperiences.com/disneyland-press/fact/frontierland-at-disneyland-park-fact-sheet/', 'Opening paragraph, 1955 original land and 1800s American West; stockade/landscaping',
 'Frontierland opened in 1955 and depicts the American West of the 1800s.',
 ['The fact sheet explicitly assigns the Old West setting to Frontierland.', 'Adventureland is not the land named by this historical-western description.', 'Tomorrowland is not the historical-western land identified here.', 'Fantasyland is not the land identified as the 1800s American West.'],
 'All alternatives are original lands, so original alone does not reveal the answer. The theme differentiates them. Magic Kingdom attraction locations and Paris Phantom Manor are independent park-specific facts.'),
1137: ('https://thewaltdisneycompany.com/news/disneyland-59-65-years-forefront-innovation/', '1959 expansion, Mike Buckhoff lists Submarine Voyage among formally introduced attractions',
 'The company\'s archive account names the 1959 Disneyland attraction Submarine Voyage.',
 ['Submarine Voyage is the name in the 1959 expansion account.', 'Finding Nemo is the later 2007 version, not its 1959 opening name.', '20,000 Leagues Under the Sea is not the Disneyland name listed in the 1959 account.', 'Nautilus Expedition is not the opening name in the archive\'s list.'],
 'A successor can trace its infrastructure to 1959. Final wording asks the name at opening, so Finding Nemo cannot be defended merely as the same lagoon\'s present attraction. #624 asks the later retheme.'),
1138: ('https://sites.disney.com/service-celebration/dx-east/more-celebration-details/frontierland/', 'Frontierland page, Attractions list Country Bear Musical Jamboree',
 'Disney lists Country Bear Musical Jamboree among Frontierland\'s attractions at Magic Kingdom.',
 ['Frontierland is the land heading above the attraction.', 'Liberty Square is not the listed land.', 'Adventureland is not the listed land.', 'Fantasyland is not the listed land.'],
 'The original and retitled bear shows should not be treated as different locations. Final wording names the current version and dates the configuration; Big Thunder and Paris Phantom Manor are distinct location facts.'),
1139: (wiki('The_Land_(Epcot)'), 'Introduction facility attractions and current attraction list; official guide p2 Land section',
 'The Land contains both Soarin\' and Living with the Land, whose boat route passes agricultural greenhouses.',
 ['The Land explicitly contains both rides.', 'The Seas is not their shared pavilion.', 'Imagination is a separate pavilion with the Figment attraction.', 'Wonders of Life is not the shared pavilion of these rides.'],
 'Soarin\'s film program can change without moving the attraction. Final wording keeps the brand rather than an obsolete subtitle and uses four pavilions. #888 asks what the greenhouse ride passes; this asks the enclosing pavilion and also uses Soarin\'s independent location.'),
1140: ('https://disneyparksblog.com/wdw/figment-dreamfinder-imagination-epcot/', 'Opening Figment description and Who is Dreamfinder history',
 'Figment is the purple dragon associated with Journey Into Imagination; Dreamfinder is his inventor/mentor.',
 ['Disney explicitly describes Figment as the creative purple dragon.', 'Elliott is not the dragon identified for Journey Into Imagination.', 'Spyro is not the dragon identified in this EPCOT history.', 'Dreamfinder is the inventor and storyteller, not the dragon he creates.'],
 'Other fictional dragons may be purple or appear in parks, but the named attraction relationship is necessary. #2212 asks Dreamfinder, #2213 the sponsor and #2214 the opening year, all additional facts.'),
1141: ('https://disneyparksblog.com/wdw/the-legacy-of-disneys-animal-kingdom-25-years-later/', 'April 22, 2023 date and opening paragraph, Earth Day 1998',
 'Animal Kingdom opened on Earth Day, April 22, 1998, as confirmed by Disney\'s anniversary and opening-day chronology.',
 ['April 22, 1998 is the recorded opening date.', 'October 1, 1982 is not Animal Kingdom\'s recorded opening date.', 'May 1, 1989 is not its recorded opening date.', 'July 17, 1955 is not its recorded opening date.'],
 'Opening and dedication are different events: the official chronology puts the dedication April 21 and public opening April 22. The four dates are mutually exclusive for this specific event.'),
1142: ('https://attractionsmagazine.com/look-demolition-sorcerers-hat-disneys-hollywood-studios/', 'January 23, 2015 report, 2001 installation and January 22 demolition photographs',
 'The giant Sorcerer\'s Hat was installed in 2001 before the Chinese Theatre and dismantled in 2015.',
 ['The contemporary removal account identifies the Hat and its 2001 addition.', 'The Earful Tower is shown as another surviving icon during this demolition, not the object removed here.', 'The Chinese Theatre stands behind the removed object.', 'The Animation Arch is not the object identified in the documented removal.'],
 'Simply standing during 2001–2015 also fit the Tower and theatre. Final wording requires installation in 2001, placement before the theatre and removal in 2015, uniquely selecting the Hat.'),
1143: ('https://dvcshop.com/disneyland-railroad-overview/', 'Attraction details, Main Street USA; entrance photograph caption',
 'The Disneyland Railroad station at the park entrance is Main Street, U.S.A.; the official railroad page lists all four stations.',
 ['Main Street, U.S.A. is the entrance station.', 'Mickey\'s Toontown is a separate station farther around the park.', 'New Orleans Square is another interior station.', 'Tomorrowland is another interior station.'],
 'The answer is a station, not a locomotive or the analogous Magic Kingdom entrance. All four final choices are actual Disneyland stations; turnstiles avoids repeating the answer word main.'),
1144: ('https://disneyexperiences.com/magic-kingdom-steam-trains/', 'Opening paragraphs, Walter E. Disney locomotive; corroborating locomotive table namesakes',
 'The Walter E. Disney is a Magic Kingdom locomotive; the roster separately names Roy O. Disney, Lilly Belle and Roger Broggie.',
 ['Walter E. Disney uses Walt\'s own name.', 'Roy O. Disney names Walt\'s brother rather than Walt.', 'Lilly Belle honors Walt\'s wife.', 'Roger E. Broggie names the Disney railroad engineer.'],
 'Sharing the Disney surname is insufficient: Roy and Walter identify different people. The question is about the honoree, not which locomotive Walt personally rode or built.'),
1145: ('https://disneyparks.disney.go.com/au/disneyworld/shops/world-of-disney/', 'Store introduction, Disney Springs/Marketplace and world\'s largest character store description',
 'Disney advertises Disney Springs\' World of Disney as the world\'s largest Disney character store.',
 ['World of Disney is the store carrying this specific advertised description.', 'DisneyStyle is not the shop named in the advertisement.', 'Marketplace Co-Op is not the shop named in the advertisement.', 'Once Upon a Toy is not the shop named in the advertisement.'],
 'Largest could mean area or inventory and could change. Final wording asks the explicitly attributed advertisement at a fixed date; a separate official store page corroborates the largest merchandise collection. World in the clue is ordinary ranking language, not a unique name giveaway.'),
1146: ('https://disneyworld.disney.go.com/entertainment/animal-kingdom/festival-of-the-lion-king/', 'Opening songs/pageantry/puppetry description and Harambe Theatre visitor guidance',
 'Festival of the Lion King is the Lion King celebration staged at Harambe Theatre.',
 ['The official show page identifies Festival and its Harambe venue.', 'The Big Blue and Beyond is a Nemo show, not this Lion King celebration.', 'Feathered Friends in Flight is a bird show, not this Lion King celebration.', 'Finding Nemo: The Musical is a different film adaptation and not the Harambe Lion King show.'],
 'The former Harambe Nights event could overlap the old broad description. Final options and venue identify the regular Festival; celebrates avoids asserting a scene-for-scene retelling.'),
1147: ('https://wdwprepschool.com/epcot-world-showcase/', 'American Adventure Pavilion, Overview: location between Italy and Japan; other pavilion location headings',
 'The American Adventure is between Italy and Japan in World Showcase.',
 ['The overview explicitly gives Italy and Japan as its neighbors.', 'Germany is on the opposite side of Italy, not between Italy and Japan.', 'Morocco is beyond Japan, not between the named neighbors.', 'France is beyond Morocco, not between Italy and Japan.'],
 'Between means the adjoining pavilion position around the World Showcase promenade, not the distant straight-line area across the lagoon. The country sequence and separate location headings exclude the other three.'),
1148: (wiki('Tom_Sawyer_Island'), 'Intro and Tom Sawyer Islands in other Disney theme parks, Magic Kingdom; closure report',
 'Magic Kingdom\'s former Tom Sawyer Island stood in the Rivers of America and closed in 2025.',
 ['Rivers of America is the body of water containing the former island.', 'Seven Seas Lagoon is outside Magic Kingdom, not the island\'s river.', 'Bay Lake is a separate resort lake, not the island\'s river.', 'Discovery River is associated with Animal Kingdom, not this Magic Kingdom island.'],
 'The present-tense premise was obsolete after July 2025. Final wording is explicitly historical and specifies Florida, not the still-existing Disneyland island; the surrounding water name is not confused with a transportation lagoon.'),
1149: ('https://thewaltdisneycompany.com/news/disneyland-59-65-years-forefront-innovation/', 'Forward Thinking Innovation, Walt\'s visit to Switzerland during Third Man on the Mountain',
 'The company archive identifies the real Matterhorn peak in Switzerland as the attraction\'s inspiration.',
 ['Switzerland is the country expressly identified in the archive account.', 'Austria is not the country identified for the inspiration.', 'Germany is not the country identified for the inspiration.', 'France is not the country identified for the inspiration.'],
 'The real mountain also borders Italy, which is not among these choices; the stem does not claim it lies exclusively in Switzerland. None of the three listed wrong countries contains that peak.'),
1151: ('https://www.olc.co.jp/en/ir/library/factbook/main/01/teaserItems1/01/linkList/09/link/factbook2017.pdf', 'PDF page 7 / printed page 7, Principal Facility Data, Tokyo DisneySea opening date',
 'The operator\'s fact book records Tokyo DisneySea\'s opening as September 4, 2001.',
 ['2001 is the year in the operator\'s recorded date.', '1983 is Tokyo Disneyland\'s opening year in the separate row.', '1992 is not DisneySea\'s recorded opening year.', '2016 is not DisneySea\'s recorded opening year.'],
 'The resort\'s first park and its second park have different openings. #2241 asks the later Fantasy Springs expansion, so its 2024 answer cannot answer this park-opening question.'),
1152: ('https://panasonic.co.jp/ew/sustainability/tokyodisneyresort/en/videospot/tds.html', 'Mediterranean Harbor entrance view and Ponte Vecchio video-spot descriptions',
 'Tokyo Disney Resort sponsor Panasonic names the prominent erupting volcano across the entrance harbor Mount Prometheus.',
 ['The sponsor\'s named harbor landmark is Mount Prometheus.', 'Mount Mayday is not the volcano named in this Tokyo park description.', 'Mount Gushmore is not the volcano named in this Tokyo park description.', 'Mount Harrison is not the volcano named in this Tokyo park description.'],
 'This is a constructed park landmark, not a Japanese natural volcano or the Matterhorn. The source repeatedly identifies the same erupting harbor-view mountain, excluding other named Disney mountains.'),
}

# Additional passages actually read, including precise matching reusable evidence.
extra = {
1102: [(script('pinocchio'), 'Blue Fairy appointment, lines 246–266', 'The fairy asks Jiminy his name and appoints him conscience.')],
1103: [(script('alice-in-wonderland'), 'Tea party, watch destruction and departure, lines 1179–1247', 'The Rabbit arrives with a watch; the party hosts examine and destroy it before throwing him out.')],
1104: [(script('peter-pan'), 'Nursery preparation, lines 138–158', 'George addresses Mary; Wendy greets her as Mother.')],
1105: [(wiki('Lady_and_the_Tramp'), 'Plot Aunt Sarah babysits; voice cast Si/Am', 'Aunt Sarah brings Si and Am, her two Siamese cats.')],
1106: [(script('sleeping-beauty-1959'), 'Christening narration, lines 51–59 and 131', 'Aurora is Stefan\'s child, while Phillip is Hubert\'s son.')],
1107: [('https://www.moviefone.com/movie/one-hundred-and-one-dalmatians/4910/quotes/', 'Pongo narration, line 1178', 'Pongo introduces Nanny as the cook and housekeeper.')],
1108: ['b20-1061'],
1109: [('https://www.rrauction.com/auctions/lot-detail/334992304641108-buzzie-and-dizzy-production-cel-from-the-jungle-book-production-cel/', 'Lot Description, lines 414–415', 'The production-cel catalogue names the vulture quartet Buzzie, Flaps, Ziggy and Dizzy.')],
1110: [(script('aristocats-the'), 'O\'Malley introduces Scat Cat and his gang, lines 1028–1055', 'O\'Malley describes Scat Cat\'s gang and introduces Duchess to him at their musical gathering.')],
1111: [(script('robin-hood-1973'), 'Royal coach, lines 90–157', 'Prince John calls Sir Hiss counselor; their exchange explicitly identifies him as a snake.')],
1112: [(script('the-rescuers'), 'Leaf boat departure, lines 589–612', 'Evinrude is told to start his engine and urged to propel the boat.')],
1113: [(script('fox-and-the-hound-the'), 'Opening adoption, lines 13–94; widow/Amos confrontation later', 'Big Mama declines to keep the fox and arranges for the woman to find him. She takes him in, names him Tod, and calls him one of the family.')],
1114: [(wiki('The_Black_Cauldron_(film)'), 'Voice cast, lines 251–255', 'Taran is a pig keeper, Dallben a wizard, Fflewddur the bard and Eidilleg the fairy king.')],
1115: [(script('great-mouse-detective-the'), 'Ratigan gives Fidget the kidnapping list, lines 266–275; wings and Felicia, 750–773', 'Ratigan orders Fidget to collect the girl and equipment; Fidget complains about his wings while Felicia holds him.')],
1116: [(script('oliver-and-company'), 'Jenny asks Georgette to find Oliver, lines 1111–1135', 'Jenny addresses Georgette as her household companion while searching for Oliver.')],
1117: [(script('little-mermaid-the'), 'Ship and beach scenes, lines 29, 32 and 54', 'Eric calls his pet Max on the ship and at the beach.')],
1118: [(script('aladdin'), 'Succession discussion and Jafar usurpation, lines 1293–1311 and 1405–1424', 'The royal office is repeatedly named sultan; Jafar takes that office by wish.')],
1119: [('https://feelinganimatedblog.wordpress.com/2017/12/15/film-review-the-lion-king-1994/', 'Sarafina paragraph below hyena discussion, line 289', 'The reviewer identifies Sarafina as Nala\'s mother and notes that the name appears in credits, not spoken dialogue.')],
1120: [(script('pocahontas'), 'Percy/Meeko encounter, lines 1295–1310', 'Percy is addressed as a dog and distinguished from Meeko.')],
1121: [('https://uw.manifoldapp.org/projects/museum-of-greek-and-roman-mythology-su-23/resource/the-fates-moirai-disney-movie-hercules', 'Scene description, lines 24–35', 'The scene analysis identifies the shared eye and the separately held thread of life.')],
1122: [(wiki('Mulan_(1998_film)'), 'Opening Plot and cast, Matchmaker/Fa Li/Grandmother Fa/Chi-Fu', 'Mulan fails the prospective-wife test with the Matchmaker; the other family members and imperial official have separate roles.')],
1124: [(wiki('The_Emperor%27s_New_Groove'), 'Voice cast, Bucky the Squirrel', 'Bucky is identified as the squirrel who encounters Kuzco and befriends Kronk.')],
1125: [(script('atlantis-the-lost-empire'), 'Whitmore crew briefing, lines 417–433', 'Whitmore assigns geology and excavation to Moliere and demolitions to Santorini.')],
1126: [(script('lilo-and-stitch'), 'Gantu ship and Councilwoman exchange, lines 2197–2222', 'Gantu identifies himself as the pursuing ship captain and answers the Grand Councilwoman.')],
1128: [(script('brother-bear'), 'Totem ceremony and Tanana\'s guidance, lines 118–131 and 330–341', 'Tanana returns for Kenai\'s totem ceremony and later directs him toward the spirits.')],
1129: [(script('chicken-little'), 'Friends fleeing the aliens, lines 1129–1178; final movie parody, 1837–1845', 'Runt participates as a friend in the escape; the later parody explicitly uses pig/pork language for him.')],
1130: [(script('meet-the-robinsons'), 'Family tree quiz, lines 849–905', 'Wilbur identifies Franny as his mother; the tree distinguishes Lucille and Bud as Cornelius\'s parents.')],
1131: [(script('bolt'), 'Bolt searches for Penny, lines 350–370', 'Bolt names Penny as the girl he is trying to rescue and find.')],
1132: [(script('the-princess-and-the-frog'), 'Opening childhood household, lines 83–115', 'Eudora takes Tiana home and James identifies their girl\'s cooking gift to Eudora.')],
1133: [(wiki('Frozen_(2013_film)'), 'Plot coronation dignitaries and search of Elsa\'s palace; Voice cast', 'The Duke is a visiting dignitary distinct from Hans; his bodyguards join the expedition.')],
1134: [(wiki('Big_Hero_6_(film)'), 'Voice cast, Honey Lemon/Go Go/Wasabi/Fred specialties', 'Honey Lemon is the chemistry enthusiast, Wasabi specializes in lasers, Go Go in electromagnetics and Fred in monster fandom.'), 'b16-882-extra-2'],
1135: [(wiki('Encanto'), 'Voice cast, Dolores/Camilo/Antonio/Isabela', 'The four gift recipients are separately identified in the film cast.')],
1137: ['b12-sub'],
1138: [('https://disneyworld.disney.go.com/en_CA/attractions/magic-kingdom/country-bear-jamboree/', 'Show name, Grizzly Hall revue', 'Disney identifies the current attraction as Country Bear Musical Jamboree in Grizzly Hall.')],
1139: [('https://disneyworld.disney.go.com/attractions/epcot/living-with-the-land/', 'Opening greenhouse boat-tour description', 'Living with the Land is the agricultural greenhouse boat ride.'), ('https://wdpromedia.disney.go.com/media/wdpro-assets/parks-and-tickets/destinations/epcot/epcot.pdf', 'Guide page 2, The Land attractions section', 'The Land guide groups the Soarin flight and greenhouse boat attraction together. This is an older guide, corroborated by the current pavilion account.')],
1141: [('https://www.prnewswire.com/news-releases/disneys-animal-kingdom-theme-park-celebrates-25-years-showcasing-the-magic-of-nature-301805977.html', 'Disney-issued chronology, April 21 and April 22, 1998', 'The dedication is April 21; the park opens April 22, 1998.')],
1142: [(wiki('Sorcerer%27s_Hat'), 'Opening/closing dates and introduction', 'The Hat debuted in 2001 in front of the theatre and was removed in 2015.')],
1143: [('https://disneyland.disney.go.com/attractions/disneyland/disneyland-railroad/', 'Find a Station list', 'The four stations are Main Street U.S.A., New Orleans Square, Mickey\'s Toontown and Tomorrowland.')],
1144: [(wiki('Walt_Disney_World_Railroad'), 'Rolling stock, locomotive table Name / Namesake columns', 'The roster distinguishes Walter E. Disney, Roy O. Disney, Lilly Belle and Roger E. Broggie and their respective namesakes.')],
1145: [('https://disneyworld.disney.go.com/shops/disney-springs/world-of-disney/', 'Opening description', 'The official shop page advertises the world\'s largest collection of Disney merchandise at World of Disney.')],
1147: [('https://wdpromedia.disney.go.com/media/wdpro-assets/parks-and-tickets/destinations/epcot/epcot.pdf', 'Page 2, World Showcase country list', 'The guide groups Italy, American Adventure and Japan consecutively in its country-by-country tour. Older guide is corroboration, not a current operations promise.')],
1148: [('https://www.mousehacking.com/blog/tom-sawyer-island-riverboat-closed-beginning-july-7', 'July 7, 2025 update and quoted closure announcement', 'Tom Sawyer Island, the riverboat and Rivers of America closed beginning July 7, 2025.')],
1152: [('https://www.tokyodisneyresort.jp/en/tds/attraction/detail/223/', 'Journey to the Center of the Earth description and Mysterious Island location', 'The official attraction description confirms the constructed erupting volcano setting in Mysterious Island; the sponsor passage supplies its name.')],
}

def author():
    library = read('audit/source-notes.json')
    # These two attempted corroborations yielded inaccessible/replaced pages;
    # they were never imported and must not remain as purported checked notes.
    library['sources'].pop('b21-1146-1', None)
    library['sources'].pop('b21-1151-1', None)
    notes = read('audit/runs/next-shard-0021-final-template.json')
    notes['reviews'] = [r for r in notes['reviews'] if r['questionId'] in rows]
    checked = set()
    changing = {1138, 1139, 1143, 1145, 1146, 1147, 1152}
    for review in notes['reviews']:
        qid = review['questionId']
        url, locator, premise, reasons, challenge = rows[qid]
        ids = []
        for index, item in enumerate([(url, locator, premise)] + extra.get(qid, [])):
            if isinstance(item, str):
                assert item in library['sources'], item
                ids.append(item)
                continue
            source_id = f'b21-{qid}-{index}'
            source_url, source_locator, evidence = item
            library['sources'][source_id] = {
                'url': source_url, 'locator': source_locator, 'evidence': evidence,
                'checkedBy': 'Codex', 'checkedAt': '2026-11-08',
                'timeSensitive': qid in changing,
                'nextReviewAt': '2027-02-06' if qid in changing else None,
                'topics': ['Batch 21'],
                'limitations': ('Text passages inspected; no original film, audio or video playback claimed. '
                    'Wikipedia and fan transcriptions are secondary, not studio-certified transcripts. '
                    'Where D23 film entries returned only sign-in shells or official summaries omitted detail, '
                    'the detailed passage and identified corroboration carry the specific fact. '
                    'Older maps are corroboration only; current dated park questions have a scheduled recheck. '
                    'The Disney store superlative is explicitly an attributed advertisement.')
            }
            ids.append(source_id)
        checked.update(ids)
        review.update({
            'checks': ['singleAnswer', 'context', 'wording', 'noGiveaway', 'distinctFact', 'category', 'difficulty', 'scope'],
            'notes': 'Final wording and all four options reviewed. ' + challenge,
            'context': ('Original theatrical film and its identified scene/character relationship.' if qid <= 1135 else
                        'The named park and historical event, or the explicitly dated November 2026 configuration.'),
            'timeSensitive': qid in changing,
            'nextReviewAt': '2027-02-06' if qid in changing else None,
            'premise': {'reason': premise, 'sources': ids},
            'options': [{'basis': 'direct' if i == 0 else 'exclusive-inference', 'reason': reason, 'sources': ids}
                        for i, reason in enumerate(reasons)],
            'challenge': {'reviewer': 'Codex', 'at': '2026-11-08', 'premiseChecked': True,
                          'alternativesExcluded': True, 'notes': challenge}
        })
    notes['sourcesChecked'] = sorted(checked)
    save('audit/source-notes.json', library)
    save('audit/runs/next-shard-0021-evidence-notes.json', notes)

if __name__ == '__main__':
    author()
