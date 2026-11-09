"""Codex's explicit batch 32 evidence authoring; never edits question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = '2026-11-08'
libpath = ROOT / 'audit/source-notes.json'
lib = json.loads(libpath.read_text(encoding='utf-8'))
sources = lib['sources']
PRIMARY = 'Institutional text inspected; no film, audio, or video playback claimed.'
SECONDARY = 'Detailed secondary text inspected; primary scene evidence was unavailable. Corroborating passages are identified separately. No film playback or studio-certified transcript claimed.'

def S(key, url, locator, evidence, limitation=PRIMARY):
    sources['b32-'+key] = dict(url=url, locator=locator, evidence=evidence, checkedBy='Codex', checkedAt=DATE,
        timeSensitive=False, nextReviewAt=None, limitations=limitation, topics=['Batch 32'])

S('swiss-bombs','https://www.springfieldspringfield.co.uk/movie_script.php?movie=swiss-family-robinson',
  'Francis tests coconut bombs, lines 1248-1254; pirate battle lines 1562-1573',
  'The family calls for coconut bombs during the pirate attack; Francis previously reports that the bombs work.',SECONDARY)
S('swiss-bombs-cor','https://www.popularmechanics.com/culture/web/a24442/coconut-grenade-explosion/',
  'Darren Orf, opening paragraph, line 286', 'The article identifies coconut grenades as an idea popularized by the 1960 Swiss Family Robinson film.',SECONDARY)
S('swiss-home','https://d23.com/a-to-z/swiss-family-robinson-film/',
  'Synopsis and treehouse paragraph, lines 87 and 91', 'The Robinsons salvage their ship and build a home in a huge tree; Disney calls the movie home a treehouse.')
S('fantasia','https://catalog.afi.com/Film/27633-FANTASIA',
  'History opening, lines 46/52; Fantasound exhibition restrictions, lines 85-89',
  'Concert Feature was the working title. Wartime material shortages hindered the expensive sound installations, and war cut off European markets.')
S('fantasia-cor','https://d23.com/15-fascinating-facts-about-fantasia/',
  'Item 11, line 120', 'War and rationing of electronic equipment for Fantasound prevented recovery of the film costs at the box office.')
S('soarin','https://d23.com/a-to-z/soarin-over-california-film/',
  'Attraction title and opening date, line 89', 'Soarin Over California opened at Disney California Adventure on February 8, 2001.')
S('mineral','https://d23.com/a-to-z/country-bear-jamboree/',
  'Original attraction history, line 88', 'Country Bear Jamboree was originally designed for the planned Mineral King ski resort.')
S('bears-songs','https://en.wikipedia.org/wiki/Country_Bear_Jamboree',
  'Songs > Walt Disney World 2012-2024, lines 309-320',
  'Big Al sings Blood on the Saddle; Liver Lips sings My Woman Aint Pretty, Henry sings Mama Dont Whip Little Buford with Wendell, and Teddi Barra sings Heart We Did All That We Could.',SECONDARY)
S('bears-songs-cor','https://www.themickeywiki.com/index.php/Country_Bear_Jamboree',
  'Show Plot > Blood On The Saddle and The Ballad of Davy Crockett/Ole Slew-Foot',
  'Big Al performs Blood on the Saddle and continues during the ensemble finale; Henry leads Davy Crockett.',SECONDARY)
S('moana-island','https://lumiere-a.akamaihd.net/v1/documents/moana_2_production_notes_final_11-18-24_c0d3a1c0.pdf',
  'Printed pp.2 and 19-20, Motufetu location profile',
  'Motufetu is the cursed, sunken meeting island Moana seeks to reconnect Pacific peoples; Motunui is her home.')
S('moana-matangi','https://lumiere-a.akamaihd.net/v1/documents/moana_2_production_notes_final_11-18-24_c0d3a1c0.pdf',
  'Printed pp.14-15, Matangi profile',
  'Nalo placed Matangi to prevent access to Motufetu; she wants freedom, surrounds herself with flying foxes, and teaches Moana through Get Lost.')
S('moana-plot','https://en.wikipedia.org/wiki/Moana_2',
  'Plot: Matangi captivity and her helping Moana; post-credits scene; Voice cast',
  'Matangi holds Maui for Nalo but helps Moana escape; Nalo later confronts her. Tamatoa is the giant crab; Kakamora are coconut-armored pirates.',SECONDARY)
S('aladdin','https://imsdb.com/scripts/Aladdin.html',
  'Cave entry qualification, lines 136-152; forbidden ruby and escape, lines 973-1039',
  'The cave calls its worthy entrant a diamond in the rough. Abu takes the ruby; water and shrine become lava, debris falls, and the group survives inside the sealed cave.',SECONDARY)
S('aladdin-cor','https://en.wikipedia.org/wiki/Aladdin_(1992_Disney_film)',
  'Plot: cave entry and Abu touching treasure',
  'Aladdin is the diamond in the rough; Abu takes a forbidden jewel, the cave collapses, and the trapped Aladdin later summons Genie.',SECONDARY)
S('olaf','https://www.springfieldspringfield.co.uk/movie_script.php?movie=olafs-frozen-adventure',
  'Family-tradition conversation lines 199-237; townswoman in tradition montage lines 286-290',
  'The sisters believe they have no family tradition. Olaf searches. A townswoman describes a large Norway-shaped cookie; later Olaf is recognized as their tradition.',SECONDARY)
S('olaf-cor','https://en.wikipedia.org/wiki/Olaf%27s_Frozen_Adventure',
  'Plot, lines 184-190', 'The sisters initially think they lack personal holiday traditions, then recognize their annual Olaf gifts as one.',SECONDARY)
S('cookie','https://books.disney.com/book/disney-frozen-the-official-cookbook-a-culinary-journey-through-arendelle/',
  'Publisher description, line 15', 'Disney lists a large Norway-shaped cookie among the Arendelle-inspired recipes.')
S('kanga','https://characters.disney.com/winnie-the-pooh/kanga-and-roo',
  'Character profile, line 44', 'Kanga is the protective mother of Roo, her young son.')
S('owl','https://characters.disney.com/winnie-the-pooh/owl',
  'Character profile, line 44', 'Owl is the know-it-all whose friends seek his advice even though it often misses the mark.')
S('groove','https://www.springfieldspringfield.co.uk/movie_script.php?movie=emperors-new-groove-the',
  'Dinner aftermath, lines 686-701', 'Yzma identifies the vial as extract of llama rather than poison; Kronk says her poisons look alike.',SECONDARY)
S('groove-cor','https://en.wikipedia.org/wiki/The_Emperor%27s_New_Groove',
  'Plot: poisoned dinner', 'The attempted poisoning accidentally uses a llama potion, changing Kuzco instead of killing him.',SECONDARY)
S('tangled','https://en.wikipedia.org/wiki/Tangled',
  'Plot, lines 264-265', 'Eugene cuts Rapunzel hair, which becomes brown and loses its magic. A tear from Rapunzel subsequently revives him.',SECONDARY)
S('tangled-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=tangled',
  'Campfire explanation of cut hair; final tower sequence, immediately before ending narration',
  'Rapunzel explains that cut hair turns brown and loses its power; the final revival follows her crying over Eugene, not Gothel administering medicine.',SECONDARY)
S('bambi-models','https://d23.com/the-lots-own-animal-kingdom/',
  'Live models, lines 74-77', 'The studio kept fawns Bambi and Faline courtesy of Maine for animation study.')
S('bambi-history','https://catalog.afi.com/Film/27130-BAMBI',
  'History, line 53; Synopsis lines 1008-1014',
  'Maine sent the two fawns. Bambi mother calls the danger Man; hunters campfire starts the fire. Spring courtship follows the winter, and the ending introduces new fawns.')
S('bambi-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=bambi',
  'Clover scene lines 241-252; danger line 287; ice scene lines 294-299; spring return after winter',
  'Mother prompts Thumper to recall his father advice about greens; Thumper recites it. Bambi mother names Man; Thumper describes the water as stiff.',SECONDARY)
S('bambi-ice','https://movies.disney.com/bambi/',
  'Official synopsis, line 64', 'Bambi and Thumper adventures include skating on stiff water.')
S('smokey','https://smokeybear.com/smokey-through-the-years',
  'Opening campaign history line 56; Before Smokey archive entry lines 1259-1266',
  'The campaign used a Bambi poster before Smokey; Smokey first appeared on campaign posters in 1944.')
S('bambi-zoo','https://mouseplanet.com/bambi-fun-fawn-facts/6059/',
  'Jim Korkis: live models, lines 43-44',
  'The Maine model fawns grew to adulthood and were donated to Griffith Park Zoo in 1942.',
  'Specialist Disney historian; no original donation record accessible. Corroborated with Todd James Pierce history of the zoo.')
S('bambi-zoo-cor','https://disney685.rssing.com/chan-7158667/all_p5.html',
  'Todd James Pierce, Walt Disney and the Griffith Park Zoo, June 22 2014, paragraph beginning The Griffith Park Zoo existed',
  'After Bambi was finished, the studio donated its two New England fawns to Griffith Park Zoo for public display.',
  'RSS republication of a named Disney historian article; compared with Korkis, not an original zoo accession record.')
S('brother-production','https://d23.com/a-to-z/brother-bear-film/brother-bear-1180w-600h/',
  'Production paragraphs, lines 62-63', 'Brother Bear was made at the Florida feature animation studio, used Cinemascope after the transformation, and had working title Bears.')
S('brother-ratio','https://cartoonresearch.com/index.php/in-their-own-words-the-directors-of-brother-bear/',
  'Jim Korkis introduction to September 2003 filmmaker presentation, lines 50-53',
  'The Florida-produced film widens its aspect ratio after Kenai transforms, representing his changed perception.',
  'Eyewitness historian account of a filmmaker presentation; ratios differ slightly between descriptions, so no numerical ratio is asked.')
S('brother-plot','https://en.wikipedia.org/wiki/Brother_Bear',
  'Plot, lines 253-259; Production > Development, line 289',
  'Kenai kills the bear later revealed as Koda mother. The spirits are sought at the mountain where lights touch earth. Production was primarily in Orlando.',SECONDARY)
S('brother-dialogue','https://www.springfieldspringfield.co.uk/movie_script.php?movie=brother-bear',
  'Opening narration lines 13-28; Tanana names mountain lines 149-152; Koda mother story and Kenai confession',
  'Ancestral spirits are identified with dancing sky lights. Tanana names their mountain. Koda describes his mother fighting the brothers, revealing the bear Kenai killed.',SECONDARY)
S('herc-design','https://www.filmeducation.org/pdf/film/hercules.pdf',
  'Film synopsis, PDF p.2; Animation PDF p.16', 'The official Buena Vista education guide identifies Gerald Scarfe original drawings and computer animation for the Hydra.')
S('herc-muses','https://animatedviews.com/2017/2017-d23-expo-exclusive/',
  'Zero to Hero panel section: Musker persuading Menken about gospel; Goldberg mouth reference',
  'Musker explains the gospel approach; Goldberg describes DeVito distinctive mouth configuration used in Phil animation.',
  'First-person event report of filmmakers discussing their work; no panel video playback claimed.')
S('herc-mouth','https://mouseinfo.com/2017/07/zero-to-hero-the-making-of-hercules-panel-at-d23expo/',
  'Eric Goldberg discussion, line 40', 'Goldberg specifically describes DeVito unusual mouth shapes as reference for Phil.',
  'Independent reporter account quoting the supervising animator at the 2017 D23 panel, compared with Animated Views.')
S('herc-cloud','https://www.springfieldspringfield.co.uk/movie_script.php?movie=hercules-1997',
  'Zeus creates baby Pegasus, lines 77-82', 'Zeus combines cirrus, nimbostratus and cumulus to create Pegasus.',SECONDARY)
S('herc-transcription','https://copioni.corrierespettacolo.it/wp-content/uploads/2016/12/WALT%20DISNEY__Hercules__inglese__null__Per%20ragazzi__0.pdf',
  'PDF p.3 Pegasus direction; PDF p.15 first Hydra decapitation',
  'Zeus shapes a cloud into Pegasus. After the Hydra original head is cut off, three new heads emerge.',
  'Unofficial scene transcription explicitly disclaims official-script status; compared with dialogue, institutional production context and separate detailed character synopsis.')
S('herc-hydra-cor','https://en.wikipedia.org/wiki/List_of_Disney%27s_Hercules_characters',
  'Hercules > In Hercules, lines 176-177; Creatures > Hydra, lines 518-519',
  'After Hercules cuts his way out of the Hydra by decapitating its first head, three heads sprout from the wound.',SECONDARY)
S('fox-production','https://d23.com/a-to-z/fox-and-the-hound-the-film/',
  'Production history lines 91-93; synopsis line 88',
  'Don Bluth and fellow animators left to establish a studio, delaying production. Vixey is the female fox Tod falls in love with at the preserve.')
S('fox-cost','https://en.wikipedia.org/wiki/The_Fox_and_the_Hound',
  'Budget and release discussion, lines 302 and 311; Animation lines 349-353',
  'The 1981 production cost about $12 million. The newer animation team included Lasseter, Burton, Bird, Buck and Musker.',SECONDARY)
S('fox-cost-cor','https://the-avocado.org/2018/01/16/building-entertainment-the-animated-films-of-the-walt-disney-studio-the-fox-and-the-hound/',
  'Budget line 18; Animation line 55', 'The historical film discussion gives a $12 million budget and includes Lasseter in the animation team.',
  'Secondary film-history account compared with Wikipedia. No accessible studio cost ledger was found; the approximate nominal cost is asked, without a superlative.')
S('vixey-keane','https://www.aimeemajor.com/anim/dkeane.html',
  'Didier Ghez interview with Glen Keane, May 2 1997, Tim Burton discussion lines 162-166',
  'Keane remembers Burton working with him animating Vixey, while Chris Buck occupied the next room.',
  'Primary participant interview reprinted with interviewer permission; exact assignment corroborated with John Musker interview.')
S('vixey-musker','https://www.awn.com/animationworld/conversation-john-musker',
  'March 30 2022 interview, line 84', 'John Musker recalls Tim Burton animating Vixey.', 'Primary participant interview.')
S('lasseter','https://d23.com/a-to-z/lasseter-john/',
  'Biography, line 90', 'John Lasseter became Pixar and Disney Animation chief creative officer in 2006 and left in 2018.')
S('soul-hands','https://news.disney.com/music-for-soul',
  'Animation performance reference, lines 84-85', 'Animators filmed Jon Batiste hands at the piano and used the reference to animate Joe frame by frame.')
S('soul-credits','https://movies.disney.com/soul',
  'Synopsis and filmmaker credits', 'Jamie Foxx voices Joe Gardner, Tina Fey voices 22, and Kemp Powers co-directs with Pete Docter.')
S('soul-city','https://www.pixar.com/soul',
  'Opening synopsis, lines 53-54', 'Joe Gardner is a New York City middle-school music teacher who enters the Great Before.')
S('soul-scientist','https://lumiere-a.akamaihd.net/v1/documents/soul_359d96b2.pdf',
  'Printed p.21, Docter explains choice of passion, lines 741-744', 'Docter says they considered a scientist or businessman before finding a jazz musician example.')
S('soul-score','https://lumiere-a.akamaihd.net/v1/documents/soul_359d96b2.pdf',
  'Printed pp.21-23, Batiste then Reznor/Ross sections', 'Batiste supplies jazz; Reznor and Ross create the otherworldly score using synthesizers treated like orchestral instruments.')
S('onward','https://www.pixar.com/onward',
  'Unicorns lines 165-167; Homes lines 197-199', 'New Mushroomton is the suburban town; its unicorns scavenge in garbage bins, while dragons have become house pets.')
S('tangled-keane','https://www.fatguysatthemovies.com/animator-glen-keane-talks-tangled/',
  'Glen Keane interview: brown hair lines 74-75; healing tear lines 97-99 and 122-124',
  'Keane explains that brown hair shows loss of hair power, while Rapunzel tear heals Flynn in the finale.',
  'Primary participant interview; scene interpretation corroborated with the detailed film plot.')
S('herc-gospel','https://d23.com/theres-no-chance-no-way-you-can-miss-out-on-these-d23-exclusive-hercules-pins/',
  'Film retrospective paragraph, line 63', 'Disney identifies gospel music and the Muses as the Greek chorus of the 1997 film.')

template=json.loads((ROOT/'audit/runs/next-shard-0032-final-template.json').read_text(encoding='utf-8'))
reviews={r['questionId']:r for r in template['reviews']}
CHECKS=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
def R(i, keys, context, premise, reasons, challenge, note=''):
    r=reviews[i]
    keys=['b32-'+k for k in keys.split()]
    assert len(reasons)==4
    r.update(checks=CHECKS,notes=note or 'Final question and four options reviewed; topic context and cross-bank fact distinctness checked.',context=context,timeSensitive=False,nextReviewAt=None)
    r['premise']={'reason':premise,'sources':keys}
    r['options']=[{'basis':'direct' if j==0 else 'exclusive-inference','reason':reason,'sources':keys} for j,reason in enumerate(reasons)]
    r['challenge']=dict(reviewer='Codex',at=DATE,premiseChecked=True,alternativesExcluded=True,notes=challenge)

R(2118,'swiss-bombs swiss-bombs-cor','Disney live-action film, 1960; final pirate battle.',
  'The dialogue names the improvised weapons used during the attack.',
  ['The family explicitly calls for coconut bombs.','Clay firepots are not the named thrown bombs.','Bottled firebombs are not the coconut-shell weapons identified.','Exploding gourds are a different container from the coconuts described.'],
  'Removed gunpowder/fuse clue and compared four explosive containers. The evidence identifies coconuts, excluding clay, bottles and gourds; other traps in the battle do not answer this revised question.')
R(2119,'swiss-home','Swiss Family Robinson, 1960; island home.',
  'Disney identifies the family home as built in a huge tree.',
  ['A treehouse is the elevated family home.','A stone tower is not a home built in a huge tree.','A stilt house stands on posts rather than in the tree.','A cliffside cabin is not the tree home in the official account.'],
  'Removed the tree-in-stem giveaway and unneeded skylight/plumbing claims. All four choices describe homes; only the treehouse matches. Park attraction #923 asks the attraction identity, a separate real-world fact.')
R(2120,'fantasia fantasia-cor','Fantasia initial 1940-1941 exhibition; historical causes, no bankruptcy magnitude claimed.',
  'Institutional histories identify costly installations, rationing and closed European markets.',
  ['Wartime losses and sound equipment costs are specifically documented.','The histories describe theatrical runs, contradicting a nationwide animation ban.','Multiple exhibition prints and roadshows contradict destruction of the sole finished print.','Ticketed roadshow engagements contradict a decision to exhibit the film free.'],
  'Checked causes against actual exhibition history; removed near-bankruptcy hyperbole. These are explanatory alternatives, and the sources positively establish the cost/war account.')
R(2121,'fantasia','Fantasia development before release in 1940.',
  'AFI names the project working title in the opening history.',
  ['Concert Feature is the working title in AFI.','Music Land is not the title identified for this project.','The Symphony Hour is not the working title identified.','Melody Parade is not the documented working title.'],
  'Replaced an undated inflation-dollar loss estimate with the documented working title. Naming the sound system in #937 does not reveal this development name.')
R(2122,'soarin','Disney California Adventure opening attraction in 2001, not EPCOT opening.',
  'The dated Disney entry identifies the original California attraction title.',
  ['Soarin Over California is the opening title.','Soarin Over the World is not its 2001 title.','Ultra Flight is not the published opening title.','California Skyway is not the published title.'],
  'Removed the conflation with EPCOT. The title is tied to California Adventure in 2001; later global/America versions do not alter it. #597 asks the 2016 global version, not this title.')
R(2123,'mineral','Proposed Mineral King resort and later Magic Kingdom attraction.',
  'Disney explicitly identifies the intended ski-resort show.',
  ['Country Bear Jamboree was designed for Mineral King.','The Enchanted Tiki Room is not the Mineral King bear show.','The Haunted Mansion is not the show named in the resort history.','Its a Small World is not the proposed bear entertainment.'],
  'Removed the unnecessary last-Walt-project claim. The resort origin belongs to the bear show; park location question #1138 requires another fact.')
R(2124,'bears-songs bears-songs-cor','Original Country Bear Jamboree at Magic Kingdom, before its 2024 replacement.',
  'Two detailed song/performer listings identify the historical soloist.',
  ['Big Al sings Blood on the Saddle.','Liver Lips has My Woman Aint Pretty in that version.','Henry leads other numbers including Davy Crockett.','Teddi Barra sings Heart We Did All That We Could.'],
  'The dated original-show wording avoids treating the 2024 Musical Jamboree as unchanged. The complete song assignments exclude all three other bears, without relying on a subjective tone-deaf description.')
R(2125,'moana-island','Moana 2, 2024; island sought to break Nalo curse.',
  'The studio production notes distinguish the lost meeting island from Moana home.',
  ['Motufetu is the sunken meeting island.','Motunui is the home island, not the lost meeting place.','Lalotai is the first film monster realm, not this island.','Te Fiti is the island goddess/location from the earlier heart quest, not Motufetu.'],
  'Checked the island profile and original Moana topic context; all are proper place names but only Motufetu matches this second-film quest.')
R(2126,'moana-matangi moana-plot','Moana 2; Matangi captivity, escape assistance and credits scene.',
  'The notes identify Nalo placement of Matangi; plot corroborates her assistance.',
  ['Matangi is the enforcer who helps Moana escape.','Tamatoa is the crab, not this bat-associated enforcer.','Te Ka is the earlier lava antagonist, not Matangi.','Kakamora are coconut-armored pirates, not this individual enforcer.'],
  'Matangi helping Moana does not mean she was freely independent of Nalo; the notes and credits consequence support both parts of the premise. Kakamora assistance is a different event and role.')
R(2127,'aladdin aladdin-cor','Aladdin animated 1992; cave qualification.',
  'The cave uses a specific phrase for its worthy entrant.',
  ['A diamond in the rough is its stated description.','A prince among men is not that phrase.','A hero of Agrabah is not that phrase.','A child of destiny is not that phrase.'],
  'Entry permission does not grant permission to take treasures. Removed claim its entrant can claim all treasure; checked exact spoken description against all alternatives.')
R(2128,'aladdin aladdin-cor','Aladdin animated 1992; Abu ruby incident.',
  'The scene directions describe lava and collapse after the forbidden ruby is taken.',
  ['The water and shrine become lava while debris falls.','Treasure becoming sand is not the described effect.','The guardian becoming a dragon is not the described event.','Frozen walls contradict the lava-filled escape.'],
  'Original wording conflated who may enter with who may touch treasure and falsely asserted burial alive. All survive; final choices ask observed cave behavior, not the warning that they will never leave.')
R(2129,'olaf olaf-cor','Olafs Frozen Adventure, 2017 short; initial belief before the ending reveal.',
  'The sisters initially believe they lack a personal family tradition.',
  ['They think they lack family holiday traditions.','Lack of a proper tree is not what prompts the search.','A family portrait is not the missing custom they discuss.','A royal Christmas ball is not the perceived lack; they have already planned a party.'],
  'The ending shows Olaf was their tradition, so never had was false as an absolute. The final question asks their initial belief. Read the short-film topic context and kept secondary-title coverage modest.')
R(2130,'olaf cookie','Olafs Frozen Adventure, 2017; town tradition montage.',
  'The townswoman describes one distinctive baked treat; Disney cookbook corroborates it.',
  ['She describes a large Norway-shaped cookie.','Gingerbread castles are not her described treat.','Snowflake pastries are not the named shape/type.','An ice-palace cake is not the Norway-shaped cookie.'],
  'Removed the Norwegian-roots hint; all four are baked novelties. The source names both cookie and shape, and does not merely describe Scandinavian food generally.')
R(2131,'kanga','Disney Winnie the Pooh character relationships.',
  'Disney character profile directly calls Roo Kanga son.',
  ['Kanga is his mother.','She is not his sister.','She is not his aunt.','She is not his grandmother.'],
  'Motherhood is explicitly named, excluding the other generations/relationships. Replaced the long correct choice and unsupported adoption alternative with parallel family roles. Roo species #2373 requires a different fact.')
R(2132,'owl','Disney Winnie the Pooh recurring characterization, not a TV episode.',
  'Disney character profile identifies Owl as the know-it-all adviser.',
  ['Owl is that adviser.','Tigger is the energetic tiger, not the described adviser.','Piglet is the timid pig, not that know-it-all.','Eeyore is the gloomy donkey, not that adviser.'],
  'Rabbit could overlap with a generic know-it-all prompt, so replaced him with a clearer distractor and retained the source-specific advice characterization. No species inference is needed from the stem.')
R(2133,'groove groove-cor','The Emperors New Groove, 2000; botched palace dinner.',
  'Yzma identifies the used vial as extract of llama, and Kronk cites look-alike vials.',
  ['Kronk uses the wrong vial, extract of llama.','His later moral hesitation is not why the dinner potion changes Kuzco.','A flawed recipe is not the error: the used vial contains a different potion.','Kuzco does not switch vials; the exchange identifies the mistaken vial on Kronk side.'],
  'Distinguished the dosing mistake from Kronk later conscience struggle in #1426. Yzma poor labeling helps explain his error but is not a recipe defect. #530 names the resulting animal; this asks the cause.')
R(2134,'tangled tangled-keane','Tangled theatrical 2010 finale, after hair-cutting.',
  'The revival is attributed to Rapunzel tear after the hair loses power.',
  ['A tear from Rapunzel carries the healing magic.','A kiss is not the mechanism identified in the account.','Gothel provides no revival potion and is already gone.','Pascal performs no revival spell.'],
  'Replaced the Pascal snake event from the television series with a theatrical-film fact. Checked revival separately from campfire hand healing #541 and hair power loss #2135. Hair is already cut, so it cannot be the healing instrument here.')
R(2135,'tangled tangled-keane tangled-dialogue','Tangled 2010 tower climax; the hair itself.',
  'Cut hair becomes brown and loses its healing power.',
  ['The hair becomes brown and powerless.','It does not regrow longer at the cut.','It does not become solid gold.','It remains physically present rather than disappearing.'],
  'Narrowed all magic to the hair healing power; Rapunzel later tear still heals Eugene. The question does not claim she loses every form of magic or that later series continuity applies.')
R(2136,'bambi-models bambi-history','Bambi animation research; two live fawns at the studio.',
  'Disney and AFI identify Maine as the source of the fawns.',
  ['Maine supplied the model fawns.','Vermont is not the named source state.','Oregon is not the named source state.','Wisconsin is not the named source state.'],
  'Checked the live-fawn donation rather than only background film shot in Maine. Removed incidental Hollywood-location wording; origin and later destination #2143 are different facts.')
R(2137,'bambi-history','Bambi 1942 final forest fire.',
  'AFI explicitly says the fire is sparked by the hunters campfire.',
  ['The hunters campfire starts it.','Lightning is not the initiating event identified.','A rifle wound endangers Bambi separately but does not ignite the fire.','No nearby-town wildfire is the origin in the scene synopsis.'],
  'Distinguished Bambi being shot from the subsequent campfire spread. The source positively gives the cause, so absence of lightning in a short summary is not the only evidence.')
R(2138,'bambi-history bambi-dialogue','Bambi 1942, mother explanation after meadow danger.',
  'The mother explicitly names Man as the danger.',
  ['Man is the word she uses.','Twolegs is not the spoken term.','The Takers is not her term.','Hunters describes the people but is not the single word asked for.'],
  'Changed the broad everyone/whenever claim to the actual speaker and scene. Literal wording asks her chosen word, not any defensible description of the hunters.')
R(2139,'smokey','U.S. historical forest-fire prevention campaign, 1944.',
  'The official campaign archive places Bambi before Smokey and dates Smokey first poster to 1944.',
  ['Smokey Bear is the mascot introduced then.','Woodsy Owl is not the mascot in the 1944 campaign entry.','Ranger Rick is not that campaign mascot.','Bucky Beaver is not the figure identified in the official timeline.'],
  'Replaced a vague claim that Bambi inspired mascot creation with the documented campaign succession. The living Smokey cub was rescued in 1950, separate from the 1944 illustrated mascot.')
R(2140,'bambi-dialogue','Bambi 1942 clover scene; source of advice rather than on-screen speaker.',
  'Mother asks what father said and Thumper recites the greens advice.',
  ['His father is the named source of the advice.','His mother prompts the recitation but is not the named original adviser.','Friend Owl is not attributed this advice.','Flower is not attributed this advice.'],
  'Original question incorrectly treated father as delivering the on-screen correction. Final asks whose advice; Thumper speaks it and mother prompts him. Explicitly excluded the strongest competing interpretation, mother.')
R(2141,'bambi-history bambi-dialogue','Bambi 1942 annual seasonal progression.',
  'AFI describes renewed spring and courtship, with new fawns returning at the ending.',
  ['Spring brings the courtship and renewed life.','Summer is not the season identified for the renewal.','Autumn is not the described courtship season.','Winter is the earlier harsh season, not the spring renewal.'],
  'Replaced the ill-formed question about opening/closing on a cycle with one clear season and parallel choices. Spring is explicit, not inferred solely from general nature knowledge. Season refers to weather, not a television season.')
R(2142,'bambi-dialogue bambi-ice bambi-history','Bambi 1942 winter skating scene.',
  'Disney synopsis and AFI use stiff water; dialogue describes water as stiff.',
  ['Stiff water matches the dialogue description.','Frozen water is a literal definition but not the unusual wording asked for.','Slick ground is not the scene phrase.','Hard water is not the phrase and would normally describe mineral content.'],
  'Frozen water could describe ice, but the question asks the unusual term used in this scene; three independent texts preserve stiff. No generic physical definition is being graded.')
R(2143,'bambi-zoo bambi-zoo-cor','Historical destination of the two adult model deer after Bambi production.',
  'Two named Disney historians identify Griffith Park Zoo as recipient.',
  ['Griffith Park Zoo received the model deer.','San Diego Zoo was visited by artists but was not this donation destination.','Lincoln Park Zoo is not the recipient in either account.','Central Park Zoo is not the recipient in either account.'],
  'Distinguished zoo visits from donation destination and old Griffith Park Zoo from the later Los Angeles Zoo. Primary accession paperwork unavailable; independent historian accounts agree on recipient.')
R(2144,'brother-production','Brother Bear development, before release as Brother Bear.',
  'Disney identifies Bears as the working title.',
  ['Bears is the documented working title.','The Great Spirit is not the working title listed.','Kenais Journey is not the working title listed.','Totem is not the working title listed.'],
  'Removed released under working title contradiction. The bear word repeats the subject but does not establish the exact plural working title against other plausible development names.')
R(2145,'brother-production brother-ratio','Brother Bear theatrical presentation after transformation.',
  'Disney and filmmaker presentation account describe a wider image after Kenai changes.',
  ['The aspect ratio widens.','The film does not change to black and white; its color opens up.','Slower frame rate is not the described image change.','A silent soundtrack is not the visual technique identified.'],
  'Do not confuse the concurrent richer color with a monochrome palette. Sources explicitly establish widened frame; no exact ratio is asked because sources vary slightly on the initial ratio.')
R(2146,'brother-dialogue brother-plot','Brother Bear spirit mountain and dancing sky lights.',
  'Opening identifies ancestor spirits with dancing sky lights and the mountain where lights touch earth.',
  ['Northern Lights are the dancing auroral lights associated with the spirits.','A solar eclipse is not a dancing display of sky lights.','A meteor shower is not the continuous auroral light curtain.','A lightning storm is not the ancestral sky-light phenomenon.'],
  'Removed the claim that a natural phenomenon itself performs magic. The question asks the visual association of the spirit mountain, rather than explaining the supernatural mechanism.')
R(2147,'brother-plot brother-dialogue','Brother Bear reveal at the salmon run.',
  'Koda account reveals the mother was the bear Kenai killed before his own transformation.',
  ['Human Kenai killed her.','Denahi pursues transformed Kenai but did not kill Koda mother.','A rival bear is not her killer.','Wolves are not the cause of her death.'],
  'Checked the reveal rather than Kenai initial belief about Sitka death. The two deaths have different immediate causes; the question targets Koda mother only.')
R(2148,'brother-plot brother-production','Brother Bear production studio location in 2003.',
  'The history locates the Florida feature studio at Disney-MGM Studios, Orlando.',
  ['Orlando is the principal studio city.','Burbank is the California studio, not this Florida production base.','Vancouver is not the Florida studio city.','Toronto is not the Florida studio city.'],
  'Removed U.S. from stem because two distractors are Canadian. Sources specifically locate the production rather than simply describing the company headquarters; closure date is unnecessary.')
R(2149,'herc-design','Hercules 1997 design attribution.',
  'The Buena Vista education guide names Gerald Scarfe as the British artist behind the original designs.',
  ['Gerald Scarfe is the credited design influence.','Ronald Searle is not the named Hercules designer.','Quentin Blake is not the named designer.','Al Hirschfeld is not the named designer.'],
  'Removed an unnecessary job-title/Greek-vase compound claim and retained the supported design attribution. Other artists are real stylists but that does not give them this film credit.')
R(2150,'herc-gospel herc-muses','Hercules 1997 Muses storytelling music.',
  'The filmmakers describe choosing a gospel approach for the Muses music.',
  ['Gospel is the identified central style.','Opera is not the approach Musker describes.','Jazz is not the approach he describes for the Muses.','Doo-wop is not the gospel concept the discussion identifies.'],
  'The score uses multiple styles, so final wording says especially rather than exclusively. The Muses role in #69 and their song titles elsewhere do not by themselves name this musical genre; moved to music category.')
R(2151,'herc-mouth herc-muses','Eric Goldberg 2017 D23 recollection about Phil animation.',
  'Goldberg singles out DeVito mouth configurations in filmed recording reference.',
  ['His unusual mouth shapes are the feature named.','Eyebrow movement is not the feature Goldberg identifies in this account.','Hand gestures are not the facial feature he singles out.','Posture is not the facial feature he singles out.'],
  'A generic reference question could allow multiple studied features. Attribution to Goldberg and the unusual feature he described narrows it to the documented mouth shapes, without claiming no other reference was ever observed.')
R(2152,'herc-cloud herc-transcription','Hercules 1997 opening birth celebration.',
  'Zeus combines named cloud types into a small cloud that becomes Pegasus.',
  ['A cloud is the material shaped.','Marble would be a statue, not the cloud he forms.','Sea foam is not the cirrus/nimbostratus/cumulus mixture.','Starlight is not the named mixture.'],
  'Checked the original film event, distinct from Pegasus general species #295 and other Greek myths. The named cloud types positively exclude marble, foam and starlight.')
R(2153,'herc-transcription herc-hydra-cor','Hercules 1997 first Hydra decapitation, not classical mythology.',
  'The specific first regrowth is described as three heads in two detailed scene accounts.',
  ['Three heads emerge from the first severed neck.','Two is the common myth version, not this Disney scene.','Four is not the count in that first regrowth.','Five is not the count in that first regrowth.'],
  'Corrected two to three and restricted to the first cut, since later mass-regrowth visuals are complex. #829 identifies the Hydra as the monster, but that does not supply the count. Two secondary accounts agree; no direct film playback claimed.')
R(2154,'fox-production','The Fox and the Hound production delay, 1979 departure.',
  'Disney production history names Don Bluth and his departing team.',
  ['Don Bluth is the animator whose departure caused the delay.','Ralph Bakshi is not the departing Disney team leader named.','Richard Williams is not that departing team leader.','Bill Melendez is not that departing team leader.'],
  'Checked that this is the documented staff departure, not merely any rival studio existing at the time. Other listed animators do not fit this specific departure.')
R(2155,'fox-cost fox-cost-cor','The Fox and the Hound approximate production cost in nominal 1981 dollars.',
  'Both film histories give a $12 million budget.',
  ['$12 million matches the reported approximate budget.','$2 million is not the reported budget.','$44 million belongs to the later Black Cauldron comparison, not this production.','$80 million is not the reported budget.'],
  'Replaced a broad record claim with approximate nominal budget; no inflation conversion or first-digital-score premise remains. #2478 asks a different film cost/record and cannot determine this figure. Primary studio cost ledger not accessible; secondary accounts agree.')
R(2156,'vixey-keane vixey-musker','Glen Keane recollection of Vixey animation on The Fox and the Hound.',
  'Keane explicitly names Tim Burton as working with him on Vixey; Musker independently recalls it.',
  ['Tim Burton is the artist Keane names.','John Lasseter worked on the film but is not the Vixey colleague Keane identifies.','Brad Bird worked on the film but is not the colleague named here.','Chris Buck occupied the neighboring room; Keane distinguishes him from Burton doing Vixey.'],
  'General involvement of all four does not make all four correct. The final wording asks for Keane specific recollection, supported by Musker; removed unneeded uncredited/acclaimed qualifiers.')
R(2157,'lasseter fox-cost fox-cost-cor','The Fox and the Hound animator who later held Pixar chief creative officer role.',
  'The animation team includes Lasseter; Disney biography identifies his later role.',
  ['John Lasseter meets both the animation and Pixar leadership conditions.','Tim Burton meets film involvement but not Pixar chief creative officer condition.','Brad Bird meets film involvement but not that leadership condition.','John Musker meets film involvement but not that leadership condition.'],
  'All four worked at Disney, so the later Pixar role is essential. Historical future wording avoids treating Lasseter as current officer; he left in 2018. Removed the debatable co-founder shorthand.')
R(2158,'fox-production','The Fox and the Hound theatrical 1981; preserve encounter.',
  'Disney explicitly identifies Tod love interest as the female fox Vixey.',
  ['Vixey is Tod love interest.','Faline is Bambi doe love interest.','Duchess is the Aristocats mother cat.','Perdita is the Dalmatian mother.'],
  'Read full Fox/Hound context: Vixey name differs from Burton assignment fact #2156. The three other names belong to distinct animals/films, not alternative names for Tod partner.')
R(2159,'soul-hands','Soul production reference for Joe piano hand animation.',
  'Disney animator interview identifies Batiste hand reference footage.',
  ['Jon Batiste hands were filmed for Joe piano reference.','Herbie Hancock was an adviser/inspiration but is not the filmed pianist identified here.','Wynton Marsalis is not that reference pianist.','Questlove voices Curley but is not the piano hand reference.'],
  'Replaced motion-captured/MIDI claim with the documented filmed reference and hand animation. #2289 asks the score Oscar recipient, while this asks a separate production method and performer role.')
R(2160,'soul-credits','Soul 2020 original English voice cast.',
  'Disney credits Joe Gardner voice to Jamie Foxx.',
  ['Jamie Foxx is the credited voice.','Denzel Washington is not credited as Joe.','Chadwick Boseman is not credited as Joe.','Michael B. Jordan is not credited as Joe.'],
  'Removed the unrelated first-Black-protagonist superlative. Exactly one original English credit answers; #2163 asks another character and actor, so the similar stem is not shared knowledge.')
R(2161,'soul-credits','Soul 2020 directing credits.',
  'Disney names Pete Docter as director and Kemp Powers as co-director.',
  ['Kemp Powers has this co-directing credit.','Ronnie del Carmen is not credited as Soul co-director.','Adrian Molina is not credited as Soul co-director.','Domee Shi is not credited as Soul co-director.'],
  'Removed an extra first-in-history claim; the question now depends only on the film credit. Other Pixar filmmakers do not share the credited Soul role.')
R(2162,'soul-city','Soul 2020 human-world setting.',
  'Pixar synopsis places Joe on New York City streets.',
  ['New York City is the main human-world setting.','Chicago is not the setting identified.','Los Angeles is not the setting identified.','New Orleans is not the setting; Batiste hometown does not relocate Joe story.'],
  'Checked distinction between performer background and narrative location. City in New York City is a formal name suffix and matches the city-type question, not an answer giveaway; all options are cities.')
R(2163,'soul-credits','Soul 2020 original English voice cast.',
  'Disney credits Tina Fey as 22.',
  ['Tina Fey voices 22.','Kristen Bell is not credited as 22.','Rachel McAdams is not credited as 22.','Amy Poehler voices a different Pixar character, not 22.'],
  'Added the missing film/version context and removed unneeded eons language. Similar wording to Joe voice question does not make the two separate cast assignments duplicates.')
R(2164,'soul-scientist','Pete Docter development recollection in Soul production notes.',
  'Docter explicitly lists scientist or businessman as earlier possible professions.',
  ['A scientist is one of Docter stated possibilities.','A doctor is not the profession named in that recollection.','An architect is not named in that recollection.','A lawyer is not named in that recollection.'],
  'Replaced teacher, which is Joe actual job, with architect to avoid confusion with the final story. The attribution asks which option Docter actually named, not every conceivable profession brainstormed.')
R(2165,'soul-score','Soul 2020 music production; electronic otherworld score.',
  'Production notes name Reznor and Ross for the synthesized soul-world score alongside Batiste jazz.',
  ['Trent Reznor and Atticus Ross are the score duo.','Hans Zimmer and Pharrell Williams are not the credited duo.','Danny Elfman and Alan Silvestri are not the credited duo.','Thomas Newman and Randy Newman are not the credited duo.'],
  'Removed Oscar-for-these-sequences implication: the Oscar was for the whole score shared by all three musicians. The final question targets different musical roles, not the same award-credit fact as #2289.')
R(2166,'onward','Onward 2020 modern suburban fantasy setting.',
  'Pixar world descriptions identify New Mushroomton and the Lightfoot home setting.',
  ['New Mushroomton is the town name.','Elftown is not the named setting.','Mysthaven is not the named setting.','Willowbrook is not the named setting.'],
  'Official homes and unicorn profiles both use New Mushroomton. Full Onward/category context contains other locations but no second active question asking the town name.')
R(2167,'onward','Onward 2020 everyday unicorn behavior.',
  'Pixar explicitly describes the unicorns as garbage scavengers.',
  ['They raid garbage bins.','Delivering parcels is not their described everyday role.','Guarding malls is not their described role.','Herding livestock is not their described role.'],
  'Replaced the subjective indignity phrasing with behavior and made all options parallel actions. Pixar distinguishes pet dragons from scavenging unicorns; mythical grace alone would not establish this detail.')

assert all(r['checks'] for r in reviews.values())
template['at']=DATE
template['sourcesChecked']=sorted({s for r in reviews.values() for s in r['premise']['sources']})
(ROOT/'audit/runs/next-shard-0032-reviewed-notes.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
libpath.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Authored',len(reviews),'explicit reviews and',len(template['sourcesChecked']),'evaluated source passages.')
