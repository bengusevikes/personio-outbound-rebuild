"""
Filter the 30-company hackathon list down to Personio's target accounts.

Input:  data/companies.csv   (30 companies: name, domain, industry, country, employees)
Output: data/targets.csv     (companies that pass every rule)
        data/removed.csv     (companies that failed, with the reason for each)

Run it from the repo folder:  python3 scripts/filter_icp.py
"""

import csv

# --- The rules -------------------------------------------------------------

# Rule 1: size. The hackathon brief set the target window at 50-500 employees.
MIN_EMPLOYEES = 50
MAX_EMPLOYEES = 500

# Rule 2: geography. Personio's core market is Germany, Austria and Switzerland.
DACH = {"DE", "AT", "CH"}

# Rule 3: competitors. Companies that sell HR software are rivals, not buyers.
# Matched on keywords in the industry column.
COMPETITOR_KEYWORDS = ["hr software", "hr & payroll", "hr & compliance", "recruiting software"]

# Rule 4: already a customer. These four were hidden in the list.
# Each was confirmed by public evidence (checked June 2026).
EXISTING_PERSONIO_CUSTOMERS = {
    "Urban Sports Club GmbH": "Official Personio customer case study",
    "HomeToGo GmbH": "Careers page runs on hometogo.jobs.personio.com",
    "Flaconi GmbH": "Careers page runs on flaconi.jobs.personio.de",
    "Scout24 SE": "Listed as a Personio customer",
}


def reasons_to_remove(company):
    """Return every rule this company breaks. An empty list means it's a target."""
    reasons = []
    employees = int(company["employees"])

    if employees < MIN_EMPLOYEES:
        reasons.append(f"Too small ({employees} employees)")
    if employees > MAX_EMPLOYEES:
        reasons.append(f"Too large ({employees} employees)")
    if company["country"] not in DACH:
        reasons.append(f"Outside DACH ({company['country']})")
    if any(k in company["industry"].lower() for k in COMPETITOR_KEYWORDS):
        reasons.append(f"Competitor ({company['industry']})")
    if company["company_name"] in EXISTING_PERSONIO_CUSTOMERS:
        reasons.append("Already uses Personio: " + EXISTING_PERSONIO_CUSTOMERS[company["company_name"]])

    return reasons


# --- Run it ----------------------------------------------------------------

with open("data/companies.csv", newline="") as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    companies = list(reader)

targets, removed = [], []
for company in companies:
    reasons = reasons_to_remove(company)
    if reasons:
        removed.append({**company, "reason": "; ".join(reasons)})
    else:
        targets.append(company)

with open("data/targets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(targets)

with open("data/removed.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns + ["reason"])
    writer.writeheader()
    writer.writerows(removed)

print(f"{len(companies)} companies in, {len(targets)} targets, {len(removed)} removed\n")
for c in removed:
    print(f"  x {c['company_name']:<26} {c['reason']}")
