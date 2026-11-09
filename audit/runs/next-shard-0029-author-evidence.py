"""Expand the explicitly researched batch-29 evidence; never edits question shards."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads((BASE / p).read_text(encoding='utf-8'))
def write(p, value):
    (BASE / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

library = read('audit/source-notes.json')
sources = library['sources']
used = set()
def src(key, url, locator, evidence, limitation='Institutional text inspected; no film, audio or video playback claimed.'):
    sid = 'b29-' + key
    sources[sid] = dict(url=url, locator=locator, evidence=evidence, checkedBy='Codex', checkedAt='2026-11-08', timeSensitive=False, nextReviewAt=None, topics=['Batch 29', key], limitations=limitation)
    return sid

secondary = 'Secondary text account, not original film viewing. Specific dialogue/plot passages and separate corroboration are identified in the review. No film/audio/video playback claimed.'
src('chicken','https://en.wikipedia.org/wiki/Chicken_Little_(2005_film)','Plot opening and Voice cast, lines 228, 237–245','Foxy Loxy is the mean school fox; Runt, Abby and Fish are Chicken Little’s outcast friends. Goosey is Foxy’s henchwoman.',secondary)
src('chicken-version','https://movies.disney.com/chicken-little','Release and synopsis, lines 52–66','The 2005 animated feature follows Chicken Little and his band of misfit friends against an alien invasion.')
src('cows','https://d23.com/a-to-z/home-on-the-range-film/','Opening synopsis and named voice roles','The three determined cows are Mrs. Caloway, Maggie and Grace; they seek Alameda Slim’s reward to save their farm. Pearl owns the farm.')
src('raya','https://www.disneyanimation.com/kumandra/','Meet Namaari','Namaari is Raya’s nemesis and daughter of the chief of Fang.')
src('raya-roles','https://www.disney.com.au/news/disney-plus-raya-and-the-last-dragon-cast','Sisu, Namaari, Virana, Boun and Little Noi sections','Sisu is a dragon; Namaari is the warrior daughter of Fang chief Virana; Boun is a boy from Tail; Noi a toddler from Talon.')
src('show','https://media.disneyanimation.com/technology/publications/2020/siggraph_2020_showYourself.pdf','Section 1 Introduction, lines 34–36','Elsa sings Show Yourself in Ahtohallan as the spirits guide her to answers about her purpose.')
src('frozen-scenes','https://www.springfieldspringfield.co.uk/movie_script.php?movie=frozen-ii','Opening lullaby and family song; voice summons; Kristoff solo 875–922; Ahtohallan 1073–1121; Olaf farewell and Anna song 1202–1276','The sequence puts Show Yourself at Ahtohallan; Kristoff’s Lost in the Woods after Anna leaves; Anna’s The Next Right Thing after Olaf’s fading farewell. Some Things Never Change is earlier, When I Am Older is Olaf’s forest number.',secondary)
src('frozen-music','https://news.disney.com/frozen-2-music','Song discussion after introduction','Disney identifies Lost in the Woods as Jonathan Groff/Kristoff’s number, distinct from the shorter Reindeer(s) Are Better Than People song.')
src('frozen-rock','https://press.disneyplus.com/disney-plus/into-the-unknown/102','Episode synopsis','The songwriters propose an 80s rock ballad for Kristoff, Lost in the Woods.')
src('frozen-chorus','https://news.disney.com/frozen-2-docuseries-disneyplus','Recording highlights','Jonathan Groff records reindeer harmonies for Lost in the Woods; Kristen Bell discusses The Next Right Thing.')
src('anna-song','https://en.wikipedia.org/wiki/The_Next_Right_Thing','Synopsis, lines 130–134','Anna sings after apparently losing Elsa and Olaf, then determines to continue despite grief.',secondary)
src('wish-songs','https://lumiere-a.akamaihd.net/v1/documents/1121_wish_production_notes_updated_final_11-20-23_8157ebfd.pdf','Music sections Welcome to Rosas, At All Costs (1150–1173), This Is the Thanks I Get?! (1199–1219), Knowing What I Know Now (following)','Welcome to Rosas introduces the kingdom; At All Costs is Asha and Magnifico’s wish-observatory duet; This Is the Thanks I Get?! is Magnifico’s threatened, underappreciated villain number; Knowing What I Know Now is the uprising song.')
src('pooh-nightmare','https://d23.com/a-to-z/heffalumps-and-woozles/','A to Z entry','Heffalumps and Woozles are Pooh’s nightmare characters in Winnie the Pooh and the Blustery Day.')
src('pooh-song','https://en.wikipedia.org/wiki/Heffalump','Film appearances, nightmare musical sequence','Heffalumps and Woozles appear together during Pooh’s nightmare in the song of that name.',secondary)
src('pooh-album','https://disney.go.com/disneyrecords/song-albums/bestofpooh//','Walt Disney Records track list','The official Pooh album lists Heffalumps and Woozles as a separate song alongside Pooh and Tigger songs.')
src('robinsons','https://go-60de6c82-be11-98e1-4d6c-c65a234eee95.disney.io/disneyvideos/animatedfilms/meettherobinsons/text_only/index.html','Music Videos under bonus features','Disney credits Little Wonders to Rob Thomas and Kids of the Future to Jonas Brothers.')
src('robinsons-track','https://en.wikipedia.org/wiki/Meet_the_Robinsons','Soundtrack track listing','Little Wonders is the soundtrack’s Rob Thomas track, not any of the three alternative proposed titles.',secondary)
src('merlin','https://d23.com/this-day/the-sword-in-the-stone-is-released/','Sherman Brothers song discussion','Higitus Figitus is Merlin’s carpetbag packing magic song; A Most Befuddling Thing and That’s What Makes the World Go Round are separately named songs.')
src('eisner','https://d23.com/a-to-z/eisner-michael-d/','Executive tenure opening and retirement paragraph','Eisner became CEO in September 1984 and retired in 2005; Frank Wells was a separate executive whose death preceded Eisner also taking the presidency.')
src('eisner-cor','https://www.hbs.edu/leadership/20th-century-leaders/details?profile=michael_d_eisner','Walt Disney Company 1984–2005 and profile','Harvard’s business leadership profile assigns Eisner the 1984–2005 Disney tenure and notes his animated hits.')
src('marvel','https://thewaltdisneycompany.com/press-releases/disney-completes-marvel-acquisition/','Dated opening paragraph','The completed Marvel acquisition is dated December 31, 2009.')
src('marvel-cor','https://d23.com/a-to-z/marvel-entertainment/','Acquisition dates','Marvel’s agreement and completion both occurred in 2009, completion December 31.')
src('lucas','https://d23.com/a-to-z/lucasfilm/','Opening acquisition paragraph','The Lucasfilm acquisition was announced October 30, 2012 and completed December 21, 2012, including Star Wars rights.')
src('lucas-cor','https://thewaltdisneycompany.com/news/disney-acquire-lucasfilm/','October 30, 2012 announcement','Disney announced Lucasfilm and Star Wars rights acquisition in 2012.')
src('stars','https://walkoffame.com/walt-disney/','Star Facts: two categories and addresses','Two stars list the same February 8, 1960 ceremony: motion pictures at 7021 Hollywood Boulevard and television at 6747.')
src('stars-cor','https://d23.com/a-to-z/hollywood-walk-fame/','Walt Disney entry','Disney lists Walt’s motion pictures and television honors in 1960.')
src('nbc','https://disney.go.com/disneyvideos/moviefinder/html/memorylane/ml61_main.html','1961 timeline entry','Disney’s color program debuts in 1961, moving from ABC to NBC.')
src('nbc-cor','https://d23.com/a-to-z/television/','Chronological program/network list','The color anthology is assigned NBC beginning September 24, 1961.')
src('iger','https://disney.go.com/disneyvideos/moviefinder/html/memorylane/ml2005_main.html','2005 timeline entry','Eisner retires after 21 years; Robert Iger becomes CEO in October 2005.')
src('iger-deals','https://thewaltdisneycompany.com/leadership/robert-a-iger/','Historical acquisitions in biography','Iger oversaw Pixar in 2006, Marvel in 2009 and Lucasfilm in 2012. The historical claims are used without assuming his present office.')
src('destiny-theme','https://disneyparksblog.com/dcl/discover-the-disney-destiny-three-days-of-heroic-and-villainous-reveals/','Introduction, Living a Legend – Wakanda Forever; 2025 inaugural-season paragraph','Disney Destiny’s overall theme is heroes and villains; its Grand Hall takes inspiration from Black Panther and Wakanda, with T’Challa’s statue. Its inaugural season begins November 2025.')
src('destiny-suites','https://disneyparksblog.com/dcl/disney-destiny-hero-worthy-staterooms-suites/','November 10, 2025; Tony Stark-Approved Accommodations','The Destiny Tower Suite honors Iron Man and Tony Stark’s industrial designs; Hercules and Incredibles themes belong to other suite classes.')
src('destiny-dining','https://disneycruise.disney.go.com/en-as/ships/destiny/','On the Savanna, lines 68–77','Pride Lands: Feast of The Lion King is the named musical dining experience celebrating Simba’s journey.')
src('destiny-show','https://disneycruise.disney.go.com/en-as/ships/destiny/','Entertainment: Disney Hercules, line 147','Disney Hercules is exclusive to Disney Destiny and retells the animated film with the Muses, pop/gospel influences and stage effects.')
src('lng','https://disneyexperiences.com/app/uploads/2024/05/fact_sheet_disney_cruise_line_2024_Q2.pdf','New Developments opening','Wish, Treasure and Destiny are identified as the three ships powered by liquefied natural gas.')
src('lng-cor','https://disneyparksblog.com/dcl/disney-destiny-updates-latest-news-from-the-heroes-and-villains-ship/','Steel cutting for the next ship: sister-ship technical specifications','The update names Wish, Treasure and Destiny as sister ships powered by LNG.')
src('adventure-debut','https://disneyparksblog.com/dcl/disney-cruise-line-adventure-updates/','March 10, 2026 Maiden Voyage; March 3, 2026 Singapore arrival','Adventure departs from Singapore March 10, 2026 for its maiden voyage; the arrival statement describes Disney cruising entering Asia for the first time.')
src('adventure-cor','https://disneyexperiences.com/adventure-cruise-ship-port-canaveral/','January 15, 2026 opening and first-Asia paragraphs','Disney states March 10, 2026 Singapore maiden voyage and first Disney cruise ship for families in Asia.')
src('adventure-nostops','https://plandisney.disney.go.com/question/wanted-know-disney-cruise-sails-meaning-no-island-stops-638689/','Answer: scheduled sailings without port stops','The answer identifies Disney Adventure from Singapore as the ship scheduled for sailings with no port stops.','Disney-hosted panelist advice corroborates launch itinerary descriptions; FAQ search result also matched but its opened page was an empty shell, so it is not claimed as read. Historical inaugural voyages only.')
src('hotpursuit','https://disneyparksblog.com/shdl/3-ways-imagineering-is-bringing-zootopia-to-life-at-shanghai-disney-resort/','Section 3 A Trackless Ride System on Zootopia: Hot Pursuit; December 20 closing','The named Zootopia ride uses trackless technology; the land welcomes guests December 20, 2023.')
src('riviera','https://www.prnewswire.com/news-releases/disneys-riviera-resort-welcomes-guests-with-the-sights-sounds-and-flavors-of-europe-300975283.html','Disney Vacation Club press release dated December 16, 2019: opening and Schultz remarks','Disney’s Riviera Resort opened December 16, 2019 and draws on Walt and Lillian’s European travels and the French and Italian Riviera.','Primary press release issued by Walt Disney World Resort, hosted by PR Newswire. No visit claimed.')
src('toy3','https://www.springfieldspringfield.co.uk/movie_script.php?movie=toy-story-3','Chuckles’s story, lines 1097–1137; Molly/Bonnie dialogue elsewhere','Chuckles tells Woody that Daisy owned him and Lotso, describes being left at a rest stop and Lotso being replaced, and says Bonnie later took Chuckles home.',secondary)
src('toy3-cor','https://www.disneyplus.com/en-gb/explore/articles/toy-story-characters-cast','Toy Story 3: Chuckles profile','Disney identifies Chuckles as the clown formerly owned by Daisy alongside Lotso and Big Baby, who helps Woody understand Lotso’s bitterness.')
src('toy3-place','https://en.wikipedia.org/wiki/Toy_Story_3','Plot: Woody at Bonnie’s house and Daisy flashback','At Bonnie’s house, Woody hears Chuckles tell Lotso’s story. Daisy is Lotso’s former owner; Bonnie is Woody’s eventual new owner; Molly is Andy’s sister.',secondary)
src('toy4-giggle','https://www.pixar.com/toy-story-4/','Giggle McDimples character profile, line 141','Officer Giggle McDimples is Bo Peep’s miniature police-officer best friend, small enough to perch on her shoulder.')
src('toy4-prizes','https://www.pixar.com/toy-story-4/','Ducky and Bunny profile, line 128','Ducky and Bunny are the named carnival prizes who join the toys’ adventure.')
src('toy4-duke','https://www.pixar.com/toy-story-4/','Duke Caboom profile, line 153','Duke is a Canadian stuntman toy with a functioning stunt-cycle and confident poses, but cannot do the awesome stunts advertised in his commercial.')
src('toy4-benson','https://www.pixar.com/toy-story-4/','Benson, Woody, Duke Caboom and Combat Carl profiles','Benson is the antique ventriloquist dummy leading Gabby’s henchmen; Woody is the sheriff, Duke the stuntman, and Combat Carl an action figure among the lost toys.')
src('lion2','https://d23.com/a-to-z/lion-king-ii-the-simbas-pride-film/','Film entry, lines 87–88','Simba’s daughter Kiara loves Kovu, Scar’s chosen successor and Zira’s son; Zira leads the exiled pride. Kiara and Kovu reconcile the prides.')
src('lion2-family','https://en.wikipedia.org/wiki/The_Lion_King_II:_Simba%27s_Pride','Plot 212–219 and Voice cast','Kiara is Simba and Nala’s daughter; Kovu is her love interest; Zira leads the Outsiders; Nuka and Vitani are Kovu’s older siblings.',secondary)
src('lion2-romance','https://en.wikipedia.org/wiki/The_Lion_King_II:_Simba%27s_Pride','Opening production/story description, line 205','The film’s plot is influenced by Shakespeare’s Romeo and Juliet.',secondary)
src('lion2-romance-cor','https://www.cinemaphile.org/reviews/1999/thelionking2simbaspride.html','David Keyes review, January 22, 1999: Shakespeare comparison paragraph','The contemporary review compares the sequel’s love-story structure to Romeo and Juliet.','Secondary critical analysis corroborates the standard influence attribution; no claim to a filmmaker quotation. The review’s unrelated claim about the first film is not used.')
src('return','https://en.wikipedia.org/wiki/The_Return_of_Jafar','Plot climax, lines 219–220','Iago returns, is injured by Jafar, and kicks the lamp into lava, destroying Jafar. Carpet was shattered, Genie knocked unconscious, and Aladdin trapped.',secondary)
src('return-cor','https://en.wikiquote.org/wiki/The_Return_of_Jafar','Climax dialogue and stage directions','The climax places Iago at the lamp’s destruction and the others reacting to his apparent sacrifice.','Secondary fan transcription corroborates the plot account; no original film viewing claimed.')
src('king3','https://en.wikipedia.org/wiki/Aladdin_and_the_King_of_Thieves','Plot, lines 198–210; Voice cast 220–231','Cassim is Aladdin’s father and leads the Forty Thieves. Sa’luk betrays and usurps him. The Hand of Midas turns touched things to gold; the Oracle locates it.',secondary)
src('king3-primary','https://www.disneyplus.com/en-sg/browse/entity-1b348f5f-fac7-4f98-8937-6fc4285d0740','Details synopsis','Aladdin’s father is King of the Forty Thieves and seeks the Hand of Midas, which can turn anything to gold.')
src('king3-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=aladdin-and-the-king-of-thieves','Father reveal; Sa’luk’s betrayal; Oracle and final Hand confrontation','Dialogue distinguishes Cassim, his son Aladdin, the Sultan, and Sa’luk; the Hand is the gold-making treasure sought by the thieves.','Secondary dialogue transcription; page header incorrectly says 1995, while Disney’s official release is 1996. Only clear dialogue/role evidence is used, corroborated with plot and Disney synopsis.')

# Each row is explicit human-reviewed authoring: source passages, premise, four
# stored-order option reasons, separate challenge, and editorial/duplicate notes.
rows = {}
def review(qid, keys, premise, reasons, challenge, notes='', sensitive=False):
    rows[qid] = (['b29-'+k for k in keys.split()], premise, reasons, challenge, notes, sensitive)

review(1596,'chicken chicken-manual','The 2005 feature has Foxy among the school bullies.',[
 'direct|Foxy Loxy is the mean fox classmate.', 'contradiction|Runt is in the outcast friend group, not a bully.', 'contradiction|Fish is Chicken Little’s outcast friend.', 'contradiction|Abby is his supportive friend.'],
 'Goosey also bullies him, so removed her from the alternatives. None of the three listed friends fills the bully role. Removed the temporary fox-species clue.', 'Specified the 2005 film and replaced the second defensible bully option.')
review(1597,'cows','The three named cows seek the bounty to save their home.',[
 'exhaustive-list|The named cow trio is Maggie, Mrs. Caloway and Grace.', 'exhaustive-list|The exhaustive protagonist trio does not contain Bessie, Buttercup or Daisy.', 'exhaustive-list|Pearl is the farm owner, not a cow in this trio; Clara and Rose do not complete the trio.', 'exhaustive-list|Molly, Patches and Belle are not the listed cow protagonists.'],
 'Checked every name in each group against the complete named trio. Corrected Caloway to the spelling used by Disney; none of the alternative groups names these three cows.', 'Corrected the character surname spelling from Calloway to Caloway. No overlapping cow-name fact in the full digests.')
review(1598,'raya raya-roles','Fang’s chief has warrior daughter Namaari, Raya’s rival.',[
 'direct|Namaari is the Fang chief’s daughter and Raya’s nemesis.', 'contradiction|Sisu is the dragon.', 'contradiction|Boun is a boy from Tail.', 'contradiction|Noi is a toddler from Talon.'],
 'A later alliance does not change identity; only Namaari fits both Fang royalty and rival. Raya’s Heart origin and Sisu’s identity are separate existing facts.')
review(1600,'show frozen-scenes','The studio’s lighting paper explicitly locates Elsa’s Show Yourself in Ahtohallan.',[
 'direct|Show Yourself is the Ahtohallan number.', 'contradiction|Into the Unknown is the earlier voice-summons song in Arendelle.', 'contradiction|Let It Go is the original film’s mountain solo.', 'contradiction|All Is Found is Iduna’s lullaby, echoed in the Ahtohallan sequence but not the title of Elsa’s principal number.'],
 'All Is Found is thematically and musically recalled, but the studio explicitly names the main Ahtohallan song Show Yourself. Removed the literal mother’s-spirit encounter interpretation.', 'The lighting paper and transcript support the final scene wording.')
review(1601,'frozen-rock frozen-music frozen-chorus frozen-scenes','Kristoff has an 80s-style solo with reindeer harmonies.',[
 'direct|Lost in the Woods is the ballad with the reindeer chorus.', 'contradiction|Reindeer(s) Are Better Than People is the short separate comic number, not the power ballad.', 'contradiction|Fixer Upper is the original film’s troll matchmaking ensemble.', 'contradiction|In Summer is Olaf’s original-film fantasy.'],
 'Kristoff also sings Reindeer(s), but the ballad and chorus identify the longer distinct number. Raised difficulty after removing the extra catch-up clause.', 'Distinct from the later Weezer-cover question: film number versus cover artist.')
review(1602,'frozen-scenes anna-song','Olaf’s farewell and disappearance precede Anna’s cave song.',[
 'direct|The Next Right Thing is Anna’s grieving cave solo.', 'contradiction|Show Yourself belongs to Elsa at Ahtohallan.', 'contradiction|Some Things Never Change is the early ensemble before the journey.', 'contradiction|When I Am Older belongs to Olaf in the forest.'],
 'Rechecked literal before/after timing: the farewell is 1202–1227; Anna’s solo begins at 1230. No distractor is the post-disappearance cave song.', 'Corrected the prior timing error; renewed review after the manual concern.')
review(1603,'wish-songs','Magnifico’s underappreciated villain number is separately named in production notes.',[
 'direct|This Is the Thanks I Get?! is his villain solo.', 'contradiction|At All Costs is the earlier duet celebrating the wishes.', 'contradiction|Knowing What I Know Now is the heroes’ uprising song.', 'contradiction|Welcome to Rosas introduces the kingdom.'],
 'At All Costs also includes Magnifico, but its observatory duet context excludes the rages-at-questioning scene.')
review(1604,'pooh-nightmare pooh-song pooh-album','Pooh dreams of Heffalumps and Woozles during the Blustery Day sequence included in Many Adventures.',[
 'direct|Heffalumps and Woozles names and accompanies the nightmare creatures.', 'contradiction|The Wonderful Thing About Tiggers is Tigger’s introduction, not the nightmare number.', 'contradiction|Rumbly in My Tumbly concerns Pooh’s hunger, not the nightmare creatures.', 'contradiction|A Rather Blustery Day concerns the windy day, not the dream’s creature song.'],
 'The compilation includes the earlier featurette’s nightmare; its framing does not turn another listed song into that dream number.', 'Used institutional creature identification and record listing with explicit secondary scene corroboration.')
review(1605,'robinsons robinsons-track','Disney’s DVD music-video credits identify the Rob Thomas song.',[
 'direct|Little Wonders is the Rob Thomas track.', 'exhaustive-list|Keep Moving Forward is not the credited Rob Thomas soundtrack song.', 'exhaustive-list|Look to the Future is not the Rob Thomas soundtrack title.', 'exhaustive-list|The Family Song is not the Rob Thomas soundtrack title.'],
 'The named recording is unique; removed the montage/end-credit placement claim so bonus-video metadata is not used as scene evidence.')
review(1606,'merlin','D23 explicitly links Higitus Figitus to magical carpetbag packing.',[
 'direct|Higitus Figitus is the packing song.', 'exclusive-inference|The separately named World Go Round number is not the uniquely identified packing song.', 'exclusive-inference|A Most Befuddling Thing is a separate listed song, not the packing number.', 'exclusive-inference|The Legend of the Sword is not the song D23 identifies for packing.'],
 'The source directly names the carpetbag action and title, excluding other song titles without inferring from a generic film page.')
review(1607,'eisner eisner-cor iger','Eisner’s Disney CEO tenure spans 1984–2005.',[
 'direct|Michael Eisner held the specified tenure.', 'contradiction|Iger succeeded him in 2005.', 'exclusive-inference|Michael Ovitz cannot be the CEO for Eisner’s exclusive named tenure.', 'contradiction|Wells was a separate president, whose death preceded Eisner also assuming that role.'],
 'The dates distinguish the CEO from company presidents. The 2003 Save Disney question tests a specific campaign target, not the entire tenure.', 'Shared Eisner answer retained as separate historical event.')
review(1608,'marvel marvel-cor','Disney completed the Marvel acquisition in 2009.',[
 'direct|Completion is dated December 31, 2009.', 'exclusive-inference|2006 is not the dated completion year.', 'exclusive-inference|2012 is not the dated completion year.', 'exclusive-inference|2015 is not the dated completion year.'],
 'Announcement versus completion cannot create another answer: both occurred in 2009; independently checked Disney press release and archive.')
review(1609,'lucas lucas-cor','The Lucasfilm acquisition occurred in 2012.',[
 'direct|Both agreement and completion are in 2012.', 'exclusive-inference|2009 predates the 2012 acquisition.', 'exclusive-inference|2015 is a later film-release year, not acquisition.', 'exclusive-inference|2006 is not the 2012 acquisition year.'],
 'Announcement and completion are both 2012. Cars Land and Grizzly Gulch merely share the year; they test different events.')
review(1610,'stars stars-cor','The two Walk of Fame records share the 1960 ceremony date.',[
 'exhaustive-list|Two category/address records are listed for 1960.', 'contradiction|One undercounts the two entries.', 'contradiction|Three exceeds the two 1960 honors.', 'contradiction|None contradicts both dated records.'],
 'Counted distinct addresses/categories, not webpages or ceremonies. Historical dating avoids an unbounded present count and removes the answer’s explanatory length clue.')
review(1611,'nbc nbc-cor','Disney changed from ABC to NBC for his 1961 color broadcasts.',[
 'direct|NBC is the new partner in 1961.', 'contradiction|ABC is the prior partner that he left.', 'exclusive-inference|CBS is not the named recipient of the 1961 move.', 'exclusive-inference|DuMont is not the named recipient of the 1961 move.'],
 'The 1954 Disneyland financing partner was ABC, a distinct transaction. This asks the 1961 business/network transition, not a television title, episode or cast fact.', 'Replaced the prohibited real-show title question with Walt’s historical business partnership; scope decision explicit.')
review(1612,'iger iger-deals eisner','Iger succeeded Eisner in 2005 and oversaw the named acquisitions.',[
 'direct|Bob Iger is the named successor.', 'contradiction|Eisner is the departing CEO.', 'exclusive-inference|Roy E. Disney is not the named 2005 successor.', 'exclusive-inference|Michael Ovitz is not the named 2005 successor.'],
 'The historical start year remains valid regardless of later CEO changes. Marvel and Lucasfilm deal years are separate from this executive identity.')
review(1614,'destiny-theme','The ship’s announced and debut overall theme is heroes and villains.',[
 'direct|Heroes & Villains is the stated ship-wide theme.', 'exclusive-inference|Pirates & Princesses is not the stated overall theme, even though pirate events exist.', 'exclusive-inference|Adventurers & Explorers is not the stated overall theme.', 'exclusive-inference|Legends & Lore is not the stated overall theme.'],
 'Presence of pirate events or adventure language does not make them the official overarching theme; final wording asks the 2025 design choice.')
review(1615,'destiny-theme','The Grand Hall’s Black Panther inspiration is Wakanda.',[
 'direct|Wakanda is the named fictional nation.', 'exclusive-inference|Sokovia is not the named Grand Hall inspiration.', 'exclusive-inference|Genovia is not the named Grand Hall inspiration.', 'exclusive-inference|Zamunda is not the named Grand Hall inspiration.'],
 'Specified fictional nation and historical debut. The general ship theme, Grand Hall nation and Tower Suite hero are three distinct design facts.')
review(1616,'destiny-dining','The current ship page identifies the musical Simba dining experience.',[
 'direct|Pride Lands: Feast of The Lion King is the advertised restaurant.', 'exclusive-inference|Simba’s Savanna Table is not its advertised name.', 'exclusive-inference|Pride Rock Kitchen is not its advertised name.', 'exclusive-inference|Circle of Life Dining is not its advertised name.'],
 'All options evoke the same story. Removed literal Lion King wording from the stem so the correct restaurant is not picked by title repetition.', sensitive=True)
review(1617,'destiny-show','The ship page identifies its exclusive Disney Hercules stage show.',[
 'direct|Disney Hercules is the named exclusive show.', 'exclusive-inference|Fantasia is not the named exclusive show.', 'exclusive-inference|The Odyssey is not the named exclusive show.', 'exclusive-inference|Aladdin is not the named exclusive show.'],
 'Other productions can share the theater, but the source singles out this exclusive musical. Removed the Greek-mythology clue and used the full title.', sensitive=True)
review(1618,'lng lng-cor','The three sister ships were designed for LNG power.',[
 'direct|Liquefied natural gas is named for all three.', 'contradiction|Biodiesel is not the stated design fuel.', 'contradiction|Hydrogen is not the stated design fuel.', 'contradiction|Nuclear fuel is not the stated design fuel.'],
 'Dual-fuel capability does not make biodiesel, hydrogen or nuclear the shared named design fuel. Removed broad emissions superiority language and matched fuel-type option forms.')
review(1619,'destiny-suites destiny-theme','The Tower Suite’s 2025 design honors Iron Man.',[
 'direct|Iron Man/Tony Stark is the named suite inspiration.', 'exclusive-inference|Captain America is not this suite’s named inspiration.', 'exclusive-inference|Thor is not this suite’s named inspiration.', 'contradiction|Black Panther inspires the Grand Hall instead.'],
 'Distinguished the Tower Suite from the Grand Hall and other suites; dropped the potentially disputable top-tier ranking.')
review(1620,'adventure-debut adventure-cor','Adventure’s maiden Singapore voyage is documented March 10, 2026.',[
 'direct|2026 is the actual departure year.', 'exclusive-inference|2024 is not the maiden-service year.', 'contradiction|2025 was an earlier plan, not the actual maiden-service year.', 'exclusive-inference|2027 is later than the documented debut.'],
 'Used the departure-day report rather than the superseded 2025 schedule; independently corroborated the launch year.')
review(1621,'adventure-debut adventure-cor','Disney calls Adventure its first Asia-based cruise ship.',[
 'direct|Asia is the continent of this first regional homeport deployment.', 'contradiction|Europe is not the region named for Adventure’s debut.', 'contradiction|South America is not the named region.', 'contradiction|Africa is not the named region.'],
 'Earlier temporary Asia visits or a European building yard do not change the first homebased deployment. Removed Singapore in the stem to avoid a simple city-to-continent giveaway.')
review(1622,'adventure-debut adventure-nostops cruise-nowhere','The inaugural short Singapore voyages are round trips without port calls.',[
 'direct|Cruises to nowhere is the itinerary term for a round trip with only sea days.', 'contradiction|World cruises travel a global multi-destination itinerary, unlike these short sea-only trips.', 'contradiction|Repositioning cruises move between homeports, unlike the specified round trips.', 'contradiction|Transatlantic crossings cross the Atlantic, not a Singapore sea-only round trip.'],
 'A transit/repositioning voyage before Singapore service is outside the explicitly inaugural Singapore round-trip scope. Historical wording avoids assuming future schedules never add stops.')
review(1623,'hotpursuit','Disney identifies the trackless Zootopia attraction and December 2023 debut.',[
 'direct|Zootopia: Hot Pursuit is the named ride.', 'exclusive-inference|Zootopia Speedway is not the ride’s name.', 'exclusive-inference|Wild Chase Adventure is not its name.', 'exclusive-inference|Predator Pursuit is not its name.'],
 'This tests the attraction name; land opening-date and first-land questions elsewhere test additional facts. Historical wording avoids a current operating-status claim.')
review(1624,'riviera','The opening-day release names Riviera Resort and its European-travel inspiration.',[
 'direct|Disney’s Riviera Resort is the named December 2019 opening.', 'exclusive-inference|BoardWalk Inn is not the named new resort in the opening-day announcement.', 'exclusive-inference|Beach Club is not the new resort named in that announcement.', 'exclusive-inference|Coronado Springs is not the new European-travel resort named in that announcement.'],
 'Coronado had a new tower in 2019, but the question specifies a hotel opening and the European-travel inspiration; the release names Riviera. Removed Riviera from the stem and the extra ongoing Skyliner claim.')
review(2001,'toy3 toy3-cor toy3-place','Lotso and Chuckles formerly belonged to Daisy and were left behind on a trip.',[
 'direct|Daisy is their explicitly named shared owner.', 'contradiction|Bonnie later takes Chuckles home, not Lotso’s original owner.', 'contradiction|Molly is Andy’s sister, not Daisy.', 'exclusive-inference|Sunny is not the named child in this account.'],
 'Daisy’s identity is distinct from the exact pendant inscription in #2307; knowing the name does not supply that inscription. Checked replacement versus abandonment distinction.')
review(2002,'toy3 toy3-cor toy3-place','Chuckles recounts the backstory at Bonnie’s house.',[
 'direct|Chuckles tells the story.', 'contradiction|Big Baby is in the backstory and remains with Lotso, not its narrator at Bonnie’s.', 'contradiction|Ken remains at Sunnyside and is not this narrator.', 'contradiction|Buzz remains among the daycare toys and is not this narrator.'],
 'Rechecked location: Chuckles formerly lived at Sunnyside but Bonnie took him home. The conversation is at Bonnie’s; removed the clown qualifier to keep all toy options plausible.', 'Corrected the false location premise.')
review(2003,'toy4-giggle','Pixar names the miniature police officer as Bo’s best friend.',[
 'direct|Giggle McDimples is the named officer friend.', 'exclusive-inference|Officer Sparkle is not that character’s name.', 'exclusive-inference|Deputy Doll is not that character’s name.', 'exclusive-inference|Tiny Trudy is not that character’s name.'],
 'The studio describes shoulder-perching, not the asserted pocket habit. Removed that unsupported detail; no option is another accepted alias.')
review(2004,'toy4-prizes','The studio identifies Ducky and Bunny as carnival prizes joining the adventure.',[
 'direct|Ducky and Bunny are the named pair.', 'exclusive-inference|Salt and Pepper are not the pair’s names.', 'exclusive-inference|Lefty and Righty are not the pair’s names.', 'exclusive-inference|Winky and Blinky are not the pair’s names.'],
 'The group is an exact two-name identity; removed unneeded county-fair specificity. No related question tests this pair.')
review(2005,'toy4-duke','Duke can ride and pose, but his performance falls short of his commercial.',[
 'direct|His admitted limitation is inability to perform the advertised stunts.', 'contradiction|The profile explicitly has him riding his powerful stunt-cycle.', 'contradiction|The profile explicitly says he confidently performs stunt poses.', 'contradiction|The profile identifies him as a Canadian stuntman toy.'],
 'Removed afraid-of-heights because it could coexist with insecurity and was not excluded by commercial failure alone. Each final alternative now contradicts a positive studio detail.', 'Narrowed the asked limitation and replaced unsupported simultaneous-trait distractors.')
review(2006,'toy4-benson','Pixar names Benson as the lead dummy.',[
 'direct|Benson leads the dummy henchmen.', 'contradiction|Woody is the cowboy sheriff.', 'contradiction|Duke Caboom is the stuntman toy.', 'contradiction|Combat Carl is an action figure among the lost toys.'],
 'Used the named individual leader rather than treating Bensons as an attested collective name; removed the unnecessary night-only patrol detail.')
review(2007,'lion2 lion2-family','Kiara is Simba and Nala’s daughter.',[
 'direct|Kiara is the daughter named by the archive and cast/plot.', 'contradiction|Vitani is Zira’s daughter and Kovu’s sibling.', 'contradiction|Zira is Kovu’s mother and the rival pride leader.', 'exclusive-inference|Kula is not the archive’s named daughter.'],
 'Original and sequel generation names are distinct; the listed alternatives cannot be alternate names for Simba’s daughter.', 'Secondary-film coverage remains modest: six questions in this title including the related pride-name question.')
review(2008,'lion2 lion2-family','Kiara’s romantic partner is Kovu of the exiled pride.',[
 'direct|Kovu is her named romantic partner.', 'contradiction|Nuka is Kovu’s older sibling, not Kiara’s partner.', 'contradiction|Scar is the deceased predecessor whose loyalists formed the exiled pride.', 'contradiction|Zazu is the royal hornbill.'],
 'Only Kovu satisfies the romance and upbringing clauses; Kiara’s own name question does not establish her partner’s name.')
review(2009,'lion2 lion2-family','Zira leads the exiles and seeks revenge for Scar.',[
 'direct|Zira is the named leader and Kovu’s mother.', 'contradiction|Sarabi is Simba’s mother, not leader of this rival pride.', 'contradiction|Vitani is Zira’s daughter, not this vengeful maternal leader.', 'contradiction|Shenzi is a hyena from the first film, not Kovu’s mother.'],
 'Vitani later leads former Outsiders away from Zira, but the stem’s son-avenging-Scar motive and vengeful leader context identify Zira, not that later transition.')
review(2010,'lion2-family lion2','The cast and plot identify Nuka and Vitani as Kovu’s siblings.',[
 'exhaustive-list|Nuka and Vitani are the named siblings.', 'contradiction|Timon and Pumbaa are Simba’s companions, not these siblings.', 'contradiction|Shenzi and Banzai are hyenas, not Kovu’s siblings.', 'contradiction|Simba and Taka are not the named sibling pair.'],
 'Family relationship is separate from their other narrative roles. Checked all members of each pair rather than matching one familiar name.')
review(2011,'lion2-romance lion2-romance-cor','The Romeo and Juliet parallel is attested in the film overview and contemporary criticism.',[
 'direct|Romeo and Juliet supplies the feuding-families romance parallel.', 'exclusive-inference|A Midsummer Night’s Dream is not the attested central-romance source.', 'exclusive-inference|Macbeth is not the attested central-romance source.', 'exclusive-inference|The Tempest is not the attested central-romance source.'],
 'This concerns the central romance, not whether another Shakespeare theme can be compared to a scene. Removed the extra Hamlet claim about the first film.', 'Primary filmmaker statement was unavailable; secondary plot attribution is corroborated by a contemporary review. No direct filmmaker quotation claimed.')
review(2013,'return return-cor','Iago’s final intervention sends the lamp into lava.',[
 'direct|Iago kicks the lamp into the lava despite his injury.', 'contradiction|Abu is not the actor of that final kick.', 'contradiction|Carpet is shattered until Jafar’s destruction reverses the magic.', 'contradiction|The Sultan is not the actor of the lamp-destroying action.'],
 'Unlike the old former-sidekick wording, the final question requires a new sequel action, not merely recalling Iago’s original-film identity. Checked the distinct lava action against the earlier well disposal.')
review(2014,'king3 king3-dialogue','Aladdin identifies Cassim as his father in the thieves’ hideout.',[
 'direct|Cassim is his father.', 'contradiction|The Sultan is Jasmine’s father, not Aladdin’s.', 'exclusive-inference|Fasir is not the father named in the reveal.', 'contradiction|Sa’luk is Cassim’s rival, not Aladdin’s father.'],
 'Distinguished Cassim’s father identity from his job as thief leader; the paired job question does not supply Cassim’s name.')
review(2015,'king3 king3-primary','Cassim leads the group explicitly called Forty Thieves.',[
 'direct|Forty Thieves is the group’s proper name.', 'contradiction|Thirty Thieves is not the name.', 'contradiction|Sixty Thieves is not the name.', 'contradiction|Fourteen Thieves is not the name.'],
 'The film title gives thieves but not the number; every final option shares Thieves. This asks the proper name, not the number still free after arrests, which is smaller.', 'Replaced distractors to remove the title-word giveaway.')
review(2016,'king3 king3-dialogue','Sa’luk betrays Cassim and takes control of the remaining thieves.',[
 'direct|Sa’luk is the usurper and final antagonist.', 'contradiction|Jafar is the earlier films’ villain, not this usurper.', 'exclusive-inference|Mozenrath is not the named usurper in this film.', 'exclusive-inference|Abis Mal is not the usurper of Cassim’s group.'],
 'The subject is the film’s criminal leadership conflict, not who was a franchise villain generally. The named takeover and final confrontation identify Sa’luk.')
review(2017,'king3 king3-primary king3-dialogue','The thieves seek the gold-making Hand of Midas.',[
 'direct|The Hand of Midas is the gold-making treasure.', 'exclusive-inference|The Golden Scarab is not the gold-transforming treasure identified here.', 'contradiction|The Oracle guides them to the Hand; Oracle’s Eye is not the named gold-making object.', 'exclusive-inference|The Sultan’s Scepter is not the treasure named for this ability.'],
 'The Oracle locates the artifact but does not itself turn touched objects to gold. Cassim and Sa’luk identities are separate from the artifact/ability fact.')

# Resume rechecks: replace unavailable draft routes with passages actually read.
src('chicken-manual','https://usermanual.wiki/Disney-Interactive-Studios/DisneyInteractiveStudiosChickenLittleUsersManual513990.956070478.pdf','Disney Interactive manual, printed pp. 6-9 (PDF pp. 3-4), character biographies','Foxy is Chicken Little’s nemesis and assigns bullying to Goosey. Abby, Fish and Runt are his friends.','Primary licensed game manual corroborates the same film character relationships; game-only events are not used.')
src('wish-songs','https://thewaltdisneycompany.com/news/behind-the-music-of-disney-animations-wish-with-julia-michaels-and-benjamin-rice/','Welcome to Rosas; At All Costs; This Is the Thanks I Get?!; Knowing What I Know Now sections','The songwriters distinguish the introductory kingdom song, the duet, Magnifico’s increasingly dark villain number, and the heroes’ uprising number.','Primary songwriter interview inspected. Draft production-notes PDF returned 403, so it is replaced, not treated as inspected.')
src('robinsons','https://music.apple.com/us/song/little-wonders/1444114787','Track title, performer and soundtrack album link, lines 9-13','Little Wonders is credited to Rob Thomas on Meet the Robinsons (Soundtrack from the Motion Picture).','Label-distributed track metadata inspected; complete track list corroborated in the secondary film article. Draft DVD site timed out and is not claimed as inspected.')
src('cruise-nowhere','https://www.ncl.com/nz/en/cruise-faq/where-does-a-cruise-to-nowhere-go','Where does a cruise to nowhere go? first definition sentence, lines 190-192','A cruise to nowhere leaves and returns to the same port without stopping at another port.','Primary cruise-line definition only. Unrelated legal explanation is not used.')
sources['b29-show']['locator'] = 'Section 1 Introduction, lines 38-42'
sources['b29-eisner']['evidence'] = 'Eisner became CEO September 22, 1984; the entry distinguishes his CEO office from the presidency he assumed after Frank Wells died. His retirement year is corroborated by the separate 2005 Disney timeline.'
for key in ['destiny-dining','destiny-show']:
    sources['b29-'+key].update(timeSensitive=True,nextReviewAt='2027-02-06')
for qid in [2001,2009]:
    rows.pop(qid)  # Preserved duplicate retirements after complete topic review.
template = read('audit/runs/next-shard-0029-final-resume-template.json')
template['at'] = '2026-11-08'  # Reviewer date in America/Toronto.
assert {r['questionId'] for r in template['reviews']} == set(rows)
for r in template['reviews']:
    qid = r['questionId']
    ids, premise, reasons, challenge, notes, sensitive = rows[qid]
    used.update(ids)
    r.update(checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],
             notes=notes or 'Reviewed complete topic/comparison context, final wording, option balance, category, difficulty and theatrical/secondary scope; distinct fact retained.',
             context='Final stored wording and four options; exact film/version or dated historical/ship context in the stem.',
             timeSensitive=sensitive, nextReviewAt='2027-02-06' if sensitive else None,
             premise=dict(reason=premise,sources=ids),
             options=[dict(basis=x.split('|',1)[0],reason=x.split('|',1)[1],sources=ids) for x in reasons],
             challenge=dict(reviewer='Codex',at='2026-11-08',premiseChecked=True,alternativesExcluded=True,notes=challenge))
template['sourcesChecked'] = sorted(used)
write('audit/source-notes.json',library)
write('audit/runs/next-shard-0029-reviewed-notes.json',template)
print(f'Authored {len(rows)} explicit final reviews using {len(used)} source passages.')
