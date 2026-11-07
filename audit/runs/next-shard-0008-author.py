"""Codex's inspected source passages and explicit final-wording evidence notes.

Only expands authored evidence. Does not infer checks or edit question shards.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from question_audit import digest

AT = '2026-11-07'
DUE = '2027-02-05'
library = json.loads((ROOT/'audit/source-notes.json').read_text(encoding='utf-8'))

def source(key, url, locator, evidence, topic, mutable=False, limitations='Primary institutional text inspected; no film or video viewing claimed.'):
    library['sources'][key] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt=AT, timeSensitive=mutable,
        nextReviewAt=DUE if mutable else None, limitations=limitations, topics=[topic])

source('tower-hotel', 'https://disneyworld.disney.go.com/en_CA/attractions/hollywood-studios/twilight-zone-tower-of-terror/',
       'Next Stop: The 5th Dimension, opening paragraph', 'The fictional setting is the Hollywood Tower Hotel, closed after the 1939 elevator incident.', 'parks', True)
source('contemporary-tower', 'https://disneyworld.disney.go.com/resorts/contemporary-resort/',
       'What Makes This Resort Hotel Unique; Resort Monorail photo caption', 'The monorail runs through the Contemporary tower; the image caption calls the interior its main concourse.', 'parks', True)
source('carousel-theater', 'https://disneyworld.disney.go.com/en_CA/attractions/magic-kingdom/walt-disney-carousel-of-progress/',
       'From the Gramophone to the Smartphone; A Revolution-ary Theatrical Experience', 'Carousel of Progress follows household inventions across generations; audience seating revolves around the central stage. Page also notes a 2026-27 refurbishment.', 'parks', True)
source('pirates-opening', 'https://d23.com/a-to-z/pirates-of-the-caribbean/', 'Opening sentence and park-by-park dates', 'Disneyland Pirates opened March 18, 1967; Magic Kingdom followed in 1973.', 'parks')
source('pirates-opening-archive', 'https://d23.com/pirates-of-the-caribbean-ride-through-disneyland/', 'Paragraph following the December 1966 preview-film description', 'The archive distinguishes December 1966 preview footage from the public opening on March 18, 1967.', 'parks')
source('illuminations-history', 'https://d23.com/a-to-z/illuminations/', 'Original 1988 show; millennium version; final-performance sentences', 'The original IllumiNations began in 1988. Reflections of Earth debuted October 1, 1999, initially with 2000 in its title, and ended September 30, 2019, before Epcot Forever.', 'parks')
source('illuminations-debut', 'https://d23.com/illuminations-reflections-of-earth-celebrates-10-years-of-magic/', 'Paragraph about Don Dorsey developing the millennium show', 'The Reflections of Earth millennium show premiered October 1, 1999.', 'parks')
source('utilidors', 'https://d23.com/a-to-z/utilidors/', 'Complete A-to-Z entry', 'Utilidors is the coined name of the service tunnel network. Built at ground level due to the water table, it sits beneath the guest level and carries supplies and cast members.', 'parks', True)
source('monorail-record', 'https://d23.com/this-day/vice-president-nixon-dedicates-the-monorail-at-disneyland/', 'June 14, 1959 dateline and closing onboard-narration description', 'Disneyland introduced the first daily-operating monorail in the Western Hemisphere in 1959.', 'parks')
source('imagineering-1959', 'https://sites.disney.com/waltdisneyimagineering/our-story/', '1959, June timeline entry', 'The 1959 Disneyland expansion included the Western Hemisphere first daily-operating monorail, submarines and the tubular-steel Matterhorn coaster.', 'parks')
source('peoplemover-identity', 'https://disneyworld.disney.go.com/en_CA/attractions/magic-kingdom/tomorrowland-transit-authority-peoplemover/', 'Title; Move Above and Beyond; Magnet-Powered Magic', 'Tomorrowland Transit Authority PeopleMover is the elevated Tomorrowland tram powered by linear induction motors.', 'parks', True)
source('tron-2023', 'https://disneyexperiences.com/disneyworld-press/release/enter-the-grid-as-tron-lightcycle-run-presented-by-enterprise-opens-april-4-2023-at-walt-disney-world/', 'Release title and opening announcement', 'Magic Kingdom TRON Lightcycle / Run opened April 4, 2023.', 'parks')
source('matterhorn', 'https://d23.com/a-to-z/matterhorn-bobsleds/', 'Opening description; mountain and bobsled-run paragraphs', 'Matterhorn Bobsleds is the Disneyland mountain attraction, opened in 1959 with dual bobsled runs.', 'parks')
source('disney-company-origin', 'https://d23.com/disney-history/', 'Opening 1923 paragraph and 1928 Mickey paragraphs', 'Walt arrived in California in 1923; the brothers formed Disney Brothers Cartoon Studio. Steamboat Willie opened November 18, 1928, after two silent Mickey shorts.', 'walt')
source('disney-parks-lifetime', 'https://d23.com/disney-history/', 'Disneyland opening, Walt death, Florida opening, EPCOT and Tokyo chronology', 'Disneyland opened in 1955 during Walt\'s life. Walt died in 1966; the Florida resort opened in 1971, EPCOT in 1982, Tokyo Disneyland in 1983.', 'walt')
source('disney-family', 'https://d23.com/about-walt-disney/', '1923 Hollywood move; 1925 marriage and daughters; 1940 Burbank paragraphs', 'Walt moved to Hollywood, California, partnered with Roy O., married Lillian Bounds, and had daughters Diane and Sharon. The Burbank studio was completed in 1940.', 'walt')
source('iwerks-first-sketch', 'https://d23.com/walt-disney-legend/ub-iwerks/', 'Paragraph beginning Ub is credited with sketching Mickey Mouse', 'Ub Iwerks is credited with the first Mickey Mouse sketch and animated Plane Crazy.', 'walt')
source('uncle-walt', 'https://www.waltdisney.org/blog/recap-our-grandpa-walt-disney', 'Opening paragraph contrasting audiences and grandchildren', 'Many children knew Walt as Uncle Walt, while his grandchildren called him Grandpa.', 'walt')
source('epcot-city', 'https://d23.com/a-world-of-tomorrow-inside-walts-last-dream/', 'Marty Sklar account of the 24-minute Florida Project film', 'Walt\'s EPCOT concept was a functioning future city with residents living, working and playing, rather than the later theme park.', 'walt')
source('travers', 'https://d23.com/a-to-z/travers-p-l/', 'Opening author attribution', 'P. L. Travers wrote the Mary Poppins books, beginning in 1934.', 'walt')
source('pixar-acquisition', 'https://thewaltdisneycompany.com/press-releases/disney-completes-pixar-acquisition/', 'May 5, 2006 dateline and opening completed-transaction announcement', 'Disney completed the Pixar acquisition on May 5, 2006.', 'walt')
source('pixar-sec', 'https://www.sec.gov/Archives/edgar/data/1001039/000119312506103659/d8k.htm', 'Item 2.01, Completion of Acquisition or Disposition of Assets', 'The filed transaction record gives May 5, 2006 as completion of the Pixar merger.', 'walt')
source('flowers-three-strip', 'https://www.waltdisney.org/blog/flowers-and-trees-first-color-movie', 'Adding Color Proves to Be Much More Difficult Than Anticipated', 'Flowers and Trees was remade in three-strip Technicolor during 1932 and identified as the first film in that process.', 'walt')
source('flowers-firsts', 'https://d23.com/90th-anniversary-disney-firsts/', 'Flowers and Trees image caption', 'Disney identifies Flowers and Trees as its first use of three-strip Technicolor in cartoons.', 'walt')
source('museum-address', 'https://www.waltdisney.org/visit', 'Location and Hours; Transportation', 'The Walt Disney Family Museum is at 104 Montgomery Street in the Presidio of San Francisco, California.', 'walt', True)
source('roy-death', 'https://d23.com/a-to-z/disney-roy-oliver/', 'Birth/death line and final Walt Disney World paragraph', 'Roy O. Disney died December 20, 1971, after attending the Florida resort\'s October opening.', 'walt')
source('wed-initials', 'https://d23.com/this-day/walt-disney-founds-wed-enterprises/', 'December 16, 1952 entry; WED name explanation', 'WED derives from Walter Elias Disney\'s initials; the design company later became Walt Disney Imagineering.', 'walt')
source('treasure-first', 'https://d23.com/a-to-z/treasure-island-film/', 'Release date and first-live-action sentences', 'Treasure Island was released July 19, 1950, as Disney\'s first live-action film without animation.', 'walt')
source('treasure-corroboration', 'https://d23.com/a-to-z/live-action/', 'Complete entry contrasting earlier animation/live-action hybrids', 'The earlier hybrid films are distinguished from Treasure Island (1950), Disney\'s first completely live-action film.', 'walt')
source('snow-reference', 'https://www.waltdisney.org/sites/default/files/SW.worksheets.final.pdf', 'Animation worksheet, item 1, Snow White Dancing, Jack Campbell', 'Marjorie Belcher\'s Snow White reference movements were filmed, traced and used to guide animators. This does not mean the entire finished performance was mechanically copied.', 'Snow White')
source('rotoscope-definition', 'https://d23.com/still-the-fairest-and-most-inspiring-of-all/', 'Mark Henn paragraph distinguishing tracing from creative reference use', 'The animator defines rotoscoping as tracing live action exactly and distinguishes it from creatively adapting reference.', 'Snow White')
source('oswald-rights', 'https://d23.com/a-to-z/oswald-the-lucky-rabbit/', 'First two paragraphs, Universal copyright and 2006 rights return', 'Universal was the copyright holder, while Charles Mintz contracted for distribution; Disney recovered the rights from Universal in 2006.', 'walt')
source('oswald-restoration', 'https://d23.com/the-art-of-restoring-27-classic-walt-disney-animation-studios-shorts/', 'Restoration interview, answer on the Oswald shorts', 'The studio restorer identifies Universal as the prior rights owner.', 'walt')
source('treasure-fleet-six', 'https://investors.thewaltdisneycompany.com/files/doc_events/2025/02/q1-fy25-executive-commentary.pdf', 'Experiences section, Disney Treasure launch sentence', 'The completed quarter\'s launch of Disney Treasure is described as the fleet\'s sixth ship.', 'cruise')
source('fleet-2025-table', 'https://disneyexperiences.com/app/uploads/2025/03/FY25-Q3-DCL-Disney-Experiences-Fact-Sheet.pdf', 'Disney Cruise Line Fleet table', 'The six listed ships are Magic (1998), Wonder (1999), Dream (2011), Fantasy (2012), Wish (2022) and Treasure (maiden voyage December 21, 2024).', 'cruise')
source('wish-nursery', 'https://disneycruise.disney.go.com/en-sg/onboard-activities/its-a-small-world-childrens-nursery/', 'Title; Ship Locations; Designed to Delight', 'The childcare venue on Disney Wish is it\'s a small world nursery, catering to babies and toddlers.', 'cruise', True)
source('dream-spa', 'https://disneycruise.disney.go.com/en-au/onboard-activities/senses-spa-salon/', 'Title; Ship Locations; A Blissful Retreat for the Senses', 'Senses Spa & Salon is named as the spa, and Disney Dream is explicitly among its ship locations.', 'cruise', True)
source('wish-dining-guide', 'https://cdn1.parksmedia.wdprapps.disney.com/media/blog/wp-content/uploads/2023/03/Wish_Pocket_Guide.pdf', 'Food & Beverage: Main/Rotational Dining', 'Wish has three rotational restaurants: 1923, Arendelle and Worlds of Marvel. The party and serving team move together between restaurants.', 'cruise', True)
source('aquamouse', 'https://disneycruise.disney.go.com/en-ph/onboard-activities/aquamouse-water-slide/', 'Title; Ship Locations; H2Go', 'AquaMouse is the Mickey-themed water attraction aboard Wish, Treasure and Destiny.', 'cruise', True)
source('water-coasters', 'https://disneycruise.disney.go.com/en-ph/why-cruise-disney/families/pools-waterslides-coasters/', 'Water coaster description; Disney Movies Poolside', 'Wish uses AquaMouse. Disney calls the poolside movie screen Funnel Vision.', 'cruise', True)
source('dining-team', 'https://www.disneyholidays.co.uk/disney-cruise-line/help/frequently-asked-questions/dining/', 'What is Rotational Dining?', 'Guests rotate among main dining rooms with the same wait staff rather than changing serving teams nightly.', 'cruise', True)
source('worlds-marvel', 'https://disneycruise.disney.go.com/en-ca/onboard-activities/worlds-of-marvel/', 'Title; Ship Locations; Rotational Dining', 'Worlds of Marvel is the Marvel-themed main dining venue aboard Disney Wish.', 'cruise', True)
source('wish-edge', 'https://disneycruise.disney.go.com/en-gb/onboard-activities/edge-youth-club/', 'On the Disney Wish, Disney Treasure & Disney Destiny', 'Edge is advertised for ages 11 through 14 aboard Wish.', 'cruise', True)
source('wish-vibe', 'https://disneycruise.disney.go.com/en-ca/onboard-activities/vibe-teen-club/', 'On the Disney Wish, Disney Treasure & Disney Destiny', 'Vibe is advertised for ages 14 through 17 aboard Wish.', 'cruise', True)
source('youth-both', 'https://disneycruise.disney.go.com/en-eu/faq/kids-teens/teen-tween-activities/', 'Answer, separate tween and teen lounges', 'The official FAQ explicitly contrasts Edge for ages 11-14 and Vibe for ages 14-17.', 'cruise', True)
source('true-life', 'https://d23.com/a-to-z/true-life-adventures-film/', 'Opening description and complete list of original films', 'True-Life Adventures was a theatrical nature-film series of shorts and features from 1948-1960; The Living Desert was among its features.', 'walt')
source('nine-old-men', 'https://d23.com/a-to-z/nine-old-men/', 'Complete entry', 'Nine Old Men was Walt\'s name for his key animators, including Thomas, Johnston and Davis.', 'walt')
source('multiplane', 'https://www.waltdisney.org/multiplane-classroom-kit', 'Opening technology description', 'The multiplane camera photographs layers of artwork to give depth to two-dimensional animation.', 'walt')
source('laughogram', 'https://d23.com/a-to-z/laugh-o-gram-films/', 'Complete entry', 'Laugh-O-gram Films was Walt\'s Kansas City company making fairy-tale shorts in 1922, before the California studio.', 'walt')
source('medal-president', 'https://www.presidency.ucsb.edu/documents/remarks-the-presentation-the-1964-presidential-medal-freedom-awards', 'September 14, 1964 transcript; Walter Disney recipient announcement', 'President Lyndon B. Johnson presented Walt Disney\'s Medal of Freedom in 1964.', 'walt')
source('cruise-originals', 'https://d23.com/a-to-z/disney-cruise-line/', 'Opening ship chronology', 'The first DCL ships were Magic in July 1998 and Wonder in August 1999; Dream and Fantasy followed in 2011 and 2012.', 'cruise')
source('cruise-theatre', 'https://disneycruise.disney.go.com/en-as/onboard-activities/walt-disney-theater/', 'Title; Broadway-Style Entertainment', 'Walt Disney Theatre is the onboard live-show venue, including on Disney Wonder.', 'cruise', True)
source('pirate-night', 'https://disneycruise.disney.go.com/en-gb/onboard-activities/pirate-night-deck-party/', 'Title; Party Like a Pirate; fireworks image captions', 'Pirate Night is the costume-and-deck-party event on select itineraries with fireworks imagery; it is not guaranteed on every sailing.', 'cruise', True)

# Each row records a performed review: sources, context, premise, four reasons,
# and a separate literal-wording challenge. No rationale is generated from a key.
rows = {}
def review(qid, sources, context, premise, reasons, challenge, notes='', bases=None):
    rows[qid] = (sources.split(), context, premise, reasons, challenge, notes, bases)

review(367, 'tower-hotel', 'Hollywood Studios version of The Twilight Zone Tower of Terror.',
 'The attraction page explicitly locates its story inside a named hotel.',
 ['The setting is named Hollywood Tower Hotel.', 'The Sunset Hotel is not the hotel named for this setting.', 'The Hollywood Haunt is not the named fictional property.', 'Tower Inn is not this property\'s name.'],
 'Tokyo uses a different Tower story; the explicit Florida park prevents that objection. The three other labels cannot name the hotel identified by the page.',
 'Distinct hotel-setting fact, unlike 609\'s attraction identity and 1160\'s California replacement history.')
review(368, 'contemporary-tower', 'Main tower atrium at Walt Disney World; not the ground-floor check-in lobby.',
 'The hotel\'s own page describes the monorail passing through its tower.',
 ['The Contemporary tower contains the monorail concourse.', 'Grand Floridian is not the named tower through which the train passes.', 'Polynesian has monorail service, but is not the identified indoor tower route.', 'BoardWalk Inn is not the hotel housing that route.'],
 'Having a monorail stop does not satisfy passing through the tower. Atrium/concourse wording removes the lobby-floor error; all options are hotel names.',
 '626 tests the three served hotels, not which building contains the track.')
review(369, 'carousel-theater', 'Magic Kingdom household-technology show, regardless of temporary refurbishment.',
 'The official description combines American family technology with a revolving auditorium.',
 ['Carousel of Progress has precisely that technology narrative and revolving seating.', 'Hall of Presidents is not the named family-technology show.', 'American Adventure is not the Magic Kingdom attraction identified here.', 'Hall of Technology is not the attraction named by the official description.'],
 'Presidential or general national history is broader than household inventions; neither creates a second match for the conjunction of location, format and subject.',
 'Distinct from 955\'s World\'s Fair sponsor and 2218\'s song. Medium suits recognition of this signature show.')
review(370, 'pirates-opening pirates-opening-archive', 'Original Disneyland attraction opening, not Florida or pre-opening footage.',
 'Two archive accounts explicitly date the public opening to March 18, 1967.',
 ['1967 is the stated Disneyland opening year.', '1965 is not the stated opening year.', '1970 is not the stated opening year.', '1973 belongs to the Florida version, not Disneyland.'],
 'A December 1966 filmed preview is not a public opening; 1973 is a real but different park date. The specified park leaves exactly 1967.',
 'Date is independent of 621\'s boat-ride identity.')
review(371, 'illuminations-history illuminations-debut', '1999 millennium version through its 2019 final performance.',
 'The timeline identifies the Reflections of Earth version and both endpoints.',
 ['Reflections of Earth is the millennium version ending in September 2019.', 'SpectroMagic is not the title of the documented EPCOT show.', 'Harmonious is not the show the archive identifies for this 1999-2019 run.', 'Epcot Forever followed the final performance, rather than occupying this run.'],
 'Earlier EPCOT lagoon shows invalidate original, so that word is removed. The initial 2000 branding is the same Reflections of Earth version, not another answer.',
 'Corrects a false first-show implication; 551 asks the later anniversary show.')
review(374, 'utilidors', 'Coined Disney name for the service network below the guest level.',
 'The A-to-Z entry explicitly names the tunnels Utilidors and explains the ground-level construction.',
 ['Utilidors is the documented coined name.', 'Castways is not the coined name given in the entry.', 'Magicways is not that network\'s documented name.', 'Underways is not that network\'s documented name.'],
 'Ordinary descriptions such as tunnels and service corridors could also fit the original question; final options are competing coined names. Below guest areas avoids implying excavation below Florida ground level.',
 'Distinct service-network terminology; hard recall is reasonable.')
review(376, 'monorail-record imagineering-1959', 'Historical 1959 monorail record in the Western Hemisphere.',
 'Disney archive narration and Imagineering\'s timeline agree on the Disneyland system and record.',
 ['Disneyland Monorail is the system credited with the record.', 'The Walt Disney World system is a distinct later system, not the Disneyland record holder.', 'Tokyo\'s Resort Line is a distinct system and outside the Western Hemisphere.', 'Seattle Center Monorail is a distinct system, not the credited Disneyland installation.'],
 'All four options now name monorails, so the transport-type word reveals no answer. The precise first daily-operating qualifier does not claim the first monorail invention worldwide.',
 'Historical record corroborated. Different from 2647\'s vehicle designer.')
review(380, 'disney-company-origin', 'Steamboat Willie\'s original synchronized-sound release.',
 'The archive gives the November 18, 1928 opening after two silent Mickey films.',
 ['1928 is the release year.', '1925 predates the stated release.', '1930 follows the stated release.', '1932 follows the stated release.'],
 'First produced and first released Mickey cartoons are different; the named sound cartoon is specifically dated. No other listed year is its original release.',
 '678 tests the short\'s identity, not its year; 930 and 931 test production order.')
review(381, 'disney-parks-lifetime', 'A park whose opening Walt witnessed, rather than a project he only planned.',
 'The chronology puts Disneyland before Walt\'s death and all three alternatives after it.',
 ['Disneyland opened in 1955 during Walt\'s life.', 'Magic Kingdom opened in the Florida resort in 1971, after 1966.', 'EPCOT opened in 1982, after Walt\'s death.', 'Tokyo Disneyland opened in 1983, after Walt\'s death.'],
 'Walt helped plan Florida but could not see its park open. His city concept called EPCOT is not the theme park in these options.',
 'Theme park options are now parallel. 1374 concerns the same-named television program, not this lifetime milestone.')
review(383, 'iwerks-first-sketch', 'Attribution of the first Mickey sketch, not every later animator of Mickey.',
 'The Ub Iwerks biography explicitly assigns the first sketch to him.',
 ['Ub Iwerks receives the first-sketch attribution.', 'Ward Kimball is not the person credited with that first sketch.', 'Ted Sears is not the person credited with that first sketch.', 'Les Clark is not the credited first sketcher, despite his early Mickey animation work.'],
 'Later creative contributions would make helped design broad. Final wording asks the singular first-sketch credit, so Les Clark\'s animation does not compete.',
 'No duplicate first-sketch attribution found in topic or cross-bank search.')
review(387, 'uncle-walt', 'Public affectionate nickname, not every form of address used by staff or relatives.',
 'The grandchildren-event account explicitly contrasts the audience\'s Uncle Walt with the family\'s Grandpa.',
 ['Uncle Walt is the documented public nickname.', 'Papa Walt is not the public nickname identified in the account.', 'Cousin Walt is not the nickname identified there.', 'Brother Walt is not the nickname identified there.'],
 'Mr. Disney was genuinely used by staff, so it is removed rather than claimed false. All final choices are comparable family-style nicknames; the account singles out Uncle.',
 'Personality/history within walt scope, not a TV episode or show-title question.')
review(392, 'epcot-city', 'Walt\'s planned EPCOT community in the 1966 Florida Project film.',
 'Sklar\'s account explicitly describes the proposed city and its residents.',
 ['A living, working experimental city is the original concept.', 'A world-cultures theme park describes a different later implementation.', 'A wildlife preserve does not describe the proposed city.', 'A production campus is not the proposed residential community.'],
 'The city included shopping and industry, but those components do not convert the whole EPCOT proposal into a film campus, preserve or later theme park.',
 'Distinct from 101\'s acronym and 1193\'s final filmed topic; options made comparable in length.')
review(393, 'travers', 'Authorship of the original Mary Poppins books, rather than screenplay or songs.',
 'The author entry explicitly attributes the books to P. L. Travers.',
 ['P. L. Travers is the named author.', 'J. M. Barrie is not the author to whom these books are attributed.', 'A. A. Milne is not their attributed author.', 'Lewis Carroll is not their attributed author.'],
 'Film adaptation collaborators do not share the authorship asked here. All four are author names and the original books have the explicit single attribution.',
 '135 asks cast and mixed media; 1206 asks songwriters. Neither repeats book authorship.')
review(394, 'pixar-acquisition pixar-sec', 'Completed acquisition of Pixar, not an earlier production agreement.',
 'The corporate completion announcement and SEC Item 2.01 both give May 5, 2006.',
 ['2006 is the completed merger year.', '2003 is not the merger year stated in the transaction record.', '2009 is not the Pixar completion year.', '2012 is not the Pixar completion year.'],
 'Pixar\'s preexisting Disney distribution relationship is not the acquisition; both transaction records specify completion. Other corporate acquisition dates cannot change Pixar\'s date.',
 'Different 2006 event from 357; no other Pixar acquisition question found.')
review(396, 'flowers-three-strip flowers-firsts', 'Disney\'s first use of three-strip Technicolor in an animated short.',
 'The museum production account and Disney\'s firsts list independently name Flowers and Trees.',
 ['Flowers and Trees is explicitly credited as the first.', 'Steamboat Willie is not the short assigned this color-process first.', 'The Skeleton Dance is not the short assigned that first.', 'Three Little Pigs followed Flowers and Trees and cannot hold its first-use credit.'],
 'Earlier partial color processes are excluded by three-strip. Later color shorts and sound milestones do not satisfy first use of this process.',
 'Removed the Oscar clue and answer dates. 1197 asks first competitive Oscar and 1196 category; the retained fact is the separate color-process innovation.')
review(397, 'museum-address', 'The Walt Disney Family Museum, rather than every museum devoted to Walt.',
 'Its own visit page places the named institution in San Francisco.',
 ['San Francisco is the city in the address.', 'Los Angeles is a different city from the museum\'s address.', 'Anaheim is a different city from the museum\'s address.', 'Marceline is a different city; another Walt museum would not be this named institution.'],
 'The singular proper museum name prevents confusion with the hometown museum. All final options have only city and state; the Presidio parenthetical no longer clues the key.',
 'Distinct museum-location fact; the named institution may change location so schedule recheck.')
review(398, 'roy-death', 'Roy O. Disney\'s death after the Florida resort opening.',
 'The archive explicitly gives December 20, 1971.',
 ['1971 is the stated year of Roy\'s death.', '1973 is not the year of the stated death date.', '1969 is not the year of the stated death date.', '1975 is not the year of the stated death date.'],
 'Roy O. is not Roy E.; the dated biography also confirms the October opening followed by death two months later. Only one listed year matches.',
 'Different event from 354\'s Haunted Mansion opening and 1490\'s family leadership.')
review(402, 'wed-initials', 'The personal initials used in WED Enterprises.',
 'The founding entry explicitly expands WED to Walter Elias Disney.',
 ['Walter Elias Disney is the documented expansion.', 'Walt\'s Entertainment Division is not the documented expansion.', 'World Entertainment Design is not the documented expansion.', 'Walt\'s Engineering Department is not the documented expansion.'],
 'An engineering organization might plausibly sound like the fourth phrase, but the recorded name origin is personal initials, not a department acronym.',
 '668 asks Walt\'s middle name, 1191 the company\'s later name, and 2357 the founding year; this tests WED etymology.')
review(404, 'treasure-first treasure-corroboration', 'Disney\'s first feature entirely in live action, excluding hybrids.',
 'Both archive entries distinguish Treasure Island (1950) from earlier films containing animation.',
 ['Treasure Island is explicitly identified as the first wholly live-action Disney film.', '20,000 Leagues Under the Sea is not the film credited with that first.', 'Davy Crockett is not the film credited with that first.', 'The Swiss Family Robinson is not the film credited with that first.'],
 'The Reluctant Dragon and Song of the South cannot defeat the premise because they contain animation and are outside the listed alternatives. All-live-action is the required distinction.',
 '521 asks the literary source of Treasure Planet; 2407 asks an island\'s historical name. Neither asks the production milestone.')
review(405, 'snow-reference rotoscope-definition', 'Tracing as a movement aid in the 1937 Snow White production; not all use of reference.',
 'The museum confirms filmed, traced reference; the animator\'s definition names tracing rotoscoping.',
 ['Rotoscoping names frame tracing of filmed live action.', 'Multiplane photography concerns layers and depth, not this tracing operation.', 'Motion capture records movement data rather than hand tracing filmed frames.', 'Stop-motion animation photographs incrementally posed physical objects, not traced live-action frames.'],
 'Live reference animation could encompass this and was removed. Tracing as an aid does not claim every finished Snow White frame was a literal copy; the two sources distinguish the techniques.',
 'Snow White production context keeps the Disney scope. Distinct from 685\'s multiplane debut and 2578\'s CAPS workflow.',
 ['direct','contradiction','exclusive-inference','exclusive-inference'])
review(408, 'oswald-rights oswald-restoration', 'Rights ownership at the 1928 loss of control, distinct from distribution contracts.',
 'The archive identifies Universal as copyright holder; a studio restoration interview corroborates ownership.',
 ['Universal Pictures held the rights.', 'MGM is not the rights holder identified for this event.', 'Paramount is not the rights holder identified for this event.', 'RKO is not the rights holder identified for this event.'],
 'Charles Mintz negotiated distribution but is not the studio owner asked here. The dated stem excludes Disney\'s later recovery of the character.',
 '375 asks the producer involved; 2422 asks the new character, not the rights-owning studio.')
review(412, 'treasure-fleet-six fleet-2025-table', 'Historical fleet count including Treasure at its December 2024 maiden voyage.',
 'Post-launch investor commentary calls Treasure sixth; the fleet table lists the six ships and maiden-voyage date.',
 ['Six includes Magic, Wonder, Dream, Fantasy, Wish and Treasure.', 'Four would omit two ships in the listed fleet.', 'Five was the prior fleet count and omits Treasure itself.', 'Seven exceeds the six ships at this historical cutoff.'],
 'The player report correctly distinguishes before from including Treasure. Final wording explicitly includes it and uses the maiden voyage cutoff; later ships cannot change this historical total.',
 'Reviewed the actual 412 player report. It was already marked resolved in production; no flag writes made. Other Six answers concern coaster music and vehicle seats.')
review(413, 'wish-nursery', 'Disney Wish childcare venue for babies and toddlers.',
 'The venue title and ship-location list establish the Wish nursery\'s proper name.',
 ['It\'s a Small World Nursery is the documented name, with punctuation normalized.', 'Mickey\'s Nursery is not the named Wish nursery.', 'Disney Baby Care is not that venue\'s proper name.', 'Pixie Dust Nursery is not that venue\'s proper name.'],
 'Other play areas for toddlers are not the nursery. The specified ship prevents reliance on a changing fleet-wide generalization.',
 'No other nursery-name fact found in the cruise digest.')
review(414, 'dream-spa', 'Named spa aboard Disney Dream.',
 'The official spa title explicitly lists Disney Dream among its ships.',
 ['Senses Spa & Salon is the named Dream spa.', 'Disney Retreat Spa is not that venue\'s name.', 'Magic Wellness is not that venue\'s name.', 'Relaxation Station is not that venue\'s name.'],
 'The final stem removes salon, which appeared only in the key. The ship list establishes Dream; no claim about a single uniform spa on every ship is required.',
 'No duplicate Dream spa-name question in the digest.')
review(415, 'wish-dining-guide', 'Disney Wish main rotational dinner schedule, not every place serving food.',
 'The official pocket guide explicitly lists three rotational restaurants.',
 ['Three is the exhaustive count: 1923, Arendelle and Worlds of Marvel.', 'Two omits one of the three main venues.', 'Four adds a venue beyond the three listed.', 'Five adds two venues beyond the three listed.'],
 'Quick service and adult specialty restaurants are outside main rotational dining. A longer sailing can repeat rooms without increasing the number of distinct restaurants.',
 '420 asks the team policy. 2551 counts songs and 5 counts films; same number is not a duplicate.',
 ['exhaustive-list']*4)
review(418, 'aquamouse water-coasters', 'Disney Wish water coaster identity.',
 'The ship list and water-coaster overview identify AquaMouse aboard Wish.',
 ['AquaMouse is the named Wish water coaster.', 'AquaDuck is not the name assigned to Wish\'s coaster.', 'WaterShip is not the documented attraction name.', 'Hydro Dash is not the documented attraction name.'],
 'The similar AquaDuck name is a plausible competitor but does not identify the Wish installation. Exact ship context makes the identity unique.',
 '733 tests Dream/Fantasy AquaDuck; 2348 asks an AquaMouse storyline company, not its ship/ride association.')
review(420, 'dining-team wish-dining-guide', 'Main rotational dining serving-team arrangement.',
 'The official FAQ and guide state that guests keep the same serving team between restaurants.',
 ['The same serving team moves with guests.', 'Nightly replacement contradicts the same-team policy.', 'Changing teams with rooms contradicts the team moving with guests.', 'A nightly lottery contradicts keeping the assigned team.'],
 'The question asks the designed assignment policy, not whether sickness could cause an exceptional staff substitution. All options now answer the same team-assignment question.',
 '415\'s restaurant count is a separate feature; the earlier general rotational-dining question is already retired.',
 ['direct','contradiction','contradiction','contradiction'])
review(423, 'worlds-marvel', 'Disney Wish Marvel-themed main dining experience.',
 'The official Worlds of Marvel page explicitly lists Wish and describes its Marvel dining.',
 ['Worlds of Marvel is the venue\'s proper name.', 'Avengers Dining is not the venue title.', 'Marvel Bistro is not the venue title.', 'Stark Industries Kitchen is not the venue title.'],
 'Avengers: Quantum Encounter is a show within the venue, not an option called Avengers Dining. A shared franchise word does not validate a different invented restaurant title.',
 '737 asks the separate Frozen-themed restaurant; knowing its title does not supply this one.')
review(424, 'wish-edge wish-vibe youth-both', 'Official advertised full age range for the Wish club.',
 'Both club pages and the FAQ distinguish Edge 11-14 from Vibe 14-17.',
 ['Edge covers the full 11-through-14 range.', 'Vibe covers 14-17 and does not cover 11-13.', 'The Loft is not the named Wish club for this range.', 'Club Tween is not the named Wish club for this range.'],
 'A 14-year-old can fit either age policy, but the literal full 11-14 range excludes Vibe. Open-house exceptions do not redefine the advertised age band.',
 '425 tests the other club and age band; either fact alone leaves the other club name unknown.')
review(425, 'wish-vibe wish-edge youth-both', 'Official advertised full age range for the Wish teen club.',
 'Both club pages and the FAQ distinguish Vibe 14-17 from Edge 11-14.',
 ['Vibe covers the full 14-through-17 range.', 'Edge stops at 14 and does not cover 15-17.', 'The Loft is not the named Wish club for this range.', 'Club Teen is not the named Wish club for this range.'],
 'The shared endpoint 14 is not enough: full 14-17 excludes Edge. The Hideaway\'s older group is a different space and is not a listed answer.',
 'Different named club from 424; age policies are mutable and scheduled for recheck.')

bank = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
notes = dict(schema=1, reviewer='Codex', at=AT, sourcesChecked=sorted({s for row in rows.values() for s in row[0]}), reviews=[])
checks = ['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
for qid, (refs, context, premise, reasons, challenge, extra, bases) in rows.items():
    q = bank[qid]
    assert len(reasons) == 4
    mutable = any(library['sources'][s]['timeSensitive'] for s in refs)
    bases = bases or ['direct','exclusive-inference','exclusive-inference','exclusive-inference']
    notes['reviews'].append(dict(questionId=qid, hash=digest(q), checks=checks,
        notes=extra+' Full matching digests and cross-bank comparisons inspected; final literal-wording challenge performed by Codex.',
        context=context, timeSensitive=mutable, nextReviewAt=DUE if mutable else None,
        premise=dict(reason=premise, sources=refs),
        options=[dict(basis=b, reason=r, sources=refs) for b,r in zip(bases,reasons)],
        challenge=dict(reviewer='Codex', at=AT, premiseChecked=True, alternativesExcluded=True, notes=challenge)))
(ROOT/'audit/source-notes.json').write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'audit/runs/next-shard-0008-evidence-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Saved {len(rows)} explicitly authored reviews and {len(library["sources"])} source passages.')
