"""Serialize Codex's inspected sources and separate final-wording challenges."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
packet = json.loads((ROOT / 'artifacts/question-audit/current.json').read_text(encoding='utf-8'))
OUT = ROOT / 'audit/runs/next-shard-0004-reviews'
OUT.mkdir(exist_ok=True)
S = {
 'oscar90': ('https://www.oscars.org/oscars/ceremonies/1990', '1990 ceremony header (March 26); Music (Original Song), complete winner/nominee list: Under the Sea, The Little Mermaid, Menken music/Ashman lyric.'),
 'oscar41': ('https://www.oscars.org/oscars/ceremonies/1941', 'Header dates ceremony February 27, 1941, honoring 1940 films; Music (Song) winner and Pinocchio two-win film listing.'),
 'mermaid': ('https://d23.com/a-to-z/little-mermaid-the-film/', 'Release paragraph dates animated film 1989; final paragraphs identify Under the Sea and original-score Oscars.'),
 'menken': ('https://disney.go.com/disneyrecords/Soundtracks/Beauty_on_Broadway/index.html', 'Opening credits explicitly distinguish composer Alan Menken from lyricist Howard Ashman for the film songs; additional stage lyrics are Tim Rice.'),
 'aladdin': ('https://d23.com/a-to-z/aladdin-film/', 'Songwriting paragraphs: Ashman collaborated with Menken; Rice supplied later lyrics. Best Original Score award paragraph.'),
 'score90': ('https://www.oscars.org/oscars/ceremonies/1990', 'Music (Original Score) winner is The Little Mermaid, Alan Menken; Original Song credits split Menken music and Ashman lyric.'),
 'score93': ('https://www.oscars.org/oscars/ceremonies/1993', 'Music (Original Score) winner: Aladdin, Alan Menken; Music (Original Song) identifies Menken music and Rice lyrics; film listing separately credits Ashman lyrics on Friend Like Me.'),
 'frozen': ('https://www.mtishows.com/disneys-frozen', 'Opening description explicitly identifies the original animated film songs as by Kristen Anderson-Lopez and Robert Lopez, separately from new stage songs.'),
 'moana': ('https://d23.com/d23-video/the-magic-makers-behind-the-music-of-moana/', 'Intro text explicitly names Mark Mancina, Lin-Manuel Miranda and Opetaia Foa\u2019i as the Moana music team; text inspected, not unplayed video.'),
 'encanto': ('https://www.disney.com.au/news/disney-encanto-home-is-where-the-magic-lives', 'Paragraph beginning It was the obvious: Miranda created the eight original songs.'),
 'bravesongs': ('https://www.awn.com/news/brave-soundtrack-available-june-19', 'Identified as a Walt Disney Records press release; THE SCORE and ORIGINAL SONGS sections credit Doyle, Mandel/Andrews and Mumford & Sons; full track list follows.'),
 'lion': ('https://disney.go.com/disneyrecords/Soundtracks/LionKing/index.html', 'Track 1 credits Carmen Twillie and separately Lebo M African vocals; track 11 is Elton John\u2019s separate Circle of Life recording.'),
 'mulan': ('https://disney.go.com/disneyrecords/mulan/index.html', 'Film soundtrack song list includes I\u2019ll Make a Man Out of You; credits Wilder/Zippel and Osmond/Salonga.'),
 'hercules': ('https://www.qobuz.com/us-en/album/hercules-alan-menken-disney-hercules-cast/kyhyjkyhcxhkc', 'Walt Disney Records 1997 English soundtrack; vocal tracks 1\u201312 list Gospel Truth, Go the Distance, One Last Hope, Zero to Hero, I Won\u2019t Say and A Star Is Born, with reprises; remaining tracks designated score.'),
 'tarzan': ('https://music.apple.com/es/album/tarzan-original-motion-picture-soundtrack/1437333655?l=en', 'Walt Disney Records 1999 soundtrack, complete 14-track listing; five original songs and reprises, with score tracks; no Mulan training song.'),
 'small': ('https://d23.com/a-to-z/its-a-small-world/', 'Opening: attraction moved from 1964\u201365 New York World\u2019s Fair; paragraph credits Richard M. and Robert B. Sherman with its repeated multilingual song.'),
 'smallpark': ('https://disneyland.disney.go.com/en_CA/attractions/disneyland/its-a-small-world/', 'One Song, Many Languages and Disney History, After All sections: Sherman brothers song commission and 1964\u20131965 New York fair origin before Disneyland in 1966.'),
 'toy': ('https://www.pixar.com/toy-story', 'Characters: Woody/Andy identify ownership; Sid and Sid\u2019s House identify the toy-torturing neighbor; The World / Pizza Planet identifies space-themed restaurant.'),
 'toydate': ('https://d23.com/a-to-z/toy-story-film/', 'Release paragraph: November 22, 1995. Opening identifies Andy\u2019s favorite toy Woody.'),
 'sid': ('https://d23.com/13-disney-characters-that-make-our-spines-tingle/', 'Sid Phillips from Toy Story subsection identifies full name, 1995 film and tormenting Andy\u2019s toys.'),
 'rat': ('https://www.pixar.com/ratatouille', 'Synopsis and Remy/Emile/Gusteau/Linguini character profiles; Gusteau profile identifies book and Ego downgrade; Chefs identifies Horst and Lalo as kitchen staff.'),
 'nemo': ('https://www.pixar.com/finding-nemo', 'Synopsis and The Tank describe dentist aquarium; Nigel profile identifies friendly pelican; Gill and Tank Gang profiles distinguish fish.'),
 'nemod23': ('https://d23.com/a-to-z/finding-nemo-film/', 'Opening explicitly identifies Sydney harbor dentist tank and Dory as a Regal Blue Tang; cast list separates Nigel/Gill/Bloat.'),
 'inc': ('https://www.pixar.com/the-incredibles', 'Mr. Incredible and Elastigirl profiles give Bob Parr and Helen Parr; The World / Nomanisan names villain\u2019s island, with Syndrome profile confirming island lair.'),
 'brave': ('https://www.pixar.com/brave', 'Synopsis and The Story of Brave / Merida profiles: heroine is Merida; mother Queen Elinor is transformed into a bear.'),
 'up': ('https://www.pixar.com/upfilm', 'A Dream of Adventure and Carl Fredricksen / Russell / Kevin / Dug / Charles F. Muntz profiles: balloon-house owner, explorer child, bird, dog and childhood hero are distinguished.'),
 'monsters': ('https://www.pixar.com/monsters-university', 'Mike Wazowski profile explicitly says green one-eyed monster. Oozma Kappa profile and Field Trip describe Mike/Sulley joining the OK group; ROR and PNK profiles distinguish rival houses.'),
 'monstersinc': ('https://www.pixar.com/monsters-inc', 'Mike Wazowski profile and named character portraits; Sulley, Randall Boggs and Roz profiles identify different characters; Celia is also one-eyed but is not among the four options.'),
 'cars': ('https://cars.disney.com/', 'Lightning McQueen character profile explicitly identifies number 95.'),
 'cars2': ('https://d23.com/have-you-spotted-these-9-easter-eggs-in-the-cars-universe/', 'Lightning\u2019s Number section states 95 refers to the year 1995; corroborates exact number independently of character homepage.'),
 'coco': ('https://www.pixar.com/coco', 'H\u00e9ctor, Santa Cecilia, Cemetery, Marigold Bridge and Las Ofrendas sections establish Day of the Dead setting; Ernesto de la Cruz profile explicitly calls him Miguel\u2019s idol.'),
 'sadness': ('https://d23.com/the-ins-and-outs-of-inside-out/', 'Filmmaker-panel report paragraph beginning The casting of Phyllis Smith identifies Sadness as the blue-hued emotion.'),
 'toy3': ('https://d23.com/a-to-z/toy-story-3-film/', 'Opening paragraphs: toys land at Sunnyside and try to escape; Lotso runs the center as a prison.'),
 'dory': ('https://www.pixar.com/finding-dory', 'Synopsis and Dory profile identify blue tang and California institute; The World / Marine Life Institute calls MLI the Jewel of Morro Bay.'),
 'doryscript': ('https://www.scripts.com/script-pdf-body.php?id=8194', 'PDF page index 53 (printed page 54/67), reunion dialogue immediately after institute speaker announcement: parents identify MLI as where Dory was born. Third-party dialogue transcription, not an inspected studio screenplay.'),
 'dorycor': ('https://en.wikipedia.org/wiki/Finding_Dory', 'Plot, institute/quarantine and Destiny paragraphs: Dory\u2019s childhood pipe-pal and undertow separation establish that the institute was her childhood home. Secondary corroboration of transcript.'),
 'wall': ('https://www.pixar.com/wall-e', 'Characters / EVE profile spells out Extra-Terrestrial Vegetation Evaluator.'),
 'bug': ('https://d23.com/a-to-z/bugs-life-a-film/', 'Opening synopsis explicitly identifies Hopper as leader of extorting grasshoppers; cast separately names Molt.'),
 'bugpixar': ('https://www.pixar.com/a-bugs-life', 'Hopper, Molt and Hopper\u2019s Hideout profiles distinguish leader from tagalong sibling.'),
 'olaf': ('https://d23.com/times-anna-and-elsa-melted-our-hearts/', 'Numbered items 1 and 6 explicitly identify the snowman built by young Anna/Elsa as Olaf.'),
 'tangled': ('https://d23.com/a-to-z/tangled-film/', 'Final sentence: Flynn\u2019s real name is Eugene Fitzherbert.'),
 'zoo': ('https://d23.com/a-to-z/zootopia-film/', 'Opening synopsis identifies Officer Judy Hopps, first bunny on police force.'),
 'belle': ('https://d23.com/tale-as-old-as-time-modern-fashion-sensibilities/', 'Opening paragraphs identify iconic yellow dress retained from 1991 animation; later paragraph distinguishes the blue village dress.'),
 'snow': ('https://d23.com/a-to-z/snow-white-and-the-seven-dwarfs-film/', 'Second plot paragraph: disguised Queen at cottage persuades Snow White to bite poisoned apple.'),
}

# Each entry supplies a source set and four separate option rationales.
D = {
158: (['oscar90','mermaid'], ['The Academy identifies this film as the winner for this song.', 'Not the film in the Academy\u2019s complete 1990 song results.', 'Not the film in the Academy\u2019s complete 1990 song results.', 'The sequel is not the 1989 film identified in the Academy\u2019s 1990 results.']),
159: (['menken','aladdin','score90','score93'], ['Menken is the composer; the three-film music attribution agrees with the song/score credits.', 'Not the composer credited for these films.', 'Ashman supplied lyrics, not Menken\u2019s musical compositions.', 'Not the composer credited for these films.']),
160: (['frozen','moana','encanto','bravesongs'], ['Licensed rights-holder description explicitly attributes the original Frozen film songs to the pair.', 'Moana\u2019s credited team is Miranda, Foa\u2019i and Mancina.', 'Disney attributes its eight original songs to Miranda.', 'WDR\u2019s press release credits other songwriters and Doyle, not the Lopez pair.']),
164: (['lion'], ['Track 1 credits Twillie as performer of the film version.', 'John performs the separate pop track 11, not the film\u2019s main English lead.', 'Not among the track 1 vocal credits.', 'Credited separately for African vocals, not the main English lead.']),
165: (['mulan','hercules','tarzan','lion'], ['WDR lists the song on Mulan\u2019s original soundtrack.', 'Its complete original vocal track list contains different songs, not this training number.', 'Its complete 14-track soundtrack has different original songs and reprises.', 'WDR\u2019s complete song list for this film does not contain the Mulan training number.']),
167: (['small','smallpark'], ['Both official histories place the original commission at the 1964\u201365 New York fair.', 'Seattle 1962 is a different event, not the documented origin.', 'Brussels 1958 is a different event, not the documented origin.', 'Montreal 1967 is a different event, later than the documented debut.']),
168: (['small','smallpark'], ['Both official sources explicitly name Richard and Robert Sherman.', 'Not the named author pair of this song.', 'Not the named author pair of this song.', 'Not the named author pair of this song.']),
169: (['oscar41'], ['The ceremony was held February 27, 1941.', '1940 is the film/eligibility year, not the ceremony year.', 'The Academy dates this win to the preceding ceremony in 1941.', 'The Academy dates this win four years earlier.']),
171: (['toy','toydate'], ['Woody is Andy\u2019s favorite toy in the explicitly scoped 1995 film.', 'The toy-abusing neighbor, not Woody\u2019s owner.', 'Later owner is outside the original-film scope; Andy is the explicitly identified original owner.', 'Not the owner identified by the original-film account.']),
172: (['rat'], ['Synopsis singles out Remy as the aspiring rat chef.', 'Profile distinguishes the food-loving brother from Remy\u2019s culinary ambition.', 'Human culinary hero, not the aspiring rat.', 'Human garbage boy and Remy\u2019s partner, not the rat.']),
173: (['nemod23','nemo'], ['Official synopsis explicitly locates the captured Nemo in a Sydney dentist aquarium.', 'Different institution and country from the stated capture destination.', 'Different institution and country from the stated capture destination.', 'Different institution and country from the stated capture destination.']),
174: (['nemod23','dory'], ['Both primary profiles identify Dory as a blue tang.', 'Nemo/Marlin\u2019s type, not the species explicitly assigned to Dory.', 'A distinct fish type, excluded by Dory\u2019s explicit blue-tang identity.', 'A distinct fish type, excluded by Dory\u2019s explicit blue-tang identity.']),
175: (['inc'], ['Mr. Incredible\u2019s profile names Bob Parr.', 'Different first name from the explicitly identified Bob.', 'Different first name from the explicitly identified Bob.', 'Different first name from the explicitly identified Bob.']),
176: (['brave'], ['Synopsis and character profile center the story on Merida.', 'Not the protagonist named in Brave\u2019s synopsis.', 'Not the protagonist named in Brave\u2019s synopsis.', 'Not the protagonist named in Brave\u2019s synopsis.']),
177: (['up'], ['Profile explicitly names Carl Fredricksen as the balloon-house adventurer.', 'Different character: the famous explorer Muntz.', 'Russell is the child stowaway; not the named elderly house owner.', 'Not the character named as the house owner in the profile.']),
178: (['monsters','monstersinc'], ['Pixar explicitly describes Mike as green and one-eyed.', 'A distinct character in the named portraits, not Mike.', 'A distinct character in the named portraits, not Mike.', 'A distinct character in the named portraits, not Mike.']),
179: (['cars','cars2'], ['Both primary accounts assign the exact number 95.', 'Different numeric identifier from the stated 95.', 'Different numeric identifier from the stated 95.', 'Different numeric identifier from the stated 95.']),
181: (['coco'], ['Holiday and ofrenda sections identify Day of the Dead as the central celebration.', 'Different holiday from the celebration driving this story.', 'Different holiday despite superficial skeleton/dead imagery.', 'Three Kings Day is distinct from the explicitly named Day of the Dead.']),
182: (['toydate'], ['Official initial release date is November 22, 1995.', 'Two years after the initial release.', 'Two years before the initial release.', 'Four years after the initial release.']),
183: (['toy','sid'], ['The neighbor who tortures toys is named Sid Phillips.', 'Not the original-film neighbor identified by the primary profiles.', 'Not the original-film neighbor identified by the primary profiles.', 'Not the original-film neighbor identified by the primary profiles.']),
184: (['inc'], ['Elastigirl\u2019s profile names Helen Parr.', 'Different first name from the explicitly identified Helen.', 'Different first name from the explicitly identified Helen.', 'Different first name from the explicitly identified Helen.']),
185: (['rat'], ['Gusteau is explicitly the author of Anyone Can Cook and Remy\u2019s inspiration.', 'The food critic who downgraded the restaurant, not the author.', 'Successor head chef, not Gusteau or the author of the book.', 'A member of the kitchen staff, not the identified author.']),
186: (['up'], ['Russell\u2019s profile identifies the child Wilderness Explorer.', 'The bird, not the human explorer child.', 'The dog, not the human explorer child.', 'The adult explorer Muntz, not Russell.']),
188: (['sadness'], ['D23\u2019s filmmaker report explicitly identifies Sadness as blue.', 'Not the color attributed to Sadness.', 'Not the color attributed to Sadness.', 'Not the color attributed to Sadness.']),
189: (['toy3'], ['D23 identifies Sunnyside as the center Lotso runs as a prison, from which the toys escape.', 'Final new home is not the Lotso-controlled escape location specified here.', 'Not the Lotso-controlled center identified in the synopsis.', 'Not the Lotso-controlled center identified in the synopsis.']),
190: (['dory','doryscript','dorycor'], ['Institute childhood is explicit in reunion dialogue and corroborated by childhood pipe-pal/undertow account; Pixar supplies Morro Bay, California.', 'Her later home with Marlin/Nemo, distinguished from institute childhood.', 'Not the childhood institute identified by dialogue and corroboration.', 'Not the childhood institute identified by dialogue and corroboration.']),
191: (['brave'], ['The Story of Brave explicitly says Elinor becomes a bear.', 'Different animal from the explicitly described transformation.', 'Different animal from the explicitly described transformation.', 'Different animal from the explicitly described transformation.']),
192: (['monsters'], ['OK and Field Trip sections explicitly connect the misfit group with Mike/Sulley.', 'Elite rival house; not the OK group they join together.', 'A different sorority, separately described by Pixar.', 'Different name and initials from the explicitly identified Oozma Kappa.']),
193: (['nemo','nemod23'], ['Pixar identifies Nigel as the dentist-window pelican; D23 confirms his name.', 'Not the named helper pelican in Pixar\u2019s profile.', 'A tank fish and its leader, not the pelican.', 'A Tank Gang fish, not the pelican.']),
194: (['wall'], ['Exact expanded designation in EVE\u2019s profile; hyphenation does not change the words.', 'Different words from the explicit designation.', 'Different words and omits Vegetation Evaluator.', 'Different words from the explicit designation.']),
195: (['coco'], ['Ernesto profile explicitly identifies him as Miguel\u2019s idol.', 'The skeleton partner and later revealed ancestor, not the idol named in the profile.', 'Not the explicitly named celebrity idol.', 'Not the explicitly named celebrity idol.']),
196: (['toy'], ['Pizza Planet section names the space-themed pizza parlor.', 'Not its explicitly identified proper name.', 'Not its explicitly identified proper name.', 'Not its explicitly identified proper name.']),
197: (['bug','bugpixar'], ['D23 explicitly names Hopper as gang leader.', 'Not the explicitly identified leader Hopper.', 'Pixar distinguishes tagalong brother Molt from Hopper.', 'The insect type is not the character\u2019s proper name Hopper.']),
198: (['inc'], ['The World section calls the island Nomanisan.', 'A description of whose island it is, not the proper name now requested.', 'A base description, not the island\u2019s proper name.', 'Not the proper name given in Pixar\u2019s island section.']),
199: (['rat'], ['Gusteau profile explicitly assigns the downgrade to critic Anton Ego.', 'The restaurant\u2019s founder, not the critic who downgraded it.', 'A kitchen chef, not the explicitly identified critic.', 'A kitchen chef, not the explicitly identified critic.']),
202: (['olaf'], ['Items 1 and 6 identify the sisters\u2019 childhood snowman as Olaf.', 'Not the snowman identified in that childhood scene.', 'Not the snowman identified in that childhood scene.', 'Not the snowman identified in that childhood scene.']),
203: (['tangled'], ['D23 explicitly gives Eugene Fitzherbert as Flynn\u2019s real name.', 'Different full name from the identity explicitly given.', 'Correct first name but wrong surname.', 'Different full name from the identity explicitly given.']),
204: (['zoo'], ['Opening synopsis explicitly identifies Judy as an officer on the police force.', 'Different profession from her stated job.', 'Different profession from her stated job.', 'Different profession from her stated job.']),
205: (['belle'], ['D23 identifies the iconic yellow dress from the 1991 animation.', 'D23 distinguishes the blue village outfit from the iconic dance dress.', 'Not the documented color of the dance dress.', 'Not the documented color of the dance dress.']),
206: (['snow'], ['The cottage plot paragraph explicitly identifies a poisoned apple.', 'A different fruit from the documented apple.', 'A different fruit from the documented apple.', 'A different fruit from the documented apple.']),
}

C = {
158: 'Challenged sequel reuse and soundtrack compilations: the final wording asks the unique 1990 Oscar-winning film, not whether a tune might be reused elsewhere. Complete Academy results identify only The Little Mermaid for this song.',
159: 'Challenged Ashman as a co-writer: composer and lyricist are different roles. Menken composed the music; the cited explicit credits distinguish Ashman and Rice as lyric collaborators. No claim that Ashman never wrote music elsewhere is needed.',
160: 'Challenged Moana and Brave rather than relying on absence in a Frozen synopsis. Their music teams are explicitly different in the primary introductions/press release; Encanto has Miranda original songs. Frozen stage source expressly identifies original film songs separately from stage additions.',
164: 'Challenged both actual alternative performers: Elton John has a separate pop recording and Lebo M sings the African opening. WDR track 1 splits Twillie from African vocals; main English lead and 1994 film scope exclude those interpretations. Zimmer is not in the track vocal list.',
165: 'Challenged song reuse across the four films. WDR names the Mulan training song; the complete released song lists for Hercules, Tarzan and Lion King exclude it. Hercules English WDR catalog is inspected through its vocal sequence, not the Japanese release returned by initial search.',
167: 'Challenged whether the attraction existed before the song or a different fair fits. The song was commissioned for the fair attraction, which was moved to Disneyland in 1966. Both official accounts specify New York 1964\u201365, ruling out all other named fairs.',
168: 'Challenged all three real Disney songwriting pairs: authorship is an explicit Richard/Robert Sherman attribution. Shortened the correct option to remove the explanatory-length clue; the other pairs are not alternate names for the brothers.',
169: 'Rechecked the underlying premise against the ceremony header and actual song winner entry. Film year 1940 is deliberately a distractor; the award ceremony was in 1941. 1942/1945 do not fit. This is a distinct ceremony-date fact from questions identifying the winning song or film.',
171: 'Challenged Bonnie because she really becomes Woody\u2019s owner in a sequel. The final wording pins the original 1995 film and Andy\u2019s ownership, excluding later ownership, Sid\u2019s temporary captivity and Al\u2019s theft.',
172: 'Challenged Emile because he is also a rat and supports Remy. Pixar explicitly contrasts his general appetite with Remy\u2019s chef ambition. Gusteau and Linguini fail the rat identity, not merely the ambition clause.',
173: 'Challenged research-lab confusion with the later Finding Dory institute. D23 explicitly states captured Nemo\u2019s dentist tank overlooks Sydney harbor, so all three institution/country alternatives fail. Address question 479 adds street-number recall and is not a reverse destination question.',
174: 'Challenged confusing Nemo\u2019s species or treating Blue as merely a color: primary sources explicitly say Regal Blue Tang. Clownfish, goldfish and angelfish are distinct types, not synonyms.',
175: 'Tried all three plausible Parr first names against the explicit Mr. Incredible identity; only Bob matches. Superpower question 634 tests a different attribute.',
176: 'Tried the three other heroines as alternate protagonists; Pixar centers this film on Merida by name. Scottish-setting and horse-name questions require different facts.',
177: 'Challenged Muntz as another elderly man, Russell as a passenger, and Asner as the voice performer: question asks the character who owns and flies the house. Pixar names Carl Fredricksen and distinguishes the other characters.',
178: 'Challenged the one-eye clue carefully: Celia is also one-eyed, but is not listed. The combined green/one-eyed description explicitly matches Mike; the three listed character portraits and profiles do not. This is an option-bounded answer, not a claim that no other one-eyed monster exists.',
179: 'Tried every numeric alternative; exact unique racing identifier 95 excludes 51, 43 and 7. Independent D23 number-origin discussion corroborates the official character profile.',
181: 'Challenged Halloween because both involve skeleton imagery. The film\u2019s ofrenda/bridge rules and cemetery celebration explicitly center Day of the Dead, not Halloween, Christmas or Three Kings Day. The question concerns the central holiday, not a claim that characters never celebrate another holiday.',
182: 'Challenged original release versus sequel or home-video date: D23 dates original theatrical release to November 1995. None of the three alternative years is that release year.',
183: 'Challenged later-series villains: the cruel human neighbor is explicitly Sid Phillips in the original film. Al, Stinky Pete and Lotso do not have that identity. Moved to easy as prominent antagonist recall.',
184: 'Tested the three alternative first names against Pixar\u2019s explicit Elastigirl civilian identity; Helen is unique. Bob\u2019s civilian identity is separate recall.',
185: 'Challenged Ego as another famous food authority and Skinner as head chef: Pixar names Gusteau as the Anyone Can Cook author, while assigning distinct critic/successor/staff roles to the alternatives.',
186: 'Challenged Kevin as a boy\u2019s name and Charles as another explorer: the official profiles distinguish bird, adult and dog from the young Wilderness Explorer Russell. Calibrated to easy character recall.',
188: 'Challenged purple glasses or gray mood language versus the character\u2019s design color. The filmmaker report explicitly calls the character blue-hued. Purple, green and gray are not alternate readings of that stated color. Calibrated to easy.',
189: 'Original wording could validly suggest Bonnie\u2019s final home. Final wording instead asks the Lotso-controlled location from which they escape, explicitly Sunnyside in D23. House, museum and toy store cannot fit that episode. Avoided asking what daycare, which would make only one option grammatical.',
190: 'Challenged later reef home versus childhood home and geographic alternatives. Pixar confirms MLI/Morro Bay/California, but not childhood by itself. Third-party film-dialogue transcription explicitly says born there; the independent plot account corroborates childhood pipe-pal and undertow separation. Direct studio screenplay unavailable: limitation retained rather than claiming the homepage alone proves childhood.',
191: 'Challenged intention versus outcome: Merida intends to change her mother, but the bear transformation is unintended. The primary story summary explicitly identifies Elinor as a bear; deer, wolf and fox do not fit. Cake question 1309 tests the mechanism/food, a different fact.',
192: 'Challenged Sulley\u2019s early association with elite ROR: the question asks the fraternity both Mike and Sulley join together. Pixar\u2019s OK field trip explicitly includes them. Rival ROR and separate sororities cannot fit that shared membership.',
193: 'Challenged Gerald as a possible different pelican rather than asserting every Gerald in the franchise is a sea lion. The helper/dentist-window bird is uniquely named Nigel by Pixar. Gill and Bloat are explicitly tank fish.',
194: 'Tested every expanded acronym verbatim. Extra-Terrestrial and Extraterrestrial differ only in spelling style; the three alternative word sequences do not match the explicit designation.',
195: 'Challenged H\u00e9ctor as true songwriter and ancestor: those later revelations do not make him the celebrity Miguel idolizes at the outset. The Ernesto profile expressly names Miguel\u2019s idol; Chicharr\u00f3n and Julio are not that named identity.',
196: 'Challenged a merely generic pizza-place description: Pixar explicitly names Pizza Planet and its space theme; each alternative is a different proper name. Park ride question 2633 adds a real attraction association and is not restaurant-name recall in the film alone. Reduced hard to medium.',
197: 'Challenged Molt as another named grasshopper and Thumper as a dangerous gang member. The source explicitly assigns leadership to Hopper and separates Molt. Grasshopper is the species, not the requested character name. Reduced hard to medium.',
198: 'Challenged Syndrome\u2019s Island as literally a true description. Final wording expressly asks the proper name, which Pixar labels Nomanisan. Omnidroid Base and Villain\u2019s Cove are not that proper name.',
199: 'Challenged whether any kitchen worker could review food: this asks the specific critic who gave the scathing restaurant review. Pixar attributes the downgrade to Anton Ego and identifies Gusteau/Horst/Lalo with different roles. Reduced hard to medium.',
202: 'Challenged animated adult Olaf versus the inanimate childhood model. D23 explicitly links the sisters\u2019 first snowman to the name Olaf. Marshmallow is a different creation; Frosty and Snowflake are not this childhood snowman\u2019s name.',
203: 'Tried every full name, including Eugene with a wrong surname. D23\u2019s explicit real-name sentence establishes Eugene Fitzherbert uniquely; Maximus question 231 tests the horse identity instead.',
204: 'Challenged temporary parking duty as a different job: it is still police work. D23 explicitly identifies Officer Judy on the police force; firefighter, teacher and journalist fail that stated profession.',
205: 'Challenged Belle\u2019s other clothing and live-action differences. Final scope specifies 1991 and the ballroom scene; D23 distinguishes the iconic yellow dress from the blue village dress. Pink/red are not the identified ballroom color.',
206: 'Challenged fairy-tale variants versus Disney\u2019s film and other fruit: D23\u2019s explicit cottage poisoning episode uses an apple. Pear, peach and plum are mutually distinct fruits. Disguise question 1353 asks a separate fact, not a fruit/name inverse.',
}

assert set(D) == {x['question']['id'] for x in packet['questions']}
for item in packet['questions']:
    qid = item['question']['id']
    keys, reasons = D[qid]
    r = copy.deepcopy(item['reviewTemplate'])
    r['reviewer'] = 'Codex'
    r['manual'] = {k: True for k in r['manual']}
    r['notes'] = 'Read all four options, full matching topic digests and cross-bank comparisons; checked wording, category, editorial difficulty and main-film scope. ' + C[qid]
    v = r['verification']
    v['context'] = item['question']['question']
    v['timeSensitive'] = False
    v['nextReviewAt'] = None
    sources = [{'url': S[k][0], 'locator': S[k][1]} for k in keys]
    v['premise'] = {'reason': reasons[0], 'sources': sources}
    v['challenge'] = {'reviewer': 'Codex', 'at': r['at'], 'premiseChecked': True, 'alternativesExcluded': True, 'notes': C[qid]}
    for i, opt in enumerate(v['options']):
        opt['reason'] = reasons[i]
        opt['sources'] = sources
        opt['basis'] = 'direct' if i == 0 else 'exclusive-inference'
    if qid == 165:
        for opt in v['options'][1:]:
            opt['basis'] = 'exhaustive-list'
    if qid in {160,172,185,186,192,193,199}:
        for opt in v['options'][1:]:
            opt['basis'] = 'contradiction' if qid != 192 or opt['answer'] != 'Eta Hiss Hiss (HSS)' else 'exclusive-inference'
    (OUT / f'{qid}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Saved {len(D)} final-wording reviews.')
