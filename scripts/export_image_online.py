import time
import os
import zlib
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io

Image.MAX_IMAGE_PIXELS = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DIST_ONLINE = os.path.join(PROJECT_ROOT, "dist", "online")

def set_png_dpi(png_path, dpi=300):
    """Embeds DPI pHYs chunk into the PNG file."""
    with open(png_path, 'rb') as f:
        data = f.read()
    
    ppm = int(round(dpi / 0.0254))  # pixels per meter
    phys_data = b'pHYs' + ppm.to_bytes(4, 'big') + ppm.to_bytes(4, 'big') + b'\x01'
    crc = zlib.crc32(phys_data).to_bytes(4, 'big')
    phys_chunk = (9).to_bytes(4, 'big') + phys_data + crc
    
    phys_idx = data.find(b'pHYs')
    if phys_idx != -1:
        start = phys_idx - 4
        new_data = data[:start] + phys_chunk + data[start+21:]
    else:
        new_data = data[:33] + phys_chunk + data[33:]
        
    with open(png_path, 'wb') as f:
        f.write(new_data)

def main():
    os.makedirs(DIST_ONLINE, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.page_load_strategy = 'eager'
    
    print("=" * 60)
    print("ONLINE POSTER EXPORT (MAX COMPRESSION & VISUAL FIDELITY)")
    print("=" * 60)
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        html_file = os.path.join(PROJECT_ROOT, "poster_online.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        driver.get(url)
        print("Waiting 4 seconds for fonts, gradients, and images to render...")
        time.sleep(4)
        
        # Set viewport with deviceScaleFactor = 4 to match 1189 * 4 = 4756px
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": 1189,
            "height": 1000,
            "deviceScaleFactor": 4,
            "mobile": False
        })
        time.sleep(2)
        
        print("Capturing high-resolution full-page screenshot via CDP...")
        res = driver.execute_cdp_cmd("Page.captureScreenshot", {
            "format": "png",
            "captureBeyondViewport": True
        })
        
        import base64
        png_bytes = base64.b64decode(res["data"])
        img = Image.open(io.BytesIO(png_bytes))
        print(f"Captured master dimensions: {img.size[0]} x {img.size[1]} px ({img.size[0]*img.size[1]/1e6:.1f} Megapixels)")
        
        # -------------------------------------------------------------
        # 1. Ultra-Optimized PNG (Lossless 100%, Scanline filter prediction)
        # -------------------------------------------------------------
        dist_png = os.path.join(DIST_ONLINE, "poster_online.png")
        print(f"\n[1/4] Encoding PNG (Lossless, optimize=True, compress_level=9)...")
        t0 = time.time()
        img.save(dist_png, format="PNG", dpi=(300, 300), optimize=True, compress_level=9)
        set_png_dpi(dist_png, 300)
        png_sz = os.path.getsize(dist_png) / (1024 * 1024)
        print(f"  -> PNG saved: {dist_png} ({png_sz:.2f} MB in {time.time()-t0:.2f}s)")
        
        # -------------------------------------------------------------
        # 2. Text-Preset WebP (Sharp typography, no ringing artifacts)
        # -------------------------------------------------------------
        dist_webp = os.path.join(DIST_ONLINE, "poster_online.webp")
        print(f"\n[2/4] Encoding WebP (quality=88, method=6, preset='text')...")
        t0 = time.time()
        img.save(dist_webp, format="WEBP", quality=88, method=6, preset="text")
        webp_sz = os.path.getsize(dist_webp) / (1024 * 1024)
        print(f"  -> WebP saved: {dist_webp} ({webp_sz:.2f} MB in {time.time()-t0:.2f}s)")
        
        # -------------------------------------------------------------
        # 3. AVIF / HEIF (AV1 Next-Gen Codec, 4:4:4 Full Chroma, RDO speed=2)
        # -------------------------------------------------------------
        dist_avif = os.path.join(DIST_ONLINE, "poster_online.avif")
        dist_heif = os.path.join(DIST_ONLINE, "poster_online.heif")
        print(f"\n[3/4] Encoding AVIF/HEIF (AV1, quality=80, speed=2, subsampling='4:4:4')...")
        t0 = time.time()
        img.save(dist_avif, format="AVIF", quality=80, speed=2, subsampling="4:4:4")
        shutil.copyfile(dist_avif, dist_heif)
        avif_sz = os.path.getsize(dist_avif) / (1024 * 1024)
        print(f"  -> AVIF saved: {dist_avif} ({avif_sz:.2f} MB in {time.time()-t0:.2f}s)")
        print(f"  -> HEIF container synced: {dist_heif} ({avif_sz:.2f} MB)")
        
        # -------------------------------------------------------------
        # 4. Social Media Pre-Optimized (2048px width, Lanczos downsampling)
        #    Prevents social platforms (Facebook/LinkedIn/X) from ruining
        #    sharpness via their aggressive server-side recompression.
        # -------------------------------------------------------------
        print(f"\n[4/4] Generating Social Media Pre-Optimized editions (2048px width)...")
        w_orig, h_orig = img.size
        social_w = 2048
        social_h = int(round(h_orig * social_w / w_orig))
        social_img = img.resize((social_w, social_h), Image.Resampling.LANCZOS)
        
        # Social WebP (~640 KB)
        social_webp = os.path.join(DIST_ONLINE, "poster_social.webp")
        social_img.save(social_webp, format="WEBP", quality=88, method=6, preset="text")
        s_webp_kb = os.path.getsize(social_webp) / 1024
        print(f"  -> Social WebP (2048px): {social_webp} ({s_webp_kb:.1f} KB)")
        
        # Social JPEG (High-grade 4:4:4 chroma, ~1.8 MB, universally accepted by all platforms)
        social_jpg = os.path.join(DIST_ONLINE, "poster_social.jpg")
        social_img.save(social_jpg, format="JPEG", quality=92, optimize=True, subsampling=0)
        s_jpg_mb = os.path.getsize(social_jpg) / (1024 * 1024)
        print(f"  -> Social JPEG (2048px 4:4:4): {social_jpg} ({s_jpg_mb:.2f} MB)")
        
        print("\n" + "=" * 60)
        print("ONLINE & SOCIAL PIPELINE COMPLETED SUCCESSFULLY:")
        print(f"  - Master PNG:    {png_sz:.2f} MB (Lossless truecolor)")
        print(f"  - Master WebP:   {webp_sz:.2f} MB (High-res text-preset)")
        print(f"  - Master AVIF:   {avif_sz:.2f} MB (AV1 4:4:4 full chroma)")
        print(f"  - Social WebP:   {s_webp_kb:.1f} KB (Optimized 2048px for web feeds)")
        print(f"  - Social JPEG:   {s_jpg_mb:.2f} MB (Universal Facebook/LinkedIn upload)")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
