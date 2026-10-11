// Frame-by-frame render with Playwright → ffmpeg.
//   node render.mjs out.mp4 [--page=scenes.html] [--w=1080 --h=1920] [--fps=30] [--from=0 --to=total] [--lang=en] [--nocap]
//   node render.mjs --stills=2,10,20 [--page=…] [--nocap] [--prefix=cover-]   → stills/*.jpg (cheap check before a full render)
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

const args = Object.fromEntries(process.argv.slice(2).filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
const out = process.argv.slice(2).find(a => !a.startsWith('--'));
const fps = +(args.fps || 30), W = +(args.w || 1080), Hh = +(args.h || 1920);
const qs = [args.lang ? `lang=${args.lang}` : '', args.nocap ? 'nocap=1' : ''].filter(Boolean).join('&');
const url = pathToFileURL(resolve(args.page || 'scenes.html')).href + (qs ? `?${qs}` : '');

const browser = await chromium.launch({ args: ['--allow-file-access-from-files', '--disable-web-security'] });
const page = await browser.newPage({ viewport: { width: W, height: Hh }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('[pageerror]', e.message));
page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') console.log('[page]', m.text()); });
await page.goto(url);
await page.waitForFunction(() => window.READY === true, null, { timeout: 30000 });
const total = await page.evaluate(() => window.TOTAL);

if (args.stills) {
  mkdirSync('stills', { recursive: true });
  for (const t of String(args.stills).split(',').map(Number)) {
    await page.evaluate(t => window.renderAt(t), t);
    await page.screenshot({ path: `stills/${args.prefix || 't'}${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 88 });
  }
  await browser.close(); process.exit(0);
}

const from = +(args.from || 0), to = +(args.to || total), n = Math.round((to - from) * fps);
const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.renderAt(t), from + i / fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 150 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('done', out, n, 'frames');
