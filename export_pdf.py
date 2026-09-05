import base64
import time
import os
import fitz  # PyMuPDF
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'eager'
    
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Set window size larger than poster width
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.abspath("poster.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        start_time = time.time()
        driver.get(url)
        print(f"Page loaded in {time.time() - start_time:.2f} seconds.")
        
        print("Waiting 4 seconds for rendering...")
        time.sleep(4)
        
        print("Exporting to PDF via Chrome DevTools Protocol (CDP)...")
        # paperWidth and paperHeight are in inches.
        # A0 size: 841mm x 1189mm -> 33.11 x 46.81 inches
        print_params = {
            'printBackground': True,
            'paperWidth': 33.11,
            'paperHeight': 46.81,
            'marginTop': 0.0,
            'marginBottom': 0.0,
            'marginLeft': 0.0,
            'marginRight': 0.0
        }
        
        cdp_result = driver.execute_cdp_cmd('Page.printToPDF', print_params)
        pdf_bytes = base64.b64decode(cdp_result['data'])
        
        output_path = os.path.abspath("poster.pdf")
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
            
        print(f"Successfully wrote PDF file to: {output_path}")
        
        # Verify the generated PDF using PyMuPDF
        print("Verifying PDF properties...")
        doc = fitz.open(output_path)
        print(f"Page count: {len(doc)}")
        for i, page in enumerate(doc):
            w_mm = page.rect.width * 25.4 / 72
            h_mm = page.rect.height * 25.4 / 72
            print(f"  Page {i} dimensions: {w_mm:.1f} mm x {h_mm:.1f} mm")
        
        if len(doc) == 1:
            print("Verification PASSED: Single page A0 PDF generated correctly.")
        else:
            print("Warning: PDF contains more than one page.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
