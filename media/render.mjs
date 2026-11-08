// Renders each .frame in an HTML file to a PNG (s1.png, s2.png, ...).  node render.mjs <file.html> <outdir>
import puppeteer from 'puppeteer-core';
import { pathToFileURL } from 'node:url';
import { mkdirSync } from 'node:fs';
const [file, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 2000, height: 1200, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(file).href, { waitUntil: 'networkidle0' });
await page.evaluateHandle('document.fonts.ready');
for (const id of await page.$$eval('.frame', (els) => els.map((e) => e.id))) {
  await (await page.$(`#${id}`)).screenshot({ path: `${out}/${id}.png` });
  console.log('saved', id);
}
await browser.close();
