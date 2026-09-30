# GitHub → Vercel setup

**Use `HALO_GitHub_Repository.zip` for these steps.** No ChatGPT connector is required. This guide assumes a new repository so an existing application is not overwritten. Button wording may vary slightly with account permissions or repository rules.

## 1. Extract the repository ZIP

1. Save `HALO_GitHub_Repository.zip` to your computer.
2. In Windows File Explorer, right-click the ZIP and select **Extract All**.
3. Click **Extract**.
4. Open the extracted folder.
5. Confirm you see `package.json`, `vercel.json`, `index.html`, `src` and `scripts` together. Upload these contents, not their enclosing folder.

Do not upload the ZIP file itself as the application. GitHub stores an uploaded ZIP as a file; this project's build needs the extracted files at the repository root.

## 2. Create a new GitHub repository

1. Sign in to GitHub in your browser.
2. Open **New repository** (normally from the plus menu at the top right).
3. Select the intended account or organization under **Owner**.
4. Enter `halo-presales-navigator` as the repository name, or another unused name.
5. Choose **Private** for this presales source unless your organization authorizes public distribution.
6. Leave README, license and gitignore initialization off; these files are already supplied where appropriate.
7. Click **Create repository**.

## 3. Upload the application

1. On the empty repository page, click **uploading an existing file**. In an initialized repository, use **Add file → Upload files** instead.
2. In the extracted local folder, select **all the contents**—including folders and dotfiles—and drag them onto GitHub's upload area. Do not drag the enclosing extraction folder.
3. Wait for the file upload list to populate. Confirm paths such as `src/app.js`, `scripts/build.mjs` and `vercel.json` are present.
4. Enter a commit message such as `Add HALO Presales Navigator 2.1.0`.
5. Complete **Commit changes** or **Propose changes**, according to the repository controls shown. If GitHub creates a branch/pull request, finish the required review and merge it before deploying `main`.
6. Return to the repository's **Code** tab. Confirm `package.json` and `vercel.json` are at the top level—not one folder below it.

Some file choosers hide names starting with a dot. Ensure `.github`, `.gitignore` and `.gitattributes` are included when using the full source package. Missing `.github` only omits the optional validation workflow; missing `src` or `scripts` will break the build. GitHub Desktop is an alternative when your browser cannot upload folders or repository rules require a branch workflow.

No customer engagement exports, API tokens or account-specific `.vercel` settings are included. Do not add your real session backups to the repository.

## 4. Import the repository in Vercel

1. Open your Vercel dashboard directly in your browser.
2. Select the workspace you authorize for this application.
3. Open **Add New → Project**, or the dashboard's **New Project** control.
4. Under **Import Git Repository**, choose **GitHub**.
5. Complete GitHub authorization if requested. Grant access to the intended repository; the ChatGPT Vercel connection is not involved.
6. Find `halo-presales-navigator` and click **Import**.
7. Check the **Project Name**. Use a new name rather than replacing an unrelated project.
8. Set or confirm the following. Most values are already defined in `vercel.json`:

| Setting | Required value |
| --- | --- |
| Framework Preset | **Other** |
| Root Directory | Repository root; leave the default or `.` |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Install Command | Empty/skipped; `vercel.json` supplies `""` |
| Node.js | 22.x, requested by `package.json` |
| Environment variables | None |

9. Click **Deploy**.
10. Wait for Vercel to report **Ready**, then open the deployment using **Visit** or its displayed URL.

The build is dependency-free. Vercel runs `npm run build` to generate `dist`; Python is not part of deployment. Only `dist` is served. The UI does not need a continuously running Node server on Vercel.

## 5. Verify the deployed portal

1. Confirm the fictional **Northstar Retail** demo loads. It must be labeled as a demo.
2. Use **New customer** to create a non-sensitive test engagement.
3. In **Customer Discovery**, save an answer and evidence reference.
4. In **GTT Readiness**, verify that an unanswered product question remains open.
5. Switch to **Executive Experience** and change the audience or scenario input.
6. Export a JSON backup and a brief from **Output Brief**.
7. Refresh the same URL in the same browser; confirm the test engagement persists when browser storage is allowed.
8. Test mobile navigation and delete the disposable test engagement when finished.

These are your post-deployment checks. Hosted operation has not been verified by the package author.

## Update the application later

Edit the readable source files in `src/`, then commit/push to the repository. Vercel's Git integration can build and deploy from the connected branch. Confirm the new deployment completes before reviewing it.

Local sessions belong to a browser and origin, not to GitHub. A different deployment hostname will not automatically carry over those sessions. Export a JSON backup on the old origin and import it on the new one.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Repository shows just one ZIP | Extract it and upload the contents. |
| Vercel cannot find `package.json` | Correct Root Directory or remove the unintended wrapper folder. |
| Python or `build.py` error | This release uses `npm run build`; replace settings left from an older package. |
| Missing build output | Output Directory must be `dist`; inspect the build log for errors. |
| Repo not shown in Vercel | Review Vercel's GitHub integration access for that repository. |
| Portal says storage unavailable | Browser policy blocks local storage; do not assume saves persist. JSON export remains available. |
| New URL looks like it lost a session | Storage is origin-specific. Restore a JSON backup on the new origin. |
| Expected production login is absent | This release has no app login or shared database. Hosting does not add these. |

## Security and scope

Use the fictional demo until approved for customer data. A private source repository, indexing exclusions and static response headers are not application authentication or server-side tenant isolation. The UI does not connect to HALO, scan customer assets or execute response actions.

## Official references

Reviewed September 30, 2026:
- GitHub uploads: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- Vercel dashboard deployment: https://vercel.com/docs/getting-started-with-vercel
- Vercel configuration: https://vercel.com/docs/project-configuration/vercel-json
- Vercel build settings: https://vercel.com/docs/builds/configure-a-build
