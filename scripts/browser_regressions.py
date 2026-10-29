"""Adversarial UI checks on the same isolated LocalStorageAdapter test site."""
def run_regressions(browser, base, check, stop_origin):
    ctx = browser.new_context(viewport={"width": 375, "height": 667}, service_workers="block")
    ctx.route("**/firestore.googleapis.com/**", lambda r: r.abort())
    ctx.route("https://www.gstatic.com/firebasejs/**", lambda r: r.fulfill(status=200, body=""))
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))

    page.set_default_timeout(10000)

    def boot():
        page.goto(base)
        page.wait_for_selector('.user-card')

    def select(name="Kristen"):
        page.locator('.user-card', has_text=name).click()
        page.wait_for_selector('#screen-settings:not(.hidden)')

    def play(n):
        for _ in range(n):
            page.locator('.answer-btn').first.click()
            page.click('#btn-next')

    def answered():
        return page.evaluate("storage._load().users.kristen.totalAnswered")

    print("Audit regression checks")
    boot()
    page.locator('.user-card').first.focus()
    page.keyboard.press('Enter')
    check.ok(page.is_visible('#screen-settings'), 'keyboard activates a player')
    checkbox = page.locator('#category-grid input').first
    checkbox.focus()
    page.keyboard.press('Space')
    check.ok(not checkbox.is_checked(), 'keyboard toggles category checkbox')
    page.click('#difficulty-group [data-value="hard"]')
    page.click('#count-group [data-value="20"]')
    page.reload()
    page.wait_for_selector('.user-card')
    select()
    check.ok(page.get_attribute('#difficulty-group [data-value="hard"]', 'aria-pressed') == 'true'
             and page.get_attribute('#count-group [data-value="20"]', 'aria-pressed') == 'true'
             and not page.locator('#category-grid input').first.is_checked(), 'settings persist and expose selected state')
    page.click('#difficulty-group [data-value="all"]')
    page.click('#count-group [data-value="10"]')
    checkbox.focus()
    page.keyboard.press('Space')

    page.evaluate("""() => {
      const real=storage.updateStats.bind(storage);let first=true;
      storage.updateStats=async(...args)=>{const result=await real(...args);if(first){first=false;throw Error('Lost response');}return result;};
    }""")
    page.click('#btn-start-game')
    play(10)
    page.wait_for_selector('#btn-retry-save:not(.hidden)')
    before = answered()
    page.click('#btn-retry-save')
    page.wait_for_function("document.getElementById('save-status').textContent.includes('Already saved')")
    check.ok(answered() == before == 10, 'lost response followed by Retry counts a game once')

    # Restore the real adapter by reloading. Block only incidental local writes,
    # leaving the test adapter's database available as a stand-in for Firestore.
    page.add_init_script("""(() => {
      const original=Storage.prototype.setItem;
      Storage.prototype.setItem=function(k,v){if(k.startsWith('disney_seen_'))throw Error('Quota exceeded');return original.call(this,k,v);};
    })();""")
    boot()
    select()
    page.click('#btn-start-game')
    play(10)
    page.wait_for_function("document.getElementById('save-status').textContent==='Saved ✓'")
    check.ok(not page.is_visible('#save-warning') and answered() == 20, 'local bookkeeping failure does not report a failed server save')

    page.click('#btn-play-again')
    page.evaluate("() => {storage._realDaily=storage.getDailyQuestions; storage.getDailyQuestions=()=>new Promise(r=>window.resolveDaily=r);}")
    page.click('#btn-daily-challenge')
    page.wait_for_function('typeof window.resolveDaily === "function"')
    page.click('#btn-settings-back')
    page.wait_for_selector('#screen-home:not(.hidden)')
    page.evaluate('window.resolveDaily(QUESTIONS.slice(0,10))')
    page.wait_for_timeout(150)
    check.ok(page.is_visible('#screen-home'), 'late daily load does not reopen a game after Back')

    page.evaluate("storage.getLeaderboard=key=>new Promise(r=>setTimeout(()=>r([{id:key,name:key===prevMonthKey()?'LATEST':'STALE',totalPoints:0,effectivePeriodPoints:7}]),key===prevMonthKey()?10:250));renderLeaderboard('month');renderLeaderboard('lastmonth')")
    page.wait_for_timeout(350)
    check.ok('LATEST' in page.inner_text('#leaderboard-list') and 'STALE' not in page.inner_text('#leaderboard-list'), 'late leaderboard response cannot replace the selected period')
    boot()
    select()
    page.click('#btn-start-game')
    page.locator('.answer-btn').first.click()
    page.click('#btn-flag')
    page.evaluate('() => {storage.flagReport=()=>new Promise(r=>window.resolveFlag=r);}')
    page.click('#btn-flag-submit')
    page.click('#btn-next')
    page.evaluate('window.resolveFlag()')
    page.wait_for_timeout(100)
    check.ok(not page.is_disabled('#btn-flag') and not page.is_visible('#flag-thanks'), 'late report completion does not mark the next question reported')

    page.evaluate("clearGameCheckpoint('kristen')")

    # A failed daily remains available after rollover and credits its own month.
    boot()
    page.evaluate("todayKey=()=> '2026-10-31'")
    select('Cara')
    page.click('#btn-daily-challenge')
    page.wait_for_selector('.answer-btn')
    page.evaluate("() => {storage._realSave=storage.updateStats;storage.updateStats=()=>Promise.reject(Error('offline'));}")
    play(10)
    page.wait_for_selector('#btn-retry-save:not(.hidden)')
    page.evaluate("() => {todayKey=()=> '2026-11-01';storage.updateStats=storage._realSave;}")
    page.click('#btn-play-again')
    check.ok(page.is_visible('#btn-pending-daily'), 'unsaved daily remains visible after date rollover')
    page.click('#btn-pending-daily')
    page.wait_for_function("document.getElementById('save-status').textContent==='Saved ✓'")
    check.ok(page.evaluate("storage._load().users.cara.lastDailyDate") == '2026-10-31'
             and page.evaluate("storage._load().users.cara.monthlyKey") == '2026-10', 'past daily saves under its challenge date and month')
    page.click('#btn-play-again')
    check.ok('Review' not in page.inner_text('#btn-daily-challenge'), 'saving yesterday does not block the new daily')

    # Homework failures retain the confirmed state; successful watches are explicit.
    boot()
    page.wait_for_selector('#homework-card:not(.hidden)')
    old = page.evaluate('JSON.stringify(homeworkState)')
    page.evaluate("() => {storage._realHomework=storage.updateHomework;storage.updateHomework=()=>Promise.reject(Error('offline'));}")
    page.click('#btn-mark-watched')
    page.wait_for_selector('#confirm-overlay:not(.hidden)')
    check.ok(page.evaluate('JSON.stringify(homeworkState)') == old, 'failed homework write retains confirmed state')
    page.click('#confirm-ok')
    page.evaluate('() => {storage.updateHomework=storage._realHomework;}')
    page.click('#btn-mark-watched')
    page.wait_for_function("document.getElementById('btn-mark-watched').textContent.includes('Watched')")
    check.ok(page.evaluate('homeworkState.watched.some(w=>w.id===homeworkState.movieId)'), 'watching a movie is explicitly confirmed and saved')
    page.evaluate("() => {const d=storage._load();d.weeklyHomework.watched=[];storage._save(d);refreshDayState();}")
    page.wait_for_function('homeworkState.watched.length===0')
    check.ok(not page.is_disabled('#btn-mark-watched'), 'foreground refresh picks up same-week homework changes from another device')

    select()
    # Explicitly seed one missed item, then ensure practice never reaches score writes.
    page.evaluate("() => {currentUser.missedQuestionIds=[QUESTIONS[0].id];renderSettings();storage.updateStats=()=>{throw Error('Practice attempted a score write');};}")
    before = answered()
    page.click('#btn-practice-missed')
    play(1)
    page.wait_for_selector('#screen-results:not(.hidden)')
    check.ok(answered() == before and 'Practice complete' in page.inner_text('#save-status'), 'missed-question practice does not change competitive scores')
    page.click('#btn-results-home')
    page.wait_for_selector('.user-card')
    page.click('#btn-offline-practice')
    page.evaluate('QUESTIONS=QUESTIONS.filter(q=>q.id===21)')
    page.click('#btn-start-game')
    page.locator('.answer-btn').first.click()
    check.ok(page.is_visible('#answer-explanation') and page.locator('#answer-explanation a').get_attribute('href').startswith('https://'), 'answer explanation includes a safe source link')
    page.click('#btn-next')
    check.ok('Practice complete' in page.inner_text('#save-status'), 'offline practice is clearly labeled and never submits scores')
    check.ok(not errors, 'no uncaught errors during adversarial UI checks: '+str(errors))
    page.wait_for_timeout(450)
    page.screenshot(path=str(check.out / '17-audit-regressions.png'))
    ctx.close()

    # Exercise the real adapter's startup failure, without giving it a Firebase
    # SDK or permitting any request to the production database.
    fallback = browser.new_context(service_workers='block')
    fallback.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, body=''))
    hits = []
    def block_database(route):
        hits.append(route.request.url)
        route.abort()
    fallback.route('**/firestore.googleapis.com/**', block_database)
    def use_real_adapter(route):
        response = route.fetch()
        source = response.text().replace('const storage = new LocalStorageAdapter();', 'const storage = new FirebaseAdapter();')
        route.fulfill(response=response, body=source)
    fallback.route('**/storage.js*', use_real_adapter)
    page = fallback.new_page()
    page.goto(base)
    page.wait_for_selector('#user-list .load-error')
    page.click('#btn-offline-practice')
    page.click('#btn-start-game')
    page.wait_for_selector('.answer-btn')
    check.ok(page.is_visible('#practice-indicator') and not hits, 'blocked Firebase CDN leaves practice usable without database traffic')
    fallback.close()

    # The installed shell must genuinely reload without a network connection.
    offline = browser.new_context(viewport={"width": 375, "height": 667})
    offline.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, body=''))
    offline.route('**/firestore.googleapis.com/**', lambda r: r.abort())
    page = offline.new_page()
    page.goto(base)
    page.wait_for_selector('.user-card')
    page.wait_for_function('navigator.serviceWorker.controller !== null', timeout=20000)
    if browser.browser_type.name == 'webkit':
        # Playwright <=1.63 kills service-worker requests before the worker can
        # respond when set_offline(True) is used (upstream issue #42775).
        # Stop the isolated origin instead: this verifies real cache fallback,
        # without claiming to emulate the entire device's network being off.
        stop_origin()
    else:
        offline.set_offline(True)
    response = page.reload(wait_until='domcontentloaded')
    check.ok(response.from_service_worker, 'unavailable-origin reload is served by the installed service worker')
    page.wait_for_selector('#btn-offline-practice', timeout=20000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && QUESTIONS.length > 0')
    page.click('#btn-offline-practice')
    page.click('#btn-start-game')
    page.wait_for_selector('.answer-btn')
    check.ok(page.is_visible('#practice-indicator'), 'cached shell and questions support offline practice after reload')
    offline.close()
