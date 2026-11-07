"""Codex's passage-based reviews, including a separate final-wording challenge."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from question_audit import digest
AT = '2026-11-07'
DUE = '2027-02-05'
library = json.loads((ROOT/'audit/source-notes.json').read_text(encoding='utf-8'))

def source(key, url, locator, evidence, topic, mutable=False, limitations='Primary institutional text inspected; no film/video playback claimed.'):
    library['sources']['b10-'+key] = dict(url=url, locator=locator, evidence=evidence, topics=[topic], checkedBy='Codex', checkedAt=AT, timeSensitive=mutable, nextReviewAt=DUE if mutable else None, limitations=limitations)

source('soul','https://www.pixar.com/soul','Opening synopsis; Joe Gardner; 22; Terry profiles','Jazz pianist Joe Gardner enters the Great Before. New souls acquire personalities there; Terry counts entrants to the distinct Great Beyond.','Soul')
source('coco','https://www.pixar.com/coco','Synopsis; Santa Cecilia world section','Miguel is the young musician visiting his ancestors; Santa Cecilia contains the Rivera family compound and shoe business.','Coco')
source('inside','https://www.pixar.com/inside-out','Opening synopsis and five emotion character profiles','Inside Out follows Riley and her personified emotions as she adjusts to moving to San Francisco.','Inside Out')
source('onward','https://www.pixar.com/onward','Opening synopsis, as captured in reusable b9-onward note','Onward follows two teenage elf brothers, Ian and Barley Lightfoot.','Onward',limitations='Previously inspected primary passage reused from b9-onward after checking that its captured evidence addresses this comparison; no new page access claimed.')
source('incredibles','https://www.pixar.com/the-incredibles','Violet, Dash, Elastigirl and Frozone profiles','Violet becomes invisible and creates force fields; Dash has super-speed; Helen stretches. Lucius Best is Frozone.','The Incredibles')
source('evelyn','https://en.wikipedia.org/wiki/Incredibles_2','Plot, Helen discovers the delivery-driver decoy and Evelyn reveals herself; Voice cast','Evelyn is the true Screenslaver; Winston promotes legalizing supers, Underminer is the opening robber, Selick the ambassador.','The Incredibles',limitations='Secondary plot and cast text, corroborated against the specific confession in a separately hosted dialogue transcript and Pixar character profiles. Promotional Pixar page withholds the twist; no film playback claimed.')
source('evelyndialogue','https://transcripts.simpleremix.com/script.php/the-incredibles-2-2018-F8HU','Freezing-cell confession, lines 2847-2878; later Helen identifies Evelyn as controller','Evelyn says she created the Screenslaver character, recorded its messages and controlled the delivery driver; Winston does not know.','The Incredibles',limitations='Secondary dialogue transcription, not an official screenplay or watched film. Exact confession corroborated with the plot account; no dependence on the promotional synopsis for the twist.')
source('hal','https://movies.disney.com/wall-e','Gallery, EVE meet Hal (5 of 20) and Later Earth (17 of 20)','Disney identifies WALL-E\'s companion as Hal in the gallery captions.','WALL-E')
source('halroach','https://news.disney.com/16-bit-wall-e-remix','Article description, fan-favorite moments paragraph','Disney explicitly calls Hal WALL-E\'s cockroach pal.','WALL-E')
source('wall','https://www.pixar.com/wall-e','EVE, Captain, Auto and John and Mary profiles','The Axiom is the luxury mother ship housing displaced humans, commanded by the Captain, with Auto as autopilot.','WALL-E')
source('toy4','https://www.pixar.com/toy-story-4','Woody, Bo Peep, Forky profiles and opening synopsis','Woody unexpectedly reunites with Bo Peep after years apart. Buzz and Jessie remain with the toy gang; Forky is Bonnie\'s newly crafted spork toy.','Toy Story')
source('toy2','https://www.pixar.com/toy-story-2','Opening synopsis; Al, Prospector and Emperor Zurg profiles','Al McWhiggin kidnaps Woody and wants to sell the Roundup collection to a museum in Japan. Stinky Pete is a collectible; Zurg is Buzz\'s enemy.','Toy Story')
source('flik','https://d23.com/12-inventors-to-inspire-an-up-and-coming-scientist/','Item 10, Flik (a bug\'s life)','Flik builds a bird-shaped aircraft to frighten grasshoppers.','A Bug\'s Life')
source('bugs','https://www.pixar.com/a-bugs-life','Opening synopsis; Princess Atta, Dot and Queen profiles','Flik aims to save Ant Island. Atta is the heir and Dot the Queen\'s younger daughter.','A Bug\'s Life')
source('island','https://video.disney.com/watch/riley-s-memories-inside-out-clip-5230b44b3df210a316fdb257','Official clip description, core memories and personality islands','Disney explicitly lists Hockey Island as one of Riley\'s personality islands.','Inside Out')
source('islandlist','https://news.disney.com/quiz-which-inside-out-personality-island-is-yours','Opening paragraphs naming Goofball, Hockey and Family Islands','Riley\'s sport-named island is Hockey Island.','Inside Out')
source('up','https://www.pixar.com/upfilm','Ellie character profile','Carl and Ellie pledge to visit Paradise Falls in South America.','Up')
source('finaldeath','https://www.dicacademy.com/_files/ugd/7a859e_f9530329bda9418f8dc451fcf5cede61.pdf','Printed screenplay pp. 66-67; Chicharrón dissolves, followed by Héctor\'s explanation','Héctor calls disappearance from the Land of the Dead after being forgotten the Final Death; he says no one knows where the soul goes.','Coco',limitations='Disney/Pixar-authored Academy screenplay on a third-party host; text inspected, not film viewing. The final question asks the explicit term rather than asserting unknown subsequent existence.')
source('wet','https://news.disney.com/luca-characters-art','Inside the Transformation; Skaria and Albright production discussion','Wet/dry states trigger human/sea-monster changes; scales appear and tails retract or emerge, with variable coverage.','Luca')
source('luca','https://www.pixar.com/luca','Just Add Water; Luca and Alberto profiles','The boys\' human appearance conceals their sea-monster nature through a physical camouflage transformation.','Luca')
source('command','https://www.pixar.com/toy-story','Buzz Lightyear character profile','Buzz believes he is on a secret mission for Star Command.','Toy Story')
source('aristocats','https://d23.com/a-to-z/aristocats-the-film/','Opening plot and rescue paragraphs','Toulouse and Berlioz are Duchess\'s kittens; mouse Roquefort joins O\'Malley in rescuing the family.','The Aristocats')
source('roquefort','https://d23.com/a-to-z/roquefort/','Complete character entry','Roquefort is the polite mouse from The Aristocats.','The Aristocats')
source('fear','https://www.vam.ac.uk/mused/films-shows/inside-out-emotional-vanda-objects/','Fear section','The V&A describes Fear as purple and designed to resemble a raw nerve.','Inside Out',limitations='Museum commentary on Pixar character design, corroborated by filmmaker-interview reporting; not film playback.')
source('fearinterview','https://www.laughingplace.com/w/articles/2015/06/19/inside-pixars-inside-out/','Character art director Albert Lozano paragraph','Filmmaker reporting identifies purple as the selected design color for Fear.','Inside Out',limitations='First-person production interview reporting, corroborated by V&A and the complete cast-color listing.')
source('colors','https://en.wikipedia.org/wiki/Inside_Out','Voice cast, five emotion descriptions','Fear is purple, Disgust green, Anger red and Sadness blue.','Inside Out',limitations='Secondary explicit color listing, used with museum and filmmaker interview corroboration. No claim of inspecting the image links visually.')
source('sina','https://www.disney.co.jp/movie/moana/character/sina','Sina page title and final character biography; Tala and Tui biographies','Sina is Moana\'s mother and Tui\'s wife; Tala is Moana\'s grandmother and Tui her father.','Moana',limitations='Official Japanese character biographies read for family roles; English name mapping corroborated by original cast credits and 2016 actor reporting.')
source('sinacast','https://www.linmanuel.com/project/moana/','Original Cast list','Nicole Scherzinger is Sina; Rachel House is Gramma Tala and Temuera Morrison is Chief Tui in the original 2016 film.','Moana')
source('alice','https://disneyland.disney.go.com/attractions/disneyland/alice-in-wonderland/','Opening attraction description','Alice in Wonderland uses oversized caterpillar vehicles.','parks',True)
source('toad','https://disneyland.disney.go.com/attractions/disneyland/mr-toads-wild-ride/','Opening attraction description','Mr. Toad\'s Wild Ride uses a motorcar.','parks',True)
source('pan','https://disneyland.disney.go.com/attractions/disneyland/peter-pans-flight/','Opening attraction description','Peter Pan\'s Flight uses an enchanted pirate ship.','parks',True)
source('pinocchio','https://disneyland.disney.go.com/attractions/disneyland/pinocchios-daring-journey/','Wish Upon a Star, first paragraph','Pinocchio\'s Daring Journey uses a woodcarver\'s cart.','parks',True)
source('bigben','https://d23.com/a-to-z/great-mouse-detective-the-film/','Final production paragraph; cast and opening plot','The final Basil-Ratigan confrontation occurs inside Big Ben\'s gearworks. Olivia is Flaversham\'s daughter; Dawson aids Basil.','The Great Mouse Detective')
source('felicia','https://d23.com/a-to-z/felicia/','Complete character entry','Felicia is Ratigan\'s feline friend.','The Great Mouse Detective')
source('fidget','https://d23.com/a-to-z/fidget/','Complete character entry','Fidget is Ratigan\'s henchman, a distinct role from Felicia.','The Great Mouse Detective')
source('goodcompany','https://filmmusiccentral.com/2019/07/01/oliver-company-good-company-1988/','Opening paragraphs, Jenny\'s adoption of Oliver and Good Company sequence','Good Company accompanies Jenny and Oliver\'s new companionship in Oliver & Company.','music',limitations='Specialist film-music commentary inspected. Primary 1988 soundtrack advertisement was indexed but full PDF access failed; SoundtrackCollector served an outage notice. Corroborated with the accessible Wikipedia soundtrack track list. No lyrics copied or video playback claimed.')
source('goodcatalog','https://en.wikipedia.org/wiki/Oliver_%26_Company_%28soundtrack%29','Track listing, side two item 2, Good Company by Myhanh Tran, 02:30','The Oliver & Company soundtrack track list includes Good Company.','music',limitations='Secondary soundtrack discography; specific recording attribution corroborates the scene commentary, rather than relying on a generic film synopsis. No writer-credit claims imported from this listing.')
source('canada','https://disneyworld.disney.go.com/attractions/epcot/canada-far-and-wide/','Title and Sweeping Scenic Views section','Canada Far and Wide is EPCOT\'s Circle-Vision 360 presentation of Canada.','parks',True)
source('mintz','https://www.waltdisney.org/blog/mickeys-follies-walts-distribution-deals-defeats-and-decisions','Oswald contract renewal paragraphs; subsequent Pat Powers distribution paragraphs','Mintz demands a pay cut and has deals with Disney\'s staff; Universal owns Oswald. Roy is Walt\'s partner; Powers enters the later Mickey sound-distribution story.','walt')
source('rite','https://www.waltdisney.org/blog/fantasia-eight-parts-rite-spring','Opening museum/California Academy of Sciences discussion','Fantasia\'s Rite of Spring depicts dinosaurs, including their deaths in a desert.','Fantasia')
source('fantasiamap','https://catalog.afi.com/Film/27633-FANTASIA','Synopsis: second, fourth and fifth musical selections','Mushrooms appear in Nutcracker Suite; dinosaurs in Rite of Spring; centaurs in Pastoral Symphony.','Fantasia',limitations='AFI institutional scene synopsis based on film documentation, corroborating the museum account; no film playback claimed.')
source('whales','https://d23.com/a-to-z/fantasia2000-film/','Opening segment-by-segment synopsis, Pines of Rome','Flying whales belong to Pines of Rome in Fantasia/2000, not the original film\'s Rite of Spring.','Fantasia')
source('ports','https://www.tokyodisneyresort.jp/en/tdr/facility/themeport','American Waterfront, Mediterranean Harbor, Port Discovery and Lost River Delta sections','American Waterfront is New York and Cape Cod; Mediterranean Harbor a Southern European town; Port Discovery futuristic; Lost River Delta Central American ruins.','parks',True)
source('5k','https://cdn1.parksmedia.wdprapps.disney.com/media/blog/wp-content/uploads/2023/06/planDisney-Disney-Castaway-Cay-Pocket-Guide.pdf','Recreation list, item 10','The official island pocket guide calls Castaway Cay 5K a self-paced activity.','cruise',True,limitations='Official guide text inspected. Corroborated by Disney\'s indexed current destination description and July 2023 planDisney account; current FAQ full-page fetch served a JS shell.')
source('5kpanel','https://plandisney.disney.go.com/question/go-cruise-september-castaway-cay-run-544013/','July 4, 2023 answer; changes to former formal start and registration','Castaway Cay 5K has no formal start time or registration and is completed at the guest\'s own pace.','cruise',True,limitations='Dated Disney-hosted eyewitness panel advice; current offering recheck scheduled, not a guarantee of access on every itinerary.')
source('palo','https://disneycruise.disney.go.com/en-gb/onboard-activities/palo-restaurant/','Exquisite Italian Cuisine, first sentence','Palo is named after the long poles used by gondoliers in Venice.','cruise')
source('laugh','https://press.disneyplus.com/media-kits/monsters-at-work','Opening sentence establishing the post-film setting','Monsters, Inc. switches from screams to children\'s laughter to power Monstropolis.','Monsters Inc/University',limitations='Official sequel-series press kit used solely to corroborate the original film\'s ending; question remains about the theatrical film, not television trivia.')
source('nemospecies','https://www.bristolaquarium.co.uk/blog/from-the-screen-to-the-sea-discover-the-fish-from-finding-nemo/','Seahorse-Sheldon and Butterflyfish-Tad sections','Sheldon is the young seahorse; Tad a butterflyfish.','Finding Nemo/Dory',limitations='Aquarium specialist commentary on film animals, corroborated with Tim Dirks\' specific school-scene listing and Pixar\'s turtle profiles; primary page does not name every schoolmate.')
source('nemoscene','https://www.filmsite.org/findingnemo.html','First school-day scene, four children at drop-off','Pearl is an octopus, Tad a butterflyfish, Sheldon a seahorse.','Finding Nemo/Dory',limitations='Secondary scene-by-scene film commentary corroborated by aquarium and Pixar character material; no claim of film playback.')
source('nemoturtles','https://www.pixar.com/finding-nemo','Turtles profile','Squirt is Crush\'s turtle offspring.','Finding Nemo/Dory')
source('luigi','https://www.pixar.com/cars','Luigi & Guido character profile','Luigi runs Luigi\'s Casa Della Tires, assisted by Guido.','Cars')

rows = {}
def review(qid, keys, context, premise, reasons, challenge, notes, bases=None):
    rows[qid] = (keys.split(), context, premise, reasons, challenge, notes, bases)

review(482,'soul coco inside onward','Pixar feature identity from its jazz protagonist and accidental cosmic journey.',
 'Joe Gardner is Soul\'s jazz pianist, entering the cosmic realm after a misstep.',
 ['Soul has the identified jazz protagonist and journey.','Coco follows young Miguel and his ancestors, not jazz pianist Joe.','Inside Out follows Riley\'s emotions, not a jazz musician in an afterlife.','Onward follows elf brothers on a magical quest, not Joe\'s journey.'],
 'Coco also depicts the dead and music, but its child guitarist does not fit the jazz-musician conjunction. Inside Out\'s mental world is not this cosmic journey.',
 'Easy film-premise recognition; distinct from 1437 piano instrument and 661 soul number; no real TV scope.')
review(483,'evelyn evelyndialogue','Original 2018 Incredibles 2; mastermind rather than delivery-driver decoy.',
 'Evelyn confesses creating the Screenslaver and controlling the delivery driver; the plot account corroborates.',
 ['Evelyn creates and controls the scheme.','Evelyn explicitly says Winston does not know; he is her unwitting brother.','Underminer is the separate opening robber, not this plot\'s creator.','Selick is the diplomat targeted by the plot, not its creator.'],
 'The man initially arrested is a hypnotized decoy. Masterminds precisely identifies Evelyn without incorrectly treating every masked wearer as her.',
 'Correct film title and medium twist recall; q1289 asks public DevTech leadership, q1573 hypnosis device, q1575 vehicle, all separate facts.')
review(484,'hal halroach','WALL-E companion name, not a word for his species.',
 'Disney explicitly names the cockroach Hal and labels him in the gallery.',
 ['Hal is the documented proper name.','Hank is a different name, not the named cockroach.','Bug describes a kind of creature but is not the proper name Disney gives him.','Rex is not the companion\'s documented name.'],
 'Lowercase bug could describe him, but the question asks his name; Disney\'s two specific captions/articles establish Hal.',
 'Hard: the proper name is obscure and not introduced in dialogue. No second Hal identity question found in the full-bank search.')
review(485,'coco','Fictional living-world town, not a real filming location.',
 'Pixar\'s Santa Cecilia section places Miguel\'s family compound there.',
 ['Santa Cecilia names the documented town.','Santa María differs from the specified town name.','San Miguel is not the documented town, despite matching Miguel\'s given name.','Santa Rosa is not that town\'s name.'],
 'Real Mexican towns or production inspirations do not rename the fictional setting. All four are parallel Spanish place names.',
 'Medium setting-name recall; distinct from ancestor names, holiday, instrument, shoemaking trade and guitar provenance.')
review(486,'toy4','Toy Story 4 reunion after years of separation.',
 'Pixar specifically describes Bo as a long-lost friend separated for years and Woody\'s unexpected reunion.',
 ['Bo Peep is the long-lost friend.','Buzz is still part of the gang; he is not the friend absent for years.','Jessie remains with the gang rather than being this long-lost friend.','Forky is newly created by Bonnie and cannot be a friend from years earlier.'],
 'Woody meets Buzz and Jessie again after brief separations too, so final wording requires years apart. Forky is new, eliminating another literal reading of reunion.',
 'Easy central reunion; distinct from q2003\'s Giggle friend and q2365\'s Molly identity. Clarified rather than changed the keyed answer.')
review(489,'incredibles','Violet\'s canonical pair of powers in The Incredibles.',
 'The Violet profile expressly pairs invisibility with force fields; profiles distinguish Dash\'s speed and Helen\'s stretch.',
 ['Both force fields and invisibility are Violet\'s powers.','Flying and super strength is not her documented pair.','Speed is Dash\'s power, so speed plus invisibility does not match Violet\'s pair.','Elasticity is Helen\'s power, so elasticity plus force fields does not match Violet\'s pair.'],
 'Running or being carried through the air is not super-speed or flight. A partially true pair does not satisfy the request for both canonical powers.',
 'Medium paired recall; distinct from q634 Bob\'s strength and q1571 Voyd\'s portals; options comparable in form.')
review(490,'toy2','Human who kidnaps Woody for the Japanese museum sale in Toy Story 2.',
 'Pixar names Al McWhiggin as kidnapper and describes his museum sale ambition.',
 ['Al is the collector who steals Woody.','Stinky Pete is one of the collected toys; wanting the sale does not make him the thief.','Zurg is Buzz\'s enemy, not Woody\'s human kidnapper.','Lotso is not the named kidnapper Al; he is a different toy character.'],
 'Stinky Pete favors the museum and obstructs escape, but the question asks who steals Woody. The explicit actor-action relation excludes him.',
 'Medium action attribution; distinct from q656 Prospector identity, q1023 franchise and q631 Jessie identity.')
review(491,'flik','Animal imitated by Flik\'s grasshopper-frightening model, not the living bird in the climax.',
 'D23 directly identifies the bird-shaped aircraft built to frighten grasshoppers.',
 ['The model imitates a bird.','A bat has a different animal form from the specified bird model.','A frog has a different animal form from that model.','A spider has a different animal form from that model.'],
 'The question asks the model\'s particular shape rather than every invention Flik might build. The bird-shaped attribution directly excludes the three other shapes without relying on silence about other traps.',
 'Medium invention recall; distinct from q1022 circus-bug recruitment, q650 villain species and q197 Hopper name. Changed to parallel animal alternatives and a precise model-shape premise.')
review(492,'island islandlist','Original Inside Out; Riley\'s sport-linked Personality Island.',
 'Disney\'s core-memory clip description names Hockey Island.',
 ['Hockey Island is the named sporting island.','Soccer Island is not the documented island name.','Baseball Island is not its name.','Skating Island differs from the specific Hockey Island name.'],
 'Hockey uses skating but the label is Hockey Island, not Skating Island. These are competing proper labels, not general activities Riley might enjoy.',
 'Medium world-name recall; q1414 asks the sequel\'s camp sport, an additional film/event relation, not this island label.')
review(493,'up','Carl and Ellie\'s named dream destination in Up.',
 'Ellie\'s profile names their pledged destination Paradise Falls.',
 ['Paradise Falls is the named fictional destination.','Angel Falls is a real-world inspiration, not its story name.','Victoria Falls is not their named destination.','Iguazu Falls is not their named destination.'],
 'A visual inspiration in Venezuela does not turn Angel Falls into the fictional proper name. The story destination is explicit.',
 'Medium destination recall; q1431 asks the wife\'s identity, q2183 her written message and q1432 Muntz\'s motive, all requiring separate facts.')
review(495,'wall','The Captain\'s luxury ship, with no claim about every surviving human.',
 'Pixar names the human-carrying luxury mother ship the Axiom.',
 ['Axiom is the documented ship.','Genesis differs from its name.','Elysium differs from its name.','Olympus differs from its name.'],
 'The original all-remaining-humans quantifier was not established. Final wording identifies the Captain\'s particular luxury ship and requires only its unique name.',
 'Medium ship-name recall; distinct from Auto identity, captain name, consumer corporation and EVE acronym.')
review(496,'finaldeath','Héctor\'s label after Chicharrón fades; no claim about unknown subsequent existence.',
 'Printed p.67 calls disappearance from this world the Final Death.',
 ['The Final Death is Héctor\'s explicit term.','The Second Journey is not the term in that explanation.','The Rebirth is not the term used there.','The Spirit Awakening is not his term.'],
 'Héctor says no one knows where Chicharrón went. Asking the term avoids making unsupported assertions about reincarnation, ghosts or forever after disappearance.',
 'Medium terminology recall; q2370 asks the preceding song, a different fact. Corrected unsupported forever claim and made all options parallel terms.')
review(497,'wet luca','Luca and Alberto\'s visible wet body regions on land.',
 'The production discussion describes wet/dry-triggered human-to-monster transformation with variable scale coverage.',
 ['Wet parts reveal their sea-monster form.','Human appearance is their dry camouflage, not the wet appearance.','The wet transformation produces scales and monster features, not stone.','The transformation produces physical monster features, not transparency.'],
 'A splash need not transform the whole body. Body-parts wording accommodates partial coverage and asks appearance, avoiding unsupported exclusion of simultaneous strength or breathing abilities.',
 'Medium transformation rule; distinct from film identity q472, town q781 and race q1043. Parallel visual alternatives eliminate the former long-answer clue.')
review(498,'command','Buzz\'s belief about his mission in Toy Story (1995), not the later television series.',
 'The Buzz profile says he believes he is on a secret mission for Star Command.',
 ['Star Command is the named mission organization.','Space Rangers Inc. is not the organization named by Pixar.','Galaxy Patrol is not that name.','Universe Corps is not that name.'],
 'Buzz is a toy who believes the mission is real; the question preserves that distinction. Space Ranger is his role, not evidence of an astronaut training program.',
 'Medium organization-name recall; no television-content scope expansion. Distinct from q298 toy identity and q72 catchphrase.')
review(499,'bugs','Flik\'s colony location name in the original theatrical A Bug\'s Life.',
 'Pixar\'s synopsis explicitly calls the threatened home Ant Island.',
 ['Ant Island is the stated home.','Colony Alpha is not its proper name.','Bug Haven is not its proper name.','Grassland Colony is not its proper name.'],
 'Ant is a species but Ant Island is the actual place name; the other generic colony labels are not alternate names supplied by the source.',
 'Medium location recall. q1272 asks royalty, not island name; the outside-scope Atta/Dot ambiguity is not resolved by this review.')
review(500,'soul','The realm in Soul for forming new souls\' personalities.',
 'Pixar\'s opening synopsis identifies the Great Before and its personality-forming purpose.',
 ['The Great Before is the realm with the stated purpose.','The Great Beyond is the distinct destination Terry counts entrants to, not this realm for new souls.','The Soul World is not the specified proper name.','Limbo is not the specified proper name.'],
 'You Seminar is another designation used in the film but was removed from the sole parenthetical answer. Final stem avoids repeating before and all options are parallel place names.',
 'Medium central world-building recall; q1439 asks Terry\'s identity and q2165 the composers, distinct facts.')
review(272,'aristocats roquefort','The mouse involved in rescuing Duchess\'s family.',
 'D23 directly calls Roquefort a mouse and identifies his rescue role.',
 ['Roquefort is the rescuing mouse.','Toulouse is one of Duchess\'s kittens, not the mouse.','Berlioz is another kitten, not the mouse.','Lafayette is not the specifically identified mouse Roquefort.'],
 'Helping cats alone is too broad, but the mouse qualifier separates Roquefort from the kittens and the farm dog. It does not ask the family\'s human owner.',
 'Medium character-role recall; q1063 asks Madame Bonfamille\'s ownership, not Roquefort\'s rescue role; q311 asks the kitten trio.')
review(309,'fear fearinterview colors','Body color of Fear in original Inside Out.',
 'Museum and production-interview text agree Fear\'s design is purple; the cast listing contrasts the other colors.',
 ['Fear is purple.','Disgust is green, not purple.','Anger is red, not purple.','Sadness is blue, not purple.'],
 'The question concerns the character\'s design color, not clothes, illumination or an emotion-colored memory orb. Each distractor has a different documented color.',
 'Easy visual-design recognition; q1284 tests Disgust/green and q1313 Joy/yellow, different color-to-character facts.', ['direct','contradiction','contradiction','contradiction'])
review(316,'sina sinacast','Moana\'s mother in the original animated film.',
 'The official Sina biography calls her Moana\'s mother, with original-cast English name confirmation.',
 ['Sina is Moana\'s mother.','Tala is her grandmother, not mother.','Pepa is not the mother identified by the official Sina biography.','Tui is Moana\'s father and Sina\'s husband, not her mother.'],
 'A mother-figure reading does not make grandmother Tala the named mother. The exact family role and name are established.',
 'Medium family-name recall; q884 grandmother and q1095 father are separate relations; no remake-only evidence used.')
review(317,'alice toad pan pinocchio','Disneyland California Fantasyland vehicles; current configuration.',
 'Disney describes the Alice ride as an oversized caterpillar and gives different vehicles for each distractor.',
 ['Alice uses the caterpillar.','Mr. Toad uses a motorcar.','Peter Pan uses a pirate ship.','Pinocchio uses a woodcarver\'s cart.'],
 'Fantasyland setting alone fits several choices; the actual vehicles distinguish all four. Alice\'s film authorship is unrelated to vehicle identity.',
 'Medium vehicle recall; q947 tests Lewis Carroll film adaptation and q905 identifies Toad from its story, different facts.', ['direct','contradiction','contradiction','contradiction'])
review(318,'bigben','Final Basil-Ratigan confrontation in the 1986 film.',
 'D23 explicitly places the climactic gearworks fight in Big Ben.',
 ['Big Ben is the named location.','Tower Bridge is not the documented clockwork fight location.','Buckingham Palace is part of the royal plot but not the final clockwork duel.','Westminster Abbey is not the final fight location.'],
 'Distinguish the palace plot from the later climax. Big Ben is the familiar landmark name used by Disney for the clock-tower sequence.',
 'Hard final-scene location recall; distinct from q1332 Basil\'s home address and q325 Ratigan\'s species.')
review(326,'felicia fidget bigben','Name of Ratigan\'s cat, not any servant associated with him.',
 'The Felicia entry names the feline; Fidget has the separate henchman role, while Olivia and Dawson oppose Ratigan.',
 ['Felicia is the named feline.','Fidget is Ratigan\'s henchman, not his cat.','Olivia is the kidnapped toymaker\'s daughter, not the cat.','Dawson is Basil\'s doctor companion, not the cat.'],
 'The original pet wording could be stretched to Fidget; explicitly asking the pet cat excludes this reading. Each distractor\'s role is documented.',
 'Hard secondary-character name; q1115 asks the bat henchman and q2500 his peg leg, separate facts.')
review(329,'goodcompany goodcatalog','Original film attribution of the song Good Company.',
 'Scene commentary and the specific soundtrack catalog place Good Company in Oliver & Company.',
 ['Oliver & Company contains the Jenny/Oliver song.','The Aristocats is not the film credited for this specific song and scene.','The Rescuers is not the film credited for this specific song and scene.','The Fox and the Hound is not the film credited for this specific song and scene.'],
 'Both cat films can depict companionship, but that theme cannot substitute for the actual song credit. Company shared by the song and film titles is necessary nomenclature, not a source establishing the credit.',
 'Medium soundtrack recall; q531 asks a different opening song, while q1003 asks Dodger\'s solo and q1254 Rita\'s, all separate credits.')
review(333,'canada','EPCOT World Showcase location of Far and Wide; not the full answer-giving title in the stem.',
 'Disney names the Canada presentation Canada Far and Wide in Circle-Vision 360.',
 ['Canada is the identified pavilion.','United Kingdom is a different pavilion, not the named Canada presentation\'s location.','France is a different pavilion, not this presentation\'s location.','The American Adventure is a different pavilion, not this Canadian presentation\'s location.'],
 'The shortened title preserves a meaningful location question. Sharing projection technology with other countries does not move this particular named film.',
 'Medium park-film location; q2224 asks China\'s separate Circle-Vision title. Current attraction recheck scheduled.')
review(375,'mintz','1928 Oswald distribution contract renewal; no implication that Walt legally owned the character.',
 'Museum documentation states Mintz demanded a cut instead of the raise Walt requested.',
 ['Charles Mintz made that demand.','Carl Laemmle\'s Universal owned the character, but the negotiation demand is attributed to Mintz.','Roy is Walt\'s partner, not the distributor demanding the cut.','Pat Powers belongs to the later Mickey sound/distribution arrangement.'],
 'Universal ownership is a different question from who demanded the cut. Date and negotiation event distinguish Mintz from the subsequent Powers conflict.',
 'Hard distribution-history recall; q408 asks rights-owning studio, while q2422 asks Mickey\'s creation link. Clarified actor/event without changing answer.')
review(389,'rite fantasiamap whales','Rite of Spring within Fantasia (1940), not other segments or the sequel.',
 'Museum and AFI descriptions specifically identify dinosaurs in Rite of Spring.',
 ['Dinosaurs appear in this evolution sequence.','Centaurs belong to Pastoral Symphony, a different segment.','The dancing mushrooms belong to Nutcracker Suite, a different segment.','Flying whales belong to Pines of Rome in Fantasia/2000, not this sequence.'],
 'The stem specifies the segment, not the whole Fantasia franchise. Its prehistoric life sequence excludes the two mapped fantasy ballets and flying whales.',
 'Medium segment imagery; q2036 asks the flying-whale sequel\'s music, requiring another association.')
review(406,'ports','Tokyo DisneySea themed ports, current description.',
 'The official overview explicitly assigns New York and Cape Cod to American Waterfront.',
 ['American Waterfront has the two American harbors.','Mediterranean Harbor is Southern European.','Port Discovery is a futuristic marina.','Lost River Delta is Central American jungle ruins.'],
 'New York and Cape Cod are a paired geographic theme, not just any waterfront or harbor. All four full official descriptions distinguish the ports.',
 'Hard international-park geography; q2641 asks railway transport, q2507 Lost River Delta\'s regional inspiration, different facts.', ['direct','contradiction','contradiction','contradiction'])
review(427,'5k 5kpanel','Self-paced Castaway Cay run/walk, bounded to November 2026.',
 'The official island guide names the Castaway Cay 5K and classifies it as self-paced.',
 ['Castaway Cay 5K is the identified activity.','Pelican Plunge Sprint is not the official self-paced activity name.','Serenity Bay Dash is not the identified activity name.','Mickey Mile is not the island activity named in this guide.'],
 'No formal start or registration is implied. Pelican Plunge and Serenity Bay exist as island places but do not make the invented run names valid; Mickey Mile is not this named 5K.',
 'Medium recreation-name recall; q141 island name and q1211 waterslide structure are distinct. Scheduled 90-day recheck; production flags left untouched.')
review(436,'palo','Disney Cruise Line venue-name origin, not cuisine or present onboard service availability.',
 'Disney expressly derives Palo from the gondoliers\' long Venetian poles.',
 ['Palo has the stated derivation.','Remy is not the venue named in the derivation.','Enchanté is not the venue named in that derivation.','Lumiere\'s is not the venue named in that derivation.'],
 'The final question follows Disney\'s wording for poles without asserting a particular use or an unbounded age policy. It asks etymology, not which restaurants serve Italian food.',
 'Hard name-origin fact; q430 cuisine and q148 French-restaurant name are distinct. Restored Enchanté\'s spelling.')
review(469,'incredibles','Lucius Best\'s superhero identity in The Incredibles.',
 'Pixar\'s Frozone profile explicitly maps Lucius Best to Frozone.',
 ['Frozone is Lucius\'s hero identity.','Gazerbeam is not the hero identity assigned to Lucius.','Dynaguy is not the identity assigned to Lucius.','Splashdown is not the identity assigned to Lucius.'],
 'All options are superhero names, but the question asks a particular individual\'s alias. Other supers\' existence does not create another Lucius alias.',
 'Medium civilian-name recall; distinct from Bob and Helen identities and Violet\'s powers.')
review(478,'laugh','End of theatrical Monsters, Inc.; after the change from scare work.',
 'Official post-film continuity describes the plant harvesting laughter to fuel Monstropolis.',
 ['Laughter is the new power source.','Screams are the old power source replaced by laughter.','Solar energy is not the new source identified in this transition.','Doors provide access to children, not the newly harvested energy itself.'],
 'Doors need power and route the workers, but the energy input is laughter. After the change excludes the formerly correct screams answer.',
 'Medium ending recall. q640 concerns the prior scream system; this asks the replacement. Series press material is evidence for film ending, with no series trivia added.')
review(487,'nemospecies nemoscene nemoturtles','Nemo\'s classmate Sheldon\'s species in Finding Nemo.',
 'Aquarium and scene commentary identify Sheldon as a seahorse and distinguish Tad and Pearl; Pixar identifies Squirt as a turtle.',
 ['Sheldon is the seahorse.','Tad is a butterflyfish, not a seahorse.','Pearl is an octopus, not a seahorse.','Squirt is a turtle, not a seahorse.'],
 'Although Squirt joins the school at the ending, he is still a turtle. This does not make the schoolmate qualifier an ambiguous species test.',
 'Medium minor-character identity; q1299 asks Crush\'s son and q1049 teacher, separate relationships.', ['direct','contradiction','contradiction','contradiction'])
review(488,'luigi','Luigi\'s tire-shop proper name in Cars.',
 'Pixar explicitly names Luigi\'s Casa Della Tires.',
 ['Casa Della Tires is the documented shop name with Luigi\'s prefix omitted.','Luigi\'s Wheel Works is not the stated shop name.','Radiator Rubber is not the stated shop name.','Piston Cup Tires is not the stated shop name.'],
 'A generic business owned by Luigi could have many descriptive names; only Casa Della Tires matches the proper name. Guido assists rather than renames the shop.',
 'Medium storefront-name recall; distinct from Ramone\'s body-shop identity and Sally\'s motel role.')

qs = {q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
planned = json.loads((ROOT/'audit/runs/next-shard-0010-plan.json').read_text())['questionIds']
assert set(rows) == {i for i in planned if i in qs}
notes = dict(schema=1, reviewer='Codex', at=AT, sourcesChecked=sorted({'b10-'+s for row in rows.values() for s in row[0]}), reviews=[])
for qid, (keys, context, premise, reasons, challenge, editorial, bases) in rows.items():
    keys = ['b10-'+s for s in keys]
    mutable = any(library['sources'][s]['timeSensitive'] for s in keys)
    notes['reviews'].append(dict(questionId=qid, hash=digest(qs[qid]), checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'], notes=editorial, context=context, timeSensitive=mutable, nextReviewAt=DUE if mutable else None, premise=dict(reason=premise,sources=keys), options=[dict(basis=(bases or ['direct','exclusive-inference','exclusive-inference','exclusive-inference'])[i],reason=reason,sources=keys) for i,reason in enumerate(reasons)], challenge=dict(reviewer='Codex',at=AT,premiseChecked=True,alternativesExcluded=True,notes=challenge)))
(ROOT/'audit/source-notes.json').write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'audit/runs/next-shard-0010-evidence-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Authored {len(rows)} final-wording reviews with individual four-option rationales and challenges.')
