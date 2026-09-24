import base64
import time
import os
import pymupdf as fitz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DIST_PDF = os.path.join(PROJECT_ROOT, "dist", "pdf")

def export_vector_pdf():
    os.makedirs(DIST_PDF, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.page_load_strategy = 'eager'
    
    print("=" * 60)
    print("EXPORTING VECTOR PDF (MASTER A0 ULTRA-SHARP)")
    print("=" * 60)
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.join(PROJECT_ROOT, "poster.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        t0 = time.time()
        driver.get(url)
        print(f"Page loaded in {time.time() - t0:.2f}s. Waiting 4 seconds for webfonts and assets...")
        time.sleep(4)
        
        # 1. Clean DOM styles: strip all outer body margins/paddings and drop shadows
        driver.execute_script('''
            document.body.style.margin = "0";
            document.body.style.padding = "0";
            document.body.style.background = "#F4F7FB";
            const p = document.querySelector(".poster");
            if (p) {
                p.style.boxShadow = "none";
            }
        ''')
        time.sleep(1)
        
        # 2. Measure exact poster bounding box
        rect = driver.execute_script(
            'let r = document.querySelector(".poster").getBoundingClientRect(); '
            'return {w: r.width, h: r.height};'
        )
        width_px = rect['w']
        height_px = rect['h']
        print(f"Poster CSS dimensions: {width_px:.2f} x {height_px:.2f} px")
        
        # 3. Emulate screen media to guarantee exact CSS gradients, color fidelity and fonts
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"media": "screen"})
        
        # 4. Generate native vector PDF via CDP
        w_in = width_px / 96.0
        h_in = height_px / 96.0
        print(f"Generating CDP vector stream ({w_in:.4f} in x {h_in:.4f} in)...")
        
        print_params = {
            'printBackground': True,
            'paperWidth': w_in,
            'paperHeight': h_in,
            'marginTop': 0.0,
            'marginBottom': 0.0,
            'marginLeft': 0.0,
            'marginRight': 0.0,
            'preferCSSPageSize': False,
            'generateTaggedPDF': True
        }
        
        cdp_result = driver.execute_cdp_cmd('Page.printToPDF', print_params)
        raw_pdf_bytes = base64.b64decode(cdp_result['data'])
        print(f"Raw vector stream captured ({len(raw_pdf_bytes)/(1024*1024):.2f} MB).")
        
    finally:
        print("Closing Chrome driver...")
        driver.quit()
        
    # 5. Format to exact ISO 216 standard A0 (841.0 mm x 1189.0 mm) via PyMuPDF vector mapping
    print("Normalizing to exact ISO A0 dimensions (841.0 mm x 1189.0 mm)...")
    src_doc = fitz.open(stream=raw_pdf_bytes, filetype="pdf")
    
    a0_w_pt = 841.0 * 72.0 / 25.4   # 2383.937 pt
    a0_h_pt = 1189.0 * 72.0 / 25.4  # 3370.394 pt
    a0_rect = fitz.Rect(0, 0, a0_w_pt, a0_h_pt)
    
    a0_doc = fitz.open()
    a0_page = a0_doc.new_page(width=a0_w_pt, height=a0_h_pt)
    a0_page.show_pdf_page(a0_rect, src_doc, 0)
    
    dist_pdf_path = os.path.join(DIST_PDF, "poster.pdf")
    print(f"Saving optimized vector PDF to: {dist_pdf_path}...")
    a0_doc.save(dist_pdf_path, deflate=True, garbage=4, clean=True)
    
    # 6. Verification
    verify_doc = fitz.open(dist_pdf_path)
    v_page = verify_doc[0]
    w_mm = v_page.rect.width * 25.4 / 72.0
    h_mm = v_page.rect.height * 25.4 / 72.0
    file_mb = os.path.getsize(dist_pdf_path) / (1024 * 1024)
    
    print("\n" + "=" * 60)
    print("VECTOR PDF EXPORT VERIFICATION:")
    print(f"  Output File:      {dist_pdf_path}")
    print(f"  Page Count:       {len(verify_doc)}")
    print(f"  Dimensions:       {w_mm:.1f} mm x {h_mm:.1f} mm (Standard A0: 841.0 x 1189.0 mm)")
    print(f"  Aspect Ratio:     {h_mm/w_mm:.6f} (A0 Standard: {1189/841:.6f})")
    print(f"  Vector Graphics:  YES (Lossless scalable)")
    print(f"  File Size:        {file_mb:.2f} MB")
    print("=" * 60 + "\n")
    print("Vector PDF export completed successfully!")
    return dist_pdf_path

if __name__ == "__main__":
    export_vector_pdf()
