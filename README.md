# PAPI Governance Scientific Poster & Research Space

> **Research Title:** *From Retrospective Benchmarking to Anticipatory Policy: A Data-Driven Framework for Governance Indexing and Forecasting Using the Viet Nam Provincial Governance and Public Administration Performance Index (PAPI)*  
> **Project ID:** `XHNV.17`  
> **Author:** Hoang Ngoc Kim Son  
> **Supervisor:** Assoc. Prof. Luu Quoc Dat  
> **Institution:** VNU University of Economics and Business & Vietnam National University, Hanoi

---

## 📁 Project Directory Structure

```text
poster-nckh/
├── dist/                              # Compiled Distribution Artifacts
│   ├── pdf/                           # Master Vector PDF (Exact ISO A0 841x1189mm)
│   │   └── poster.pdf
│   ├── print/                         # Ultra-High-Resolution Print Images
│   │   ├── poster_print_600dpi.png    # 600 DPI PNG (19,866 x 28,072 px, ~558 MP)
│   │   ├── poster_print_800dpi.png    # 800 DPI PNG (26,488 x 37,429 px, ~991 MP)
│   │   ├── poster_print_600dpi.tif    # 600 DPI TIFF (LZW Lossless, 138 MB)
│   │   └── poster_print_800dpi.tif    # 800 DPI TIFF (LZW Lossless, 216 MB)
│   ├── online/                        # Multi-format Web & Social Media Distribution
│   │   ├── poster_online.png          # 300 DPI Lossless PNG (4,756 x 7,720 px, 4.80 MB)
│   │   ├── poster_online.webp         # WebP text-preset (4,756 x 7,720 px, 1.77 MB)
│   │   ├── poster_online.avif         # AV1 4:4:4 full chroma (4,756 x 7,720 px, 1.15 MB)
│   │   ├── poster_online.heif         # Apple HEIF container (4,756 x 7,720 px, 1.15 MB)
│   │   ├── poster_social.webp         # 2048px Lanczos WebP for social feeds (641 KB)
│   │   └── poster_social.jpg          # 2048px Universal 4:4:4 JPEG for Facebook/LinkedIn (1.85 MB)
│   └── eureka/                        # Euréka 2026 Poster Competition
│       └── poster-eureka.png          # 300 DPI PNG (4,224 x 6,864 px, 8:13 Ratio)
│
├── scripts/                           # Production Automation & Export Pipeline
│   ├── export_all.py                  # Master batch pipeline (orchestrates all exports)
│   ├── export_pdf.py                  # Generates borderless, normalized ISO A0 Vector PDF
│   ├── export_image.py                # Tiled band rasterizer for 600 & 800 DPI PNG / TIFF
│   ├── export_image_online.py         # Full-page online poster capture (PNG, WebP, HEIF)
│   ├── export_eureka.py               # Element capture for Euréka format
│   └── legacy/                        # Legacy Node/Puppeteer export scripts
│
├── figure/                            # Research Plots & Visualizations
│   ├── forecasting/                   # Time-series, TFT, AutoGluon diagnostics
│   ├── ranking/                       # MCDM consensus, rank stability, distribution
│   └── weighting/                     # Hierarchical CRITIC heatmaps & radars
├── logo/                              # University & Institutional Logos (VNU, UEB)
├── table/                             # Numerical Tables, CSVs, and LaTeX Snippets
├── codebook/                          # Province and Indicator Metadata Dictionaries
│
├── index.html                         # Interactive Web Viewer (GitHub Pages entry)
├── poster.html                        # Master A0 Print Canvas (CSS Grid, Gold & Navy theme)
├── poster_online.html                 # Optimized Online Viewing Canvas
├── poster-eureka.html                 # Euréka 2026 Poster Layout (8:13 aspect ratio)
│
├── main.tex                           # Full Research Paper (XeLaTeX)
├── main.bib                           # Comprehensive Academic Bibliography
├── export_all.py                      # Root Convenience Entry Point
└── README.md                          # Documentation & Usage Guide
```

---

## 🚀 How to Export Posters

To re-export all formats across the entire workspace in one single command:

```powershell
python export_all.py
```

Or execute individual export modules:

| Task | Command | Target Outputs |
| :--- | :--- | :--- |
| **Export All** | `python export_all.py` | Updates all PDFs and images in `dist/` |
| **Vector PDF** | `python scripts/export_pdf.py` | `dist/pdf/poster.pdf` |
| **Print Images** | `python scripts/export_image.py` | `dist/print/*.png`, `dist/print/*.tif` (600 & 800 DPI) |
| **Online Formats** | `python scripts/export_image_online.py` | `dist/online/*.png`, `*.webp`, `*.heif` |
| **Euréka Poster** | `python scripts/export_eureka.py` | `dist/eureka/poster-eureka.png` |

---

## 🖨️ Printing & Production Guidelines

When submitting the poster to commercial printing houses:
1. **First Choice:** [dist/pdf/poster.pdf](dist/pdf/poster.pdf)  
   *(100% vector typography and geometries. Machine RIP renders at native hardware resolution: 2400/4800 DPI without pixelation).*
2. **Prepress TIFF:** [dist/print/poster_print_800dpi.tif](dist/print/poster_print_800dpi.tif)  
   *(Industry-standard LZW lossless compressed 800 DPI continuous-tone raster image).*
3. **Reference PNG:** [dist/print/poster_print_800dpi.png](dist/print/poster_print_800dpi.png) or [dist/print/poster_print_600dpi.png](dist/print/poster_print_600dpi.png)  
   *(For fast preview, cross-checking, and digital distribution).*
