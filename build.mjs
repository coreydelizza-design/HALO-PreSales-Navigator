/** Dependency-free production build. Publishes only the allowlisted web files. */
import { readFile, writeFile, mkdir, rm, copyFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
const root = fileURLToPath(new URL('../', import.meta.url));
const out = path.join(root, 'dist');
try {
  for (const file of ['src/data.js', 'src/app.js']) {
    execFileSync(process.execPath, ['--check', path.join(root, file)], { stdio: 'inherit' });
  }
  const [template, css, data, app] = await Promise.all(
    ['src/template.html', 'src/style.css', 'src/data.js', 'src/app.js']
      .map(file => readFile(path.join(root, file), 'utf8'))
  );
  const script = data + '\n' + app;
  assert(!/<\/script/i.test(script), 'Source must not close its enclosing script element.');
  assert(!/<\/style/i.test(css), 'Styles must not close their enclosing style element.');
  for (const marker of ['{{HALO_STYLES}}', '{{HALO_SCRIPT}}']) {
    assert.equal(template.split(marker).length, 2, `Expected one ${marker} placeholder.`);
  }
  // Functions avoid replacement-string dollar expansion in application code.
  const html = template.replace('{{HALO_STYLES}}', () => css)
    .replace('{{HALO_SCRIPT}}', () => script);
  assert(!html.includes('{{HALO_'), 'Unexpanded template placeholder.');
  await rm(out, { recursive: true, force: true });
  await mkdir(out, { recursive: true });
  await writeFile(path.join(out, 'index.html'), html, 'utf8');
  await writeFile(path.join(root, 'index.html'), html, 'utf8');
  for (const name of ['robots.txt', '404.html']) {
    await copyFile(path.join(root, 'public', name), path.join(out, name));
  }
  console.log(`HALO production build complete: dist/index.html (${Buffer.byteLength(html).toLocaleString()} bytes).`);
  console.log('Published files: index.html, robots.txt, 404.html. No credentials or environment variables required.');
} catch (error) {
  console.error('HALO build failed:', error.message);
  process.exitCode = 1;
}
