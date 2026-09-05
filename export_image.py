import time
import os
import base64
import zlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import fitz  # PyMuPDF
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def set_png_dpi(png_path, dpi=600):
    """Embeds 600 DPI pHYs chunk into the PNG file."""
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
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'eager'
    
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.abspath("poster.html")
        url = f"file:///{html_file.replace(os.sep, '/')}"
        print(f"Loading URL: {url}")
        
        driver.get(url)
        print("Waiting 4 seconds for fonts, gradients, and images to render...")
        time.sleep(4)
        
        # Prepare layout cleanly for exact bounding box capture
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
        
        # Measure poster dimensions
        rect = driver.execute_script(
            'let r = document.querySelector(".poster").getBoundingClientRect(); '
            'return {w: r.width, h: r.height};'
        )
        width_px = rect['w']
        height_px = rect['h']
        ratio = height_px / width_px
        a0_ratio = 1189.0 / 841.0
        print(f"Poster CSS dimensions: {width_px:.2f} x {height_px:.2f} px")
        print(f"Aspect ratio H/W: {ratio:.6f} (A0 standard: {a0_ratio:.6f}, diff: {abs(ratio - a0_ratio):.6f})")
        
        # Emulate screen media to ensure colors, gradients, and typography render in fidelity
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"media": "screen"})
        
        # Convert CSS px (96 px per inch) to inches for vector PDF generation
        w_in = width_px / 96.0
        h_in = height_px / 96.0
        
        print(f"Exporting vector page representation via CDP ({w_in:.4f} in x {h_in:.4f} in)...")
        print_params = {
            'printBackground': True,
            'paperWidth': w_in,
            'paperHeight': h_in,
            'marginTop': 0.0,
            'marginBottom': 0.0,
            'marginLeft': 0.0,
            'marginRight': 0.0,
            'preferCSSPageSize': False
        }
        
        cdp_result = driver.execute_cdp_cmd('Page.printToPDF', print_params)
        pdf_bytes = base64.b64decode(cdp_result['data'])
        print(f"Vector data captured ({len(pdf_bytes)/(1024*1024):.2f} MB).")
        
    finally:
        print("Closing Chrome driver...")
        driver.quit()
        
    # Render at 600 DPI using PyMuPDF high-performance rasterizer
    # Standard A0: 841 mm = 33.1102 inches -> at 600 DPI = 19,866 pixels width
    #              1189 mm = 46.8110 inches -> at 600 DPI = 28,087 pixels height
    print("Rasterizing to 600 DPI image via PyMuPDF...")
    t0 = time.time()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    
    target_width = 19866
    zoom = target_width / page.rect.width
    mat = fitz.Matrix(zoom, zoom)
    
    pix = page.get_pixmap(matrix=mat, alpha=False)
    t1 = time.time()
    print(f"Pixmap rendered in {t1 - t0:.2f} seconds!")
    print(f"Rendered dimensions: {pix.width} x {pix.height} pixels")
    
    output_path = os.path.abspath("poster_print.png")
    print(f"Saving high-resolution print image to: {output_path}...")
    pix.save(output_path)
    
    # Set 600 DPI metadata chunk in the PNG file
    set_png_dpi(output_path, 600)
    
    # Verification
    img = Image.open(output_path)
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    megapixels = (img.size[0] * img.size[1]) / 1e6
    dpi_info = img.info.get('dpi')
    
    print("\n" + "="*60)
    print("PRINT IMAGE EXPORT VERIFICATION:")
    print(f"  Output File:      {output_path}")
    print(f"  Pixel Dimensions: {img.size[0]} x {img.size[1]} px")
    print(f"  Resolution:       {megapixels:.1f} Megapixels")
    print(f"  Embedded DPI:     {dpi_info}")
    print(f"  Print Size (600DPI): {img.size[0]/600*25.4:.1f} mm x {img.size[1]/600*25.4:.1f} mm (Standard A0: 841.0 x 1189.0 mm)")
    print(f"  Aspect Ratio:     {img.size[1]/img.size[0]:.6f} (A0 standard: {1189/841:.6f})")
    print(f"  File Size:        {file_size_mb:.2f} MB")
    print("="*60 + "\n")
    print("Export completed successfully!")

if __name__ == "__main__":
    main()
