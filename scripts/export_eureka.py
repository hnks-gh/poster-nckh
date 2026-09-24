import time
import os
import zlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import io

Image.MAX_IMAGE_PIXELS = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DIST_EUREKA = os.path.join(PROJECT_ROOT, "dist", "eureka")

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
    os.makedirs(DIST_EUREKA, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.page_load_strategy = 'eager'
    
    print("=" * 60)
    print("EUREKA POSTER EXPORT (PNG 300 DPI, 8:13 RATIO)")
    print("=" * 60)
    print("Initializing Chrome WebDriver for Eureka poster...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.join(PROJECT_ROOT, "poster-eureka.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        driver.get(url)
        print("Waiting 4 seconds for fonts, gradients, and images to render...")
        time.sleep(4)
        
        poster = driver.find_element(By.CLASS_NAME, "poster")
        w = poster.size['width']
        h = poster.size['height']
        print(f"Poster CSS dimensions: {w} x {h} px")
        
        # Scale factor 4 produces 1056 * 4 = 4224px width, 1716 * 4 = 6864px height
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": 1920,
            "height": 3000,
            "deviceScaleFactor": 4,
            "mobile": False
        })
        time.sleep(2)
        
        print("Capturing element screenshot for Eureka poster...")
        png_bytes = poster.screenshot_as_png
        
        img = Image.open(io.BytesIO(png_bytes))
        print(f"Captured Eureka poster dimensions: {img.size[0]} x {img.size[1]} pixels ({img.size[0]*img.size[1]/1e6:.1f} Megapixels)")
        
        dist_png = os.path.join(DIST_EUREKA, "poster-eureka.png")
        
        print(f"Saving to {dist_png}...")
        img.save(dist_png, format="PNG", dpi=(300, 300), compress_level=6)
        set_png_dpi(dist_png, 300)
        
        print(f"Successfully saved: {dist_png} ({os.path.getsize(dist_png)/(1024*1024):.2f} MB)")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
