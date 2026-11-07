# Batch 3 audit working notes

Reviewer: Codex. Fixed scope: next-shard-0003-plan.json (50 IDs, 101–155 with gaps). Research started 2026-11-06 UTC. Work is not complete until the result report says complete-for-scope.

Read-only player reports were saved to artifacts/question-audit/batch-3-player-flags.json. Eleven reports returned, no pagination token. Question 138 has Kristen's report that multiple songs fit; do not resolve this production flag until a fix is published.

Confirmed concerns from initial source challenge:

- 114: both Disneyland Paris and Euro Disney name the same resort at different dates. D23 https://d23.com/a-to-z/disneyland-paris/ opening paragraph gives original name, opening April 12 1992, official name change October 1 1994. Specify the date and naming event.
- 123: wording conflates competitive, honorary and lifetime totals. Disney+ https://www.disneyplus.com/en-nz/explore/articles/oscars-academy-awards-guide-2026 distinguishes 22 competitive and four honorary. Academy's 1969 ceremony lists Walt as producer of the winning Winnie the Pooh and the Blustery Day, after his 1966 death. Family Museum https://www.waltdisney.org/blog/walt-disneys-oscarsr uses a different expanded total including technical awards; that page must not be used to substantiate 22 lifetime awards.
- 138: multiple listed songs fit the Disney Dream. https://www.laughingplace.com/w/news/2011/01/21/hear-all-six-songs-from-the-disney-dream-horn/ lists When You Wish Upon a Star, A Dream Is a Wish Your Heart Makes and Be Our Guest. Official Disney Parks video https://www.youtube.com/watch?v=JJ0CEN-hoj0 demonstrates the horn repertoire, but its description alone does not verify individual melodies. Original blog URL failed to load. Further primary evidence is needed for revised wording.
- 109: opening day conflates July 17 invitation-only ceremony with July 18 public opening, and adult versus child admission. D23 https://d23.com/e-ticket-memories-five-favorite-facts-about-ticket-books/ section 1 distinguishes $1 entry from $2.50 adult coupon books introduced in October.
- 122: broad 'successful character before Mickey' admits earlier Disney characters; pin the rabbit and 1927–1928 series. D23 https://d23.com/a-to-z/oswald-the-lucky-rabbit/ opening paragraph.
- 129: asks a type but gives proper names; ask the railroad's name. D23 https://d23.com/a-to-z/carolwood-pacific-railroad/ opening paragraph.
- 130: first-studio wording is imprecise, and Alice's Wonderland was also made in Kansas City. D23 Laugh-O-gram Films and Alice Comedies entries distinguish the 1922 fairy-tale shorts from the pilot and later Hollywood series.
- 134: two distractors refer to the Art Institute; replace one. D23 About Walt Disney says Academy of Fine Arts in Chicago, not the Art Institute.
- 135: unsupported 'last major production' assertion conflicts with subsequent Jungle Book involvement. Remove that assertion; Mary Poppins has sufficient identifying context without it. D23 Mary Poppins film entry establishes 1964, Julie Andrews, and live action/animation.
- 144,149: 'launch' can mean float-out rather than maiden voyage. D23 Disney Dream and Disney Fantasy entries provide maiden-voyage dates (2011 and 2012).
- 147: Lookout Cay is a destination on Eleuthera, not a separate private island; verify and correct the premise.
- 150: 'different restaurant each night' is overbroad on longer cruises; clarify assigned rotation and dinner service or preserve the better existing servers question 420.

## Completion

Closed complete-for-scope in next-shard-0003-result.json: 50 reviewed, 35 current four-option evidence records and approvals, 19 retained edits, 15 preserved duplicate retirements, zero unresolved scoped questions. Final schema-2 reviews are in next-shard-0003-reviews/, with separate premise evidence, per-option exclusions and a final challenge. Research notes above describe starting concerns; the final review files and snapshots describe their resolutions.

Change types overlap: factual 3 (123, 135, 147), clarification 19, distractors 3, difficulty 6; explanation/category/scope/metadata zero. A wording edit does not mean the original answer was factually wrong.

The horn question now explicitly concerns the original Magic-class ships. Independent specialist accounts from TouringPlans and historian Jim Korkis support the one-tune distinction from later ships, with the unavailable original official blog documented as a source limitation. Recheck is scheduled for 2027-02-04. The production player flag remains open, since this local content has not been published.

Lookout Cay now asks its June 7, 2024 first-preview date, documented by the dated official announcement, instead of repeating destination-name question 1512 or describing Eleuthera as a separate private island. Oceaneer Club now tests the ship-specific Marvel Super Hero Academy association, rather than repeating generic club-name question 1396. The current official youth-activity directory uses ages 3–10; related out-of-scope question 1396 still uses 3–12 and should be checked when its own scope is reached. No approval of that related question is implied.

Lyrics were checked against licensed MTI sheets/scores and independent film transcriptions; uninspected official videos are not asserted as inspected film evidence. DisneyFiles Winter 2009, PDF page 29, independently corroborates the New Orleans Square dedication year and mayor context.

Final structural validation: 2,008 active questions, zero structural errors. Coverage: q-001 121/216 approved; whole bank 121/2,008 approved, 1,887 remaining. Next request resumes batch 4 in q-001, 50 questions. No new plan was selected.

Final release gate remains blocked by the pre-existing question 683 review and manual concern. Batch 3 has no gate errors. No commit, push, deployment or production player-data mutation was performed.
