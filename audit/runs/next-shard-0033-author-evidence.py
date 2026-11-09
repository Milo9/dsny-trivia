"""Batch 33: explicit editorial changes and source-grounded evidence notes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

changes = {}
def change(i,types,reason,**fields): changes[i]=(types,reason,fields)
change(2168,'clarification','Removed the gang name clue pixies and distinguished disused wings from permanent inability.',question="In Onward (2020), what is the name of Dewdrop's motorcycle gang?")
change(2169,'clarification','Removed unsupported shortcut characterization; the debate concerns the route.',question="In Onward (2020), which ancient trail does Barley suggest taking instead of the expressway?")
change(2170,'clarification','Specified the original English-language voice credit.',question="Who voices Laurel Lightfoot in the original English-language version of Onward (2020)?")
change(2171,'clarification difficulty','Asked directly about the filmmaker account and calibrated recognition difficulty.',question="Which loss from Dan Scanlon's childhood helped inspire the story of Onward?",difficulty='medium')
change(2174,'clarification difficulty','Vespa is a scooter brand rather than a specific model; calibrated easy.',question="In Luca (2021), which scooter brand do Luca and Alberto dream of owning?",difficulty='easy')
change(2176,'clarification','Removed an unnecessary first/sole-direction superlative.',question="Before directing Luca (2021), Enrico Casarosa directed which Pixar short?")
change(2178,'clarification','Distinguished an attempted disguise from a successful crossing.',question="In Coco (2017), whom does Héctor impersonate when he tries to get past the bridge checkpoint?")
change(2179,'clarification distractors','Made all proposed crimes parallel and removed the repeated songs wording clue.',question="In Coco (2017), what does Ernesto de la Cruz do to Héctor before taking credit for his music?",answers=['Poisons him','Tricks him into signing away the rights','Bribes his publisher','Waits for him to die of natural causes'])
change(2180,'clarification distractors','Used parallel, mutually exclusive permanent fates instead of uneven fragments.',question="In Coco (2017), what would missing the sunrise deadline mean for Miguel?",answers=['He would remain in the Land of the Dead','He would return home without his memories','He would return home as an old man','He would return home unable to play music'])
change(2181,'clarification','Shortened the role description without changing the three-dog fact.',question="In Up (2009), which trio names Charles Muntz's lead dog and his two main lieutenants?")
change(2182,'clarification','Removed unnecessary decades-long residence claim.',question="In Up (2009), what is the name of Charles Muntz's airship?")
change(2183,'clarification distractors','Replaced a long quotation and short distractors with parallel interpretations of the note.',question="In Up (2009), what does Ellie's final note in the Adventure Book encourage Carl to do?",answers=['Go have a new adventure','Stay home and preserve their belongings','Take the house back to their old street','Give up his friendship with Russell'])
change(2185,'distractors','Replaced a different film title with a plausible segment title.',answers=['Aim to Please','Tall Tail','An Uncommon Romance','A Royal Welcome'])
change(2187,'clarification','Removed unsupported chasing/nonrecognition motive; the dialogue establishes Jaq remains frightened.',question="In Cinderella II: Dreams Come True, which cat still frightens Jaq after he becomes human in 'Tall Tail'?")
change(2188,'clarification','Specified the film and the particular banquet assignment.',question="In Cinderella II: Dreams Come True, what event must Cinderella organize while the King and Prince are away in 'Aim to Please'?",answers=['A royal banquet','A treasury inspection','A royal wedding','A coronation'])
change(2190,'clarification','Tied reduced magic to freedom, rather than suggesting travel caused a gradual decline.',question="In The Return of Jafar, how does Genie describe his magic now that he is free?",answers=['Less powerful than before','More powerful than before','Completely gone','Transferred to Iago'])
change(2191,'clarification distractors','The Sultan says royal vizier; court advisor is also defensible and is replaced.',question="In The Return of Jafar, which title does the Sultan offer Aladdin during the palace dinner?",answers=['Royal vizier','Royal wizard','Head of the guard','Palace treasurer'])
change(2192,'clarification','Removed inaccurate timing shorthand for the framing/execution sequence.',question="In The Return of Jafar, whom does Jafar impersonate while accusing Aladdin of murdering the Sultan?")
change(2195,'clarification distractors','Made all options parallel actions with the same subject.',question="In Brother Bear 2, what do the Spirits do at the end so Nita can live with Kenai?",answers=['Turn Nita into a bear','Turn Kenai back into a human','Turn Atka into a bear','Turn Koda into a human'])
change(2196,'factual clarification','The brothers are trapped in the valley by their fear of Zugor, rather than rulers of Dark Mountain.',question="In Tarzan II, which pair of gorilla brothers lives near Dark Mountain with Mama Gunda?")
change(2200,'clarification','The supposed rejuvenation product is a scam, not a genuine new youth potion.',question="In Kronk's New Groove, what does Yzma claim the bottled product she has Kronk sell to the seniors will do?",answers=['Restore their youth','Cure their hiccups','Improve their memory','Make them stronger'])
change(2201,'clarification distractors','Used parallel activities and identified the actual Junior Chipmunk rivalry.',question="In Kronk's New Groove, what competition strains Kronk's romance with Miss Birdwell?",answers=['Their Junior Chipmunk teams competing at camp','Their restaurants competing for customers','Their entries competing in a cooking contest','Their deliveries competing to arrive first'])
change(2202,'clarification','Narrowed to the documented playful sparring scene; removed uncorroborated bouncing/failed teaching detail.',question="In Bambi II, what does Bambi playfully practice with his father before Friend Owl introduces Mena?")
change(2203,'clarification distractors','Specified the interrupted moment and removed tickle as an overlapping description.',question="In Bambi II, what does the Great Prince do to Bambi's belly just before Friend Owl interrupts their play?",answers=['Blows a raspberry','Grooms his fur','Checks for thorns','Brushes off snow'])
change(2204,'clarification','Asked about the named delegation rather than all three characters who help guard the courtyard.',question="In Frozen Fever, whom does Elsa explicitly ask if she can leave in charge of the courtyard?")
change(2205,'distractors','Removed the live-action clue that excluded two animated distractors.',question="Frozen Fever premiered in theaters in 2015 alongside which Disney feature?",answers=['Cinderella','Tomorrowland','Into the Woods','Maleficent'])
change(2206,'clarification','Used the transcript spelling and focused on the named holiday bell.',question="In Olaf's Frozen Adventure, what do Kristoff and Sven bring to mark the start of Arendelle's holidays?",answers=['The Jule Bell','The town clock','A giant snowflake','The royal chandelier'])
change(2207,'clarification','Separated loading and return transport from door-to-door walking.',question="In Olaf's Frozen Adventure, what vehicle does Olaf load with collected traditions for the trip back to the castle?")
change(2208,'factual clarification','The glasses-wearing persona wins from the aggressive persona, not vice versa; removed the reversed identities.',question="In the Pixar short Geri's Game, what is the prize handed over at the end of the chess match?")
change(2210,'clarification difficulty','Removed sensational language and calibrated a prominent plot event to medium.',question="In the Pixar short Bao, what does the mother do to stop her dumpling son from leaving with his fiancée?",difficulty='medium')
change(2212,'clarification','Removed unsupported accidental-creation characterization and redundant opening-year clue.',question="In EPCOT's original Journey Into Imagination ride, which red-bearded character accompanies Figment?")
change(2213,'factual clarification','Corrected the pavilion opening year; 1983 belongs to the ride opening.',question="Which company sponsored EPCOT's Journey Into Imagination pavilion when it opened in 1982?")
change(2214,'clarification','Explicitly distinguished the ride from its pavilion.',question="In what year did the original Journey Into Imagination ride open at EPCOT?")
change(2215,'clarification','Bound the attraction song addition to the historical 2021 update.',question="Which Coco song was added to Magic Kingdom's Mickey's PhilharMagic in its 2021 update?")
change(2216,'clarification','Bound the brand to the documented 2012 design-center version rather than current sponsorship.',question="Which car brand was featured in EPCOT's Test Track redesign that opened in December 2012?")
change(2217,'clarification difficulty','Used approximate historical advertised speed and calibrated medium.',question="About what top speed did Disney advertise for EPCOT's original Test Track, which opened in 1999?",difficulty='medium')

if __name__=='__main__':
    path=ROOT/'questions/q-007.json'
    lines=path.read_text(encoding='utf-8').splitlines()
    for n,line in enumerate(lines):
        raw=line.strip().rstrip(',')
        if not raw.startswith('{'): continue
        q=json.loads(raw)
        if q['id'] in changes:
            q.update(changes[q['id']][2]); lines[n]=json.dumps(q,ensure_ascii=False)+(',' if line.rstrip().endswith(',') else '')
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write('audit/runs/next-shard-0033-changes.json',{str(i):{'types':t.split(),'reason':r} for i,(t,r,f) in changes.items()})
    print('Edited',len(changes),'questions; no out-of-scope question edits.')
