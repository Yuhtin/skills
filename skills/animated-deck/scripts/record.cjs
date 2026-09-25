// Record the deck to MP4 from ROOT/video/pages + plan.json (run tools/video_pages.py first).
//   node tools/record.cjs video/deck.mp4                 whole deck, 30 fps, H.264
//   node tools/record.cjs --test <id> 0 3000 12000       PNG samples at those real-time ms, into renders/
// Each slide page loads in headless Chrome; its scene's clock is stepped 1/30 s at a time
// (postMessage → two animation frames → ack) and every frame is piped to ffmpeg — no frame files,
// so disk use is only the final MP4. Slides fade in/out over FADE frames on the shared background.
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const ROOT = process.env.DECK_ROOT || path.resolve(__dirname, '..'), FPS = 30, FADE = 9;
const cfg = fs.existsSync(path.join(ROOT, 'deck.config.json')) ? JSON.parse(fs.readFileSync(path.join(ROOT, 'deck.config.json'), 'utf8')) : {};

function loadPuppeteer() {
  const tries = [cfg.puppeteer, 'puppeteer', 'puppeteer-core', path.join(ROOT, 'node_modules/puppeteer'), path.join(ROOT, 'node_modules/puppeteer-core')].filter(Boolean);
  for (const t of tries) { try { return require(t); } catch {} }
  console.error('puppeteer not found. In the work folder run:  npm i --no-save puppeteer-core   (or set "puppeteer" in deck.config.json)');
  process.exit(1);
}
function chromePath() {
  if (cfg.chrome) return cfg.chrome;
  for (const c of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'])
    if (fs.existsSync(c)) return c;
  return undefined; // puppeteer's own browser, if it has one
}

const puppeteer = loadPuppeteer();
const plan = JSON.parse(fs.readFileSync(path.join(ROOT, 'video/plan.json'), 'utf8'));
const args = process.argv.slice(2);

async function open(browser, id) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(ROOT, 'video/pages', id + '.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => {
    window.__seq = 0;
    window.__setT = (vt, op) => new Promise((res) => {
      const seq = ++window.__seq;
      document.querySelector('section').style.opacity = op;
      const f = document.querySelector('iframe');
      if (!f) return requestAnimationFrame(() => res(true));
      const h = (e) => { if (e.data && e.data.ack === seq) { removeEventListener('message', h); res(true); } };
      addEventListener('message', h);
      f.contentWindow.postMessage({ vt, seq }, '*');
      setTimeout(() => { removeEventListener('message', h); res(false); }, 1500);
    });
  });
  await new Promise((r) => setTimeout(r, 400)); // let the scene lay out and measure its text
  return page;
}

(async () => {
  const browser = await puppeteer.launch({ executablePath: chromePath(), headless: true, args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  if (args[0] === '--test') {
    const id = args[1], page = await open(browser, id);
    for (const t of args.slice(2).map(Number)) {
      const ok = await page.evaluate((vt) => window.__setT(vt, 1), t);
      const out = path.join(ROOT, 'renders', `video-${id}-${t}.png`);
      await page.screenshot({ path: out });
      console.log(out, ok ? 'ack' : 'NO ACK');
    }
    await browser.close(); return;
  }
  const out = path.resolve(ROOT, args[0] || 'video/deck.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const write = (buf) => new Promise((r) => (ff.stdin.write(buf) ? r() : ff.stdin.once('drain', r)));
  let frames = 0, noack = 0; const t0 = Date.now();
  for (let s = 0; s < plan.length; s++) {
    const { id, dur } = plan[s], n = Math.round(dur / 1000 * FPS), page = await open(browser, id);
    for (let k = 0; k < n; k++) {
      let op = 1;
      if (s > 0 && k < FADE) op = k / FADE;
      if (s < plan.length - 1 && k >= n - FADE) op = (n - 1 - k) / FADE;
      if (!(await page.evaluate((a, b) => window.__setT(a, b), k * 1000 / FPS, op))) noack++;
      await write(await page.screenshot({ type: 'jpeg', quality: 92, optimizeForSpeed: true }));
      frames++;
    }
    await page.close();
    console.log(`${id} done — ${frames} frames, ${((Date.now() - t0) / 1000).toFixed(0)} s elapsed, no-ack ${noack}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  await browser.close();
  console.log('DONE', out, frames, 'frames');
})().catch((e) => { console.error(e); process.exit(1); });
