"""Batch 35 content corrections after source and four-option review."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'questions/q-008.json'
changes={}
def change(i,types,reason,**fields): changes[i]=(types,reason,fields)
change(2268,['clarification'],'Distinguish the 1933 brand from its later corporate successor Timex.',question='Under which watch brand was the original Mickey Mouse wristwatch released in 1933?')
change(2270,['clarification'],'Identify the Disney Store chain; Disney already operated an Orlando airport shop.',question='In which city did the first location of the Disney Store retail chain open in 1987?')
change(2272,['clarification','difficulty'],'Avoid implying the Magic hosted the initial premiere; Wonder received it first in 2003.',question='Which Disney Cruise Line stage show presents Disney characters in a Hollywood-style awards ceremony?',difficulty='medium')
change(2273,['distractors'],'Use parallel plausible names rather than three familiar characters from other films.',answers=['Franco DiFortunato','Lorenzo Bellafiore','Vittorio Malaspina','Carlo Bonaventura'])
change(2275,['clarification'],'Ask the fixed plot fact without an unnecessary current ship assignment.',question="In Disney Cruise Line's stage show Disney's Believe, what is the name of Dr. Greenaway's daughter?")
change(2276,['clarification'],'Replace an unbounded exclusive-current-show claim with the documented 2017 debut.',question='Which Disney Cruise Line ship debuted a new Beauty and the Beast stage production in November 2017?')
change(2277,['clarification'],'Date the changeable ship assignment.',question="As of November 2026, Disney's Aladdin - A Musical Spectacular is listed for Disney Wish and which other ship?")
change(2278,['clarification'],'Distinguish the parent company from its Dream Cruises brand.',question='The ship later renamed Disney Adventure was originally built as Global Dream for the Dream Cruises brand of which parent company?')
change(2279,['clarification'],'Remove the uncertain pants-specific origin story; sources disagree about the garment.',question="What nickname is given to the dark blue hull color of Disney Cruise Line's original ships?")
change(2281,['clarification'],'Avoid a broad career-start claim; retain the documented former ship-performer relationship.',question='Which singer, a former performer aboard Disney Wonder, became godmother of Disney Dream at its 2011 christening?')
change(2282,['clarification'],'Remove the inaccurate suggestion that every earlier godmother was a celebrity.',question="Which group was honored as Disney Wish's godchildren at its 2022 christening?")
change(2283,['clarification'],'Focus on the Toy Story credit rather than supplying other answers as extra clues.',question="Who composed the score and recorded 'You've Got a Friend in Me' for the original Toy Story (1995)?")
change(2285,['clarification'],'Remove the release-year clue that uniquely identifies the film among the options.',question="For which Pixar film did Randy Newman win his first competitive Academy Award, for 'If I Didn't Have You'?")
change(2286,['clarification'],'Remove the release-year clue; ask the song-film relationship.',question="Randy Newman won his second Best Original Song Oscar for 'We Belong Together,' from which Pixar film?")
change(2287,['clarification'],'Remove the title translation giveaway and specify the Land of the Dead contest.',question='In Coco (2017), which song do Miguel and Héctor perform together at the Land of the Dead talent contest?')
change(2288,['clarification'],'Distinguish the music credit from Molina\'s lyrics.',question="Who composed the music for Coco's 'Un Poco Loco', with lyrics by Adrian Molina?")
change(2290,['clarification'],'Remove songwriter names that unnecessarily supply the neighboring question\'s answer.',question="In Turning Red (2022), which 4*Town song joins with the family's ritual chant during the climactic stadium scene?")
change(2291,['clarification','distractors'],'Remove sibling clue, since none of the original alternative duos are siblings; use comparable songwriter teams.',question="Who wrote the three original songs performed by 4*Town in Turning Red (2022)?",answers=["Billie Eilish and Finneas O'Connell",'Kristen Anderson-Lopez and Robert Lopez','Benj Pasek and Justin Paul','Elton John and Tim Rice'])
change(2292,['clarification'],'Remove distracting Pitch Perfect franchise attribution; focus on the two Frozen score credits.',question='Who composed the orchestral scores for Frozen (2013) and Frozen II (2019)?')
change(2295,['clarification','distractors'],'The original stem spells out the answer EGOT; ask the dated award achievement instead.',question='Which Disney composer completed a competitive EGOT in July 2020?',answers=['Alan Menken','Randy Newman','Christophe Beck','Michael Giacchino'])
change(2296,['clarification'],'Specify the animated film version.',question="In Tarzan (1999), what is the name of the gorilla troop leader and Kala's mate?")
change(2299,['clarification','distractors'],'Name the actual injury mechanism and use plausible parallel alternatives.',question='In Finding Nemo (2003), what caused Gill\'s scars and damaged fin during his first escape attempt?',answers=['Landing on dental tools','Being bitten by a shark','Getting tangled in a net','Scraping against a coral reef'])
change(2300,['clarification'],'Specify the original English-language voice cast.',question='Who voices Gill in the original English-language Finding Nemo (2003)?')
change(2301,['clarification','distractors','difficulty'],'Use a role supported by retainer/adviser evidence and parallel household roles; specify animation.',question="In the animated The Little Mermaid (1989), what is Grimsby's role in Prince Eric's household?",answers=['Personal attendant and adviser','Captain of the royal guard','Head cook of the palace','Court composer and musician'],difficulty='medium')
change(2303,['clarification'],'Focus the name reference; omit an unnecessary voice-credit premise.',question="Duke Weaselton's name in Zootopia (2016) echoes which character's name from Frozen (2013)?")
change(2305,['clarification','distractors'],'Use Pixar\'s Formula Racer description without inventing an official plural series name or claiming reigning status.',question='In Cars 2 (2011), Francesco Bernoulli is a champion in which type of racing?',answers=['Formula racing','Stock-car racing','Rally racing','Drag racing'])
change(2306,['clarification'],'Specify the doll type to distinguish other enforcers.',question="In Toy Story 3 (2010), which large baby doll acts as Lotso's enforcer at Sunnyside?",answers=['Big Baby','Chunk','Stretch','Chuckles'])
change(2307,['clarification','distractors'],'The pendant is discarded in the flashback; ask the child\'s name instead of treating it as continuously worn.',question="In Toy Story 3 (2010), whose name appears on Big Baby's old heart-shaped pendant?",answers=['Daisy','Molly','Bonnie','Emily'])
change(2308,['factual','clarification','distractors','difficulty'],'The script reveals Kenneth, not Kenneth Sean Carson; ask only the film-backed longer first name.',question='In Toy Story 3 (2010), what longer first name does Lotso use when addressing Ken?',answers=['Kenneth','Kendall','Kenton','Kendrick'],difficulty='medium')
change(2309,['clarification','distractors'],'The wardrobe and disco are explicitly features of the same house, so remove overlapping alternatives.',question="In Toy Story 3 (2010), what does Ken introduce to Barbie before saying he has everything except someone to share it with?",answers=['His Dream House','His private yacht','His model train set','His rooftop greenhouse'])
change(2312,['clarification'],'Specify Disney\'s 1996 animated version rather than the novel or musical.',question='In the animated The Hunchback of Notre Dame (1996), what official position does Claude Frollo hold in Paris?')
change(2313,['clarification'],'Shorten to the source-established character-song relationship; avoid a fire/title clue.',question="In The Hunchback of Notre Dame (1996), which song expresses Frollo's conflicted desire for Esmeralda?")
rows=[]
saved={}
for line in p.read_text(encoding='utf-8').splitlines():
    if line.startswith('{'):
        q=json.loads(line.rstrip(',')); i=q['id']
        if i in changes:
            before=q.copy(); types,reason,fields=changes[i]; q.update(fields)
            saved[str(i)]=dict(types=types,reason=reason,before=before,after=q)
            line=json.dumps(q,ensure_ascii=False)+(',' if line.endswith(',') else '')
    rows.append(line)
p.write_text('\n'.join(rows)+'\n',encoding='utf-8')
(ROOT/'audit/runs/next-shard-0035-changes.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Edited',len(saved),'retained questions.')
