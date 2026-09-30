# GTT Defense Halo — Presales Navigator

**Release 2.1.0 · GitHub/Vercel package · September 30, 2026**

A working, HALO-only presales application for engineers and architects. Black/green interface, eight screens, editable engagement data, guided discovery, separate GTT product-evidence questions, executive framing, pilot planning and exports. This is not a screenshot wrapper.

## Deploy this repository

Upload the **extracted contents** of `HALO_GitHub_Repository.zip` to a new repository. Do not upload the ZIP itself and do not place everything inside another folder. At the repository root you should see `package.json`, `vercel.json`, `index.html`, `src/` and `scripts/`.

Then import that repository into Vercel using its GitHub integration. See **[GITHUB-VERCEL-SETUP.md](GITHUB-VERCEL-SETUP.md)** for the individual steps.

| Setting | Value for this package |
| --- | --- |
| Framework Preset | Other |
| Root Directory | Repository root (`.`) |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | Skipped; configured as an empty string |
| Node.js | 22.x |
| Environment variables | None |

These settings are supplied in `vercel.json` and `package.json`. There are no external npm build or runtime dependencies. Python is **not** used by the deployment build. Python is needed only to run the optional browser acceptance tests.

Only `dist/` is published. Readable source, tests, documentation and the Windows launcher are not deployed as static files. Vercel builds `dist` from source on each deployment; you do not have to upload `dist` separately.

## Application screens

| Screen | Working behavior |
| --- | --- |
| Overview | Engagement context, discovery progress, product validation and evaluation readiness. |
| Customer Discovery | Sixteen guided questions; answers, statuses, evidence references, owners, dates, filters and interview mode. |
| GTT Readiness | Fourteen validation questions; evidence requirements, review dates, ownership, unresolved issues and freshness flags. |
| HALO vs Current Stack | Editable control coverage, product inventory and comparison notes. Existing customer tools are not automatically treated as inadequate. |
| Executive Experience | Audience selectors, desired outcomes, baselines and transparent effort scenarios. No invented financial results. |
| Strategic Opportunities | Customer-specific hypotheses, priorities and selected evaluation paths tied to discovery and product evidence. |
| Pilot Plan | Scope, dates, owners, success criteria, planning tasks and unresolved product gates. |
| Output Brief | Internal/customer views, notes, Markdown/HTML exports, print, JSON backups and import. |

Additional controls: hover help, keyboard search, responsive navigation, customer-session switching, explicit deletion confirmation and a fictional demo. The UI contains no support-flow or technology-transformation module.

## Important boundaries

This release has **no login, backend database, shared user accounts, server-side tenant isolation or live HALO integration**. It does not scan assets, observe a real network, execute security actions or contact an AI API. Executive briefs are assembled deterministically from entered information.

Engagements remain in the current browser's local storage, when permitted. This application does not encrypt that storage. Separate engagement records are not a security boundary. Browser cleanup, private browsing, a new device, a new deployment hostname or changing from a local file to a hosted URL may make earlier records unavailable. Export JSON backups and import them on the target URL.

Use fictional/demo information until the intended organization approves the environment. Do not enter credentials, customer secrets, raw production telemetry or restricted personal data. Indexing exclusions are included, but they are not authentication or access control. A private GitHub repository does not configure this application's authorization.

The supplied demo is fictional. Customer posture begins unassessed for a new engagement. Product compatibility, coverage, integrations, service boundaries and response authority require current GTT confirmation. The 90-day evidence-refresh convention is a Navigator design rule, not a stated GTT policy.

## Local development

With Node.js 22 installed, run from the repository root:

```bash
npm run build
npm start
```

Open the local address printed by the server, normally `http://127.0.0.1:4173`. Stop it with Ctrl+C. `npm run dev` builds and starts the same preview; it does not provide hot reloading. After editing source, rebuild and refresh.

The included `index.html` is a generated standalone copy. Edit `src/`, not that generated file. `START-HALO.cmd` is an optional local-browser launcher; it is not needed for GitHub or Vercel.

```bash
npm test
```

This checks syntax, rebuilds and runs the Node build/server tests. Optional browser tests:

```bash
python -m pip install -r tests/requirements.txt
python -m playwright install chromium
npm run build
python tests/acceptance.py
```

Linux systems may need `python -m playwright install --with-deps chromium`. The included GitHub workflow runs build and browser tests without deploying or requesting Vercel credentials. The workflow has been supplied, not run in your GitHub account.

## Project structure

```text
index.html                 Generated standalone application
package.json               Node scripts; no third-party dependencies
package-lock.json          Reproducible npm metadata
vercel.json                Build/output settings and response headers
src/data.js                Discovery, validation and product-orientation content
src/app.js                 UI and browser-local application behavior
src/style.css              Responsive black/green design
src/template.html          Build template
scripts/build.mjs          Node-only build; writes dist and index.html
scripts/serve.mjs          Local preview of allowlisted production files
public/                    robots.txt and 404.html
.github/workflows/         Validation workflow, no deployment credentials
tests/                     Reproducible Node and browser checks
docs/                      QA report, results, boundaries and release notes
GITHUB-VERCEL-SETUP.md      Click-by-click upload and deployment guide
```

## Verification

The packaged production HTML passed 29 browser interaction checks. The repository also passed 13 Node build/server test results. See [docs/QA-REPORT.md](docs/QA-REPORT.md) for scope, results and limitations. This is not a production security assessment. No hosted deployment was created or tested for this release.

## Sources and content review

Product orientation: GTT's public Defense Halo page, reviewed September 30, 2026: https://www.gtt.net/defense-halo/ . Technical support claims still require current, scoped GTT evidence. AI-assisted software and discovery content require accountable human review; this is not an official GTT product certification.

Public deployment documentation used for the guide:
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://vercel.com/docs/getting-started-with-vercel
- https://vercel.com/docs/project-configuration/vercel-json
- https://vercel.com/docs/builds/configure-a-build

The separate `HALO_Static_Web.zip` contains the already-built web files for static hosting. It is an alternative delivery package, not additional files to merge into this repository.
