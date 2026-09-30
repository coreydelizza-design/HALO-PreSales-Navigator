/** Local preview only. Vercel serves dist directly; it does not run this server. */
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('./', import.meta.url));
const dist = path.join(root, 'dist');
const port = Number(process.env.PORT || 4173);
if (!Number.isInteger(port) || port < 1024 || port > 65535) {
  console.error('PORT must be an integer from 1024 through 65535.');
  process.exit(1);
}
const files = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/index.html', ['index.html', 'text/html; charset=utf-8']],
  ['/robots.txt', ['robots.txt', 'text/plain; charset=utf-8']],
  ['/404.html', ['404.html', 'text/html; charset=utf-8']]
]);
const config = JSON.parse(await readFile(path.join(root, 'vercel.json'), 'utf8'));
const headers = Object.fromEntries(config.headers[0].headers.map(h => [h.key, h.value]));
const server = http.createServer(async (req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { ...headers, Allow: 'GET, HEAD' });
    return res.end();
  }
  const entry = files.get((req.url || '/').split('?')[0]);
  const [file, mime] = entry || ['404.html', 'text/html; charset=utf-8'];
  try {
    const body = await readFile(path.join(dist, file));
    res.writeHead(entry ? 200 : 404, { ...headers, 'Content-Type': mime });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch {
    res.writeHead(503, { ...headers, 'Content-Type': 'text/plain; charset=utf-8' });
    res.end(req.method === 'HEAD' ? undefined : 'Build missing. Run npm run build, then npm start.');
  }
});
server.on('error', error => { console.error(error.message); process.exitCode = 1; });
server.listen(port, '127.0.0.1', () => console.log(`HALO preview: http://127.0.0.1:${port}`));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
