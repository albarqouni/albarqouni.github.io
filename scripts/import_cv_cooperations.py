#!/usr/bin/env python3
"""One-off import of research cooperations and funding from the PI's CV (LaTeX) into content/projects.

  * research collaborations  → content/projects/<slug>/index.md with `project_type: collaboration`
  * funded projects           → existing pages get `kind: funded`, amounts/roles from the CV, and the CV's
                                description as an "Outcomes" section; missing grants are created.
Usage: python3 scripts/import_cv_cooperations.py /path/to/CV
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PI = "shadi-albarqouni"


def latex_to_md(s):
    s = re.sub(r"(?m)^\s*%.*$", "", s)
    s = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", "", s, flags=re.S)
    s = re.sub(r"\{\\footnotesize.*?\}\s*$", "", s, flags=re.S | re.M)
    s = re.sub(r"\\printbibliography\[[^\]]*\]", "", s)
    s = re.sub(r"\\(label|ref)\{[^}]*\}", "", s)
    s = re.sub(r"\\(medskip|noindent|smallskip|bigskip|centering|newline)\b", "", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", s)
    s = re.sub(r"\\(textit|emph)\{([^}]*)\}", r"*\2*", s)
    s = re.sub(r"\\url\{([^}]*)\}", r"<\1>", s)
    s = s.replace("\\\\", "\n").replace("---", "—").replace("--", "–").replace("~", " ").replace("\\&", "&").replace("\\%", "%")
    s = re.sub(r"\$([^$]*)\$", lambda m: m.group(1).replace("\\,", " ").replace("\\sim", "~").replace("\\times", "×").replace("\\rightarrow", "→"), s)
    s = re.sub(r"\\[a-zA-Z]+\{?", "", s).replace("{", "").replace("}", "")
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def sections(text):
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    out = {}
    for chunk in re.split(r"\\subsubsection\{", text)[1:]:
        title = chunk[: chunk.index("}\n")]
        out[re.sub(r"\s+", " ", title)] = chunk[chunk.index("}\n") + 2:]
    return out


def field(chunk, name):
    m = re.search(r"\\textbf\{" + name + r"[^}]*:\}\s*(.*?)(?:\\\\|\n\\textbf|\n\\medskip|\n\n)", chunk, re.S)
    return latex_to_md(m.group(1)) if m else ""


def body_of(chunk):
    desc = re.search(r"Description and outcomes\.\}(.*?)(?:\\noindent \\textbf\{(?:Perspective|Role)|\\begin\{figure\}|\\noindent \\textbf\{Outcome|$)", chunk, re.S)
    persp = re.search(r"\\textbf\{Perspective\.\}(.*?)(?:\\begin\{figure\}|\\medskip\s*\\noindent \\textbf\{Outcome|\\noindent \\textbf\{Outcome|$)", chunk, re.S)
    role = re.search(r"\\textbf\{Role\.\}(.*?)(?:\\medskip|$)", chunk, re.S)
    md = latex_to_md(desc.group(1)) if desc else latex_to_md(chunk.split("\\medskip", 1)[-1])
    if role:
        md += "\n\n### Our role\n\n" + latex_to_md(role.group(1))
    if persp:
        md += "\n\n### Perspective\n\n" + latex_to_md(persp.group(1))
    return md


# key words in CV title → (slug, title, start, end, partners, team, themes, datasets, short summary)
COLLAB = {
    "Giant Cell Arteritis": ("gca-us-ai", "GCA-US-AI: Deep learning–based ultrasound diagnosis of Giant Cell Arteritis", "2022-01", "", ["ukb"],
                             ["sarah-schaab", "pranav-kirti", "valentin-schaefer"], ["computational-imaging", "responsible-ai"], ["gca-ultrasound"]),
    "pancreatic cancer": ("pdac-fl", "Federated foundation models for multi-center CT staging of pancreatic cancer", "2023-05", "", ["ukb", "charite", "umg", "unimelb"],
                          ["david-gaviria", "parinishtha-bhalla"], ["computational-imaging", "federated-learning"], ["pdac-ct"]),
    "ultra-low-field": ("mriqt", "MRIQT: Image-quality transfer from ultra-low-field to high-field neonatal MRI", "2024-01", "", ["ukb"],
                        ["malek-al-abed", "elodie-germani", "sebiha-demir", "anne-groteklaes", "hemmen-sabir"], ["computational-imaging", "responsible-ai"], ["neonatal-ulf-mri"]),
    "prostate cancer": ("prostate-mrf", "Deep learning for clinically significant prostate cancer in 3D mpMRI and MR Fingerprinting", "2023-01", "2024-12", ["ukb", "unimelb"],
                        ["barbara-wichtmann"], ["computational-imaging"], ["prostate-mri-mrf"]),
    "conjunctival": ("interact-cmil", "INTERACT-CMIL: Interpretable multi-task grading of conjunctival melanocytic lesions", "2024-01", "", ["ukb", "ukt", "uker"],
                     ["mert-ikinci", "martina-herwigcarl"], ["computational-imaging", "responsible-ai"], ["cmil-histopathology"]),
    "diaphragmatic hernia": ("fetal-cdh", "Deep learning for fetal diaphragmatic hernia detection in ultrasound", "2022-06", "2023-12", ["ukb"], [], ["computational-imaging"], ["fetal-us-cdh"]),
    "brain anomaly": ("feddis", "FedDis: Federated disentangled representation learning for brain anomaly detection", "2020-06", "2022-12", ["tum", "imperial"],
                      ["cosmin-bercea"], ["federated-learning", "computational-imaging"], []),
    "Large vision models": ("lvm-med", "Large vision models for robust and trustworthy medical image understanding", "2022-01", "", ["dfki"], [], ["computational-imaging", "responsible-ai"], []),
    "Digital staining": ("digital-staining", "Digital staining with confidence estimation for hematological imaging", "2020-01", "2023-12", ["tum", "siemens"], [], ["computational-imaging", "responsible-ai"], []),
    "hematology": ("computational-hematology", "Interpretable learning for rare disease classification in computational hematology", "2021-01", "2024-12", ["helmholtz-munich"], [], ["computational-imaging"], []),
    "breast cancer screening": ("fair-mammo", "Bias-aware foundation models for equitable breast cancer screening", "2024-01", "", ["lau"],
                                ["elodie-germani", "jiajun-zeng"], ["responsible-ai", "computational-imaging"], ["breast-mammography"]),
    "international guidelines": ("future-ai", "FUTURE-AI: International guidelines for trustworthy medical AI", "2021-01", "2025-12", [], [], ["responsible-ai"], []),
    "FLamby": ("flamby", "FLamby: Federated learning benchmarks for realistic healthcare settings", "2021-06", "2022-12", ["owkin", "epfl", "inria", "ip-paris", "usc", "uc-berkeley"], [], ["federated-learning"], ["flamby"]),
    "LYSTO": ("lysto", "LYSTO: Benchmark and hackathon for lymphocyte assessment", "2019-01", "2024-12", ["radboud"], [], ["computational-imaging"], ["lysto"]),
    "retinal diseases": ("affordable-retina", "Affordable deep learning for inherited and common retinal diseases", "2022-06", "", ["ukb", "bau"],
                         ["elyes-farjallah", "razieh-rezaei"], ["responsible-ai", "computational-imaging"], ["retinal-fundus"]),
    "surgical tool": ("surgical-tools", "Robust surgical tool segmentation with state-space vision models", "2024-01", "", ["kyung-hee-university"], [], ["computational-imaging"], []),
    "musculoskeletal": ("msk-fl", "Federated learning for musculoskeletal segmentation in CT", "2022-11", "", ["naist", "ukb"], ["mazen-soufi"], ["federated-learning", "computational-imaging"], ["msk-ct"]),
}
FUNDED = {"MRI-guided online adaptive radiotherapy": "radiotherapy", "Open Medical Inference": "omi", "aging estimation": "chestage",
          "cancer imaging to improve patient outcomes": "bonn-melbourne", "materials science": "eyesight-to-ai", "Joint teaching in artificial": "air-guc"}

# amounts / roles from the CV funding table
FUNDING = {
    "radiotherapy": dict(grant_number="DFG 469106425", role="co-PI", start="2022-01", end="2026-12",
                         co_pis=[{"name": "Prof. Guillaume Landry", "org": "lmu"}, {"name": "Dr. Christopher Kurz", "org": "lmu"}, {"name": "Prof. Nassir Navab", "org": "tum"}]),
    "omi": dict(role="Scientific Lead", start="2023-01", end="2027-12"),
    "chestage": dict(grant_number="DFG 525002713", role="co-PI", co_pis=[{"name": "PD Dr. Jakob Weiss", "org": "uk-freiburg"}]),
    "bonn-melbourne": dict(role="co-PI", co_pis=[{"name": "Dr. Hyun Soo Ko", "org": "unimelb"}, {"name": "A/Prof. Louise Cheng", "org": "unimelb"}]),
    "sanad": dict(grant_number="DAAD 57799851", role="PI"),
    "saai": dict(role="PI (AGYA working group)", funders=["bmbf"]),
    "eeda": dict(grant_number="DAAD 57698168", role="PI"),
    "bonn-fellowship": dict(role="PI", start="2025-01", end="2026-12", co_pis=[{"name": "Dr. Ceren Tozlu (visiting researcher)", "org": "weill-cornell"}]),
    "bacatec": dict(role="co-PI", co_pis=[{"name": "Prof. Leonidas Guibas", "org": "stanford"}, {"name": "Dr. Tolga Birdal", "org": "stanford"}, {"name": "Prof. Nassir Navab", "org": "tum"}]),
    "federated-learning": dict(role="Young Investigator Group Leader (PI)"),
}
NEW_FUNDED = {
    "eyesight-to-ai": dict(title="Eyesight to AI: Discovery of efficient corrosion modulators via predictive machine learning", acronym="Eyesight to AI",
                           summary="Helmholtz-funded cooperation with Helmholtz-Zentrum hereon applying deep learning to high-throughput corrosion screening (2021–2023).",
                           start="2021-01", end="2023-12", funders=["helmholtz"], partners=["helmholtz-zentrum-hereon", "helmholtz-munich"],
                           role="co-PI", co_pis=[{"name": "Dr. Christian Feiler", "org": "helmholtz-zentrum-hereon"}],
                           themes=["computational-imaging"]),
    "air-guc": dict(title="AI in Radiology – From Pixels to Decisions (joint teaching with GUC)", acronym="AiR-GUC",
                    summary="BMFTR-funded joint teaching seminar between the University of Bonn and the German University in Cairo (2025).",
                    start="2025-01", end="2025-12", funders=["bmbf"], partners=["guc", "uni-bonn"], role="co-PI",
                    co_pis=[{"name": "Prof. Mohammed Salem", "org": "guc"}, {"name": "Dr. Shereen Afifi", "org": "guc"}], authors=[PI, "adea-nesturi"],
                    themes=["responsible-ai"]),
    "siemens-cad-tracking": dict(title="CAD model-based detection and tracking of large objects", acronym="Siemens CAD",
                                 summary="Industry project with Siemens AG on CAD model-based detection and tracking of large objects in RGB(D) video (2017–2019).",
                                 start="2017-01", end="2019-12", funders=["siemens"], partners=["siemens", "tum"], 
                                 role="Scientific Lead (with N. Navab)", themes=["computational-imaging"]),
    "siemens-xray-dose": dict(title="Optimisation of X-ray images with respect to image quality and dose", acronym="Siemens X-ray",
                              summary="Industry project with Siemens Healthineers on learning-based X-ray image-quality and dose optimisation (2016–2019).",
                              start="2016-01", end="2019-12", funders=["siemens"], partners=["siemens", "tum"], 
                              role="Scientific Lead (with N. Navab)", themes=["computational-imaging"]),
}


def read(p):
    _, h, b = p.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(h) or {}, b


def write(p, fm, body):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n" + body.strip() + "\n", encoding="utf-8")


def main():
    cv = Path(sys.argv[1])
    secs = sections((cv / "cooperation_v1.tex").read_text())
    authors = {p.stem for p in (ROOT / "data/authors").glob("*.yaml")}
    made = 0
    for title, chunk in secs.items():
        md = body_of(chunk)
        partners_txt, collab_txt = field(chunk, "Partners"), field(chunk, "Collaborators")
        for key, (slug, ttl, start, end, partners, team, themes, datasets) in COLLAB.items():
            if key.lower() in title.lower():
                fm = {"title": ttl, "project_type": "collaboration", "summary": md.split("\n\n")[0][:300].rsplit(" ", 1)[0] + "…",
                      "date": f"{start}-01", "start": start, "end": end, "funders": [], "pis": [PI],
                      "co_pis": [{"name": n.strip(" *")} for n in re.split(r",| and ", re.sub(r"Prof\.|Dr\.|PD|med\.|mudr\.|rer\. nat\.", "", partners_txt)) if n.strip(" *") and len(n.strip()) > 3][:6],
                      "authors": [PI] + [a for a in team if a in authors], "partners": partners, "work_packages": [], "themes": themes,
                      "datasets": datasets, "tags": [], "featured": False}
                body = (f"**Partners:** {partners_txt}\n\n" if partners_txt else "") + (f"**Collaborators:** {collab_txt}\n\n" if collab_txt else "") + md
                p = ROOT / "content/projects" / slug / "index.md"
                if p.exists():
                    old, _ = read(p)
                    fm = {**fm, **{k: v for k, v in old.items() if k in ("image", "featured")}}
                write(p, fm, body)
                made += 1
        for key, slug in FUNDED.items():
            if key.lower() in title.lower():
                p = ROOT / "content/projects" / slug / "index.md"
                if p.exists():
                    fm, body = read(p)
                    if "### Outcomes (from the PI's CV)" not in body:
                        body = body.rstrip() + "\n\n### Outcomes\n\n" + md
                    write(p, fm, body)
                else:
                    NEW_FUNDED.setdefault(slug, {})["_body"] = md
    for slug, d in NEW_FUNDED.items():
        p = ROOT / "content/projects" / slug / "index.md"
        body = d.pop("_body", d["summary"])
        fm = {"title": d["title"], "project_type": "funded", "acronym": d.get("acronym", ""), "summary": d["summary"], "date": f"{d['start']}-01",
              "start": d["start"], "end": d["end"], "status": "", "funders": d["funders"], "grant_number": d.get("grant_number", ""),
              "funding_url": "", "role": d.get("role", ""), "pis": [PI], "co_pis": d.get("co_pis", []),
              "authors": d.get("authors", [PI]), "partners": d["partners"], "work_packages": [], "themes": d["themes"], "datasets": [], "tags": [], "featured": True}
        write(p, fm, body)
        made += 1
    # mark all other projects as funded + apply CV amounts/roles
    for p in (ROOT / "content/projects").glob("*/index.md"):
        fm, body = read(p)
        fm.setdefault("project_type", "funded")
        for k, v in FUNDING.get(p.parent.name, {}).items():
            fm[k] = v
        write(p, fm, body)
    print(f"projects written: {made}")


if __name__ == "__main__":
    main()
