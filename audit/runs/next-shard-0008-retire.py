"""Preserve Codex's full duplicate comparisons via the supported retire command."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PAIRS={
 373:(2631,'peoplemover-identity','The retained propulsion question explicitly names the Magic Kingdom PeopleMover and adds its motor fact. This repeats the simple elevated-transit identity.',
      ['The official title is Tomorrowland Transit Authority PeopleMover.','WEDway Express is not the title.','Future Commuter is not the title.','Tomorrowland Monorail is not the elevated tram\'s title.']),
 377:(2249,'tron-2023','2249 explicitly supplies the Magic Kingdom 2023 opening in its stem while asking the additional Shanghai origin. Retain that additional historical context.',
      ['2023 matches the April opening announcement.','2021 does not match.','2022 does not match.','2024 does not match.']),
 378:(1172,'matterhorn','Both identify the same Disneyland Matterhorn coaster. 378 repeats the answer\'s mountain name and uses invented alternatives; retain the less obvious mountain-coaster question.',
      ['Matterhorn Bobsleds is the documented mountain ride.','Alpine Coaster is not its name.','Yeti Run is not its name.','Snowpeak Express is not its name.']),
 379:(1177,'disney-company-origin laughogram','1177 already names Disney Brothers Cartoon Studio and asks its founding year. Retire the name-only question, whose first-studio premise also conflicts with earlier Kansas City work.',
      ['Disney Brothers Cartoon Studio is the brothers\' 1923 company, but not Walt\'s first studio overall.','Walt Disney Productions is a later company name, not the original 1923 name.','Laugh-O-gram predates the California company, exposing the first-studio ambiguity; the with-Roy qualifier does not make first-studio generally true.','Mickey Mouse Studios is not the original company name.']),
 382:(131,'disney-family','131 gives the more precise Los Angeles/Hollywood location of Walt\'s first California studio. The same move supplies California; no separate state fact is gained.',
      ['California is the destination of the Hollywood move.','New York is not that destination state.','Florida is not that destination state.','Texas is not that destination state.']),
 385:(1372,'disney-family','Both ask Walt\'s wife\'s given name; adding Disney to each answer changes no fact. Retain 1372\'s marriage context.',
      ['Lillian Bounds Disney was Walt\'s wife.','Edna is not his wife\'s name.','Mary is not his wife\'s name.','Rose is not his wife\'s name.']),
 386:(127,'disney-family','127 explicitly says two daughters and asks their names, Diane and Sharon. This count-only question supplies no additional fact.',
      ['Two is the count given with Diane and Sharon.','One omits a daughter.','Three exceeds the stated count.','None contradicts the two named daughters.']),
 388:(1490,'disney-family roy-death','1490 explicitly names Roy O. as Walt\'s older brother and successor in overseeing the Florida resort. This repeats the brother/business-partner identity.',
      ['Roy O. was the brother who partnered with Walt.','Ward Disney is not that partner.','Ray Disney is not that partner; another relative does not identify the cofounder.','Robert Disney is not the brother/cofounder identified here.']),
 390:(946,'true-life','946 explicitly names the True-Life Adventure series while asking its first feature. Keep that additional theatrical-film fact rather than repeating the series name.',
      ['True-Life Adventures is the documented nature-film series.','Nature\'s Wonders is not its name.','Disney Nature Shorts is not its name.','Wild Kingdom is not this Disney series.']),
 391:(1379,'medal-president','Inverse of the same 1964 Johnson/Disney Medal of Freedom event. The retained stem gives Johnson and the year while asking the honor, directly disclosing 391\'s answer.',
      ['Lyndon B. Johnson is the president in the ceremony transcript.','Kennedy did not present this 1964 ceremony.','Eisenhower did not present it.','Nixon did not present it.']),
 395:(960,'nine-old-men','Both identify the same honorary group of animators. Retain 960\'s concrete member names instead of the vague top-creative-team description.',
      ['Nine Old Men is the documented group name.','Walt\'s Boys is not the documented name.','The Ink Squad is not the documented name.','The Originals is not the documented name.']),
 399:(1495,'multiplane','1495 names the multiplane camera and asks the depth effect, the same fact in reverse. Retire 399 also because parallax can describe the effect, making that alternative weakly distinguished.',
      ['Multiplane camera is the documented layered-artwork apparatus.','A zoom changes scale but does not identify the documented apparatus.','Parallax describes the depth phenomenon and is not safely excluded by this broad original wording; no single-answer approval is claimed.','Stereoscopy is distinct from layered photography, but the broad depth wording is less precise than 1495.']),
 400:(690,'disney-family','Inverse of 690\'s Burbank/since-1940 association; 959 also explicitly supplies Burbank and 1940. Retain those counterparts without adding a third question on the same move.',
      ['1940 is the documented completed Burbank studio year.','1935 is not that documented completion year.','1945 is not that documented completion year.','1950 is not that documented completion year.']),
 401:(1191,'wed-initials','1191 asks WED Enterprises\' later name and supplies the same Walt Disney Imagineering identity. Retire 401, whose unbounded wording also allows WED Enterprises historically.',
      ['Walt Disney Imagineering is the later name of the design organization.','WED Enterprises is its genuine former name and historically participated in park design, so the unbounded original is not cleanly exclusive.','Disney Creative Group is not the documented name.','Disney Theme Park Design is not the documented name.']),
 403:(677,'laughogram','677 explicitly identifies Laugh-O-Gram as Walt\'s Kansas City company before Hollywood. It directly supplies this city answer; 1492 repeats that association too.',
      ['Kansas City, Missouri is the company\'s stated location.','Chicago is not its stated location.','Los Angeles is not the Kansas City company\'s location.','New York is not its stated location.']),
 411:(136,'cruise-originals fleet-2025-table','This pair aggregates the same original-ship identities as 136 (first ship Magic) and 961 (Wonder, the 1999 sister). Retain those more specific historical questions; 136 is the primary replacement pointer.',
      ['Magic and Wonder were the first pair, in 1998 and 1999.','Dream and Fantasy followed in 2011 and 2012.','Wish and Treasure entered service much later, in 2022 and 2024.','Magic fits but Dream does not belong to the 1990s pair.']),
 417:(2274,'cruise-theatre','2274 explicitly names Walt Disney Theatre as the Disney Wonder stage venue and asks the additional musical/ship fact. The simple theatre name is already supplied.',
      ['Walt Disney Theatre is the official live-show venue name.','Disney Broadway is not the venue title.','Magic Kingdom Stage is not the venue title.','Stateroom Stage is not the venue title.']),
 419:(434,'pirate-night','434 explicitly supplies Pirate Night as the fireworks occasion while asking the fireworks-show name. Retain that additional show fact rather than the broad event identity.',
      ['Pirate Night is the named costume/deck-party occasion.','Princess Night is not that official event title.','Superhero Night is not that official pirate-themed event title.','Adventure Night is not that official event title.']),
 421:(750,'water-coasters','750 asks the outdoor-movie experience and explicitly gives the Funnel Vision screen in its answer. This repeats that same screen identity.',
      ['Funnel Vision is the documented screen name.','Deck Cinema is not the documented screen name.','Big Screen at Sea is not the documented screen name.','Movie Deck is not the documented screen name.']),
 422:(729,'fleet-2025-table','Inverse of Wish/2022 identity in 729. Both test the ship and debut year; keep one question, preserving the other snapshot.',
      ['2022 is Wish\'s maiden-voyage year.','2020 is not the stated year.','2019 is not the stated year.','2023 is not the stated year.']),
}
bank={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
sources=json.loads((ROOT/'audit/source-notes.json').read_text(encoding='utf-8'))['sources']
out=ROOT/'audit/runs/next-shard-0008-retirements'
out.mkdir(exist_ok=True)
for old,(new,refs,reason,assessments) in PAIRS.items():
    additional=[bank[i] for i in ({400:[959],403:[1492],411:[961]}.get(old,[]))]
    ref=out/f'{old}-{new}.json'
    value=dict(reviewer='Codex',at='2026-11-07',retired=bank[old],retained=bank[new],
        additionalComparisons=additional,rationale=reason,
        sources=[dict(sourceNoteId=s,**sources[s]) for s in refs.split()],
        originalOptionAssessments=[dict(answer=a,assessment=r) for a,r in zip(bank[old]['answers'],assessments)],
        finalChallenge=dict(reviewer='Codex',at='2026-11-07',notes=reason+' All four original options inspected. Retirement avoids asserting approval of a flawed premise or an insufficiently excluded alternative.'),
        scope='Only the planned ID is retired. Counterpart comparison is not approval of its other claims.')
    ref.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=subprocess.run([sys.executable,'scripts/question_audit.py','retire',str(old),'--replaced-by',str(new),'--reviewer','Codex','--reason',reason,'--reference',str(ref.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if result.returncode: raise SystemExit(result.stdout+result.stderr)
    print(f'Retired {old}; retained {new}',flush=True)
