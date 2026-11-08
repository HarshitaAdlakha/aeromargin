// Builds the slide PDF and PowerPoint from the rendered PNGs (docs/slides/s1..s9.png).
// The PowerPoint carries the narration as speaker notes (from media/build/narration.txt if present).
//   node deck.mjs
import puppeteer from 'puppeteer-core';
import pptxgen from 'pptxgenjs';
import { readFileSync, existsSync } from 'node:fs';

const dir = '../docs/slides';
const n = 9;
const imgs = Array.from({ length: n }, (_, i) => `${dir}/s${i + 1}.png`);

const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
const page = await browser.newPage();
await page.setContent(`<style>@page{size:1920px 1080px;margin:0}body{margin:0}img{display:block;width:1920px;height:1080px;page-break-after:always}</style>` +
  imgs.map((f) => `<img src="data:image/png;base64,${readFileSync(f).toString('base64')}">`).join(''), { waitUntil: 'load' });
await page.pdf({ path: `${dir}/AeroMargin-slides.pdf`, width: '1920px', height: '1080px', printBackground: true });
await browser.close();
console.log('wrote AeroMargin-slides.pdf');

const notesFile = 'build/narration.txt';
const notes = existsSync(notesFile) ? readFileSync(notesFile, 'utf8').split(/\n\n(?=\[Slide )/).map((s) => s.replace(/^\[Slide \d+\] /, '')) : [];
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'AeroMargin';
pres.author = 'Paras Adlakha and Harshita Adlakha';
pres.company = 'Paras Adlakha and Harshita Adlakha';
pres.subject = 'micro1 Eval Hackathon, November 2026';
imgs.forEach((f, i) => {
  const s = pres.addSlide();
  s.addImage({ path: f, x: 0, y: 0, w: 10, h: 5.625, altText: `AeroMargin slide ${i + 1}` });
  if (notes[i]) s.addNotes(notes[i]);
});
await pres.writeFile({ fileName: `${dir}/AeroMargin-slides.pptx` });
console.log('wrote AeroMargin-slides.pptx');
