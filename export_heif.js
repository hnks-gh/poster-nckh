const puppeteer = require('puppeteer');
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

(async () => {
  const screenshotBuffer = fs.readFileSync('poster_online.png');
  const image = sharp(screenshotBuffer);
  
  console.log('Saving AVIF (HEIF container with AV1 codec) for highest efficiency...');
  await image
    .avif({ quality: 80, effort: 6 })
    .toFile('poster_online.heif');
  
  console.log('All exports completed successfully!');
})();
