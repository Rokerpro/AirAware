# Hackathon Challenge Brief

**Status: UPDATED from the official PDF "Veritas AI International High School Hackathon 2026: Project Briefs" (22 pages, `highschoolhackathon.org`).** Sections 3, 4.3 (Climate), 5, 6 and 7 of the PDF are summarised below. The official brief overrides everything in `plans/`. The copy of the PDF in `docs/` is truncated at page 8, so the text below comes from the pasted pages 9-22.

Event: Veritas AI International High School Hackathon 2026, a virtual 48-hour AI build. Hacking starts Sat Nov 14, 12:00 AM ET. Submissions close **Sun Nov 15, 11:59 PM ET**. No kickoff call and nothing to attend live. Teams have 1-3 high-school students and everyone listed must have contributed. Our team: two students (beginner level in ML).

Organizers give no technical help during the event (debugging, errors, model choice). Submission problems only: contact@veritasai.com. If an upload fails at the deadline, email links to the code and write-up right away.

Results: shortlisted students and finalists are emailed Wed Nov 18. Finalists present live at the Award Ceremony, Sat Nov 21, 11:00 AM ET.

## Track
**AI + Climate.** Challenge: "Build an AI tool that helps a community, a city or an energy system measure, predict or reduce its climate impact."

Suggested project we are following: **4.3.2 Next-day air quality forecast** (Intermediate, time series; OpenAQ with a free API key, and Open-Meteo; Google Colab, pandas, scikit-learn). Goal in the brief: "Forecast tomorrow's average fine particle pollution (PM2.5) for one city, so schools and families know when to limit time outdoors."

Climate track requirements:
- Focus on one location or region (Kathmandu).
- Train on earlier dates, test on later ones. Never shuffle days together.
- Compare with the persistence baseline: "tomorrow will be the same as today."
- Explain what decision the prediction supports and who makes it.

Backup if OpenAQ has no usable Kathmandu history: the brief allows Open-Meteo's air-quality API (no key), but its values are model estimates, not measurements, so say so in the write-up. Second backup: MonsoonRain (heavy rain tomorrow for a Nepal location, which fits 4.3.4 "Your own idea"). Official advice: if data does not load within about 30 minutes, switch dataset or idea.

## Problem
Kathmandu has serious air pollution (winter smog, burning season), and apps like IQAir and AQICN already show readings and forecasts. What is missing is a check of whether a small local model, trained on real Kathmandu monitor data, beats the persistence baseline and the global CAMS forecast for this valley, plus a clear early warning tied to a real decision.

One-sentence version: help Kathmandu schools and residents plan outdoor activity by taking recent PM2.5 and weather readings and returning tomorrow's predicted daily-average PM2.5, plus an early warning per monitored neighbourhood and a plain-language precaution.

## Target users
- Primary: school staff deciding "Should schools hold outdoor PE/assembly tomorrow?" (this is the specific user and moment the write-up and demo must name).
- Secondary: Kathmandu residents planning outdoor activity, especially sensitive groups.
- Output in English and Nepali.

## What every project must show (PDF section 3)
The write-up and demo must answer four questions:
1. **Who is it for?** One specific user and the moment they reach for the tool.
2. **What goes in, and what comes out?** A real input producing a result.
3. **Does it beat a simple baseline?** Report the baseline score next to the model score.
4. **Where does it fail?** At least one wrong example and why.

All results must come from test data the model did not see in training.

## Baseline steps for 4.3.2 (from the brief)
1. Register for a free OpenAQ API key. Choose one monitoring station with at least a year of mostly complete PM2.5 readings.
2. Convert hourly readings to daily averages.
3. Add daily weather for the same location from Open-Meteo's historical weather API, especially wind speed and rainfall.
4. Baseline: tomorrow equals today. Then train a regression model on today's PM2.5 and weather.
5. Test on the most recent months and report the mean absolute error (MAE) for the baseline and the model.

Our plan extends this to several stations plus the CAMS baseline. If only one or two stations qualify, the single-station version above is exactly what the brief asks for.

