// Screenshots of the live pages for the README.  Serve docs/ first (python -m http.server 8811 --directory docs), then:
//   node shot.mjs http://localhost:8811 ../docs/img
import puppeteer from 'puppeteer-core';
const [base, out] = process.argv.slice(2);
const shots = [
  ['explorer.png', '/app/#task=09-inverted-taper-spar-web&model=gpt-5.6-sol-none', 1400, 1500],
  ['explorer-lug.png', '/app/#task=01-oblique-lug-fitting&model=o3', 1400, 1500],
  ['project-page.png', '/', 1280, 1700],
];
const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
for (const [name, path, w, h] of shots) {
  const page = await browser.newPage();
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }]);
  await page.setViewport({ width: w, height: h });
  await page.goto(base + path, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise((r) => setTimeout(r, 600));
  await page.screenshot({ path: `${out}/${name}` });
  console.log('saved', name);
  await page.close();
}
await browser.close();
