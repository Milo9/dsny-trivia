"""Expand the explicitly authored evidence below; does not edit question shards."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# id, passage locator, inspected evidence, three individual exclusions, final challenge
DATA=[
(801,'Queen instructs Huntsman before the forest sequence','The Queen orders the Huntsman to kill Snow White and bring back her heart in the box.',
 ['A crown is not the bodily proof demanded.','The mirror advises the Queen; it is not the demanded proof.','A necklace is not the heart demanded in the instruction.'],
 'Checked the demand rather than what the Huntsman actually delivers: the later pig-heart deception does not change the requested proof.'),
(802,'Road to school, Honest John and Gideon encounter; Pleasure Island recruitment later','Honest John interrupts the journey to school and sells an acting career; Gideon accompanies him. Lampwick and the Coachman belong to the later Pleasure Island episode.',
 ['Lampwick befriends Pinocchio on the Pleasure Island journey, after Stromboli.','Geppetto sends him to school and does not lure him away.','The Coachman organizes Pleasure Island rather than the first acting-career lure.'],
 'Gideon could fit the original broad question as an accomplice. Replaced that option with Geppetto and challenged the final initial-school-lure wording against the later recruitment.'),
(803,'Blue Fairy letter, before the underwater search','The letter tells Pinocchio that Geppetto has been swallowed by the whale Monstro.',
 ['Cetus is not the name given in the letter.','Bruno is not the whale named in the letter.','Neptune is not the whale named in the letter.'],
 'This is an exclusive named identity, not a claim about every whale in mythology; all three competing names fail the explicit naming.'),
(805,'Circus departure and Casey Junior song','The circus travels on Casey Jr.; the departure song names Casey Junior.',
 ['Cannonball Express is not the named circus train.','Circus Limited is not the named circus train.','Jumbo Line is not the named circus train.'],
 'Distinguished the train name from Mrs. Jumbo and from generic railway names. The explicit naming excludes all three alternative identifiers.'),
(806,'Friend Owl explains springtime courtship after Bambi matures','Friend Owl calls the springtime romantic state twitterpated and describes encountering a pretty face and losing one\'s head.',
 ['Moonstruck is a possible English synonym but not Owl\'s chosen word.','Love-bitten is not the word in Owl\'s explanation.','Springstruck is not the word in Owl\'s explanation.'],
 'Synonyms for infatuation would fit a general definition, but the question asks Owl\'s specific word. His explicit utterance excludes them.'),
(807,'Morning animal feeding; Fairy Godmother transformation; cast','Bruno is Cinderella\'s bloodhound; Major is the horse, Gus a mouse, and Lucifer the cat.',
 ['Major is her horse, not her dog.','Gus is one of the mice.','Lucifer is Lady Tremaine\'s cat.'],
 'Rechecked species and ownership rather than merely a familiar animal name: only Bruno is Cinderella\'s dog.'),
(808,'Opening park lesson and rabbit-hole chase','Alice follows the waistcoat-wearing White Rabbit into the hole before her Wonderland encounters.',
 ['The March Hare is encountered later at the tea party.','The Cheshire Cat is encountered inside Wonderland, not the initial chase.','The Dormouse is at the later tea party.'],
 'Alice later follows or listens to several characters. The before-entering context selects the White Rabbit alone.'),
(809,'Hook and Smee discuss the missing hand and ticking crocodile','Hook says the crocodile liked his hand and has followed him ever since, wanting the rest of him.',
 ['A giant squid is not the pursuing creature in the original Peter Pan; do not import the sequel.','A sea serpent is not the pursuer identified by Hook.','A shark is not the pursuer identified by Hook.'],
 'Checked the original Peter Pan story against the squid in Return to Never Land. Hook explicitly identifies the crocodile in the hand-and-clock scene.'),
(810,'Lady shows her new collar; opening neighborhood introductions','Lady\'s neighborhood friends are Jock and Trusty, a terrier and an elderly bloodhound.',
 ['Tito and Francis is a different pair of names, not the two identified neighbors.','Rutt and Tuke is a different pair, not Lady\'s named neighbors.','Max and Toby is not the pair introduced as these neighbors.'],
 'Jock\'s breed question #2480 asks an additional breed fact, whereas this asks the named pair; knowing either answer does not supply the other required answer.'),
(811,'Narrator introduces the fairies\' forest cottage and Aurora\'s sixteenth birthday','The fairies rear Aurora in a woodcutter\'s cottage and call her Briar Rose.',
 ['Rose Red is not the alias stated by the narrator.','Dawn Rose is not the alias stated by the narrator.','Woodland Rose is not the alias stated by the narrator.'],
 'Aurora is the princess\'s birth name, while Briar Rose is specifically the forest alias; similar rose names are not additional aliases in this sequence.'),
(812,'Pongo and Perdita after Scotland Yard fails; all-dog alert','Pongo proposes the Twilight Bark, called a gossip chain and the fastest way to send news; dogs relay the missing-puppy alert.',
 ['The Midnight Howl is not the network named in this exchange.','The Bark Brigade is not the network named in this exchange.','The Dog Signal is not the network named in this exchange.'],
 'A howl can be part of the relay, but that does not make Midnight Howl its proper name. The passage explicitly names Twilight Bark.'),
(813,'Merlin\'s lessons, moat fish episode before squirrels and bird flight','The lesson sequence transforms Wart into a fish first, then a squirrel and later a bird.',
 ['The bird transformation is later, after the fish and squirrel lessons.','The squirrel lesson follows the fish episode.','A rabbit is not the first lesson transformation; the fish scene establishes the first event.'],
 'Challenged first rather than merely any transformation. Read the complete Plot and the ordered fish, squirrel and bird dialogue passages; no numeric or sequence inference from a short synopsis alone.'),
(815,'First countryside encounter; journey to Paris; later alley-cat rescue','O\'Malley meets Duchess in the countryside and offers to guide her and the kittens to Paris. Scat Cat and his band join the later mansion rescue.',
 ['Scat Cat joins later in Paris and the rescue, not the first countryside offer.','Peppo is a band member, not the cat making the countryside offer.','Hit Cat is a band member, not the cat making the countryside offer.'],
 'All three band cats could help them return home under the original wording. The final question fixes the initial encounter and guide offer, excluding the later rescue helpers.'),
(816,'Prince John and Sir Hiss carriage scene; Plot and cast','Prince John occupies Richard\'s place while Richard is away on crusade; Hiss advises John, the Sheriff enforces taxation, and Little John aids Robin.',
 ['Sir Hiss is the adviser, not the ruler.','The Sheriff is a local official and tax collector under Prince John.','Little John is Robin Hood\'s ally opposing Prince John.'],
 'Local authority does not equal rule of England: the question asks who rules in Richard\'s absence, identifying Prince John alone.'),
(817,'Medusa and Snoops discuss Penny\'s cave search','Medusa explicitly demands the Devil\'s Eye diamond and forces Penny to retrieve it from the cave.',
 ['The Blue Diamond is not the jewel she names.','The Bayou Star is not the jewel she names.','The Queen\'s Tear is not the jewel she names.'],
 'Checked the specific jewel, not the swamp setting or other valuable stones. The explicit diamond name excludes the three alternatives.'),
(818,'Copper\'s arrival at Slade\'s home; Tweed confronts Amos Slade','Hunter Amos Slade owns Copper and Chief; Widow Tweed confronts him by name after he pursues Tod.',
 ['Chief Daniels is not the owner; Chief is Slade\'s older dog.','Tod Slade is not the owner; Tod is the fox.','Dinky Jones is not the owner; Dinky is the sparrow.'],
 'Kept Copper\'s owner separate from Tod\'s adopter Widow Tweed and from the dog Chief; the invented surname combinations do not identify the hunter.'),
(819,'Gurgi steals Taran\'s apple; companions and Morva witches in Plot','Gurgi is the small hairy creature who joins Taran. Fflewddur is a bard, Dallben the enchanter, and Orddu a witch.',
 ['Fflewddur is the human bard, not the small hairy creature.','Dallben is Taran\'s elderly enchanter guardian.','Orddu is one of the three witches at Morva.'],
 'The broad word creature could technically include humans, so checked the ordinary character-description sense: the small hairy companion is Gurgi, while all three alternatives have distinct human roles.'),
(820,'Opening kidnapping, Dawson meets Olivia, and arrival at Basil\'s home','Olivia Flaversham seeks Basil after Fidget kidnaps her father, the toymaker Hiram Flaversham.',
 ['Miss Bianca is not the child whose father Basil is asked to find.','Felicity Ratigan is not the named daughter in the kidnapping case.','Jenny Foxworth is not the child who brings Basil this case.'],
 'Dawson helps Olivia reach Basil but is not the girl asking about her father. The explicit daughter identity excludes all three alternative names.'),
(821,'Foxworth limousine discovery; Jenny tells Georgette her parents agreed','Jenny Foxworth takes in the kitten, names him Oliver, and announces that her parents will let her keep him.',
 ['Penny is not the girl who adopts Oliver.','Anita Radcliffe is not the Foxworth child.','Olivia Flaversham is not Oliver\'s adopter.'],
 'Jenny is the child adopter even though her parents authorize it; being adopted by the household does not make any other listed girl correct. #447\'s singer/scene and #1070\'s coat type test additional facts.'),
(822,'Ursula\'s human disguise and wedding barge vows','Ursula takes the human identity Vanessa; the wedding officiant addresses the bride by that name before the disguise breaks.',
 ['Marina is not the disguise\'s name.','Serena is not the disguise\'s name.','Cordelia is not the disguise\'s name.'],
 'Separated Ariel\'s stolen voice from the identity using it. The named human disguise is Vanessa, regardless of who supplies the voice.'),
(823,'Cody caught in the poacher\'s trap; Plot and cast','Percival C. McLeach kidnaps Cody and seeks Marahute; Cody identifies the trap owner as a poacher.',
 ['Commander Rourke is not the villain in this Australian rescue.','Amos Slade is not Cody\'s captor or this film\'s poacher.','Clayton is not the villain pursuing Marahute.'],
 'The alternatives can be villains or hunters in other films; the fixed film context and Cody/Marahute case exclude them.'),
(824,'Opening narration: enchantress, rose bloom and last petal','The enchanted rose blooms until the prince\'s twenty-first year; earning love before its last petal falls can break the curse.',
 ['A golden lily is not the flower described by the narrator.','A glass tulip is not the curse\'s flower.','A silver daisy is not the curse\'s flower.'],
 'The glass covering must not be confused with a glass flower. The rose itself measures the time; #1072 tests the love condition rather than the flower identity.'),
(825,'Prince Ali parade, chorus names the royal persona','The parade introduces Aladdin\'s disguise as Prince Ali Ababwa.',
 ['Prince Amir Agrabah changes the stated given name and realm into an incorrect persona.','Prince Aziz Ababwa changes Ali to the wrong name.','Prince Hakim of Shirabad is not the persona announced in the parade.'],
 'Asked the full assumed name, not merely Prince Ali. Difficulty is medium for surname recall; the other royal-sounding names do not match the introduction.'),
(826,'Opening presentation at Pride Rock; Simba tells Scar he will be king there','The royal lion family lives and presents its heirs at Pride Rock; Simba calls himself its future king.',
 ['The Elephant Graveyard is a forbidden destination beyond the family\'s home.','Kings Peak is not the named landmark.','Lion Mountain is not the named landmark.'],
 'Removed pride from the stem to avoid echoing the answer. Checked the actual home landmark, not a general name for the whole Pride Lands.'),
(827,'Pocahontas brings her necklace, marriage question and dream to Grandmother Willow','Grandmother Willow is the talking willow tree Pocahontas consults for guidance.',
 ['Mother Maple is not the name of the tree she consults.','Old Oak is not the name of the tree she consults.','Spirit Cedar is not the name of the tree she consults.'],
 'Tree species and kinship title form a specific character name. #1257 asks the guidance song, a separate fact from the tree\'s identity.'),
(828,'After childhood prologue, Quasimodo and the gargoyles discuss the celebration outside','Quasimodo leaves Notre Dame to attend the Festival of Fools, where the crowd initially crowns and then abuses him.',
 ['Feast of Bells is not the named celebration.','Notre Dame Day is not the named celebration.','Carnival of Saints is not the named celebration.'],
 'Removed at the start because the film opens with an earlier childhood prologue. Feast of Fools is a variant spoken by a gargoyle, but Feast of Bells is not that variant.'),
(829,'Plot, Hades\' staged Hydra encounter; Animation section on multiplying heads','Hercules fights the Hydra, which develops multiple heads during the fight; the production describes its computer-generated heads.',
 ['The Minotaur is not the monster growing multiple heads in that fight.','The Cyclops has one eye and is not the head-growing Hydra.','The Kraken is not the head-growing monster in the film.'],
 'Cerberus is also many-headed and thus challenged the old options. The final options and grows-during-battle wording isolate the Hydra. #2153 asks how many replacement heads, a separate numeric fact.'),
(830,'Training camp name exchange; Plot identifies fellow recruits','Mulan gives her assumed name as Ping; Ling, Yao and Chien-Po are other soldiers in the unit.',
 ['Ling is another recruit, not Mulan\'s alias.','Yao is another recruit, not Mulan\'s alias.','Chien-Po is another recruit, not Mulan\'s alias.'],
 'The film dialogue explicitly settles on Ping after Mushu\'s suggestions; the other three are real soldiers, not additional aliases.'),
(832,'Kuzco\'s introductory account of Pacha; Plot and cast','Pacha is the village leader who helps the llama Kuzco return to the palace; Kronk is Yzma\'s assistant.',
 ['Kronk can help at other moments but is not the village leader.','Rudy is the old man expelled for throwing off Kuzco\'s groove, not this leader.','Tipo is Pacha\'s son, not the leader helping Kuzco.'],
 'The role village leader is essential because Kronk also assists in the wider story. Final wording excludes him without claiming that he never helps Kuzco.'),
(833,'Milo and Kida formally introduce themselves before the city exploration','Kida introduces herself as Kidagakash, then offers Kida as the shorter name.',
 ['Kidanara is not the first name she gives.','Kidalani is not the first name she gives.','Kidastra is not the first name she gives.'],
 'Checked full first name, not her surname Nedakh or her father Kashekim. #2594 therefore tests a distinct person\'s name.'),
(834,'Lilo explains family to Nani; Stitch later repeats the principle','Lilo explains that ohana means family and links it to not leaving anyone behind.',
 ['Aloha is not the word she defines as family in this exchange.','Mahalo is not the word she defines as family.','Lanai is not the word she defines as family.'],
 'The question asks Lilo\'s explicit explanation rather than all possible Hawaiian kinship vocabulary; the other words do not match her utterance.'),
(835,'Doppler\'s observatory, Jim unlocks Billy Bones\' sphere','Billy Bones gives Jim a sphere; Jim unlocks it to project the star map to Treasure Planet.',
 ['The map mechanism is not a paper scroll.','The map mechanism is not a crystal sword.','The map mechanism is not a silver compass.'],
 'Distinguished the physical sphere from the projected holographic map and B.E.N.\'s later missing memory. Removed the unnecessary golden color claim.'),
(836,'Kenai agrees to travel with the cub; Koda introduces his name','The young bear introduces himself as Koda and becomes Kenai\'s traveling companion.',
 ['Sitka is Kenai\'s elder brother, not the young bear companion.','Denahi is Kenai\'s other human brother, not the cub.','Tuke is a moose, not the young bear companion.'],
 'Kenai himself is a transformed bear, but the question asks his young companion. The other names have distinct family/species roles.'),
(837,'Opening premise and cast: Maggie, Mrs. Calloway and Grace','The three heroines are dairy cows; their quest also includes a horse and other farm animals.',
 ['The horse Buck is a supporting ally, not one of the three heroines.','Goats are not the trio identified in the premise.','Pigs are not the trio identified in the premise.'],
 'Checked the three leading heroines rather than every animal on the farm. Recalibrated the basic species question from hard to easy.'),
(838,'School baseball game and winning pennant; Plot','Chicken Little joins the baseball team and wins the decisive game, briefly restoring his reputation and his father\'s pride.',
 ['Basketball is not the sport of the reputation-restoring match.','Soccer is not the sport of that match.','Football is not the sport of that match.'],
 'Other school activities do not answer the question: the baseball victory specifically changes how the town treats him.'),
(839,'Wilbur explains his father\'s motto while Lewis repairs the time machine','Keep moving forward is the Robinson motto Lewis learns, including learning from mistakes.',
 ['Never grow up is not the Robinson motto.','Dream it, do it is not the motto Wilbur gives him.','Believe in tomorrow is not the motto Wilbur gives him.'],
 'All four are plausible encouragements, but this is an explicit motto quotation, not a general interpretation of the film\'s message.'),
(840,'RV-park introduction of Rhino to Bolt and Mittens','Rhino introduces himself as a hamster and is a fan of Bolt\'s show.',
 ['Mittens is the cat; Rhino is not a cat.','Rhino is identified as a hamster, not a guinea pig.','Rhino is identified as a hamster, not a rabbit.'],
 'His comic claim of partly wolf ancestry does not change the character\'s depicted hamster species. This is theatrical-film character trivia; it asks no real television-show fact.'),
(841,'Louis questions the identity of the boat-in-tree voodoo lady; animator Deja masterclass section 3','Mama Odie lives in a boat stuck in a tree; animator Andreas Deja explicitly confirms this setting.',
 ['Her home is in the tree, not a cave beneath the bayou.','The boat is lodged in a tree, not floating on the river.','The bayou boat is not a New Orleans mansion.'],
 'A boat home could suggest a houseboat, but the stated tree location excludes the floating-river alternative. #1014 asks her song, not her dwelling.'),
(842,'Opening narration, annual lanterns after Rapunzel\'s abduction','The king and queen release lanterns on their missing daughter\'s birthday, hoping she will return.',
 ['The annual date is the princess\'s birthday, not the queen\'s.','It is not the king\'s birthday.','It is not the captain of the guard\'s birthday.'],
 'Made the answers parallel possessives and fixed the birthday being marked. The first lantern at her birth is distinct from the annual releases after she goes missing.'),
(843,'Ralph returns from Bad-Anon; surge protector checkpoint','Game Central Station is the power-strip hub through which characters move between arcade games.',
 ['Sugar Rush Station is not the hub name at the checkpoint.','Hero\'s Duty Gate is not that shared hub.','Arcade Junction is not the hub\'s name.'],
 'Removed game from the stem to avoid lexical answer echo. Other game locations are destinations, whereas the named hub connects the arcade worlds.'),
(844,'Elsa\'s Let It Go construction; Anna and Kristoff arrive at the palace','Elsa creates an ice palace on the North Mountain and stays there; Kristoff calls it a palace made of ice.',
 ['A bridge is an approach to the palace, not the home she makes there.','She does not establish a snow village as her home.','A frozen ship is not the mountaintop home.'],
 'Elsa really does create a bridge, so the old unqualified builds wording was vulnerable. Asking for her home selects the palace and excludes the approach bridge.'),
(845,'Hiro\'s science showcase pitch and Krei\'s offer afterward','Hiro introduces his microbots, demonstrates linked configurations controlled by a neural transmitter, and receives an offer from Krei.',
 ['Nanowings are not the invention Hiro introduces at this showcase.','Health pods are not his showcased invention; Baymax is Tadashi\'s healthcare robot.','Magnet boots are not the invention demonstrated in this pitch.'],
 'Checked the specific expo demonstration, not every later superhero tool Hiro builds. The pitch explicitly names microbots.'),
(846,'Gideon and Judy\'s parents identify toxic flowers; Doug\'s lab and Bellwether confrontation','Night howlers are toxic flowers; Doug makes the serum from them and darts predators. A rabbit can also be affected.',
 ['Moon lilies are not the flowers identified as the serum source.','Dusk daisies are not the flowers identified as the serum source.','Shadow orchids are not the flowers identified as the serum source.'],
 'Preserved mammals rather than predators-only because Uncle Terry is a rabbit. Distinguished flowers from the manufactured serum and made every option a flower name.'),
(847,'Maui explains the entrance to Lalotai before the Tamatoa encounter','Maui identifies Lalotai as the Realm of Monsters where Tamatoa has his hook; Moana enters and helps recover it.',
 ['Motunui is Moana\'s island home, not the realm of monsters.','Te Fiti is not the named realm where the hook is held.','Ahtohallan belongs to Frozen 2, not this destination.'],
 '#70 asks which crab lives there, adding Tamatoa\'s identity; this asks the destination of the hook-retrieval episode. The other location names cannot denote this realm.'),
(848,'Shank directs Ralph to BuzzzTube; Yesss promotes the viral videos','Yesss is BuzzzTube\'s head algorithm. Shank is the racer who sends them there, Spamley offers schemes, and KnowsMore handles searches.',
 ['Shank helps and gives the referral, but is a racer rather than BuzzzTube\'s algorithm.','Spamley is the pop-up salesman, not BuzzzTube\'s head algorithm.','KnowsMore is the search engine character, not the BuzzzTube algorithm.'],
 'Several characters help Ralph, so retained the specific head-algorithm role and named BuzzzTube to exclude Shank\'s real contribution.'),
(849,'Opening narration of unified Kumandra and the fractured present','Kumandra is the once-united land divided into regions including Heart, Fang, Spine, Talon and Tail.',
 ['Fangora is not the name of the whole land; Fang is a region.','Heartland is not the name of the whole land; Heart is one region.','Talonia is not the name of the whole land; Talon is a region.'],
 '#1098 asks Raya\'s particular homeland Heart, whereas this asks the larger land Kumandra. Different geographic levels require different facts.'),
(850,'Asha\'s home scene; Star gives the goat speech; official synopsis and cast','Valentino is Asha\'s pet goat, voiced by Alan Tudyk; Star is the cosmic wishing companion.',
 ['Star is the celestial companion, not her goat.','Sakina is Asha\'s mother, not her goat.','Dahlia is Asha\'s friend, not her goat.'],
 'Checked the animal identity rather than just a companion\'s name: Star and Dahlia help Asha, but only Valentino is the goat.'),
(851,'Doc Presentation and character model sheet; Kaufman excerpt on leadership','Doc wears round spectacles and acts as the dwarfs\' self-appointed leader; Grumpy, Sleepy and Bashful have different character traits.',
 ['Grumpy is the surly dwarf, not the bespectacled leader.','Sleepy is the perpetually tired dwarf, not the bespectacled leader.','Bashful is the shy dwarf, not the bespectacled leader.'],
 'Grumpy can lead opposition or influence the others, but does not satisfy the glasses attribute. The conjunction selects Doc alone.'),
]

film=read('artifacts/question-audit/b15-film-map.json')
library=read('audit/source-notes.json')
base=read('audit/runs/next-shard-0015-final-evidence-notes.json')
questions={q['id']:q for q in read('questions/q-004.json')}
templates={r['questionId']:r for r in base['reviews']}
ledger=read('audit/ledger.json')
allchecks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope']
scriptfix={811:'sleeping-beauty-1959',812:'one-hundred-and-one-dalmatians-101-dalmatians',816:'robin-hood-1973',817:'the-rescuers',819:'the-black-cauldron',824:'beauty-and-the-beast-1991',844:'frozen-2013'}
special={
825:[('https://www.springfieldspringfield.co.uk/movie_script.php?movie=aladdin','Prince Ali parade chorus'),('https://en.wikipedia.org/wiki/Prince_Ali_(song)','Synopsis of the original 1992 number, royal alter ego')],
829:[('https://www.filmeducation.org/pdf/film/hercules.pdf','Animation, printed page 14 / PDF page 15; Hydra computer animation'),('https://en.wikipedia.org/wiki/Hercules_(1997_film)','Plot and Animation sections')],
841:[('https://filmeducation.org/theprincessandthefrog/animation_masterclass_transcripts.html','Section 3, Andreas Deja: Mama Odie and Juju'),('https://andreasdeja.blogspot.com/2011/12/early-mama-odie.html','Opening character briefing and home setting')],
851:[('https://snowwhitemuseum.com/about-the-film/the-cast/doc/','Presentation, spectacles and self-appointed leader; model sheet'),('https://www.waltdisney.org/blog/seven-dwarf-days-doc','Kaufman excerpt, mid-October 1934 leadership description'),('https://www.disneyclips.com/characters/the-seven-dwarfs.html','Doc appearance; Grumpy, Sleepy and Bashful profiles')],
837:[('https://movies.disney.com/home-on-the-range','Synopsis, three determined cows'),('https://en.wikipedia.org/wiki/Home_on_the_Range_(2004_film)','Premise and voice cast')],
839:[('https://movies.disney.com/meet-the-robinsons','Synopsis, Lewis learns to keep moving forward'),('https://www.springfieldspringfield.co.uk/movie_script.php?movie=meet-the-robinsons','Wilbur explains his father\'s motto')],
849:[('https://movies.disney.com/raya-and-the-last-dragon','Synopsis, fractured Kumandra'),('https://www.springfieldspringfield.co.uk/movie_script.php?movie=raya-and-the-last-dragon','Opening history of Kumandra')],
850:[('https://movies.disney.com/wish','Synopsis and voice cast, Valentino the goat'),('https://en.wikipedia.org/wiki/Wish_(film)','Plot and voice cast')],
}

reviews=[]
for i,locator,evidence,wrong,challenge in DATA:
    wiki,slug,_=film[str(i)]
    refs=special.get(i,[('https://www.springfieldspringfield.co.uk/movie_script.php?movie='+scriptfix.get(i,slug),locator),('https://en.wikipedia.org/wiki/'+wiki,'Plot and Voice cast; '+locator)])
    sourceids=[]
    for n,(url,loc) in enumerate(refs):
        sid=f'b15-{i}-{n+1}'
        sourceids.append(sid)
        library['sources'][sid]={'url':url,'locator':loc,'evidence':evidence,'checkedBy':'Codex','checkedAt':'2026-11-07','timeSensitive':False,'nextReviewAt':None,'topics':['Batch 15',wiki],
          'limitations':'Text evidence inspected. No film playback claimed. Mirrored dialogue is not a studio-certified transcript; plot/cast corroboration was read separately. D23 A-to-Z pages returned a sign-in shell and are not used as newly verified evidence.' if i not in special else 'Named institutional, filmmaker or specialist text inspected and corroborated as listed; no film playback claimed.'}
    r=templates[i]
    # Final snapshots and hashes are supplied by a fresh template after edits.
    r['checks']=allchecks
    r['notes']='Full four-option question and complete topic/comparison context reviewed. Distinct tested fact retained; category and difficulty checked. '+challenge
    r['context']=locator
    r['timeSensitive']=False
    r['nextReviewAt']=None
    r['premise']={'reason':evidence,'sources':sourceids}
    r['options']=[{'basis':'direct','reason':evidence,'sources':sourceids}]+[{'basis':'exclusive-inference','reason':v,'sources':sourceids} for v in wrong]
    r['challenge']={'reviewer':'Codex','at':'2026-11-07','premiseChecked':True,'alternativesExcluded':True,'notes':challenge}
    reviews.append(r)
base['reviews']=reviews
base['sourcesChecked']=list(dict.fromkeys(s for r in reviews for s in r['premise']['sources']))
write('audit/source-notes.json',library)
write('audit/runs/next-shard-0015-reviewed-notes.json',base)
print('Authored',len(reviews),'explicit reviews; final template hashes must be current.')
