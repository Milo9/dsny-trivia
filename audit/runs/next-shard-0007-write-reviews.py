"""Serialize the source and final-wording reviews performed by Codex in batch 7.

This file records human-readable reasoning; it does not infer verification from
the mechanical checks. Run record-many separately to validate the filled records.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from question_audit import review_template

SOURCES = {
 'brave': ('https://www.pixar.com/brave', 'The Characters: Triplets; Merida; King Fergus; Angus and the clan lords'),
 'cars': ('https://en.wikipedia.org/wiki/Cars_(film)', 'Plot: opening Rust-eze/Dinoco sponsorship contrast; final tiebreaker paragraph identifying Chick causing the King crash and Lightning returning to help'),
 'carsplot': ('https://www.imdb.com/title/tt0317219/plotsummary/', 'Synopsis: final Los Angeles race, Chick employing the PIT maneuver against the King; Lightning stopping and pushing the King'),
 'rust': ('https://www.youtube.com/watch?v=Q4sBvyM-Ruk', 'Disney Jr. official clip title: Lightning McQueen Loves Rust-eze!; corroborating title only, not a claim to have watched its video'),
 'nemo': ('https://www.pixar.com/finding-nemo', 'The Characters: Sharks (Bruce, Anchor and Chum; fish-eaters group); The Sunken Ship production section explicitly identifies Bruce as the great white'),
 'nemospecies': ('https://en.wikipedia.org/wiki/Finding_Nemo', 'Voice cast: Barry Humphries/Bruce great white; Eric Bana/Anchor hammerhead; Bruce Spence/Chum mako'),
 'darling': ('https://d23.com/a-to-z/darling/', 'Complete Darling family entry: George and Mary parents; Wendy, John and Michael children'),
 'cats': ('https://d23.com/a-to-z/aristocats-the-film/aristocats/', 'Opening synopsis: Duchess and exactly three kittens Toulouse, Berlioz, Marie; greedy butler Edgar; alley cat Thomas O\'Malley and mouse Roquefort'),
 'nightmare': ('https://news.disney.com/quiz-are-you-lock-shock-or-barrel-from-the-nightmare-before-christmas', 'Introduction explicitly names Lock, Shock and Barrel as Oogie Boogie minions and discusses capturing Sandy Claws'),
 'hunchback': ('https://d23.com/a-to-z/hunchback-of-notre-dame-the-film/', 'Synopsis: Phoebus Captain of the King guards; mutual Phoebus/Esmeralda love; Frollo Minister of Justice and Quasimodo bell-tower outsider'),
 'clopin': ('https://d23.com/a-to-z/clopin/', 'Character entry for Clopin, the gypsy leader in The Hunchback of Notre Dame'),
 'turbo': ('https://d23.com/13-disney-characters-that-make-our-spines-tingle/', 'King Candy from Wreck-It Ralph subsection: former identity Turbo, classic racing-game origin, takeover of Sugar Rush'),
 'dogs': ('https://d23.com/celebrate-lunar-new-year-with-our-favorite-disney-dogs/', 'Item 6, Dodger (Oliver & Company): head of Fagin pack, charismatic and brave leader'),
 'diablo': ('https://d23.com/ask-the-archives/films/page/13/', 'J of Los Angeles asks for unnamed characters including Maleficent raven from Sleeping Beauty; Archives answer: raven known as Diablo'),
 'rat': ('https://en.wikipedia.org/wiki/The_Great_Mouse_Detective', 'Voice cast: Vincent Price as Ratigan, explicitly a rat who dislikes being reminded; Animation: Glen Keane describes the sewer-rat design'),
 'ratscene': ('https://www.greatmousedetective.net/criminal', 'Fan transcription of original film musical scene: Bartholomew calls Ratigan a rat, Ratigan denies it, intimidated henchmen call him a mouse; corroboration of the denial, not independent biological proof'),
 'ghosts': ('https://disneyparksblog.com/disney-experiences/new-disney-haunted-mansion-wallpapers-featuring-hitchhiking-ghosts/', 'Paragraph beneath Hitchhiking Ghosts Wallpaper 2023 names the complete trio Ezra Beane, Professor Phineas Plump and Gus'),
 'thunder': ('https://d23.com/a-to-z/big-thunder-mountain-railroad/', 'Opening paragraph separately assigns Magic Kingdom version to Frontierland and Tokyo version to Westernland'),
 'street': ('https://d23.com/a-to-z/main-street-u-s-a/', 'Entry: railroad station/Town Square to Hub and castle street layout; final paragraph confirms Magic Kingdom also has Main Street'),
 'showcase': ('https://d23.com/a-to-z/world-showcase/', 'Complete entry explicitly locates the international-pavilion area at EPCOT and enumerates its countries'),
 'dole': ('https://disneyparksblog.com/disney-experiences/disney-eats-new-dole-whip-day-wallpapers-2024/', 'History bullet list: original DOLE Pineapple Whip name and introduction at Aloha Isle in 1984'),
 'fantasmic': ('https://disneyland.disney.go.com/entertainment/disneyland/fantasmic/', 'Title and When Dreams Come to Life: Disneyland Rivers of America, Mickey dreaming and defeating villains'),
 'fantasmichistory': ('https://d23.com/a-to-z/fantasmic/', 'Opening Disneyland production description and later paragraph describing separate Hollywood Studios version'),
 'apartment': ('https://d23.com/a-to-z/fire-station/', 'Fire Station entry: Town Square at Disneyland and Walt small apartment upstairs'),
 'springs': ('https://d23.com/a-to-z/disney-springs/', 'Entry: shopping/dining center replacing Downtown Disney; effective name change September 29, 2015'),
 'navi': ('https://d23.com/a-to-z/navi-river-journey/', 'Opening sentence locates May 27, 2017 attraction in Pandora at Disney Animal Kingdom'),
 'waffles': ('https://disneyparksblog.com/wdw/cooking-up-the-magic-with-a-chocolate-waffle-recipe-to-kick-off-waffle-week/', 'Waffle Instructions steps 2-6: batter preparation and iron cooking; Classic Mickey Waffles gallery caption identifies the Mickey-shaped park food'),
 'wafflebreakfast': ('https://plandisney.disney.go.com/question/recipe-mickey-waffles-370726/', 'May 28, 2018 answer: Mickey waffles each morning for breakfast and waffle-iron preparation context'),
 'boats': ('https://disneyworld.disney.go.com/en_CA/resorts/swan-hotel/amenities/', 'Disney Watercraft Transportation: Friendship Boat to EPCOT and Hollywood Studios, with Dolphin and other hotel stops'),
 'starcruiser': ('https://d23.com/7-burning-questions-answered-about-star-wars-galactic-starcruiser/', 'Questions 1 and 4: two-night immersive vacation and named Halcyon starcruiser crew; question 6 describes both nights of dining'),
 'kali': ('https://disneyworld.disney.go.com/attractions/animal-kingdom/kali-river-rapids/', 'Title, whitewater introduction and Raft Down a Rip-Roaring River section'),
 'mansion': ('https://d23.com/a-to-z/haunted-mansion/', 'Separate opening dates: Disneyland August 9, 1969 and Magic Kingdom Liberty Square October 1, 1971'),
 'mansionhistory': ('https://disneyparksblog.com/disney-experiences/hauntingly-historic-mansion-celebrates-55-years-next-week/', 'Paragraph following 1969 Disneyland opening; Florida opening in 1971; Spine-Tingling Start on the East Coast identifies Magic Kingdom'),
 'mission': ('https://disneyworld.disney.go.com/attractions/epcot/mission-space/', 'Which Mission Should I Choose: Orange Mission to Mars, Green Mission orbits Earth; Orange centrifuge simulation'),
 'test': ('https://d23.com/a-to-z/test-track/', 'Opening paragraphs: grand opening March 17, 1999; vehicles travel on outside loop at real speeds up to 65 mph'),
 'testcurrent': ('https://disneyworld.disney.go.com/attractions/epcot/test-track/', 'Current Portuguese-language page: Viajando para um amanhã mais brilhante describes road journey and electrifying high-speed run, not a stationary speed simulation'),
 'everest': ('https://d23.com/a-to-z/expedition-everest/', 'Opening sentence: Asia at Animal Kingdom, opened April 7, 2006'),
 'everestsecondary': ('https://en.wikipedia.org/wiki/Expedition_Everest', 'Opening/history: previews January 26, 2006; grand opening April 7, 2006'),
 'paris': ('https://news.disneylandparis.com/en/history/', '1992 timeline section THE GRAND OPENING OF DISNEYLAND PARIS: public opening April 12, 1992; distinguishes 2002 second park'),
 'parisarchive': ('https://d23.com/a-to-z/disneyland-paris/', 'Opening paragraph: resort and original Euro Disneyland park opening April 12, 1992'),
 'ticket': ('https://d23.com/a-to-z/e-ticket/', 'Complete entry: E introduced 1959, A/B/C books October 1955, D added 1956; E became slang for thrills'),
 'guardians': ('https://disneyparksblog.com/wdw/guardians-of-the-galaxy-cosmic-rewind-opens-at-epcot/', 'May 28, 2022 opening report: new family coaster at EPCOT Wonders of Xandar pavilion'),
 'lodge': ('https://disneyworld.disney.go.com/resorts/animal-kingdom-lodge/', 'What Makes This Resort Hotel Unique: design around four savannas; Exotic Animals explicitly includes giraffes and zebras'),
 'wilderness': ('https://d23.com/hidden-gems-from-disneys-wilderness-lodge/', 'Introduction and item 7: Yellowstone/Pacific Northwest design, Old Faithful Lodge inspiration, not African savannas'),
 'caribbean': ('https://d23.com/a-to-z/caribbean-beach-resort/', 'Entry describes Florida hotel and themed Caribbean island villages around Old Port Royale'),
 'portorleans': ('https://disneyworld.disney.go.com/resorts/port-orleans-resort-riverside/', 'What Makes This Resort Hotel Unique: rural Louisiana, Magnolia Bend/Alligator Bayou and Sassagoula River'),
 'anniversary': ('https://d23.com/details-on-walt-disney-worlds-50th-anniversary-celebration/', 'February 19, 2021 announcement, first paragraph: celebration begins October 1, 2021 and lasts 18 months'),
 'galaxy': ('https://d23.com/a-to-z/star-wars-galaxys-edge/', 'Opening-date paragraph: Disneyland May 31, 2019; Disney Hollywood Studios August 29, 2019; land named in title'),
 'dolehistory': ('https://en.wikipedia.org/wiki/Dole_Whip', 'History: Dole spokesperson explanation and Magic Kingdom debut in 1984, Disneyland in 1986'),
 'testhistory': ('https://en.wikipedia.org/wiki/Test_Track', 'History: December 19, 1998 soft opening distinguished from March 17, 1999 official opening'),
 'tickethistory': ('https://en.wikipedia.org/wiki/E_ticket', 'History: June 1959 introduction of E designation; original A/B/C books'),
 'guardianshistory': ('https://en.wikipedia.org/wiki/Guardians_of_the_Galaxy:_Cosmic_Rewind', 'History: previews and public grand opening May 27, 2022'),
 'anniversaryactual': ('https://disneyexperiences.com/app/uploads/sites/4/2022/08/fact_sheet_walt_disney_world_2022_Q3.pdf', 'PDF page 2, New Developments: October 1, 2021 actual kickoff and 18-month duration, corroborating the prior announcement'),
 'galaxyhistory': ('https://en.wikipedia.org/wiki/Star_Wars:_Galaxy%27s_Edge', 'Development and History: Hollywood Studios land opened August 29, 2019, separate from May Disneyland opening'),
}

# Per question: sources, four option rationales, separate final evidence challenge.
DATA = {
304: (['brave'], [
 'The complete triplet list is Harris, Hubert and Hamish.',
 'Fergus replaces Hubert; Fergus is their father, not one of the triplets.',
 'Angus replaces Harris; Angus is Merida horse, not a brother.',
 'Dingwall replaces Hamish and is not in the exhaustive triplet list.'
], 'Challenged the overlapping name sets individually: retaining two correct names does not make a three-name answer correct. The complete official sibling list excludes every substituted name. Main theatrical film and character category fit; this is name recall, not clan competition in 555.'),
305: (['cars','rust'], [
 'Rust-eze is the sponsorship McQueen already has in the 2006 story.',
 'Dinoco is the prestigious sponsor he wants instead, not his main sponsor in this film.',
 'The stated main sponsorship is Rust-eze, not Octane Gain.',
 'The stated main sponsorship is Rust-eze, not Vitoline.'
], 'Bound the question to the first film: later Dinoco/Rust-eze ownership developments cannot change this answer. Main sponsor is a single role; possible minor decals do not count as main sponsorship. Plot evidence is secondary, corroborated only by the official clip title; no claim to have watched that clip. This is Pixar brand trivia, so moved it from characters to pixar.'),
306: (['nemo','nemospecies'], [
 'Pixar identifies Bruce as the great white and describes the fish-abstaining shark group.',
 'Anchor is a hammerhead, so the shared fish-abstaining goal does not make him the great white.',
 'Chum is a mako, not the great white specified in the stem.',
 'The film group is Bruce, Anchor and Chum; Jaws is not a member or the named Nemo great white.'
], 'Specifically challenged Anchor and Chum: all three give up fish, so the great-white qualification is essential. Pixar identifies Bruce species; secondary cast detail corroborates the other two. Jaws is plausible shark association, not this character. Distinct from Anchor species question 2317.'),
310: (['darling'], [
 'The two male Darling children alongside Wendy are John and Michael.',
 'James and Timothy are not the two boys in the complete Darling child list.',
 'George is the father, not a brother; Edward is absent from the child list.',
 'Tom and Harry are not the two boys in the complete child list.'
], 'Checked parents versus siblings and the full two-name sets. The official complete family list excludes all three alternative pairs. 854 and 1104 ask parents; 1324 asks youngest sibling and does not explicitly supply both brothers. Medium pair-name recall; character and theatrical scope fit.'),
311: (['cats'], [
 'Duchess three kittens are Marie, Berlioz and Toulouse.',
 'Roquefort replaces Toulouse; he is the mouse helper, not a kitten.',
 'Scat Cat replaces Berlioz and is absent from the complete three-kitten list.',
 'O\'Malley replaces Marie; he is the alley cat who helps the family, not a kitten.'
], 'Challenged the two-correct/one-wrong sets, including O\'Malley later joining the family. Becoming a parental companion does not make him Duchess kitten. Original silly pet-name lists replaced with overlapping film-character sets. Other Aristocats questions concern mother identity, city, owners, music and helpers, not this list.'),
312: (['nightmare'], [
 'Disney names the minion trio Lock, Shock and Barrel.',
 'Grim, Ghost and Ghoul is not the identified trio.',
 'Trick, Treat and Terror is not the identified trio.',
 'Bone, Blood and Bite is not the identified trio.'
], 'Confirmed the group belongs to Oogie as well as doing Jack errands; those roles coexist. Official introduction explicitly supplies the full trio, excluding all invented alternative sets. Main theatrical film, character category and medium three-name recall; no same-fact question in the full Nightmare search.'),
313: (['hunchback'], [
 'Phoebus is the captain and Esmeralda reciprocates his love.',
 'Frollo is the Minister of Justice; desire for Esmeralda does not make him the captain.',
 'Clopin is not the captain whom the synopsis identifies as Phoebus.',
 'Quasimodo loves Esmeralda but is the bell-tower outsider, not the captain.'
], 'Tried Frollo and Quasimodo under the love wording: both have feelings, so retained the captain qualification and named the 1996 version. The primary synopsis establishes the captain identity and separates the competing men. 2312 is Frollo office; 547 is Esmeralda identity, so neither tests this captain identification.'),
319: (['turbo'], [
 'King Candy is Turbo, originally from a different racing game.',
 'His origin is the established racer Turbo, not an anonymous Sugar Rush glitch.',
 'He originates in a classic racing game, not Hero\'s Duty.',
 'He took over Sugar Rush from outside; he was not originally a deleted Sugar Rush character.'
], 'Distinguished original identity from the later Cy-Bug/virus form and his manipulation of game code. Those events do not turn his true origin into the glitch distractor. The official villain subsection explicitly describes the outsider racer. Other Ralph questions ask games, Vanellope, hubs, and tools, not this reveal.'),
320: (['cars','carsplot'], [
 'Chick intentionally damages the King during the tiebreaker.',
 'Lightning stops to help the King finish after the crash; he does not cause it.',
 'The incident is attributed to Chick, not Finn McMissile.',
 'The incident is attributed to Chick, not Francesco Bernoulli.'
], 'The original main-rival wording also fits the King as a title rival. Replaced it with a specific attributable action, removed the named victim from the options, and fixed the film year. Two secondary plot accounts agree; primary screenplay fetch failed and no primary viewing is claimed. Unique action attribution excludes the alternatives. Cars 2 nationality and Cars 3 rival are different facts.'),
321: (['dogs'], [
 'Disney explicitly identifies Dodger as the head of Fagin pack.',
 'Einstein is not the dog identified as that pack head.',
 'Tito is not the dog identified as that pack head.',
 'Francis is not the dog identified as that pack head.'
], 'The head-of-pack role decides the answer, not subjective smoothness or bravery. The primary character passage names the leader; other gang members cannot fill that singular identity in this film. Tito breed in 865 and Sykes guard-dog breeds in 2494 are different facts. Character category and medium recall fit.'),
323: (['diablo'], [
 'The Walt Disney Archives explicitly says the raven is known as Diablo.',
 'Corvus is not the name given in the Archives answer.',
 'Raven is a species/descriptor here, not the specific name given by the Archives.',
 'Shade is not the name given in the Archives answer.'
], 'Checked the possibility that the bird is unnamed in dialogue: the question asks his character name, not a spoken introduction. The Archives specifically answers this exact Sleeping Beauty naming question, so no reliance on the live-action Diaval or on a Villains novel is needed. Hard ancillary-character name recall is appropriate.'),
325: (['rat','ratscene'], [
 'The cast/design account identifies Ratigan as a rat, despite his denial.',
 'The henchmen mouse claim is appeasement after his anger, not the true species.',
 'He is identified as a rat, not a shrew.',
 'He is identified as a rat, not a vole.'
], 'Did not treat Bartholomew intoxicated line alone as biological proof. The secondary cast/design account independently identifies a rat; the fan-reproduced film scene establishes why the denial/mouse answer is tempting. No primary scene viewing claimed. Ratigan name is a natural character clue, not an artificial answer repetition. 2481 asks an unrelated Lady and the Tramp intruder.'),
328: (['cats'], [
 'The synopsis expressly names Madame Bonfamille greedy butler Edgar.',
 'Georges is not the named butler Edgar.',
 'Napoleon is not the named butler Edgar.',
 'Lafayette is not the named butler Edgar.'
], 'Removed the unneeded surname test: the readily accessible primary synopsis supports Edgar, while the indexed merchandise PDF for Balthazar could not be fully fetched. This is a narrower supported identification, not a claim that Balthazar is wrong. Four first names are parallel. Other cat/horse/dog questions mention Edgar but do not identify the butler by role.'),
331: (['ghosts'], [
 'Gus, Ezra and Phineas are the complete hitchhiking trio; order does not matter.',
 'The Hatbox Ghost replaces Phineas and is not in the listed hitchhiking trio.',
 'Master Gracey replaces Gus and is not in the listed hitchhiking trio.',
 'The Ghost Host replaces Ezra and is not in the listed hitchhiking trio.'
], 'Distinguished the attraction from the film cast and from other mansion ghosts. The complete primary trio list excludes each substituted character even if that character also haunts the Mansion. Short names legitimately match full names Ezra Beane and Professor Phineas Plump. Changed implausible invented groups into plausible overlapping sets; hard group-name recall fits.'),
336: (['thunder'], [
 'The Magic Kingdom version is expressly in Frontierland.',
 'Tomorrowland is not the assigned land for this Magic Kingdom attraction.',
 'Adventureland is not the assigned land for this Magic Kingdom attraction.',
 'Fantasyland is not the assigned land for this Magic Kingdom attraction.'
], 'Checked park-specific variation: Tokyo Westernland cannot answer a Magic Kingdom question. The entry explicitly distinguishes the versions, not merely an assumed Western theme. Other Frontierland questions test Country Bear, Disneyland Old West design, or Paris Phantom Manor; they do not supply this ride-to-land link. Easy local-map recall.'),
337: (['street'], [
 'Main Street, U.S.A. is the named entry street running toward the castle.',
 'Main Boulevard is not the documented name of that street.',
 'Disney Way is not the documented name of that street.',
 'Fantasyland Road is not the documented name of that street.'
], 'Kept Magic Kingdom distinct from Tokyo World Bazaar and Shanghai Mickey Avenue. Main Street source describes the entry-to-hub layout and explicitly includes the Florida park. 1143 asks Disneyland railroad station, 1354 asks Marceline inspiration; neither supplies a new Magic Kingdom street identity. Easy naming with plausible street-style alternatives.'),
338: (['showcase'], [
 'World Showcase is explicitly the EPCOT international-pavilion area.',
 'Magic Kingdom is not the park assigned to that named area.',
 'Animal Kingdom is not the park assigned to that named area.',
 'Hollywood Studios is not the park assigned to that named area.'
], 'Not a claim that other parks lack international influences: the proper-named World Showcase area is the exclusive EPCOT association. 776 asks country count and pavilion questions ask individual placements; 1193 asks Walt last filmed concept presentation, a historical planning fact. Easy park recognition and parks scope fit.'),
340: (['dole','dolehistory'], [
 'The primary history identifies DOLE Whip, originally DOLE Pineapple Whip, with the 1984 Aloha Isle introduction.',
 'Citrus Swirl is not the named product in that documented introduction.',
 'Mickey Bar is not the pineapple soft-serve identified in the 1984 entry.',
 'Tropical Float is not the documented product name; a serving format is not the brand introduced.'
], 'Removed the dairy-implying ice cream label and vague beloved wording. Final stem binds the product to a historical venue/year; the source names that product directly. A float may contain the product but is not its name. Castaway Cay availability in 739 is separate from this Aloha Isle introduction and pineapple identity.'),
345: (['fantasmic','fantasmichistory'], [
 'The Disneyland show page names Fantasmic! and describes Mickey confronting villains.',
 'SpectroMagic is not the production named by the Disneyland show page.',
 'World of Color is a separate production, not this Disneyland Mickey dream show.',
 'Illuminations is not the production named by the Disneyland show page.'
], 'Checked the specific Disneyland version against the official current description and the historical entry. World of Color has water effects but does not become this named Disneyland production. 1477 asks the Hollywood Studios version; shared title does not establish the second park location. Retained park-specific coverage, with a scheduled recheck for changeable entertainment.'),
346: (['apartment'], [
 'Walt apartment was upstairs from the Disneyland fire station.',
 'The Opera House is not the building identified for that apartment.',
 'City Hall is not the building identified for that apartment.',
 'The Emporium is not the building identified for that apartment.'
], 'Changed to historical occupancy and parallel building names; removed the much longer correct option and the Town Hall/City Hall near-duplicate distractors. The entry identifies the apartment as upstairs in one specific building; it is not an assertion about every planned Disney apartment. Other Main Street questions concern street geography or inspiration.'),
347: (['springs'], [
 'Disney Springs became the replacement name in September 2015.',
 'Disney Town is not the documented replacement name.',
 'Disney Plaza is not the documented replacement name.',
 'Disney Boulevard is not the documented replacement name.'
], 'Bound the question to the 2015 renaming instead of an unbounded current name. Similar shopping districts at other resorts do not answer a Walt Disney World renaming. All options have a parallel Disney/place form. 1145 asks the largest character store within the district, not this name change.'),
348: (['navi'], [
 'The named attraction is at Disney Animal Kingdom, in Pandora.',
 'EPCOT is not the park assigned to that attraction.',
 'Hollywood Studios is not the park assigned to that attraction.',
 'Magic Kingdom is not the park assigned to that attraction.'
], 'Checked specifically the gentle Na\'vi River Journey, not Avatar Flight of Passage or a planned Avatar experience elsewhere. Primary entry explicitly gives the park. 2635 asks the Shaman figure, 1359 asks Pandora land and 91 asks park conservation purpose, so these require different facts. Easy location recall.'),
349: (['waffles','wafflebreakfast'], [
 'Mickey waffles are the breakfast item; waffle batter is cooked in an iron.',
 'Pretzels may be Mickey-shaped but are dough products, not this batter-and-iron breakfast item.',
 'Popcorn is popped corn, not batter cooked in a patterned iron.',
 'Bread is a baked dough product, not the named iron-cooked batter breakfast item.'
], 'The original generic Mickey-shaped treat wording admitted pretzels as well as waffles. Challenged the final preparation qualification: warm snacks or Mickey shapes alone do not suffice. The recipe cooking method and Mickey-waffle gallery support the answer, with breakfast context corroborated by planDisney. No identical food-preparation fact elsewhere in bank.'),
351: (['boats'], [
 'The official Swan amenities page calls them Friendship Boats.',
 'Disney Water Taxis is not the specific name Disney uses for these boats on that page.',
 'Resort Launches is not the specific name assigned to this service.',
 'EPCOT Ferries is not the specific name assigned to this service.'
], 'Explicitly asks Disney\'s name so that a loose generic water-taxi description cannot also qualify. Source lists the same parks and hotel route under Friendship Boats, not merely boats somewhere on property. The common word boats is shared by the question and multiple options and does not disclose Friendship. Parks transport scope fits; scheduled recheck for route/name changes.'),
352: (['starcruiser'], [
 'The two-night Halcyon vacation experience was Star Wars: Galactic Starcruiser.',
 'Rise of the Resistance is not the named two-night Halcyon vacation.',
 'Smugglers Run is not the named two-night Halcyon vacation.',
 'Star Tours is not the named two-night Halcyon vacation.'
], 'Removed The Halcyon Hotel, a potentially defensible informal name for the same experience, and replaced invented hotel names with comparable real Star Wars titles. Final wording is historical, does not suggest bookings remain open and does not depend on opening/closing date precision. The primary account explicitly identifies this two-night product and its ship.'),
353: (['kali'], [
 'The official whitewater rafting attraction is Kali River Rapids.',
 'Expedition Splash is not the documented title of that attraction.',
 'Congo Cascade is not the documented title of that attraction.',
 'White Water Run is not the documented title of that attraction.'
], 'Checked the type and park, rather than assuming every Animal Kingdom water attraction is rafting. The primary description explicitly pairs the title with whitewater and raft travel. 2634 asks the fictional river/storyline and does not state that this is the park whitewater ride. Easy recognition; parks category and scope fit.'),
354: (['mansion','mansionhistory'], [
 'Magic Kingdom Haunted Mansion opened October 1, 1971.',
 '1969 is Disneyland opening, not Magic Kingdom opening.',
 '1975 is not the documented Magic Kingdom opening year.',
 '1980 is not the documented Magic Kingdom opening year.'
], 'Challenged the common Disneyland/Florida confusion: two primary histories explicitly separate the 1969 and 1971 openings. Opening is a unique dated event and excludes other years without assuming every Haunted Mansion opened together. 599 asks land and 398 asks Roy death; neither tests this opening date. Historical fact, no routine recheck needed.'),
355: (['mission'], [
 'Mission: SPACE offers the Orange Mars simulation.',
 'Cosmic Rewind is not the attraction explicitly offering the named Orange Mission.',
 'Test Track is not the attraction explicitly offering the named Orange Mission.',
 'Spaceship Earth is not the attraction explicitly offering the named Orange Mission.'
], 'Specified orange: green orbits Earth, so the blanket ride description needed context. Replaced the repeated Mission word with version after the warning was recorded unresolved. The primary page names both programs and destinations; the unique Orange/Mars program assignment excludes other attractions, not just their space themes. Medium program recognition and parks scope fit.'),
356: (['test','testcurrent','testhistory'], [
 'Test Track had its grand opening in 1999 and takes cars onto a real high-speed loop outside.',
 'Mission: SPACE is not the 1999 car-loop attraction named in this history.',
 'Spaceship Earth is not the 1999 car-loop attraction named in this history.',
 'Journey Into Imagination is not the 1999 car-loop attraction named in this history.'
], 'Removed simulated speeds: the vehicles really move around the outdoor track. Distinguished the December 1998 soft opening from the documented 1999 grand opening and checked the current page does still describe a high-speed road run after retheming. The 65 mph question 2217 and sponsor question 2216 ask different numeric/production facts. No direct Test-word giveaway remains.'),
357: (['everest','everestsecondary'], [
 'Expedition Everest opened in 2006; the primary entry dates it April 7.',
 '2004 is not the documented opening year.',
 '2008 is not the documented opening year.',
 '2010 is not the documented opening year.'
], 'Checked soft-opening ambiguity: secondary history gives previews and grand opening both in 2006, agreeing with the primary date, so year wording stays unambiguous. 922 asks Asia location, 394 asks Pixar acquisition; sharing 2006 does not repeat the event. Historical year recall is medium; no future status claim.'),
358: (['paris','parisarchive'], [
 'The original Paris resort/park opened April 12, 1992.',
 '1989 is not the original Paris opening year.',
 '1995 is not the original Paris opening year.',
 '1999 is not the original Paris opening year.'
], 'Confirmed original Euro Disney opening, not 1994 name change, 2002 second park, or 2026 rebranding. Operator timeline and Archives agree on 1992. 114 asks the name-change date, 111 Shanghai opening, and 463 an Academy Award year; they require different facts. Historical opening year is medium.'),
359: (['ticket','tickethistory'], [
 'The E coupon was added in 1959 and became the thrill-ride expression.',
 'A tickets were present in the original 1955 book, not introduced in 1959.',
 'B tickets were present in the original 1955 book, not introduced in 1959.',
 'C tickets were present in the original 1955 book, not introduced in 1959.'
], 'Corrected the original-system implication: the first 1955 books had no E coupon. The primary chronology independently lists all three distractor letters before E was added, and defines the slang usage. All answers now parallel coupon names. Historical parks vocabulary; no same-fact question in the full parks digest.'),
360: (['guardians','guardianshistory'], [
 'The 2022 opening report names Cosmic Rewind at Wonders of Xandar.',
 'Remy\'s Ratatouille Adventure is not the new Xandar attraction named in that report.',
 'Frozen Ever After is not the new Xandar attraction named in that report.',
 'Journey Into Imagination With Figment is not the new Xandar attraction named in that report.'
], 'Removed Guardians from the stem and replaced short invented coaster names with comparable real attraction titles. The source binds the one new attraction to both pavilion and year. 913 tests vehicle terminology and 2636 song count; neither provides the Xandar/2022 opening context. Medium venue/year recognition; fixed historical event.'),
361: (['lodge','wilderness','caribbean','portorleans'], [
 'Animal Kingdom Lodge design centers on savannas and its wildlife list includes giraffes and zebras.',
 'Wilderness Lodge was designed around the American Northwest/Yellowstone, not African savannas.',
 'Caribbean Beach is designed as Caribbean island villages, not the giraffe/zebra savanna lodge.',
 'Port Orleans recreates Louisiana riverside settings, not the African savanna lodge.'
], 'Challenged whether generic wildlife or a hotel in the Animal Kingdom resort area would suffice: the question requires design around giraffe/zebra savannas. All four resort design accounts distinguish the concepts. Removed invented Safari/Savanna hotel distractors and the repeated animal word. 900 asks Northwest lobby design; neither full question names the other hotel association.'),
364: (['anniversary','anniversaryactual'], [
 'The celebration began October 1, 2021.',
 '2020 precedes the stated beginning.',
 '2022 falls during the event, but is not its beginning year.',
 '2019 precedes the stated beginning.'
], 'Original celebrate wording allowed 2022 during an 18-month event. Final begin wording excludes that tempting alternative; the primary announcement explicitly supplies both date and duration. This is not asking when every celebration day occurred or when Guardians opened. Medium historical-year recall; the start cannot change.'),
366: (['galaxy','galaxyhistory'], [
 'Galaxy\'s Edge opened at Hollywood Studios on August 29, 2019.',
 'Star Wars Zone is not the documented land name.',
 'The Outer Rim is not the documented name of this 2019 land opening.',
 'Force Land is not the documented land name.'
], 'Fixed the historical opening context and distinguished the Disneyland May opening from Hollywood Studios August opening. The proper-name land is Galaxy\'s Edge, while Outer Rim is a broader in-universe region, not an alternative official title here. 1467 and 778 ask particular rides within the land, not this opening/name event.'),
}

CHANGING = {336,337,338,345,348,351,353,355,356,361}
BASES = {
304: ['direct','exhaustive-list','exhaustive-list','exhaustive-list'],
306: ['direct','contradiction','contradiction','exhaustive-list'],
310: ['direct','exhaustive-list','contradiction','exhaustive-list'],
311: ['direct','contradiction','exhaustive-list','contradiction'],
312: ['direct','exhaustive-list','exhaustive-list','exhaustive-list'],
313: ['direct','contradiction','exclusive-inference','contradiction'],
319: ['direct','contradiction','contradiction','contradiction'],
320: ['direct','contradiction','exclusive-inference','exclusive-inference'],
325: ['direct','contradiction','exclusive-inference','exclusive-inference'],
331: ['direct','exhaustive-list','exhaustive-list','exhaustive-list'],
359: ['direct','contradiction','contradiction','contradiction'],
361: ['direct','contradiction','contradiction','contradiction'],
364: ['direct','contradiction','contradiction','contradiction'],
}

bank = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
plan = json.loads((ROOT/'audit/runs/next-shard-0007-plan.json').read_text())
assert set(DATA) == set(plan['questionIds']) & bank.keys()
out = ROOT/'audit/runs/next-shard-0007-reviews'
out.mkdir(exist_ok=True)
reviews = []
for qid, (keys, reasons, challenge) in DATA.items():
    q = bank[qid]
    r = review_template(q)
    r.update(reviewer='Codex', at='2026-11-06', manual={k: True for k in r['manual']})
    r['notes'] = challenge + ' Full topic digests, ranked comparisons, both category digests, and additional cross-bank title/name searches were read for distinctness; only this saved plan is in scope.'
    refs = [{'url': SOURCES[k][0], 'locator': SOURCES[k][1]} for k in keys]
    v = r['verification']
    v.update(context=q['question']+' English-language Disney version; park/venue/version qualifications are literal. Historical events are reviewed as historical events.', timeSensitive=qid in CHANGING, nextReviewAt='2027-02-04' if qid in CHANGING else None)
    v['premise'] = {'reason': reasons[0]+' The cited locator establishes the named role, list, place, preparation, or event in the final stem.', 'sources': refs}
    v['challenge'] = {'reviewer': 'Codex', 'at': '2026-11-06', 'premiseChecked': True, 'alternativesExcluded': True, 'notes': challenge}
    bases = BASES.get(qid, ['direct','exclusive-inference','exclusive-inference','exclusive-inference'])
    for i, option in enumerate(v['options']):
        option.update(basis=bases[i], reason=reasons[i], sources=refs)
    (out/f'{qid}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    reviews.append(r)
(out/'all.json').write_text(json.dumps(reviews, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Wrote {len(reviews)} final-wording schema-2 reviews; import all.json with record-many.')
