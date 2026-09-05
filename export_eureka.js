const puppeteer = require('puppeteer');
const sharp = require('sharp');
const path = require('path');

(async () => {
  console.log('Starting export for poster-eureka...');
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  const filePath = `file:///${path.resolve(__dirname, 'poster-eureka.html').replace(/\\/g, '/')}`;
  
  // Set window / viewport size larger than poster width so nothing gets constrained
  // deviceScaleFactor: 4 produces ultra-high resolution:
  // 1056 * 4 = 4224px width
  // 1716 * 4 = 6864px height
  // Ratio: 4224 / 6864 = 8 / 13 = 0.8 / 1.3
  await page.setViewport({
    width: 1920,
    height: 3000,
    deviceScaleFactor: 4,
  });
  
  console.log(`Loading page: ${filePath}`);
  await page.goto(filePath, { waitUntil: 'networkidle0' });
  
  // Wait 3 seconds for Google Fonts, images, and charts to stabilize
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  console.log('Measuring .poster element...');
  const posterEl = await page.$('.poster');
  const dims = await page.evaluate(el => {
    const cols = document.querySelectorAll('.column');
    return {
      width: el.offsetWidth,
      height: el.offsetHeight,
      col0: cols[0].offsetHeight,
      col1: cols[1].offsetHeight,
      ratio: el.offsetWidth / el.offsetHeight
    };
  }, posterEl);
  
  console.log(`Poster CSS dimensions: ${dims.width}px x ${dims.height}px`);
  console.log(`Columns balance: Col1 = ${dims.col0}px, Col2 = ${dims.col1}px`);
  console.log(`Measured ratio: ${dims.ratio.toFixed(6)} vs Target (8/13): ${(8/13).toFixed(6)}`);
  
  console.log('Capturing high-resolution element screenshot...');
  const screenshotBuffer = await posterEl.screenshot({ type: 'png' });
  
  await browser.close();
  console.log('Screenshot captured. Processing image with sharp (300 DPI metadata)...');
  
  const outputPng = path.resolve(__dirname, 'poster-eureka.png');
  await sharp(screenshotBuffer)
    .withMetadata({ density: 300 })
    .png({ compressionLevel: 9 })
    .toFile(outputPng);
    
  console.log(`Successfully saved: ${outputPng}`);
  
  // Verify output metadata
  const meta = await sharp(outputPng).metadata();
  console.log(`PNG Dimensions: ${meta.width} x ${meta.height} px (${(meta.width * meta.height / 1e6).toFixed(1)} Megapixels)`);
  console.log(`PNG Aspect ratio: ${meta.width} / ${meta.height} = ${(meta.width / meta.height).toFixed(6)} (Target: ${(8/13).toFixed(6)})`);
  console.log('All exports completed successfully!');
})();
