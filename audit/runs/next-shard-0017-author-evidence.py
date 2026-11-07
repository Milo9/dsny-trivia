"""Save explicitly authored passage assessments; does not edit question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8'))
def write(p, v): (ROOT / p).write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# ID, inspected URL, locator, evidence/premise, wrong-option exclusions, separate challenge.
D = [
(902,'https://d23.com/11-real-life-landmarks-that-inspired-epcot-world-showcase/','Sections 4, 5, 8 and 9: Germany, Italy, Morocco and France',
 'Italy contains the St. Mark\'s campanile replica.',
 ['France\'s landmark here is the Eiffel Tower, not this Venetian campanile.','Germany\'s landmark is St. George and the Dragon, not this campanile.','Morocco\'s tower is the Koutoubia minaret, not this campanile.'],
 'Other pavilions have towers, but the named Venetian original fixes Italy. #433 asks a shipbuilding country, a separate fact.'),
(903,'https://d23.com/11-real-life-landmarks-that-inspired-epcot-world-showcase/','Sections 2, 3, 7 and 11; Japan waterside gate paragraph',
 'Japan\'s torii gate welcomes guests from World Showcase Lagoon.',
 ['China\'s Gate of the Golden Sun and Temple of Heaven are different structures, not this torii.','Norway\'s distinctive wooden structure is the Stave Church, not the lagoon torii.','Canada\'s landmark is Hotel du Canada, not this torii.'],
 'Challenged China\'s gate as a competing answer: the source distinguishes its named gate from the Japanese torii and waterside position.'),
(904,'https://d23.com/11-real-life-landmarks-that-inspired-epcot-world-showcase/','Sections 2, 4, 10 and 11: pavilion architecture',
 'The Stave Church Gallery is in Norway.',
 ['Germany\'s town-square pavilion is not the location of this named gallery.','The United Kingdom\'s architectural sequence includes a Tudor pub, not this gallery.','Canada\'s chateau-inspired pavilion is not this gallery\'s location.'],
 'The gallery\'s exhibit has changed from Frozen to Viking artifacts; the question tests its Norwegian location, not its changing exhibit.'),
(905,'https://disneyland.disney.go.com/attractions/disneyland/mr-toads-wild-ride/','Toad Rage; A One-of-a-Kind Drive',
 'Mr. Toad\'s Wild Ride follows J. Thaddeus Toad on a destructive motorcar journey based on Wind in the Willows.',
 ['Alice in Wonderland follows Alice rather than this named amphibian\'s motorcar journey.','Pinocchio\'s Daring Journey follows the puppet rather than Toad.','Snow White\'s Enchanted Wish follows Snow White rather than Toad.'],
 'The amphibian and reckless motorcar premise uniquely identifies Toad. Ride is generic vocabulary and does not reveal Mr. Toad; #317 asks the Alice vehicle, a different fact.'),
(906,'https://disneyland.disney.go.com/attractions/disney-california-adventure/radiator-springs-racers/','Cruise Through Radiator Springs; Ready, Get Set, Go',
 'Radiator Springs Racers tours Ornament Valley and then stages a race through the rock formations.',
 ['Luigi\'s Rollickin\' Roadsters is not the identified Ornament Valley road race.','Mater\'s Junkyard Jamboree is not the identified Ornament Valley road race.','Incredicoaster is not the identified Ornament Valley road race.'],
 'Seeing the same mountains from Cars Land is not racing through the valley. The source expressly links the tour and competitive road course to Racers; #2237 and #2240 ask capacity and opening year.'),
(907,'https://d23.com/a-to-z/world-of-color/','Opening entry: Paradise Bay and June 11, 2010',
 'World of Color opened on Paradise Bay at Disney California Adventure in 2010.',
 ['Fantasmic! is not the named 2010 Paradise Bay debut.','Harmonious is not the named 2010 Paradise Bay debut.','Wondrous Journeys is not the named 2010 Paradise Bay debut.'],
 'Historical debut wording avoids treating the latest World of Color version as permanent. #2238 asks the 2023 ONE update, which is a separate version-name fact.'),
(909,'https://disneyland.disney.go.com/attractions/disneyland/storybook-land-canal-boats/','Opening; Mini Magic list of scale models',
 'Storybook Land Canal Boats tours miniature movie locales including Arendelle, Agrabah and the dwarfs\' cottage.',
 ['Jungle Cruise is not this named tour of scale-model Disney movie villages.','It\'s a Small World depicts singing children and nations, not this catalogue of miniature movie villages.','Mark Twain Riverboat tours the frontier river, not this catalogue of miniature movie locales.'],
 'Small World also has small figures, so the specific animated-film settings and miniature model architecture are decisive. Boat is not a unique answer clue because the alternatives are boat attractions too.'),
(910,'https://disneyworld.disney.go.com/attractions/magic-kingdom/enchanted-tiki-room/','Opening; A Polynesian Paradise',
 'The Enchanted Tiki Room features a musical cast of tropical birds and flowers.',
 ['The Hall of Presidents presents presidents, not this tropical chorus.','Country Bear Musical Jamboree presents bears, not this tropical chorus.','Carousel of Progress presents an American family, not this tropical chorus.'],
 'Removed tiki from the stem. A singing bear or human musical scene does not satisfy the combined bird-and-flower cast; #1475 asks the Disneyland first-Animatronics milestone.'),
(912,'https://thewaltdisneycompany.com/news/how-disney-imagineers-advanced-omnimover-technology-for-guardians-of-the-galaxy-cosmic-rewind/','Second paragraph: Omnimover examples',
 'Disney identifies Spaceship Earth as an attraction using the Omnimover ride system.',
 ['Monorail is not the attraction\'s named Omnimover system.','A trackless rover is not the attraction\'s named system.','A boat flume is not the attraction\'s named system.'],
 'The attraction\'s elevated track does not turn it into the resort Monorail. Disney expressly names Spaceship Earth as an Omnimover example; #913 tests the newer coaster system.'),
(913,'https://thewaltdisneycompany.com/news/how-disney-imagineers-advanced-omnimover-technology-for-guardians-of-the-galaxy-cosmic-rewind/','Second paragraph: first Omnicoaster and controlled rotation',
 'Disney calls Cosmic Rewind\'s coaster system an Omnicoaster, with controlled vehicle rotations.',
 ['Omnimover is the older system whose technology was advanced for this coaster; it is not the new system name.','Trackless dark ride does not name this rail-based coaster system.','Water coaster does not name this indoor space-themed system.'],
 'The old wording confused a system name with vehicle names. The final wording tests Disney\'s term for the coaster; derivation from Omnimover does not make that older term the answer.'),
(914,'https://disneyworld.disney.go.com/en_CA/attractions/animal-kingdom/gorilla-falls-forest-exploration-trail/','Gorillas in Your Midst: Pangani Forest',
 'Gorilla Falls Exploration Trail follows paths through Pangani Forest with African animals.',
 ['Maharajah Jungle Trek is the Anandapur Asian forest trail, not Pangani Forest.','Discovery Island Trails is not the named Pangani Forest trail.','Oasis Exhibits is not the named Pangani Forest trail.'],
 'Removed gorilla from the stem. Africa/Pangani distinguish this trail from the Asian tiger trail #915, so both animal-area facts remain separate.'),
(915,'https://disneyworld.disney.go.com/attractions/animal-kingdom/maharajah-jungle-trek/','Explore a Mystical Forest: Asian tigers; Anandapur Royal Forest',
 'Maharajah Jungle Trek is a self-guided Anandapur forest trail featuring Asian tigers.',
 ['Gorilla Falls is the African Pangani Forest trail, not the tiger trail.','Discovery Island Trails is not the named Asian tiger trail.','Wild Africa Trek is an African experience, not the Anandapur tiger trail.'],
 'General wildlife walking does not suffice: the conjunction of Asia and tiger habitats fixes Maharajah. This does not duplicate #914\'s Pangani Forest identification.'),
(916,'https://disneyworld.disney.go.com/attractions/magic-kingdom/tomorrowland-speedway/','Drivers, Start Your Engines; Designed for Smaller Racers',
 'Tomorrowland Speedway lets Magic Kingdom guests steer miniature gas-powered race cars.',
 ['Autopia is not the named Magic Kingdom attraction.','Test Track is not the named Magic Kingdom attraction.','Radiator Springs Racers is not the named Magic Kingdom attraction.'],
 'Autopia also permits driving, but at Disneyland; Test Track is at EPCOT and Racers at California Adventure. Removed Tomorrowland from the stem to avoid giving away the name.'),
(917,'https://disneyworld.disney.go.com/attractions/magic-kingdom/prince-charming-regal-carrousel/','An Authentic Treasure',
 'Prince Charming Regal Carrousel was built in 1917 by the Philadelphia Toboggan Company, before coming to Magic Kingdom.',
 ['Mad Tea Party is not the historic Philadelphia Toboggan Company attraction identified here.','Dumbo the Flying Elephant is not that historic attraction.','Astro Orbiter is not that historic attraction.'],
 'The former question said carousel with only one carousel option. The final asks the documented manufacturer/year provenance, without inventing an origin story for the other rides.'),
(918,'https://d23.com/a-to-z/richard-f-irvine-riverboat/','Final sentence: renamed after 1996 rehab',
 'The Richard F. Irvine riverboat was renamed Liberty Belle after its 1996 refurbishment.',
 ['Mark Twain is the Disneyland vessel, not the 1996 replacement name.','Admiral Joe Fowler was a different Magic Kingdom riverboat, retired in 1980.','Molly Brown is not the recorded replacement name for Richard F. Irvine.'],
 'Original Richard F. Irvine distractor was an earlier name for the same vessel, and present tense ignored closure. The final asks specifically for the 1996 new name; all four options are vessel names.'),
(919,'https://disneyworld.disney.go.com/pt-br/attractions/magic-kingdom/haunted-mansion/','Opening attraction description: Doom Buggy',
 'Magic Kingdom\'s Haunted Mansion ride vehicle is called a Doom Buggy.',
 ['Ghost Coaches is not the identified vehicle name.','Hauntmobiles is not the identified vehicle name.','Spirit Seats is not the identified vehicle name.'],
 'Scoped to Magic Kingdom rather than every international Mansion variant. The Portuguese official page retains the English proper name Doom Buggy; plural Doom Buggies names the vehicles.'),
(922,'https://disneyworld.disney.go.com/destinations/animal-kingdom/','Asia heading: Expedition Everest; Africa and Discovery Island lists',
 'The official Animal Kingdom park directory places Expedition Everest in Asia.',
 ['Africa is a different mapped land, not Everest\'s location.','DinoLand U.S.A. is a different mapped land, not Everest\'s location.','Discovery Island is a different mapped land, not Everest\'s location.'],
 'The coaster\'s Himalayan story is consistent with Asia, but location is verified from the current park directory and historic map text rather than inferred from geography. #357 asks opening year and #1621 asks a cruise deployment continent.'),
(923,'https://disneyworld.disney.go.com/attractions/magic-kingdom/swiss-family-treehouse/','At Home in the Sky',
 'Swiss Family Treehouse lets guests climb into open-air living quarters furnished from salvaged shipwreck articles.',
 ['Tom Sawyer Island is not the identified elevated Robinson home.','The Many Adventures of Winnie the Pooh is not this walk-through home.','Country Bear Musical Jamboree is not this walk-through home.'],
 'Tom Sawyer Island once had structures to explore, but the wreck-salvaged elevated dwelling specifically identifies the Robinson attraction. Removed Swiss/chalet/treehouse words from the stem.'),
(924,'https://disneyland.disney.go.com/attractions/disneyland/roger-rabbits-car-toon-spin/','Toontown\'s Newest Private Eye',
 'Roger Rabbit\'s Car Toon Spin is in Mickey\'s Toontown.',
 ['Fantasyland is not the location named for this attraction.','Tomorrowland is not the location named for this attraction.','New Orleans Square is not the location named for this attraction.'],
 'Car Toon is part of the ride\'s title, not an explicit statement of the land. #1168 asks Toontown\'s debut year/design history, which does not establish Roger Rabbit\'s location.'),
(925,'https://disneyland.disney.go.com/attractions/disneyland/mark-twain-riverboat/','Along the Mississippi; Alternate Adventures',
 'Mark Twain Riverboat is the paddle-wheel vessel touring Disneyland\'s Rivers of America.',
 ['Liberty Belle is the renamed Magic Kingdom boat, not the Disneyland paddle-wheeler.','Sailing Ship Columbia shares the river route but is a sailing ship, not the paddle-wheeler.','Admiral Joe Fowler was a Magic Kingdom vessel, not this Disneyland boat.'],
 'Columbia also circles the river, so paddle-wheel is essential. Standardized its official name. The other riverboats make the generic vessel wording insufficient to reveal the answer.'),
(926,'https://d23.com/about-walt-disney/','Birth and parentage paragraph',
 'Walt Disney was born December 5, 1901.',
 ['July 17 is not his documented birth date.','October 1 is not his documented birth date.','November 18 is not his documented birth date.'],
 'Distinguished Walt\'s birthday from Disneyland, Florida and Mickey anniversary dates. Exact full date excludes the three other days; #118 tests the city.'),
(927,'https://d23.com/a-to-z/disney-elias/','Opening: Father of Walt Disney',
 'Elias Disney was Walt Disney\'s father.',
 ['Roy is not the father identified in this family record.','Herbert is not the father identified in this family record.','Raymond is not the father identified in this family record.'],
 'Walt\'s middle name Elias does not itself prove fatherhood; the entry explicitly names the relationship. #928 asks the other parent, a separate fact.'),
(928,'https://d23.com/about-walt-disney/','Birth and parentage paragraph',
 'Flora Call Disney was Walt\'s mother.',
 ['Lillian was Walt\'s wife, not his mother.','Ruth is not the mother identified in the parentage record.','Edna is not the mother identified in the parentage record.'],
 'Distinguished maternal parentage from other Disney women; the source identifies both mother and wife. The father question does not establish the mother\'s name.'),
(929,'https://d23.com/about-walt-disney/','July 13, 1925 marriage paragraph',
 'Walt married Lillian Bounds; Bounds was her maiden surname.',
 ['Miller is not Lillian\'s maiden surname in the marriage record.','Smith is not Lillian\'s maiden surname in the marriage record.','Taylor is not Lillian\'s maiden surname in the marriage record.'],
 'Original options repeated Lillian and answered a surname question with full names. Final options are parallel surnames; #1372 tests first name and #1180 marriage year.'),
(930,'https://d23.com/a-to-z/plane-crazy-film/','Opening first-made/third-released statement',
 'Plane Crazy was the first Mickey Mouse cartoon made, before Steamboat Willie\'s release.',
 ['The Band Concert cannot be the first-produced Mickey cartoon because the source assigns that unique place to Plane Crazy.','Mickey\'s Follies cannot occupy that unique first-production place.','The Karnival Kid cannot occupy that unique first-production place.'],
 'Production, public preview and sound release order differ. The museum corroborates Plane Crazy then Gaucho then Willie; the final wording asks production, not the first sound release.'),
(931,'https://d23.com/a-to-z/gallopin-gaucho-the-film/','Opening second-produced statement',
 'The Gallopin\' Gaucho was the second Mickey cartoon produced, between Plane Crazy and Steamboat Willie.',
 ['The Opry House is not the uniquely identified second-produced cartoon.','The Barn Dance is not the uniquely identified second-produced cartoon.','The Chain Gang is not the uniquely identified second-produced cartoon.'],
 'The museum independently gives the first-three production sequence. The later sound release of Gaucho does not move its original production after Willie.'),
(932,'https://d23.com/a-to-z/skeleton-dance-the-film/','Opening: first Silly Symphony, 1929',
 'The Skeleton Dance was the first Silly Symphony.',
 ['Flowers and Trees was released in 1932, after the 1929 first.','The Old Mill was released in 1937, after the 1929 first.','Three Little Pigs was released in 1933, after the 1929 first.'],
 'First Silly Symphony is distinct from first Technicolor cartoon, first Oscar and first multiplane film. The museum history corroborates the first-title attribution.'),
(933,'https://d23.com/a-to-z/wise-little-hen-the-film/','Opening release/debut paragraph',
 'Donald Duck debuted in The Wise Little Hen in June 1934.',
 ['Orphan\'s Benefit is not his initial debut; Disney assigns that distinction to Wise Little Hen.','The Band Concert is not his initial debut.','Mickey\'s Service Station is not his initial debut.'],
 'Later ensemble appearances also feature Donald; appearance is not debut. Removed the series-label clue since the three distractors are Mickey shorts. Disney\'s Donald character entry corroborates the debut.'),
(934,'https://www.waltdisney.org/blog/ten-things-not-miss-mickey-mouse-walt-world','Section 4: original drawings from The Karnival Kid',
 'Mickey speaks his first dialogue, Hot dogs, as a vendor in The Karnival Kid.',
 ['Steamboat Willie has earlier sounds but not his first spoken dialogue.','Plane Crazy is earlier and does not contain his first spoken dialogue.','The Gallopin\' Gaucho is earlier and does not contain his first spoken dialogue.'],
 'The museum distinguishes grunts/squeaks from actual dialogue. D23\'s Karnival Kid entry independently identifies the first-speaking short.'),
(935,'https://d23.com/about-walt-disney/','December 21, 1937 Carthay Circle premiere paragraph',
 'Snow White and the Seven Dwarfs premiered at Carthay Circle Theatre in 1937.',
 ['Pinocchio premiered in 1940, not at the named 1937 event.','Fantasia was released in 1940, not at the named 1937 event.','Bambi premiered in 1942, not at the named 1937 event.'],
 'The long answer is the real film title, not an explanatory sentence. The film list corroborates years; song placements #991/#1241 and first-feature #119 require different facts.'),
(937,'https://d23.com/a-to-z/fantasound/','Complete entry',
 'Fantasound was the stereophonic system created for Fantasia, Disney\'s 1940 concert feature.',
 ['CinemaScope is not the system Disney identifies for this film; it is the later widescreen process associated with Lady and the Tramp.','Sensurround is not the named Fantasia sound system.','Cinerama is not the named Fantasia sound system.'],
 'The Library of Congress corroborates Fantasound. Removed Fantasia from the stem to avoid echoing the coined answer; #939 reverses the same film/system fact and is retired.'),
(938,'https://www.disneyanimation.com/films/','Chronological film list, 1937-1942; Pinocchio before Fantasia in 1940',
 'Pinocchio follows Snow White in Disney\'s animated-feature chronology.',
 ['Fantasia follows Pinocchio within 1940, so is not second.','Dumbo follows in 1941, so is not second.','Bambi follows in 1942, so is not second.'],
 'Two films share 1940; ordering, not year alone, selects Pinocchio. #1199 tests its Oscars and #993 a song, not its production position.'),
(940,'https://d23.com/a-to-z/dumbo-film/','Paragraph beginning Coming after two expensive movies',
 'Dumbo moved quickly through animation at relatively low cost after Pinocchio and Fantasia, and made a welcome profit.',
 ['Bambi is listed in 1942, not the 1941 release in the question.','Fantasia is one of the preceding expensive 1940 films, not this economical 1941 release.','The Three Caballeros is a 1944/45 release, not the 1941 film.'],
 'The source supports fast economical production and financial benefit; it is not a claim that Dumbo alone permanently solved every studio financial problem. #2262 asks strike production context.'),
(941,'https://d23.com/a-to-z/bambi-film/','Opening synopsis, release and Felix Salten credit',
 'Bambi was released in 1942 and based on Felix Salten\'s book about the fawn.',
 ['Dumbo is the elephant story released in 1941, not this Salten adaptation.','The Reluctant Dragon is not the identified 1942 Salten adaptation.','Make Mine Music is the 1946 musical anthology, not this adaptation.'],
 'Knowing Bambi is a deer in #4 does not establish the novel\'s author or adaptation history. Original theatrical feature is intended, not Bambi II.'),
(942,'https://d23.com/a-to-z/three-caballeros-the-film/','Opening Donald/Jose/Panchito framing and 1944/45 dates',
 'The Three Caballeros brings Donald, Jose Carioca and Panchito together in Latin American sequences.',
 ['Saludos Amigos precedes this film and does not introduce the complete named trio together.','Make Mine Music is the musical-segment anthology, not this trio\'s Latin American feature.','Fun and Fancy Free frames Bongo and Mickey and the Beanstalk, not this trio\'s feature.'],
 'Jose and Donald also appear in Saludos Amigos, so Panchito is essential. The December 1944 Mexico premiere and February 1945 US release both fit wartime; #2632 tests a park ride cast.'),
(943,'https://d23.com/a-to-z/fun-and-fancy-free-film/','Complete two-story framing synopsis',
 'Fun and Fancy Free combines Bongo with Mickey and the Beanstalk.',
 ['Melody Time\'s complete seven-segment list contains neither of this pair.','Make Mine Music\'s complete ten-segment list contains neither of this pair.','The Adventures of Ichabod and Mr. Toad combines Wind in the Willows with Legend of Sleepy Hollow.'],
 'Package-film membership alone is not enough; the specific pair fixes the answer. Removed the release-year shortcut. #2384 tests the Beanstalk narrator, a separate production credit.'),
(945,'https://www.oscars.org/oscars/ceremonies/1949','Short Subject (Two-reel) winner',
 'Seal Island won the 1949 two-reel short Oscar credited to Walt Disney, Producer.',
 ['Beaver Valley was released in 1950 and cannot be this 1949 winner.','The Living Desert was released in 1953 and cannot be this 1949 winner.','White Wilderness was released in 1958 and cannot be this 1949 winner.'],
 '1949 means ceremony year, not original qualifying release year. D23 gives Seal Island\'s December 1948 qualifying run; the Academy category is authoritative over D23\'s loose documentary label.'),
(946,'https://d23.com/a-to-z/living-desert-the-film/','Paragraph beginning As Walt Disney had had a difficult time; first feature-length',
 'The Living Desert was the first feature-length True-Life Adventure in 1953.',
 ['Seal Island was a 27-minute featurette, not the first full-length feature.','The Vanishing Prairie was the next feature in 1954, after Living Desert.','White Wilderness was a later feature in 1958, after Living Desert.'],
 'Series first and feature-length first differ: Seal Island began the series but is short. The museum\'s documentary history corroborates the first-feature distinction.'),
(947,'https://d23.com/a-to-z/alice-in-wonderland-film/','Opening Lewis Carroll adaptation and July 1951 premiere',
 'Alice in Wonderland is Disney\'s 1951 animated adaptation of Lewis Carroll.',
 ['Peter Pan is the 1953 Barrie adaptation, not the 1951 Carroll film.','Cinderella was released in 1950, not the 1951 Carroll film.','The Adventures of Ichabod and Mr. Toad was released in 1949 and adapts Grahame/Irving, not Carroll.'],
 'Earlier Alice Comedies mixed live action and animation; removed an unnecessary first claim. #317 tests an attraction\'s vehicle design rather than literary source.'),
(948,'https://d23.com/a-to-z/peter-pan-film/','1953 release; 1939 arrangement for Barrie play rights',
 'Peter Pan was released in 1953 and based on the J. M. Barrie play.',
 ['Alice in Wonderland is the 1951 Carroll adaptation, not this Barrie film.','Cinderella is a 1950 film, not this 1953 Barrie adaptation.','Lady and the Tramp is a 1955 film, not this 1953 Barrie adaptation.'],
 'Barrie also wrote a novel, but the question\'s play attribution is supported by the rights account. #996 tests a song and #2242 a themed-area inspiration.'),
(949,'https://d23.com/a-to-z/lady-and-the-tramp-film/','First Disney animated feature filmed in CinemaScope paragraph',
 'Lady and the Tramp was Disney\'s first animated feature filmed in CinemaScope.',
 ['Sleeping Beauty came later and used Technirama 70, a different process.','Peter Pan preceded Lady but was not the first CinemaScope animated feature.','101 Dalmatians came later, not first.'],
 'Widescreen alone does not identify CinemaScope. Museum production history independently corroborates Lady\'s first use; final wording specifies animated, avoiding live-action 20,000 Leagues.'),
(950,'https://d23.com/a-to-z/sleeping-beauty-film/','Release/format paragraph: January 29, 1959, Technirama 70',
 'Sleeping Beauty is the 1959 Disney animated feature presented in Technirama 70.',
 ['Lady and the Tramp is the 1955 CinemaScope feature, not the named 1959 process.','101 Dalmatians is the 1961 feature, not this 1959 film.','The Sword in the Stone is the 1963 feature, not this 1959 film.'],
 'Distinguished the two widescreen processes. The wording does not claim the animation was photographed on 70mm negative; it identifies the Super Technirama 70 presentation process.'),
(951,'https://www.waltdisney.org/blog/making-101-dalmatians','New Xerox Technology For Hand-Drawn Animation',
 '101 Dalmatians was the first feature to use xerography throughout for transferring animation drawings to cels.',
 ['Sleeping Beauty used the process only in a few test scenes, not throughout.','The Jungle Book is later than the 1961 first feature-wide use.','The Aristocats is later than the 1961 first feature-wide use.'],
 'Sleeping Beauty was a defensible distractor under introduced. Goliath II used it throughout but is a short, not a feature. Final wording narrows the precise first claim and D23 corroborates it.'),
(952,'https://www.disneyanimation.com/films/','Chronology: 1963, 1967, 1970, 1973',
 'The Sword in the Stone (1963) was the last new Disney animated feature released before Walt\'s December 1966 death.',
 ['The Jungle Book was released in 1967, after his death.','The Aristocats was released in 1970, after his death.','Robin Hood was released in 1973, after his death.'],
 'Release is different from personally supervised: Walt worked on Jungle Book but did not live to its release. Removed the 1963 shortcut; theatrical reissues do not count as new features.'),
]

library = read('audit/source-notes.json')
base = read('audit/runs/next-shard-0017-final-evidence-notes.json')
templates = {r['questionId']:r for r in base['reviews']}
reviews=[]
for i,url,loc,premise,wrong,challenge in D:
    sid=f'b17-{i}'
    changing = i < 926 and i not in (907,917,918)
    library['sources'][sid]={'url':url,'locator':loc,'evidence':premise,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':changing,'nextReviewAt':'2027-02-05' if changing else None,'topics':['Batch 17', 'parks' if i<926 else 'walt'],'limitations':'Institutional text inspected; no film or video viewing claimed. Location questions describe the reviewed park configuration; a dated map is supplemented by current material where needed.'}
    r=templates[i]
    r['checks']=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
    r['notes']=challenge
    r['context']='Reviewed original theatrical-film history or the specifically named park, not television episodes, remakes or an assumed worldwide attraction configuration. Full parks/walt and matching film digests read; ranked comparisons and additional cross-bank relationships inspected.'
    r['timeSensitive']=changing
    r['nextReviewAt']='2027-02-05' if changing else None
    r['premise']={'reason':premise,'sources':[sid]}
    r['options']=[{'basis':'direct','reason':premise,'sources':[sid]}]+[{'basis':'exclusive-inference','reason':v,'sources':[sid]} for v in wrong]
    r['challenge']={'reviewer':'Codex','at':'2026-11-07','premiseChecked':True,'alternativesExcluded':True,'notes':challenge}
    reviews.append(r)

# Additional inspected passages: keep their claims narrow and link them only where used.
EXTRA={
'luigi':('https://disneyland.disney.go.com/attractions/disney-california-adventure/luigis-rollickin-roadsters/','Hop in for a Spirited Spin','Luigi\'s Roadsters dance in Casa Della Tires\' storage yard, not on the Ornament Valley road race.'),
'mater':('https://disneyland.disney.go.com/attractions/disney-california-adventure/maters-junkyard-jamboree/','Grab Yer Partner','Mater\'s tractors whirl in figure eights around a junkyard dancefloor.'),
'incredicoaster':('https://disneyland.disney.go.com/attractions/disney-california-adventure/incredicoaster/','The Supers Are Back; Reimagined','Incredicoaster is a Jack-Jack pursuit around Pixar Pier\'s Incredibles Park, not the Cars valley race.'),
'park-directory':('https://disneyworld.disney.go.com/destinations/animal-kingdom/','Africa and Asia attraction lists','The current directory lists Kilimanjaro Safaris and Gorilla Falls under Africa; Everest and Maharajah Jungle Trek under Asia.'),
'landmarks':('https://d23.com/11-real-life-landmarks-that-inspired-epcot-world-showcase/','Pavilions 2-11; architecture descriptions','Norway has Stave Church; China Temple of Heaven and Gate of Golden Sun; Germany St George; Italy campanile; Japan lagoon torii; Morocco minaret; France Eiffel Tower; UK Tudor pub; Canada chateau.'),
'omnis':('https://www.disneycampus.com/blog/the-science-behind-the-magic-guardians-of','What is it? How do we use it?','Cosmic Rewind combines Omnimover technology with a roller coaster, using controlled yaw rotations; Disney calls it OmniCoaster.'),
'gorillas':('https://disneyworld.disney.go.com/attractions/animal-kingdom/disney-animals-gorillas/','Gorillas at Walt Disney World Resort','The park\'s gorillas live on Gorilla Falls Exploration Trail.'),
'tigers':('https://disneyworld.disney.go.com/attractions/animal-kingdom/maharajah-jungle-trek/','Explore a Mystical Forest','Maharajah Jungle Trek is the Asian tiger and Anandapur forest trail.'),
'africa':('https://www.disneyworld.eu/attractions/animal-kingdom/disney-animals/','Wildlife at Disney\'s Animal Kingdom: Africa and Asia','Africa wildlife experiences include Gorilla Falls and Kilimanjaro Safaris; Asia includes the Asian animal collection.'),
'fowler':('https://d23.com/a-to-z/admiral-joe-fowler-riverboat/','Complete entry','Admiral Joe Fowler operated at Magic Kingdom 1971-1980, when it was retired; Richard F. Irvine remained.'),
'irvine':('https://d23.com/walt-disney-legend/richard-irvine/','Final paragraph','Richard F. Irvine riverboat was renamed Liberty Belle in 1996; a Seven Seas Lagoon ferry then received the Irvine name.'),
'mark':('https://disneyland.disney.go.com/attractions/disneyland/mark-twain-riverboat/','Along the Mississippi; Alternate Adventures','Mark Twain is Disneyland\'s steam paddle-wheeler. Sailing Ship Columbia follows the same Rivers of America route.'),
'animation':('https://www.disneyanimation.com/films/','Chronological catalogue 1937-1973','Snow White 1937; Pinocchio then Fantasia 1940; Dumbo 1941; Bambi 1942; Make Mine Music 1946; Fun and Fancy Free 1947; Melody Time 1948; Ichabod/Toad 1949; Cinderella 1950; Alice 1951; Peter Pan 1953; Lady 1955; Sleeping Beauty 1959; Dalmatians 1961; Sword 1963; Jungle Book 1967; Aristocats 1970; Robin Hood 1973.'),
'mouse':('https://www.waltdisney.org/blog/birth-mouse','First-three-cartoon paragraphs','Production order: Plane Crazy, The Gallopin\' Gaucho, Steamboat Willie; sound distribution did not follow initial production order.'),
'donald':('https://d23.com/a-to-z/donald-duck/','Opening debut paragraph','Donald debuted in The Wise Little Hen on June 9, 1934.'),
'karnival':('https://d23.com/a-to-z/karnival-kid-the-film/','Opening first-speaking statement','The Karnival Kid was the first Mickey cartoon in which Mickey speaks, in 1929.'),
'flowers':('https://d23.com/a-to-z/flowers-and-trees-film/','Opening release and ordinal','Flowers and Trees was the 29th Silly Symphony, released in 1932.'),
'mill':('https://d23.com/a-to-z/old-mill-the-film/','Opening release sentence','The Old Mill was a 1937 Silly Symphony.'),
'pigs':('https://d23.com/a-to-z/three-little-pigs-film/','Opening release sentence','Three Little Pigs was a 1933 Silly Symphony.'),
'fantasound':('https://wwws.loc.gov/exhibits/music-and-animation/fantasia-1940.html','Opening exhibition text','Fantasia, a 1940 concert feature, used stereophonic Fantasound.'),
'beaver':('https://d23.com/a-to-z/beaver-valley-film/','Opening release/runtime and award','Beaver Valley was a 32-minute featurette released in 1950, and won the two-reel short Oscar.'),
'desert':('https://d23.com/a-to-z/living-desert-the-film/','Opening and first-feature paragraph','The Living Desert was the first feature-length True-Life Adventure, released in 1953, with a 69-minute runtime.'),
'docs':('https://www.waltdisney.org/blog/walt-disneys-award-winning-documentaries','Seal Island through feature-length expansion paragraphs','Seal Island won at the March 1949 ceremony; Beaver Valley followed in 1950. Living Desert was the first feature in 1953, Vanishing Prairie followed in 1954, and White Wilderness in 1958.'),
'melody':('https://d23.com/a-to-z/melody-time-film/','Complete seven-segment list','Melody Time comprises Once Upon a Wintertime, Bumble Boogie, Johnny Appleseed, Little Toot, Trees, Blame It on the Samba and Pecos Bill.'),
'music':('https://d23.com/a-to-z/make-mine-music-film/','Complete ten-segment list','Make Mine Music includes Martins and Coys, Blue Bayou, All the Cats Join In, Without You, Casey at the Bat, Two Silhouettes, Peter and the Wolf, After You\'ve Gone, Johnny Fedora/Alice Bluebonnet and Whale Who Wanted to Sing at the Met.'),
'ichabod':('https://d23.com/a-to-z/adventures-of-ichabod-and-mr-toad-the-film/','Complete two-story synopsis and authors','The two stories are Wind in the Willows by Kenneth Grahame and Legend of Sleepy Hollow by Washington Irving, not Bongo/Beanstalk or Carroll.'),
'peter':('https://d23.com/a-to-z/peter-pan-film/','1953 release and Barrie rights paragraph','Peter Pan was released in 1953; Disney arranged rights to the Barrie play.'),
'lady':('https://d23.com/a-to-z/lady-and-the-tramp-film/','First CinemaScope animated-feature and release paragraph','Lady and the Tramp was the first Disney animated feature filmed in CinemaScope in 1955.'),
'lady-museum':('https://www.waltdisney.org/blog/bella-notte-eyvind-earle-lady-and-tramp','CinemaScope paragraph','The museum independently describes Lady and the Tramp as the first Disney feature produced in CinemaScope, requiring wide backgrounds.'),
'sleep':('https://d23.com/a-to-z/sleeping-beauty-film/','1959 release and Technirama 70 paragraph','Sleeping Beauty was released in 1959 in Technirama 70, distinct from Lady\'s CinemaScope.'),
'dalmatians':('https://d23.com/a-to-z/one-hundred-and-one-dalmatians-film/','Xerox paragraph','101 Dalmatians was the first feature to use Xerox throughout to transfer drawings to cels, in 1961.'),
'death':('https://d23.com/about-walt-disney/','CalArts paragraph','Walt Disney died December 15, 1966.'),
'calarts':('https://d23.com/about-walt-disney/','Final CalArts paragraphs','CalArts was formed in 1961 by merging Chouinard Art Institute and Los Angeles Conservatory of Music.'),
'lincoln':('https://disneyland.disney.go.com/en-ca/attractions/disneyland/disneyland-story/','A Historic Presentation; An Updated President Lincoln','Great Moments with Mr. Lincoln has an Audio-Animatronic Lincoln; it debuted at the 1964 fair and moved to Disneyland in 1965.'),
'land':('https://disneyworld.disney.go.com/attractions/epcot/living-with-the-land/','Opening and A Taste of the Future','Living with the Land tours greenhouses and teaches farming, linking its greenhouse setting and agriculture theme.'),
}
for k,(url,loc,evidence) in EXTRA.items():
    library['sources']['b17-'+k]={'url':url,'locator':loc,'evidence':evidence,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':False,'nextReviewAt':None,'topics':['Batch 17'],'limitations':'Inspected institutional text or evaluated narrowly matching reusable passage; no film playback claimed. Historic source claims retain their stated date.'}
MAP={902:['landmarks'],903:['landmarks'],904:['landmarks'],912:['omnis'],913:['omnis'],914:['tigers','africa'],915:['gorillas','africa'],918:['fowler','irvine','mark'],925:['fowler','irvine','mark'],930:['mouse'],931:['mouse'],932:['flowers','mill','pigs','docs'],933:['donald'],934:['karnival'],935:['animation'],937:['fantasound','lady'],938:['animation'],940:['animation'],941:['animation'],942:['music'],943:['melody','music','ichabod'],945:['beaver','desert','docs'],946:['docs'],947:['animation','peter','ichabod'],948:['animation','peter'],949:['animation','sleep','lady-museum'],950:['animation','lady'],951:['dalmatians','animation'],952:['death','animation']}
for r in reviews:
    added=['b17-'+k for k in MAP.get(r['questionId'],[])]
    r['premise']['sources']+=added
    for o in r['options']: o['sources']+=added
    if r['questionId']==943:
        for j,k in enumerate(['melody','music','ichabod'],1):
            r['options'][j]['basis']='exhaustive-list'
            r['options'][j]['sources']=['b17-'+k]
    if r['questionId']==951: r['options'][1]['basis']='contradiction'
    if r['questionId']==938:
        for o in r['options'][1:]: o['basis']='exhaustive-list'
    if r['questionId']==906:
        for j,k in enumerate(['luigi','mater','incredicoaster'],1):
            r['options'][j]['sources']=['b17-'+k]
            r['options'][j]['basis']='contradiction'
        r['options'][1]['reason']='Luigi\'s cars dance within the storage yard, not along the Ornament Valley race course.'
        r['options'][2]['reason']='Mater\'s tractors circle a junkyard dancefloor in figure eights, not an Ornament Valley race.'
        r['options'][3]['reason']='Incredicoaster pursues Jack-Jack around Pixar Pier, not Cars Land\'s Ornament Valley.'
    if r['questionId'] in (914,915,922):
        r['premise']['sources'].append('b17-park-directory')
        for o in r['options']: o['sources'].append('b17-park-directory')
base['reviews']=reviews
base['sourcesChecked']=list(dict.fromkeys(s for r in reviews for part in [r['premise']]+r['options'] for s in part['sources']))
write('audit/source-notes.json',library)
write('audit/runs/next-shard-0017-reviewed-notes.json',base)
print('Authored',len(reviews),'explicit reviews; no automatic approval.')

RETIRE={
908:(956,'Both ask the Great Moments/Lincoln Audio-Animatronic association. Retain the more specific 1964 World\'s Fair question; the attraction\'s later Disneyland location does not make another association-identification question necessary.','b17-lincoln'),
911:(956,'The attraction title explicitly supplies Lincoln; it also reverses the same Lincoln/Great Moments fact retained in #956. Two current player reports identify the giveaway.','b17-lincoln'),
920:(888,'Both test the Living with the Land agriculture/greenhouse experience. The retained question already names the ride and asks about working greenhouses; reversing this to identify the agricultural boat ride adds no materially distinct fact.','b17-land'),
921:(1484,'Both connect Kilimanjaro Safaris, Harambe and the African village setting. The retained question supplies African-village context and asks Harambe; the reverse land question is already answered by that context.','b17-africa'),
939:(937,'Exact inverse of the film/Fantasound association. Retain the technical-name question, whose final wording avoids the Fantasia/Fantasound word echo.','b17-fantasound'),
944:(2571,'Both test CalArts\' formation by merging Chouinard and the Los Angeles Conservatory. Retain the more specific constituent-school question; its stem already supplies the institution asked here.','b17-calarts'),
}
catalog=read('artifacts/question-audit/batch17-context.json')['catalog']
for i,(replacement,reason,sid) in RETIRE.items():
    write(f'audit/runs/next-shard-0017-comparison-{i}-{replacement}.json',{'reviewer':'Codex','at':'2026-11-07','retiredQuestion':catalog[str(i)],'replacementQuestion':catalog[str(replacement)],'reason':reason,'source':library['sources'][sid],'additionalContext':'Complete topic digest read; preserved scope; related replacement is context only, not approved by this decision.'})
write('audit/runs/next-shard-0017-retirement-actions.json',[{'id':i,'replacement':v[0],'reason':v[1],'reference':f'audit/runs/next-shard-0017-comparison-{i}-{v[0]}.json'} for i,v in RETIRE.items()])
