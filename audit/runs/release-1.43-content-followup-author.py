"""Two release-blocker reviews, researched and challenged by Codex."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lib=read('audit/source-notes.json')
sources={
'release43-abc':('https://d23.com/a-to-z/american-broadcasting-company/','Opening 1954 agreement paragraph','ABC invested in Disneyland in 1954 under Walt\'s programming agreement. The named park is Disneyland.'),
'release43-deal':('https://d23.com/this-day/abc-and-disney-boards-approve-ownership-and-financing-deal-for-disneyland/','April 2, 1954 entry; investment paragraphs','The ownership and financing deal concerns construction of Disneyland.'),
'release43-laugh':('https://www.waltdisney.org/blog/how-walt-started-in-animation','Paragraph contrasting Newman shorts and Kaycee Studios in 1921 with spring 1922 incorporation','Walt incorporated Laugh-O-gram Films in spring 1922; 1921 refers to earlier work and the Kaycee venture.'),
'release43-studio':('https://www.thankyouwaltdisney.org/history/','Opening paragraphs; May 1922 timeline; Animation Pioneers paragraph','The studio preservation organization identifies Laugh-O-gram Films incorporation in May 1922, and Disney Brothers Studio as the later Hollywood venture.')}
for k,(url,loc,evidence) in sources.items():
    lib['sources'][k]=dict(url=url,locator=loc,evidence=evidence,checkedBy='Codex',checkedAt='2026-11-07',timeSensitive=False,nextReviewAt=None,topics=['walt'],limitations='Institutional or original-studio preservation organization text inspected. No film playback claimed; exact calendar day is not asserted.')
write('audit/source-notes.json',lib)
n=read('audit/runs/release-1.43-content-followup-template.json')
for r in n['reviews']:
    r.update(checks=['singleAnswer','context','wording','noGiveaway','distinctFact','category','difficulty','scope'],timeSensitive=False,nextReviewAt=None)
    if r['questionId']==1374:
        ss=['release43-abc','release43-deal']
        r['context']='Historical park construction agreement, not the title or content of a real television show.'
        r['notes']='Full Walt-category context and financing/ABC cross-bank search read. q381 asks Walt\'s lifetime park opening, q2353 presentation-map artist, q2354 financing-trip city: all different facts.'
        p='The 1954 agreement explicitly finances Disneyland construction.'
        reasons=['Disneyland is the park named in the agreement.','Magic Kingdom is not the park named in this 1954 ABC agreement.','EPCOT is not the park named in the agreement.','Disney California Adventure is not the named park.']
        c='Tried the identical Disneyland television title as a competing interpretation: final wording explicitly asks a theme park construction project and all four choices are parks. Removed the false color claim and all TV-series trivia. Knowing Walt saw Disneyland open does not establish its ABC financing.'
    else:
        ss=['release43-laugh','release43-studio']
        r['context']='Specific corporate incorporation in Kansas City in spring 1922; no first-studio superlative.'
        r['notes']='Full Walt-category context and Laugh-O-gram search read. q130 asks the fairy-tale short series, not company incorporation. q682/q1177 concern Hollywood founding; q959 concerns Burbank.'
        p='Both museum and studio-preservation organization place Laugh-O-gram incorporation in spring/May 1922.'
        reasons=['Laugh-O-Gram Films is the incorporated company.','Disney Brothers Studio is the later Hollywood venture, not this Kansas City company.','Kansas City Film Co. is not the identified incorporated company; the real Film Ad company was an employer, not this business.','Missouri Motion Pictures is not the company identified by either institutional history.']
        c='Challenged 1921: the earlier Newman shorts and Kaycee partnership are different from Laugh-O-gram Films incorporation. Independent May 1922 corroboration establishes the spring date. Avoided disputed exact-day variants and removed the unnecessary bankruptcy clause.'
    r['premise']=dict(reason=p,sources=ss)
    r['options']=[dict(basis='direct' if i==0 else 'exclusive-inference',reason=x,sources=ss) for i,x in enumerate(reasons)]
    r['challenge']=dict(reviewer='Codex',at='2026-11-07',premiseChecked=True,alternativesExcluded=True,notes=c)
n['sourcesChecked']=list(sources)
write('audit/runs/release-1.43-content-followup-evidence-notes.json',n)
