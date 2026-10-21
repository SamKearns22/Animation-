// Drive scene.js in headless Chromium.
//   node render.mjs stills OUT.png W H t1,t2,...      one sheet of stills (dance seconds)
//   node render.mjs video OUT.mp4 W H FPS T0 T1        frames piped to ffmpeg (no sound)
//   node render.mjs check OUT.json FPS                 clipping audit of every frame, no pictures
import { chromium } from 'playwright-core';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const ROOT = path.dirname(new URL(import.meta.url).pathname);
const FF = '/usr/local/lib/python3.13/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const MIME = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.html': 'text/html', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg' };
const [mode, out, ...rest] = process.argv.slice(2);

const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(f, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); res.end(data);
  });
}).listen(0);
const port = server.address().port;

const [w, h] = mode === 'check' ? [320, 180] : [+rest[0], +rest[1]];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: w, height: h } });
page.on('console', m => { if (m.type() === 'error') console.error('page:', m.text()); });
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(`http://localhost:${port}/index.html?w=${w}&h=${h}`);
await page.waitForFunction('window.READY === true', null, { timeout: 120000 });

const grab = async () => Buffer.from((await page.evaluate(() => window.frame())).split(',')[1], 'base64');
const t0 = Date.now();

if (mode === 'stills') {
  const times = rest[2].split(',').map(Number);
  const dir = out.replace(/\.png$/, '');
  fs.mkdirSync(dir, { recursive: true });
  for (const [k, t] of times.entries()) {
    const r = await page.evaluate(t => window.renderAt(t), t);
    fs.writeFileSync(`${dir}/${k}.jpg`, await grab());
    console.log(t, JSON.stringify(r), JSON.stringify(await page.evaluate(() => window.DBG ? window.DBG() : null)));
  }
  const n = times.length, cols = Math.min(n, 3), rows = Math.ceil(n / cols);
  const inputs = times.flatMap((_, k) => ['-i', `${dir}/${k}.jpg`]);
  const layout = times.map((_, k) => `${(k % cols) * w}_${Math.floor(k / cols) * h}`).join('|');
  const filt = n > 1 ? `xstack=inputs=${n}:layout=${layout}:fill=black` : 'null';
  await new Promise(r => spawn(FF, ['-v', 'error', '-y', ...inputs, '-filter_complex', filt, out], { stdio: 'inherit' }).on('close', r));
} else if (mode === 'video') {
  const [fps, T0, T1] = rest.slice(2).map(Number);
  const ff = spawn(FF, ['-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const log = [];
  const N = Math.round((T1 - T0) * fps);
  for (let k = 0; k < N; k++) {
    const t = T0 + k / fps;
    const r = await page.evaluate(t => window.renderAt(t), t);
    log.push({ t: +t.toFixed(3), ...r });
    if (!ff.stdin.write(await grab())) await new Promise(r => ff.stdin.once('drain', r));
    if (k % 60 === 0) console.log(`frame ${k}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  fs.writeFileSync(out.replace(/\.mp4$/, '-check.json'), JSON.stringify(log));
} else if (mode === 'check') {
  const fps = +rest[0];
  const log = await page.evaluate(fps => { const L = []; for (let t = -0.4; t < 24.95; t += 1 / fps) L.push({ t: +t.toFixed(3), ...window.renderAt(t) }); return L; }, fps);
  fs.writeFileSync(out, JSON.stringify(log));
}
console.log(`done in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
await browser.close(); server.close();
