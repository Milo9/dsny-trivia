"""Codex's inspected passages and explicit four-option, final-wording reviews."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
from question_audit import digest
AT='2026-11-07'
DUE='2027-02-05'
library=json.loads((ROOT/'audit/source-notes.json').read_text(encoding='utf-8'))
def source(key,url,locator,evidence,topic,mutable=False,limitations='Primary institutional text inspected; no film or video playback claimed.'):
    library['sources']['b9-'+key]=dict(url=url,locator=locator,evidence=evidence,topics=[topic],checkedBy='Codex',checkedAt=AT,timeSensitive=mutable,nextReviewAt=DUE if mutable else None,limitations=limitations)
source('anniversary','https://disneyparksblog.com/disney-experiences/disney-cruise-lines-25th-anniversary-season-starts-today-heres-what-you-need-to-know/','May 1, 2023 dateline; opening Silver Anniversary at Sea announcement','The 25th anniversary season began May 1, 2023.','cruise')
source('fleet2024','https://disneyconnect.com/app/uploads/2024/07/fact_sheet_disney_cruise_line_2024_Q3-1.pdf','Disney Cruise Line Fleet table, birthplaces and Wish capacity','The fleet table identifies Fincantieri in Marghera/Ancona, Italy for Magic and Marghera, Italy for Wonder; Wish capacity is 4,000.','cruise',True)
source('wishcapacity','https://plandisney.disney.go.com/question/wanted-know-total-passenger-size-dcl-ships-curious-link-605735/','March 14, 2025 answer, final main paragraph','The panelist explicitly says Disney Wish holds about 4,000 passengers.','cruise',True,'Official Disney-hosted panel advice, corroborated by the institutional fleet table; maximum guests, not typical double occupancy or crew.')
source('hyperspace','https://disneycruise.disney.go.com/en-gb/onboard-activities/star-wars-hyperspace-lounge/','Title, Ship Locations and opening description','Star Wars: Hyperspace Lounge is the space-themed lounge aboard Disney Wish.','cruise',True)
source('palo','https://disneycruise.disney.go.com/en-as/onboard-activities/palo-restaurant/','Ship Locations; Meal Period; opening cuisine description','Magic is listed; Palo offers adult-exclusive Northern Italian cooking at brunch and dinner.','cruise',True)
source('dreamcolors','https://www.meyerwerft.de/en/ships/ship_detail/disney_dream','Opening ship-history paragraphs, especially paragraph 2','The builder describes Dream and Fantasy with black hulls, white superstructures, red funnels and yellow lifeboats, recalling classic ocean liners.','cruise')
source('magicitaly','https://www.disneyholidays.co.uk/disney-cruise-line/ships/magic-wonder/','Opening paragraph under Disney Magic and Disney Wonder','Disney Magic was built at Fincantieri shipyards in Italy.','cruise')
source('wonderitaly','https://cruiseindustrynews.com/cruise-news/2024/09/disney-wonder-completes-25-years-of-service/','September 8, 2024 article, second body paragraph','Wonder was built at Fincantieri Marghera in Venice, Northern Italy.','cruise',False,'Specialist trade reporting corroborates the primary Disney fleet table; shipyard website served only a navigation shell.')
source('buccaneer','https://insidethemagic.net/2011/01/videos-buccaneer-blast-fireworks-launch-and-jack-sparrow-runs-amuck-at-sea-on-the-disney-dream-cruise-ship/','January 22, 2011 report; opening three body paragraphs','The eyewitness christening-cruise report calls Dream’s new pirate fireworks show Buccaneer Blast and identifies its pirate activities.','cruise',False,'Contemporaneous first-person reporting; text inspected, embedded video not played. Official planDisney corroboration also consulted; no fleetwide or current-sailing guarantee inferred.')
source('buccaneerpanel','https://plandisney.disney.go.com/question/details-pirate-deck-party-disney-dream-really-crowded-245458/','Dream Pirate Deck Party answer, late-evening fireworks sentence','The official-hosted panel answer calls Dream’s pirate fireworks Buccaneer Blast.','cruise',False,'Indexed Disney-hosted panel answer corroborates the contemporaneous christening report; used for naming, not exact current schedule.')
source('satellite','https://disneycruise.disney.go.com/en-gb/onboard-activities/satellite-falls-pool-lounge/','Title; Ship Locations; adult-exclusive description; cascading-water image caption','Satellite Falls is an adult-exclusive wading pool on Dream and Fantasy; a curtain of water cascades into the pool.','cruise',True)
source('letitgo','https://video.disney.com/watch/disney-s-frozen-let-it-go-sequence-performed-by-idina-menzel-4ecd3e729706a16e5090f1de','Official sequence title and descriptive paragraph','The film sequence is Elsa fleeing Arendelle and creating her palace; Let It Go is performed by Elsa’s voice Idina Menzel.','Frozen')
source('jiminy','https://d23.com/walt-disney-legend/ned-washington/','Opening biography paragraph','When You Wish Upon a Star was first introduced by Jiminy Cricket in Pinocchio.','Pinocchio')
source('surface','https://thewaltdisneycompany.eu/news/disneys-first-ever-british-sign-language-music-video-released-for-encantos-hit-song-surface-pressure/','July 14, 2022 release; first and third body paragraphs','Surface Pressure is from Encanto’s original motion picture soundtrack and is Luisa’s song about her superstrength burden.','Encanto')
source('toystory2','https://d23.com/a-to-z/toy-story-2-film/','Production/music paragraph','Randy Newman added When She Loved Me and Woody’s Roundup as new songs for Toy Story 2 (1999).','Toy Story')
source('unknown','https://music.apple.com/us/song/into-the-unknown/1487738283','Track title and artist/album metadata','Into the Unknown is credited to Idina Menzel and AURORA on the Frozen 2 original motion picture soundtrack.','Frozen',False,'Label-distributed recording metadata, not independent viewing. Actor/character mapping corroborated with Disney production notes and original film credits.')
source('unknowncast','https://lumiere-a.akamaihd.net/v1/documents/into_the_unknown_disney_production_notes_final_a8c39e97.pdf','Idina Menzel biography heading','Production notes explicitly credit Idina Menzel as voice of Elsa.','Frozen')
source('eltonalbum','https://www.eltonjohn.com/discography/the-lion-king','Tracklist items 1, 5, 10 and 12; liner notes','The album distinguishes film cast renditions from Elton John’s separate Circle of Life and Can You Feel the Love Tonight tracks.','The Lion King')
source('eltondisney','https://thewaltdisneycompany.com/press-releases/sir-elton-john-among-12-honorees-to-receive-prestigious-disney-legends-award/','Elton John biography, soundtrack singles paragraph','Disney identifies Can You Feel the Love Tonight and Circle of Life as the soundtrack’s hit singles for Elton John.','The Lion King')
source('oscars1995','https://www.oscars.org/oscars/ceremonies/1995','Music (Original Score); Music (Original Song); Lion King film entry','Hans Zimmer won Original Score for The Lion King. Can You Feel the Love Tonight won Original Song; Circle of Life and Hakuna Matata were nominees. Songs credit music to Elton John and lyrics to Tim Rice.','The Lion King')
source('encantosongs','https://d23.com/a-to-z/encanto-film/','Release/credits paragraph','Encanto (2021) has a Germaine Franco score and eight original songs by Lin-Manuel Miranda.','Encanto')
source('savages','https://music.apple.com/us/song/savages/1442941927','Title; album and performer metadata','Savages appears on Walt Disney Records’ Pocahontas (Music From the Motion Picture), credited to David Ogden Stiers, Jim Cummings, Judy Kuhn and the Pocahontas cast.','Pocahontas',False,'Label-distributed soundtrack metadata inspected; not video playback. This establishes the specific film attribution rather than generic plot-synopsis silence.')
source('beautysinger','https://d23.com/a-to-z/beauty-and-the-beast-film/','Voice cast and title-song paragraph','Angela Lansbury voices Mrs. Potts and sings the title song in the story; Celine Dion and Peabo Bryson sing the separate end-credits rendition.','Beauty and the Beast')
source('jungleprofiles','https://skgaleana.com/wp-content/uploads/2020/10/Meet-the-characters-feature-profiles-Jungle-Book.pdf','Disney 2013 character profiles, PDF pages 4 (King Louie), 5 (Baloo), 6 (Kaa), 9 (vultures)','King Louie’s featured number is I Wanna Be Like You, sung by Louis Prima; The Bare Necessities introduces Baloo; Trust in Me belongs to Kaa; vultures perform the friendship quartet.','The Jungle Book',False,'Disney-copyrighted promotional character profiles hosted by a third party; authorship printed in PDF. Corroborated with Disney A-to-Z film entry.')
source('junglelist','https://d23.com/a-to-z/jungle-book-the-film/','Voice cast and song list in final paragraph','Louis Prima voices King Louie. Film songs include I Wanna Be Like You, Trust in Me, That’s What Friends Are For and Bare Necessities.','The Jungle Book')
source('moanacredits','https://www.disneymusiccredits.com/album/moana/','Original Songs and Original Score headings','Original songs credited to Lin-Manuel Miranda, Opetaia Foaʻi and Mark Mancina; score separately credited to Mancina.','Moana')
source('moanacreator','https://www.linmanuel.com/project/moana/','2016 Project Description; Original Music; Original Cast','The 2016 Moana credits list Miranda, Foaʻi and Mancina for original music; Dwayne Johnson is Maui; Auliʻi Cravalho is Moana; Jemaine Clement is Tamatoa.','Moana')
source('welcomeclip','https://www.herzogcompany.com/case-studies/moana-youre-welcome-split-screen-music-video/','Video creator case-study description','The company that made the split-screen Disney video identifies You’re Welcome as written by Miranda and performed by Dwayne Johnson.','Moana',False,'Primary production vendor describing its own work; corroborated by Disney’s indexed official You’re Welcome clip description, whose full-page fetch timed out.')
source('moanasolos','https://princess.disney.com/moana','Original Moana video catalog, Shiny and How Far I’ll Go entries','Disney credits Shiny to Jemaine Clement and How Far I’ll Go to Auliʻi Cravalho.','Moana')
source('moanaway','https://video.disney.com/watch/we-know-the-way-clip-disney-s-moana-54318b5389b986747895af65','Description below official clip title','We Know the Way is written and performed by Miranda and Foaʻi, rather than Johnson.','Moana')
source('oscars2000','https://www.oscars.org/oscars/ceremonies/2000','Tarzan entry; Original Song and Original Score results','Tarzan’s sole nomination and win was You’ll Be in My Heart, music and lyrics by Phil Collins, for Original Song; Original Score went to The Red Violin.','Tarzan')
source('tarzan','https://d23.com/a-to-z/tarzan-film/','Music/voice cast paragraph and following award sentence','Tarzan features five Collins songs, four sung by him in the film, and Mark Mancina’s score; You’ll Be in My Heart won the Song Oscar.','Tarzan')
source('oscars1992','https://www.oscars.org/oscars/ceremonies/1992','Music (Original Song), winner and nominees','Beauty and the Beast won Original Song at the 1992 ceremony; Menken is composer and Ashman lyricist.','Beauty and the Beast')
source('oscars2014','https://www.oscars.org/oscars/ceremonies/2014','Frozen entry and Music (Original Song) winner','Frozen’s two wins were Animated Feature and Original Song for Let It Go; the song’s category is distinct from the film’s feature award.','Frozen')
source('ashman','https://d23.com/a-to-z/ashman-howard/','Complete biography entry','Ashman, a lyricist partnering with Alan Menken on Little Mermaid, Beauty and the Beast and Aladdin, died March 14, 1991.','Beauty and the Beast')
source('ashmanloc','https://www.loc.gov/exhibits/music-and-animation/aladdin-1992.html','Opening paragraph; Ashman storyboard archival description','Aladdin began with lyricist Ashman; Tim Rice added lyrics after Ashman’s 1991 death; the archive has Ashman’s 1990 Friend Like Me storyboard.','Aladdin')
source('dory','https://www.pixar.com/finding-dory','Synopsis; Hank; Bailey; Destiny; Fluke & Rudder character sections','Bailey is a beluga whale, Destiny a nearsighted whale shark, Hank a seven-armed octopus, and Fluke a sea lion.','Finding Nemo/Dory')
source('inside2','https://www.pixar.com/inside-out-2','Anxiety, Ennui and Envy character sections','Anxiety prepares for every negative outcome and wants Riley to fit in. Ennui embodies bored apathy and controls the console via a mobile app; Envy covets what others have.','Inside Out 2')
source('luca','https://www.pixar.com/luca','Synopsis; Luca Paguro; Alberto Scorfano; Just Add Water','Luca and Alberto are sea monsters hiding their identities in an Italian seaside town. Luca is already a sea monster herding goatfish before he explores the human world; transformation conceals their sea-monster nature.','Luca')
source('red','https://www.pixar.com/turning-red','Growing Up Is a Beast; Meilin Lee','Emotional excitement transforms Mei into a giant red panda.','Turning Red')
source('onward','https://www.pixar.com/onward','Opening synopsis; Ian Lightfoot and Barley Lightfoot sections','Onward follows two teenage elf brothers, Ian and Barley Lightfoot.','Onward')
source('soul','https://www.pixar.com/soul','Synopsis; Joe Gardner character profile','Soul follows jazz pianist Joe Gardner into the Great Before, not two young sea monsters.','Soul')
source('sulley','https://video.disney.com/sully','Character description under Sully Videos heading','Sulley is identified as the large furry blue monster with purple spots.','Monsters Inc/University')
source('monsters','https://www.pixar.com/monsters-inc','Synopsis; James P. Sulley Sullivan; Mike Wazowski; Randall; Roz','Sulley is James P. Sullivan, the top scarer; Mike is his assistant, Randall his rival and Roz the administrative character.','Monsters Inc/University')
source('nemoaddress','https://news.disney.com/a-finding-nemo-quote-for-every-occasion','When you forget where you’re going quotation','Disney reproduces the Finding Nemo address as 42 Wallaby Way, Sydney.','Finding Nemo/Dory')
source('nemomask','https://www.springfieldspringfield.co.uk/movie_script.php?movie=finding-nemo','Anglerfish-lit mask-reading sequence, from Look. A mask through Dory remembering its text (lines 763–810 in inspected transcript)','Dory reads the street and city from the mask, then remembers it after the escape. The address matches Disney’s published quotation.','Finding Nemo/Dory',False,'Secondary dialogue transcript corroborates scene context; exact address independently confirmed by Disney’s own quotation. No video playback claimed.')

rows={}
def review(qid,keys,context,premise,reasons,challenge,notes='',bases=None):
    rows[qid]=(keys.split(),context,premise,reasons,challenge,notes,bases)
review(426,'anniversary','DCL’s historical 25th anniversary season.',
 'The dated announcement explicitly identifies 2023 as the 25th season.',
 ['2023 is the announcement and celebration year.','2021 is two years before this anniversary.','2022 is one year before this anniversary.','2024 is one year after this anniversary.'],
 'The anniversary is historical, not the present age of the company. None of the other years can be the dated 25th season.',
 'Distinct anniversary fact; launch year q137 and Pearl-tier introduction q982 require different recall.')
review(428,'fleet2024 wishcapacity','Approximate maximum passenger capacity of Disney Wish; excludes crew.',
 'The fleet table and panel advice agree on about 4,000 guests.',
 ['4,000 matches the stated guest capacity.','2,500 understates the identified Wish capacity.','6,000 overstates that capacity.','1,800 understates that capacity.'],
 'Do not substitute double-occupancy totals, cabins or crew. Approximate advertised maximum excludes each alternative.',
 'Distinct from rotational restaurant count and youth age ranges; annual recheck not needed yet, 90-day source recheck scheduled.')
review(429,'hyperspace','Disney Wish Star Wars lounge identity.',
 'Disney names the Wish venue Star Wars: Hyperspace Lounge.',
 ['Hyperspace Lounge is the named venue.','Cantina Bar is not the identified Wish venue name.','Rebel Outpost is not the identified venue.','Millennium Falcon Bar is not its name.'],
 'Other Star Wars experiences elsewhere cannot rename this Wish bar. Only the exact venue title fits.',
 'q2349 tests the cocktail artifact, not the venue name.')
review(430,'palo','Palo on Magic, distinct from Palo Steakhouse aboard Wish.',
 'The venue page identifies Italian, adult-exclusive cuisine, brunch and dinner, and lists Magic.',
 ['Italian adult-exclusive brunch/dinner matches all stated attributes.','French cuisine contradicts Northern Italian.','Family French dining conflicts with both age policy and cuisine.','A poolside buffet conflicts with the described adult-exclusive restaurant.'],
 'Magic prevents conflation with Wish’s steakhouse. The correct option’s extra parenthesis supplies service context, but each choice gives a comparable cuisine/service claim.',
 'Distinct from Remy’s French cuisine (148) and Palo’s name etymology (436).')
review(432,'dreamcolors','Disney Dream’s 2011 debut exterior, not current fleet variations.',
 'The builder describes the original Dream design as dark/black hull with red funnels.',
 ['Dark hull and red funnels matches the builder.','White hull and gold funnels disagrees on both colors.','Red hull and white funnels reverses the actual placement.','White hull and blue funnels disagrees on both.'],
 'Dark includes the custom near-black/navy shade without asserting pure black paint. Yellow belongs to lifeboats, not funnels; all options are parallel pairs.',
 'q2279 asks the shade nickname, which is a distinct naming fact. Historical scope avoids future fleet exceptions; medium suits paired-color recall.')
review(433,'fleet2024 magicitaly wonderitaly','Original construction country for both Magic and Wonder, not flag or homeport.',
 'Disney’s table gives Italian yards for both; official Magic page and trade Wonder history corroborate.',
 ['Both were built in Italy.','Germany applies to later Meyer-built ships, not these two.','United States is not either listed original construction country.','Finland is not either listed original construction country.'],
 'A Bahamian flag or Florida homeport does not change the build country. Both ships, not merely one, are covered.',
 '1219 tests company identity, not country; 902’s Italian pavilion is unrelated.')
review(434,'buccaneer buccaneerpanel','Disney Dream at its 2011 debut; not every ship’s present Pirate Night.',
 'The eyewitness debut report identifies Buccaneer Blast as the pirate fireworks show; panel text corroborates its name.',
 ['Buccaneer Blast is the recorded show title.','Pirate’s Salute is not the title in the debut report.','Cannon Fire is not that show’s name.','Sea Blaze is not that show’s name.'],
 'Wish’s later pirate show and itineraries with no fireworks cannot challenge the historical Dream-specific claim.',
 'Distinguishes the named show from q422’s generic Pirate Night event association.')
review(435,'satellite','Adult water-curtain wading pool on Dream and Fantasy.',
 'The dedicated official page names Satellite Falls and both ships, plus adult-only access and cascading water.',
 ['Satellite Falls matches name, ship pair and water-curtain description.','Rainforest Falls is not the named pool.','Cascade Pool is not this venue’s title.','Neptune’s Retreat is not this venue’s title.'],
 'The wording refers to the cascading-water wading area, not the broader Quiet Cove pool; a waterfall need not be a natural cliff.',
 '975 asks the general Quiet Cove area, not this named wading pool.')
review(438,'letitgo','Original English-language Frozen sequence.',
 'Disney explicitly maps the song sequence and its singer to Elsa.',
 ['Elsa performs the identified sequence.','Anna is not the character singing this solo.','Kristoff is not its singer.','Olaf is not its singer.'],
 'Actor Menzel is the voice of Elsa; other characters’ songs or later sing-alongs do not make them this original sequence’s singer.',
 '701 tests performer identity, requiring the actor name; 697 asks the song itself. This character-performance question remains distinct.')
review(441,'jiminy','Original Pinocchio performance, not later covers.',
 'Disney’s archive explicitly says Jiminy Cricket introduced the song in Pinocchio.',
 ['Jiminy Cricket is the identified singer.','Pinocchio is the title character but not this song’s introducing vocalist.','Geppetto is not the introducing singer.','The Blue Fairy is not the identified vocalist.'],
 'Jiminy’s conscience role does not prove a song credit; the separate archival performance sentence does. Cover versions do not alter it.',
 '993 concerns Give a Little Whistle, a different song; 1102 concerns his appointment as conscience.')
review(446,'surface','Film attribution for Surface Pressure, not a later signed adaptation.',
 'The company release directly places Surface Pressure on Encanto’s soundtrack and identifies Luisa’s role.',
 ['Encanto is the explicit film attribution.','Frozen is not the originating film identified for this Luisa song.','Brave is not the identified film.','Moana is not the identified film.'],
 'The signed adaptation is derived from Encanto; it does not introduce a second listed film. Luisa’s burden provides specific corroborating context.',
 'No other full-topic question tests this particular song-to-film link.')
review(447,'toystory2','First introduction of the song, not later franchise references or reprises.',
 'The archive calls When She Loved Me a new Toy Story 2 song.',
 ['Toy Story 2 introduced the song.','The 1995 Toy Story predates the new sequel song.','Toy Story 3 follows its documented introduction.','Toy Story 4 follows that introduction.'],
 'A later reprise cannot satisfy introduced; the new-song production credit, rather than absence from a synopsis, excludes the other numbered films.',
 'Separate from 437/2283’s You’ve Got a Friend in Me and 2286’s We Belong Together.')
review(448,'welcomeclip moanacreator moanasolos moanaway','Maui’s original 2016 Moana number, not the end-credits duet.',
 'The production vendor credits You’re Welcome to Dwayne Johnson; creator credits identify Johnson as Maui.',
 ['You’re Welcome is Johnson/Maui’s identified number.','How Far I’ll Go is the Moana longing number, not the identified Maui performance.','Shiny is Tamatoa’s number, not the identified Maui solo.','We Know the Way is the voyaging song, not this self-introducing Maui number.'],
 'We Know the Way also concerns ancestors, but the requested Maui number is specifically identified by its performer and original-song title; end-credits vocals are a separate rendition.',
 'Distinct from 2547’s Jordan Fisher end-credits duet attribution and 699’s Moana solo.')
review(450,'unknown unknowncast','Original English Frozen 2 Elsa vocals, not a pop cover or other language dub.',
 'The soundtrack credits Menzel/AURORA; production notes identify Menzel as Elsa.',
 ['Idina Menzel is Elsa’s credited vocalist.','Celine Dion is not in the track’s performer list.','Demi Lovato is not in this track’s performer list.','Adele is not in the performer list.'],
 'AURORA also sings on the track but is not Elsa and is not a listed alternative. Earlier Lovato Frozen cover does not establish an Elsa credit here.',
 '701 tests a different song; 2544 tests the Panic! end-credits cover.')
review(451,'eltonalbum eltondisney','Pop recordings on the 1994 album; distinguish film-scene vocals.',
 'The artist tracklist and Disney biography both assign the separate soundtrack pop recordings to Elton John.',
 ['Elton John is credited on both pop tracks.','Phil Collins is not their credited singer.','Hans Zimmer’s score role is not these pop-vocal credits.','Lebo M’s film vocal/arrangement contribution is not the separate Elton pop recordings.'],
 'Lebo M is a serious competing answer under vague film-performance wording. Explicit pop-version album scope excludes him without denying his real contribution.',
 '709 asks songwriters, not the pop vocalist; 164 asks original film opening vocals.')
review(453,'oscars1995','1994 animated Lion King orchestral score and 1995 ceremony.',
 'The Academy credits the Original Score win to Hans Zimmer.',
 ['Hans Zimmer is the listed score winner.','Alan Menken is not the film’s credited score winner.','Elton John wrote songs but is not this score winner.','John Williams is not the credited score winner.'],
 'Song composition is distinct from score composition; John’s Song win cannot satisfy the score credit.',
 'Distinct from retained 458’s Song winner and 451’s pop recordings.')
review(456,'encantosongs','Eight original songs in the 2021 film; excludes orchestral score.',
 'Disney’s complete music credit gives eight original songs by Miranda and a separate Franco score.',
 ['Miranda is the credited original songwriter.','Menken is not the songwriter in this credit.','The Sherman Brothers are not the credited writers.','Elton John is not the credited writer.'],
 'Franco’s score does not contradict the original-song credit. Eight original songs avoids overclaiming all incidental or background music.',
 'Distinct from 2549’s score-composer milestone and 446’s particular song association.')
review(457,'savages','Savages as a song title on the original Pocahontas film soundtrack.',
 'The label-distributed track is explicitly linked to Pocahontas music from the motion picture.',
 ['Pocahontas is the credited film.','Mulan is not this recording’s film attribution.','Hunchback is not its film attribution despite shared Disney performers.','Tarzan is not its film attribution.'],
 'Artist recommendation links on a music page are not film credits. Specific track/album attribution, not thematic similarity, supports one answer.',
 '1382 tests a different song; 2284 tests an Oscar outcome, not Savages.')
review(458,'oscars1995','Original Song winner for 1994 Lion King at the 1995 Oscars.',
 'The Academy distinguishes the winning song from the other Lion King nominees.',
 ['Can You Feel the Love Tonight is marked winner.','Hakuna Matata is a nominee, not the winner.','Circle of Life is a nominee, not the winner.','Be Prepared is not the winning song or a nominee in the complete category.'],
 'All are real film songs. Being Oscar-nominated is insufficient: the winner designation singles out the first answer.',
 'Necessary authentic title length; shortening only the winner would distort it. Different from q718’s 1993 Aladdin winner and q2551’s nomination count.')
review(459,'beautysinger','Original 1991 in-story ballroom rendition; not the end-credits duet or remake.',
 'The archive distinguishes Lansbury’s in-story title song from the pop duet and maps her to Mrs. Potts.',
 ['Mrs. Potts is the singer voiced by Lansbury.','Belle dances but does not perform this ballroom rendition.','Lumiere’s voice credit is Jerry Orbach, not the identified singer.','The Beast dances but is not the identified title-song vocalist.'],
 'The two dancing characters can be mistaken for the singers. The original film and in-story scope excludes the duet and later Emma Thompson rendition.',
 '2538 asks the pop duet; the in-film singer is a separate performance fact. Parallel character-only answers remove the actor parenthesis clue.')
review(460,'jungleprofiles junglelist','Original 1967 King Louie featured number.',
 'Disney’s character profile explicitly identifies King Louie’s Prima performance as I Wanna Be Like You.',
 ['I Wanna Be Like You is Louie’s named featured number.','The Bare Necessities introduces Baloo, not Louie.','Trust in Me is Kaa’s hypnotic song, not Louie’s featured number.','That’s What Friends Are For is the vultures’ friendship number, not Louie’s.'],
 'Other songs are from the same film and stylistic labels alone would be weak. The performer/character attribution isolates the answer; corrected Bare spelling makes the distractor genuine.',
 '814/1331 test the secret of fire, not the song title.')
review(461,'moanacredits moanacreator','Original songs for animated Moana (2016), not the 2026 remake.',
 'Publisher and creator list Miranda, Foaʻi and Mancina as original-song collaborators.',
 ['Foaʻi is in the original-song team.','Elton John is absent from the complete songwriting credit.','Howard Ashman is absent from that team.','Alan Menken is absent from that team.'],
 'Mancina also co-wrote songs, so he cannot be a distractor. The final list removes him and explicitly asks which of these; all three wrong names are excluded by the complete team credit.',
 'The replacement resolves genuine multiple-answer ambiguity, rather than changing the designated answer.')
review(462,'oscars2000 tarzan','2000 ceremony award to the 1999 Tarzan song.',
 'The Academy lists Tarzan’s only nomination/win as Original Song for Collins’s song.',
 ['Original Song is the recorded award.','Original Score went to The Red Violin, not this song.','Sound is not the category of Tarzan’s sole win.','Animated Short is not the category of this song’s win.'],
 'The film’s award list is exhaustive; soundtrack albums and pop song awards are not Oscar categories. Replaced those invented choices with real categories and set medium.',
 'Different song/event from 466; sharing an award category does not repeat a fact.')
review(463,'oscars1992','Ceremony year of the original title song’s Oscar, not film release year.',
 'The Academy’s 1992 ceremony page records Beauty and the Beast’s Original Song win.',
 ['1992 is the ceremony year.','1990 precedes the film and recorded win.','1994 is two ceremonies later.','1988 precedes the film and recorded win.'],
 '1991 is the film release year, not an offered alternative; the dated official ceremony fixes the requested award year uniquely.',
 'Distinct from 718’s Aladdin song winning in 1993.')
review(466,'oscars2014','The Let It Go song’s 2014 award, not Frozen’s separate film award.',
 'The Academy assigns Let It Go to Original Song and Frozen separately to Animated Feature.',
 ['Original Song is the track’s win.','Original Score is not the song’s category.','Animated Feature belongs to the film, not Let It Go.','Original Screenplay is not a recorded Frozen win.'],
 'Frozen did win Animated Feature, so the subject song is essential to uniqueness. Literal wording clearly asks the song’s category.',
 'Medium suits common song-award recognition; separate from q462’s Tarzan award.')
review(468,'ashman ashmanloc oscars1992','Lyricist partnership across the 1991/1992 animated films.',
 'Disney biography names Ashman’s lyricist role and both films; the Academy credits his Beast lyrics and LOC distinguishes Rice’s later Aladdin work.',
 ['Ashman matches both film collaborations.','Rice contributed to Aladdin after Ashman, but not to the identified original Beauty and the Beast songs.','Sondheim is not the lyricist identified for these films.','Hamlisch is not the lyricist identified for these films.'],
 'Ashman was not the music composer and did not write all Aladdin lyrics. Final wording says lyricist, collaborated and songs, allowing Rice’s later contributions.',
 'Removed the death-date clue, which overlapped 1392’s completion biography. The retained fact is the lyricist collaboration on both named films, distinct from 703’s Little Mermaid credit. No claim that these were his only films.')
review(470,'dory','Finding Dory’s beluga character.',
 'Pixar explicitly assigns different species to all four named options.',
 ['Bailey is the beluga.','Destiny is a whale shark.','Hank is an octopus.','Fluke is a sea lion.'],
 'Whale shark contains whale but is not a beluga; the four character profiles positively establish all distinct species.',
 '481 asks Destiny’s species; 494 asks Hank’s name; no repeated Bailey identity fact.')
review(471,'inside2','New emotion’s planning behavior in Inside Out 2.',
 'Pixar describes Anxiety as preparing negative outcomes and pushing Riley to fit in.',
 ['Anxiety matches both planning and fitting-in behavior.','Envy covets others’ possessions and attributes rather than this protective planning role.','Pride is not the named new emotion with this role.','Nostalgia is not the emotion identified with anticipatory planning.'],
 'Several emotions are new; subjective main focus wording was insufficient. The precise behavioral profile excludes the competing new emotions.',
 '1416 tests the Sense of Self and 1417 tests what happens to old emotions; this asks the defining planning role.')
review(472,'luca soul red onward','Sea monsters concealing themselves during an Italian summer, not discovering their species.',
 'Pixar’s synopsis and both boys’ profiles establish the exact paired identity and setting.',
 ['Luca has the two sea-monster friends in an Italian town.','Soul follows Joe’s jazz/spiritual story, not that identified pair.','Turning Red follows Mei’s panda transformation, not sea monsters.','Onward follows elf brothers, not sea monsters.'],
 'Luca knows his nature from birth; his discovery is the human world. Final wording removes the false reveal and asks the distinctive two-boy premise.',
 '497 asks wet-triggered transformation; 781 asks town name, not film premise.')
review(473,'red','Mei’s emotional transformation in Turning Red.',
 'Pixar explicitly states excitement produces a giant red panda.',
 ['Giant red panda is the specified transformation.','A red fox is a different animal from the documented panda.','A red dragon is not that transformation.','A red wolf is not that transformation.'],
 'The red color alone is insufficient; all options preserve it and only one has the correct animal. Emotional trigger and character are explicit.',
 '1405 tests Mei’s final choice, not her transformed species.')
review(474,'onward','Species of both Lightfoot brothers in Onward.',
 'Pixar calls them two teenage elf brothers.',
 ['Elves directly matches their species.','Dwarves are not the documented brother species.','Centaurs exist in the world but are not these brothers.','Fauns are not their documented species.'],
 'A mixed-species fantasy setting does not make every creature type true for Ian and Barley; both are specifically identified as elves.',
 'Distinct from van, mother, spell, town and voice-actor questions.')
review(477,'sulley monsters','Large blue furry protagonist in original Monsters, Inc.',
 'Disney’s specific physical description identifies Sulley, while Pixar supplies his complete name and distinct colleagues.',
 ['Sulley is the described blue furry protagonist.','Mike is his separate assistant, not the described character.','Randall is the separate rival, not that furry protagonist.','Roz is the separate administrator, not that protagonist.'],
 'Randall’s camouflage does not make him the large furry blue character named by Disney; the description identifies an individual rather than all things capable of looking blue.',
 '178 asks one-eyed green Mike; 292 asks Boo’s nickname, both different identity facts.')
review(479,'nemoaddress nemomask','Street address and city remembered by Dory, from the mask scene.',
 'Disney reproduces the exact address as 42 Wallaby Way, Sydney.',
 ['42 Wallaby Way, Sydney matches the quoted address.','Brisbane changes the documented city.','123 Shark Lane changes both number and street.','42 Coral Road changes the street.'],
 'P. Sherman is an addressee/name rather than part of the street address. Removing that prefix equalizes option style; the city alone does not distinguish all choices.',
 '173 gives Sydney dentist-tank location but not the street or number; medium suits exact address recall.')
review(480,'inside2','Ennui’s boredom and phone-console behavior.',
 'Pixar identifies Ennui as bored and operating the console remotely via mobile app.',
 ['Ennui has both specified attributes.','Anxiety is the future-planning emotion, not the documented boredom role.','Nostalgia is not the identified app-using boredom emotion.','Envy’s covetous role differs from the documented apathy.'],
 'Removed the false monocle condition. The conjunction of boredom and app control positively identifies Ennui instead of relying on absent accessories in a synopsis.',
 'Distinct from 1047’s teal Envy, 1297’s pink Embarrassment and 471’s planning behavior.')
review(481,'dory','Destiny’s species in Finding Dory.',
 'Pixar repeatedly calls Destiny a whale shark, contrasting her with Bailey’s beluga species.',
 ['A whale shark is Destiny’s stated species.','Beluga whale describes Bailey, not Destiny.','Blue whale is not her documented species.','Hammerhead shark is not her documented species.'],
 'Speaking whale and the word whale in her name do not make her a cetacean; exact species attribution excludes all other species.',
 '1036 tests Hank’s species; 470 tests Bailey’s name. Species of a different character is a new fact.')

qs={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
planned=json.loads((ROOT/'audit/runs/next-shard-0009-plan.json').read_text())['questionIds']
assert set(rows)=={i for i in planned if i in qs}, sorted(set(rows)^{i for i in planned if i in qs})
notes={'schema':1,'reviewer':'Codex','at':AT,'sourcesChecked':sorted({'b9-'+s for r in rows.values() for s in r[0]}),'reviews':[]}
for qid,(keys,context,premise,reasons,challenge,editorial,bases) in rows.items():
    keys=['b9-'+s for s in keys]
    mutable=any(library['sources'][s]['timeSensitive'] for s in keys)
    notes['reviews'].append(dict(questionId=qid,hash=digest(qs[qid]),checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],notes=editorial,context=context,timeSensitive=mutable,nextReviewAt=DUE if mutable else None,premise={'reason':premise,'sources':keys},options=[{'basis':(bases or ['direct','exclusive-inference','exclusive-inference','exclusive-inference'])[i],'reason':r,'sources':keys} for i,r in enumerate(reasons)],challenge={'reviewer':'Codex','at':AT,'premiseChecked':True,'alternativesExcluded':True,'notes':challenge}))
(ROOT/'audit/source-notes.json').write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'audit/runs/next-shard-0009-evidence-notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Authored {len(rows)} individually challenged reviews.')
