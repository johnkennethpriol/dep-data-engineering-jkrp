# Can Publicly Available Data Reveal Unusual Patterns in DPWH Flood Control Projects? (2022–2025)

## Problem Statement

I want to answer:

**"Can publicly available DPWH flood control project data reveal unusual geographic, financial, and contractor-related patterns that may indicate areas requiring further audit or investigation between 2022 and 2025?"**

My hypothesis is that while most flood control projects are distributed according to infrastructure and disaster mitigation needs, the data may reveal patterns that warrant closer examination. These may include unusually high concentrations of projects within specific provinces, repeated awards to the same contractors, or significant differences in project costs across comparable locations. Such patterns do **not** establish corruption, fraud, or wrongdoing. Instead, they provide evidence-based indicators that can help auditors, policymakers, journalists, and citizens identify projects that deserve further review. If the analysis finds no unusual concentrations or inconsistencies, it would suggest that the observed project distribution is generally consistent with available public data. If notable anomalies are identified, the findings could support stronger transparency initiatives, more detailed public reporting, and more targeted oversight by government auditing agencies.

## Audience

This project is intended for the Commission on Audit (COA), the Department of Public Works and Highways (DPWH), policymakers, local government units (LGUs), journalists, researchers, civil society organizations, and citizens interested in government transparency and infrastructure accountability. It aims to provide an objective, data-driven view of how publicly funded flood control projects are distributed across the Philippines.

## KPI or Key Metric

The primary metrics I want to track include:

* Number of completed flood control projects per province and region
* Total project cost by province and region
* Average project cost
* Number of projects awarded per contractor
* Contractor concentration ratio
* Geographic distribution of completed projects
* Project density relative to province or municipality
* Identification of statistical outliers in project allocation and cost

## Likely Data Source

I will explore the following data sources:

* DPWH Flood Control Projects Dataset (Kaggle) — https://www.kaggle.com/datasets/bwandowando/dpwh-flood-control-projects
* DPWH Project DIME Dashboard — https://www.dime.gov.ph/dashboard
* DPWH Official Website — https://www.dpwh.gov.ph
* Commission on Audit (COA) Annual Audit Reports — https://www.coa.gov.ph
* Philippine Statistics Authority (PSA) — https://psa.gov.ph (for regional and population statistics if normalization is required)

## Possible Final Dashboard

The dashboard should help users quickly identify how flood control projects are distributed across regions and provinces, which contractors receive the highest number of projects, how project costs compare geographically, and whether statistically unusual allocation patterns exist. Interactive maps, contractor rankings, regional summaries, and cost distribution charts will allow users to explore the data and identify projects or areas that may warrant further review by oversight agencies.

## Data Source Notes

### Flood Control Projects

**Primary:** DPWH Flood Control Projects Dataset (Kaggle)

* URL: https://www.kaggle.com/datasets/bwandowando/dpwh-flood-control-projects
* Format: CSV
* Coverage: Completed DPWH flood control projects from July 2022 to May 2025
* Why it fits: Provides structured project-level information including project names, locations, implementing offices, contractors, coordinates, and other metadata suitable for ETL and analytics.
* Known limitations: Covers completed projects only and relies on publicly available government records compiled into a machine-readable dataset.

**Fallback:** DPWH Project DIME Dashboard

* URL: https://www.dime.gov.ph/dashboard
* Format: Web dashboard / downloadable reports
* Coverage: Government infrastructure project monitoring and implementation status
* Why it fits: Can supplement project metadata and validate project information.
* Known limitations: Coverage and available fields may differ from the Kaggle dataset and may require manual extraction.

### Audit and Oversight Data

**Primary:** Commission on Audit (COA) Annual Audit Reports

* URL: https://www.coa.gov.ph
* Format: PDF
* Coverage: Audit findings and observations on government infrastructure projects
* Why it fits: Provides additional context for interpreting observed data patterns.
* Known limitations: Reports are document-based and require PDF extraction; audit observations may not correspond directly to every project in the dataset.

### Geographic and Demographic Data

**Primary:** Philippine Statistics Authority (PSA)

* URL: https://psa.gov.ph
* Format: CSV, Excel, PDF
* Coverage: Population and regional statistics
* Why it fits: Enables normalization of project counts and supports regional comparisons.
* Known limitations: May require joining multiple datasets and harmonizing geographic identifiers.

### First Pull Path

Download the Kaggle DPWH Flood Control Projects dataset as the primary source and ingest it into the Bronze layer. Clean and standardize project locations, contractor names, and administrative boundaries in the Silver layer. Enrich the data by joining regional information from PSA and validating selected projects against the DPWH Project DIME Dashboard. Finally, build Gold-layer analytical tables that summarize project distribution, contractor participation, regional investment patterns, and statistical outliers for visualization in an interactive dashboard.
