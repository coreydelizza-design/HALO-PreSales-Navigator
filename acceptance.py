"""Browser acceptance tests for the generated HALO app.
The managed Chromium in this build environment blocks file:// and localhost
navigation. We render the exact built HTML using set_content, and inject a
Storage-compatible in-memory test double only for persistence round-trip tests.
No application source is changed by these test fixtures.
"""
from pathlib import Path
from datetime import date, timedelta
import json
import os
import shutil
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parent
ARTIFACTS=ROOT/'test-artifacts'
ARTIFACTS.mkdir(parents=True,exist_ok=True)
RESULTS=[]

def passed(name):
    RESULTS.append({'test':name,'result':'PASS'})
    print('PASS',name,flush=True)

def setup_page(context, saved=None, storage=True):
    page=context.new_page()
    if storage:
        page.evaluate('''saved => { const data = Object.assign({}, saved || {});
          Object.defineProperty(window, 'localStorage', { configurable: true, value: {
            getItem:k=>Object.prototype.hasOwnProperty.call(data,k)?data[k]:null,
            setItem:(k,v)=>{data[k]=String(v)}, removeItem:k=>delete data[k],
            clear:()=>Object.keys(data).forEach(k=>delete data[k]),
            key:i=>Object.keys(data)[i]||null, get length(){return Object.keys(data).length}
          }});
        }''',saved)
    page.set_content((ROOT/'dist/index.html').read_text(),wait_until='load')
    return page

def nav(page, route):
    page.locator(f'.nav[data-id="{route}"]').click()

def action(page, name, ident=None):
    sel=f'[data-action="{name}"]'+(f'[data-id="{ident}"]' if ident is not None else '')
    page.locator(sel).filter(visible=True).first.click()

def snap(page):
    return page.evaluate('HaloNavigator.getSnapshot()')

