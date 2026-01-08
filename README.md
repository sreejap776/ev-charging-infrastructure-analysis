# ⚡ Washington State EV Infrastructure Gap Analysis

> *Where the demand is, but the plugs aren't.*

A data-driven analysis identifying **Charging Deserts** — high-EV areas with limited public charging infrastructure — to guide strategic infrastructure investment decisions.

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| **Total BEVs in Washington** | 165,000+ vehicles |
| **Total Public Charging Ports** | 4,800+ ports |
| **Statewide EV/Port Ratio** | 34:1 (34 vehicles per port) |
| **Critical Desert ZIPs** | 80+ ZIP codes with **ZERO** public charging |
| **EVs in Deserts** | 6,500+ vehicles with no nearby public options |

### 🔴 Top 5 Critical Investment Zones

| ZIP | City | County | EVs | Ports | EV/Port Ratio |
|-----|------|--------|-----|-------|---------------|
| 98329 | Gig Harbor | Pierce | 302 | 0 | ∞ |
| 98606 | Brush Prairie | Clark | 313 | 0 | ∞ |
| 98236 | Clinton | Island | 275 | 0 | ∞ |
| 98333 | Fox Island | Pierce | 232 | 0 | ∞ |
| 98077 | Woodinville | Snohomish | 84 | 0 | ∞ |

> *These ZIPs have 50+ BEVs each and literally zero public charging infrastructure.*

---

## 🎯 The Opportunity Metric

We calculate an **EV-to-Port Ratio** for each ZIP code:

```
EV_to_Port_Ratio = Total_BEVs / Total_Public_Ports
```

| Ratio | Interpretation | Priority |
|-------|----------------|----------|
| **∞** | No ports exist | 🔴 CRITICAL |
| **>100** | Severe undersupply | 🔴 High |
| **50-100** | Moderate undersupply | 🟡 Medium |
| **<50** | Adequate supply | 🟢 Low |

---

## 📍 County-Level Insights

| County | BEVs | Ports | EV/Port Ratio |
|--------|------|-------|---------------|
| King | 58,000+ | 1,800+ | 32:1 |
| Snohomish | 21,000+ | 500+ | 42:1 |
| Pierce | 18,000+ | 400+ | 45:1 |
| Clark | 11,000+ | 250+ | 44:1 |
| Thurston | 5,000+ | 100+ | 50:1 |

*King County leads in EV adoption but also has the most infrastructure. Rural counties show the highest gaps.*

---

## Project Structure

```
ev-charging-desert-analysis/
├── data/
│   ├── ev_population.csv              # EV registration data (BEV only)
│   └── charging_stations.csv          # Public charging station locations
├── output/
│   ├── charging_desert_map.html       # Interactive strategic map
│   └── top_50_investment_zones.csv    # Exported target list
├── ev_charging_desert_analysis.ipynb  # Main analysis notebook
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch Jupyter

```bash
jupyter notebook ev_charging_desert_analysis.ipynb
```

### 3. Run All Cells

Execute the notebook cells sequentially to generate:
- Strategic map visualization
- Top 50 target ZIP codes
- County-level analysis
- Business recommendations

---

## 📂 Data Sources

| Dataset | Source | Key Columns |
|---------|--------|-------------|
| EV Population | [data.wa.gov](https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2) - WA State DOL | Postal Code, County, EV Type, Make, Year |
| Charging Stations | [afdc.energy.gov](https://afdc.energy.gov/data_download) - NREL | ZIP, Access Code, Level 2 Count, DC Fast Count |

---

## 📋 Outputs

### 1. Interactive Map (`output/charging_desert_map.html`)
- Bubble size = EV demand
- Color = Opportunity level (Red = Desert, Green = Served)
- Hover for detailed metrics per ZIP

### 2. Top 50 Investment Targets (`output/top_50_investment_zones.csv`)
Exported CSV with ZIPs sorted by opportunity metric.

---

## 💡 Strategic Recommendations

| Priority | Action | Impact |
|----------|--------|--------|
| **1** | Install DC Fast in Top 10 ZIPs | Immediate coverage for 2,000+ EVs |
| **2** | Deploy Level 2 in Critical Deserts | 80+ ZIPs with zero infrastructure |
| **3** | Urban Corridor Strategy | Workplace charging in high-density areas |
| **4** | Rural Hub Model | Strategic placement along highway corridors |

---

## ⚙️ Business Logic

1. **BEV Only**: Analysis filters for Battery Electric Vehicles (BEV) only — PHEV owners can charge at home
2. **Public Stations Only**: Private/residential stations excluded — analyzing public infrastructure gaps
3. **Washington Focus**: High EV adoption market, representative of national trends

---

## 👤 Author

**Sreeja Penke** — Data Analyst | January 2026

---

## 📄 License

Internal use for infrastructure planning purposes.