## Make it your own (required)
Following the suggested steps only gives a working baseline, which "will land toward the lower end of the range". Reviewers compare teams that started from the same project and score each on what it added: its own user, data or question, and how well it tested the result. We must say what we added in the write-up and on the form. Our additions:
- **Own user or setting:** school staff in Kathmandu, with a warning designed for them (bilingual precaution, one alert card per neighbourhood).
- **Own data:** local Kathmandu monitor data from OpenAQ, with Open-Meteo/CAMS as a comparison.
- **Own question:** focus on the worst days. The brief suggests a daily-average threshold of **35 μg/m3 (US EPA 24-hour standard)**: decide how to balance missed warnings against false alarms, and explain why. Also investigate what drives pollution in Kathmandu (season, wind, burning).

## Climate judging note
"In this track, judges pay extra attention to a fair comparison with a simple forecast, a clear link between your prediction and a decision someone could make, and a test period your model never saw. Teams that build a small project tied to a real place usually score better than teams that tackle the whole planet."

## Required deliverables (PDF section 5)
One person submits for the whole team through the submission form. We can resubmit as often as we like and the latest version is judged. Submit a first version a few hours before the deadline.

| Item | Required | Details |
|---|---|---|
| Code | Yes | Google Colab notebook or GitHub repo, viewable by anyone with the link. Save the notebook with outputs visible. |
| Write-up | Yes | About one page, using the template below. Google Doc ("anyone with the link can view"), the GitHub README, or an uploaded PDF/Word file. |
| Demo video | Optional, recommended (we plan one) | Up to 2 minutes. Unlisted YouTube or Google Drive ("anyone with the link can view"). |
| Team details | Yes | Track, plus every member's name, email and school. |
| Credits | Yes | Every dataset, pretrained model, tutorial and AI tool, with links. |

The submission is complete once it includes working links to both code and write-up. Before submitting: open every link in a private/incognito window, and double-check names and emails.

### Write-up template
```
# Project name
**Track:** Climate
**Team:** names
# The problem            Who has this problem, why it matters (2-3 sentences)
# What we built          What goes in, what comes out, how someone would use it
# What we added          Suggested project 4.3.2, and what we added (own user, data or question)
# How it works           Data: which dataset, how many examples, how cleaned. Model: what and why
# Results                Baseline scored X. Our model scored Y on held-out test data. Where it fails and why
# What we'd do next      One or two concrete next steps
# Sources                Datasets, pretrained models, tutorials, AI tools, with links
```

### Demo video structure (about 2 minutes, screen recording with voice-over is enough)
| Part | Length | Show |
|---|---|---|
| The problem | ~15 s | Who it is for and why it matters |
| The demo | ~60 s | A real input going in and the result coming out |
| How it works | ~30 s | Data, model, comparison with the baseline |
| Next steps | ~15 s | One limitation and what we'd do next |

### Suggested schedule
- First 2 hours: track and idea picked, data loading in the notebook.
- Saturday evening: baseline and first model work end to end.
- Sunday midday: one measured improvement made, demo runs start to finish.
- 2 hours before the deadline: write-up done, video uploaded, project submitted.

## Constraints and rules (PDF section 2)
- Time: all project work happens between Sat Nov 14 12:00 AM ET and Sun Nov 15 11:59 PM ET. Learning tools, starter notebooks and browsing datasets beforehand are fine, but a project built before the hackathon cannot be extended. Stop new features about 6 hours before the deadline.
- AI/ML must do the project's main job.
- Allowed: public datasets, pretrained models, AI APIs (e.g. the Gemini free tier), open-source libraries, tutorial code, coding assistants and chatbots, if everything is cited and the team understands and can explain every part. Any public dataset is allowed if its licence is checked and it is cited with a link.
- Not allowed: submitting someone else's project as our own (disqualification). No personal information without permission; public or synthetic data only.
- One project per team, one track per project. Judges only see what was submitted before the deadline.
- Disclaimers: the brief requires the prototype/not-advice line for health and finance projects. AirAware gives health-related precautions, so include "This project is a prototype and is not medical advice." in the write-up, and keep "Prototype, not health advice." in the demo.
- Honest results: report the results we actually got, including weak ones. No minimum accuracy is required.
- Free tools only. We do not need to train our own model; pretrained models and AI APIs are fine, and judges focus on what we build around them.
- Data (our choices): OpenAQ v3 (needs a free API key, returns 401 without one; Kathmandu station history is not yet verified and is the main project risk) and Open-Meteo weather and air quality (no key; its air-quality values are CAMS model output, not monitors).
- Technology: Google Colab, pandas, scikit-learn, Gradio. Simple, explainable models. If Colab is blocked, use GitHub.
- Never commit API keys (e.g. the OpenAQ key); use environment variables or Colab secrets.

