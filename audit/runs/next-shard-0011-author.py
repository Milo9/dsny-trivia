"""Explicit evidence authoring for batch 11; does not edit question shards."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

plan = read('audit/runs/next-shard-0011-plan.json')
at = '2026-11-07'
library = read('audit/source-notes.json')
def source(key, url, locator, evidence, topic, limitations='', changing=False):
    library['sources']['b11-'+key] = dict(url=url, locator=locator, evidence=evidence,
        checkedBy='Codex', checkedAt=at, timeSensitive=changing,
        nextReviewAt='2027-02-04' if changing else None,
        limitations=limitations or 'Text inspected; no claim of film playback.', topics=[topic])

source('smee','https://d23.com/a-to-z/mr-smee/','Complete character entry','Smee is Hook\'s first mate in Peter Pan.','Peter Pan')
source('queen','https://www.disneystore.com/the-queen-of-hearts-off-with-their-heads-figure-by-jim-shore-%C2%A0alice-in-wonderland-028399484782.html','Product Details, Queen temperament paragraph','The Queen of Hearts is identified with her command to behead people.','Alice in Wonderland')
source('roses','https://filmmusiccentral.com/2018/02/16/alice-in-wonderland-painting-the-roses-red-1951/','Gardening mistake explanation, and Queen arrival paragraphs','Card gardeners cover mistakenly planted white roses with red paint, trying to avoid punishment; the Queen objects on discovering the deception.','Alice in Wonderland','Specialist scene commentary and reproduced dialogue inspected; corroborated by Disney\'s account linking the song to the 1951 film. No lyrics copied.')
source('rosesofficial','https://d23.com/alices-wonderland-bakery-is-painting-the-roses-red-in-this-exclusive-clip/','Opening and executive producer explanation','Disney identifies Painting the Roses Red as a song from the 1951 Alice film, connected to the Queen\'s preference for red.','Alice in Wonderland','Used only to corroborate original-film song/context, not to import television events into the film.')
source('dumbo','https://d23.com/a-to-z/dumbo-film/','Opening synopsis','Dumbo discovers that his oversized ears enable flight.','Dumbo')
source('ariel','https://d23.com/14-ultimate-fans-from-the-worlds-of-disney/','The Little Mermaid\'s Ariel: The Human World','Ariel\'s cavern collection expresses her fascination with humans and the world above the sea.','The Little Mermaid')
source('robin','https://d23.com/a-to-z/robin-hood-film/','Opening animal-cast description','Robin Hood and Marian are foxes; Little John is a bear; the royal brothers are lions.','Robin Hood')
source('dukas','https://d23.com/fantasia-at-80-exploring-ponchielli-and-dukas/','Dukas entry; Fantasia 00:28:48–00:39:06','Dukas\'s Sorcerer\'s Apprentice is the Mickey sequence about enchanted brooms.','Fantasia')
source('fantasiatracks','https://d23.com/a-to-z/fantasia-film/','Complete eight-sequence list','Original Fantasia uses Dukas for Apprentice, Mussorgsky for Bald Mountain and Tchaikovsky for Nutcracker; its Beethoven selection is Pastoral Symphony.','Fantasia')
source('merlin','https://d23.com/a-to-z/sword-in-the-stone-the-film/','Merlin teaching Wart and Mim confrontation paragraphs','Merlin teaches Arthur, who lives with Ector; Mim is the hostile rival magician.','The Sword in the Stone')
source('tony','https://d23.com/a-to-z/tony/','Complete character entry','Tony owns the Italian restaurant serving Lady and Tramp spaghetti, with help from Joe.','Lady and the Tramp')
source('oliver','https://d23.com/a-to-z/oliver-company-film/','Opening adaptation description','Oliver & Company adapts Oliver Twist, relocating it to New York with a kitten Oliver and human Fagin.','Oliver & Company')
source('brother','https://d23.com/a-to-z/brother-bear-film/brother-bear-1180w-600h/','Opening synopsis and cast list','The brothers are eldest Sitka, Denahi and youngest Kenai. Great Spirits transform Kenai into a bear; Koda is a bear cub and Rutt a moose.','Brother Bear')
source('treasure','https://d23.com/a-to-z/treasure-planet-film/','Opening literary-source, cook/mentor and pirate-reveal paragraphs; cast','Treasure Planet reimagines Stevenson\'s Treasure Island. Cyborg cook John Silver mentors Jim but is a mutinous pirate; Amelia is captain, Doppler the doctor, and B.E.N. the robot character.','Treasure Planet')
source('baymax','https://movies.disney.com/big-hero-6','The Characters: Baymax','Tadashi designed and built Baymax to provide healthcare; Hiro later makes him a hero.','Big Hero 6')
source('sisu','https://d23.com/go-behind-the-magic-with-the-raya-and-the-last-dragon-filmmakers/','Opening synopsis, 500 years later paragraph','Raya seeks Sisu, the surviving dragon, to restore Kumandra after the Druun return.','Raya and the Last Dragon')
source('magnifico','https://lumiere-a.akamaihd.net/v1/documents/1121_wish_production_notes_updated_final_11-20-23_8157ebfd.pdf','KING MAGNIFICO character section; Allison Moore explanation','Magnifico keeps citizens\' wishes in bubbles and withholds most of them to control Rosas.','Wish','Official 2023 production notes, character section inspected in indexed text.')
source('atlantis','https://clip.cafe/atlantis-the-lost-empire-2001/the-heart-of-atlantis/','Milo/Kida power-source dialogue, clip-relative 00:02–00:23','Milo identifies the life-sustaining crystal power source as the Heart of Atlantis.','Atlantis','Third-party film-dialogue transcription, read rather than video playback; corroborated by independent contemporary review.')
source('atlantisreview','https://www.decentfilms.com/reviews/atlantisthelostempire','New Age influences: Crystal spirituality','The review identifies the levitating life/technology power crystal by the film\'s Heart of Atlantis name.','Atlantis','Independent film criticism corroborates the exact dialogue and function; its religious opinions are not evidence used here.')
source('kuzco','https://d23.com/a-to-z/emperors-new-groove-the-film/','Opening plot and Yzma/Kronk roles','Kuzco becomes a llama in Yzma\'s plot; Kronk is her assistant and Pacha helps Kuzco.','Emperor\'s New Groove')
source('medusa','https://d23.com/a-to-z/rescuers-the-film/','Opening kidnapping and diamond paragraphs','Medusa kidnaps Penny to retrieve the Devil\'s Eye diamond.','The Rescuers')
source('basil','https://movies.disney.com/the-great-mouse-detective','Opening synopsis','Basil is the mouse-world counterpart to Sherlock Holmes in Victorian London.','The Great Mouse Detective')
source('henwen','https://d23.com/a-to-z/hen-wen/','Complete character entry','Hen Wen is the oracular pig in The Black Cauldron.','The Black Cauldron')
source('rhapsody','https://d23.com/a-to-z/fantasia2000-film/','Segment-by-segment synopsis, Gershwin entry','Rhapsody in Blue accompanies Jazz Age Manhattan in Fantasia 2000.','Fantasia')
source('hand','https://www.springfieldspringfield.co.uk/movie_script.php?movie=tangled','Campfire healing dialogue, lines 931–957; firewood exit 995–997','Flynn identifies his injured hand as Rapunzel wraps her hair around it; she performs the healing incantation.','Tangled','Secondary dialogue transcript inspected; corroborated by Disney Princess official clip title How Did Rapunzel Heal Flynn\'s Hand? Video playback unavailable. Specific body part is explicit, not inferred from generic healing ability.')
source('handclip','https://www.youtube.com/watch?v=X1OuGcgxzWo','Official Disney Princess clip title, How Did Rapunzel Heal Flynn\'s Hand?','The official clip identifies Flynn\'s hand as the object of Rapunzel\'s healing.','Tangled','Indexed official title corroboration only: full YouTube page fetch failed; no video playback claimed. Used with inspected complete dialogue passage.')
source('elsa','https://movies.disney.com/frozen','Opening synopsis and Elsa character description','Elsa\'s icy magic traps Arendelle in winter.','Frozen')
source('elsamaterials','https://en.wikipedia.org/wiki/Elsa_(Frozen)','Opening character description and quoted original Disney character biography','Elsa can create and manipulate ice and snow.','Frozen','Secondary explicit materials description corroborates Disney\'s winter/icy-power synopsis. No claim that these are her only possible abilities.')
source('hook','https://www.springfieldspringfield.co.uk/movie_script.php?movie=moana','Opening legend, lines 28–36','Maui changes his physical form with the magical fishhook.','Moana','Secondary transcript has typographical errors; core hook/form-change dialogue corroborated by Disney\'s own Maui profile/quote. No verbatim dialogue copied.')
source('mauiofficial','https://news.disney.com/moana-quotes','Maui quote introduction','Maui identifies himself as a shapeshifter.','Moana')
source('hawkmaui','https://www.gamesradar.com/entertainment/animation-movies/zootopia-2-has-a-surprise-moana-crossover-as-director-reveals-the-sequel-teasing-feather-was-borrowed-from-a-major-character-in-the-disney-movie/','Jared Bush account of Hawk Maui asset; explanation of the Moana form','The filmmaker identifies the hawk-form Maui asset from Moana, corroborating his bird transformation.','Moana','Filmmaker-interview/social-post reporting corroborates the form; the original opening dialogue independently establishes the fishhook form-changing mechanism.')
source('meeko','https://d23.com/a-to-z/pocahontas-film/','Opening companions paragraph','Meeko is the raccoon; Flit is a hummingbird and Kocoum a human warrior.','Pocahontas')
source('esmeralda','https://d23.com/a-to-z/hunchback-of-notre-dame-the-film/','Opening Quasimodo and Esmeralda romance paragraphs','Quasimodo falls in love with Esmeralda, who loves Phoebus.','The Hunchback of Notre Dame')
source('pooh','https://d23.com/re-live-these-ho-ho-home-video-classics-from-disney-christmases-past/','Winnie the Pooh Christmas account, what he wants most','The food Pooh most wants is honey.','Winnie the Pooh','Used for general character food preference, not a TV-episode trivia question.')
source('badge','https://www.rrauction.com/auctions/lot-detail/351701907490625-jiminy-cricket-production-cel-from-pinocchio/','Lot 625, Description','The original production cel is catalogued as Jiminy with his gold Official Conscience badge, received at the film\'s end.','Pinocchio','Primary artifact catalogue account; original film not played. Corroborated with detailed academic analysis of the final scene.')
source('badgeanalysis','https://qmro.qmul.ac.uk/xmlui/bitstream/handle/123456789/6859/JACOBSAnimatedEnchantment2014.pdf?sequence=1','Printed page 173, final Pinocchio scene description','At the ending Jiminy receives his gold badge as a reward after Pinocchio is restored.','Pinocchio','Academic analysis of the actual scene inspected in indexed full passage; no claim of personally examining film frames.')
source('scrooge','https://d23.com/a-to-z/scrooge-mcduck/','Opening identity sentence','Scrooge McDuck is Donald\'s rich uncle.','Disney characters')
source('max','https://d23.com/a-to-z/goofy-movie-a-film/','Opening fishing-trip synopsis and cast','Goofy takes his son Max on a road trip; Pete is a separate adult character.','A Goofy Movie')
source('chernabog','https://d23.com/a-to-z/chernabog/','Complete character entry','Chernabog is Fantasia\'s devil on Bald Mountain.','Fantasia')
source('clarabelle','https://d23.com/a-to-z/clarabelle-cow/','Complete character entry','Clarabelle is a bovine cartoon character, paired with Horace Horsecollar.','Disney characters')
source('major','https://d23.com/ask-dave/j-los-angeles-california/','Dave Smith answer, Cinderella horse sentence','Cinderella\'s horse is named Major.','Cinderella')
source('philippe','https://d23.com/a-to-z/philippe/','Complete character entry','Philippe is Maurice\'s horse in Beauty and the Beast.','Beauty and the Beast')
source('sebastian','https://d23.com/a-to-z/sebastian/','Complete character entry','Sebastian is a crab; his full name is Horatio Thelonious Ignacious Crustaceous Sebastian.','The Little Mermaid')
source('cave','https://news.disney.com/aladdin-quotes','Cave of Wonders heading and its lamp-only instruction','The named Cave of Wonders instructs the entrant to touch only the lamp.','Aladdin')
source('hans','https://thewaltdisneycompany.com/news/celebrating-10-years-of-disney-animations-frozen/','Opening story synopsis','Anna, Elsa, Kristoff and Olaf save Arendelle from Hans.','Frozen')
source('heihei','https://d23.com/news-briefs-july-27-2016/','Huge Moana News: character/cast announcement','Heihei is the rooster who stows away on Moana\'s canoe; Tamatoa is a crab and Tui Moana\'s father.','Moana')
source('judy','https://movies.disney.com/zootopia','Opening synopsis','Judy is the first bunny on the Zootopia police force; Nick is a fox.','Zootopia')
source('naveen','https://d23.com/app/uploads/2012/08/azsupp_082712.pdf','Princess and the Frog, The (film), opening synopsis','Prince Naveen is the frog Tiana kisses, becoming a frog herself.','The Princess and the Frog','Official Disney A to Z supplement, specific story entry inspected in indexed text.')
source('hyenas','https://www.lionkingexperience.com/inline/junior/sessions/15/provided-materials/Session%2015%20-%20Script%20Excerpt%20-%20Pride%20C.pdf','Scene 6, Elephant Graveyard, three-hyena entrance','The three hyenas are Shenzi, Banzai and Ed.','The Lion King','Official Disney stage education excerpt corroborates identities with original 1994 film cast entry; staging itself is not treated as original film evidence.')
source('lioncast','https://d23.com/a-to-z/lion-king-the-film/lion-king/','Original 1994 voice cast list','The original film credits Shenzi, Banzai and Ed as three named characters.','The Lion King')
source('clayton','https://d23.com/seven-swinging-facts-disneys-tarzan/','Brian Blessed paragraph','Clayton is the villainous hunter voiced by Brian Blessed.','Tarzan')
source('jumba','https://d23.com/10-favorite-disney-pets-for-national-love-your-pet-day/','Stitch (Lilo & Stitch) entry','Dr. Jumba Jookiba created Experiment 626, Stitch.','Lilo & Stitch')
source('nessus','https://ogcma.byu.edu/Nessus2.0001_ClementsMusker.htm','1997 character identification and first meeting with Meg discussion','The centaur Nessus is the opponent holding Meg when Hercules first encounters her.','Hercules','BYU classical reception analysis examines the film scene and differentiates it from classical mythology; corroborated by Disney\'s Jim Cummings voice credit.')
source('nessuscast','https://d23.com/a-to-z/cummings-jim/','Film voice credits','Jim Cummings voices Nessus in Hercules.','Hercules')
source('figaro','https://d23.com/a-to-z/figaro/','Complete character entry','Figaro is the kitten co-star in Pinocchio.','Pinocchio')
source('tree','https://disneyworld.disney.go.com/attractions/animal-kingdom/tree-of-life/','Title, opening iconic-symbol line, Alive with Natural Wonder','Tree of Life is the giant tree icon at Animal Kingdom.','parks',changing=True)
source('soarin','https://d23.com/get-ready-to-go-soarin-around-the-world/','June 17, 2016 dateline; opening debut and landmarks paragraphs','The reimagined U.S. Soarin\' experience debuted June 17, 2016 with global landmarks including the Great Wall.','parks')
source('soarinscenes','https://disneyworld.disney.go.com/attractions/epcot/soarin-around-world/','An Exhilarating Aerial Expedition; current-unavailability notice','Soarin\' Around the World simulates flight over global landmarks; Disney currently directs visitors to Across America instead.','parks',changing=True)
write('audit/source-notes.json', library)

# Each record below supplies independently authored premise, four option reasons,
# and final challenge. Expansion only supplies repeated schema scaffolding.
R = {}
def review(qid, keys, premise, reasons, challenge, notes):
    R[qid] = (keys.split(), premise, reasons, challenge, notes)

review(504,'smee','Hook\'s named first-mate role has a specific holder.',[
 'Smee is explicitly identified as Hook\'s first mate.', 'Tinker Bell is a different named individual, not the identified mate.', 'Tiger Lily cannot replace the explicitly named Smee in this role.', 'Wendy is not the identified first mate.'],
 'Tried interpreting first mate as a general companion; the naval role identifies Smee, rather than any of Peter\'s companions.', 'Distinct from Peter\'s fairy, Tiger Lily rescue and Darling-family questions.')
review(505,'queen','The quoted execution command identifies the film\'s ruler-villain.',[
 'Disney links the Queen of Hearts to this command.', 'The Mad Hatter is not the named royal speaker.', 'The Cheshire Cat is not the named royal speaker.', 'The White Rabbit is not the named royal speaker.'],
 'A character repeating another\'s words would not become the villain described; the attribution is to the Queen herself.', 'Villain/catchphrase identification differs from croquet, roses and tea-party facts.')
review(507,'ariel','Ariel\'s collecting passion is specifically directed toward the human world.',[
 'Disney explicitly identifies humans as her fascination.', 'Deep-sea fish do not describe the above-water human interest.', 'Polar wildlife is not the human civilization that inspires her collection.', 'Coral reefs are her underwater environment, not the world of human artifacts.'],
 'Removed gold coins, which can themselves be human artifacts. The revised alternatives identify separate subjects of fascination.', 'Retains the collection-interest fact while eliminating subset overlap; q704 identifies a song, not the world of interest.')
review(510,'robin','The 1973 animated character is portrayed as a particular species.',[
 'Disney explicitly lists Robin as a fox.', 'A wolf is a different species from the identified fox.', 'The bear is Little John rather than Robin.', 'A rabbit is not Robin\'s identified species.'],
 'No actor/voice interpretation survives the explicit animated-animal wording. Robin and Little John are different characters.', 'Easy species recall; distinct from Little John bear and Friar Tuck badger.')
review(514,'dukas fantasiatracks','The broom sequence has the Dukas composition as its soundtrack.',[
 'Dukas\'s Sorcerer\'s Apprentice accompanies Mickey and the enchanted brooms.', 'Mussorgsky accompanies Bald Mountain, a separate sequence.', 'Tchaikovsky accompanies Nutcracker imagery, a separate sequence.', 'Beethoven\'s Fifth is not the original film\'s Mickey selection; its Beethoven piece is Pastoral.'],
 'Removed Sorcerer\'s Apprentice from the stem. Other Fantasia selections cannot become this sequence simply by being in the anthology.', 'Composer/composition attribution is distinct from film release year, Fantasound and Chernabog identity.')
review(515,'roses rosesofficial','The gardeners conceal white roses by applying one paint color.',[
 'The scene account explicitly identifies red paint.', 'Blue is not the paint color used to conceal the mistake.', 'Pink is explicitly distinguished from the desired red in the scene.', 'Purple does not match the identified red paint.'],
 'The Queen wants red roses, not a paint deception; final wording assigns the painting to the card gardeners.', 'Clarifies the mistaken actor/purpose, not the keyed color. Cars q636 shares Red but describes a different object and film.')
review(516,'merlin','The wizard who teaches Wart is Merlin.',[
 'Merlin explicitly begins teaching Arthur.', 'Archimedes may help with lessons, but is not the wizard Merlin named in the source.', 'Mim is the hostile magician, not Arthur\'s mentor.', 'Ector is the guardian whose castle houses Arthur, not the teaching wizard.'],
 'Archimedes is a competing teacher only if wizard is ignored; Mim is magical but hostile. Both stem conditions matter.', 'Retains medium recall; pupil nickname q268 is distinct from mentor identity.')
review(517,'tony','The spaghetti meal takes place at Tony\'s establishment.',[
 'Tony is explicitly the proprietor of the restaurant serving the meal.', 'Mario\'s is a different owner/name from Tony\'s.', 'Luigi\'s is not the named Tony establishment.', 'Antonio\'s is not the film establishment\'s stated name, even if Tony can be a nickname for Antonio in real life.'],
 'Did not substitute the real park restaurant title. The question identifies the fictional film restaurant and source names Tony.', 'Restaurant is a shared noun, not a clue selecting among four Italian venue labels.')
review(518,'oliver','The film is explicitly an Oliver Twist adaptation.',[
 'Disney calls the film an Oliver Twist retelling.', 'A Tale of Two Cities is not the source novel identified for this film.', 'Great Expectations is not the identified source, despite being Dickens.', 'David Copperfield is not the identified source, despite being Dickens.'],
 'All four are Dickens novels, so author alone does not select the answer. Title resemblance is legitimate literary-adaptation context.', 'Distinct from New York setting, Dodger identity and Jenny adoption.')
review(520,'brother','Kenai\'s 2003 transformation is into a bear.',[
 'The synopsis explicitly describes transformation into a bear.', 'Wolf is not the resulting form, even though it occurs in the film\'s symbolism.', 'Deer is not the resulting form.', 'Eagle is not Kenai\'s transformed body.'],
 'The question asks his body, not a totem or spirit representation; those alternatives do not fit.', 'Distinct from his choice to remain a bear at the ending and Elinor\'s different transformation in Brave.')
review(521,'treasure','Disney identifies Stevenson\'s Treasure Island as the literary source.',[
 'Treasure Island is explicitly identified as the adapted novel.', 'Gulliver\'s Travels is not the credited source.', 'Robinson Crusoe is not the credited source.', '20,000 Leagues Under the Sea is not the credited source.'],
 'Science-fiction imagery does not make Verne\'s novel the adaptation source; retained title context is needed to identify the film.', 'Different from the 1950 live-action milestone and the 1974 preserve name, despite shared Treasure Island.')
review(526,'baymax','The question now asks Tadashi\'s original design purpose.',[
 'Tadashi built Baymax to care for patients.', 'Combat is a later modification, not Tadashi\'s original design role.', 'Teaching is not the specified healthcare purpose.', 'Patrolling for police is not the specified healthcare purpose.'],
 'Battle robot could fit the old unrestricted question after Hiro\'s upgrades; original design excludes that interpretation.', 'Parallel role options replace a notably longer correct answer; medium retained.')
review(527,'sisu','Raya\'s quest seeks the named surviving dragon Sisu.',[
 'Disney explicitly identifies Sisu as the dragon Raya seeks.', 'Namaari is not the dragon named Sisu.', 'The Druun are the threatening force rather than the named dragon.', 'Boun is not the dragon named Sisu.'],
 'Quest timing avoids implying no other dragons ever return; different names cannot fit the specifically identified sought dragon.', 'Distinct from land name Kumandra and Raya\'s homeland Heart.')
review(528,'magnifico','The king withholding citizens\' wishes is identified by name in production notes.',[
 'Magnifico\'s character section explicitly describes the hoarding.', 'Aldric is not the king named in that character account.', 'Florian is not the king named in that account.', 'Desmond is not the king named in that account.'],
 'Sought an alternative royal title/name; the production notes give Magnifico and explain the control motive directly.', 'Villain identity differs from Rosas, Star and Valentino facts.')
review(529,'atlantis atlantisreview','The life-sustaining power crystal is named in Milo\'s dialogue.',[
 'Milo names the power source the Heart of Atlantis.', 'Soul Stone is not the term in the identification passage.', 'Crystal of Power is a possible description, but not the name given in the film.', 'Blue Gem is a possible visual description, but not the name given in the film.'],
 'Tested descriptive labels against called: the question asks the explicit designation, not whether a crystal is blue or powerful.', 'Atlantis is necessary setting context; the other headword Heart must still be recalled.')
review(530,'kuzco','The dinner transformation gives Kuzco a llama body.',[
 'Disney explicitly identifies the llama transformation.', 'A frog is not Kuzco\'s resulting form after dinner.', 'A bear is not the resulting form after dinner.', 'A parrot is not the resulting form after dinner.'],
 'Removed imprecise direct agency: Kronk handles the vial/drink in Yzma\'s scheme. Later potion effects do not change the dinner result.', 'Distinct from Kronk\'s wrong-vial cause and Yzma\'s kitten outcome; q2380 is an unrelated Donald llama encounter.')
review(532,'medusa','Penny\'s kidnapper intends to exploit her to retrieve the diamond.',[
 'Medusa is explicitly the kidnapper seeking the Devil\'s Eye.', 'Cruella is not the woman named in this kidnapping.', 'Yzma is not the woman named in this kidnapping.', 'The Evil Queen is not the woman named in this kidnapping.'],
 'Other Disney villains cannot fit the specific Penny/diamond conjunction; no answer is based merely on being evil.', 'Distinct from the diamond name and rescue organization; difficulty remains hard for less familiar film.')
review(534,'basil','Basil is the rodent counterpart of Sherlock Holmes.',[
 'Disney explicitly compares Basil with Sherlock Holmes.', 'Poirot is not the stated model.', 'Marlowe is not the stated model.', 'Spade is not the stated model.'],
 'The inspiration is a detective character, not the author Eve Titus; q2499 asks a separate real-world author fact.', 'Replaces vague parody with inspired; medium recognition rather than hard.')
review(536,'brother','Sitka is identified as the eldest of the three human brothers.',[
 'Sitka is explicitly eldest.', 'Denahi is the other older brother, not the eldest.', 'Koda is the young bear companion, not a human elder brother.', 'Rutt is a moose, not Kenai\'s eldest brother.'],
 'The source orders all three brothers. Removing death-cause shorthand avoids confusing Sitka\'s sacrifice with a direct mauling.', 'Distinct from Denahi\'s revenge and Kenai\'s transformation.')
review(537,'treasure','The cyborg cook/mentor who reveals a pirate agenda is John Silver.',[
 'The synopsis explicitly combines all three roles in Silver.', 'Amelia is captain, not the cyborg cook.', 'Doppler is doctor, not the cyborg cook.', 'B.E.N. is the robot character, not the named cook/mentor.'],
 'The word villain allows Silver\'s moral complexity, but the cyborg cook condition still uniquely selects him.', 'Distinct from Morph identity, map form and source novel.')
review(538,'henwen','The film\'s oracular pig is named Hen Wen.',[
 'Hen Wen is explicitly the oracular pig.', 'Piglet is not that character\'s name.', 'Pumbaa is not that character\'s name.', 'Hamm is not that character\'s name.'],
 'All choices are plausible Disney/Pixar pig-associated names; none is a second name for Hen Wen in this film.', 'Replaced joke names with recognizable parallel distractors; main-canon film.')
review(539,'rhapsody','The film\'s Gershwin segment depicts Jazz Age Manhattan.',[
 'Disney assigns Manhattan to Rhapsody in Blue.', 'An American in Paris is a different Gershwin work, not the identified selection.', 'Porgy and Bess is not the identified Fantasia 2000 selection.', 'Summertime is not the identified selection.'],
 'A general New York association with Gershwin does not suffice; the film\'s actual selected score is explicit.', 'Distinct from other anthology pieces and original Fantasia\'s chronology.')
review(541,'hand handclip','The campfire scene identifies the body part wrapped in her hair.',[
 'Flynn explicitly refers to his injured hand as she wraps it.', 'The healing passage identifies hand rather than shoulder.', 'The identified wound is not on his knee.', 'The identified wound is not on his ankle.'],
 'Generic healing knowledge from q2134 cannot identify the body part; the final options require the specific scene. Excluded the later fatal torso wound by naming the campfire.', 'Focuses the existing healing question on a distinct observable detail; avoids claiming an exhaustive list of Rapunzel\'s powers.')
review(543,'elsa elsamaterials','Elsa\'s established magic creates the icy conditions of Arendelle.',[
 'Ice and snow match the explicitly icy winter magic.', 'Sand and dust are not the wintry materials identified.', 'Smoke and ash are not ice or snow.', 'Leaves and vines are not ice or snow.'],
 'The revised options compare material pairs instead of requiring proof that Elsa could never possess another ability.', 'Distinct from ice-palace construction, Olaf identity and Let It Go performance.')
review(544,'hook mauiofficial hawkmaui','Changing one\'s bodily form into an animal is shapeshifting.',[
 'The opening legend explicitly links changing form to the hook.', 'Mind reading accesses thoughts rather than changing the body.', 'Time travel changes temporal location rather than bodily form.', 'Invisibility conceals a body rather than changing it into a hawk.'],
 'Question asks the mechanism of a physical form-change, not an exhaustive claim about every power the hook has. Other abilities cannot explain becoming a different creature.', 'Distinct from hook retrieval in Lalotai and ocean wayfinding; hawk-form contextual example is corroborated in filmmaker reporting.')
review(546,'meeko','Pocahontas\'s raccoon companion is named Meeko.',[
 'The synopsis explicitly calls Meeko a raccoon.', 'Flit is the hummingbird, not the raccoon.', 'Percy is a separate named companion, not the raccoon identified as Meeko.', 'Kocoum is a human warrior, not the raccoon.'],
 'Companionship alone might include multiple animals; the raccoon condition selects Meeko.', 'Distinct from Flit hummingbird and Percy pug.')
review(547,'esmeralda','Quasimodo\'s romantic interest in the original film is Esmeralda.',[
 'The synopsis explicitly says he falls in love with Esmeralda.', 'Madeline is not the named romantic interest in this original film.', 'Colette is not the named romantic interest.', 'Isabelle is not the named romantic interest.'],
 'Later sequel romance must not be imported into the original film; Esmeralda\'s love for Phoebus does not negate Quasimodo\'s feelings.', 'Distinct from Phoebus identity and Frollo\'s position.')
review(553,'pooh','Pooh\'s characteristic favorite food is honey.',[
 'Disney identifies honey as what he wants most.', 'Apples do not replace the specified preferred food.', 'Berries do not replace the specified preferred food.', 'Acorns do not replace the specified preferred food.'],
 'A bear might eat other foods, but the question asks his established favorite, not everything he can eat.', 'General character trait; no television plot knowledge required.')
review(556,'badge badgeanalysis','The reward at the ending certifies Jiminy\'s official conscience status.',[
 'The artifact account and scene analysis identify a gold badge.', 'The reward is not an umbrella, even though Jiminy already carries one.', 'The reward is not the top hat he already wears.', 'The reward is not a whistle; Give a Little Whistle is a different association.'],
 'End-of-film timing excludes confusing the initial appointment/outfit with the later earned badge; no claim about pure-gold assay is made.', 'Difficulty raised to medium and reward timing clarified.')
review(562,'scrooge','The rich-uncle identification is explicit.',[
 'Scrooge is identified as Donald\'s rich uncle.', 'Gladstone is a different character, not the named rich uncle.', 'Gyro is not the named rich uncle.', 'Ludwig can also be an uncle, but is not the fabulously rich Scrooge described here.'],
 'Did not interpret this as only uncle; the wealth qualifier is necessary because Ludwig is also related.', 'Distinct from the activity of swimming in the Money Bin.')
review(563,'max','The 1995 theatrical film pairs Goofy with his teenage son Max.',[
 'The film synopsis names Max as his son.', 'Pete is a separately credited adult character.', 'Chumley is not the named son.', 'Junior cannot replace the Max identity specified for this film.'],
 'Film anchor excludes earlier Mr. Geef/Junior portrayals. Max the dog in q1117 is an unrelated character sharing a name.', 'Explicit theatrical anchor preserves no-real-TV-trivia scope.')
review(564,'chernabog','The named Bald Mountain devil is Chernabog.',[
 'Disney names Chernabog in this exact role.', 'Mephisto is not the name given for this film character.', 'Diablo is not this named Bald Mountain character.', 'Beelzebub is not this film character\'s proper name.'],
 'Generic demon synonyms are not alternative proper names in this specific film; source supplies the character identity.', 'Distinct from how the revelry ends and score composer.')
review(565,'clarabelle','Disney identifies Clarabelle as bovine.',[
 'Bovine establishes cow.', 'Horse is a different species, associated with Horace rather than Clarabelle.', 'Donkey is not bovine.', 'Sheep is not bovine.'],
 'Anthropomorphic behavior does not change the explicitly bovine design. The stem omits Cow so it does not supply its own answer.', 'General classic-character identity, not episode trivia.')
review(566,'major','The Archives answer names Cinderella\'s horse.',[
 'Major is the explicitly named horse.', 'Philippe is not this horse\'s name.', 'Maximus is not this horse\'s name.', 'Angus is not this horse\'s name.'],
 'Other Disney horses are plausible names, but the source uniquely assigns Major to Cinderella.', 'Distinct from dog Bruno and Fairy Godmother carriage transformations.')
review(567,'philippe','The original film\'s family horse is Maurice\'s Philippe.',[
 'Philippe is explicitly Maurice\'s horse.', 'Major is not that named horse.', 'Maximus is not that named horse.', 'Angus is not that named horse.'],
 'Ownership is now Maurice\'s, while Belle riding him is context rather than a competing ownership assertion.', 'Distinct from Cinderella\'s Major and Tangled\'s Maximus.')
review(569,'sebastian','Sebastian\'s species is explicitly crab.',[
 'Disney calls him a crab.', 'Lobster is a different crustacean from crab.', 'Shrimp is a different crustacean from crab.', 'Crayfish is a different crustacean from crab.'],
 'Replaced starfish, which was not even a crustacean. This now requires species recognition among crustaceans.', 'Easy character-species recall; full-name q579 is a separate fact.')
review(573,'cave','The lamp-only instruction belongs to the named Cave of Wonders.',[
 'Disney labels the speaker Cave of Wonders.', 'Cave of Secrets is not the supplied name.', 'Golden Cavern is not the supplied name.', 'Cave of Destiny is not the supplied name.'],
 'All choices could describe a magical cave generically; the official speaker heading establishes its proper name.', 'Moved place trivia to movies; distinct from entry qualification and forbidden-treasure consequence.')
review(575,'hans','The original Frozen story ends with the heroes saving Arendelle from Hans.',[
 'The company synopsis identifies Hans as the threat.', 'Kristoff assists the heroes rather than being that prince.', 'Erik is not the named prince threatening Arendelle.', 'Leon is not the named prince threatening Arendelle.'],
 'The Duke is another antagonist but is not among the named prince options; Hans is uniquely the royal betrayal.', 'Distinct from Hans\'s Southern Isles origin.')
review(576,'heihei','The 2016 cast announcement explicitly identifies the stowaway rooster.',[
 'Heihei is the rooster aboard the canoe.', 'Pua is not the named rooster.', 'Tamatoa is the crab, not the rooster.', 'Tui is Moana\'s father, not the rooster.'],
 'Removed useless because he contributes to the journey; factual stowaway description uniquely identifies him.', 'Neutral wording and 2016 anchor avoid remake/sequel drift.')
review(577,'judy','The synopsis explicitly identifies Judy as a bunny.',[
 'Bunny means rabbit.', 'The fox is Nick, not Judy.', 'Mouse is a different species.', 'Squirrel is a different species.'],
 'Her surname may hint at the answer but the actual species is explicitly established; police officer q204 is a different role fact.', 'Easy identity recall rather than medium.')
review(578,'naveen','The frog-prince Tiana encounters is Naveen.',[
 'The official supplement names frog-transformed Naveen.', 'Phillip is not that named frog prince.', 'Eric is not that named frog prince.', 'Charming is not that named frog prince.'],
 'A familiar prince name is insufficient: the source gives Naveen in Tiana\'s frog-transformation story.', 'Distinct from Naveen\'s kingdom and Tiana\'s mother Eudora.')
review(579,'sebastian','The ordered full-name entry fixes the word immediately preceding Sebastian.',[
 'Crustaceous immediately precedes Sebastian in the official full name.', 'Bartholomew is not in that position.', 'Reginald is not in that position.', 'Archibald is not in that position.'],
 'Equal-form single-word options remove the exceptionally long correct-answer clue. The full name was checked in order, not guessed from crab association.', 'Retains rare name-detail difficulty; no spelling variants affect the queried word.')
review(580,'hyenas lioncast','The named original-film trio is Shenzi, Banzai and Ed.',[
 'All three match the Disney trio and 1994 credits.', 'Nuka replaces Ed, so the trio is wrong.', 'Vitani replaces Banzai, so the trio is wrong.', 'Kovu replaces Shenzi, so the trio is wrong.'],
 'Checked every member, not just two familiar names; 1994 anchor excludes the remake\'s renamed hyenas.', 'Parallel mixed trios improve distractors; medium multi-name recall.')
review(583,'clayton','The original Tarzan hunter-villain is Clayton.',[
 'Disney calls Clayton the villainous hunter.', 'Kerchak is not the identified human hunter.', 'Terk is not the identified human hunter.', 'Professor Porter is an explorer but not the villainous Clayton.'],
 'Hunting could be used broadly for animals, but the named film villain condition selects Clayton, not Kerchak or a scientist.', 'Medium character recall; distinct from Sabor predator and gorilla leader.')
review(587,'jumba','Stitch\'s creator is explicitly Dr. Jumba Jookiba.',[
 'Disney identifies Jumba as the creator.', 'Pleakley is not the named scientist creator.', 'Gantu is not the named scientist creator.', 'Grand Councilwoman is not the named scientist creator.'],
 'Alien status alone is shared; creation of Stitch identifies Jumba exclusively.', 'Film character creation fact differs from experiment number and Lilo\'s family.')
review(588,'nessus nessuscast','The question names Hercules\'s first meeting with Meg, not a global first battle.',[
 'BYU identifies the centaur in this encounter as Nessus.', 'Chiron is not the film opponent identified in that encounter.', 'Pholus is not the identified opponent.', 'Eurytion is not the identified opponent.'],
 'All four are centaur names, removing the old species giveaway. Specific Meg encounter avoids unsupported first-monster chronology.', 'Retains hard minor-character recall; distinct from Hydra battle.')
review(589,'figaro','Pinocchio\'s named kitten character is Figaro.',[
 'Disney identifies the kitten as Figaro.', 'Felix is not the identified kitten.', 'Whiskers is not the identified kitten.', 'Mittens is not the identified kitten.'],
 'The 1940 film anchor excludes later Figaro ownership in Minnie shorts; none of the other labels names Geppetto\'s kitten here.', 'Medium rather than hard for a prominent named pet.')
review(596,'tree','The official attraction title identifies Animal Kingdom\'s tree icon.',[
 'The official name is Tree of Life.', 'Baobab describes a tree type, not the icon\'s official name.', 'World Tree is not the published name.', 'Life Tree reverses the actual title and is not the published name.'],
 'Asked the proper name, not the botanical inspiration; a baobab-like shape cannot make Baobab Tree a second official title.', 'Current landmark identity scheduled for recheck; separate from the theater show inside it.')
review(597,'soarin soarinscenes','The global flight experience debuted in June 2016.',[
 'Disney\'s dated debut article identifies Soarin\' Around the World.', 'Test Track is not the named global-flight debut.', 'Mission: SPACE is not the named global-landmark flight experience.', 'Living with the Land is not the named global-flight experience.'],
 'Present tense was stale because Across America is now offered. Historical June 2016 wording avoids assuming current film availability.', 'Distinct from pavilion location, California origin and Tokyo museum backstory.')

templates = read('audit/runs/next-shard-0011-final-template.json')
checks = ['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
filled=[]
for item in templates['reviews']:
    qid=item['questionId']
    if qid==506:
        continue
    keys,premise,reasons,challenge,notes=R[qid]
    keys=['b11-'+k for k in keys]
    item.update(checks=checks,notes=notes,context='Original released film/character continuity as named in the question; official park context where applicable.',timeSensitive=qid==596,nextReviewAt='2027-02-04' if qid==596 else None)
    item['premise']={'reason':premise,'sources':keys}
    item['options']=[dict(basis='direct' if i==0 else 'exclusive-inference',reason=reason,sources=keys) for i,reason in enumerate(reasons)]
    item['challenge']={'reviewer':'Codex','at':at,'premiseChecked':True,'alternativesExcluded':True,'notes':challenge}
    filled.append(item)
templates.update(reviewer='Codex',at=at,sourcesChecked=sorted({key for i in filled for key in i['premise']['sources']}),reviews=filled)
write('audit/runs/next-shard-0011-evidence-notes.json',templates)
print(f'Authored {len(filled)} explicit final-wording reviews.')
