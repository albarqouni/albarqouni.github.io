#!/usr/bin/env python3
"""Reach and impact statistics of the lab's publications, from OpenAlex → data/impact.json.

  - field-weighted citation impact (mean FWCI) and papers in the global top 10% / 1% most cited (same field, year, type)
  - international co-authorship: share of papers with authors in more than one country, partner countries, institutions
  - geographic reach: countries of the authors of works citing us
  - open-access share and UN Sustainable Development Goals
  - optional: policy-document and patent citations from Altmetric (needs ALTMETRIC_API_KEY)

Usage: python3 scripts/impact_stats.py
Environment: OPENALEX_MAILTO, OPENALEX_API_KEY (optional), ALTMETRIC_API_KEY (optional).
"""
import collections
import datetime as dt
import json
import os
import statistics
import urllib.parse

import sync_publications as sp

OUT = sp.ROOT / "data/impact.json"
FIELDS = "id,doi,authorships,cited_by_count,citation_normalized_percentile,fwci,open_access,sustainable_development_goals"


def openalex(path, **params):
    if sp.MAILTO:
        params["mailto"] = sp.MAILTO
    if sp.OPENALEX_KEY:
        params["api_key"] = sp.OPENALEX_KEY
    return sp.get_json("https://api.openalex.org/" + path + "?" + urllib.parse.urlencode(params))


def works(author):
    out, cursor = [], "*"
    while cursor:
        d = openalex("works", filter=f"authorships.author.id:{author}", select=FIELDS, cursor=cursor, **{"per-page": 200})
        out += d["results"]
        cursor = d["meta"].get("next_cursor") if d["results"] else None
    return out


def citing_countries(ids):
    """Number of citing works per author country (max over batches, so a work citing two batches is not double counted)."""
    counts = collections.Counter()
    for i in range(0, len(ids), 90):
        d = openalex("works", filter="cites:" + "|".join(ids[i:i + 90]), group_by="authorships.countries")
        for g in d["group_by"]:
            code = g["key"].rsplit("/", 1)[-1].upper()
            counts[code] = max(counts[code], g["count"])
    return counts


def altmetric(dois):
    key = os.environ.get("ALTMETRIC_API_KEY")
    if not key:
        return None
    policy = patents = papers_policy = papers_patents = 0
    for doi in dois:
        try:
            d = sp.get_json(f"https://api.altmetric.com/v1/doi/{urllib.parse.quote(doi)}?key={key}")
        except Exception:
            continue
        p, t = d.get("cited_by_policies_count", 0), d.get("cited_by_patents_count", 0)
        policy, patents = policy + p, patents + t
        papers_policy, papers_patents = papers_policy + (p > 0), papers_patents + (t > 0)
    return {"policy_mentions": policy, "papers_in_policy": papers_policy, "patent_mentions": patents, "papers_in_patents": papers_patents}


def main():
    author = sp.load_params().get("openalex_author")
    ws = works(author)
    coauthor, institutions, international = collections.Counter(), set(), 0
    for w in ws:
        countries = set()
        for a in w["authorships"]:
            countries |= set(a.get("countries") or [])
            institutions |= {i["id"] for i in a.get("institutions") or []}
        coauthor.update(countries)
        international += len(countries) > 1
    fwci = [w["fwci"] for w in ws if w.get("fwci") is not None]
    pct = [w.get("citation_normalized_percentile") or {} for w in ws]
    sdg = collections.Counter(g["display_name"] for w in ws for g in w.get("sustainable_development_goals") or [])
    cited = citing_countries([w["id"].rsplit("/", 1)[-1] for w in ws if w["cited_by_count"]])
    data = {
        "updated": dt.date.today().isoformat(),
        "source": "OpenAlex",
        "works": len(ws),
        "fwci_mean": round(sum(fwci) / len(fwci), 2) if fwci else None,
        "fwci_median": round(statistics.median(fwci), 2) if fwci else None,
        "top10": sum(1 for p in pct if p.get("is_in_top_10_percent")),
        "top1": sum(1 for p in pct if p.get("is_in_top_1_percent")),
        "international": international,
        "institutions": len(institutions),
        "open_access": sum(1 for w in ws if w["open_access"]["is_oa"]),
        "coauthor_countries": dict(coauthor.most_common()),
        "citing_countries": dict(cited.most_common()),
        "sdg": dict(sdg.most_common()),
    }
    alt = altmetric([w["doi"].replace("https://doi.org/", "") for w in ws if w.get("doi")])
    if alt:
        data["altmetric"] = alt
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"impact: {len(ws)} works · FWCI {data['fwci_mean']} · top10% {data['top10']} · "
          f"{international} international · cited from {len(cited)} countries → {OUT.relative_to(sp.ROOT)}")


if __name__ == "__main__":
    main()
