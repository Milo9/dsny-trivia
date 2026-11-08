"""Explicit evidence notes from the batch 23 research; does not edit questions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))
def write(p, value):
    (ROOT / p).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

library = read('audit/source-notes.json')
def source(key, url, locator, evidence, changing=False, limitation='Institutional text inspected; no film or video playback claimed.'):
    library['sources']['b23-'+key] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt='2026-11-08', timeSensitive=changing,
        nextReviewAt='2027-02-05' if changing else None, limitations=limitation, topics=['Batch 23'])

D='https://d23.com/a-to-z/'
C='https://disneycruise.disney.go.com/'
S='https://www.springfieldspringfield.co.uk/movie_script.php?movie='
source('verne',D+'20000-leagues-under-the-sea-film/','Release and adaptation sentences','The 1954 Disney film adapts Jules Verne, not Wells, Stevenson or Twain.')
source('junglelast',D+'jungle-book-the-film/','Release date and last-supervised-feature sentence','The Jungle Book was the last animated feature Walt supervised; it was released in 1967.')
source('junglelast2','https://d23.com/the-1967-premiere-of-the-jungle-book-was-a-swinging-star-studded-safari/','Opening paragraphs, premiere invitation','The premiere account independently identifies The Jungle Book as the last animated feature personally supervised by Walt.')
source('ranch','https://www.waltdisney.org/blog/new-heights-walt-disneys-golden-oak-ranch','March 11, 1959 purchase paragraph','Walt Disney Productions purchased Golden Oak Ranch in 1959 as a filming location.')
source('star','https://content.ucpress.edu/pages/10093/10093.ch01.pdf','PDF page 20 / printed page 16; return from France and art-department application','After returning to Kansas City, Walt sought work at the Star, which had no art-department vacancies; a separate office-boy application failed too.',False,'Michael Barrier scholarly biography quoting Walt recollections; secondary historical evidence, not the false fired-for-lacking-imagination story.')
source('island',C+'en-ca/disney-island-destinations/castaway-cay/','Pelican Plunge, Post Office, Port Adventures and Olaf location sections','Pelican Plunge has two twisting waterslides into the lagoon. The dock post office gives mail the Castaway Cay postmark. Private cabanas are reservable extras. Olaf is near the Pelican Point tram stop.',True)
source('spring','https://plandisney.disney.go.com/question/water-spring-leak-castaway-cay-clean-chlorinated-568774/','March 11 2024 answer, first descriptive paragraph','Spring-A-Leak is a freshwater play area with splash pads, misters and dripping pipes.',True,'Disney-hosted panelist reports a conversation with a crew member; no promise of daily availability.')
source('springdesign','https://disneyvacationclub.disney.go.com/media/dvc/languagespecific/eng/member/justformembers/disneyfilesmagazine/2010/DisneyFilesMagazine_Summer2010.pdf','Printed pages 5-6, Castaway Cay additions, Spring-a-Leak paragraph','Spring-a-Leak depicts a storm-damaged beach dwelling with dripping pipes, broken plumbing and hissing misters; contrasted with the offshore Pelican Plunge platform.')
source('islandmap','https://disneysquared.com/wp-content/uploads/2019/06/CastawayCayMap2018.pdf','Map attractions list, G Monstro Point; E Scuttles Cove; P Pelican Plunge','The Disney-issued map labels Monstro Point as the whale dig site, Scuttles Cove as childrens program areas and Pelican Plunge separately.',False,'Official map hosted by third party; indexed full map legend inspected. PDF fetch had no readable lines; no claim to have visually inspected its map geometry.')
source('tramfree','https://cdn1.parksmedia.wdprapps.disney.com/media/blog/wp-content/uploads/2023/06/planDisney-Disney-Castaway-Cay-Pocket-Guide.pdf','Transportation paragraph, complimentary trams and beach stops','The official guide describes complimentary trams with two Family Beach stops and a connection to Serenity Bay.',True,'Indexed guide transportation passage inspected; PDF extraction was empty. Corroborated by current official destination page tram stop and panel route account.')
source('eye',C+'en-as/onboard-activities/eye-scream-treats/','Opening description','Eye Scream Treats is named after Mike Wazowski and serves soft-serve ice cream.',True)
source('festival',C+'en-ca/onboard-activities/mickey-friends-festival-of-foods/','Ship Locations, opening description and Fast & Fresh','Wish has this open-air quick-bite area on the upper decks, offering pizza, burgers, tacos and BBQ.',True)
source('cove',C+'en-gb/onboard-activities/cove-cafe/','Adult Exclusive and opening description','Cove Cafe is an adults-only lounge serving coffee, tea and drinks.',True)
source('lab',C+'en-gb/onboard-activities/oceaneer-lab-youth-club/','Ship locations; Designed for Kids; On the Disney Fantasy','Oceaneer Lab serves children with experiments, science labs and workshops; staffed by Disney Youth Counselors.',True)
source('youth',C+'en-eu/onboard-activities/list/magic-ship/','Oceaneer Club, Oceaneer Lab, Edge and Vibe entries','Club, Lab, Edge and Vibe are classified as Youth Clubs; Cove Cafe is a lounge.',True)
source('wonder',C+'en-eu/ships/wonder/','Action-Packed Kids Clubs and Oasis on the High Seas','Vibe serves teens, Edge tweens, Club young children, and Quiet Cove is an adults-only pool area.',True)
source('meyer','https://www.meyerwerft.de/en/ships/ship_detail/disney_dream','Opening builder paragraphs, Papenburg ships and sister ship','Meyer Werft built Dream in Papenburg and also built sister ship Fantasy.')
source('meyer2','https://www.meyerwerft.de/en/ships/ship_detail/disney_fantasy','Opening construction paragraph','Fantasy is the second Disney cruise ship built by Meyer Werft.')
source('statues','https://www.disneyholidays.co.uk/disney-cruise-line/ships/disney-fantasy/','Fun Facts, Mademoiselle Minnie and Admiral Donald sentence','Mademoiselle Minnie is the Fantasy lobby statue and Admiral Donald the Dream lobby statue.',True)
source('wishstatue','https://disneyparksblog.com/disney-experiences/beginners-guide-to-the-disney-wish-cruise-ship/','Welcome Aboard','A bronze Cinderella welcomes guests into Wish Grand Hall.',True)
source('rooms',C+'en-gb/ships/dream/staterooms-overview/','Inside; Deluxe Oceanview; Deluxe Oceanview with Verandah; Concierge Royal Suite','Dream uses Stateroom in standard category names. Inside has a virtual porthole; Oceanview has a real window; Verandah categories have private balconies.',True)
source('transfers','https://www.disneyholidays.co.uk/disney-cruise-line/help/frequently-asked-questions/getting-to-your-disney-cruise/','Are transfers included from the airport to the port','Transfers can be added to carry guests between airport and cruise ship.',True)
source('groundterms',C+'contracts-terms-safety/terms-conditions/singapore/','Ground Transfer Information','Disney calls airport-port transport ground transfers, distinguishing it from shore excursions.',True,'Only transport naming is used; no legal advice, cancellation policy or region-wide availability inference.')
source('seaday','https://disneyparksblog.com/dcl/disney-wish-itineraries/','3-Night Itinerary: Castaway Cay and Day at Sea, route and voyage paragraphs','The route distinguishes Castaway Cay from a full day at sea spent enjoying the ship.')
source('debark','https://plandisney.disney.go.com/question/happen-morning-disembarkation-breakfast-time-leave-room-631980/','February 12 2026 answer, final breakfast and leaving-ship paragraphs','Debarking is leaving the ship on the last morning of the cruise.',False,'Disney-hosted panel advice; used for terminology, not departure time or policy.')
source('tender',C+'en-au/faq/ports-port-adventure-excursions/getting-on-off-ship/','Answer opening paragraph','Docked ships use a gangway; ships anchored offshore transport guests to the dock in smaller tender boats.')
source('card',C+'en-gb/faq/bands-cards/using-key-to-the-world-card/','Answer paragraphs 1-2','Key to the World cards are issued for room entry and charging purchases; DisneyBand+ can also do some tasks.',True)
source('wishbars','https://d23.com/set-sail-for-fun-with-new-ways-for-adults-to-relax-recharge-and-reconnect-on-the-disney-wish/','Enchanting Nightlife, named lounge paragraphs; Exquisite Specialty Dining','Keg & Compass evokes a Norwegian sailor map room; Nightingale is Cinderella-inspired; Bayou is Princess and Frog-inspired; Hyperspace is Star Wars; Rose is Beauty and Beast-inspired.',True)
source('treasurebars','https://disneyparksblog.com/dcl/every-place-you-can-eat-onboard-the-disney-treasure/','Lounge Spaces, Skipper Society and Periscope Pub','Skipper Society takes its theme from Jungle Cruise; Periscope Pub from the 1954 20000 Leagues film.',True)
source('hidden',D+'hidden-mickeys/','Complete entry','Hidden Mickeys are subtly visible Mickey silhouettes or three-circle forms in Disney designs.')
source('hiddencruise','https://allears.net/2014/10/27/disney-magic-cruise-ship-hidden-mickeys/','Opening Oceaneer Lab photograph and description','An eyewitness documents a three-circle Mickey worked into a painting aboard Disney Magic.',False,'First-person ship photographs and descriptions corroborate application of Disney term aboard ships; no claim these exact items remain today.')
source('tram','https://plandisney.disney.go.com/question/moved-tram-stop-closer-ship-ondisneys-cay-351155/','Answer describing Kargo Handling, Scuttles Cove, Pelican Point stops','Castaway Cay uses trams between stops near the dock and family beaches.',True,'Disney-hosted panel guidance corroborated by the current destination page reference to Pelican Point tram stop.')

# Scene transcripts are secondary transcriptions; primary catalog entries below
# corroborate film/song identities. No original-film playback is claimed.
def scene(key,slug,locator,evidence):
    source(key,S+slug,locator,evidence,False,'Secondary transcription of film dialogue/song sequence; corroborated by institutional song/catalog evidence; no film playback claimed.')
scene('snow','snow-white-and-the-seven-dwarfs','Forest animals encounter, lines 123-151','Snow White sings With a Smile and a Song after her frightened escape into the forest.')
source('snowrecord','https://americanhistory.si.edu/collections/object/nmah_667456','Object description, RCA Victor record and Songs From Walt Disney Snow White album','Museum record associates With a Smile and a Song with the Snow White album.',False,'Full object-page fetch returned an error; indexed museum object description inspected and corroborated with film transcription, not used alone.')
scene('pinocchio','pinocchio','Opening puppet demonstration lines 111-143; conscience lesson 287-350; school journey and Stromboli stage later','Geppetto sings Little Wooden Head at the first puppet demonstration; Jiminy sings Give a Little Whistle; Honest John sings Hi Diddle Dee Dee; Pinocchio performs Ive Got No Strings for Stromboli.')
source('pinmusic','https://catalog.afi.com/Catalog/MovieDetails/5131','Songs list','AFI lists Little Wooden Head, Ive Got No Strings, Give a Little Whistle and Hi Diddle Dee Dee among Pinocchio songs.',False,'Indexed institutional music listing corroborates transcript song names; not independent proof of every scene.')
scene('dumbo','dumbo','Bubble visions 709-759; Baby Mine mother visit; Casey departure; roustabout tent raising','Pink Elephants on Parade accompanies the bubble visions; Baby Mine is the mother lullaby; Casey Junior the train song; roustabouts sing during work.')
source('dumbomusic',D+'dumbo-film/','Song paragraph','D23 lists Pink Elephants on Parade and Baby Mine in the 1941 Dumbo.')
scene('cinderella','cinderella','Mice plan and dressmaking 481-525; later Dream reprise 564-579; Fairy Godmother and ballroom later','Mice begin the dressmaking plan with The Work Song. A later Dream reprise also occurs while the dress is completed; Bibbidi is the magic scene, So This Is Love the ballroom, Nightingale the washing/music-lesson sequence.')
source('cindmusic',D+'cinderella-film/','Songs paragraph','D23 lists The Work Song, A Dream Is a Wish Your Heart Makes, So This Is Love and Bibbidi-Bobbidi-Boo.')
scene('alice','alice-in-wonderland','Tea party 993-1066; caucus shore, flower garden and card gardeners earlier/later','Unbirthday is the tea-party number; Caucus Race belongs to the shore, Golden Afternoon to flowers, Painting Roses to card gardeners.')
source('alicemusic',D+'alice-in-wonderland-film/','Tea-party synopsis and song list','D23 describes Hatter and Hare celebrating an unbirthday at tea and lists The Unbirthday Song.')
scene('peter','peter-pan','Pixie dust and first flight 450-528; opening Star and later pirate/marching scenes','You Can Fly accompanies the Darlings first flight; Second Star opens the film; Following the Leader is the Lost Boys march; Pirates Life introduces pirates.')
source('petermusic',D+'peter-pan-film/','Synopsis and songs paragraph','D23 describes Peter teaching the Darlings flight and lists You Can Fly and Second Star.')
scene('lady','lady-and-the-tramp','Pound introduction of Peg and song 959-1026; restaurant song 808-824; opening Christmas and baby lullaby','Peg sings Hes a Tramp in the pound; Bella Notte is the restaurant serenade; La La Lu the baby lullaby; Peace on Earth the Christmas number.')
source('ladymusic',D+'lady-and-the-tramp-film/','Songs paragraph','D23 lists Hes a Tramp among the 1955 films songs.')
source('sleepmusic',D+'sleeping-beauty-film/','George Bruns orchestral score paragraph','George Bruns adapted themes from Tchaikovsky ballet for Sleeping Beauty score; Tchaikovsky is the source composer, not Bruns.')
scene('aristocats','aristocats-the','Scat Cat arrival and jam 1025-1149; opening, kitten lesson and OMalley introduction','Everybody Wants to Be a Cat is Scat Cat band jam at OMalley home; Scales and Arpeggios is kitten practice; Thomas OMalley his introduction; Aristocats the title tune.')
source('aristomusic',D+'aristocats-the-film/','Music credits paragraphs','D23 lists Everybody Wants to Be a Cat, Thomas OMalley, Scales and Arpeggios and the title song as separate numbers.')
source('robinmusic','https://catalog.afi.com/Film/55027-ROBIN-HOOD','Songs section and cast Phil Harris/Little John; forest celebration in Synopsis','Phony King is sung by Phil Harris as Little John; Oo De Lally and Not in Nottingham by Roger Miller; Love by Nancy Adams. The forest party ridicules John.',False,'Institutional catalog credits and synopsis corroborate Disney song list; transcript omits some songs.')
scene('rescuers','the-rescuers','Opening emergency meeting 25-65; opening Journey, Penny sadness and later travel montage','Mouse delegates sing Rescue Aid Society at the emergency meeting; Journey is opening, Someone Waiting the Penny consolation song, Tomorrow Another Day the travel song.')
source('rescuemusic',D+'rescuers-the-film/','Song list','D23 identifies all four songs as distinct Rescuers numbers.')
scene('ratigan','great-mouse-detective-the','Ratigan lair celebration 297-408, Bartholomew calls him a rat at 359; tavern later','Worlds Greatest Criminal Mind praises Ratigan at his lair before Bartholomew offense; Let Me Be Good to You is the tavern act. Goodbye So Soon is his later trap recording.')
source('ratmusic',D+'great-mouse-detective-the-film/','Music paragraph','The film contains three featured songs, including Melissa Manchester Let Me Be Good to You; Henry Mancini collaborated on the other two.')
source('ratalbum','https://classical.music.apple.com/us/album/1444080679','Complete Disney-licensed soundtrack, vocal tracks and copyright line','The Disney-licensed album lists Worlds Greatest Criminal Mind and Goodbye So Soon with Vincent Price, and Let Me Be Good to You with Melissa Manchester. No Rat Trap vocal number appears in this listing.')
scene('oliver','oliver-and-company','Street-survival lesson 615-659; Dodger early solo; Jenny montage; Georgette entrance','Streets of Gold is Rita street-survival lesson; Why Should I Worry is Dodger; Good Company is Jenny; Perfect Isnt Easy is Georgette.')
source('olivermusic',D+'oliver-company-film/','Cast and music credits','D23 identifies Rita, Dodger and Georgette cast roles and credits Streets of Gold, Why Should I Worry and Perfect Isnt Easy as distinct songs.')
source('ritacredits','https://en.wikipedia.org/wiki/Oliver_%26_Company','Voice cast Rita and Georgette; reception paragraphs on musical performances','Ruth Pointer supplies Rita singing voice; reception identifies Streets of Gold with Pointer. Billy Joel is Dodger and Bette Midler is Georgette.',False,'Secondary cast/performance reference supplements the primary Disney credit list and scene transcription. Jenny Good Company assignment comes from the transcript, not this page.')
scene('beast','beauty-and-the-beast-1991','Snowy garden feelings sequence 1351-1394; dinner show, tavern and mob later/earlier','Something There expresses Belle and Beast changing feelings; Be Our Guest the servants dinner show; Gaston the tavern praise; Mob Song the attack rally.')

write('audit/source-notes.json',library)

# Four ordered option reasons and a separate adversarial challenge, authored
# explicitly for the final questions. Sources may be shared only where the
# uniquely named identity or separately described scene excludes alternatives.
data={}
def review(i, keys, premise, reasons, challenge, context, changing=False, notes=''):
    data[i]=(keys.split(),premise,reasons,challenge,context,changing,notes)

review(1205,'b23-verne','The Disney adaptation explicitly credits Verne as the original story author.',
 ['Verne is the credited source novelist.','Wells is not the novelist credited for this adaptation.','Stevenson is not the source author identified by Disney.','Twain is not the author credited for this novel.'],
 'Screenwriter Earl Felton is distinct from the source novelist. Only Verne is assigned original authorship, excluding all three competing authors.','Disney 1954 live-action feature; original novel authorship.')
review(1207,'b23-junglelast b23-junglelast2','Disney identifies Jungle Book as the last animated feature Walt personally supervised.',
 ['Jungle Book is explicitly the last supervised animated feature.','Aristocats had early Walt involvement, but was not the last feature he supervised.','Robin Hood was produced after Walt death and is not the identified supervised feature.','Sword in Stone predates Jungle Book, so is not the last supervised feature.'],
 'The original personally-worked-on phrasing could include early Aristocats development and later Pooh compilations. Supervised is the source claim. Removed 1967 clue so #688 release chronology alone does not answer this.','Feature supervision, not release during his lifetime or any preliminary involvement.')
review(1208,'b23-ranch','Museum account identifies Walt Disney Productions purchase of Golden Oak Ranch in 1959.',
 ['Golden Oak is the purchased filming ranch.','Smoke Tree was Walt retreat, not this studio film-ranch purchase.','Carolwood is not the name given in the purchase record.','Hyperion is not the ranch identified in the purchase account.'],
 'Studio ownership of the filming property is explicit; Walt private Smoke Tree retreat from #958 is a different fact and cannot substitute for this purchase.','California film property purchase by Walt Disney Productions, 1959.')
review(1209,'b23-star','Barrier account identifies the Star as having no art vacancy when Walt returned in 1919.',
 ['The Star is explicitly the paper whose art department had no vacancy.','The Times is not the paper named for this application.','Chicago Tribune is not the named Kansas City application.','Los Angeles Times is not the named newspaper.'],
 'This was not a dismissal for lacking imagination. The final premise states no vacancy and separates the later office-boy rejection. Two newspapers share Kansas City but only Star is identified in the application account.','1919 return to Kansas City after France; art-department application, not firing.')
review(1211,'b23-island b23-spring b18-island b23-islandmap','Disney names Pelican Plunge as the offshore platform with two twisting waterslides.',
 ['Pelican Plunge is the platform with slides into the lagoon.','Scuttle Cove is supervised sand-and-games play.','Spring a Leak is the shore splash pad, not the offshore slide platform.','Monstro Point is the whale-bone dig area, not the slide platform.'],
 'Spring a Leak has water play, but not this offshore pair of slides; Scuttle and Monstro are land play. Refurbishment can affect opening, so no promise of availability is inferred.','Castaway Cay attraction identity, checked November 2026.',True)
review(1213,'b23-island','Disney dock post office sends letters with the Castaway Cay island postmark.',
 ['The post office is explicitly the mailing amenity.','No message-bottle service is the named postal facility.','Navigator is not the island postal office.','Harbor mailbox is not the official amenity identified here.'],
 'A ship guest-services desk may accept mail, but this asks the island amenity with its special postmark. The source specifically places that post office on the dock.','Castaway Cay in The Bahamas; special postal facility, not delivery speed.',True)
review(1214,'b23-spring b23-springdesign b23-island b18-island b23-islandmap','The storm-damaged splash-and-play setting is Spring-A-Leak.',
 ['Spring a Leak has the splash pads and misters.','Pelican Plunge is the offshore slide platform.','Scuttle Cove is supervised play and sand activities, not the named splash-pad attraction.','Monstro Point names a whale-bone dig, not the splash pad.'],
 'Scuttle can include water play too, so final wording requires the storm-damaged dwelling theme with pipes and misters. The Disney magazine assigns these features specifically to Spring a Leak and separately describes Pelican Plunge offshore.','Castaway Cay themed splash-and-play attraction.',True)
review(1215,'b23-eye','Disney explicitly derives Eye Scream Treats from Mike Wazowski.',
 ['Eye Scream is explicitly named after Mike and serves soft serve.','Frozone is a different character name, not the Mike-derived pun.','Cove Cafe is a coffee lounge, not the Mike-named ice cream counter.','Sweet on You is not the name Disney says was derived from Mike.'],
 'Other outlets can serve frozen treats, but the question requires the documented Mike naming origin. The official page states that origin explicitly.','Naming inspiration for soft-serve outlet, not availability on every ship.',True)
review(1216,'b23-festival b18-wish b18-dream b18-cabanas','Wish open-air poolside counter grouping is Mickey & Friends Festival of Foods.',
 ['Festival is explicitly the quick-bite area with these counters.','Marceline is the indoor marketplace, not this open-air grouping.','Flo Cafe is on Dream and Fantasy, not this Wish venue.','Cabanas is not the named Wish poolside grouping.'],
 'Marceline also provides casual food but does not satisfy poolside open-air counter grouping. Removed Mickey/friends words from stem; full normal venue name is necessarily longer than the other venue names.','Disney Wish upper-deck quick-service grouping.',True)
review(1217,'b23-cove b23-youth b23-wonder','Cove Cafe is explicitly an adults-only coffee lounge.',
 ['Cove Cafe is the adult coffee lounge.','Oceaneer Club is for children.','Vibe is a teen club, not an adult cafe.','Edge is a tween club, not an adult cafe.'],
 'Youth open-house access does not turn a youth club into the designated adult coffee lounge. Both adult audience and coffee-lounge function are required.','Named adult lounge compared with youth venues.',True)
review(1218,'b23-lab b23-wonder','Fantasy Lab offers science labs, workshops and experiments for children.',
 ['Oceaneer Lab explicitly has the described science and workshops.','Vibe serves teens, not the described children club.','Edge serves tweens, not this named children science space.','Quiet Cove is an adult pool area.'],
 'The old interactive-activities stem could fit multiple youth spaces. Final wording asks the Fantasy children science venue; it is not a claim that teens never do an experiment.','Disney Fantasy children club; ship selected from the official location list.',True)
review(1219,'b9-magicitaly b9-wonderitaly b9-fleet2024','Fincantieri built both original Disney ships in Italy.',
 ['Fincantieri is identified for both Magic and Wonder.','Meyer is not the builder assigned to these two ships.','Chantiers is not their recorded builder.','Harland and Wolff is not their recorded builder.'],
 'A builder of later Disney ships does not become builder of Magic/Wonder. Company attribution is a new fact beyond #433 Italy; the fleet table and separate ship accounts agree.','Original Magic and Wonder shipbuilding attribution, historical.')
review(1220,'b23-meyer b23-meyer2','The builder identifies itself as constructor of both Dream and Fantasy in Papenburg.',
 ['Meyer Werft built both named ships.','Fincantieri built the earlier pair, not these.','Blohm+Voss is not the builder credited for Dream or Fantasy.','Chantiers is not the builder named in either ship record.'],
 'Dream delivery in 2010 and maiden voyage in 2011 are different milestones; neither changes the builder. Both ship-specific builder pages identify Meyer.','Dream and Fantasy builder, Germany; historical.')
review(1221,'b23-statues','Official ship account assigns Admiral Donald to the Dream lobby.',
 ['Dream has Admiral Donald.','Magic is not the ship assigned Admiral Donald in this pairing.','Wonder is not the identified Admiral Donald ship.','Fantasy has Mademoiselle Minnie instead.'],
 'The question is the named main-atrium statue, not any Donald depiction onboard. Minnie and Donald are assigned to distinct sister ships; Magic/Wonder cannot substitute for Dream. Statue identity differs from stage-show or maiden-voyage facts.','Main atrium bronze statue assignment; November 2026.',True)
review(1222,'b23-statues','Official ship account assigns Mademoiselle Minnie to Fantasy lobby.',
 ['Fantasy has Mademoiselle Minnie.','Dream instead has Admiral Donald.','Wonder is not the Minnie ship identified in the pairing.','Magic is not the ship assigned Mademoiselle Minnie.'],
 'Any Minnie art elsewhere does not satisfy the main atrium bronze statue identity. Each character-ship mapping is independent; knowing Dream Donald does not logically locate Minnie.','Main atrium bronze statue assignment; November 2026.',True)
review(1223,'b23-wishstatue b23-statues','Disney Wish welcome account explicitly identifies bronze Cinderella in Grand Hall.',
 ['Wish has the described Grand Hall Cinderella.','Fantasy has Minnie, not this Grand Hall statue.','Dream has Donald, not Cinderella as its lobby statue.','Magic is not the ship identified by the Grand Hall account.'],
 'Cinderella imagery in other ships does not make it their Grand Hall bronze centerpiece. Statue assignment is distinct from ship size, class, opening date or stage shows.','Disney Wish Grand Hall centerpiece; November 2026.',True)
review(1224,'b23-rooms','Dream Deluxe Oceanview uses a real porthole and lacks the Verandah category balcony.',
 ['Deluxe Oceanview has the real porthole without private verandah.','Standard Inside has a virtual porthole, not a real window.','Royal Suite with Verandah explicitly includes a balcony.','Oceanview with Verandah explicitly includes a balcony.'],
 'Some concierge rooms on other ships have windows without balconies, so final options use exact Dream categories. A virtual porthole is excluded by real; a window in a balcony room does not satisfy without balcony.','Disney Dream exact accommodation categories.',True)
review(1225,'b23-transfers b23-groundterms b23-tender b18-muster','Disney names airport-to-port transport ground transfers.',
 ['Ground transfers is the land transport service.','Port Adventures are shore excursions, not the airport transfer service.','Tendering uses small boats between anchored ship and shore.','Muster names a safety assembly, not land transport.'],
 'A shore excursion might include a bus, but does not become the airport/hotel transfer product. Ground transport identity is distinct from vehicle type and does not promise every hotel is served.','Service name; routes and availability vary.',True)
review(1226,'b23-seaday b18-muster b18-port','Disney itinerary distinguishes a day at sea from port and boarding days.',
 ['Sea day is the full day without a port stop.','Port day has a port call.','Embarkation day is the starting boarding day.','Muster is a drill, not the label for a full no-port cruise day.'],
 'Guests may stay aboard during a port call, but that does not turn the itinerary into a sea day. A muster exercise can happen on a sailing day without naming that day.','Cruise itinerary terminology, not a specific scheduled sailing.')
review(1227,'b23-debark b18-muster b23-tender','Disney uses debarkation for guests leaving at cruise end.',
 ['Debarkation is leaving at the end.','Embarkation is boarding at the beginning.','Muster is the safety drill.','Tendering is transport by small boat, not the end-of-voyage process.'],
 'Debark can also mean leaving at a port, but end-of-cruise leaving is still correctly debarkation. Tendering could be a transport method on a visit; it does not replace this process label.','End-of-voyage terminology; no timing or customs policy asserted.')
review(1228,'b23-tender b18-muster','Anchored ships use smaller tender boats to reach the dock.',
 ['Tendering is that small-boat transfer.','Mustering is safety assembly.','Rotating describes dining changes, not a boat transfer.','Docking is bringing the ship to a pier, the alternative to remaining offshore.'],
 'Tender boarding is physically embarking a boat, but among these options only tendering names this ship-shore transfer process; docking is explicitly contrasted in Disney FAQ.','Anchored-offshore ship-to-shore transport terminology.')
review(1229,'b23-card','Disney continues issuing Key to the World cards for room entry and onboard charges.',
 ['Key to the World is explicitly the issued card.','SeaPass is not the card named by Disney FAQ.','Sail and Sign is not Disney issued card name.','SeaPass Plus is not the card identified by Disney.'],
 'DisneyBand+ can perform overlapping functions, so removed the band distractor and specified physical card. Only the issued card name is asked; no claim it is the sole access method.','Physical Disney cruise card, current FAQ.',True)
review(1230,'b23-youth b23-lab b23-wonder','The four spaces are youth clubs overseen by Disney Youth Counselors.',
 ['Youth activities is the umbrella program for these clubs.','Port Adventures concern shore excursions, not the onboard clubs program.','Room service delivers food to rooms, not youth clubs.','Rotational dining governs restaurant schedules, not these clubs.'],
 'The ship fleet wording groups offerings across ships; it does not say all four are on every ship. Two old resolved player complaints concerned vague original wording; the current named-club stem supplies concrete context.','Program grouping across Disney ships; excludes a claim of identical fleetwide facilities.',True)
review(1231,'b23-wishbars','Keg and Compass evokes a nineteenth-century Norwegian sailor map room.',
 ['Keg and Compass is the nautical-exploration pub.','Bayou follows Princess and Frog/New Orleans.','Nightingale follows Cinderella music.','Rose follows Beauty and Beast.'],
 'A shipboard bar is nautical by location, but this asks design theme. The source explicitly contrasts the venues and identifies Norwegian seafaring for Keg and Compass.','Disney Wish pub design theme.',True)
review(1232,'b23-wishbars','Nightingale piano bar is inspired by Cinderella Sing Sweet Nightingale.',
 ['Nightingale is explicitly Cinderella inspired.','Bayou is Princess and Frog inspired.','Keg is Norwegian seafaring inspired.','Hyperspace is Star Wars inspired.'],
 'All lounges on a ship can share a general enchantment aesthetic; the asked film inspiration is explicitly assigned only to Nightingale among the choices.','Disney Wish lounge inspiration.',True)
review(1233,'b23-treasurebars b23-wishbars','Periscope Pub uses the 1954 20000 Leagues film theme.',
 ['Periscope is the film-inspired submarine pub.','Haunted Mansion Parlor uses Haunted Mansion theme.','Skipper Society uses Jungle Cruise theme.','Rose uses Beauty and Beast theme.'],
 'Periscope also references the former park ride, but this does not invalidate its explicit film inspiration. The other venues have separate documented themes.','Disney Treasure pub theme.',True)
review(1234,'b23-treasurebars b23-wishbars','Skipper Society is explicitly Jungle Cruise inspired.',
 ['Skipper Society is the Jungle Cruise-inspired lounge.','Periscope is 20000 Leagues inspired.','Bayou uses Princess and Frog.','Nightingale uses Cinderella.'],
 'Generic adventure overlaps with Periscope, so the question specifically requires Jungle Cruise rather than any exploration theme. Source assigns the exact attraction.','Disney Treasure lounge inspiration.',True)
review(1236,'b23-hidden b23-hiddencruise','The term Hidden Mickeys denotes subtle Mickey forms, including on cruise ships.',
 ['Hidden Mickeys is Disney documented term.','Magic Marks is not the documented name.','Castaway Icons is not the identified term.','Pixie Prints is not the name of these Mickey silhouettes.'],
 'Original wording included any hidden character, which could include non-Mickey Easter eggs. Final wording specifies Mickey silhouettes and removes hidden from the stem; necessary character context is not the complete answer.','Terminology for decor silhouettes, not a current inventory of particular pieces.')
review(1237,'b23-island','Disney lists private cabana reservations among Castaway Cay extras.',
 ['Cabanas is the documented rental.','Bungalows is not the listed island rental name.','Verandahs are ship balconies, not this island rental.','Villas is not the beachfront rental identified here.'],
 'Cabana can be described generically as a small shelter, but the question asks the rental name. Cabanas restaurant #974 is an unrelated use of the same word.','Castaway Cay rental amenity, subject to availability.',True)
review(1238,'b23-tram b23-tramfree b23-island','Castaway Cay has complimentary trams serving beach stops.',
 ['Tram is the documented island transport.','Monorail is not this island vehicle service.','Skyliner is not the described ground route.','PeopleMover is not the island service name.'],
 'Walking and rented bikes also move guests around, so narrowed the question to the complimentary vehicle service between beach stops. None of those omitted activities makes the other listed branded systems defensible.','Castaway Cay transport, not a promise of a specific current timetable.',True)
review(1240,'b23-rooms','Disney labels standard room categories as Staterooms.',
 ['Staterooms is the general label in those category headings.','Villas is not the label on these room categories.','Bungalows is not the category label.','Chalets is not the heading used by Disney.'],
 'Cabins was a synonym and Suites a legitimate subset under original broad question. Final asks the actual general category label, with competing labels rather than true synonyms.','Official accommodation nomenclature, not a claim cabins is incorrect English.')

review(1241,'b23-snow b23-snowrecord','The 1937 Snow White film includes With a Smile and a Song.',
 ['Snow White contains the forest song in the transcript and museum record.','Cinderella is not the original film identified for this song.','Sleeping Beauty is not the film associated with this recording.','Bambi is not the film in which this Snow White song appears.'],
 'Song title alone could be reused outside Disney, but the question asks its Disney film placement. Both the film transcript and cataloged Snow White record identify the same film; other Snow White music questions test different numbers.','Original Disney film association, not every later cover.')
review(1242,'b23-pinocchio b23-pinmusic','Geppetto sings Little Wooden Head in his initial puppet demonstration.',
 ['Little Wooden Head accompanies Geppetto manipulating the new puppet.','Ive Got No Strings belongs to Pinocchio Stromboli performance.','Give a Little Whistle is Jiminy conscience lesson.','Hi Diddle Dee Dee is Honest John actor recruitment song.'],
 '2022 Pinocchio changes Geppetto music, so final specifies 1940. Original opening puppet demonstration is separate from Pinocchio later stage performance in #994.','1940 animated film, Geppetto opening demonstration.')
review(1243,'b23-dumbo b23-dumbomusic','Pink Elephants accompanies the surreal bubble visions.',
 ['Pink Elephants is the sequence song.','Baby Mine accompanies mother-child reunion.','Casey Junior is the circus train song.','Roustabouts accompanies tent-raising work.'],
 'The sequence is intoxicated hallucination rather than ordinary sleep dream; final says visions. The mother lullaby can feel dreamlike but does not accompany the bubbles.','1941 animated Dumbo, bubble hallucination sequence.')
review(1244,'b23-cinderella b23-cindmusic','The mice begin their dressmaking plan with The Work Song.',
 ['Work Song is the mice dressmaking-plan number.','Bibbidi is Fairy Godmother magic, not the mice plan.','So This Is Love is the ballroom romance.','Sing Sweet Nightingale is the washing/music-lesson sequence.'],
 'A Dream reprise does accompany later dress completion, so removed it as distractor and specified launch of the mice plan. This is song identity, distinct from #287 dress-object fact.','1950 animated Cinderella, initial mice dressmaking plan.')
review(1245,'b23-alice b23-alicemusic','Hatter and Hare sing Unbirthday at their tea party.',
 ['Unbirthday is explicitly the tea-party number.','Caucus Race belongs to the shore creatures.','Painting Roses belongs to the card gardeners.','Golden Afternoon belongs to the singing flowers.'],
 'Unbirthday is reprised at the trial too; this does not mean another listed song is sung at the tea party. Film and performers fix the event.','1951 animated Alice, Hatter/Hare tea party.')
review(1246,'b23-peter b23-petermusic','You Can Fly accompanies first flight after pixie dust.',
 ['You Can Fly accompanies the Darlings rising and flying from London.','Second Star is the opening song, not the first-flight number.','Following Leader accompanies the Lost Boys march.','Pirates Life belongs to the pirate crew.'],
 'Second Star mentions the route and plays in the film opening, but the transcript places You Can Fly at the flight lesson itself. Prior #996 asks a different song-to-film association.','1953 animated Peter Pan, Darlings first flight.')
review(1247,'b23-lady b23-ladymusic','Peg is introduced at the pound and sings Hes a Tramp.',
 ['Hes a Tramp immediately follows Peg introduction.','Bella Notte accompanies the restaurant date.','La La Lu is Darling baby lullaby.','Peace on Earth is Christmas music.'],
 'Added film/year to isolate animated Peg from live-action portrayals. Tramp in film title does not establish which of four songs Peg performs; all four are from that film.','1955 animated Lady and the Tramp, pound scene.')
review(1248,'b23-sleepmusic','Bruns adapted themes from Tchaikovsky ballet.',
 ['Tchaikovsky composed the source ballet music.','Beethoven is not the ballet composer identified for this score.','Stravinsky is not the composer credited for the source ballet.','Gershwin is not the score source named by Disney.'],
 'George Bruns arranged the film score, so is not conflated with the composer whose music it draws from. Fantasia uses other composers but is a separate film.','1959 animated Sleeping Beauty; ballet source composer.')
review(1249,'b9-jungleprofiles b9-junglelist','Disney character profiles assign Trust in Me to Kaa.',
 ['Trust in Me is Kaa hypnotic number.','I Wanna Be Like You is King Louie number.','Bare Necessities is Baloo number.','My Own Home is the girl village song, not Kaa.'],
 'Kaa also appears in other musical contexts, but the 1967 hypnotic solo is explicitly assigned in the profiles. King Louie association #460 does not identify Kaa own song.','1967 animated Jungle Book, Kaa hypnosis number.')
review(1250,'b23-aristocats b23-aristomusic','Scat Cat band plays Everybody Wants to Be a Cat at OMalley home.',
 ['Everybody Wants is the band jam.','Scales and Arpeggios is kitten practice at Madame home.','Thomas OMalley Cat is his solo introduction.','Aristocats is the opening title tune.'],
 'All numbers involve cats, so removed vague feline musicianship and specified band/location. The full song title is long naturally, not an explanation added only to the answer. Raised difficulty for a specific scene association.','1970 Aristocats, band jam at OMalley home.')
review(1251,'b23-robinmusic','Phony King is Phil Harris/Little John number mocking John at the celebration.',
 ['Phony King is Little John forest-party ridicule.','Oo De Lally is Allan a Dale introductory narration.','Love is the romantic interlude sung by Nancy Adams.','Not in Nottingham is Allan a Dale lament after the tax crackdown.'],
 'Not in Nottingham also criticizes life under John, so simple mocks rule was too broad. Final requires Little John forest celebration, distinguishing the later sorrowful narrator number.','1973 Disney animated Robin Hood, forest celebration.')
review(1252,'b23-rescuers b23-rescuemusic','The delegates sing Rescue Aid Society at the opening emergency meeting.',
 ['Rescue Aid Society is the delegates anthem.','Someone Waiting is the later Penny consolation song.','Tomorrow Another Day accompanies travel.','Journey is the opening message-bottle song.'],
 'The source describes the assembly anthem but does not require custodian Bernard to be one of the singers. Final assigns it to the delegates and avoids that unsupported participation claim. Film title overlap is necessary context, not the full anthem answer.','1977 animated Rescuers, opening delegates meeting.')
review(1253,'b23-ratigan b23-ratmusic b23-ratalbum','Ratigan henchmen praise him in Worlds Greatest Criminal Mind before Bartholomew offense.',
 ['Worlds Greatest is the lair celebration interrupted by Bartholomew.','Goodbye So Soon is the later trap recording, not this henchmen celebration.','Let Me Be Good is the tavern entertainment.','Rat Trap is not one of the three documented vocal numbers and is not the title of this praise number.'],
 'Ratigan has another vocal recording, so about himself did not uniquely locate the number. The interruption and henchmen make the scene explicit; title Great shares a root with Greatest accidentally.','1986 animated Great Mouse Detective, early lair celebration.')
review(1254,'b23-oliver b23-olivermusic b23-ritacredits','Rita sings Streets of Gold as Oliver learns street survival.',
 ['Streets of Gold is Rita lesson.','Why Should I Worry is Dodger vocal.','Good Company is Jenny vocal.','Perfect Isnt Easy is Georgette vocal.'],
 'Rita speaking voice Sheryl Lee Ralph differs from singing voice Ruth Pointer; question asks character, not performer. The four songs have distinct leads, corroborated by soundtrack assignments.','1988 animated Oliver and Company; Rita street lesson.')
review(1255,'b23-beast','Something There accompanies changing feelings in the snowy garden sequence.',
 ['Something There expresses both leads changing perceptions.','Be Our Guest is the earlier dinner presentation.','Gaston is tavern praise of Gaston.','Mob Song rallies villagers for attack.'],
 'Other romantic numbers also express closeness, but none is a listed distractor here. Specified original 1991 snowy-garden sequence; the later transcript includes Human Again restoration, which does not alter this number placement.','1991 animated Beauty and Beast, snowy garden feelings sequence.')

data.pop(1245)  # Later cross-bank search found the unbirthday-party inverse.
notes=read('audit/runs/next-shard-0023-final-active-template.json')
assert {r['questionId'] for r in notes['reviews']}==set(data)
for r in notes['reviews']:
    keys,premise,reasons,challenge,context,changing,extra=data[r['questionId']]
    r.update(checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],
        notes=extra or 'Complete topic digests and full four-option comparisons read; category, difficulty and scope checked on final wording. Distinct fact except documented retirements.',
        context=context,timeSensitive=changing,nextReviewAt='2027-02-05' if changing else None,
        premise={'reason':premise,'sources':keys})
    r['options']=[{'basis':'direct' if j==0 else 'exclusive-inference','reason':reason,'sources':keys} for j,reason in enumerate(reasons)]
    r['challenge']=dict(reviewer='Codex',at='2026-11-08',premiseChecked=True,alternativesExcluded=True,notes=challenge)
notes['sourcesChecked']=sorted({k for row in data.values() for k in row[0]})
write('audit/runs/next-shard-0023-evidence-notes.json',notes)
print('Authored',len(data),'explicit four-option reviews; ledger unchanged.')
