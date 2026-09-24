import time
import os
import base64
import zlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymupdf as fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DIST_PRINT = os.path.join(PROJECT_ROOT, "dist", "print")

def set_png_dpi(png_path, dpi=600):
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

def rasterize_and_save(doc, dpi, num_strips=6):
    """Rasterizes vector PDF page into high-DPI image bands and saves PNG & TIFF."""
    os.makedirs(DIST_PRINT, exist_ok=True)
    page = doc[0]
    
    # Calculate exact pixels for standard A0 (841mm x 1189mm)
    target_width = int(round(841.0 / 25.4 * dpi))
    zoom = target_width / page.rect.width
    total_h = int(round(page.rect.height * zoom))
    mat = fitz.Matrix(zoom, zoom)
    
    print(f"\n--- Rasterizing {dpi} DPI ({target_width} x {total_h} px, {target_width*total_h/1e6:.1f} MP) ---")
    t0 = time.time()
    
    strip_h_pt = page.rect.height / num_strips
    strips = []
    for i in range(num_strips):
        y0 = i * strip_h_pt
        y1 = (i + 1) * strip_h_pt if i < num_strips - 1 else page.rect.height
        clip = fitz.Rect(0, y0, page.rect.width, y1)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        strips.append(pix)
        
    t_render = time.time() - t0
    print(f"  Rendered {num_strips} bands in {t_render:.2f}s")
    
    # Assemble into PIL Image
    t0 = time.time()
    final_img = Image.new('RGB', (target_width, total_h))
    cur_y = 0
    for s in strips:
        sim = Image.frombytes('RGB', (s.width, s.height), s.samples)
        final_img.paste(sim, (0, cur_y))
        cur_y += s.height
    print(f"  Assembled in {time.time() - t0:.2f}s")
    
    # 1. Save TIFF (Lossless LZW compression - Industry prepress standard)
    tif_name = f"poster_print_{dpi}dpi.tif"
    dist_tif_path = os.path.join(DIST_PRINT, tif_name)
    
    print(f"  Saving TIFF (LZW) to: {dist_tif_path}...")
    t0 = time.time()
    final_img.save(dist_tif_path, format="TIFF", compression="tiff_lzw", dpi=(dpi, dpi))
    tif_size_mb = os.path.getsize(dist_tif_path) / (1024 * 1024)
    print(f"  TIFF saved in {time.time() - t0:.2f}s ({tif_size_mb:.2f} MB)")
    
    # 2. Save PNG
    png_name = f"poster_print_{dpi}dpi.png"
    dist_png_path = os.path.join(DIST_PRINT, png_name)
    
    print(f"  Saving PNG to: {dist_png_path}...")
    t0 = time.time()
    final_img.save(dist_png_path, format="PNG", compress_level=4, dpi=(dpi, dpi))
    set_png_dpi(dist_png_path, dpi)
    png_size_mb = os.path.getsize(dist_png_path) / (1024 * 1024)
    print(f"  PNG saved in {time.time() - t0:.2f}s ({png_size_mb:.2f} MB)")
    
    return {
        "dpi": dpi,
        "width": target_width,
        "height": total_h,
        "megapixels": (target_width * total_h) / 1e6,
        "tif_path": dist_tif_path,
        "tif_size_mb": tif_size_mb,
        "png_path": dist_png_path,
        "png_size_mb": png_size_mb
    }

def main(dpis=[600, 800]):
    os.makedirs(DIST_PRINT, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.page_load_strategy = 'eager'
    
    print("=" * 60)
    print("PRINT MASTER EXPORT (PNG & TIFF: 600 DPI & 800 DPI)")
    print("=" * 60)
    print("Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 3000)
    
    try:
        html_file = os.path.join(PROJECT_ROOT, "poster.html")
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
        
        rect = driver.execute_script(
            'let r = document.querySelector(".poster").getBoundingClientRect(); '
            'return {w: r.width, h: r.height};'
        )
        width_px = rect['w']
        height_px = rect['h']
        print(f"Poster CSS dimensions: {width_px:.2f} x {height_px:.2f} px")
        
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"media": "screen"})
        
        w_in = width_px / 96.0
        h_in = height_px / 96.0
        print(f"Capturing vector CDP representation ({w_in:.4f} in x {h_in:.4f} in)...")
        
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
        pdf_bytes = base64.b64decode(cdp_result['data'])
        print(f"Vector data captured ({len(pdf_bytes)/(1024*1024):.2f} MB).")
        
    finally:
        print("Closing Chrome driver...")
        driver.quit()
        
    # Open vector document in PyMuPDF
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    results = []
    for dpi in dpis:
        strips = 4 if dpi <= 600 else 8
        res = rasterize_and_save(doc, dpi=dpi, num_strips=strips)
        results.append(res)
    
    print("\n" + "=" * 60)
    print("ALL PRINT ASSETS SUCCESSFULLY GENERATED IN dist/print/:")
    for r in results:
        print(f"\n  [DPI {r['dpi']}] Dimensions: {r['width']} x {r['height']} px ({r['megapixels']:.1f} MP)")
        print(f"    - PNG:  {os.path.basename(r['png_path'])} ({r['png_size_mb']:.2f} MB)")
        print(f"    - TIFF: {os.path.basename(r['tif_path'])} ({r['tif_size_mb']:.2f} MB)")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
