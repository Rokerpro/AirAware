# Hackathon Challenge Brief

**Status: DRAFT.** Filled in from `plans/AirAware Plan.md` and `CLAUDE.md`. The official track brief is released at kickoff and overrides anything here. Items marked **(TBD)** must be copied from or checked against the official brief.

Event: Veritas AI International High School Hackathon 2026, a virtual 48-hour AI build. Kickoff Nov 14, 12:00 AM ET. Submission deadline Sun Nov 15, 11:59 PM ET. Team: two high-school students (beginner level in ML).

## Track
Climate (planned). **(TBD)** Confirm AirAware fits the official Climate brief at kickoff. Backup: MonsoonRain (predict heavy rain tomorrow for a Nepal location), which uses the same pipeline and costs about an hour to switch to. Second backup: BhashaBridge.

## Problem
Kathmandu has serious air pollution (winter smog, burning season), and apps like IQAir and AQICN already show readings and forecasts. What is missing is a check of whether a small local model, trained on real Kathmandu monitor data, beats the global CAMS forecast for this valley, plus a clear early warning tied to a real decision.

One-sentence version: help Kathmandu residents plan outdoor activity by taking recent air-quality and weather readings and returning tomorrow's predicted AQI, plus an early warning per monitored neighbourhood, with a plain-language precaution.

## Target users
- Primary: school staff deciding "Should schools hold outdoor PE/assembly tomorrow?"
- Secondary: Kathmandu residents planning outdoor activity, especially sensitive groups.
- Output in English and Nepali.

## Required deliverables
Official list **(TBD)**. Per the handout as understood so far:
- Public code link (Colab or GitHub), tested while logged out
- Write-up from the handout template (problem, approach, results vs. baseline, what failed)
- Demo video of at most 2 minutes (unlisted YouTube or Drive)
- All team member names
- Citations for every dataset, model, code source and AI tool used

What we plan to build for this: a Colab notebook with a data pipeline, baseline, linear regression and Random Forest, a warning layer using standard AQI bands with one alert card per station, and a Gradio demo.

## Constraints
- Time: 48 hours. Stop new features about 6 hours before the deadline. Do not build before kickoff (only learning tools, browsing datasets and checking that data loads).
- Data: public or synthetic only. Planned sources:
  - OpenAQ v3 (Kathmandu monitors). Needs a free API key, and returns 401 without one. Station history is not yet verified; this is the main project risk.
  - Open-Meteo weather and air-quality history (no key). Its air-quality values are CAMS model output, not monitors, so use them as a baseline, not ground truth.
- Technology: Google Colab, pandas, scikit-learn, Gradio. Simple, explainable models; never train from scratch without a strong reason.
- Budget: free tools and free-tier APIs only. **(TBD)** Check the brief for any compute or API limits.
- Rules:
  - Cite every dataset, model, code source and AI tool.
  - Check model performance across groups (stations, seasons) and report real results, including failures.
  - Health outputs must be labelled "prototype, not advice".
  - Both teammates must be able to explain everything.
  - Never commit API keys (e.g. the OpenAQ key); use environment variables or Colab secrets.
  - Split by time, never randomly, to prevent leakage.

## Judging criteria
**(TBD)** Copy the official criteria from the brief at kickoff. Until then, our own priorities (from `CLAUDE.md`), in order:
1. Correctness
2. Working end-to-end product
3. Measurable AI performance
4. User experience
5. Presentation quality

## Proposed solution
AirAware: a Kathmandu next-day AQI forecast with an early-warning layer.
- Data: OpenAQ station readings plus Open-Meteo weather, cleaned with pandas. Features: yesterday's AQI, 3-day average, temperature, wind, humidity, month.
- Models: baseline "tomorrow = today", then linear regression, then Random Forest. Second baseline: the CAMS forecast.
- Warning layer: convert each station's predicted AQI to a standard AQI band and warn at "Unhealthy for Sensitive Groups" or worse. One alert card per station, labelled by area, with no interpolation between stations.
- Demo: Gradio app where the user picks a day and sees the forecast, the warning and a bilingual precaution, labelled "prototype, not health advice".
- Fallback: if OpenAQ has only 1-2 usable stations, drop the neighbourhood cards and keep a city-level warning. If OpenAQ has no usable history, switch to MonsoonRain.
- Interface details: see `docs/API_CONTRACT.md`.

## Measurable success criteria
No results exist yet, so these are targets to measure, not claims.
- The model's MAE on a time-based test set beats "tomorrow = today". Report the actual difference either way.
- Compare against the CAMS forecast and report the answer, including if the local model loses.
- Warning quality: recall and precision on the unhealthy days, as raw counts (e.g. "7 of 9 caught"), compared against both baselines.
- Error broken down by station and by season or month, including the high-pollution months, with the missed spikes shown.
- The demo runs end to end without fixes, and the submission checklist is complete before the deadline.
