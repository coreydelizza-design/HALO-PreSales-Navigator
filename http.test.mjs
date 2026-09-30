import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import net from 'node:net';
const root = fileURLToPath(new URL('./', import.meta.url));
async function freePort() {
  const s = net.createServer();
  await new Promise((resolve, reject) => { s.once('error', reject); s.listen(0, '127.0.0.1', resolve); });
  const port = s.address().port;
  await new Promise(resolve => s.close(resolve));
  return port;
}
test('HTTP preview serves only production assets with safe method and path handling', async t => {
  const port = await freePort();
  const child = spawn(process.execPath, ['serve.mjs'], {cwd:root, env:{...process.env,PORT:String(port)}});
  t.after(() => child.kill('SIGTERM'));
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Preview failed to start in 10 seconds')), 10000);
    child.stdout.once('data', () => { clearTimeout(timeout); resolve(); });
    child.once('error', e => { clearTimeout(timeout); reject(e); });
    child.once('exit', code => { if (code) {clearTimeout(timeout); reject(new Error('Preview exited '+code));} });
  });
  const base = `http://127.0.0.1:${port}`;
  await t.test('home serves the exact built application', async () => {
    const res = await fetch(base);
    assert.equal(res.status, 200);
    assert.equal(await res.text(), readFileSync(path.join(root, 'dist/index.html'), 'utf8'));
    assert.equal(res.headers.get('x-content-type-options'), 'nosniff');
    assert.equal(res.headers.get('x-robots-tag'), 'noindex, nofollow');
  });
  await t.test('robots file and HEAD work', async () => {
    const robots = await fetch(base+'/robots.txt');
    assert.equal(robots.status, 200);
    assert((await robots.text()).includes('Disallow: /'));
    const head = await fetch(base, {method:'HEAD'});
    assert.equal(head.status, 200);
    assert.equal(await head.text(), '');
  });
  await t.test('source, configuration, tests, credentials and unknown paths are not served', async () => {
    for (const route of ['/app.js','/package.json','/vercel.json','/acceptance.py','/.env','/not-a-page']) {
      assert.equal((await fetch(base+route)).status, 404, route);
    }
  });
  await t.test('write methods are rejected', async () => {
    assert.equal((await fetch(base, {method:'POST',body:'{}'})).status, 405);
  });
});
