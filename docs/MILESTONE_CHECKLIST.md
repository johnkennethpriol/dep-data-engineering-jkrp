# DEP Milestone Checklist

Use this to track your progress. Milestone reviewers also use this when evaluating submissions.

---

## M0 — Problem Statement *(End of Week 1)*

> The most important milestone. Everything else builds on it.

- [ ] Problem is framed as a **specific, answerable question** (not just a topic)
- [ ] Intended audience is clearly identified
- [ ] At least one potential data source has been found and linked
- [ ] README has an initial project description in your own words
- [ ] GitHub repo is public with at least one commit

**Submission:** [Insert form link]

---

## M1 — Data Source Identified *(End of Week 5)*

- [ ] Dataset is chosen and accessible (downloaded or API confirmed working)
- [ ] Data source documented in README (name, URL, format)
- [ ] You have explored at least the first few rows and understand the structure
- [ ] `data/raw/` folder exists in the repo

**Submission:** [Insert form link]

---

## M2 — Data Ingestion Script *(End of Week 8)*

- [ ] `scripts/01_ingest.py` runs without errors
- [ ] Script fetches or loads data from the actual source
- [ ] Raw output is saved to `data/raw/`

**Submission:** [Insert form link]

---

## M3 — Clean Dataset *(End of Week 12)*

- [ ] `scripts/02_clean.py` runs without errors
- [ ] Missing values are handled (dropped, filled, or documented)
- [ ] Column data types are correct (dates as dates, numbers as numbers)
- [ ] Clean data saved to `data/processed/`
- [ ] Brief notes in README or notebook on cleaning decisions

**Submission:** [Insert form link]

---

## M4 — Initial Insights *(End of Week 16)*

- [ ] At least 3 charts exist in `notebooks/01_exploration.ipynb`
- [ ] Each chart has a title that explains what it shows
- [ ] Charts directly relate back to the problem statement
- [ ] Brief written interpretation under each chart

**Submission:** [Insert form link]

---

## M5 — Public Repo *(End of Week 20)*

- [ ] README is complete: problem statement, data source, how to run, key findings
- [ ] Folder structure matches the template (`data/`, `scripts/`, `notebooks/`, `dashboard/`)
- [ ] No unnecessary files committed (check `.gitignore`)
- [ ] Commit history is clean and readable
- [ ] `requirements.txt` is present and up to date

**Submission:** [Insert form link]

---

## M6 — Live Deployment *(End of Week 24)*

- [ ] `scripts/03_analyze.py` generates `dashboard/index.html`
- [ ] Dashboard is deployed to GitHub Pages and accessible via a public URL
- [ ] Dashboard URL is added to the README
- [ ] GitHub Actions workflow runs successfully (green checkmark)

**Submission:** [Insert form link]

---

*Questions? Ask in the community Discord or reach out to your Squad Guide.*
