# NCR Air Quality and EV Fleet Growth: Measuring EVIDA's Impact (2014-Present)

## Problem Statement

I want to answer: "Does early data after the Electric Vehicle Industry Development Act (EVIDA) in 2022 show any measurable change in NCR PM2.5 air quality and fleet composition trends, and is that change significant relative to the continued growth of the overall vehicle fleet?"

My hypothesis is that EVIDA has had a positive but limited effect on air quality in the NCR. Any gains from cleaner vehicles are likely being offset by the simultaneous growth in total vehicle registrations, which means the net improvement in PM2.5 may not yet be statistically significant. If the data confirms this, the findings point to specific next actions: mandating Euro 5 emission standards for new vehicle registrations, setting binding EV fleet share targets per LGU, expanding EVIDA's charging infrastructure mandate, and introducing end-of-life vehicle policies to phase out the oldest and most polluting vehicles from the NCR fleet. If the data instead shows a meaningful improvement in PM2.5 alongside growing EV adoption, the findings would support accelerating EVIDA's implementation timeline, scaling up EV incentives, and using the NCR as a model for replication in other high-density regions in the country.

## Audience

This project is for national government agencies - specifically DOTr, DENR-EMB, and DOE - who need data-grounded evidence to evaluate whether EVIDA's current implementation pace is sufficient, and whether complementary policies are needed to achieve meaningful air quality improvements in the NCR. It is also relevant to the automotive industry for aligning product roadmaps with regulatory direction, and to businesses and LGUs planning supportive infrastructure for accelerated EV adoption.

## KPI or Key Metric

The main metric I want to track is NCR annual average PM2.5 concentration (ug/m3), measured against the share of electric and hybrid vehicles as a percentage of total registered vehicles in the NCR per year.

## Likely Data Source

I will explore the following sources. Note that data coverage varies per source - vehicle fleet data currently runs to 2023, DENR-EMB air quality baselines cover 2016-2021, and OpenAQ station data covers 2023 onward with a gap during the EVIDA transition itself (see Known Limitations below):

- DENR-EMB National Air Quality Status Reports (https://air.emb.gov.ph) - annual NCR PM2.5 averages, 2016-2021
- DENR official press releases (https://denr.gov.ph) - NCR PM2.5 averages, 2022-2023
- PSA Compendium of Philippine Environment Statistics, Table 5.8.1 (https://psa.gov.ph) - registered vehicles by fuel type, 2014-2023
- DOE / EVAP Annual EV Industry Reports - EV and hybrid registration counts, 2022-2024
- OpenAQ API (https://api.openaq.org/v3) - station-level PM2.5 readings from NCR stations, 2023-present

## Possible Final Dashboard

The dashboard should help the audience quickly see whether NCR PM2.5 levels declined after EVIDA took effect in 2022, and whether the growth in EV and hybrid vehicle share is large enough to explain any observed change - or whether total fleet growth is canceling out the gains from cleaner vehicles.

## Data Source Notes

### Air Quality

**Primary (current signal):** OpenAQ API - Ortigas station, NCR
- Sensor ID: 10253230 | Provider: Clarity (low-cost optical sensor, not a government reference monitor)
- Coverage: Aug 13, 2024-present, continuous, live as of this writing
- Why it fits: the only continuously-reporting NCR station identified after checking datetimeLast across ~70 candidate sensors

**Secondary (historical bridge):** OpenAQ API - Manila station, NCR
- Sensor ID: 6909373 | Provider: AirNow (U.S. government reference monitor)
- Coverage: Sept 6, 2023-Feb 5, 2026, then stopped reporting (confirmed dead via API metadata, not a pull error)
- Why it fits: government-grade reference data bridging the gap between DENR-EMB's pre-2022 baseline and Ortigas's live signal

**Known limitations:**
- No continuous station-level PM2.5 data exists for NCR during the EVIDA transition itself (April 2022-Sept 2023); only annual pre-period baselines (DENR-EMB) and post-2023 station data are available
- Manila and Ortigas are different instrument classes (government reference vs. low-cost optical) with different accuracy profiles; kept distinguishable by a station column rather than treated as interchangeable
- OpenAQ's /v3/sensors/{id} summary statistics were found to be unreliable for at least one sensor tested (reported mean and max did not match that sensor's own raw measurement history) and are not used anywhere in this project; all statistics are computed directly from raw records
- An earlier version of this pipeline used a different OpenAQ sensor that had stopped reporting after nine days; that sensor and its data were discarded and are not part of the current dataset

**Fallback (not yet ingested):** DENR-EMB National Air Quality Status Reports
- URL: https://air.emb.gov.ph
- Format: PDF
- Coverage: NCR annual PM2.5 averages, 2016-2021
- Why it fits: establishes the pre-EVIDA baseline that no OpenAQ station covers
- Known limitations: PDF extraction required; annual granularity only, not station-level; no coverage for the 2022-mid-2023 transition period

### Vehicle Fleet Composition

**Primary:** PSA Compendium of Philippine Environment Statistics, Table 5.8.1
- URL: https://psa.gov.ph
- Format: Excel/PDF table
- Coverage: Registered vehicles by fuel type, NCR, 2014-2023
- Why it fits: official government fleet registration data covering nearly the full study period
- Known limitations: Stops at 2023, doesn't extend to "present"

**Fallback:** DOE / EVAP Annual EV Industry Reports
- Format: PDF/report
- Coverage: EV and hybrid registration counts, 2022-2024
- Why it fits: Extends fleet composition data one year closer to present than PSA alone
- Known limitations: Narrower scope (EV/hybrid only, not full fleet breakdown)

### First Pull Path

OpenAQ: API calls via Python requests, authenticated with X-API-Key header, paginated by calendar month per sensor (deep page-offset pagination times out server-side on this API). DENR-EMB and PSA: manual download of published PDF/Excel tables, parsed with pdfplumber/pandas.

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Get a free API key from OpenAQ (https://explore.openaq.org/register) and set it in a .env file at the repo root:
   ```
   OPENAQ_API_KEY=your_key_here
   ```
3. Run the ingestion script:
   ```
   python scripts/ingest.py
   ```
   This pulls raw PM2.5 measurements from the Manila and Ortigas sensors, one calendar month at a time, and saves the untouched responses to data/raw/.
4. Run the transformation script:
   ```
   python scripts/transform.py
   ```
   This combines both raw sources, validates timestamps and values, flags but does not silently drop implausible readings, and writes the cleaned dataset plus a cleaning log to data/processed/.
