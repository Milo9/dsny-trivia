"""Expand explicitly authored batch-19 evidence; does not edit questions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sources_path = ROOT / 'audit/source-notes.json'
library = json.loads(sources_path.read_text(encoding='utf-8'))
notes_path = ROOT / 'audit/runs/next-shard-0019-reviewed-notes.json'
notes = json.loads(notes_path.read_text(encoding='utf-8'))
data = {}

def add(qid, url, locator, evidence, reasons, extra=None, challenge=None):
    sid = f'b19-{qid}'
    library['sources'][sid] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt='2026-11-07', timeSensitive=False,
        nextReviewAt=None, topics=['Batch 19'], limitations=
        'Text passage inspected; no film/audio playback claimed. Transcripts are third-party transcriptions; institutional material and corroboration are identified separately.')
    refs = [sid] + (extra or [])
    data[qid] = (refs, reasons, challenge)

SS = 'https://www.springfieldspringfield.co.uk/movie_script.php?movie='
PX = 'https://www.pixar.com/'
add(1005, SS+'aladdin', 'Early bread-theft chase, lines 126-198; contrast opening Arabian Nights and later parade/carpet sequences',
    'The marketplace pursuit moves into the One Jump Ahead number. Arabian Nights is the narrator opening; Prince Ali is the later royal parade; A Whole New World is the carpet duet.',
    ['The chase chorus identifies One Jump Ahead.', 'Prince Ali accompanies the later parade, not the early escape.', 'Arabian Nights precedes Aladdin’s marketplace chase.', 'A Whole New World is the later carpet duet.'])
add(1007, 'https://disney.go.com/disneyrecords/Soundtracks/NightmareBeforeChristmas/', 'Production-number descriptions and track order, lines 3-12',
    'This Is Halloween introduces the story. Jack’s Lament expresses his dissatisfaction, What’s This concerns Christmas Town, and Town Meeting Song comes later. Overture and spoken narration precede the first sung number.',
    ['This Is Halloween is the first sung number.', 'Jack’s Lament follows the opening celebration.', 'What’s This occurs after Jack reaches Christmas Town.', 'Town Meeting Song follows his return.'],
    challenge='Distinguished a sung musical number from the preceding instrumental overture and spoken narration; none of the later three numbers opens the singing.')
add(1008, 'https://en.wikipedia.org/wiki/Out_There_(Disney_song)', 'Synopsis: Frollo leaves, Quasimodo imagines the outside world; corroborated by Schwartz’s Out There discussion',
    'Out There is Quasimodo’s early wish to experience life outside Notre Dame. The other offered songs concern romantic hope, Esmeralda’s prayer, and the festival celebration.',
    ['Out There expresses his wish to join the people outside.', 'Heaven’s Light concerns romantic hope later in the story.', 'God Help the Outcasts is Esmeralda’s cathedral prayer.', 'Topsy Turvy is the festival number, not this private early wish.'], ['b14-bells'],
    'Challenged Heaven’s Light as another Quasimodo solo; the early wish for a day outside, rather than later romantic hope, uniquely identifies Out There.')
add(1009, SS+'hercules-1997', 'Meg and the Muses after Hercules’s date; lines 946-986, contrasted with opening, Phil training and finale',
    'Meg denies being in love in I Won’t Say (I’m in Love). The Muses narrate The Gospel Truth and the finale A Star Is Born; Phil’s training song is One Last Hope.',
    ['Meg’s denial is the subject of I Won’t Say (I’m in Love).', 'A Star Is Born is the Muses’ finale.', 'The Gospel Truth supplies the Muses’ narration.', 'One Last Hope is Phil’s training number.'])
add(1010, 'https://en.wikipedia.org/wiki/Honor_to_Us_All', 'Opening description and Context: bathhouse, makeover, Matchmaker procession',
    'Honor to Us All accompanies Mulan’s preparation for the Matchmaker. Reflection follows her failure; the two soldier numbers belong to training and the army march.',
    ['Honor to Us All accompanies the makeover and Matchmaker preparation.', 'Reflection is her subsequent identity lament.', 'A Girl Worth Fighting For is sung by marching soldiers.', 'I’ll Make a Man Out of You accompanies military training.'],
    challenge='Rechecked the 1998 animated version and exact preparation scene, not the 2020 remake or Mulan’s later Reflection.')
add(1011, SS+'tarzan', 'Jane takes over teaching, lines 1177-1238; earlier opening, childhood growth and camp percussion scenes',
    'Strangers Like Me accompanies Tarzan’s education with Jane. Two Worlds is the opening family montage, Son of Man the growing-up montage, and Trashin’ the Camp the gorillas’ camp percussion.',
    ['Strangers Like Me accompanies the human-world lessons.', 'Two Worlds accompanies the opening family montage.', 'Son of Man accompanies Tarzan’s childhood growth.', 'Trashin’ the Camp accompanies the gorillas’ camp antics.'],
    challenge='Changed follows to accompanies: a broad chronological follows could include later music. The teaching montage uniquely supplies the answer.')
add(1012, 'https://www.oscars.org/oscars/ceremonies/2001', 'Music (Original Song), complete nominee list and The Emperor’s New Groove film listing',
    'The sole nomination for The Emperor’s New Groove at the 2001 ceremony was My Funny Friend and Me, with music by Sting and David Hartley and lyrics by Sting.',
    ['My Funny Friend and Me appears in the nominee list.', 'Perfect World is absent from the complete song nominee list.', 'One Day She’ll Love Me is absent from that complete list.', 'Snuff Out the Light is absent from that complete list.'])
add(1013, 'https://www.latimes.com/entertainment-arts/movies/story/2022-08-25/lilo-and-stitch-soundtrack-disney-kamehameha-schools-childrens-chorus',
    'Paragraph beginning Less than a year later, opening-title hula sequence, line 290',
    'The opening hula uses He Mele No Lilo.',
    ['The identified opening cue is He Mele No Lilo.', 'This is a different soundtrack song.', 'This is not the identified opening cue.', 'This is not the identified opening cue.'],
    challenge='Checked the 2002 animated opening, not the 2025 remake. The title’s Lilo token comes from the film name and does not disclose the Hawaiian song title.')
add(1014, SS+'the-princess-and-the-frog', 'Mama Odie’s advice and song, lines 1620-1705; contrast Tiana restaurant fantasy, New Orleans opening and Facilier deal',
    'Mama Odie sings Dig a Little Deeper to distinguish wants from needs. Almost There is Tiana’s restaurant fantasy; Down in New Orleans establishes the city; Friends on the Other Side is Facilier’s deal.',
    ['Dig a Little Deeper is the advice number in this scene.', 'Almost There is Tiana’s restaurant fantasy.', 'Down in New Orleans is not the wants-versus-needs advice number.', 'Friends on the Other Side belongs to Facilier’s deal.'])
add(1015, SS+'tangled', 'Tower departure request and Gothel’s warning song, lines 248-323; opening routine, tavern and lantern scenes',
    'Mother Knows Best is Gothel’s coercive safety warning. When Will My Life Begin is Rapunzel’s routine song, I See the Light the lantern duet, and I’ve Got a Dream the tavern ensemble.',
    ['Mother Knows Best is Gothel’s manipulative warning.', 'When Will My Life Begin introduces Rapunzel’s routine.', 'I See the Light is Rapunzel and Flynn’s lantern duet.', 'I’ve Got a Dream is the tavern ensemble number.'], ['b13-tangledcatalog'])
add(1016, 'https://en.wikipedia.org/wiki/Love_Is_an_Open_Door', 'Opening and Synopsis: Anna and Hans at Elsa’s coronation reception',
    'Love Is an Open Door is Anna and Hans’s romantic duet ending in a proposal. For the First Time in Forever is associated with Anna and Elsa, Fixer Upper with trolls, and Do You Want to Build a Snowman with Anna’s childhood attempts to reconnect.',
    ['Love Is an Open Door is the Anna-Hans duet.', 'For the First Time in Forever is not sung as their duet.', 'Fixer Upper is the troll matchmaking number.', 'Do You Want to Build a Snowman is Anna’s childhood appeal.'])
add(1017, 'https://en.wikipedia.org/wiki/Try_Everything', 'Background and composition: Gazelle’s recording in the film',
    'Gazelle, voiced by Shakira, performs Try Everything in Zootopia. Let It Go is Frozen’s Elsa song; How Far I’ll Go is Moana’s solo; Touch the Sky is from Brave.',
    ['Try Everything is Gazelle’s recording and concert song.', 'Let It Go is from Frozen, not Gazelle’s song.', 'How Far I’ll Go is from Moana.', 'Touch the Sky is from Brave.'])
add(1018, SS+'moana', 'Hidden boats, drum and ancestral vision, ending We were voyagers, lines 330-404; later I Am Moana sequence',
    'We Know the Way accompanies the ancestral voyage vision in the hidden canoe cavern. How Far I’ll Go expresses Moana’s longing, Where You Are introduces island duties, and I Am Moana is her later identity affirmation.',
    ['We Know the Way accompanies the cavern vision.', 'How Far I’ll Go expresses her own longing to sail.', 'Where You Are introduces present island life.', 'I Am Moana invokes ancestry later, outside this cavern vision.'], ['b9-moanaway'],
    'I Am Moana also mentions voyaging ancestry, so the original broad history wording was insufficient. The drum-triggered cavern vision excludes that later song.')
add(1019, SS+'encanto', 'Mirabel’s initial family-and-gifts roll call, lines 76-269; later Bruno, miracle lament and reconstruction numbers',
    'The Family Madrigal introduces the relatives and gifts at the start. We Don’t Talk About Bruno is the later ensemble account of Bruno, All of You the rebuilding finale, and Waiting on a Miracle Mirabel’s private lament.',
    ['The Family Madrigal is the opening roll call.', 'We Don’t Talk About Bruno concerns Bruno later.', 'All of You is the rebuilding finale.', 'Waiting on a Miracle is Mirabel’s later private lament.'])
add(1020, 'https://www.laughingplace.com/w/articles/2021/03/24/james-newton-howard-talks-about-scoring-disneys-raya-and-the-last-dragon-and-the-jungle-cruise-in-new-for-scores-podcast-episode/',
    'Opening podcast recap and Southeast Asian instruments discussion, lines 143-147',
    'The Disney For Scores interview identifies James Newton Howard as Raya’s score composer and discusses his work incorporating Southeast Asian instruments.',
    ['Howard is the identified score composer.', 'Menken is a different composer, not the credited score author.', 'Giacchino is a different composer, not the credited score author.', 'Zimmer is a different composer, not the credited score author.'])
add(1021, PX+'toy-story', 'Rex, Hamm, Mr. Potato Head and Slinky character profiles',
    'Rex is the insecure plastic dinosaur; Hamm is the piggy bank, Slinky a stretchy toy dog, and Mr. Potato Head a detachable-face toy.',
    ['Rex is the insecure dinosaur.', 'Slinky Dog is a dog toy.', 'Hamm is the piggy bank.', 'Mr. Potato Head is the potato-shaped toy.'])
add(1022, PX+'a-bugs-life', 'Born To Be Wild synopsis and Francis/circus character profiles',
    'Flik’s recruited warrior bugs are actually a circus troupe; they are entertainers, not palace guards, merchants or deserters.',
    ['The recruited bugs are circus performers.', 'The troupe is not employed as palace guards.', 'Their occupation is performing, not trading goods.', 'They are not deserters from an army.'])
add(1023, PX+'toy-story-2', 'Opening synopsis: 1950s TV show and Roundup collectibles',
    'Woody is a collectible from the fictional 1950s show Woody’s Roundup. Cowboy Camp is Andy’s destination; the two other offered titles are not the show’s name.',
    ['Woody’s Roundup is explicitly named as the show.', 'The Roundup Gang is not the identified title.', 'Sheriff Woody Show is not the identified title.', 'Cowboy Camp is Andy’s destination, not the program.'],
    challenge='This tests a fictional program as part of a theatrical Toy Story 2 plot, not real television trivia. The actual program name excludes all alternate titles; the Shanghai attraction asks a separate location fact.')
add(1024, SS+'finding-nemo', 'Aquarium initiation: From this moment on, lines 830-835; Tank Gang and turtle names corroborated by Pixar',
    'The tank initiation names Nemo Sharkbait. Bubbles is another tank fish; Squirt is Crush’s child; Little Fin is not the name bestowed at this initiation.',
    ['Sharkbait is the name bestowed during initiation.', 'Little Fin is not the bestowed name.', 'Bubbles names another tank resident.', 'Squirt names Crush’s offspring.'])
add(1025, 'https://catalog.afi.com/Film/54376-THE-INCREDIBLES', 'Synopsis first paragraph: crime fighting hours before the wedding',
    'AFI places Mr. Incredible and Elastigirl’s pre-wedding crime fighting in Metroville. The question is bounded to the 2004 opening rather than a contested generalized home-city label.',
    ['Metroville is the explicitly identified opening city.', 'Municiberg is not the city named for this scene.', 'Nomanisan is not the city named for this scene.', 'Supersburg is not the city named for this scene.'],
    challenge='Avoided carrying sequel geography or generic home-city claims into the opening. The cited synopsis directly identifies Metroville for the specified event.')
add(1026, PX+'cars-3', 'Thomasville section; Doc Hudson described as McQueen’s mentor',
    'Pixar names Doc Hudson as McQueen’s mentor and Smokey as Doc’s former coach. The King and Chick Hicks are racers, and Mack is McQueen’s transporter, not this mentor.',
    ['Doc Hudson is the named mentor.', 'The King is a competing veteran racer, not the mentor identified here.', 'Mack transports McQueen rather than mentoring his racing.', 'Chick Hicks is McQueen’s rival.'])
add(1027, PX+'ratatouille', 'Linguini profile, first sentence; Skinner profile distinguishes former sous-chef',
    'Pixar gives Linguini’s initial position as garbage boy. The question asks his hired title, not whether his cleanup duties could include washing dishes.',
    ['Garbage boy is his initial hired title.', 'Sous-chef is not his initial hired title.', 'Waiter is not his initial hired title.', 'Dishwasher describes a possible cleanup task, not his stated hired title.'],
    challenge='The screenplay calls him a plongeur or something, so general cleanup tasks could overlap dishwasher. The final question explicitly asks the hired title stated in Pixar’s profile.')
add(1028, PX+'wall-e', 'The World: Axiom section',
    'Pixar describes the Axiom as the refuge of consumer culture built by Buy n’ Large Corporation. Axiom is the ship name, not Axiom Corp; MegaBuy and EarthMart are not the identified corporation.',
    ['Buy n Large is the named corporation.', 'Axiom is the ship rather than this corporation.', 'MegaBuy is not the corporation named by Pixar.', 'EarthMart is not the corporation named by Pixar.'])
add(1029, SS+'up', 'Russell’s first doorstep visit, lines 251-267; badge ceremony lines 1351-1359',
    'Russell explicitly says the missing badge he seeks is Assisting the Elderly; the ceremony names the same award.',
    ['Assisting the Elderly is his stated missing badge.', 'Animal Tracking is not the badge he says he needs.', 'Knot Tying is not the missing badge he identifies.', 'Balloon Safety is not the missing badge he identifies.'])
add(1030, 'https://en.wikipedia.org/wiki/Toy_Story_3', 'Plot: trash-center conveyor, shredder, incinerator and Aliens’ crane rescue',
    'At the trash center the toys face a shredder before reaching an incinerator; the Aliens’ crane rescue saves them from being burned.',
    ['The landfill incinerator is the imminent burning hazard.', 'A shredder threatens earlier but is not the burning hazard at the rescue.', 'They are at the landfill, not a daycare furnace.', 'They are at the landfill, not a museum crusher.'],
    challenge='The earlier shredder also fits the original broad near-destruction wording. The final burn-and-rescue wording excludes that separate hazard.')
add(1031, PX+'cars-2', 'Finn McMissile, Holley Shiftwell, Professor Z and Miles Axlerod profiles',
    'Finn is the experienced British spy with years in the field; Holley is a British desk agent turned rookie field spy. Professor Z is a weapons designer and Axlerod the fuel-promoting former oil baron.',
    ['Finn is the veteran British spy.', 'Holley is explicitly a rookie field spy.', 'Professor Z is the weapons designer.', 'Miles Axlerod is the former oil baron and race organizer.'],
    challenge='Both Finn and Holley fit the old spy/mistaken-agent question. The veteran-versus-rookie distinction is explicit in the source and rules out Holley.')
add(1032, PX+'brave', 'The Lords profile: clans summoned to Castle DunBroch for Highland Games',
    'Pixar names the gathering as the Highland Games. It is the suitor competition, not a preliminary test of who is eligible to compete.',
    ['The Highland Games is the named gathering.', 'The Royal Tournament is not its identified name.', 'The Clan Trials is not its identified name.', 'The Games of DunBroch is not its identified name.'])
add(1033, PX+'monsters-university', 'Oozma Kappa, Python Nu Kappa and Roar Omega Roar profiles',
    'The campus inter-fraternity contest is repeatedly named the Scare Games in Pixar’s fraternity profiles.',
    ['The Scare Games is the named contest.', 'The Roar Cup is not the contest’s name.', 'The Monster Games is not the contest’s name.', 'The Fear Finals is not the contest’s name.'])
add(1034, 'https://en.wikipedia.org/wiki/Inside_Out_(2015_film)', 'Plot opening: experiences processed into colored memory orbs in Headquarters',
    'Riley’s experiences become memories stored as colored orbs; core memories are a significant subset, not a separate container shape.',
    ['Memory orbs are the spherical recollection containers.', 'Emotion jars are not the identified containers.', 'Dream reels concern a different concept and are not the spherical memory containers.', 'Thought cubes are not the identified containers.'], ['b12-inside'],
    'Distinguished ordinary memory storage from #1312’s special core-memory subset. No source inference from a single emotional ability is used; the passage identifies the physical containers.')
add(1035, PX+'the-good-dinosaur', 'Opening synopsis and Arlo profile',
    'Pixar identifies Arlo as an Apatosaurus. The offered alternative genera are distinct from that identification.',
    ['Arlo is an Apatosaurus.', 'Tyrannosaurus is a different genus.', 'Triceratops is a different genus.', 'Stegosaurus is a different genus.'])
add(1036, PX+'finding-dory', 'Hank, Bailey, Destiny and Fluke & Rudder profiles, previously inspected b9-dory',
    'Hank is a seven-armed octopus. Fluke and Rudder are sea lions, Bailey a beluga, and Destiny a whale shark.',
    ['Hank is an octopus despite having seven arms.', 'Sea lion describes Fluke and Rudder.', 'Beluga whale describes Bailey.', 'Whale shark describes Destiny.'], ['b9-dory'])
add(1037, PX+'cars-3', 'Cruz Ramirez profile and comeback synopsis; Natalie Certain and Miss Fritter profiles',
    'Cruz is McQueen’s trainer at the Rust-eze Racing Center. Sally is his partner, Natalie an analyst, and Miss Fritter a demolition-derby bus.',
    ['Cruz is the trainer helping his comeback.', 'Sally is his partner, not the assigned trainer.', 'Natalie is an analyst, not his trainer.', 'Miss Fritter is a demolition-derby competitor.'])
add(1038, PX+'coco', 'Dante profile',
    'Pixar explicitly identifies Dante as a Xoloitzcuintli, a Xolo dog. Hairlessness alone does not identify him as some other hairless breed.',
    ['Xoloitzcuintli is Dante’s stated breed.', 'Labrador retriever is a different breed.', 'Chinese crested is a different hairless breed.', 'Peruvian hairless dog is a distinct breed despite a shared hairless appearance.'],
    challenge='Challenged the two hairless alternatives; the answer rests on the explicit breed designation, not an inference from appearance. Replaced short distractors with comparably specific breed names.')
add(1039, PX+'incredibles-2', 'Jack-Jack and Raccoon profiles, contrasted with Helen, Violet and Dash',
    'Jack-Jack discovers an emerging set of powers, including the backyard encounter. Helen stretches, Dash has speed and Violet invisibility/force fields; these are their established abilities rather than Jack-Jack’s expanding unpredictable set.',
    ['Jack-Jack has the emerging unpredictable set of powers.', 'Dash has his established super-speed.', 'Violet has her established invisibility and force fields.', 'Helen has her established elasticity.'], ['b10-incredibles'],
    'Multiple powers alone would not exclude Violet’s two powers. Rechecked the newly developing, unpredictable set in this sequel; that distinguishes Jack-Jack. Replaced Tony, who is not a Parr family member.')
add(1040, 'https://en.wikipedia.org/wiki/Toy_Story_4', 'Plot: Gabby explains wanting Woody’s voice box; cast distinguishes Gabby and Giggle',
    'Gabby Gabby wants Woody’s working voice box to repair her defective one. Giggle is Bo’s tiny policewoman friend, Dolly belongs to Bonnie, and Bo helps Woody rather than seeking his voice box.',
    ['Gabby Gabby seeks the working voice box.', 'Giggle McDimples is Bo’s tiny policewoman friend.', 'Dolly is Bonnie’s doll, not the antique-store doll seeking this repair.', 'Bo Peep is Woody’s ally, not the doll seeking his voice box.'], ['b10-toy4'])
add(1042, PX+'soul', 'The Counselors, Terry, Joe Gardner and Moonwind profiles',
    'The counselors are all known as Jerry. Terry keeps the count, Joe is the musician, and Moonwind a living mystic.',
    ['Jerry is the counselors’ shared name.', 'Terry is the individual counter.', 'Joe is the musician’s name.', 'Moonwind names the mystic.'])
add(1043, PX+'luca', 'Ercole Visconti profile: repeat champion of the Portorosso Cup',
    'Pixar names the local town race the Portorosso Cup. The Vespa-owning bully’s scooter does not make the event a Vespa race.',
    ['Portorosso Cup is the named local event.', 'Vespa Grand Prix is not the identified event name.', 'Cinque Terre Challenge is not the identified name.', 'Sea Monster Derby is not the identified name.'], ['b14-luca'])
add(1044, PX+'turning-red', 'Meilin Lee profile',
    'Mei and her friends obsess over the boy band 4*Town; the other offered group names do not identify that band.',
    ['4*Town is the band named in Mei’s profile.', '5 Alarm is not the band named in the profile.', 'Town4U is not the band named in the profile.', 'Red Panda Pop is not the band named in the profile.'])
add(1045, PX+'lightyear', 'Opening synopsis and Sox profile',
    'Buzz’s robotic companion cat is Sox. Rex is the Toy Story dinosaur, M-O the WALL-E cleaner, and Mittens is not the identified cat companion.',
    ['Sox is the robotic cat.', 'Mittens is not the named robotic companion.', 'Rex is a dinosaur toy, not this cat.', 'M.O. is a cleaner robot from WALL-E, not this cat.'])
add(1046, PX+'elemental', 'Wade Ripple, Clod, Gale and Bernie Lumen profiles',
    'Wade Ripple is Water, Clod Earth, Gale Wind/Air and Bernie Fire. The specified Water character who meets Ember is Wade.',
    ['Wade Ripple is the Water element.', 'Clod is an Earth element.', 'Gale is a Wind element.', 'Bernie Lumen is a Fire element.'])
add(1047, 'https://lumiere-a.akamaihd.net/v1/documents/inside_out_2_production_notes_updated_final_05-23-2024_f2901ceb.pdf',
    'Printed page 11, production designer Jason Deamer’s four new-emotion design descriptions',
    'Envy is teal and small, Anxiety orange with electric shapes, Embarrassment pink and giant, and Ennui shaped with limp, slumped posture.',
    ['Envy has the tiny teal design.', 'Anxiety has the orange electric design.', 'Ennui has the lanky limp-noodle posture.', 'Embarrassment is large and pink.'],
    challenge='Used the production designer’s explicit color/size account, not a color inference from another emotion or an unviewed image. Removed the unnecessary wide-eyed claim.')
add(1048, PX+'toy-story', 'Hamm, Rex and Slinky profiles; contrast Toy Story 3 Lotso profile',
    'Hamm is the piggy bank; Rex is a dinosaur and Slinky a dog toy. Lotso is a plush teddy bear from Toy Story 3 rather than Andy’s piggy bank.',
    ['Hamm is the piggy bank.', 'Rex is a plastic dinosaur.', 'Slinky Dog is a dog toy.', 'Lotso is a plush teddy bear.'])
add(1049, PX+'finding-nemo', 'Mr. Ray’s Class, Gill, Nigel and Turtles profiles',
    'Mr. Ray is the class’s teacher; Gill leads the tank gang, Nigel is the pelican who helps the search, and Crush is the turtle parent in the current.',
    ['Mr. Ray teaches the school class.', 'Gill leads the aquarium fish.', 'Nigel is the pelican helper.', 'Crush is the turtle parent, not the schoolteacher.'])
add(1050, 'https://www.sellingyourscreenplay.com/wp-content/uploads/screenplay/scripts/Ratatouille.pdf',
    'Printed screenplay pages 23-26 (PDF 24-27): spilled pot, Linguini’s additions, Remy seasoning it, soup served',
    'Linguini spills and ruins soup; Remy seasons and repairs it. The screenplay mentions leeks but does not establish a complete leek-and-potato recipe.',
    ['Soup is explicitly the spilled and repaired dish.', 'Risotto is not the dish in this sequence.', 'Souffle is not the dish in this sequence.', 'Roast chicken is not the dish in this sequence.'],
    challenge='Rejected unsupported recipe specificity: leeks are mentioned but that does not prove potato content or a fixed recipe name. The final dish-level question is fully supported.')

# Supporting passages, independently read or reusable notes explicitly inspected.
extras = {
 'b19-mulan-primary': ('https://disney.go.com/disneyrecords/mulan/index.html', 'Sound clips/song titles', 'Disney lists Honor to Us All, Reflection, I’ll Make a Man Out of You and A Girl Worth Fighting For as distinct Mulan songs.'),
 'b19-schwartz': ('https://stephenschwartz.com/wp-content/uploads/2017/05/DisneyHunchbackMovie.pdf', 'Out There, printed pages 4-5', 'Schwartz describes imagining Quasimodo looking at the city from his bell tower while writing Out There.'),
 'b19-odie-primary': ('https://www.disneyplus.com/en-au/browse/entity-7b60e41d-9ab3-4d73-8f5e-3cd72e64fcea', 'Details', 'Disney’s song description identifies Mama Odie and Dig a Little Deeper, performed by Jenifer Lewis and the Pinnacle Gospel Choir.'),
 'b19-raya-primary': ('https://music.amazon.com/podcasts/4b5b8694-6c34-46e3-b4e4-eea006a88a8b/episodes/7d62a6d1-eb8f-4cb4-b329-2c64a584af9a/disney-for-scores-james-newton-howard', 'Disney For Scores episode description', 'Disney’s podcast description identifies James Newton Howard’s Raya and the Last Dragon score.'),
 'b19-ksbe': ('https://www.ksbe.edu/assets/annual_report/annual_report_2002.pdf', 'Children’s Chorus soundtrack participation paragraph', 'Kamehameha Schools reports recording He Mele No Lilo and Hawaiian Roller Coaster Ride for the 2002 film.'),
 'b19-plot-toy4': (PX+'toy-story-4', 'Gabby Gabby, Bo Peep and Giggle profiles', 'Gabby has a faulty voice box and seeks a replacement; Bo is a porcelain lamp figure and Giggle a miniature policewoman.'),
 'b19-cars': (PX+'cars', 'Doc Hudson profile', 'Doc is a Hudson Hornet with a racing past, serving as Radiator Springs’ doctor and judge.'),
 'b19-inside-primary': (PX+'inside-out', 'Headquarters, Long Term Memory and Islands of Personality', 'Headquarters contains the emotions; significant core memories power Riley’s personality islands.'),
}
for sid, (url, loc, evidence) in extras.items():
    library['sources'][sid] = dict(url=url, locator=loc, evidence=evidence,
        checkedBy='Codex', checkedAt='2026-11-07', timeSensitive=False,
        nextReviewAt=None, topics=['Batch 19'], limitations='Text inspected; no audio/video playback claimed.')
for qid, sid in [(1010,'b19-mulan-primary'),(1008,'b19-schwartz'),(1014,'b19-odie-primary'),(1020,'b19-raya-primary'),(1013,'b19-ksbe'),(1040,'b19-plot-toy4'),(1026,'b19-cars'),(1034,'b19-inside-primary')]:
    data[qid][0].append(sid)

checks = ['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
assert len(data) == 44
for review in notes['reviews']:
    qid = review['questionId']
    refs, reasons, challenge = data[qid]
    review.update(checks=checks, notes='Reviewed final wording and all four options. Read the complete union of all 32 packet topic digests (813 unique context questions), including music/Pixar categories and film-specific context, plus cross-bank named-entity matches. Retained facts differ from related character, production, song and location facts. Categories and recall difficulty fit the final version. No real-TV or unbounded-current-status trivia.',
        context='Original English-language theatrical film named in the final question; historical released-film fact.', timeSensitive=False, nextReviewAt=None)
    review['premise'] = dict(reason=library['sources'][refs[0]]['evidence'], sources=refs)
    for i, option in enumerate(review['options']):
        option.update(basis='direct' if i == 0 else ('exhaustive-list' if qid == 1012 else 'exclusive-inference'), reason=reasons[i], sources=refs)
    review['challenge'] = dict(reviewer='Codex', at='2026-11-07', premiseChecked=True,
        alternativesExcluded=True, notes=challenge or ('Rechecked the literal final question against the cited passage. ' + ' '.join(reasons) + ' The alternatives do not identify the same scene, entity, title or role.'))
notes['sourcesChecked'] = sorted({sid for r in notes['reviews'] for sid in r['premise']['sources']})
sources_path.write_text(json.dumps(library, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
notes_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Authored {len(notes["reviews"])} explicit reviews; {len(notes["sourcesChecked"])} source passages.')
