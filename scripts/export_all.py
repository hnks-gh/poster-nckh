import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

def run():
    print("=" * 60)
    print("MASTER EXPORT PIPELINE: ALL POSTERS & FORMATS")
    print(f"Project Root: {PROJECT_ROOT}")
    print("=" * 60)
    
    t_start = time.time()
    
    # 1. Master Vector PDF (Exact ISO A0)
    print("\n[1/4] Exporting Vector PDF -> dist/pdf/poster.pdf...")
    import export_pdf
    export_pdf.export_vector_pdf()
    
    # 2. Print posters (PNG & TIFF: 600 DPI & 800 DPI)
    print("\n[2/4] Exporting Print Posters -> dist/print/ (PNG & TIFF at 600 & 800 DPI)...")
    import export_image
    export_image.main()
    
    # 3. Online poster formats (PNG 300 DPI, WebP, HEIF)
    print("\n[3/4] Exporting Online Formats -> dist/online/ (.png, .webp, .heif)...")
    import export_image_online
    export_image_online.main()
    
    # 4. Eureka poster
    print("\n[4/4] Exporting Eureka Poster -> dist/eureka/poster-eureka.png...")
    import export_eureka
    export_eureka.main()
    
    t_total = time.time() - t_start
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETED SUCCESSFULLY in {t_total:.2f} seconds!")
    print(f"All artifacts organized in: {os.path.join(PROJECT_ROOT, 'dist')}")
    print("=" * 60)

if __name__ == "__main__":
    run()
