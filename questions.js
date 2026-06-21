/**
 * Disney Trivia Questions
 * Format: { id, question, answers: [correct, wrong, wrong, wrong], correct: 0, difficulty, category }
 * The correct answer is always index 0; app.js shuffles display order.
 *
 * Categories: movies | characters | parks | walt | cruise | music | pixar
 * Difficulties: easy | medium | hard
 *
 * Distribution:
 *   movies (50): easy 25, medium 18, hard 7
 *   characters (35): easy 15, medium 15, hard 5
 *   parks (30): easy 10, medium 13, hard 7
 *   walt (20): easy 5, medium 10, hard 5
 *   cruise (15): easy 5, medium 7, hard 3
 *   music (20): easy 8, medium 8, hard 4
 *   pixar (30): easy 12, medium 13, hard 5
 */

const QUESTIONS = [

  // =========================================================
  // MOVIES — EASY (25)
  // =========================================================
  {
    id: 1,
    question: "What color is Cinderella's iconic ball gown?",
    answers: ["Blue", "Pink", "Yellow", "White"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 2,
    question: "What is the name of Simba's father in The Lion King?",
    answers: ["Mufasa", "Scar", "Rafiki", "Zazu"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 3,
    question: "Who is the villain in The Little Mermaid?",
    answers: ["Ursula", "Maleficent", "Cruella de Vil", "The Evil Queen"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 4,
    question: "What animal is the main character Bambi?",
    answers: ["Deer", "Rabbit", "Fox", "Bear"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 5,
    question: "In Aladdin, how many wishes does Aladdin receive from the Genie?",
    answers: ["Three", "One", "Seven", "Unlimited"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 6,
    question: "What is the name of Aladdin's pet monkey?",
    answers: ["Abu", "Iago", "Rajah", "Carpet"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 7,
    question: "What happens to Pinocchio's nose when he tells a lie?",
    answers: ["It grows longer", "It glows red", "It changes color", "It shrinks"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 8,
    question: "What is the name of the toy cowboy in Toy Story?",
    answers: ["Woody", "Buzz", "Rex", "Hamm"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 9,
    question: "Who is the villain in Sleeping Beauty?",
    answers: ["Maleficent", "Ursula", "The Evil Queen", "Cruella de Vil"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 10,
    question: "What special ability does Dumbo discover he has?",
    answers: ["He can fly", "He is super strong", "He can speak", "He is invisible"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 11,
    question: "What was the first feature-length animated film ever released by Walt Disney?",
    answers: ["Snow White and the Seven Dwarfs", "Pinocchio", "Fantasia", "Bambi"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 12,
    question: "What is the name of Nemo's father in Finding Nemo?",
    answers: ["Marlin", "Gill", "Bruce", "Nigel"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 13,
    question: "What is the name of the princess in Sleeping Beauty?",
    answers: ["Aurora", "Ariel", "Merida", "Rapunzel"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 14,
    question: "Who is Elsa's younger sister in Frozen?",
    answers: ["Anna", "Merida", "Moana", "Tiana"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 15,
    question: "What color is Ariel's tail in The Little Mermaid?",
    answers: ["Green", "Blue", "Purple", "Red"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 16,
    question: "In Frozen, what power does Elsa possess?",
    answers: ["She can create ice and snow", "She can fly", "She can speak to animals", "She can turn invisible"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 17,
    question: "In Beauty and the Beast, which character is a teapot?",
    answers: ["Mrs. Potts", "Lumiere", "Cogsworth", "Chip"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 18,
    question: "What is the name of Rapunzel's pet chameleon in Tangled?",
    answers: ["Pascal", "Maximus", "Archimedes", "Figaro"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 19,
    question: "What type of fish is Dory in Finding Nemo?",
    answers: ["Blue tang", "Clownfish", "Goldfish", "Angelfish"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 20,
    question: "What magical object does the Evil Queen consult in Snow White?",
    answers: ["A magic mirror", "A crystal ball", "An enchanted book", "A wishing well"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 21,
    question: "What spell does the Fairy Godmother say while transforming Cinderella?",
    answers: ["Bibbidi-Bobbidi-Boo", "Abracadabra", "Alakazam", "Hocus Pocus"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 22,
    question: "What does Maui steal from the island goddess Te Fiti in Moana?",
    answers: ["Te Fiti's heart", "Moana's boat", "The ocean's power", "A glowing pearl"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 23,
    question: "In The Lion King, who is Scar to Simba?",
    answers: ["Simba's uncle", "Simba's father", "Simba's brother", "Simba's cousin"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 24,
    question: "What does Ariel trade to Ursula in exchange for legs in The Little Mermaid?",
    answers: ["Her voice", "Her fins", "Her memories", "Her red hair"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 25,
    question: "In Beauty and the Beast, which character is a candlestick?",
    answers: ["Lumiere", "Cogsworth", "Mrs. Potts", "Chip"],
    correct: 0, difficulty: "easy", category: "movies"
  },

  // =========================================================
  // MOVIES — MEDIUM (18)
  // =========================================================
  {
    id: 26,
    question: "In Mulan, what is the name of Mulan's tiny dragon guardian?",
    answers: ["Mushu", "Shenlong", "Long", "Cri-Kee"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 27,
    question: "What is the villain's name in The Princess and the Frog?",
    answers: ["Dr. Facilier", "Chef Louis", "Lawrence", "Raymond"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 28,
    question: "In WALL-E, what does WALL-E stand for?",
    answers: ["Waste Allocation Load Lifter Earth-Class", "World Automated Life Lab Earth", "Waste Activated Lift Loader Earth", "Wide Area Load Lifter Earth"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 29,
    question: "In Tarzan, what is the name of Tarzan's gorilla mother?",
    answers: ["Kala", "Kerchak", "Terk", "Jane"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 30,
    question: "What is the name of Merida's horse in Brave?",
    answers: ["Angus", "Maximus", "Phillip", "Braveheart"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 31,
    question: "What is the name of the villain in Tangled?",
    answers: ["Mother Gothel", "Lady Tremaine", "The Evil Queen", "Maleficent"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 32,
    question: "Who is the villain in The Hunchback of Notre Dame?",
    answers: ["Judge Claude Frollo", "Captain Phoebus", "The Archdeacon", "King Louis"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 33,
    question: "In Pocahontas, what is the name of Pocahontas's English love interest?",
    answers: ["John Smith", "John Ratcliffe", "Thomas", "Captain Newport"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 34,
    question: "Who presents Simba to the animals at the beginning of The Lion King?",
    answers: ["Rafiki", "Zazu", "Mufasa", "Sarabi"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 35,
    question: "In Ratatouille, what is the name of the famous restaurant Remy longs to cook in?",
    answers: ["Gusteau's", "La Maison", "Le Gourmet", "Chez Antoine"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 36,
    question: "Who is the main villain in Hercules?",
    answers: ["Hades", "Zeus", "Ares", "Poseidon"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 37,
    question: "In Coco, whose guitar does Miguel find in the family mausoleum?",
    answers: ["Ernesto de la Cruz", "Héctor Rivera", "Mamá Imelda", "Miguel's grandfather"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 38,
    question: "In Up, what is the name of the exotic bird Carl and Russell encounter?",
    answers: ["Kevin", "Dug", "Alpha", "Beta"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 39,
    question: "In Encanto, who is the only Madrigal family member without a magical gift?",
    answers: ["Mirabel", "Luisa", "Isabela", "Julieta"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 40,
    question: "In Lilo & Stitch, what is Stitch's experiment number?",
    answers: ["626", "428", "726", "001"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 41,
    question: "In The Little Mermaid, what is the name of Ariel's red crab friend?",
    answers: ["Sebastian", "Flounder", "Scuttle", "Grimsby"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 42,
    question: "In The Jungle Book, what is the name of the villainous tiger?",
    answers: ["Shere Khan", "King Louie", "Kaa", "Bagheera"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 43,
    question: "What kingdom does the story of Frozen take place in?",
    answers: ["Arendelle", "Agrabah", "Corona", "Motunui"],
    correct: 0, difficulty: "medium", category: "movies"
  },

  // =========================================================
  // MOVIES — HARD (7)
  // =========================================================
  {
    id: 44,
    question: "What are the names of the three good fairies in Sleeping Beauty?",
    answers: ["Flora, Fauna, and Merryweather", "Rose, Lily, and Violet", "Faith, Hope, and Charity", "Sparkle, Glimmer, and Shine"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 45,
    question: "What year was the Disney film Fantasia originally released?",
    answers: ["1940", "1937", "1942", "1950"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 46,
    question: "What is the name of the villain in The Great Mouse Detective?",
    answers: ["Professor Ratigan", "Shere Khan", "Ratso Rizzo", "Professor Moriarty"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 47,
    question: "What is the name of the main villain in The Black Cauldron?",
    answers: ["The Horned King", "The Dark Lord", "Malchor", "The Shadow King"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 48,
    question: "In The Aristocats, what is the name of the elegant mother cat?",
    answers: ["Duchess", "Marie", "Berlioz", "Toulouse"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 49,
    question: "What is the name of the mouse who befriends Dumbo and convinces him he can fly?",
    answers: ["Timothy Q. Mouse", "Jerry Mouse", "Stuart Little", "Danger Mouse"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 50,
    question: "In which Disney film does the villain character Yzma appear?",
    answers: ["The Emperor's New Groove", "Hercules", "Mulan", "Treasure Planet"],
    correct: 0, difficulty: "hard", category: "movies"
  },

  // =========================================================
  // CHARACTERS — EASY (15)
  // =========================================================
  {
    id: 51,
    question: "What is the name of Mickey Mouse's girlfriend?",
    answers: ["Minnie Mouse", "Daisy Duck", "Clarabelle Cow", "Tinker Bell"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 52,
    question: "What are the names of Donald Duck's three nephews?",
    answers: ["Huey, Dewey, and Louie", "Chip, Dale, and Monty", "Larry, Moe, and Curly", "Tick, Tack, and Tock"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 53,
    question: "What is the name of Mickey Mouse's pet dog?",
    answers: ["Pluto", "Rex", "Goofy", "Spot"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 54,
    question: "What color is Tinker Bell's dress?",
    answers: ["Green", "Blue", "Pink", "Yellow"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 55,
    question: "Who is the main villain in The Lion King?",
    answers: ["Scar", "Mufasa", "Zazu", "Rafiki"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 56,
    question: "In Beauty and the Beast, what is the name of Belle's arrogant suitor?",
    answers: ["Gaston", "Jafar", "Frollo", "Hades"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 57,
    question: "In Snow White, how many dwarfs does Snow White live with?",
    answers: ["Seven", "Five", "Eight", "Six"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 58,
    question: "In which Disney film does Maleficent first appear as a villain?",
    answers: ["Sleeping Beauty", "Snow White", "Cinderella", "Bambi"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 59,
    question: "What is the name of Winnie the Pooh's gloomy donkey friend?",
    answers: ["Eeyore", "Tigger", "Kanga", "Roo"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 60,
    question: "What is the name of the crab who watches over Ariel in The Little Mermaid?",
    answers: ["Sebastian", "Flounder", "Grimsby", "Chef Louis"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 61,
    question: "Who provided the original voice for Mickey Mouse?",
    answers: ["Walt Disney", "Clarence Nash", "Jim Henson", "Mel Blanc"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 62,
    question: "What is the name of the evil stepmother in Cinderella?",
    answers: ["Lady Tremaine", "Maleficent", "Ursula", "The Evil Queen"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 63,
    question: "What is Goofy's trademark exclamation of surprise?",
    answers: ["Gawrsh!", "Oh boy!", "Wahoo!", "Shucks!"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 64,
    question: "What is the name of the evil cat belonging to Cinderella's stepmother?",
    answers: ["Lucifer", "Felix", "Tom", "Shadow"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 65,
    question: "What is the name of the prince in Sleeping Beauty?",
    answers: ["Prince Phillip", "Prince Charming", "Prince Eric", "Prince Adam"],
    correct: 0, difficulty: "easy", category: "characters"
  },

  // =========================================================
  // CHARACTERS — MEDIUM (15)
  // =========================================================
  {
    id: 66,
    question: "What type of animal is Timon in The Lion King?",
    answers: ["Meerkat", "Prairie dog", "Mongoose", "Weasel"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 67,
    question: "What type of animal is Pumbaa in The Lion King?",
    answers: ["Warthog", "Wild boar", "Pig", "Hippo"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 68,
    question: "What are the names of Ursula's two eel servants in The Little Mermaid?",
    answers: ["Flotsam and Jetsam", "Scuttle and Slog", "Barnacle and Murk", "Slick and Sludge"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 69,
    question: "In Hercules, who are the narrators of the film?",
    answers: ["The Muses", "The Fates", "The Olympians", "The Nymphs"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 70,
    question: "In Moana, what is the name of the glittery, giant crab who captures Maui's fishhook?",
    answers: ["Tamatoa", "Te Kā", "Lalotai", "Maui's rival"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 71,
    question: "In The Incredibles, what is the real name of the villain Syndrome?",
    answers: ["Buddy Pine", "Oliver Sansweet", "Gazerbeam", "Chad Brentley"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 72,
    question: "What is Buzz Lightyear's famous catchphrase?",
    answers: ["To infinity and beyond!", "I'm a Space Ranger!", "Reach for the sky!", "One universe, one destiny!"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 73,
    question: "In Coco, who banned music from the Madrigal — er, Rivera family?",
    answers: ["Mamá Imelda", "Mamá Coco", "Abuelita Elena", "Papá Julio"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 74,
    question: "What is the name of the social worker in Lilo & Stitch who tries to take Lilo away?",
    answers: ["Cobra Bubbles", "Agent Hood", "Mr. Big", "Officer Reynolds"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 75,
    question: "What are the names of Hades' two bumbling henchmen in Hercules?",
    answers: ["Pain and Panic", "Fear and Dread", "Chaos and Discord", "Slime and Sludge"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 76,
    question: "In Cinderella, what are the names of Cinderella's two main mouse friends?",
    answers: ["Jaq and Gus", "Tic and Tac", "Nibbles and Chuck", "Tom and Jerry"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 77,
    question: "What is the name of Tarzan's best friend gorilla?",
    answers: ["Terk", "Kala", "Tantor", "Kerchak"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 78,
    question: "In The Jungle Book, what is the name of the friendly bear?",
    answers: ["Baloo", "Bagheera", "Shere Khan", "King Louie"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 79,
    question: "What type of animal is Meeko in Pocahontas?",
    answers: ["Raccoon", "Fox", "Squirrel", "Beaver"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 80,
    question: "In Aladdin, what type of animal is Jafar's sidekick Iago?",
    answers: ["Parrot", "Crow", "Raven", "Macaw"],
    correct: 0, difficulty: "medium", category: "characters"
  },

  // =========================================================
  // CHARACTERS — HARD (5)
  // =========================================================
  {
    id: 81,
    question: "Which of these is NOT one of Snow White's Seven Dwarfs?",
    answers: ["Jumpy", "Bashful", "Grumpy", "Dopey"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 82,
    question: "In The Aristocats, what is the name of the butler who stands to inherit everything?",
    answers: ["Edgar", "Henri", "Ferdinand", "Jacques"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 83,
    question: "What is the name of Yzma's loyal but dim-witted henchman in The Emperor's New Groove?",
    answers: ["Kronk", "Pacha", "Bucky", "Tipo"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 84,
    question: "In Atlantis: The Lost Empire, what is the name of the young linguist and cartographer?",
    answers: ["Milo Thatch", "Lewis Robinson", "Wilbur Robinson", "Pleakley"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 85,
    question: "What are the names of Madame Medusa's two pet alligators in The Rescuers?",
    answers: ["Brutus and Nero", "Snap and Crunch", "Jaws and Rex", "Fluffy and Spike"],
    correct: 0, difficulty: "hard", category: "characters"
  },

  // =========================================================
  // DISNEY PARKS — EASY (10)
  // =========================================================
  {
    id: 86,
    question: "In which U.S. state is Walt Disney World located?",
    answers: ["Florida", "California", "Texas", "New York"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 87,
    question: "In which U.S. state is the original Disneyland located?",
    answers: ["California", "Florida", "Nevada", "Arizona"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 88,
    question: "What is the name of the iconic castle at Magic Kingdom in Walt Disney World?",
    answers: ["Cinderella Castle", "Sleeping Beauty Castle", "Aurora's Palace", "Enchanted Castle"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 89,
    question: "What year did Walt Disney World open?",
    answers: ["1971", "1955", "1982", "1965"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 90,
    question: "What is the name of the famous Disney attraction that sends guests through scenes of children from around the world?",
    answers: ["It's a Small World", "Pirates of the Caribbean", "The Haunted Mansion", "Jungle Cruise"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 91,
    question: "What is the name of the Disney World theme park known for its animal exhibits and conservation focus?",
    answers: ["Animal Kingdom", "EPCOT", "Hollywood Studios", "Typhoon Lagoon"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 92,
    question: "What is the iconic geodesic sphere that serves as EPCOT's centerpiece attraction?",
    answers: ["Spaceship Earth", "The Magic Orb", "Epcot Globe", "Future World"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 93,
    question: "What is the name of the haunted attraction at Magic Kingdom featuring 999 happy haunts?",
    answers: ["The Haunted Mansion", "Ghost Train", "Tower of Terror", "Phantom Manor"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 94,
    question: "What is the name of Disney Cruise Line's private island destination in the Bahamas?",
    answers: ["Castaway Cay", "Paradise Island", "Magic Isle", "Treasure Island"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 95,
    question: "What are the four main theme parks at Walt Disney World?",
    answers: ["Magic Kingdom, EPCOT, Hollywood Studios, Animal Kingdom", "Magic Kingdom, EPCOT, Hollywood Studios, Universal", "Magic Kingdom, EPCOT, Adventureland, Animal Kingdom", "Magic Kingdom, Hollywood Studios, Animal Kingdom, SeaWorld"],
    correct: 0, difficulty: "easy", category: "parks"
  },

  // =========================================================
  // DISNEY PARKS — MEDIUM (13)
  // =========================================================
  {
    id: 96,
    question: "What year did the original Disneyland first open?",
    answers: ["1955", "1960", "1950", "1963"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 97,
    question: "In what year did EPCOT open at Walt Disney World?",
    answers: ["1982", "1971", "1989", "1975"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 98,
    question: "What is the name of the roller coaster at Animal Kingdom themed around an expedition to find the Yeti?",
    answers: ["Expedition Everest", "Mount Yeti", "Summit Plummet", "Everest Explorer"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 99,
    question: "What was the original name of Disney's Hollywood Studios when it opened in 1989?",
    answers: ["Disney-MGM Studios", "Disney Movie Studios", "Hollywood Park", "Disney Film Studios"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 100,
    question: "What is the land in Magic Kingdom that is home to Pirates of the Caribbean?",
    answers: ["Adventureland", "Frontierland", "Tomorrowland", "Liberty Square"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 101,
    question: "What does EPCOT stand for?",
    answers: ["Experimental Prototype Community of Tomorrow", "Experimental Park Community of Tomorrow", "Enhanced Park for Community of Tomorrow", "Expanding Park Center of Tomorrow"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 102,
    question: "In what year did Disney's Animal Kingdom open at Walt Disney World?",
    answers: ["1998", "2001", "1995", "2000"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 103,
    question: "In which Disney World park can guests visit Pandora — The World of Avatar?",
    answers: ["Animal Kingdom", "Hollywood Studios", "EPCOT", "Magic Kingdom"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 104,
    question: "What is the name of Toy Story Land's main roller coaster at Hollywood Studios?",
    answers: ["Slinky Dog Dash", "Woody's Wild Ride", "Buzz Blaster", "Rex's Runway"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 105,
    question: "What is the name of the Disney theme park located in Shanghai, China?",
    answers: ["Shanghai Disneyland", "China Disney Park", "Disney Shanghai", "Magic Kingdom Shanghai"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 106,
    question: "How many Disney theme park resorts are there worldwide?",
    answers: ["6", "5", "7", "8"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 107,
    question: "What is the name of the TRON-themed roller coaster at Magic Kingdom that opened in 2023?",
    answers: ["TRON Lightcycle / Run", "TRON Legacy Coaster", "TRON Power Run", "TRON Speedway"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 108,
    question: "What themed land at Hollywood Studios is dedicated to Star Wars?",
    answers: ["Galaxy's Edge", "Star Wars Zone", "The Outer Rim", "Force Land"],
    correct: 0, difficulty: "medium", category: "parks"
  },

  // =========================================================
  // DISNEY PARKS — HARD (7)
  // =========================================================
  {
    id: 109,
    question: "What was the opening day general admission price for Disneyland in 1955?",
    answers: ["$1.00", "$0.50", "$2.50", "$5.00"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 110,
    question: "What is the name of the Disneyland castle in California?",
    answers: ["Sleeping Beauty Castle", "Cinderella Castle", "Aurora's Palace", "Fantasyland Castle"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 111,
    question: "In what year did Shanghai Disneyland open?",
    answers: ["2016", "2014", "2018", "2012"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 112,
    question: "What is the name of the steam railroad that circles the perimeter of Magic Kingdom?",
    answers: ["Walt Disney World Railroad", "Magic Kingdom Express", "Fantasyland Railroad", "Disney Steam Railway"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 113,
    question: "What themed area in Magic Kingdom is modeled after 19th-century New Orleans?",
    answers: ["Liberty Square", "Frontierland", "Adventureland", "Main Street, U.S.A."],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 114,
    question: "What is the name of the Disney resort that opened in Paris, France?",
    answers: ["Disneyland Paris", "Euro Disney", "Disney France", "Paris Magic Kingdom"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 115,
    question: "The Tiana's Bayou Adventure ride replaced which beloved Disney attraction?",
    answers: ["Splash Mountain", "Big Thunder Mountain", "Pirates of the Caribbean", "Jungle Cruise"],
    correct: 0, difficulty: "hard", category: "parks"
  },

  // =========================================================
  // WALT DISNEY — EASY (5)
  // =========================================================
  {
    id: 116,
    question: "What was Walt Disney's full name?",
    answers: ["Walter Elias Disney", "Walter Edward Disney", "William Elias Disney", "Walter Eugene Disney"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 117,
    question: "In what year was Walt Disney born?",
    answers: ["1901", "1895", "1910", "1898"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 118,
    question: "What city was Walt Disney born in?",
    answers: ["Chicago, Illinois", "Los Angeles, California", "New York City, New York", "St. Louis, Missouri"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 119,
    question: "What was the first animated feature film produced by Walt Disney Studios?",
    answers: ["Snow White and the Seven Dwarfs", "Pinocchio", "Fantasia", "Bambi"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 120,
    question: "What is the name of the famous mouse character Walt Disney created?",
    answers: ["Mickey Mouse", "Stuart Little", "Danger Mouse", "Jerry Mouse"],
    correct: 0, difficulty: "easy", category: "walt"
  },

  // =========================================================
  // WALT DISNEY — MEDIUM (10)
  // =========================================================
  {
    id: 121,
    question: "In what year did Walt Disney pass away?",
    answers: ["1966", "1971", "1960", "1975"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 122,
    question: "What was the name of Walt Disney's successful cartoon character before Mickey Mouse?",
    answers: ["Oswald the Lucky Rabbit", "Pete the Cat", "Julius the Cat", "Roger Rabbit"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 123,
    question: "Approximately how many Academy Awards did Walt Disney win or receive during his lifetime — the most by any individual?",
    answers: ["22", "10", "15", "30"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 124,
    question: "What was the name of Walt Disney's production company before it became The Walt Disney Company?",
    answers: ["Walt Disney Productions", "Disney Brothers Studio", "Laugh-O-Gram Films", "Mickey Mouse Studios"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 125,
    question: "Walt Disney served in an ambulance corps for which military conflict?",
    answers: ["World War I", "World War II", "The Korean War", "The Spanish-American War"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 126,
    question: "What famous TV show did Walt Disney create to help promote Disneyland?",
    answers: ["Disneyland (The Wonderful World of Disney)", "The Mickey Mouse Club", "Walt Disney Presents", "Fantasy Hour"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 127,
    question: "What were the names of Walt Disney's two daughters?",
    answers: ["Diane and Sharon", "Mary and Susan", "Anne and Patricia", "Jane and Lillian"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 128,
    question: "What was the original intended name for Mickey Mouse before Walt's wife suggested a change?",
    answers: ["Mortimer Mouse", "Marty Mouse", "Mighty Mouse", "Murray Mouse"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 129,
    question: "What type of miniature railroad did Walt Disney build at his home?",
    answers: ["Carolwood Pacific Railroad", "Disney Home Railway", "Lilly Belle Express", "Riverside Train"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 130,
    question: "Walt Disney's first animation studio produced a series of short films called what?",
    answers: ["Laugh-O-Grams", "Mickey Shorts", "Silly Symphonies", "Alice Comedies"],
    correct: 0, difficulty: "medium", category: "walt"
  },

  // =========================================================
  // WALT DISNEY — HARD (5)
  // =========================================================
  {
    id: 131,
    question: "In what city did Walt Disney open his first studio in California?",
    answers: ["Los Angeles (Hollywood)", "Burbank", "Anaheim", "San Francisco"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 132,
    question: "What special Academy Award did Walt Disney receive in 1932 for the creation of Mickey Mouse?",
    answers: ["Honorary Oscar with seven miniature statuettes", "Best Animated Short", "Irving G. Thalberg Award", "Lifetime Achievement Award"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 133,
    question: "Walt Disney's studio lost the rights to which character to Universal Pictures in the late 1920s?",
    answers: ["Oswald the Lucky Rabbit", "Felix the Cat", "Koko the Clown", "Bimbo the Dog"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 134,
    question: "What art school did Walt Disney briefly attend in Chicago?",
    answers: ["The Art Institute of Chicago", "The Chicago Academy of Fine Arts", "Columbia College Chicago", "School of the Art Institute"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 135,
    question: "Which 1964 Disney film — the last major production Walt Disney personally championed — combined live action with animation and starred Julie Andrews?",
    answers: ["Mary Poppins", "The Jungle Book", "The Sword in the Stone", "Bedknobs and Broomsticks"],
    correct: 0, difficulty: "hard", category: "walt"
  },

  // =========================================================
  // DISNEY CRUISE LINE — EASY (5)
  // =========================================================
  {
    id: 136,
    question: "What is the name of Disney Cruise Line's first ship?",
    answers: ["Disney Magic", "Disney Wonder", "Disney Dream", "Disney Fantasy"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 137,
    question: "In what year did Disney Cruise Line begin operating?",
    answers: ["1998", "1994", "2002", "2006"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 138,
    question: "What song does the Disney Cruise Line ship horn play?",
    answers: ["When You Wish Upon a Star", "A Dream Is a Wish Your Heart Makes", "Be Our Guest", "Zip-a-Dee-Doo-Dah"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 139,
    question: "What is the main Florida homeport for most Disney Cruise Line sailings?",
    answers: ["Port Canaveral", "Port Everglades", "PortMiami", "Tampa Bay Port"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 140,
    question: "What is the name of the children's play area on Disney Cruise Line ships?",
    answers: ["The Oceaneer Club", "Kids Kingdom", "Disney Playhouse", "The Magic Den"],
    correct: 0, difficulty: "easy", category: "cruise"
  },

  // =========================================================
  // DISNEY CRUISE LINE — MEDIUM (7)
  // =========================================================
  {
    id: 141,
    question: "What is the name of Disney's private island in the Bahamas frequented by cruise guests?",
    answers: ["Castaway Cay", "Treasure Cay", "Magic Isle", "Adventure Bay"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 142,
    question: "What is the newest Disney Cruise Line ship, launched in 2022?",
    answers: ["Disney Wish", "Disney Destiny", "Disney Dream", "Disney Treasure"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 143,
    question: "What is the name of the adults-only Italian specialty restaurant found on all Disney Cruise Line ships?",
    answers: ["Palo", "Remy", "Lumiere's", "Triton's"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 144,
    question: "What year did the Disney Dream launch?",
    answers: ["2011", "2009", "2013", "2015"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 145,
    question: "What is the name of the AquaDuck — Disney's onboard water coaster concept — and on which ship did it debut?",
    answers: ["AquaDuck on Disney Dream", "AquaRun on Disney Magic", "WaterDuck on Disney Wonder", "AquaSlide on Disney Fantasy"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 146,
    question: "In what country are Disney Cruise Line ships registered?",
    answers: ["The Bahamas", "The United States", "Panama", "The Cayman Islands"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 147,
    question: "What is the name of Disney's second private island destination, which opened in 2024?",
    answers: ["Lookout Cay at Lighthouse Point", "Adventure Cay", "Treasure Point", "Disney Island"],
    correct: 0, difficulty: "medium", category: "cruise"
  },

  // =========================================================
  // DISNEY CRUISE LINE — HARD (3)
  // =========================================================
  {
    id: 148,
    question: "What is the name of the adults-only French specialty restaurant aboard the Disney Dream and Disney Fantasy?",
    answers: ["Remy", "Palo", "Lumiere's", "Triton's"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 149,
    question: "What year did the Disney Fantasy launch?",
    answers: ["2012", "2011", "2014", "2010"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 150,
    question: "Disney Cruise Line's rotational dining system means guests do what?",
    answers: ["Move to a different restaurant each night while their servers follow them", "Stay in one restaurant for the entire cruise", "Choose any restaurant each night independently", "Eat all meals at a single buffet"],
    correct: 0, difficulty: "hard", category: "cruise"
  },

  // =========================================================
  // MUSIC & SONGS — EASY (8)
  // =========================================================
  {
    id: 151,
    question: "In what Disney film does the song 'A Whole New World' appear?",
    answers: ["Aladdin", "Beauty and the Beast", "The Little Mermaid", "Pocahontas"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 152,
    question: "Which Disney princess sings 'Part of Your World'?",
    answers: ["Ariel", "Belle", "Jasmine", "Rapunzel"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 153,
    question: "In what Disney film does 'Circle of Life' appear?",
    answers: ["The Lion King", "The Jungle Book", "Tarzan", "Brother Bear"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 154,
    question: "Complete the lyric from Frozen: 'Let it go, let it go, can't hold it back ___.'",
    answers: ["anymore", "today", "again", "no more"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 155,
    question: "Complete the lyric from The Lion King: 'Hakuna Matata, what a wonderful ___.'",
    answers: ["phrase", "day", "life", "song"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 156,
    question: "In what Disney film does 'Be Our Guest' appear?",
    answers: ["Beauty and the Beast", "Cinderella", "Sleeping Beauty", "The Little Mermaid"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 157,
    question: "What Disney movie features the song 'Colors of the Wind'?",
    answers: ["Pocahontas", "Moana", "Brave", "Mulan"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 158,
    question: "Which Disney film features the song 'Under the Sea'?",
    answers: ["The Little Mermaid", "Finding Nemo", "Moana", "The Little Mermaid II"],
    correct: 0, difficulty: "easy", category: "music"
  },

  // =========================================================
  // MUSIC & SONGS — MEDIUM (8)
  // =========================================================
  {
    id: 159,
    question: "Who composed the music for The Little Mermaid, Beauty and the Beast, and Aladdin?",
    answers: ["Alan Menken", "Elton John", "Howard Ashman", "Phil Collins"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 160,
    question: "The songwriting duo Kristen Anderson-Lopez and Robert Lopez wrote the songs for which Disney film?",
    answers: ["Frozen", "Moana", "Encanto", "Brave"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 161,
    question: "In what Disney film does the song 'Reflection' appear?",
    answers: ["Mulan", "Pocahontas", "Brave", "Moana"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 162,
    question: "Which Disney film's soundtrack was the first to win the Academy Award for Best Original Score?",
    answers: ["The Little Mermaid", "Beauty and the Beast", "Aladdin", "The Lion King"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 163,
    question: "What Disney film features the song 'I See the Light'?",
    answers: ["Tangled", "Frozen", "Brave", "Moana"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 164,
    question: "Who performed the opening vocals of 'Circle of Life' in The Lion King (1994)?",
    answers: ["Carmen Twillie", "Elton John", "Hans Zimmer", "Lebo M"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 165,
    question: "In what Disney film does the song 'I'll Make a Man Out of You' appear?",
    answers: ["Mulan", "Hercules", "Tarzan", "The Lion King"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 166,
    question: "Which Disney film features the song 'How Far I'll Go'?",
    answers: ["Moana", "Brave", "Frozen", "Encanto"],
    correct: 0, difficulty: "medium", category: "music"
  },

  // =========================================================
  // MUSIC & SONGS — HARD (4)
  // =========================================================
  {
    id: 167,
    question: "The song 'It's a Small World' was originally written for which event before becoming a Disney park attraction?",
    answers: ["The 1964 New York World's Fair", "The 1962 Seattle World's Fair", "The 1958 Brussels World's Fair", "The 1967 Montreal World's Fair"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 168,
    question: "Which songwriting duo wrote 'It's a Small World' and numerous other Disney classics?",
    answers: ["The Sherman Brothers (Richard and Robert)", "Menken and Ashman", "Lopez and Anderson-Lopez", "John and Rice"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 169,
    question: "In what year did 'When You Wish Upon a Star' from Pinocchio win the Academy Award for Best Original Song?",
    answers: ["1940", "1942", "1938", "1945"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 170,
    question: "Lin-Manuel Miranda wrote the songs for which Disney animated film?",
    answers: ["Encanto", "Moana", "Frozen II", "Raya and the Last Dragon"],
    correct: 0, difficulty: "hard", category: "music"
  },

  // =========================================================
  // PIXAR — EASY (12)
  // =========================================================
  {
    id: 171,
    question: "In Toy Story, who is Woody's owner?",
    answers: ["Andy", "Sid", "Bonnie", "Al"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 172,
    question: "What is the name of the rat who dreams of being a chef in Ratatouille?",
    answers: ["Remy", "Emile", "Gusteau", "Linguini"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 173,
    question: "In Finding Nemo, where does Nemo end up after being captured?",
    answers: ["A dentist's fish tank in Sydney, Australia", "An aquarium in Tokyo, Japan", "A pet store in London, England", "A research lab in California"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 174,
    question: "What type of fish is Dory in Finding Nemo?",
    answers: ["Blue tang", "Clownfish", "Goldfish", "Angelfish"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 175,
    question: "In The Incredibles, what is Mr. Incredible's real name?",
    answers: ["Bob Parr", "Bill Parr", "Ben Parr", "Brad Parr"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 176,
    question: "What is the name of the main character in Brave?",
    answers: ["Merida", "Moana", "Tiana", "Mirabel"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 177,
    question: "In Up, what is the name of the elderly man who floats his house with balloons?",
    answers: ["Carl Fredricksen", "Charles Muntz", "Russell Fredricksen", "Ed Asner"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 178,
    question: "In Monsters, Inc., what is the name of the one-eyed green monster?",
    answers: ["Mike Wazowski", "Sulley", "Randall", "Roz"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 179,
    question: "In Cars, what is Lightning McQueen's racing number?",
    answers: ["95", "51", "43", "7"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 180,
    question: "In Inside Out, which emotion is colored yellow and is the lead character?",
    answers: ["Joy", "Sadness", "Anger", "Fear"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 181,
    question: "In Coco, what holiday is the film centered around?",
    answers: ["Día de los Muertos (Day of the Dead)", "Christmas", "Halloween", "El Día de los Reyes"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 182,
    question: "What year was the original Toy Story released?",
    answers: ["1995", "1997", "1993", "1999"],
    correct: 0, difficulty: "easy", category: "pixar"
  },

  // =========================================================
  // PIXAR — MEDIUM (13)
  // =========================================================
  {
    id: 183,
    question: "In Toy Story, who is the main villain — the cruel kid next door?",
    answers: ["Sid Phillips", "Al McWhiggin", "Stinky Pete", "Lotso"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 184,
    question: "In The Incredibles, what is Elastigirl's real name?",
    answers: ["Helen Parr", "Sarah Parr", "Karen Parr", "Lisa Parr"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 185,
    question: "In Ratatouille, what is the name of the famous chef whose motto is 'Anyone can cook'?",
    answers: ["Auguste Gusteau", "Anton Ego", "Skinner", "Lalo"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 186,
    question: "In Up, what is the name of the young Wilderness Explorer who accompanies Carl?",
    answers: ["Russell", "Kevin", "Dug", "Charles"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 187,
    question: "In Cars, what is the name of the small town where Lightning McQueen gets stuck?",
    answers: ["Radiator Springs", "Carburetor County", "Piston Cup City", "Route 66 Junction"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 188,
    question: "In Inside Out, what color represents the emotion Sadness?",
    answers: ["Blue", "Purple", "Green", "Gray"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 189,
    question: "In Toy Story 3, where do Andy's toys end up being donated?",
    answers: ["Sunnyside Daycare", "Bonnie's house", "A museum", "A toy store"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 190,
    question: "In Finding Dory, where does Dory discover she grew up?",
    answers: ["The Marine Life Institute in Morro Bay, California", "The Great Barrier Reef in Australia", "A coral reef in Hawaii", "The Pacific Ocean near Japan"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 191,
    question: "In Brave, what does the spell Merida uses on her mother accidentally turn her into?",
    answers: ["A bear", "A deer", "A wolf", "A fox"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 192,
    question: "In Monsters University, what is the name of the fraternity Mike and Sulley join?",
    answers: ["Oozma Kappa (OK)", "Roar Omega Roar (ROR)", "Python Nu Kappa (PNK)", "Eta Hiss Hiss (HSS)"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 193,
    question: "In Finding Nemo, what is the name of the pelican who helps Marlin find Nemo?",
    answers: ["Nigel", "Gerald", "Gill", "Bloat"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 194,
    question: "In WALL-E, what does EVE stand for?",
    answers: ["Extraterrestrial Vegetation Evaluator", "Environmental Vegetation Explorer", "Extra-Vehicular Explorer", "Earth Vegetation Examiner"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 195,
    question: "In Coco, what is the full name of the famous musician Miguel idolizes?",
    answers: ["Ernesto de la Cruz", "Héctor Rivera", "Chicharrón", "Papá Julio"],
    correct: 0, difficulty: "medium", category: "pixar"
  },

  // =========================================================
  // PIXAR — HARD (5)
  // =========================================================
  {
    id: 196,
    question: "In Toy Story, what is the name of the pizza restaurant delivery rocket ship that appears throughout the film?",
    answers: ["Pizza Planet", "Cosmic Pizza", "Galaxy Slice", "Star Pizza"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 197,
    question: "In A Bug's Life, what is the name of the grasshopper who leads the villain gang?",
    answers: ["Hopper", "Thumper", "Molt", "Grasshopper"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 198,
    question: "In The Incredibles, what is the name of the island where Syndrome has his secret lair?",
    answers: ["Nomanisan Island", "Syndrome's Island", "Omnidroid Base", "Villain's Cove"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 199,
    question: "In Ratatouille, what is the full name of the food critic who gives Gusteau's restaurant a scathing review?",
    answers: ["Anton Ego", "Auguste Gusteau", "Horst", "Lalo"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 200,
    question: "In Up, what is the name of the famous explorer and villain that Carl idolized as a child?",
    answers: ["Charles Muntz", "Carl Fredricksen", "Spencer Muntz", "Howard Muntz"],
    correct: 0, difficulty: "hard", category: "pixar"
  },

  // =========================================================
  // MOVIES — EASY (201–235)
  // =========================================================
  {
    id: 201,
    question: "What type of animal is Bambi's friend Thumper?",
    answers: ["Rabbit", "Squirrel", "Fox", "Raccoon"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 202,
    question: "What is the name of the snowman that Elsa and Anna built as children in Frozen?",
    answers: ["Olaf", "Marshmallow", "Frosty", "Snowflake"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 203,
    question: "What is Flynn Rider's real name in Tangled?",
    answers: ["Eugene Fitzherbert", "Frederick Rider", "Eugene Hunter", "Francis Flynn"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 204,
    question: "In Zootopia, what is Judy Hopps' job?",
    answers: ["Police officer", "Firefighter", "Teacher", "Journalist"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 205,
    question: "What color is Belle's famous ball gown in Beauty and the Beast?",
    answers: ["Yellow", "Blue", "Pink", "Red"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 206,
    question: "In Snow White, what fruit does the Evil Queen use to poison Snow White?",
    answers: ["An apple", "A pear", "A peach", "A plum"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 207,
    question: "What is the name of Moana's island home?",
    answers: ["Motunui", "Lalotai", "Te Fiti", "Maui"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 208,
    question: "In Big Hero 6, what is the name of the inflatable healthcare robot?",
    answers: ["Baymax", "Hiro", "Wasabi", "GoGo"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 209,
    question: "In The Princess and the Frog, what city does Tiana live in?",
    answers: ["New Orleans", "Atlanta", "New York", "Savannah"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 210,
    question: "In Encanto, what is the name of the magical Madrigal family's house?",
    answers: ["La Casita", "El Encanto", "Casa Madrigal", "La Magia"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 211,
    question: "In Cinderella, at what time does the Fairy Godmother's spell wear off?",
    answers: ["Midnight", "Dawn", "Noon", "Sunset"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 212,
    question: "What is the name of Moana's pet pig?",
    answers: ["Pua", "Hei Hei", "Tala", "Sina"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 213,
    question: "What is the name of Moana's rooster?",
    answers: ["Hei Hei", "Pua", "Maui", "Tui"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 214,
    question: "In Brave, what country does Merida's story take place in?",
    answers: ["Scotland", "Ireland", "England", "Wales"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 215,
    question: "In Hercules, who is Hercules' divine father?",
    answers: ["Zeus", "Hades", "Apollo", "Poseidon"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 216,
    question: "In The Nightmare Before Christmas, what holiday does Jack Skellington rule?",
    answers: ["Halloween", "Christmas", "Easter", "Thanksgiving"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 217,
    question: "What is the name of the main character in The Hunchback of Notre Dame?",
    answers: ["Quasimodo", "Frollo", "Phoebus", "Clopin"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 218,
    question: "In Bambi, what is the name of Bambi's skunk friend?",
    answers: ["Flower", "Daisy", "Blossom", "Thistle"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 219,
    question: "What does Rapunzel use as a weapon in Tangled?",
    answers: ["A frying pan", "A sword", "A bow and arrow", "A magic wand"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 220,
    question: "In The Little Mermaid, what does Scuttle the seagull incorrectly call a fork?",
    answers: ["A dinglehopper", "A thingamabob", "A gizmo", "A whatsit"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 221,
    question: "In Aladdin, what does Jafar become when he makes his final wish?",
    answers: ["A genie", "A dragon", "A sorcerer", "A king"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 222,
    question: "In Coco, what instrument does Miguel play?",
    answers: ["Guitar", "Trumpet", "Piano", "Violin"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 223,
    question: "In The Jungle Book, who is Mowgli's protective panther guardian?",
    answers: ["Bagheera", "Baloo", "Shere Khan", "King Louie"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 224,
    question: "What is the name of the city in Aladdin?",
    answers: ["Agrabah", "Arabistan", "Baghdad", "Sharabah"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 225,
    question: "In Encanto, what special gift does Luisa possess?",
    answers: ["Super strength", "Growing flowers", "Healing powers", "Shape-shifting"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 226,
    question: "In 101 Dalmatians, who is the main villain who wants the puppies for their fur?",
    answers: ["Cruella de Vil", "Lady Tremaine", "Maleficent", "Ursula"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 227,
    question: "In Lilo & Stitch, what U.S. state does Lilo live in?",
    answers: ["Hawaii", "California", "Florida", "Oregon"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 228,
    question: "In Sleeping Beauty, what does Maleficent's curse compel Aurora to do?",
    answers: ["Prick her finger on a spindle and fall into a deep sleep", "Turn into a dragon", "Be trapped in a tower", "Forget her true identity"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 229,
    question: "What does Cinderella's Fairy Godmother turn into a horse-drawn carriage?",
    answers: ["A pumpkin", "A watermelon", "A squash", "A turnip"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 230,
    question: "In The Princess and the Frog, what does Tiana dream of opening?",
    answers: ["A restaurant", "A bakery", "A dance studio", "A hotel"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 231,
    question: "What is Flynn Rider's horse's name in Tangled?",
    answers: ["Maximus", "Angus", "Khan", "Phillip"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 232,
    question: "In Frozen, who is the ice harvester who helps Anna find Elsa?",
    answers: ["Kristoff", "Hans", "The Duke of Weselton", "Olaf"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 233,
    question: "What gift does Isabela have in Encanto?",
    answers: ["Growing flowers and plants", "Super strength", "Healing", "Shapeshifting"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 234,
    question: "In Wreck-It Ralph, what is the name of the candy-themed racing game?",
    answers: ["Sugar Rush", "Candy Kart", "Sweet Speedway", "Candy Kingdom Racers"],
    correct: 0, difficulty: "easy", category: "movies"
  },
  {
    id: 235,
    question: "In The Emperor's New Groove, what animal does Kuzco accidentally get turned into?",
    answers: ["A llama", "A frog", "A bear", "A cat"],
    correct: 0, difficulty: "easy", category: "movies"
  },

  // =========================================================
  // MOVIES — MEDIUM (236–263)
  // =========================================================
  {
    id: 236,
    question: "In Zootopia, who turns out to be the true mastermind villain?",
    answers: ["Dawn Bellwether", "Mayor Lionheart", "Mr. Big", "Duke Weaselton"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 237,
    question: "In Big Hero 6, what is the name of Hiro's older brother?",
    answers: ["Tadashi", "Wasabi", "Fred", "Honey Lemon"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 238,
    question: "In Big Hero 6, what fictional city does the story take place in?",
    answers: ["San Fransokyo", "Neo San Francisco", "Techno Bay", "Futurisco"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 239,
    question: "In The Nightmare Before Christmas, what is the name of Jack Skellington's ghost dog?",
    answers: ["Zero", "Ghost", "Boo", "Bones"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 240,
    question: "In Pocahontas, what is the name of Pocahontas's best friend?",
    answers: ["Nakoma", "Kocoum", "Grandmother Willow", "Meeko"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 241,
    question: "What is the name of Mulan's horse?",
    answers: ["Khan", "Angus", "Maximus", "Samson"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 242,
    question: "In Toy Story 2, which character pretends to be a mentor but is secretly the villain?",
    answers: ["Stinky Pete the Prospector", "Al McWhiggin", "Emperor Zurg", "Lotso"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 243,
    question: "In Frozen, what is the name of Prince Hans' kingdom?",
    answers: ["The Southern Isles", "Arendelle", "Weselton", "Northuldra"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 244,
    question: "In Coco, who is the true original songwriter of the songs Ernesto de la Cruz claims as his own?",
    answers: ["Héctor", "Chicharrón", "Papá Julio", "Miguel"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 245,
    question: "In The Princess and the Frog, what is the name of the firefly who is in love with a star?",
    answers: ["Ray", "Louis", "Charlotte", "James"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 246,
    question: "In 101 Dalmatians, how many puppies do Pongo and Perdita originally have?",
    answers: ["15", "99", "101", "50"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 247,
    question: "In The Fox and the Hound, what are the names of the two main animal characters?",
    answers: ["Tod and Copper", "Fox and Dog", "Red and Blue", "Wily and Butch"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 248,
    question: "In The Rescuers, what organization do mice Bernard and Miss Bianca work for?",
    answers: ["The Rescue Aid Society", "The World Mouse Agency", "The International Rescue Bureau", "The Mouse League"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 249,
    question: "In Atlantis: The Lost Empire, what lost place does young Milo Thatch seek?",
    answers: ["The continent of Atlantis", "El Dorado", "Avalon", "Shangri-La"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 250,
    question: "In Pocahontas, what type of animal is the hummingbird Flit?",
    answers: ["A hummingbird", "A parrot", "A hawk", "A sparrow"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 251,
    question: "In Encanto, which Madrigal family member can see the future?",
    answers: ["Bruno", "Camilo", "Dolores", "Luisa"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 252,
    question: "In The Princess and the Frog, who is Charlotte La Bouff's wealthy father?",
    answers: ["Big Daddy La Bouff", "Eli La Bouff", "Louis La Bouff", "Etienne La Bouff"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 253,
    question: "What are the names of Cinderella's two wicked stepsisters?",
    answers: ["Anastasia and Drizella", "Victoria and Lavinia", "Prudence and Millicent", "Beatrice and Eugenia"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 254,
    question: "In The Rescuers Down Under, what rare animal does the boy Cody try to protect?",
    answers: ["Marahute the golden eagle", "A rare white kangaroo", "A rainbow parrot", "A white crocodile"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 255,
    question: "In Mulan, what is the name of the Hun leader and main villain?",
    answers: ["Shan Yu", "General Li", "Chi Fu", "Emperor Shang"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 256,
    question: "In Oliver & Company, what famous city does the story take place in?",
    answers: ["New York City", "Los Angeles", "Chicago", "Miami"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 257,
    question: "In Oliver & Company, who is the ruthless loan shark villain?",
    answers: ["Sykes", "Fagin", "Dodger", "Roscoe"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 258,
    question: "In Peter Pan, what gift does Wendy give Peter that makes Tinker Bell jealous?",
    answers: ["A kiss (called a thimble)", "A hug", "Her shadow", "A story"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 259,
    question: "In Treasure Planet, who is the morally complex villain and reluctant mentor to Jim?",
    answers: ["Long John Silver", "Scroop", "Captain Flint", "Black Dog"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 260,
    question: "In Wreck-It Ralph, what is the name of the girl racer Ralph befriends in Sugar Rush?",
    answers: ["Vanellope von Schweetz", "Taffyta Muttonfudge", "Rancis Fluggerbutter", "Candlehead"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 261,
    question: "In Frozen, what is the name of Kristoff's reindeer?",
    answers: ["Sven", "Bjorn", "Lars", "Erik"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 262,
    question: "In The Nightmare Before Christmas, what is the name of Jack Skellington's ragdoll love interest?",
    answers: ["Sally", "Shock", "Oogie", "Lock"],
    correct: 0, difficulty: "medium", category: "movies"
  },
  {
    id: 263,
    question: "In Ratatouille, what is the shocking secret about Alfredo Linguini that is revealed?",
    answers: ["Auguste Gusteau is his biological father", "He secretly knows how to cook", "He used to be a food critic", "He owns the restaurant"],
    correct: 0, difficulty: "medium", category: "movies"
  },

  // =========================================================
  // MOVIES — HARD (264–278)
  // =========================================================
  {
    id: 264,
    question: "In The Aristocats, what European city does the story take place in?",
    answers: ["Paris, France", "London, England", "Rome, Italy", "Vienna, Austria"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 265,
    question: "In Sleeping Beauty, which of the three good fairies changes Maleficent's death curse to a deep sleep?",
    answers: ["Merryweather", "Flora", "Fauna", "Lumina"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 266,
    question: "In Pinocchio, what is the name of the island where boys are turned into donkeys?",
    answers: ["Pleasure Island", "Treasure Island", "Pony Land", "Donkey Island"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 267,
    question: "In The Hunchback of Notre Dame, what are the names of Quasimodo's three gargoyle friends?",
    answers: ["Victor, Hugo, and Laverne", "Peter, Paul, and Mary", "Larry, Moe, and Curly", "Faith, Hope, and Charity"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 268,
    question: "In The Sword in the Stone, what is the nickname of the boy who will become King Arthur?",
    answers: ["Wart", "Arthur", "Lancelot", "Galahad"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 269,
    question: "In Fantasia, which Paul Dukas piece accompanies Mickey Mouse as The Sorcerer's Apprentice?",
    answers: ["The Sorcerer's Apprentice", "Night on Bald Mountain", "The Nutcracker Suite", "The Rite of Spring"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 270,
    question: "In Dumbo, what is the name of Dumbo's mother?",
    answers: ["Mrs. Jumbo", "Nellie", "Ellie", "Dumba"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 271,
    question: "In The Sword in the Stone, what is the name of Merlin's pet owl?",
    answers: ["Archimedes", "Hooter", "Newton", "Feathers"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 272,
    question: "What is the name of the butler villain in The Aristocats who stands to inherit everything?",
    answers: ["Edgar", "Henri", "Ferdinand", "Jacques"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 273,
    question: "In Tarzan, what is the full name of Jane's scientist father?",
    answers: ["Professor Archimedes Q. Porter", "Professor James Porter", "Dr. Henry Porter", "Professor William Robinson"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 274,
    question: "In 101 Dalmatians, what are the names of Cruella's two dimwitted henchmen?",
    answers: ["Jasper and Horace", "Larry and Lenny", "Biff and Griff", "Sid and Ted"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 275,
    question: "In The Rescuers, what is the name of the little orphan girl that Bernard and Miss Bianca rescue?",
    answers: ["Penny", "Jenny", "Molly", "Annie"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 276,
    question: "What Disney classic features a villain named Madam Mim who battles Merlin in a magic duel?",
    answers: ["The Sword in the Stone", "The Black Cauldron", "The Great Mouse Detective", "Sleeping Beauty"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 277,
    question: "In The Hunchback of Notre Dame, what is the name of Esmeralda's pet goat?",
    answers: ["Djali", "Clopin", "Achilles", "Quasi"],
    correct: 0, difficulty: "hard", category: "movies"
  },
  {
    id: 278,
    question: "In Sleeping Beauty, what is the name of Maleficent's domain?",
    answers: ["The Forbidden Mountain", "The Dark Castle", "The Shadow Keep", "Maleficent's Peak"],
    correct: 0, difficulty: "hard", category: "movies"
  },

  // =========================================================
  // CHARACTERS — EASY (279–300)
  // =========================================================
  {
    id: 279,
    question: "In Frozen, what type of animal is Sven?",
    answers: ["A reindeer", "A horse", "A moose", "A dog"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 280,
    question: "What is the name of Winnie the Pooh's bouncing tiger friend?",
    answers: ["Tigger", "Eeyore", "Piglet", "Roo"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 281,
    question: "Where does Peter Pan live?",
    answers: ["Neverland", "Fantasyland", "Dreamland", "Fairyland"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 282,
    question: "What is Simba's mother's name in The Lion King?",
    answers: ["Sarabi", "Nala", "Kiara", "Sarafina"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 283,
    question: "What is the name of Ariel's father, the king of the sea?",
    answers: ["King Triton", "King Neptune", "King Poseidon", "King Aquaman"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 284,
    question: "In Beauty and the Beast, which household object is Cogsworth?",
    answers: ["A clock", "A candlestick", "A teapot", "A wardrobe"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 285,
    question: "What is the name of the fairy who accompanies Peter Pan?",
    answers: ["Tinker Bell", "Pixie", "Glitter", "Fairy Dust"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 286,
    question: "In Snow White, which dwarf never speaks?",
    answers: ["Dopey", "Sleepy", "Bashful", "Grumpy"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 287,
    question: "In Cinderella, what do the mice help Cinderella make for the ball?",
    answers: ["Her ball gown", "Glass slippers", "A carriage", "A tiara"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 288,
    question: "What is the name of Ariel's fish best friend in The Little Mermaid?",
    answers: ["Flounder", "Sebastian", "Scuttle", "Grimsby"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 289,
    question: "In Aladdin, what is the name of Princess Jasmine's pet tiger?",
    answers: ["Rajah", "Shere", "Tiger", "Stripes"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 290,
    question: "What is the name of Ariel's seagull friend in The Little Mermaid?",
    answers: ["Scuttle", "Flounder", "Sebastian", "Grimsby"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 291,
    question: "In The Lion King, who is Simba's childhood best friend?",
    answers: ["Nala", "Timon", "Zazu", "Pumbaa"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 292,
    question: "In Monsters, Inc., what is the name of the little girl Sulley befriends?",
    answers: ["Boo", "Sue", "Bonnie", "Mary"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 293,
    question: "In Cars, what is the name of Lightning McQueen's best friend tow truck?",
    answers: ["Mater", "Finn", "Ramone", "Chick"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 294,
    question: "What is Donald Duck's middle name?",
    answers: ["Fauntleroy", "Eugene", "Barnabas", "Frederick"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 295,
    question: "What type of animal is Pegasus in Hercules?",
    answers: ["A winged horse", "A griffin", "A dragon", "A unicorn"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 296,
    question: "In Mulan, what is the name of Mulan's lucky cricket?",
    answers: ["Cri-Kee", "Jiminy", "Lucky", "Pal"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 297,
    question: "What are the names of Pongo and Perdita's human owners in 101 Dalmatians?",
    answers: ["Roger and Anita", "Carl and Ellie", "Jim and Sarah", "Bob and Betty"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 298,
    question: "In Toy Story, what is the name of the space ranger toy who becomes Woody's friend?",
    answers: ["Buzz Lightyear", "Emperor Zurg", "Lotso", "Rex"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 299,
    question: "In The Jungle Book, what type of snake hypnotizes Mowgli?",
    answers: ["A python (Kaa)", "A cobra", "A mamba", "A boa constrictor"],
    correct: 0, difficulty: "easy", category: "characters"
  },
  {
    id: 300,
    question: "What is the name of Winnie the Pooh's human friend?",
    answers: ["Christopher Robin", "Billy Moon", "Piglet", "Roo"],
    correct: 0, difficulty: "easy", category: "characters"
  },

  // =========================================================
  // CHARACTERS — MEDIUM (301–322)
  // =========================================================
  {
    id: 301,
    question: "In Zootopia, what is the name of Nick Wilde's tiny con partner?",
    answers: ["Finnick", "Duke Weaselton", "Jerry Vole", "Peter Moosebridge"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 302,
    question: "In Big Hero 6, who is the masked villain Yokai's true identity?",
    answers: ["Professor Robert Callaghan", "Alistair Krei", "Professor Granville", "Fred's father"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 303,
    question: "In Toy Story 3, what is the name of the strawberry-scented bear villain?",
    answers: ["Lots-o'-Huggin' Bear (Lotso)", "Big Baby", "Chuckles", "Ken"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 304,
    question: "In Brave, what are the names of Merida's triplet younger brothers?",
    answers: ["Harris, Hubert, and Hamish", "Larry, Moe, and Curly", "Tick, Tack, and Tock", "Alvin, Simon, and Theodore"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 305,
    question: "In Cars, what is the name of Lightning McQueen's primary racing sponsor?",
    answers: ["Rust-eze", "Dinoco", "Octane Gain", "Vitoline"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 306,
    question: "In Finding Nemo, what is the name of the great white shark who is trying to give up eating fish?",
    answers: ["Bruce", "Anchor", "Chum", "Jaws"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 307,
    question: "In Hercules, who is Hercules' satyr trainer and mentor?",
    answers: ["Phil (Philoctetes)", "Zeus", "Hades", "Pegasus"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 308,
    question: "In Inside Out, what is the name of Riley's imaginary friend?",
    answers: ["Bing Bong", "Ping Pong", "Bong Bing", "Happy"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 309,
    question: "In Mulan, what is the name of the Hun warlord villain?",
    answers: ["Shan Yu", "General Li", "Chi Fu", "Khan"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 310,
    question: "What are the names of Peter Pan's two Wendy's brothers?",
    answers: ["John and Michael", "James and Timothy", "George and Edward", "Tom and Harry"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 311,
    question: "In The Aristocats, what are the names of Duchess's three kittens?",
    answers: ["Marie, Berlioz, and Toulouse", "Lily, Rose, and Daisy", "Fluffy, Patches, and Mittens", "Kitty, Whiskers, and Sox"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 312,
    question: "In The Nightmare Before Christmas, what are the names of Oogie Boogie's three trick-or-treat helpers?",
    answers: ["Lock, Shock, and Barrel", "Grim, Ghost, and Ghoul", "Trick, Treat, and Terror", "Bone, Blood, and Bite"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 313,
    question: "In The Hunchback of Notre Dame, who is the brave soldier who falls for Esmeralda?",
    answers: ["Phoebus", "Frollo", "Clopin", "Quasimodo"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 314,
    question: "In Coco, who placed the ban on music in the Rivera family?",
    answers: ["Mamá Imelda", "Mamá Coco", "Abuelita Elena", "Papá Julio"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 315,
    question: "In Moana, what is the name of the giant glittery crab who hoards shiny objects?",
    answers: ["Tamatoa", "Te Kā", "Lalotai", "Aumoe"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 316,
    question: "In The Rescuers Down Under, what is the name of the rare golden eagle Cody befriends?",
    answers: ["Marahute", "Eagle", "Goldie", "Sunwing"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 317,
    question: "In Lilo & Stitch, what is the name of the social worker who tries to take Lilo away?",
    answers: ["Cobra Bubbles", "Agent Hood", "Mr. Stern", "Officer Reynolds"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 318,
    question: "In Tarzan, what is the name of Tarzan's gorilla best friend?",
    answers: ["Terk", "Kala", "Tantor", "Kerchak"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 319,
    question: "In Wreck-It Ralph, what is King Candy's true identity?",
    answers: ["Turbo, a racer from another game", "A glitch in the Sugar Rush code", "An escaped villain from Hero's Duty", "A deleted character from Sugar Rush"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 320,
    question: "In Cars, who is Lightning McQueen's main rival racer?",
    answers: ["Chick Hicks", "The King", "Finn McMissile", "Francesco Bernoulli"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 321,
    question: "In Oliver & Company, who is the cool, smooth-talking lead dog of Fagin's gang?",
    answers: ["Dodger", "Einstein", "Tito", "Francis"],
    correct: 0, difficulty: "medium", category: "characters"
  },
  {
    id: 322,
    question: "In Brave, what animal does Merida's mother Queen Elinor accidentally transform into?",
    answers: ["A bear", "A deer", "A wolf", "A fox"],
    correct: 0, difficulty: "medium", category: "characters"
  },

  // =========================================================
  // CHARACTERS — HARD (323–333)
  // =========================================================
  {
    id: 323,
    question: "In Sleeping Beauty, what is the name of Maleficent's loyal raven?",
    answers: ["Diablo", "Corvus", "Raven", "Shade"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 324,
    question: "What title is Bambi's father known by in the film?",
    answers: ["The Great Prince of the Forest", "The Stag King", "Lord of the Meadow", "The Elder Buck"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 325,
    question: "In The Great Mouse Detective, what is Professor Ratigan's true species (despite his protests)?",
    answers: ["A rat", "A mouse", "A shrew", "A vole"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 326,
    question: "In The Sword in the Stone, what is the name of Merlin's pet owl?",
    answers: ["Archimedes", "Hooter", "Newton", "Feathers"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 327,
    question: "In Bambi, what are the names of the three characters Bambi meets in the opening scene as a fawn?",
    answers: ["Thumper, Flower, and Faline", "Thumper, Flower, and Friend Owl", "Faline, Thumper, and the Great Prince", "Flower, Friend Owl, and Faline"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 328,
    question: "In The Aristocats, what is the full name of the butler villain?",
    answers: ["Edgar Balthazar", "Edgar Beaumont", "Edgar Dupont", "Edgar Rousseau"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 329,
    question: "In The Hunchback of Notre Dame, what is the name of Esmeralda's pet goat?",
    answers: ["Djali", "Clopin", "Achilles", "Quasi"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 330,
    question: "In The Sword in the Stone, what is the name of the female wizard who battles Merlin?",
    answers: ["Madam Mim", "Morgana", "Maleficent", "Ursula"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 331,
    question: "What are the names of the three hitchhiking ghosts in the Haunted Mansion attraction?",
    answers: ["Gus, Ezra, and Phineas", "Grim, Ghoul, and Ghost", "Bones, Skull, and Coffin", "Rex, Max, and Zap"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 332,
    question: "In Pocahontas, what type of animal is Percy, Governor Ratcliffe's pampered pet?",
    answers: ["A pug dog", "A parrot", "A cat", "A ferret"],
    correct: 0, difficulty: "hard", category: "characters"
  },
  {
    id: 333,
    question: "In The Rescuers, what are the names of Madame Medusa's two pet alligators?",
    answers: ["Brutus and Nero", "Snap and Crunch", "Jaws and Rex", "Fluffy and Spike"],
    correct: 0, difficulty: "hard", category: "characters"
  },

  // =========================================================
  // DISNEY PARKS — EASY (334–351)
  // =========================================================
  {
    id: 334,
    question: "In which Walt Disney World park is Pandora — The World of Avatar located?",
    answers: ["Animal Kingdom", "EPCOT", "Hollywood Studios", "Magic Kingdom"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 335,
    question: "In which Magic Kingdom land can you find Space Mountain?",
    answers: ["Tomorrowland", "Fantasyland", "Adventureland", "Frontierland"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 336,
    question: "In which Magic Kingdom land can you find Big Thunder Mountain Railroad?",
    answers: ["Frontierland", "Tomorrowland", "Adventureland", "Fantasyland"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 337,
    question: "What is the name of the main entrance street at Magic Kingdom?",
    answers: ["Main Street, U.S.A.", "Main Boulevard", "Disney Way", "Fantasyland Road"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 338,
    question: "Which Disney World park features a 'World Showcase' with pavilions representing different countries?",
    answers: ["EPCOT", "Magic Kingdom", "Animal Kingdom", "Hollywood Studios"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 339,
    question: "What is the name of the themed land in Magic Kingdom with fairy-tale castles and attractions?",
    answers: ["Fantasyland", "Adventureland", "Tomorrowland", "Frontierland"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 340,
    question: "What famous pineapple soft-serve ice cream treat is beloved at Disney parks?",
    answers: ["Dole Whip", "Pineapple Swirl", "Tiki Treat", "Tropical Freeze"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 341,
    question: "In which Disney World park is the Tower of Terror located?",
    answers: ["Hollywood Studios", "EPCOT", "Magic Kingdom", "Animal Kingdom"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 342,
    question: "What is the name of the Disney Skyliner gondola system that connects resorts and parks at Walt Disney World?",
    answers: ["Disney Skyliner", "Disney Sky Gondola", "Disney SkyTram", "Disney AerialRide"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 343,
    question: "What is the name of Disney World's water park with an icy, ski-resort theme?",
    answers: ["Blizzard Beach", "Typhoon Lagoon", "Ice Mountain", "Powder Keg"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 344,
    question: "What is the name of the signature roller coaster in Fantasyland at Magic Kingdom?",
    answers: ["Seven Dwarfs Mine Train", "Big Thunder Mountain", "Space Mountain", "The Barnstormer"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 345,
    question: "What is the name of the famous nighttime spectacular at Disneyland featuring Mickey Mouse battling villains?",
    answers: ["Fantasmic!", "SpectroMagic", "World of Color", "Illuminations"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 346,
    question: "Where is Walt Disney's preserved private apartment located at Disneyland?",
    answers: ["Above the fire station on Main Street, U.S.A.", "Inside the Town Hall", "Above the Opera House", "In City Hall"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 347,
    question: "What is the name of the shopping and dining district at Walt Disney World (formerly Downtown Disney)?",
    answers: ["Disney Springs", "Disney Town", "Disney Plaza", "Disney Boulevard"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 348,
    question: "In which Walt Disney World park is the Na'vi River Journey ride located?",
    answers: ["Animal Kingdom", "EPCOT", "Hollywood Studios", "Magic Kingdom"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 349,
    question: "What famous food shaped like Mickey Mouse is a classic treat sold at Disney parks?",
    answers: ["Mickey-shaped waffles", "Mickey-shaped pretzels", "Mickey-shaped popcorn", "Mickey-shaped bread"],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 350,
    question: "What is the name of the Magic Kingdom area that evokes early America, home of the Hall of Presidents?",
    answers: ["Liberty Square", "Frontierland", "Adventureland", "Main Street, U.S.A."],
    correct: 0, difficulty: "easy", category: "parks"
  },
  {
    id: 351,
    question: "What is the name of the boat transportation that connects EPCOT to Hollywood Studios and Animal Kingdom?",
    answers: ["Friendship Boats", "Disney Water Taxis", "Resort Launches", "EPCOT Ferries"],
    correct: 0, difficulty: "easy", category: "parks"
  },

  // =========================================================
  // DISNEY PARKS — MEDIUM (352–368)
  // =========================================================
  {
    id: 352,
    question: "What is the name of the Star Wars-themed immersive hotel at Walt Disney World that opened and closed in 2022–2023?",
    answers: ["Star Wars: Galactic Starcruiser", "The Halcyon Hotel", "Star Wars Resort", "Galactic Inn"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 353,
    question: "What is the name of the white-water rafting ride at Animal Kingdom?",
    answers: ["Kali River Rapids", "Expedition Splash", "Congo Cascade", "White Water Run"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 354,
    question: "In what year did the Haunted Mansion open at Magic Kingdom?",
    answers: ["1971", "1969", "1975", "1980"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 355,
    question: "What EPCOT ride takes guests on a simulated journey to Mars?",
    answers: ["Mission: SPACE", "Guardians of the Galaxy: Cosmic Rewind", "Test Track", "Spaceship Earth"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 356,
    question: "What is the name of the EPCOT ride where guests test a car at high simulated speeds?",
    answers: ["Test Track", "Mission: SPACE", "Spaceship Earth", "Journey Into Imagination"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 357,
    question: "In what year did Expedition Everest open at Animal Kingdom?",
    answers: ["2006", "2004", "2008", "2010"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 358,
    question: "In what year did Disneyland Paris open?",
    answers: ["1992", "1989", "1995", "1999"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 359,
    question: "What was the term used for Disney's most thrilling rides in the original Disneyland coupon-book system?",
    answers: ["E-Ticket attractions", "A-List rides", "Gold Pass attractions", "Premium rides"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 360,
    question: "What is the name of the EPCOT ride that opened in 2022 themed around Guardians of the Galaxy?",
    answers: ["Guardians of the Galaxy: Cosmic Rewind", "Galaxy's Edge Coaster", "Marvel Mountain", "Infinity Ride"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 361,
    question: "What is the name of the Disney resort hotel overlooking an African animal savanna?",
    answers: ["Disney's Animal Kingdom Lodge", "Disney's Wilderness Lodge", "Disney's Safari Resort", "Disney's Savanna Inn"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 362,
    question: "What is the name of the Disney theme park located in Tokyo, Japan?",
    answers: ["Tokyo Disneyland", "Disney Japan", "Japan Magic Kingdom", "Tokyo Disney Park"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 363,
    question: "What is the name of the Disney theme park in Hong Kong?",
    answers: ["Hong Kong Disneyland", "Asia Magic Kingdom", "Disney China", "Hong Kong Disney Park"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 364,
    question: "In what year did Walt Disney World celebrate its 50th anniversary?",
    answers: ["2021", "2020", "2022", "2019"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 365,
    question: "What is the name of Disney's resort and spa in Hawaii?",
    answers: ["Aulani, a Disney Resort & Spa", "Disney Polynesian Hawaii", "Disney Honolulu", "Aloha Disney Resort"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 366,
    question: "What is the name of the immersive Star Wars land at Disney's Hollywood Studios?",
    answers: ["Star Wars: Galaxy's Edge", "Star Wars Zone", "The Outer Rim", "Force Land"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 367,
    question: "What is the name of the Tower of Terror ride's fictional hotel setting?",
    answers: ["Hollywood Tower Hotel", "The Sunset Hotel", "The Hollywood Haunt", "Tower Inn"],
    correct: 0, difficulty: "medium", category: "parks"
  },
  {
    id: 368,
    question: "What is the name of the Disney World hotel where guests can watch the monorail pass through the lobby?",
    answers: ["Disney's Contemporary Resort", "Grand Floridian", "Polynesian Village", "BoardWalk Inn"],
    correct: 0, difficulty: "medium", category: "parks"
  },

  // =========================================================
  // DISNEY PARKS — HARD (369–378)
  // =========================================================
  {
    id: 369,
    question: "What is the name of the rotating theater attraction at Magic Kingdom that chronicles American technology through the ages?",
    answers: ["Carousel of Progress", "Hall of Presidents", "American Adventure", "Hall of Technology"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 370,
    question: "In what year did Pirates of the Caribbean first open at Disneyland?",
    answers: ["1967", "1965", "1970", "1973"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 371,
    question: "What was the name of the original EPCOT nighttime lagoon spectacular that ran from 1999 to 2019?",
    answers: ["IllumiNations: Reflections of Earth", "SpectroMagic", "Harmonious", "Epcot Forever"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 372,
    question: "What Disney attraction was the first to ever use Audio-Animatronic figures?",
    answers: ["The Enchanted Tiki Room", "The Haunted Mansion", "It's a Small World", "Pirates of the Caribbean"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 373,
    question: "What is the name of the elevated transit ride in Tomorrowland at Magic Kingdom?",
    answers: ["Tomorrowland Transit Authority PeopleMover", "WEDway Express", "Future Commuter", "Tomorrowland Monorail"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 374,
    question: "What is the name of the underground tunnel system beneath Magic Kingdom used by cast members?",
    answers: ["Utilidors", "The Tunnels", "Underground Way", "Service Corridors"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 375,
    question: "What is the name of the adults-only waterfall pool on the Disney Dream and Disney Fantasy?",
    answers: ["Satellite Falls", "Cascade Falls", "Rainforest Pool", "Niagara"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 376,
    question: "What Disneyland attraction opened in 1956 was also the world's first daily-operating monorail in the Western Hemisphere?",
    answers: ["Disneyland Monorail", "The WEDway PeopleMover", "The Disneyland Railroad", "Matterhorn Bobsleds"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 377,
    question: "What year did the TRON Lightcycle / Run coaster open at Magic Kingdom?",
    answers: ["2023", "2021", "2022", "2024"],
    correct: 0, difficulty: "hard", category: "parks"
  },
  {
    id: 378,
    question: "What is the name of the Disneyland attraction inside the Matterhorn mountain?",
    answers: ["Matterhorn Bobsleds", "Alpine Coaster", "Yeti Run", "Snowpeak Express"],
    correct: 0, difficulty: "hard", category: "parks"
  },

  // =========================================================
  // WALT DISNEY — EASY (379–389)
  // =========================================================
  {
    id: 379,
    question: "What was the name of Walt Disney's first studio, co-founded with his brother Roy?",
    answers: ["Disney Brothers Cartoon Studio", "Walt Disney Productions", "Laugh-O-Gram Films", "Mickey Mouse Studios"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 380,
    question: "In what year was Mickey Mouse's first synchronized-sound cartoon, Steamboat Willie, released?",
    answers: ["1928", "1925", "1930", "1932"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 381,
    question: "Which Disney theme park did Walt personally oversee and see opened during his lifetime?",
    answers: ["Disneyland", "Walt Disney World", "EPCOT", "Tokyo Disneyland"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 382,
    question: "What state did Walt Disney move to from the Midwest in order to pursue his animation career?",
    answers: ["California", "New York", "Florida", "Texas"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 383,
    question: "Who was the animator who helped Walt Disney design Mickey Mouse's original look?",
    answers: ["Ub Iwerks", "Ward Kimball", "Ted Sears", "Les Clark"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 384,
    question: "In what Missouri town did Walt Disney spend part of his childhood?",
    answers: ["Marceline", "Kansas City", "St. Louis", "Springfield"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 385,
    question: "What is the name of Walt Disney's wife?",
    answers: ["Lillian Disney", "Edna Disney", "Mary Disney", "Rose Disney"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 386,
    question: "How many daughters did Walt Disney have?",
    answers: ["Two (Diane and Sharon)", "One", "Three", "None"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 387,
    question: "What nickname was Walt Disney known by among fans and employees?",
    answers: ["Uncle Walt", "Mr. Disney", "Walt the Dreamer", "Mr. D"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 388,
    question: "What was the name of Walt Disney's brother and business partner?",
    answers: ["Roy O. Disney", "Ward Disney", "Ray Disney", "Robert Disney"],
    correct: 0, difficulty: "easy", category: "walt"
  },
  {
    id: 389,
    question: "What city was Walt Disney born in?",
    answers: ["Chicago, Illinois", "Kansas City, Missouri", "Los Angeles, California", "New York City, New York"],
    correct: 0, difficulty: "easy", category: "walt"
  },

  // =========================================================
  // WALT DISNEY — MEDIUM (390–402)
  // =========================================================
  {
    id: 390,
    question: "What was the name of Walt Disney's live-action nature documentary film series?",
    answers: ["True-Life Adventures", "Nature's Wonders", "Disney Nature Shorts", "Wild Kingdom"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 391,
    question: "Which U.S. president awarded Walt Disney the Presidential Medal of Freedom in 1964?",
    answers: ["Lyndon B. Johnson", "John F. Kennedy", "Dwight D. Eisenhower", "Richard Nixon"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 392,
    question: "What was Walt Disney's original vision for EPCOT before his death?",
    answers: ["An experimental city of tomorrow where real people would live and work", "A theme park dedicated to world cultures", "A nature preserve and conservation center", "A film production campus"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 393,
    question: "Who wrote the original Mary Poppins books that Walt Disney adapted into the 1964 film?",
    answers: ["P.L. Travers", "J.M. Barrie", "A.A. Milne", "Lewis Carroll"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 394,
    question: "In what year did The Walt Disney Company acquire Pixar Animation Studios?",
    answers: ["2006", "2003", "2009", "2012"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 395,
    question: "What name is given to the group of Walt Disney's core lead animators — his top creative team?",
    answers: ["The Nine Old Men", "Walt's Boys", "The Ink Squad", "The Originals"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 396,
    question: "What was the first Disney animated short to be made entirely in color, which also won the Academy Award for Best Animated Short Film?",
    answers: ["Flowers and Trees (1932)", "Steamboat Willie (1928)", "The Skeleton Dance (1929)", "Three Little Pigs (1933)"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 397,
    question: "Where is the Walt Disney Family Museum located?",
    answers: ["San Francisco, California (at the Presidio)", "Los Angeles, California", "Anaheim, California", "Marceline, Missouri"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 398,
    question: "In what year did Roy O. Disney pass away, just months after Walt Disney World opened?",
    answers: ["1971", "1973", "1969", "1975"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 399,
    question: "What innovative camera technique did Disney develop to create a sense of depth in 2D animation?",
    answers: ["The multiplane camera", "The zoom lens method", "The parallax camera", "The stereoscopic technique"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 400,
    question: "In what year did the Walt Disney Studios move from Hollywood to their current Burbank, California location?",
    answers: ["1940", "1935", "1945", "1950"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 401,
    question: "What is the full name of the company responsible for designing and building all Disney theme parks?",
    answers: ["Walt Disney Imagineering", "WED Enterprises", "Disney Creative Group", "Disney Theme Park Design"],
    correct: 0, difficulty: "medium", category: "walt"
  },
  {
    id: 402,
    question: "What does WED stand for in WED Enterprises, Walt's personal design company?",
    answers: ["Walter Elias Disney", "Walt's Entertainment Division", "World Entertainment Design", "Walt's Engineering Department"],
    correct: 0, difficulty: "medium", category: "walt"
  },

  // =========================================================
  // WALT DISNEY — HARD (403–410)
  // =========================================================
  {
    id: 403,
    question: "In what city was Walt Disney's Laugh-O-Gram Films animation studio located?",
    answers: ["Kansas City, Missouri", "Chicago, Illinois", "Los Angeles, California", "New York City, New York"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 404,
    question: "What was Disney's first all-live-action feature film, released in 1950?",
    answers: ["Treasure Island", "20,000 Leagues Under the Sea", "Davy Crockett", "The Swiss Family Robinson"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 405,
    question: "What animation technique — in which live actors are filmed and then traced by animators — was used in Snow White to achieve realistic human movement?",
    answers: ["Rotoscoping", "The multiplane camera", "Motion capture", "Live reference animation"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 406,
    question: "In what year did Walt Disney win his first Academy Award for Best Animated Short Film, for Flowers and Trees?",
    answers: ["1932", "1930", "1935", "1928"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 407,
    question: "What is the name of the miniature railroad Walt Disney built at his Holmby Hills, California home?",
    answers: ["Carolwood Pacific Railroad", "Disney Home Railway", "Lilly Belle Express", "Riverside Train"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 408,
    question: "What company originally owned Oswald the Lucky Rabbit, forcing Walt to create a new character?",
    answers: ["Universal Pictures", "MGM", "Paramount", "RKO"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 409,
    question: "Approximately how many Academy Awards did Walt Disney win or receive in his lifetime — the most ever by one individual?",
    answers: ["22", "10", "15", "30"],
    correct: 0, difficulty: "hard", category: "walt"
  },
  {
    id: 410,
    question: "Which art school did Walt Disney briefly attend in Chicago as a teenager?",
    answers: ["The Art Institute of Chicago", "The Chicago Academy of Fine Arts", "Columbia College Chicago", "DePaul Art School"],
    correct: 0, difficulty: "hard", category: "walt"
  },

  // =========================================================
  // DISNEY CRUISE LINE — EASY (411–421)
  // =========================================================
  {
    id: 411,
    question: "What are the names of the two original Disney Cruise Line ships that launched in the late 1990s?",
    answers: ["Disney Magic and Disney Wonder", "Disney Dream and Disney Fantasy", "Disney Wish and Disney Treasure", "Disney Magic and Disney Dream"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 412,
    question: "How many ships are in the Disney Cruise Line fleet as of 2025?",
    answers: ["Six", "Four", "Five", "Seven"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 413,
    question: "What is the name of the children's nursery on Disney Cruise Line ships for young toddlers?",
    answers: ["It's a Small World Nursery", "Mickey's Nursery", "Disney Baby Care", "Pixie Dust Nursery"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 414,
    question: "What is the name of the spa found on Disney Cruise Line ships?",
    answers: ["Senses Spa & Salon", "Disney Retreat Spa", "Magic Wellness", "Relaxation Station"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 415,
    question: "How many restaurants does Disney Cruise Line's rotational dining system cycle through?",
    answers: ["Three", "Two", "Four", "Five"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 416,
    question: "What is the name of Disney Cruise Line's loyalty program for returning guests?",
    answers: ["Castaway Club", "Disney Rewards", "Club Mickey", "Magic Circle"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 417,
    question: "What is the name of the main theater on Disney Cruise ships where Broadway-style shows are performed?",
    answers: ["Walt Disney Theatre", "Disney Broadway", "Magic Kingdom Stage", "Stateroom Stage"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 418,
    question: "What is the name of the water coaster attraction on the Disney Wish?",
    answers: ["AquaMouse", "AquaDuck", "WaterShip", "Hydro Dash"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 419,
    question: "What special themed night on Disney cruises features costumes, deck parties, and fireworks at sea?",
    answers: ["Pirate Night", "Princess Night", "Superhero Night", "Adventure Night"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 420,
    question: "In the rotational dining system, what is unique about your servers on a Disney cruise?",
    answers: ["Your servers follow you to each restaurant each night", "You get new servers every night", "You stay in one restaurant the whole cruise", "Servers are chosen by random lottery"],
    correct: 0, difficulty: "easy", category: "cruise"
  },
  {
    id: 421,
    question: "What is the name of the large outdoor movie screen mounted on Disney Cruise ships?",
    answers: ["Funnel Vision", "Deck Cinema", "Big Screen at Sea", "Movie Deck"],
    correct: 0, difficulty: "easy", category: "cruise"
  },

  // =========================================================
  // DISNEY CRUISE LINE — MEDIUM (422–431)
  // =========================================================
  {
    id: 422,
    question: "In what year did the Disney Wish launch?",
    answers: ["2022", "2020", "2019", "2023"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 423,
    question: "What is the name of the Marvel-themed dining experience on the Disney Wish?",
    answers: ["Worlds of Marvel", "Avengers Dining", "Marvel Bistro", "Stark Industries Kitchen"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 424,
    question: "What is the name of the tween club (ages 11–14) on Disney Cruise ships?",
    answers: ["Edge", "Vibe", "The Loft", "Club Tween"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 425,
    question: "What is the name of the teen club (ages 14–17) on Disney Cruise ships?",
    answers: ["Vibe", "Edge", "The Loft", "Club Teen"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 426,
    question: "What year did Disney Cruise Line celebrate its 25th anniversary?",
    answers: ["2023", "2021", "2022", "2024"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 427,
    question: "What is the name of the Disney Cruise ship that launched in November 2024?",
    answers: ["Disney Treasure", "Disney Adventure", "Disney Destiny", "Disney Legend"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 428,
    question: "What is the approximate passenger capacity of the Disney Wish?",
    answers: ["4,000 guests", "2,500 guests", "6,000 guests", "1,800 guests"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 429,
    question: "What is the name of the Star Wars-themed bar on the Disney Wish?",
    answers: ["Hyperspace Lounge", "Cantina Bar", "Rebel Outpost", "Millennium Falcon Bar"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 430,
    question: "What type of dining does Palo offer on all Disney Cruise ships?",
    answers: ["Adults-only Italian dining (brunch and dinner)", "Adults-only French fine dining", "Family-style French dining", "Poolside Italian buffet"],
    correct: 0, difficulty: "medium", category: "cruise"
  },
  {
    id: 431,
    question: "What year was the Disney Fantasy launched?",
    answers: ["2012", "2011", "2014", "2010"],
    correct: 0, difficulty: "medium", category: "cruise"
  },

  // =========================================================
  // DISNEY CRUISE LINE — HARD (432–436)
  // =========================================================
  {
    id: 432,
    question: "What color scheme are Disney Cruise Line ships painted in?",
    answers: ["White hull with navy and red accents and Mickey Mouse silhouettes on the yellow funnels", "All white with gold trim", "Blue and white with red accents", "White hull with gold funnels"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 433,
    question: "In what country were the original Disney Cruise Line ships (Disney Magic and Disney Wonder) built?",
    answers: ["Italy", "Germany", "United States", "Finland"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 434,
    question: "What is the name of the fireworks show that Disney launches from their ships at sea on Pirate Night?",
    answers: ["Buccaneer Blast", "Pirate's Salute", "Cannon Fire", "Sea Blaze"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 435,
    question: "What is the name of the adults-only waterfall pool area on the Disney Dream and Fantasy?",
    answers: ["Satellite Falls", "Rainforest Falls", "Cascade Pool", "Neptune's Retreat"],
    correct: 0, difficulty: "hard", category: "cruise"
  },
  {
    id: 436,
    question: "What year did the Disney Dream launch?",
    answers: ["2011", "2009", "2013", "2015"],
    correct: 0, difficulty: "hard", category: "cruise"
  },

  // =========================================================
  // MUSIC & SONGS — EASY (437–449)
  // =========================================================
  {
    id: 437,
    question: "In which Disney film does 'You've Got a Friend in Me' appear?",
    answers: ["Toy Story", "Monsters, Inc.", "Cars", "The Incredibles"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 438,
    question: "Which character sings 'Let It Go' in Frozen?",
    answers: ["Elsa", "Anna", "Kristoff", "Olaf"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 439,
    question: "In which Disney film does 'I Just Can't Wait to Be King' appear?",
    answers: ["The Lion King", "The Jungle Book", "Hercules", "Mulan"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 440,
    question: "In which Disney film does 'Someday My Prince Will Come' appear?",
    answers: ["Snow White and the Seven Dwarfs", "Cinderella", "Sleeping Beauty", "The Little Mermaid"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 441,
    question: "Which character sings 'When You Wish Upon a Star' in Pinocchio?",
    answers: ["Jiminy Cricket", "Pinocchio", "Geppetto", "The Blue Fairy"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 442,
    question: "In which Disney film does the opening number 'Belle' appear?",
    answers: ["Beauty and the Beast", "Cinderella", "Sleeping Beauty", "Enchanted"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 443,
    question: "In which Disney film does 'Can You Feel the Love Tonight' appear?",
    answers: ["The Lion King", "Tarzan", "Hercules", "Mulan"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 444,
    question: "In which Disney film does 'Almost There' appear?",
    answers: ["The Princess and the Frog", "Moana", "Encanto", "Frozen"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 445,
    question: "In which Disney film does 'Go the Distance' appear?",
    answers: ["Hercules", "Mulan", "Pocahontas", "Moana"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 446,
    question: "In which Disney film does 'Surface Pressure' appear?",
    answers: ["Encanto", "Frozen", "Brave", "Moana"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 447,
    question: "In which Disney film does 'When She Loved Me' appear?",
    answers: ["Toy Story 2", "Toy Story", "Toy Story 3", "Toy Story 4"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 448,
    question: "What is the song Maui sings about himself in Moana?",
    answers: ["You're Welcome", "How Far I'll Go", "Shiny", "We Know the Way"],
    correct: 0, difficulty: "easy", category: "music"
  },
  {
    id: 449,
    question: "In which Disney film does 'Zero to Hero' appear?",
    answers: ["Hercules", "Mulan", "The Lion King", "Tarzan"],
    correct: 0, difficulty: "easy", category: "music"
  },

  // =========================================================
  // MUSIC & SONGS — MEDIUM (450–461)
  // =========================================================
  {
    id: 450,
    question: "Who sang 'Into the Unknown' as Elsa in Frozen 2?",
    answers: ["Idina Menzel", "Celine Dion", "Demi Lovato", "Adele"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 451,
    question: "Which famous singer performed 'Circle of Life' and 'Can You Feel the Love Tonight' for The Lion King (1994)?",
    answers: ["Elton John", "Phil Collins", "Hans Zimmer", "Lebo M"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 452,
    question: "Who wrote and performed the entire musical soundtrack for Tarzan (1999)?",
    answers: ["Phil Collins", "Elton John", "Michael Bolton", "Sting"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 453,
    question: "Who composed the orchestral score for The Lion King (1994), winning the Academy Award for Best Original Score?",
    answers: ["Hans Zimmer", "Alan Menken", "Elton John", "John Williams"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 454,
    question: "Who wrote the music and lyrics for The Little Mermaid's songs?",
    answers: ["Alan Menken (music) and Howard Ashman (lyrics)", "Alan Menken and Tim Rice", "The Sherman Brothers", "Phil Collins and Tim Rice"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 455,
    question: "Which Disney film's credits song 'Reflection' was performed by Christina Aguilera?",
    answers: ["Mulan", "Pocahontas", "Brave", "Moana"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 456,
    question: "Who wrote all of the songs for Encanto?",
    answers: ["Lin-Manuel Miranda", "Alan Menken", "The Sherman Brothers", "Elton John"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 457,
    question: "In which Disney film does the song 'Savages' appear?",
    answers: ["Pocahontas", "Mulan", "The Hunchback of Notre Dame", "Tarzan"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 458,
    question: "Which song from The Lion King actually won the Academy Award for Best Original Song (not 'Hakuna Matata' or 'Circle of Life')?",
    answers: ["Can You Feel the Love Tonight", "Hakuna Matata", "Circle of Life", "Be Prepared"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 459,
    question: "Who sings 'Beauty and the Beast' during the ballroom scene in the original 1991 animated film?",
    answers: ["Mrs. Potts (Angela Lansbury)", "Belle", "Lumiere", "The Beast"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 460,
    question: "What is the name of King Louie's swinging jazz number in The Jungle Book (1967)?",
    answers: ["I Wanna Be Like You", "Bear Necessities", "Trust in Me", "That's What Friends Are For"],
    correct: 0, difficulty: "medium", category: "music"
  },
  {
    id: 461,
    question: "Who co-wrote the songs for Moana alongside Lin-Manuel Miranda?",
    answers: ["Opetaia Foa'i", "Mark Mancina", "Howard Ashman", "Alan Menken"],
    correct: 0, difficulty: "medium", category: "music"
  },

  // =========================================================
  // MUSIC & SONGS — HARD (462–468)
  // =========================================================
  {
    id: 462,
    question: "What Academy Award did Phil Collins' 'You'll Be in My Heart' from Tarzan win at the 2000 ceremony?",
    answers: ["Best Original Song", "Best Original Score", "Best Original Soundtrack Album", "Best Pop Song"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 463,
    question: "In what year did 'Beauty and the Beast' win the Academy Award for Best Original Song?",
    answers: ["1992", "1990", "1994", "1988"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 464,
    question: "In which Disney film does the notably dark villain song 'Hellfire' appear?",
    answers: ["The Hunchback of Notre Dame", "Sleeping Beauty", "The Black Cauldron", "Hercules"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 465,
    question: "Who is credited as the lyricist for 'Circle of Life' and 'Can You Feel the Love Tonight' in The Lion King?",
    answers: ["Tim Rice", "Elton John", "Hans Zimmer", "Howard Ashman"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 466,
    question: "What Academy Award category did 'Let It Go' from Frozen win at the 2014 ceremony?",
    answers: ["Best Original Song", "Best Original Score", "Best Animated Feature", "Best Original Screenplay"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 467,
    question: "Which Disney film's soundtrack was the first to win the Grammy Award for Album of the Year?",
    answers: ["The Lion King (1994)", "Beauty and the Beast (1991)", "Aladdin (1992)", "Pocahontas (1995)"],
    correct: 0, difficulty: "hard", category: "music"
  },
  {
    id: 468,
    question: "What legendary Broadway composer wrote the songs for Aladdin and Beauty and the Beast before his untimely death in 1991?",
    answers: ["Howard Ashman", "Tim Rice", "Stephen Sondheim", "Marvin Hamlisch"],
    correct: 0, difficulty: "hard", category: "music"
  },

  // =========================================================
  // PIXAR — EASY (469–487)
  // =========================================================
  {
    id: 469,
    question: "In Toy Story 3, what is the name of the strawberry-scented bear villain?",
    answers: ["Lots-o'-Huggin' Bear (Lotso)", "Emperor Zurg", "Stinky Pete", "Big Baby"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 470,
    question: "In Finding Dory, what is the name of the friendly beluga whale?",
    answers: ["Bailey", "Destiny", "Hank", "Fluke"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 471,
    question: "In Inside Out 2, what new emotion is introduced as the main focus?",
    answers: ["Anxiety", "Envy", "Pride", "Nostalgia"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 472,
    question: "In which Pixar film does a boy discover he is secretly a sea monster while living in an Italian seaside town?",
    answers: ["Luca", "Soul", "Turning Red", "Onward"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 473,
    question: "In Turning Red, what does Meilin Lee transform into when she gets excited or emotional?",
    answers: ["A giant red panda", "A red fox", "A red dragon", "A red wolf"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 474,
    question: "In Onward, what type of magical creature are brothers Ian and Barley Lightfoot?",
    answers: ["Elves", "Dwarves", "Centaurs", "Fauns"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 475,
    question: "In Soul (2020), what is Joe Gardner's lifelong passion?",
    answers: ["Jazz music", "Basketball", "Cooking", "Painting"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 476,
    question: "In Toy Story 4, what is the name of the toy made from a plastic spork?",
    answers: ["Forky", "Sporky", "Spork", "Forkie"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 477,
    question: "In Monsters, Inc., what is the name of the large blue furry monster?",
    answers: ["Sulley", "Mike", "Randall", "Roz"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 478,
    question: "In Brave, what animal does Merida's mother accidentally turn into after eating a magic spell?",
    answers: ["A bear", "A deer", "A wolf", "A fox"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 479,
    question: "In Finding Nemo, what is the full address of the dentist's office where Nemo is held?",
    answers: ["P. Sherman, 42 Wallaby Way, Sydney", "42 Wallaby Way, Brisbane", "123 Shark Lane, Sydney", "P. Sherman, 42 Coral Road, Sydney"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 480,
    question: "In Inside Out 2, which new emotion wears a monocle and represents boredom?",
    answers: ["Ennui", "Anxiety", "Nostalgia", "Envy"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 481,
    question: "In Finding Dory, what type of animal is Destiny?",
    answers: ["A whale shark", "A beluga whale", "A blue whale", "A hammerhead shark"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 482,
    question: "What is the title of the Pixar film about a jazz musician who accidentally enters the afterlife?",
    answers: ["Soul", "Coco", "Inside Out", "Onward"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 483,
    question: "In The Incredibles 2, who is revealed to be the villain Screenslaver?",
    answers: ["Evelyn Deavor", "Winston Deavor", "The Underminer", "Ambassador Selick"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 484,
    question: "What is the name of WALL-E's cockroach companion?",
    answers: ["Hal", "Hank", "Bug", "Rex"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 485,
    question: "In Coco, what is the name of the fictional Mexican town where Miguel's family lives?",
    answers: ["Santa Cecilia", "Santa María", "San Miguel", "Santa Rosa"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 486,
    question: "In Toy Story 4, which toy from Woody's past does Woody reunite with?",
    answers: ["Bo Peep", "Buzz Lightyear", "Jessie", "Forky"],
    correct: 0, difficulty: "easy", category: "pixar"
  },
  {
    id: 487,
    question: "In Monsters University, what fraternity do Mike and Sulley join to compete in the Scare Games?",
    answers: ["Oozma Kappa (OK)", "Roar Omega Roar (ROR)", "Python Nu Kappa (PNK)", "Eta Hiss Hiss (HSS)"],
    correct: 0, difficulty: "easy", category: "pixar"
  },

  // =========================================================
  // PIXAR — MEDIUM (488–497)
  // =========================================================
  {
    id: 488,
    question: "In Ratatouille, what shocking family secret is revealed about Alfredo Linguini?",
    answers: ["Auguste Gusteau is his biological father", "He was secretly trained as a chef", "He used to be a food critic", "He owns the restaurant under a false name"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 489,
    question: "In The Incredibles, what are Violet's two superpowers?",
    answers: ["Creating force fields and turning invisible", "Flying and super strength", "Speed and invisibility", "Elasticity and force fields"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 490,
    question: "In Toy Story 2, who steals Woody to sell him to a museum in Japan?",
    answers: ["Al McWhiggin", "Stinky Pete", "Emperor Zurg", "Lotso"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 491,
    question: "In A Bug's Life, what does Flik build to try to scare away the grasshoppers?",
    answers: ["A giant fake bird", "A catapult", "A trap pit", "A scarecrow"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 492,
    question: "In Inside Out, which of Riley's Personality Islands is named for her favorite sport?",
    answers: ["Hockey Island", "Soccer Island", "Baseball Island", "Skating Island"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 493,
    question: "In Up, what is the name of Carl and Ellie's dream destination?",
    answers: ["Paradise Falls", "Angel Falls", "Victoria Falls", "Iguazu Falls"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 494,
    question: "In Finding Dory, what is the name of the grumpy seven-tentacled octopus (who lost one tentacle)?",
    answers: ["Hank", "Bailey", "Destiny", "Gerald"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 495,
    question: "In WALL-E, what is the name of the spaceship where all the remaining humans live?",
    answers: ["Axiom", "Genesis", "Elysium", "Olympus"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 496,
    question: "In Coco, what happens to a soul in the Land of the Dead when no living person remembers them?",
    answers: ["They experience the 'final death' and disappear forever", "They return to Earth as a ghost", "They are reincarnated", "They turn into a spirit animal"],
    correct: 0, difficulty: "medium", category: "pixar"
  },
  {
    id: 497,
    question: "In Luca, what happens to sea monsters when they get wet with water while on land?",
    answers: ["They revert to their sea monster form, revealing their true identity", "They become stronger", "They lose the ability to speak", "They can breathe underwater only"],
    correct: 0, difficulty: "medium", category: "pixar"
  },

  // =========================================================
  // PIXAR — HARD (498–500)
  // =========================================================
  {
    id: 498,
    question: "In Toy Story, what is the name of the astronaut program that Buzz Lightyear believes he is part of?",
    answers: ["Star Command", "Space Rangers Inc.", "Galaxy Patrol", "Universe Corps"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 499,
    question: "In A Bug's Life, what is the name of Flik's ant colony home?",
    answers: ["Ant Island", "Colony Alpha", "Bug Haven", "Grassland Colony"],
    correct: 0, difficulty: "hard", category: "pixar"
  },
  {
    id: 500,
    question: "In Soul, what is the name of the place where new souls develop their personalities before being born?",
    answers: ["The Great Before (You Seminar)", "The Great After", "The Soul World", "Limbo"],
    correct: 0, difficulty: "hard", category: "pixar"
  }

];
