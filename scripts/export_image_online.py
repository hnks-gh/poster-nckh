import time
import os
import zlib
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
    print("ONLINE POSTER EXPORT (PNG 300 DPI, WebP, HEIF)")
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
        print(f"Captured image dimensions: {img.size[0]} x {img.size[1]} pixels ({img.size[0]*img.size[1]/1e6:.1f} Megapixels)")
        
        # 1. Save poster_online.png
        dist_png = os.path.join(DIST_ONLINE, "poster_online.png")
        print(f"Saving PNG to {dist_png}...")
        img.save(dist_png, format="PNG", dpi=(300, 300), compress_level=6)
        set_png_dpi(dist_png, 300)
        print(f"PNG saved successfully: {os.path.getsize(dist_png)/(1024*1024):.2f} MB")
        
        # 2. Save poster_online.webp
        dist_webp = os.path.join(DIST_ONLINE, "poster_online.webp")
        print(f"Saving WebP to {dist_webp}...")
        img.save(dist_webp, format="WEBP", quality=90, method=6)
        print(f"WebP saved successfully: {os.path.getsize(dist_webp)/(1024*1024):.2f} MB")
        
        # 3. Save poster_online.heif (AVIF format in HEIF container)
        dist_heif = os.path.join(DIST_ONLINE, "poster_online.heif")
        print(f"Saving HEIF to {dist_heif}...")
        img.save(dist_heif, format="AVIF", quality=80)
        print(f"HEIF saved successfully: {os.path.getsize(dist_heif)/(1024*1024):.2f} MB")
        
        print("All online poster formats exported successfully in dist/online/!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
