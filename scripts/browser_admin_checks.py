"""Admin flag UI checks with an in-browser Firestore stand-in; no live traffic."""

FIREBASE_STUB = r"""
(() => {
  const data=new Map([
    ['flags/report',{questionId:1,questionText:'Which option is correct?',correctAnswer:'A',difficulty:'easy',category:'movies',reportedBy:'Tester',timestamp:'2026-11-01T12:00:00Z',comment:'Check the options.'}],
    ['flags/legacy',{questionId:2,questionText:'Legacy report',correctAnswer:'B',difficulty:'medium',category:'movies',_resolved:true}]
  ]);
  let serial=0;
  const doc=path=>({id:path.split('/').pop(),collection:name=>collection(path+'/'+name),
    get:async()=>({exists:data.has(path),data:()=>data.get(path)}),
    set:value=>data.set(path,value),update:value=>data.set(path,{...data.get(path),...value})});
  const collection=path=>({doc:id=>doc(path+'/'+(id||'event-'+(++serial))),get:async()=>({docs:[...data]
    .filter(([key])=>key.startsWith(path+'/')&&key.split('/').length===path.split('/').length+1)
    .map(([key,value])=>({id:key.split('/').pop(),data:()=>value}))})});
  const db={collection,runTransaction:async fn=>fn({get:ref=>ref.get(),set:(ref,v)=>ref.set(v),update:(ref,v)=>ref.update(v)})};
  window.firebase={initializeApp(){},firestore:()=>db};
  window.testFlagData=data;
})();
"""


def run_admin_checks(browser, base, check):
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900}, service_workers='block')
    traffic, errors = [], []
    ctx.route('**/firestore.googleapis.com/**', lambda r: (traffic.append(r.request.url), r.abort()))
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(
        status=200, content_type='application/javascript',
        body=FIREBASE_STUB if 'firebase-app-compat.js' in r.request.url else ''))
    page = ctx.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base.replace('/index.html', '/review.html'))
    page.wait_for_selector('#output tbody tr')
    row = page.locator('#output tbody tr').filter(has_text='Which option is correct?')
    check.ok('Legacy resolution' in page.inner_text('#output'), 'legacy flags disclose absent resolution evidence')
    check.ok(row.locator('.q-text').bounding_box()['width'] >= 250, 'question text retains readable width in the review table')
    row.get_by_role('button', name='Resolve', exact=False).click()
    page.fill('#flag-reviewer', 'Milo')
    page.fill('#flag-reason', 'Corrected the attribution after checking all options.')
    page.click('#flag-save')
    page.wait_for_function("document.getElementById('flag-status').textContent.includes('Decision failed')")
    check.ok(page.evaluate("testFlagData.get('flags/report')._resolved !== true"), 'missing fix link leaves report unresolved')
    page.fill('#flag-reference', 'https://github.com/Milo9/dsny-trivia/commit/abc')
    page.click('#flag-save')
    page.wait_for_function("document.getElementById('flag-resolution-form').hidden")
    page.wait_for_function("document.getElementById('output').textContent.includes('Corrected the attribution')")
    check.ok(row.get_by_role('link', name='Change / evidence').count() == 1, 'saved flag resolution displays evidence link')
    row.get_by_role('button', name='Reopen', exact=True).click()
    page.fill('#flag-reason', 'Another option needs checking.')
    page.click('#flag-save')
    page.wait_for_function("document.getElementById('flag-resolution-form').hidden")
    page.wait_for_function("document.getElementById('output').textContent.includes('Another option needs checking.')")
    check.ok(page.evaluate("[...testFlagData.keys()].filter(k=>k.startsWith('flags/report/resolutions/')).length===2"), 'reopening retains previous resolution event')
    page.get_by_role('button', name='Export JSON', exact=False).click()
    check.ok('Corrected the attribution' in page.inner_text('#json-out'), 'flag export includes resolution history')
    page.screenshot(path=str(check.out / 'admin-flag-history.png'), full_page=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    row.get_by_role('button', name='Resolve', exact=False).click()
    page.locator('#flag-resolution-form').scroll_into_view_if_needed()
    page.screenshot(path=str(check.out / 'admin-resolution-mobile.png'))
    check.ok(not traffic and not errors, 'admin checks produce no live Firestore traffic or page errors')
    ctx.close()
