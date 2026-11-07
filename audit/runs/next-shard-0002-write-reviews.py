"""Serialize the reviewer's authored evidence; does not infer truth from checks."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_audit import review_template, validate_review

def d23(slug):
    return 'https://d23.com/a-to-z/' + slug + '/'

def src(url, locator):
    return {'url': url, 'locator': locator}

S = {
 'minnie': src(d23('minnie-mouse'), 'Opening sentence explicitly identifies Minnie as Mickey Mouse’s girlfriend.'),
 'nephews': src(d23('donalds-nephews-film'), 'First-film-appearance paragraph: Huey, Dewey and Louie visit their uncle Donald.'),
 'pluto': src(d23('pluto'), 'Opening two paragraphs: Mickey’s pet dog; explicit distinction from Goofy; earlier Rover identity belongs to Minnie.'),
 'tink': src('https://www.disneystore.com/movies-shows/disney/peter-pan/', 'Tinker Bell Classic Doll – Peter Pan – 10-inch product description, signature leafy green dress. Licensed design evidence corroborates the animated character; no claim about every later costume.'),
 'lion': src(d23('lion-king-the-film'), 'Opening three synopsis paragraphs: Scar’s murder and usurpation; Mufasa as king/father; Pumbaa as warthog; Timon as meerkat; Rafiki as guiding shaman.'),
 'zazu': src(d23('zazu'), 'Single character entry: Pride Lands chief of protocol.'),
 'gaston': src(d23('gaston'), 'Single character entry identifies the character courting Belle.'),
 'beauty': src(d23('beauty-and-the-beast-film'), 'First two synopsis paragraphs: vain suitor Gaston and his attack on the Beast.'),
 'snow': src(d23('snow-white-and-the-seven-dwarfs-film'), 'Opening synopsis: Snow White lives in the house of seven dwarfs; the jealous Queen pursues her.'),
 'dwarfs': src(d23('seven-dwarfs'), 'Entire entry is the complete seven-name roster: Doc, Sleepy, Happy, Grumpy, Sneezy, Bashful, Dopey.'),
 'sleep': src(d23('sleeping-beauty-film'), 'Opening synopsis and cast: evil fairy Maleficent, Prince Phillip, Aurora; release January 29, 1959.'),
 'maleficent': src(d23('maleficent'), 'Single character entry identifies Maleficent as the evil fairy in Sleeping Beauty.'),
 'eeyore': src(d23('eeyore'), 'Single character entry identifies Eeyore as the Pooh films’ donkey.'),
 'tigger': src(d23('tigger'), 'Single character entry identifies Tigger as a tiger.'),
 'kanga': src(d23('kanga'), 'Single character entry identifies Kanga as a kangaroo.'),
 'roo': src(d23('roo'), 'Single character entry identifies Roo as a baby kangaroo.'),
 'tremaine': src(d23('lady-tremaine'), 'Single character entry identifies Lady Tremaine as Cinderella’s evil stepmother.'),
 'goofy': src('https://d23.com/celebrating-disney-characters-who-are-mad-as-hatters/', 'Goofy subsection, immediately after Roger Rabbit: introductory Gawrsh expression associated with Goofy.'),
 'lucifer': src('https://d23.com/cinderella-added-to-national-film-registry/', 'Animation discussion contrasts Frank Thomas’s villainess with Ward Kimball’s cat Lucifer, the mice’s comical foil.'),
 'cat-owner': src('https://cinemacats.com/cinderella-1950/', 'Bad Kitty subsection explicitly identifies Lucifer as Lady Tremaine’s pet cat; secondary scene-based corroboration for ownership, which the D23 paragraph does not explicitly state.'),
 'phillip': src(d23('prince-phillip'), 'Single character entry gives Prince Phillip’s proper name and film.'),
 'meerkat': src('https://animals.sandiegozoo.org/animals/meerkat', 'Taxonomy header and ABOUT opening: Suricata suricatta, Herpestidae; member of mongoose family, with Timon identified as a meerkat.'),
 'warthog': src('https://animals.sandiegozoo.org/animals/warthog', 'Taxonomy header FAMILY Suidae and FAMILY LIFE section on boars, sows and piglets; explains why original Pig distractor overlaps.'),
 'eels': src(d23('flotsam-and-jetsam'), 'Entire character entry identifies the two named eels as Ursula’s henchmen.'),
 'hercules': src(d23('hercules-film'), 'Second synopsis paragraph explicitly identifies Pain and Panic as Hades’ two sidekicks; cast separately credits Charlton Heston as opening narrator.'),
 'chorus': src('https://d23.com/theres-no-chance-no-way-you-can-miss-out-on-these-d23-exclusive-hercules-pins/', 'Opening film-history paragraph describes the Muses as the traditional Greek chorus using gospel music.'),
 'tamatoa': src('https://d23.com/5-things-you-might-not-know-about-moana/', 'Word play subsection identifies shiny crustacean Tamatoa living in Lalotai beneath the ocean floor.'),
 'incredibles': src('https://movies.disney.com/the-incredibles', 'The Characters / Syndrome profile explicitly gives Buddy Pine as his other name.'),
 'buzz': src('https://ismbucket.s3.amazonaws.com/scriptLibrary/cleanscripts/TOY%20STORY.pdf', 'November 1995 final draft, PDF page index 25, bedpost jump immediately before rubber-ball bounce and Hot Wheels track; Buzz has one shouted line. Original screenplay on a third-party host, corroborated by Disney’s own quote attribution.'),
 'buzz-disney': src('https://news.disney.com/ultimate-list-toy-story-quotes', 'Buzz Lightyear subsection attributes To infinity and beyond to Buzz; Woody subsection attributes Reach for the sky to Woody.'),
 'imelda': src('https://www.pixar.com/coco', 'THE CHARACTERS / Mamá Imelda: director Lee Unkrich identifies her as the source of the family music ban; compare Abuelita and Mamá Coco profiles.'),
 'cobra': src('https://d23.com/giving-thanks-for-our-favorite-disney-families/', 'Lilo and Stitch subsection, following the ohana explanation: identifies Cobra Bubbles as the social worker in the sisters’ family circle.'),
 'lilo': src(d23('lilo-stitch-film'), '2002 animated-film entry and cast identifies Cobra Bubbles, voiced by Ving Rhames.'),
 'mice': src('https://d23.com/enchanting-cinderella-facts-fit-royalty/', 'Section 1: mouse helpers led by Jaq and Gus; other mouse names also discussed, so the question is about the main pair, not all mice.'),
 'tarzan': src(d23('tarzan-film'), 'Opening synopsis: Kerchak and Kala raise Tarzan; his companions are talkative gorilla Terk and elephant Tantor.'),
 'jungle': src(d23('jungle-book-the-film'), 'Opening synopsis: Baloo is a lovable bear; Bagheera a panther; Shere Khan a tiger; King Louie belongs to the apes.'),
 'kronk': src(d23('emperors-new-groove-the-film'), 'Opening synopsis contrasts peasant Pacha with Yzma’s muscular manservant Kronk; cast confirms name.'),
 'atlantis': src(d23('atlantis-the-lost-empire-film'), 'Opening sentence identifies young museum cartographer and linguistics expert Milo Thatch.'),
 'reptiles': src(d23('nero-and-brutus'), 'Entire entry names Madame Medusa’s pet pair Nero and Brutus and calls them crocodiles.'),
 'rescuers': src(d23('rescuers-the-film'), 'Second synopsis paragraph calls the two reptiles alligators, contrary to Nero and Brutus entry. Final question avoids choosing between these labels.'),
 'wdw': src(d23('walt-disney-world-resort'), 'Opening sentence locates resort near Orlando, Florida and gives October 1, 1971 opening.'),
 'castle': src('https://disneyworld.disney.go.com/attractions/magic-kingdom/cinderella-castle/', 'Page title and introduction identify Cinderella Castle as Magic Kingdom’s symbol; A Fairytale Come to Life locates its gateway at Fantasyland.'),
 'castle-land': src(d23('cinderella-castle'), 'Opening sentence: castle at entrance to Fantasyland in Magic Kingdom Park; distinguishes Disneyland’s Sleeping Beauty Castle later in the same paragraph.'),
 'small': src('https://disneyworld.disney.go.com/attractions/magic-kingdom/its-a-small-world/', 'Page title and opening description: boat ride with singing children representing the globe; historical section distinguishes 1964 World’s Fair and 1971 Magic Kingdom versions.'),
 'pirates': src('https://disneyworld.disney.go.com/attractions/magic-kingdom/pirates-of-the-caribbean/', 'A Pirate’s Life for You / main experience description: pirate raid on Caribbean seaport towns, not international children’s chorus.'),
 'haunted': src('https://disneyworld.disney.go.com/attractions/magic-kingdom/haunted-mansion/', 'A Spirited Tour: Doom Buggy, Ghost Host, haunted estate and graveyard; does not describe a children’s boat ride.'),
 'cruise': src('https://disneyworld.disney.go.com/attractions/magic-kingdom/jungle-cruise/', 'Opening description and main experience paragraphs: exotic-river boat trip with animals and skipper commentary.'),
 'animal': src(d23('animal-kingdom-disneys'), 'Opening synopsis: live animal encounters and habitats; Rafiki’s Planet Watch paragraph explicitly discusses conservation.'),
 'parks': src('https://disneyworld.disney.go.com/destinations/', 'Complete theme-park listing: Animal Kingdom, Hollywood Studios, EPCOT and Magic Kingdom.'),
 'sphere': src('https://disneyworld.disney.go.com/attractions/epcot/spaceship-earth/', 'Page title and A Landmark Attraction section: EPCOT flagship inside iconic geosphere, signature park symbol.'),
 'epcot': src(d23('epcot'), 'Opening paragraph gives October 1, 1982 park opening; later original-layout paragraph identifies Future World and World Showcase as areas.'),
 'epcot-history': src('https://d23.com/weve-just-begun-to-dream/', 'Walt Disney Archives account, opening paragraph dates public opening October 1, 1982; later paragraph calls Spaceship Earth a geodesic sphere.'),
 'everest': src('https://disneyworld.disney.go.com/attractions/animal-kingdom/expedition-everest/', 'Page title, introduction and Yeti or Not, Here He Comes section describe Himalayan train coaster and Yeti encounter.'),
 'pirates-land': src(d23('pirates-of-the-caribbean'), 'Second paragraph separately places Magic Kingdom version in Adventureland, opened December 15, 1973; Disneyland version is in New Orleans Square.'),
}

# id: (sources, source-backed premise, reasons in final answer order,
#      explicit final challenge, distinctness/editorial note)
R = {
51: (['minnie'], 'Disney’s character reference explicitly identifies Mickey’s romantic partner as Minnie.',
 ['Minnie is the identified girlfriend.', 'Daisy is a different named character, not the partner identified by this entry.', 'Clarabelle is a different character, not another name for Minnie.', 'Tinker Bell is a separate character, not Minnie.'],
 'Tested the husband/wife anecdote against the literal girlfriend wording: Disney itself uses girlfriend. The three alternative names are not aliases for Minnie. Mouse in the stem is an ordinary character surname, not a disclosed first name.',
 'No other question asks this romantic relationship; same surname is acceptable easy recall.'),
52: (['nephews'], 'In English-language Disney naming, the three nephews form the Huey/Dewey/Louie trio.',
 ['This exactly matches the complete named trio.', 'None of these three names is in the established trio.', 'The listed names do not match any of the three nephews.', 'This complete trio is not the English-language Huey/Dewey/Louie list.'],
 'Compared all three positions in each answer, including the similar-sounding Tick/Tack/Tock set. No alternative is an English alias list for this trio. The question concerns characters, not facts about a TV adaptation.',
 'Distinct from other named trios and Donald’s uncle; familiar basic characters justify easy.'),
53: (['pluto'], 'Pluto is identified as Mickey’s actual pet dog, expressly distinguished from Goofy.',
 ['The entry directly names Pluto as Mickey’s pet.', 'Rex is not the name of the pet identified here.', 'The source explicitly distinguishes Goofy from the actual dog character Pluto.', 'Spot is not Pluto’s name; the earlier documented alternate dog name was Rover, not Spot.'],
 'Challenged Goofy as another dog and Spot as a possible pet alias. Disney explicitly separates Goofy’s human-like role and documents Rover, excluding both proposed alternatives under this relationship.',
 'Distinct from Pluto’s debut-short history and the Peter Pan fairy identity.'),
54: (['tink'], 'The animated Peter Pan character’s signature dress design is green; the final stem fixes the 1953 film context.',
 ['The official Peter Pan product description expressly identifies the signature dress as green.', 'Blue is a different hue from the identified garment color.', 'Pink is not the signature green garment color.', 'Yellow is not the signature green garment color.'],
 'Rechecked actual garment color rather than fairy glow, wings or hair. The claim is scoped to the animated character design, not every park costume or later adaptation. The official licensed depiction supplies an explicit color, not an inference from a generic homepage.',
 'Ariel’s green tail q15 is a separate character-and-garment fact; fairy identity q285 does not give dress color.'),
55: (['lion','zazu'], 'Scar drives the murder, usurpation and final opposition to Simba.',
 ['Scar kills Mufasa and takes the throne, establishing him as the main antagonist.', 'Mufasa is Simba’s father and the murdered king, not the antagonist.', 'Zazu is the chief of protocol rather than the usurping villain.', 'Rafiki guides Simba toward his rightful role rather than opposing him.'],
 'Tried treating a stern father, adviser or shaman as a villain. Their documented functions differ from Scar’s deliberate murder and usurpation; none rivals him as the film’s main antagonist.',
 'Distinct from Scar’s kinship q23 and Be Prepared’s song identity.'),
56: (['gaston','beauty'], 'Disney explicitly identifies Gaston as the vain man courting Belle.',
 ['Gaston is the named suitor.', 'Jafar is not Gaston, the suitor identified in this film.', 'Frollo is not the named suitor.', 'Hades is not the named suitor.'],
 'The question requests the suitor’s identity, not any villain from a Disney film. The source names that character unambiguously, and none of the alternative proper names is an alias for him.',
 'q567 asks Belle’s horse; q1384 asks which film contains the song Gaston. A character-romance fact and a soundtrack attribution require different knowledge.'),
57: (['snow','dwarfs'], 'Snow White takes refuge with a roster containing exactly seven dwarfs.',
 ['The complete roster has seven entries.', 'Five undercounts the complete roster by two.', 'Eight exceeds the complete roster by one.', 'Six undercounts the complete roster by one.'],
 'Counted the complete named roster against the refuge premise, rather than inferring from a title alone. Five, six and eight cannot describe this seven-person household.',
 'q81 tests membership rather than count; q2364’s seven credited musicians are unrelated.'),
58: (['maleficent','sleep','snow','tremaine'], 'Maleficent is the evil fairy in the 1959 Sleeping Beauty feature; final wording does not claim chronological first appearance.',
 ['The character entry and 1959 film synopsis agree on Sleeping Beauty.', 'Snow White’s persecutor is the Queen, not Maleficent.', 'Cinderella’s stepmother is Lady Tremaine, not Maleficent.', 'Bambi is not the Sleeping Beauty feature that introduces this named fairy.'],
 'Removed first to avoid asserting an unnecessary chronology from a role identification. The question is now an animated-film attribution among four titles. The official character entry names Sleeping Beauty, and none of the other proposed titles identifies that feature.',
 'q950 asks a widescreen production process. Knowing Maleficent’s film does not establish its cinematographic process.'),
59: (['eeyore','tigger','kanga','roo'], 'Among the Pooh characters listed, Eeyore is the donkey.',
 ['Eeyore is explicitly identified as the donkey.', 'Tigger is a tiger.', 'Kanga is a kangaroo.', 'Roo is a baby kangaroo.'],
 'Checked animal identity for every alternative rather than relying on a gloomy personality description. None of the three other animal types is a donkey.',
 'q300 asks the human friend Christopher Robin, a different relationship and animal identity.'),
62: (['tremaine'], 'The Cinderella stepmother’s established character name is Lady Tremaine.',
 ['Lady Tremaine is the explicitly named evil stepmother.', 'Maleficent is not another name for Lady Tremaine.', 'Ursula is not another name for the stepmother.', 'The Evil Queen is not the given name Lady Tremaine.'],
 'Tested whether generic evil-queen wording could fit the household role. The stem requests a name, and Disney’s explicit character identification fixes that name; the other villain names do not identify her.',
 'Distinct from the stepsisters’ names and Lady Tremaine’s cat.'),
63: (['goofy'], 'Disney associates the stylized Gawrsh expression with Goofy in its dedicated character subsection.',
 ['Gawrsh is the expression Disney uses to introduce Goofy’s subsection.', 'Oh boy is not the Goofy expression identified in that character introduction.', 'Wahoo is not the identified signature expression.', 'Shucks is not the stylized Gawrsh expression.'],
 'The question concerns a recognized signature expression, not a claim that Goofy never says any other exclamation. Comparing literal spellings and the character-specific attribution leaves Gawrsh as the defensible signature among these options.',
 'No duplicate expression question found in the character digest or all-shard search. Easy character recognition.'),
64: (['lucifer','cat-owner'], 'Lucifer is the cat in Cinderella; scene-based secondary corroboration explicitly connects him to Lady Tremaine.',
 ['Lucifer is identified as the stepmother’s pet.', 'Felix is not Lucifer’s name.', 'Tom is not the identified pet’s name.', 'Shadow is not the identified pet’s name.'],
 'D23’s separate Lucifer dictionary entry describes an unrelated Pluto short, so that entry was deliberately not used. The Cinderella-specific animation article plus ownership corroboration establish the relevant cat and exclude the three different names.',
 'Distinct from Cinderella’s dog Bruno, horse Major and Geppetto’s kitten Figaro. Ownership support has a documented secondary-source limitation.'),
65: (['phillip','sleep'], 'Sleeping Beauty identifies its prince by the proper name Phillip.',
 ['Prince Phillip is the explicitly named prince.', 'Prince Charming is not the proper name supplied for this prince.', 'Prince Eric is not the prince named by the Sleeping Beauty reference.', 'Prince Adam is not the prince named by the Sleeping Beauty reference.'],
 'Read name as the character’s proper identity, not a generic compliment such as charming. The character entry and film cast independently identify Phillip; the other three proposed proper names are different identities.',
 'Distinct from Aurora, the fairies, the villain’s raven and the curse mechanics.'),
66: (['lion','meerkat'], 'Timon is a meerkat; a meerkat belongs to the mongoose family.',
 ['Both the film synopsis and zoo reference identify Timon as a meerkat.', 'A prairie dog is not the identified meerkat.', 'An otter is not a meerkat.', 'A weasel is not a meerkat; resemblance does not make them the same animal.'],
 'Original Mongoose option was defensible as the broader family description, so it was replaced. Challenged the final alternatives for the same nesting problem: prairie dog, otter and weasel do not contain meerkat as a subgroup.',
 'q67 requests Pumbaa’s species, not Timon’s. Animal identifications require separate facts.'),
67: (['lion','warthog'], 'Pumbaa is a warthog, which is a member of the pig family.',
 ['The film synopsis explicitly identifies Pumbaa as a warthog.', 'A hyena is a different animal from a warthog.', 'A rhinoceros is a different animal from a warthog.', 'A hippo is a different animal from a warthog.'],
 'Original Pig overlapped the correct animal family and Wild boar was liable to be read broadly. Both were replaced. None of the final distractors is a broader label that includes warthogs.',
 'Distinct from Timon’s meerkat identity. This is distractor repair, not a correction to Warthog.'),
68: (['eels'], 'Disney’s entry identifies exactly two eel henchmen of Ursula by name.',
 ['Flotsam and Jetsam are the explicitly identified pair.', 'Scuttle and Slog is not this named pair.', 'Barnacle and Murk is not this named pair.', 'Slick and Sludge is not this named pair.'],
 'Compared both names in each pair, not merely a plausible nautical sound. The complete pair in the official entry excludes every other proposed pair.',
 'Distinct from Ursula’s identity, Scuttle’s name and the sequel’s henchman Undertow.'),
69: (['chorus','hercules'], 'The Muses function as the musical Greek chorus; the film also has an opening spoken narrator.',
 ['The Muses are explicitly identified as the musical Greek chorus.', 'The Fates are not the group identified as that chorus.', 'The Olympians are not the named musical chorus.', 'The Nymphs are not the named musical chorus.'],
 'Original broad narrators wording failed to distinguish Charlton Heston’s opening narration. Final wording asks for the musical Greek chorus, the precise function attributed to the Muses; none of the other groups supplies that chorus.',
 'q2150 asks the Muses’ musical genre; this asks which group fills a narrative role. Retain as separate identity and style facts.'),
70: (['tamatoa'], 'Disney identifies the shiny crustacean living in Lalotai as Tamatoa.',
 ['Tamatoa is the named resident crab.', 'Te Kā is not another name for the crab identified here.', 'Tui is not another name for Tamatoa.', 'Heihei is not another name for Tamatoa.'],
 'Removed the generic Maui’s rival answer, which could describe Tamatoa, and replaced the place-name answer with a character name. Final premise uses exactly the shiny resident and Lalotai relationship supported by the cited section; it no longer requires unlocated fishhook-possession evidence.',
 'q1386 asks the song title Shiny, not the Lalotai resident’s name. q847 asks which realm Moana enters, not the crab’s identity. Parallel final character-name options.'),
71: (['incredibles'], 'Disney’s Syndrome character profile explicitly gives Buddy Pine as his other name.',
 ['Buddy Pine is explicitly given in the Syndrome profile.', 'Oliver Sansweet is not the personal name given for Syndrome.', 'Gazerbeam is not Buddy Pine’s personal name.', 'Chad Brentley is not the name given for Syndrome.'],
 'Distinguished personal identity from superhero aliases and other named people. The explicit Syndrome/Buddy Pine identification excludes the three different proposed identities, without assuming that a short plot synopsis establishes every detail.',
 'Character category is permitted for Pixar characters. Distinct from the island lair and other superheroes’ real names.'),
72: (['buzz','buzz-disney'], 'The final draft gives Buzz’s shouted line directly before his bedpost jump in Andy’s room.',
 ['This is the line immediately preceding the specified jump.', 'This is not the shouted line at that exact cue.', 'This is not the bedpost-jump line; Disney’s quote list assigns this phrase to Woody.', 'This does not match the line at the specified screenplay cue.'],
 'Original famous catchphrase wording could invite other actual Buzz quotations. The final scene cue fixes a single utterance; read the line and subsequent bounce/track action together. Each distractor is excluded as a different utterance, not because Buzz could never say it elsewhere.',
 'Distinct from Buzz’s space-ranger identity and Star Command. Familiar line merits easy; screenplay is primary authored evidence on a third-party mirror.'),
73: (['imelda'], 'Pixar’s director explicitly names Imelda as the source of the Rivera music ban.',
 ['Imelda is the stated originator.', 'Coco is not the ancestor identified as the source of the ban.', 'Elena’s enforcement is not the original establishment attributed to Imelda.', 'Julio is not the person identified as the source.'],
 'Actively challenged Elena, who also forbids music in the story. Originally established now separates originating a rule from enforcing it. Pixar’s explicit origin attribution excludes Coco, Elena and Julio under that temporal wording.',
 'q664 asks which ancestor is Imelda, q1288 asks Elena’s identity, and q2177 asks the family trade; these are different facts.'),
74: (['cobra','lilo'], 'The animated 2002 film’s social worker is Cobra Bubbles.',
 ['Cobra Bubbles is the identified social worker and animated-film cast character.', 'Agent Hood is not the social worker identified in these references.', 'Mr. Big is not the identified social worker.', 'Officer Reynolds is not the identified social worker.'],
 'Fixed the animated 2002 context to exclude the changed social-services roles in the 2025 remake. Rechecked the family article’s direct role attribution, rather than using a cast name alone to prove occupation. None of the other proper names identifies this worker.',
 'Distinct from Nani’s name, David Kawena’s role and the alien officials; assess-care wording avoids implying that removing Lilo is his sole motive.'),
75: (['hercules'], 'The film synopsis gives Hades’ two sidekicks as Pain and Panic.',
 ['This exactly matches the named pair.', 'Fear and Dread does not match the named pair.', 'Chaos and Discord does not match the named pair.', 'Slime and Sludge does not match the named pair.'],
 'Read the complete two-character identification and checked both entries in each answer. The other paired abstract nouns are plausible invented names but are not alternate identities for the film’s sidekicks.',
 'Distinct from Hades’ villain identity, the Fates’ shared eye and unrelated character duos. Main theatrical feature is in scope.'),
76: (['mice'], 'The Cinderella mouse helpers are explicitly described as led by Jaq and Gus.',
 ['Jaq and Gus are the identified leading pair.', 'Tic and Tac is not the identified leading pair.', 'Nibbles and Chuck is not the identified leading pair.', 'Tom and Jerry is not the identified leading pair.'],
 'The source names additional mice, so it would not prove a claim that Cinderella has only two mouse friends. The actual wording says two main friends; the explicit leading-pair identification supports that narrower premise and excludes all alternative pairs.',
 'Distinct from Gus’s yellow shirt and the mice’s dressmaking action. Options are uniformly pairs.'),
77: (['tarzan'], 'The synopsis distinguishes talkative gorilla Terk from parental figures Kala/Kerchak and elephant Tantor.',
 ['Terk is the described talkative gorilla companion.', 'Kala is the adoptive mother figure, not the companion identified here.', 'Tantor is an elephant, not this gorilla.', 'Kerchak leads the gorilla family as Kala’s mate, not the described talkative companion.'],
 'The word friend alone could be stretched to include relatives. Final wording tracks the source’s talkative gorilla description; the source explicitly separates the parental pair and elephant. No unsupported childhood chronology is required.',
 'q29 asks the mother; q872 the elephant; q2296 the troop leader. Each is a separate character role.'),
78: (['jungle'], 'The Jungle Book synopsis distinguishes the friendly bear from the panther, tiger and ape king.',
 ['Baloo is the friendly bear.', 'Bagheera is a panther.', 'Shere Khan is a tiger.', 'King Louie is an ape, not a bear.'],
 'Did not assume that being friendly excludes Bagheera: animal identity is decisive. All three distractors have animal types that exclude bear under the literal wording.',
 'q2451 asks a specific sequel action. That action is independent of identifying the original film’s bear.'),
81: (['dwarfs'], 'The official seven-name roster includes Bashful, Grumpy and Dopey and excludes Jumpy.',
 ['Jumpy is absent from the complete seven-name roster, so it is correct for NOT.', 'Bashful is present, making this wrong for NOT.', 'Grumpy is present, making this wrong for NOT.', 'Dopey is present, making this wrong for NOT.'],
 'Reversed the verdict test to account for NOT, then compared every option against the exhaustive official list. This is not an inference from a short synopsis omitting a name.',
 'Count q57 and mute-character q286 test different facts. Basic roster recognition is easy rather than hard.'),
83: (['kronk'], 'Disney identifies Kronk as Yzma’s muscular manservant pursuing Kuzco.',
 ['Kronk is the identified muscular helper.', 'Pacha is the peasant helping Kuzco, explicitly contrasted with Yzma’s helper.', 'Bucky is not the named muscular manservant.', 'Tipo is not the manservant named in the synopsis.'],
 'Removed unqualified loyal and dim-witted character judgments. The final muscular henchman identification is directly supported; Pacha’s different allegiance is explicit and the two other proper names do not identify Kronk.',
 'Distinct from Kronk’s cooking, squirrel language and conscience figures. A main sidekick’s identity is medium, not obscure hard recall.'),
84: (['atlantis'], 'The opening synopsis identifies the young linguist/cartographer by name.',
 ['Milo Thatch is the named linguist and cartographer.', 'Lewis Robinson is not the expedition expert identified here.', 'Wilbur Robinson is not Milo Thatch’s identity.', 'Pleakley is not the named Atlantis cartographer.'],
 'Checked both professional descriptors in the source’s opening sentence. They attach to Milo Thatch, and no alternative is an alias for him; no inference from a generic film title was used.',
 'Distinct from the expedition’s funder, mechanic, commander and Milo’s voice actor. Lead-character name merits medium.'),
85: (['reptiles','rescuers'], 'Disney names Medusa’s pet pair Nero and Brutus; its two entries disagree on the precise crocodilian label.',
 ['Brutus and Nero is the same pair as Nero and Brutus, in reverse order.', 'Snap and Crunch is not the complete named pair.', 'Jaws and Rex is not the identified pair.', 'Fluffy and Spike is not the identified pair.'],
 'Challenged the animal premise against both D23 entries and found alligator/crocodile inconsistency. Pet reptiles remains true under either description. Pair order is immaterial; none of the three alternative pairs matches either canonical name.',
 'No other Medusa-pet name question found across shards. Retains hard for relatively obscure paired-name recall; neutral species wording is clarification, not an established factual correction.'),
86: (['wdw'], 'The resort is explicitly located near Orlando in Florida.',
 ['Florida is the stated US state.', 'California is not the state identified for this resort.', 'Texas is not the stated location.', 'New York is not the stated location.'],
 'Distinguished Walt Disney World from the original Disneyland resort. The full resort’s location is Florida, so the other mutually exclusive state options cannot also answer the question.',
 'Distinct from Disneyland’s Anaheim location. Geography is enduring; no unbounded operational claim.'),
88: (['castle','castle-land'], 'Magic Kingdom’s central castle is officially named Cinderella Castle.',
 ['Cinderella Castle is the official attraction name.', 'Sleeping Beauty Castle is the different Disneyland castle referenced in Disney’s comparison.', 'Aurora’s Palace is not this attraction’s official name.', 'Enchanted Castle is not this attraction’s official name.'],
 'Fixed location in the original wording is decisive: Disneyland’s Sleeping Beauty Castle does not become correct merely because it is also a Disney icon. The remaining names do not match the official Magic Kingdom name.',
 'Distinct from q110 at Disneyland, q94’s land and the suite/restaurant inside the castle.'),
90: (['small','pirates','haunted','cruise'], 'The Magic Kingdom boat ride with an international children’s chorus is it’s a small world.',
 ['The official introduction exactly describes this children’s boat ride.', 'Pirates depicts pirate raids on seaport towns, not this international chorus.', 'Haunted Mansion uses Doom Buggies for a haunted-estate tour, not this boat ride.', 'Jungle Cruise tours exotic rivers and animal scenes, not a singing children’s chorus.'],
 'Challenged Pirates and Jungle Cruise as other boats with human figures. Their documented defining scenes do not match the specified international singing children; Haunted Mansion additionally fails the boat requirement. Removed the World/world lexical clue.',
 'q692 tests World’s Fair origin. Historical origin and present ride experience are separate facts; park location now explicit.'),
91: (['animal','parks'], 'Animal Kingdom’s core experience combines live habitats, animal encounters and conservation education.',
 ['Animal Kingdom is the wildlife/conservation park described by Disney.', 'EPCOT is a different park in the complete theme-park roster, not the animal-habitat park identified here.', 'Hollywood Studios is a different park, not the identified wildlife park.', 'Typhoon Lagoon is not the wildlife theme park in Disney’s complete four-park roster.'],
 'Did not infer that EPCOT can never discuss conservation: the stem asks which park is centered on live wildlife habitats and conservation. Animal Kingdom’s documented overall identity supplies that distinction, rather than the existence of any one environmental exhibit.',
 'q103 and q348 test specific attraction locations, not the park’s defining wildlife purpose. Easy recognition.'),
92: (['sphere','epcot','epcot-history'], 'The officially named sphere attraction at EPCOT is Spaceship Earth.',
 ['Spaceship Earth is the attraction’s official name.', 'The Magic Orb is not the official name.', 'Epcot Globe is a descriptive nickname rather than the official attraction name.', 'Future World was an original park area, not the sphere attraction’s official name.'],
 'Original Epcot Globe option was potentially defensible as an informal label. Official name now makes the requested naming standard explicit. The historical Future World area cannot be substituted for its sphere attraction.',
 'Distinct from the ride system q912 and narrator q2221; does not assert that no one calls it a globe.'),
94: (['castle-land','castle'], 'Disney locates the castle at the entrance/gateway to Fantasyland.',
 ['Fantasyland is the land whose entrance the castle marks.', 'Adventureland is not the identified land.', 'Tomorrowland is not the identified land.', 'Liberty Square is not the identified land.'],
 'Read the official entrance/gateway location rather than guessing from the central hub’s proximity to several lands. Both official references identify Fantasyland; geographic nearness to other lands does not make their names correct.',
 'q779 asks the small-world boat ride’s land, a different attraction-location fact.'),
95: (['parks'], 'Disney’s complete destination listing identifies four Walt Disney World theme parks.',
 ['This exactly reproduces the four listed theme parks.', 'Universal replaces Animal Kingdom and is absent from Disney’s complete list.', 'Adventureland replaces Hollywood Studios; it is not a separately listed theme park.', 'SeaWorld replaces EPCOT and is absent from the four-park list.'],
 'Compared each four-item set against the complete official list, not just its first matching names. Every wrong option has one substitution, so shared correct items do not make an entire list correct. Water parks are outside the stated theme-park set.',
 'Distinct from locating one attraction or identifying a park theme. Answer lengths are sufficiently parallel.'),
97: (['epcot','epcot-history'], 'EPCOT Center opened to guests on October 1, 1982.',
 ['1982 is the documented public-opening year.', '1971 is not EPCOT’s opening year.', '1989 is not EPCOT’s opening year.', '1975 is not EPCOT’s opening year.'],
 'Distinguished public opening from later October dedication ceremonies and the 1966 EPCOT concept. Both official historical accounts agree on 1982; the other years cannot also identify that event.',
 'q687 concerns the resort’s 1971 opening and q102 Animal Kingdom’s 1998 opening: different establishments and events.'),
98: (['everest'], 'The official Animal Kingdom attraction is Expedition Everest, a Himalayan train coaster with a Yeti encounter.',
 ['Expedition Everest is the attraction named by the exact official experience description.', 'Mount Yeti is not the official attraction name.', 'Summit Plummet is not the named Himalayan train coaster.', 'Everest Explorer is not the attraction name.'],
 'Rechecked the full coaster experience rather than treating every mountain-themed name as correct. Only Expedition Everest matches the official title and train/Yeti description. The final stem removes the expedition word echoed by the answer.',
 'Distinct from the attraction’s opening year q357 and its Asia location q922.'),
100: (['pirates-land'], 'The Magic Kingdom Pirates of the Caribbean attraction is in Adventureland.',
 ['Adventureland is explicitly specified for the Magic Kingdom version.', 'Frontierland is not the land identified for that version.', 'Tomorrowland is not the stated location.', 'Liberty Square is not the stated location.'],
 'The source separately locates Disneyland’s version in New Orleans Square; the question explicitly says Magic Kingdom. Under that fixed park context the three other land names are excluded by the unique listed location.',
 'q886 and q2525 share Adventureland but concern different attractions at different international parks.'),
}

bank = {}
for path in (ROOT / 'questions').glob('q-*.json'):
    bank.update({q['id']: q for q in json.loads(path.read_text(encoding='utf-8'))})
expected = set(range(51, 101)) - {60,61,79,80,82,87,89,93,96,99}
assert set(R) == expected
out = ROOT / 'audit/runs/next-shard-0002-reviews'
reviews = []
for qid, (keys, premise, reasons, challenge, notes) in R.items():
    q = bank[qid]
    review = review_template(q)
    review['reviewer'] = 'Codex (OpenAI)'
    review['manual'] = dict.fromkeys(review['manual'], True)
    review['notes'] = notes + ' Checked all four final options, mobile wording, clue fairness, category, editorial difficulty and theatrical/character/park scope. Full topic digests and additional all-shard searches were used for distinctness; context questions are not approved by this review.'
    v = review['verification']
    v['context'] = ('Walt Disney World, specified park/attraction; current naming/layout at review date.' if q['category'] == 'parks' else 'English-language Disney character naming; original theatrical feature where a film is named. ' + q['question'])
    v['timeSensitive'] = qid in {88,90,91,92,94,95,98,100}
    v['nextReviewAt'] = '2027-01-30' if v['timeSensitive'] else None
    sources = [S[k] for k in keys]
    v['premise'] = {'reason': premise, 'sources': sources}
    v['challenge'].update(reviewer='Codex (OpenAI)', premiseChecked=True, alternativesExcluded=True, notes=challenge)
    for i, (option, reason) in enumerate(zip(v['options'], reasons)):
        option.update(basis='direct' if i == 0 else 'exclusive-inference', reason=reason, sources=sources)
        if qid in {52,57,68,75,76,81,85,95}:
            option['basis'] = 'exhaustive-list'
        if qid == 59:
            option.update(basis='direct' if i == 0 else 'contradiction', sources=[S[keys[i]]])
        if qid in {54,57,66,67,72,77,78,86,94,97,100} and i:
            option['basis'] = 'contradiction'
    errors = validate_review(review, review['at'])
    assert not errors, (qid, errors)
    (out / f'{qid}.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    reviews.append(review)
(out / 'reviews.json').write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Wrote {len(reviews)} authored, final-wording reviews; import is a separate record-many operation.')
