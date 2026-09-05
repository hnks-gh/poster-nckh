**Role:** You are an elite, world-class graphic designer and academic layout expert. You specialize in designing award-winning, high-impact academic posters for international scientific conferences and exhibitions.

**Task:** Design and generate the complete layout, structure, and styling code (or highly detailed exact visual specifications) for an A0 Portrait academic poster based on a provided scientific paper. The goal is to win the "Best Poster Award". The design must be extremely professional, visually stunning, academically rigorous, and structurally optimized for readability from 1 meter distance. 

**Working Directory Context:**
All assets are located in: C:\Users\hoang\Downloads\poster

**1. Dimensional & Canvas Specifications**
- **Size:** A0 Portrait (841 mm width x 1189 mm height).
- **Resolution:** 300 DPI standard minimum for printing.
- **Layout Model:** A clean, spacious 2-column grid for the main content body.
- **Color Palette:** 
  - Primary: Deep Navy Blue (#003366) to match Vietnam National University (VNU) branding.
  - Accent: Elegant Gold (#D4AF37) for section headers, highlights, and borders.
  - Background: Crisp White (#FFFFFF) or Ultra-light Gray (#F8F9FA).
  - Text: Dark Charcoal (#2B2B2B) for high-contrast, comfortable reading.
- **Typography:** Modern Sans-Serif (e.g., Inter, Roboto, or Open Sans). Use heavy weights for headings and large, legible sizes for body text (minimum 30pt for body).

**2. Poster Structure & Content Requirements**

**SECTION A: HEADER (Top 10%)**
- **Left Side (Logos):** Arrange the following images in a horizontal row from left to right, properly aligned and scaled:
  1. logo/vnu-logo.png
  2. logo/logo-vnu-caption.png
  3. logo/ueb-logo.png
  4. logo/ueb-logo-caption.png
- **Right Side (Prize Name):** Vertically centered, bold, elegant typography, split into exactly these 3 lines:
  - Line 1: 2026 POSTER PRIZE
  - Line 2: STUDENT SCIENTIFIC RESEARCH
  - Line 3: VIETNAM NATIONAL UNIVERSITY, HANOI

**SECTION B: GENERAL INFORMATION (Next 10%)**
- **Paper Title:** "From Retrospective Benchmarking to Anticipatory Policy: A Data Driven Framework for Governance Indexing and Forecasting Using the Viet Nam Provincial Governance and Public Administration Performance Index (PAPI)" (Center-aligned, massive font size, Navy Blue).
- **Metadata Bar:** A beautifully styled banner or ribbon underneath the title containing:
  - Project ID: XHNV.88
  - Author: Hoang Ngoc Kim Son
  - Supervisor: Assoc. Prof. Luu Quoc Dat

**SECTION C: MAIN CONTENT (Next 70% - Split into 2 Equal Columns)**
**CRITICAL: The paper is dense. Do not use walls of text. Extract only core messages, use bullet points, and maximize the use of high-quality assets from the figure/ and table/ folders.**

Column 1 (Left):
- **1. Introduction:**
  - **Problem Statement:** Current subnational governance indexing frameworks (e.g., PAPI, PCI) are predominantly *retrospective* and rely on equal-weighting defaults. This limits their capacity to provide forward-looking signals and early warnings for proactive policymaking.
  - **Research Objectives:**
    1. Develop an integrated subnational governance framework combining **Two-Level Hierarchical CRITIC Weighting**, **MCDM Consensus Ranking**, and **Ensemble Machine Learning Forecasting**.
    2. Validate the temporal stability and robustness of data-driven weights over a 14-year period (2011–2024).
    3. Generate probabilistic projections for 2025 to operationalize an institutional Early Warning System for subnational governance.

- **2. Methods and Data:**
  - **Data Description:** Balanced panel dataset from PAPI (2011–2024) across Viet Nam's 63 provinces.
    - *2011–2017 Period:* 6 criteria (C01–C06), comprising 21 sub-criteria.
    - *2018–2024 Period:* Expanded to 8 criteria (adding C07: Environmental Governance & C08: E-Governance), totaling 29 sub-criteria (SC11–SC83).
  - **Three-Tier Methodological Framework:**
    ```mermaid
    graph TD
        A[PAPI Longitudinal Panel 2011-2024] --> B[Tier 1: Two-Level Hierarchical CRITIC Weighting]
        B --> C[Tier 2: Multi-Method MCDM Consensus Ranking]
        C --> D[Tier 3: AutoGluon Stacked Ensemble Forecasting for 2025]
    ```
    1. **Hierarchical CRITIC Weighting:**
       - *Level 1:* Computes sub-criterion weights within each of the 8 governance criteria.
       - *Level 2:* Derives weights across the 8 criteria, capturing data-driven contrast intensity and correlation patterns.
    2. **Consensus MCDM Ranking:** Integrates five distinct decision algorithms representing different mathematical paradigms: TOPSIS, VIKOR, PROMETHEE II, COPRAS, and EDAS.
    3. **Stacked Ensemble Forecasting:** Stacked pipeline of ten diverse base learners (combining statistical, tabular ML, deep learning, and foundation models like Chronos) optimized via AutoGluon.

- **3. Weighting & Ranking Results:**
  - *Objective: Present the data-driven weighting hierarchy and demonstrate consensus across distinct ranking algorithms.*
  - **Visual Elements:**
    - *Left Visual:* Heatmap of sub-criterion weights over time (`figure/weighting/weight-heatmap.png`) or radar chart (`figure/weighting/weight-radar.png`).
    - *Right Visual:* Time-averaged criterion weights table and rank agreement coefficients.
  - **Table 1: Mean CRITIC Criterion Weights (2011–2024)** (Source: [criterion_weight_table.tex](file:///c:/Users/hoang/Downloads/poster/table/weighting/criterion_weight_table.tex)):
    
    | Criterion | Mean Weight | Volatility (CV) | Informational Role & Interpretation |
    | :--- | :---: | :---: | :--- |
    | **C06: Public Service Delivery** | **16.76%** | 0.2379 | Primary differentiator across provinces. |
    | **C05: Public Administrative Procedures** | **14.59%** | 0.2125 | Highly stable administrative priority. |
    | C01: Local Participation | 14.21% | 0.1486 | Lowest weight variance (most consistent). |
    | C04: Control of Corruption | 13.64% | 0.3168 | Highest temporal weight volatility. |
    | C03: Vertical Accountability | 13.22% | 0.2110 | Moderate information value. |
    | C02: Transparency | 12.46% | 0.2295 | Lowest weight among long-standing criteria. |
    | C07: Environmental Governance (since 2018) | 8.14% | 1.0516 | Graceful integration of index expansion. |
    | C08: E-Governance (since 2018) | 6.99% | 1.0715 | Graceful integration of index expansion. |

  - **Key Findings & Validation:**
    - **Temporal Stability:** Sliding 5-year window analysis yields a very low mean distance ($\bar{\text{RMSD}} = 0.0107 \pm 0.0046$), proving that empirical governance weights remain highly stable over time.
    - **Methodological Concordance:** Spearman rank correlation across the 5 MCDM methods averages **$\bar{\rho} = 0.96$**, confirming that provincial orderings are robust and independent of mathematical choices. **PROMETHEE II** is selected as the optimal ranking function.

Column 2 (Right):
- **4. Forecasting Results (2025):**
  - *Objective: Highlight the accuracy of the stacked ensemble model and analyze the projected spatial distribution of subnational governance in 2025.*
  - **Visual Elements:**
    - *Top:* Horizontal sequence of Metric Callout Cards.
    - *Center:* National choropleth map of projected 2025 PROMETHEE II scores (`figure/forecasting/forecast_papi_2025.png`).
    - *Bottom:* Model family weight distribution bar chart (`figure/forecasting/ensemble_model_diversity.png`) or MASE validation leaderboard.
  - **Metric Callout Cards:**
    - `Card 1:` **Ensemble MASE: 0.6411** *(Well below the 1.0 naive baseline threshold)*
    - `Card 2:` **Improvement vs. TFT: +14.12%** *(TFT was the best single baseline at MASE = 0.7316)*
    - `Card 3:` **Improvement vs. Naive: +86.0%** *(Naive baseline MASE = 1.1924)*
  - **Spatial 2025 Projections:**
    - *Choropleth Map:* Darker regions represent stronger projected governance performance.
    - **Leading Cluster:** Concentrated in the Northern and North-Central coastal regions. **Quang Ninh (1.000)** maintains the lead, followed by **Thai Nguyen (0.862)**, **Bac Ninh (0.855)**, and **Ha Tinh (0.819)**, indicating potential regional knowledge spillovers.
    - **Lagging Cluster:** Observed in the Central Highlands and peripheral areas of the Mekong Delta. **Phu Yen (0.000)** records the lowest projected score, followed by **Kien Giang (0.020)**, **Kon Tum (0.037)**, and **Dak Nong (0.060)**.
    - **Metropolitan Centers:** **Hanoi (0.477)** and **Ho Chi Minh City (0.302)** score moderately, reflecting the administrative challenges of scaling public services under rapid urbanization.

- **5. Discussion:**
  - *Objective: Translate predictive signals into actionable policy interventions, targeting the specific sub-criteria driving projected declines.*
  - **Visual Elements:**
    - *Left Visual:* Bar chart of provinces with the steepest projected declines in composite PAPI scores (`figure/forecasting/composite_decline_bar.png`).
    - *Right Visual:* 5-pillar Policy Response Matrix linking projected contractions to concrete policy actions.
  - **Decline Analysis Findings:**
    - **29 out of 63 provinces** are projected to experience governance contractions in 2025.
    - **Ca Mau** faces the steepest contraction (~50%), followed by **Dak Lak** (~48%), **Quang Ngai** (41.12%), and **Binh Thuan** (32.55%).
    - *Systemic Bottlenecks:* Recurring contractions in **Internet Access (SC82)** and **Civic Knowledge (SC11)** signal systemic issues in digital administration and grassroots civic engagement.
  - **5-Pillar Policy Response Matrix:**
    
    | Policy Pillar | Target Sub-Criteria | Regulatory & Operational Response |
    | :--- | :--- | :--- |
    | **1. Digital Access & E-Governance** | SC82 (Internet Access)<br>SC81 (E-Gov Portals) | - Amend the Universal Service Obligation funding to ringfence capital for "last-mile" broadband in lagging provinces.<br>- Align performance indicators with the National Digital Transformation Program (**Decision 749/QD-TTg**).<br>- Deploy commune-level digital navigators (Lao Cai model). |
    | **2. Civic Engagement & Grassroots Democracy** | SC11 (Civic Knowledge)<br>SC14 (Voluntary Contrib.) | - Mandate commune-level deliberative forums as prescribed by **Law 10/2022/QH15** and **Decree 59/2023/ND-CP**.<br>- Establish Village Development Funds with transparent community auditing structures to rebuild voluntary co-production. |
    | **3. Accountability & Anti-Corruption** | SC23 (Communal Budget Trans.)<br>SC42 (Control of Corruption) | - Standardize commune budget execution reports via templates from the Ministry of Finance.<br>- Deploy targeted audits via the **State Audit of Vietnam (SAV)** in high-risk provinces.<br>- Implement mandatory e-procurement platforms at the district level. |
    | **4. Environmental & Resource Governance** | SC73 (Water Quality)<br>SC71 (Env. Protection) | - Formulate an inter-provincial water quality compact across Mekong Delta provinces to address jurisdictional fragmentation.<br>- Recapitalize forest stewardship payments (**Decree 156/2018/ND-CP** & **Decree 91/2024/ND-CP**) in Central Highlands (Dak Lak, Phu Yen). |
    | **5. Tiered Governance Compact (TGC)** | Composite Scores | - Establish the **Tiered Governance Compact (TGC)**:<br>  *   *Top-Quartile Provinces:* Enhanced fiscal and administrative autonomy, reduced compliance checks.<br>  *   *Bottom-Quartile/Declining Provinces:* Trigger central support mechanisms and capacity reinforcement programs. |

- **6. Conclusion:**
  - **Academic Contribution:** Bridges static multi-criteria ranking (MCDM) with dynamic temporal machine learning forecasting, defining a methodology for "Anticipatory Governance" in developing economies.
  - **Policy Value:** Transitions subnational governance evaluations from retrospective benchmarking to proactive, one-year-ahead early-warning interventions.
  - **Reproducibility:** Code repositories and processed datasets are published as open-source assets.

**SECTION D: FOOTER (Bottom 10%)**
- A solid Navy Blue (#003366) bar spanning the entire width at the bottom.
- Text in pure White (#FFFFFF).
- **Contact Information:** Centered or elegantly spaced:
  - Contact: Hoang Ngoc Kim Son
  - Tel: 0985825656
  - Email: sonhoang.nk@outlook.com

**Execution Instructions for the Agent:**
1. Do not hallucinate or extract blurry images from the PDF; strictly link to the high-quality assets in the provided logo/, figure/, and table/ directories.
2. Balance the white space. Do not clutter. A winning poster breathes.
3. Apply the Gold (#D4AF37) color to all Section Numbers and Section Titles (e.g., "1. Introduction").
4. Output the result in the format you are best at (e.g., a complete LaTeX tikzposter source code file, a complete HTML/CSS printable grid, or an exhaustive design specification document ready for print production). 

Ensure the final output reflects the prestige of the Vietnam National University and the absolute highest standards of international academic research as long as poster industrial designate!