## Judging criteria (PDF section 6)
Round 1: the Veritas AI team reviews every complete submission blind (no names or schools). Judges score every track on the same four criteria:

| Criterion | What judges look for | How we show it |
|---|---|---|
| Technical quality | Project works, approach is sound, tested fairly | Compare with a baseline, report results on unseen test data, show where it fails |
| Impact | Tackles a real problem for real people | Explain who it helps (Kathmandu schools) and what would change for them |
| Creativity | Fresh approach, not a repeated tutorial | Apply a known technique to an unusual dataset, question or user group (local monitors, school decision, bilingual warning) |
| Clarity | A judge understands it in two minutes | Clear demo, concise write-up, one main takeaway |

"If your results look too good to be true, test data has usually leaked into training. Judges score an honest, modest result higher than an unexplained high one."

Note: highschoolhackathon.org/judges.html lists a different point breakdown (Round 1 technical execution 30, originality 20, impact and track fit 20, testing and honesty 15, communication 15; finals demo 30, technical depth 30, impact 20, Q&A 20; final rank 70% finals, 30% Round 1). The PDF's four criteria are the official ones for the brief, but the finals weighting is a reminder that both teammates must be able to explain everything in live Q&A.

Our own working priorities (from `CLAUDE.md`), in order: correctness, working end-to-end product, measurable AI performance, user experience, presentation quality.

## Proposed solution
AirAware: a Kathmandu next-day PM2.5 forecast with an early-warning layer.
- Target: tomorrow's **daily-average PM2.5 (μg/m3)** per station, as the brief specifies.
- Data: OpenAQ station readings (hourly, averaged to daily) plus Open-Meteo weather, cleaned with pandas. Features: today's PM2.5, 3-day average, temperature, wind speed, rainfall, humidity, month.
- Models: baseline "tomorrow = today", then linear regression, then Random Forest. Second baseline: the CAMS forecast from Open-Meteo (model output, not ground truth). Split by time, test on the most recent months.
- Warning layer: warn when predicted daily-average PM2.5 exceeds **35 μg/m3** (US EPA 24-hour standard, the threshold the brief suggests). Show the standard AQI band as extra context. One alert card per station, labelled by area, with no interpolation between stations. Balance missed warnings against false alarms and explain the choice.
- Demo: Gradio app where the user picks a day and sees the forecast, the warning and a bilingual precaution, labelled "prototype, not health advice".
- Fallback: if OpenAQ has only 1-2 usable stations, drop the neighbourhood cards and keep a city-level warning (this matches the brief's one-station baseline). If OpenAQ has no usable history, use Open-Meteo air quality (say it is model output) or switch to MonsoonRain.
- Interface details: see `docs/API_CONTRACT.md`.

## Measurable success criteria
No results exist yet, so these are targets to measure, not claims.
- The model's MAE on a time-based test set (most recent months) beats "tomorrow = today". Report the actual difference either way.
- Compare against the CAMS forecast and report the answer, including if the local model loses.
- Warning quality on days above 35 μg/m3: recall and precision as raw counts (e.g. "7 of 9 caught"), compared against both baselines, with the missed-vs-false-alarm trade-off explained.
- Error broken down by station and by season or month, including the high-pollution months, with at least one missed spike shown as the "where it fails" example.
- The demo runs end to end without fixes, a first submission goes in a few hours early, and the checklist (code link, write-up, video, names/emails/schools, credits, private-window link check) is complete before the deadline.

## FAQ points worth remembering (PDF section 7)
- Suggested projects are optional starting points; judges score each project in one track only.
- No technical help from organizers. No minimum accuracy.
- List everyone who worked on the project on the form; awards and certificates go to those listed.
- Judges only see what was submitted before the deadline, but we can keep working afterwards.
