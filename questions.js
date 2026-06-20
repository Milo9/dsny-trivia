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
  }

];
