"""Record Codex's researched review of the existing q683 opening-date fix."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/'audit/runs/release-1.43-followup-review-683.json'
r=json.loads(path.read_text(encoding='utf-8'))
assert r['questionSnapshot']['question']=='On what date did Disneyland hold its televised, invitation-only opening ceremony?'
r['reviewer']='Codex'
r['manual']={key:True for key in r['manual']}
r['notes']=(
 'Reviewed final stem and all four dates, Walt-history category context, and cross-bank opening/dedication/1955 matches. '
 'This tests an exact historical ceremony date, not a real television-show plot. Hard exact-date recall; options all use the same format/year, with no date supplied by the stem. '
 'q109 asks admission price, q1380 dedication words, q2081 the Black Sunday nickname, q2082 riverboat overload, and q2083 a utility failure; those require different facts. '
 'Retired q96 is preserved duplicate context, not an active second opening-date question. '
 'The prior public-opening premise was wrong: final wording explicitly selects the invited ceremony, not public admission the following day. '
 'No new content edit in this follow-up; this renews evidence on the already-corrected final hash.'
)
sources=[
 {'url':'https://d23.com/a-to-z/disneyland/','locator':'Opening paragraph: July 17, 1955 invited audience; public admitted the following day. Third paragraph identifies elaborate live television opening special.'},
 {'url':'https://d23.com/a-to-z/dateline-disneyland-television/','locator':'Opening sentence dates Disneyland opening-day live ABC broadcast to Sunday July 17, 1955. Used as evidence of the park ceremony date, not TV-series trivia.'},
 {'url':'https://thewaltdisneycompany.com/press-releases/happy-50th-birthday-disneyland/','locator':'July 17, 2005 release: introductory Art Linkletter paragraph dates original telecast; paragraph beginning Thousands of Guests were already lined up explicitly dates invitation-only dedication to July 17, 1955.'},
]
v=r['verification']
v.update(context='Disneyland in Anaheim: televised invitation-only dedication/opening ceremony, distinguished from first general-public admission.',timeSensitive=False,nextReviewAt=None)
v['premise']={'reason':'Disney sources identify one invitation-only opening ceremony, televised on July 17, 1955; general-public opening followed on July 18.','sources':sources}
v['challenge']={
 'reviewer':'Codex','at':'2026-11-06','premiseChecked':True,'alternativesExcluded':True,
 'notes':'Separately challenged final wording against public July 18 admission, broadcast versus on-site attendance, Independence Day association, Florida October opening confusion, and Christmas. The archive explicitly distinguishes July 17 invited ceremony from public admission next day, and the corporate anniversary release independently corroborates July 17 invitation-only dedication. None of July 4, October 1 or December 25 is that one dated event. This does not claim no other ceremonies or broadcasts ever occurred. Reviewed full four-option historical-topic comparisons; no active question asks this same exact date.'
}
reasons=[
 'July 17, 1955 is explicitly the invitation-only dedication and live opening telecast date in the archive and corporate anniversary account.',
 'July 4 is thirteen days earlier than the uniquely dated July 17 ceremony; Independence Day is not the date specified by either account.',
 'October 1, 1955 is later than the uniquely dated July 17 ceremony. A different park opening on October 1 in another year cannot satisfy Disneyland Anaheim ceremony wording.',
 'December 25, 1955 is later than the uniquely dated July 17 ceremony. Holiday celebrations or broadcasts would not be this invitation-only opening event.',
]
for i,o in enumerate(v['options']):
    o.update(basis='direct' if i==0 else 'exclusive-inference',reason=reasons[i],sources=sources)
path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved final-hash review for question 683.')
