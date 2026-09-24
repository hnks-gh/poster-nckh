import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'eager'
    
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # CRITICAL: Set browser window size to be larger than the poster width (1189px)
    # to prevent the poster container from shrinking/squishing due to a small default viewport.
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.abspath("poster_online.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        driver.get(url)
        print("Waiting 4 seconds for fonts, gradients, and images to render...")
        time.sleep(4)  # Ensure everything renders completely
        
        # Get poster element dimensions
        poster = driver.find_element(By.CLASS_NAME, "poster")
        width = poster.size['width']
        height = poster.size['height']
        print(f"Poster original dimensions: {width}x{height}")
        
        if width < 1189:
            print("Warning: Poster width is still smaller than the designed 1189px.")
        
        # A0 standard size width is 841mm, height is 1189mm.
        # To get 300 DPI (dots per inch) for printing:
        # A0 in inches is ~33.11in x ~46.81in.
        # 33.11 * 300 = 9933 px, 46.81 * 300 = 14043 px.
        # Since the original poster width in HTML is 1189px,
        # we can use a scale factor of 6.0 to get:
        # Width: 1189 * 6 = 7134 px
        # Height: ~2006 * 6 = ~12036 px
        # This scale factor gives an incredibly high-resolution image suitable for professional A0 printing.
        scale_factor = 2
        print(f"Overriding device metrics with scale factor {scale_factor}x...")
        
        # Set viewport to poster dimensions with scale factor
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": scale_factor,
            "mobile": False
        })
        
        time.sleep(2)  # Wait for layout to scale and stabilize
        
        screenshot_path = os.path.abspath("poster_online.png")
        print(f"Capturing high-resolution screenshot of the poster to: {screenshot_path}")
        
        # Take screenshot of the poster element
        poster.screenshot(screenshot_path)
        print("Screenshot captured successfully!")
        
        # Verify the dimensions of the saved image
        img = Image.open(screenshot_path)
        print(f"Verified saved image dimensions: {img.size[0]} x {img.size[1]} pixels ({img.size[0]*img.size[1]/1e6:.1f} Megapixels)")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