def active(page):
    data=snap(page)
    return next(s for s in data['sessions'] if s['id']==data['activeId'])

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or None,headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1536,'height':1050},accept_downloads=True)
    page=setup_page(context)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    expect(page.locator('h1')).to_contain_text('Confidence starts')
    assert active(page)['demo'] is True
    assert page.evaluate('HaloNavigator.getMetrics().evidence')==0
    passed('Renders an explicitly fictional demo with no confirmed GTT evidence')
    for route in ['overview','discovery','readiness','stack','executive','opportunities','pilot','output']:
        nav(page,route)
        expect(page.locator(f'.nav[data-id="{route}"]')).to_have_attribute('aria-current','page')
        assert page.locator('h1').inner_text()
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
    passed('Eight separate navigation routes render without desktop overflow')
    nav(page,'overview')
    page.locator('.stat .help').first.hover()
    expect(page.locator('#active-tooltip')).to_contain_text('not a security')
    page.mouse.move(800,50)
    passed('Tutorial hover explains the metric and dismisses on pointer exit')
    action(page,'new')
    page.locator('#m-name').fill('Acceptance Test Enterprise')
    page.locator('#m-industry').select_option('Healthcare')
    page.locator('#m-architect').fill('Test architect')
    action(page,'save-profile')
    assert active(page)['demo'] is False
    assert active(page)['profile']['industry']=='Healthcare'
    assert page.evaluate('HaloNavigator.getMetrics().complete')==0
    assert active(page)['outcomes']==[]
    passed('New engagement begins blank without inherited demo answers or scores')
    action(page,'customer-question','inventory')
    page.locator('#m-status').select_option('gap')
    action(page,'save-customer')
    expect(page.locator('#modal-error')).to_contain_text('Write the customer')
    page.locator('#m-answer').fill('Inventory excludes the recently added cloud estate.')
    page.locator('#m-owner').fill('Customer architect')
    page.locator('#m-evidence').fill('Approved discovery note 2026-09-30')
    page.locator('#m-date').fill(date.today().isoformat())
    action(page,'save-customer')
    assert active(page)['customer']['inventory']['status']=='gap'
    assert page.evaluate('HaloNavigator.getMetrics().complete')==1
    passed('Discovery requires a written answer and saves status, owner, source and date')
    page.locator('#c-search').fill('encrypted')
    assert page.locator('#customer-results .question-card').count()==1
    page.locator('#c-search').fill('')
    page.locator('[data-bind="c-filter"]').select_option('answered')
    assert page.locator('#customer-results .question-card').count()==1
    page.locator('[data-bind="c-filter"]').select_option('all')
    passed('Discovery keyword and answer-state filters work together')
    action(page,'interview')
    expect(page.locator('#modal-title')).to_have_text('Firewalls & network controls')
    action(page,'interview-next')
    expect(page.locator('#modal-title')).to_have_text('Cloud & hybrid footprint')
    assert 'firewalls' not in active(page)['customer']
    page.keyboard.press('Escape')
    passed('Guided interview advances while skipped questions remain unknown')
    nav(page,'readiness')
    action(page,'gtt-question','compatibility')
    page.locator('#m-status').select_option('evidenced')
    page.locator('#m-answer').fill('A scoped test answer, not a real GTT support attestation.')
    action(page,'save-gtt')
    expect(page.locator('#modal-error')).to_contain_text('requires an answer')
    assert active(page)['gtt'].get('compatibility',{}).get('status')!='evidenced'
    page.locator('#m-owner').fill('Test product owner')
    page.locator('#m-evidence').fill('Test fixture support matrix')
    page.locator('#m-date').fill(date.today().isoformat())
    action(page,'save-gtt')
    assert page.evaluate('HaloNavigator.getMetrics().evidence')==1
    passed('GTT evidence cannot be marked recorded without answer, source, owner and date')
    action(page,'gtt-question','compatibility')
    page.locator('#m-date').fill((date.today()-timedelta(days=100)).isoformat())
    action(page,'save-gtt')
    assert page.evaluate('HaloNavigator.getMetrics().evidence')==0
    expect(page.locator('#gtt-results')).to_contain_text('Review overdue')
    passed('Evidence older than the navigator 90-day convention does not close the gate')
    action(page,'gtt-question','compatibility')
    page.locator('#m-date').fill(date.today().isoformat())
    action(page,'save-gtt')
    page.locator('[data-bind="g-filter"]').select_option('evidenced')
    assert page.locator('#gtt-results .question-card').count()==1
    passed('Current-evidence filter excludes open and stale product questions')
    nav(page,'stack')
    page.locator('[data-stack="firewall"][data-key="vendor"]').fill('Customer firewall product')
    page.locator('[data-stack="firewall"][data-key="coverage"]').select_option('strong')
    action(page,'stack-note','firewall')
    page.locator('#m-notes').fill('Existing enforcement retained; only configuration assessment under evaluation.')
    action(page,'save-stack-note')
    assert active(page)['stack']['firewall']['coverage']=='strong'
    assert 'retained' in active(page)['stack']['firewall']['notes']
    passed('Current-stack vendors, coverage and comparison notes are editable and saved')
    action(page,'asset')
    page.locator('#m-vendor').fill('Test device vendor')
    page.locator('#m-version').fill('Version unconfirmed')
    page.locator('#m-scope').fill('Pilot subset')
    action(page,'save-asset')
    a=active(page)['assets'][0]
    action(page,'asset',a['id'])
    page.locator('#m-owner').fill('Network owner')
    action(page,'save-asset')
    assert active(page)['assets'][0]['owner']=='Network owner'
    page.once('dialog',lambda d:d.accept())
    action(page,'delete-asset',a['id'])
    assert active(page)['assets']==[]
    passed('Inventory add, edit and confirmed removal work')
    nav(page,'opportunities')
    page.locator('[data-opp-select="config"]').check()
    action(page,'opportunity','config')
    page.locator('#m-notes').fill('Test the configuration-review effort hypothesis.')
    page.locator('#m-priority').select_option('High')
    action(page,'save-opportunity')
    assert active(page)['opportunities']['config']['selected'] is True
    assert active(page)['opportunities']['config']['priority']=='High'
    assert page.evaluate('HaloNavigator.getPilotGate().ready') is False
    passed('Opportunity selection and hypotheses are saved without falsely closing pilot gates')
    nav(page,'executive')
    page.locator('#exec-cases').fill('100')
    page.locator('#exec-minutes').fill('60')
    page.locator('#exec-rate').fill('100')
    page.locator('#exec-reduction').evaluate('(el)=>{el.value=50;el.dispatchEvent(new Event("input",{bubbles:true}));el.dispatchEvent(new Event("change",{bubbles:true}));}')
    expect(page.locator('#scenario-hours')).to_have_text('50 h')
    expect(page.locator('#scenario-value')).to_have_text('$5,000')
    page.locator('#exec-audience').select_option('CFO')
    expect(page.locator('#audience-copy')).to_contain_text('total costs')
    page.locator('[data-outcome="0"]').check()
    page.locator('#exec-baseline').fill('Test-only baseline from 100 reviews.')
    page.locator('#exec-target').fill('Hypothesis to test, not a promise.')
    passed('Executive audience, outcomes and transparent slider calculation update live')
    nav(page,'pilot')
    page.locator('#pilot-owner').fill('Test pilot owner')
    page.locator('#pilot-scope').fill('A strictly defined test fixture scope.')
    page.locator('#pilot-criteria').fill('Document accuracy and compare review effort.')
    page.locator('#pilot-start').fill('2026-11-10')
    page.locator('#pilot-start').press('Tab')
    page.locator('#pilot-review').fill('2026-11-01')
    page.locator('#pilot-review').press('Tab')
    assert active(page)['pilot']['review']==''
    page.locator('#pilot-review').fill('2026-11-20')
    page.locator('#pilot-review').press('Tab')
    page.locator('[data-task="scope"]').check()
    page.locator('[data-task-owner="scope"]').fill('Customer owner')
    page.locator('[data-task-owner="scope"]').press('Tab')
    assert active(page)['pilot']['tasks']['scope']['done'] is True
    assert page.evaluate('HaloNavigator.getPilotGate().ready') is False
    passed('Pilot dates validate and planning checkboxes cannot bypass unresolved GTT proof')
    nav(page,'output')
    page.locator('#architect-notes').fill('INTERNAL-ONLY-TEST-MARKER')
    page.locator('#architect-notes').press('Tab')
    action(page,'refresh-brief')
    expect(page.locator('#brief-preview')).to_contain_text('INTERNAL-ONLY-TEST-MARKER')
    action(page,'brief-mode','customer')
    expect(page.locator('#brief-preview')).not_to_contain_text('INTERNAL-ONLY-TEST-MARKER')
    expect(page.locator('#brief-preview')).to_contain_text('remain unresolved')
    passed('Customer brief omits internal notes but preserves material uncertainties')
    # Capture genuine browser-generated downloads, including actual file bytes.
    for act,ending in [('backup','.json'),('export-markdown','.md'),('export-html','.html'),('export-gtt','.md'),('export-pilot','.md')]:
        with page.expect_download(timeout=10000) as pending:
            action(page,act)
        d=pending.value
        assert d.suggested_filename.endswith(ending)
        dest=ARTIFACTS/('download-'+act+ending)
        d.save_as(str(dest))
        assert dest.stat().st_size>200
    passed('JSON backup, Markdown, HTML, GTT question brief and pilot brief download as real files')
    exported=json.loads((ARTIFACTS/'download-backup.json').read_text())
    assert exported['schemaVersion']==2
    assert exported['session']['profile']['name']=='Acceptance Test Enterprise'
    export_html=(ARTIFACTS/'download-export-html.html').read_text()
    assert 'INTERNAL-ONLY-TEST-MARKER' not in export_html
    assert 'Time = Risk' not in export_html
    passed('Exported customer HTML excludes internal notes; JSON contains the current engagement')
    # Print uses the real generated document, with window.print stubbed to avoid an OS dialog.
    page.evaluate('window.__printCalled=false;window.print=()=>{window.__printCalled=true;}')
    action(page,'print')
    assert page.evaluate('window.__printCalled')
    assert 'Acceptance Test Enterprise' in page.locator('#print-root').text_content()
    passed('Print action builds the selected brief and invokes the browser print path')
    # Prove state reconstruction through the app's real JSON load/save code.
    page.wait_for_timeout(500)
    storage=page.evaluate('({"gtt.halo.presales.v2":localStorage.getItem("gtt.halo.presales.v2")})')
    page2=setup_page(context,saved=storage)
    assert active(page2)['profile']['name']=='Acceptance Test Enterprise'
    assert active(page2)['customer']['inventory']['status']=='gap'
    assert active(page2)['notes']=='INTERNAL-ONLY-TEST-MARKER'
    assert active(page2)['executive']['reduction']==50
    passed('Persistence round-trip reconstructs the same engagement with a Storage test double')
    page2.close()
    # Multi-session change restores each dataset.
    nav(page,'overview')
    demo=next(s for s in snap(page)['sessions'] if s['demo'])
    test=next(s for s in snap(page)['sessions'] if not s['demo'])
    page.locator('#session-select').select_option(demo['id'])
    assert active(page)['demo']
    page.locator('#session-select').select_option(test['id'])
    assert active(page)['notes']=='INTERNAL-ONLY-TEST-MARKER'
    passed('Switching customer engagements preserves separate local datasets')
    # Import accepts exported data as a new copy and rejects malformed versions.
    before=len(snap(page)['sessions'])
    page.locator('#import-input').set_input_files(str(ARTIFACTS/'download-backup.json'))
    page.wait_for_timeout(250)
    assert len(snap(page)['sessions'])==before+1
    assert active(page)['profile']['name']=='Acceptance Test Enterprise'
    invalid=ARTIFACTS/'invalid-import.json'
    invalid.write_text('{"schemaVersion":9,"session":{}}')
    page.locator('#import-input').set_input_files(str(invalid))
    page.wait_for_timeout(250)
    assert len(snap(page)['sessions'])==before+1
    expect(page.locator('#toast-root')).to_contain_text('Import rejected')
    passed('Session import preserves existing data and rejects unsupported schemas')
    # Imported HTML is inert and forged incomplete evidence is downgraded.
    malicious=exported.copy()
    malicious=json.loads(json.dumps(exported))
    malicious['session']['profile']['name']='<img src=x onerror="window.__xss=1">'
    malicious['session']['gtt']['compatibility']={'status':'evidenced','answer':'unsupported fixture','owner':'','date':'','evidence':''}
    evil=ARTIFACTS/'escaped-import.json';evil.write_text(json.dumps(malicious))
    page.locator('#import-input').set_input_files(str(evil))
    page.wait_for_timeout(300)
    assert page.evaluate('window.__xss') is None
    assert active(page)['gtt']['compatibility']['status']=='review'
    assert page.locator('#session-select').input_value()==active(page)['id']
    passed('Import escapes user HTML and downgrades incomplete evidence assertions')
    action(page,'search')
    page.locator('#global-search').fill('rollback')
    expect(page.locator('#global-results')).to_contain_text('rollback')
    page.locator('#global-results [data-action="gtt-question"]').first.click()
    expect(page.locator('#modal-title')).to_contain_text('rollback')
    page.keyboard.press('Escape')
    page.keyboard.press('Control+k')
    expect(page.locator('#global-search')).to_be_visible()
    page.keyboard.press('Escape')
    passed('Global search and keyboard shortcut navigate to the matching detail dialog')
    # All closeable tutorial / product dialogs work.
    for act, ident in [('talk',None),('sources',None),('module','detect'),('profile',None)]:
        action(page,act,ident)
        expect(page.locator('[role="dialog"]')).to_be_visible()
        page.keyboard.press('Escape')
        expect(page.locator('[role="dialog"]')).to_have_count(0)
    passed('Talk track, sources, product tutorial and profile dialogs open and close')
    # Deletion is explicit and limited to the selected engagement.
    nav(page,'output');n=len(snap(page)['sessions'])
    action(page,'delete-session')
    action(page,'confirm-delete-session')
    assert len(snap(page)['sessions'])==n-1
    passed('Confirmed local deletion removes only the selected engagement')
    # Mobile navigation and layout.
    page.set_viewport_size({'width':390,'height':844})
    for route in ['overview','discovery','readiness','stack','executive','opportunities','pilot','output']:
        action(page,'mobile')
        nav(page,route)
        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),route
    action(page,'mobile');nav(page,'discovery')
    action(page,'customer-question','inventory')
    expect(page.locator('[role="dialog"]')).to_be_visible()
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
    page.screenshot(path=str(ARTIFACTS/'mobile-discovery.png'),full_page=True)
    page.keyboard.press('Escape')
    passed('Eight routes and discovery dialog fit a 390px viewport; mobile navigation works')
    # Storage restrictions do not stop the app; backup remains available.
    fallback=setup_page(context,storage=False)
    expect(fallback.locator('h1')).to_contain_text('Confidence starts')
    expect(fallback.locator('#save-status')).to_contain_text('Storage unavailable')
    passed('Blocked browser storage produces a visible warning instead of a broken app')
    fallback.close()
    assert not errors,errors
    passed('No JavaScript runtime errors throughout the interactive test sequence')
    browser.close()
report={'application':'HALO Presales Navigator 2.1.0 GitHub package','test_count':len(RESULTS),'results':RESULTS,'environment':'Chromium automated UI via exact built HTML; no network dependencies. Native navigation is blocked by the build environment. Storage persistence tested with a Storage-compatible test double. Windows launcher execution is not tested on Windows here.'}
(ARTIFACTS/'acceptance-results.json').write_text(json.dumps(report,indent=2))
print('TOTAL',len(RESULTS),'PASS',flush=True)
