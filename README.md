# Personio Outbound: from 30 companies to a ready-to-send campaign

An outbound campaign for Personio, the HR software company. It starts from a raw list of 30 companies and ends with qualified target accounts, enriched contacts in a CRM and a 3-step email sequence.

I first built this with a team at the Clay Club Berlin GTM hackathon (June 2026, 90 minutes, Clay + HubSpot + Salesforge through Claude). This repo is my solo rebuild afterwards, done step by step so every decision is written down.

## The brief

Act as Personio's GTM team. You get 30 companies with only a name, domain, industry, country and headcount. Find who's worth contacting, enrich them, put them in the CRM and write the campaign.

## Step 1: Qualify 

`scripts/filter_icp.py` applies four rules and writes every removed company with its reason to `data/removed.csv`.

| Rule | Why |
|---|---|
| 50–500 employees | The brief's target window. My own research put Personio's sweet spot wider (roughly 100–2,000), but the brief focused on smaller mid-market teams. |
| Germany, Austria or Switzerland | Personio's core market. Most of its customers are in Germany. |
| Not an HR software company | SmartHR, BambooHR, Keka, Recruitee, Factorial and Haufe sell HR software themselves. They're competitors, not buyers. |
| Not already a Personio customer | Four companies in the list were already customers. Nothing in the data said so; they had to be found. |

**Why these rules:** The obvious filters (size, region) removed the easy cases. The rule that mattered most was the last one. Urban Sports Club, HomeToGo, Flaconi and Scout24 looked like perfect targets on paper, but each was already using Personio: one has an official case study, two run their careers pages on Personio's job platform. Emailing a current customer as if they were a prospect is the fastest way to look careless, so checking for this comes before any outreach.

**Result: 30 companies → 17 targets.** See `data/targets.csv`.

## Step 2: Enrich in Clay

For the 17 targets:
- Detected the current HR tool. The brief asked to keep only companies with no HRIS or a legacy one. The dataset had this column empty, so this check still needed to run.
- Finded the Head of People or HR lead.
- Finded and verified their work email.



## Step 3: Organize in HubSpot

- Imported companies and contacts.
- Tagged each company by fit.


## Step 4: The sequence

Three emails to the Head of People sent.

## What I learned

The hard part of outbound isn't building the workflow, it's deciding who is worth contacting. The four hidden customers were the real test in this brief: a list that looks clean can still be wrong.

## Files

- `data/companies.csv`: the 30 companies from the brief (company data only)
- `scripts/filter_icp.py`: the qualification rules
- `data/targets.csv`: the 17 companies that passed
- `data/removed.csv`: the 13 that didn't, and why
