# TP10_DS

Data science workspace for TP10. This repository contains the project datasets, exploratory notebooks, cleaned intermediate data, and final result files used across the AoA, library-story, map, and NAPLAN workstreams.

## Repository Structure

```text
TP10_DS/
├── data/
│   ├── raw/
│   │   ├── AoA_51715_words.xlsx
│   │   ├── iteration2/story/
│   │   ├── lida_stories/lida_stories_en.json
│   │   ├── map/
│   │   ├── overview/
│   │   ├── merged_story_corpus_3class.json
│   │   ├── metadataset.csv
│   │   ├── stories_final.json
│   │   ├── story_categories_v2_raw.json
│   │   └── storyweaver_texts_cleaned.json
│   └── processed/
│       ├── iteration2/
│       ├── library_data/
│       ├── map/
│       └── overview/
├── notebooks/
│   ├── iteration2_AOA/
│   ├── iteration3_library/
│   ├── map/
│   └── overview/
└── outputs/
    ├── figures/
    └── results/
        ├── iteration2_AOA/
        └── iteration3_library/
```

## What Is In Each Area

- `data/raw/` stores original source files and should be treated as input-only.
- `data/processed/` stores cleaned intermediate datasets produced by notebooks.
- `notebooks/` stores analysis, cleaning, feature engineering, and demo notebooks.
- `outputs/figures/` stores presentation-ready figures.
- `outputs/results/` stores final handoff artifacts that are useful outside the notebook workflow.

## Notebook Guide

### `notebooks/iteration2_AOA/`

- `AOA_data.ipynb`
  - Input: `data/raw/AoA_51715_words.xlsx`
  - Outputs: cleaned AoA datasets in `data/processed/iteration2/`
- `AOA_generated_files_analysis.ipynb`
  - Compares the generated AoA candidate datasets
  - Reads from `data/processed/iteration2/`
- `AOA_feature_engineering.ipynb`
  - Builds feature tables for downstream modeling
  - Reads and writes in `data/processed/iteration2/`
- `extract_story_pdf_text.ipynb`
  - Extracts story text from `data/raw/iteration2/story/`
  - Outputs `.txt` files and a manifest to `data/processed/iteration2/`

### `notebooks/iteration3_library/`

- `lida_storyweaver_merge_analysis.ipynb`
  - Inputs: `data/raw/lida_stories/lida_stories_en.json`, `data/raw/storyweaver_texts_cleaned.json`
  - Output: `data/processed/library_data/lida_storyweaver_merge_ready.json`
- `story_category_v1_analysis.ipynb`
  - Input: `data/processed/library_data/lida_storyweaver_merge_ready.json`
  - Output: `data/processed/library_data/story_categories_v1.json`
- `story_categories_v2_clean.ipynb`
  - Input: `data/processed/library_data/story_categories_v1.json`
  - Main output: `data/processed/library_data/story_categories_v2.json`
  - Also writes cleaning logs and backups into `data/processed/library_data/`
- `lida_v2_final_candidate_merge.ipynb`
  - Inputs: `data/processed/library_data/story_categories_v2.json`, `data/raw/lida_stories/lida_stories_en.json`
  - Intermediate output: `data/processed/library_data/story_categories_final_candidate.json`
  - Final output: `outputs/results/iteration3_library/story_categories_v3.json`

### `notebooks/map/`

- `map_data_cleaning.ipynb`
  - Inputs: `data/raw/map/datadotgov_main.csv`, `data/raw/map/healthdirect_nhsd_services_directory_2025.csv`
  - Output: `data/processed/map/map_data.csv`
  - Note: geocoding may require internet access when the notebook is executed
- `map_from_map_data.ipynb`
  - Input: `data/processed/map/map_data.csv`
  - Demonstrates how the cleaned dataset can power the support-center map

### `notebooks/overview/`

- `NAPLAN_data.ipynb`
  - Input: `data/raw/overview/NAPLAN national results dataset.xlsx`
  - Output: `data/processed/overview/naplan_analysis_ready.csv`
- `NAPLAN_analysis.ipynb`
  - Input: `data/processed/overview/naplan_analysis_ready.csv`
  - Produces exploratory analysis and visual summaries

## Running The Notebooks

All notebooks were updated to locate the project root automatically, so teammates can run them from their own machines without editing hard-coded local paths.

Recommended workflow:

1. Clone the repository.
2. Create a Python environment with the notebook dependencies you need.
3. Open Jupyter Notebook or JupyterLab from anywhere inside the repository.
4. Run notebooks in workflow order so upstream processed files exist before downstream notebooks read them.

Suggested order by stream:

1. AoA: `AOA_data.ipynb` -> `AOA_generated_files_analysis.ipynb` -> `AOA_feature_engineering.ipynb`
2. Library: `lida_storyweaver_merge_analysis.ipynb` -> `story_category_v1_analysis.ipynb` -> `story_categories_v2_clean.ipynb` -> `lida_v2_final_candidate_merge.ipynb`
3. Map: `map_data_cleaning.ipynb` -> `map_from_map_data.ipynb`
4. Overview: `NAPLAN_data.ipynb` -> `NAPLAN_analysis.ipynb`

## Dependencies

The notebooks use common data-science libraries, including:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `folium`
- `openpyxl`
- Jupyter Notebook or JupyterLab

Some notebooks may also rely on standard-library modules such as `json`, `pathlib`, `re`, `csv`, `urllib`, and `subprocess`.

## Notes

- There are currently no active `.py` source files in the repository root workflow; the project logic is notebook-based.
- Several files under `outputs/results/` are final exported artifacts, while `data/processed/` should be treated as reproducible intermediate data.
- macOS `.DS_Store` files exist in the working tree and are not part of the project logic.
