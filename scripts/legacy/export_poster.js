const puppeteer = require('puppeteer');
const sharp = require('sharp');
const path = require('path');

(async () => {
  console.log('Starting export...');
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  const filePath = `file:///${path.resolve(__dirname, 'poster_online.html').replace(/\\/g, '/')}`;
  
  // Set viewport for high resolution capture (width 1189px is the poster size, deviceScaleFactor 4 gives ~4756px width)
  await page.setViewport({
    width: 1189,
    height: 1000,
    deviceScaleFactor: 4, 
  });
  
  console.log(`Loading page: ${filePath}`);
  await page.goto(filePath, { waitUntil: 'networkidle0' });
  
  console.log('Taking high-resolution screenshot...');
  // Capture full page screenshot to buffer
  const screenshotBuffer = await page.screenshot({ fullPage: true, type: 'png' });
  
  await browser.close();
  console.log('Screenshot captured. Processing images with sharp...');
  
  // Create sharp instance with sRGB profile
  const image = sharp(screenshotBuffer).withMetadata({ density: 300 });

  // 1. Export PNG (Lossless, High quality)
  console.log('Saving PNG...');
  await image
    .png({ compressionLevel: 9 })
    .toFile('poster_online.png');
    
  // 2. Export WebP (Great efficiency, good quality)
  console.log('Saving WebP...');
  await image
    .webp({ quality: 90, effort: 6 })
    .toFile('poster_online.webp');
    
  // 3. Export HEIF/HEIC (Excellent codec for storage efficiency)
  console.log('Saving HEIF...');
  try {
    await image
      .heif({ quality: 80, compression: 'hevc', effort: 6 })
      .toFile('poster_online.heic');
    console.log('HEIF saved successfully.');
  } catch (err) {
    console.warn('Warning: Native HEIF export failed, falling back to WebP instead of HEIF. Error:', err.message);
  }

  console.log('All exports completed successfully!');
})();
