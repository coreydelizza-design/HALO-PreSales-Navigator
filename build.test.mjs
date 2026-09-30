import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import vm from 'node:vm';
const root = fileURLToPath(new URL('./', import.meta.url));
const read = file => readFileSync(path.join(root, file), 'utf8');
const html = read('dist/index.html');
const config = JSON.parse(read('vercel.json'));
const pkg = JSON.parse(read('package.json'));
test('production output includes only the three web files', () => {
  assert.deepEqual(readdirSync(path.join(root, 'dist')).sort(), ['404.html', 'index.html', 'robots.txt']);
});
test('standalone and production entry points are identical', () => {
  assert.equal(read('index.html'), html);
});
test('generated HTML contains current readable sources exactly', () => {
  for (const file of ['style.css', 'data.js', 'app.js']) assert(html.includes(read(file)), file);
  assert(!html.includes('{{HALO_'));
});
test('runtime has no remote script, stylesheet, frame, or image dependency', () => {
  assert(!/<script[^>]+src\s*=/i.test(html));
  assert(!/<link[^>]+rel=["']stylesheet/i.test(html));
  assert(!/<(?:iframe|img)[^>]+src=["']https?:/i.test(html));
  assert(html.includes("connect-src 'none'"));
  assert(html.includes('noindex,nofollow'));
});
test('Vercel configuration points to a dependency-free production build', () => {
  assert.equal(config.framework, null);
  assert.equal(config.installCommand, '');
  assert.equal(config.buildCommand, 'npm run build');
  assert.equal(config.outputDirectory, 'dist');
  assert.equal(pkg.scripts.build, 'node build.mjs');
  assert.equal(Object.keys(pkg.dependencies || {}).length, 0);
  assert.equal(Object.keys(pkg.devDependencies || {}).length, 0);
});
test('response protection and indexing headers are included', () => {
  const h = Object.fromEntries(config.headers[0].headers.map(x => [x.key, x.value]));
  assert.equal(h['X-Content-Type-Options'], 'nosniff');
  assert.equal(h['X-Frame-Options'], 'DENY');
  assert.equal(h['X-Robots-Tag'], 'noindex, nofollow');
  assert.equal(h['Cache-Control'], 'no-store');
  assert(read('dist/robots.txt').includes('Disallow: /'));
});
test('discovery and validation questions have unique identifiers and valid module links', () => {
  const c = vm.createContext({});
  vm.runInContext(read('data.js') + '\nthis.fixture={CUSTOMER,GTT,MODULES};', c);
  const {CUSTOMER, GTT, MODULES} = c.fixture;
  assert.equal(CUSTOMER.length, 16);
  assert.equal(GTT.length, 14);
  for (const list of [CUSTOMER, GTT, MODULES]) assert.equal(new Set(list.map(x => x.id)).size, list.length);
  const modules = new Set(MODULES.map(x => x.id));
  for (const q of [...CUSTOMER, ...GTT]) {
    assert(q.question && q.title);
    for (const id of q.modules || []) assert(modules.has(id), id);
  }
});
test('runtime still explicitly distinguishes demo, evidence and non-connected systems', () => {
  assert(html.includes('Northstar Retail'));
  assert(html.includes('No HALO APIs'));
  assert(html.includes('not confirmed product fit'));
  assert(html.includes('Browser data is not encrypted by this application'));
});
