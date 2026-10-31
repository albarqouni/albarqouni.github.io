---
title: 'Unsupervised anomaly detection in full-head CT for emergency triage'
project_type: collaboration
acronym: deepc Head CT
summary: Collaboration with the Munich radiology-AI company deepc on unsupervised anomaly detection in volumetric head CT — prioritising emergency scans for any pathology, fractures included, without labelled examples of every disease.
date: '2021-01-01'
start: 2021-01
end: 2022-12
status: ''
funders: []
grant_number: ''
funding_url: ''
role: Academic Lead
pis:
- shadi-albarqouni
co_pis:
- name: Dr. Mehmet Yigitsoy
  org: deepc
authors:
- shadi-albarqouni
- abhijeet-parida
- daniel-rueckert
partners:
- deepc
- tum
work_packages: []
themes:
- computational-imaging
datasets: []
tags:
- anomaly detection
- head CT
- emergency radiology
featured: false
---
In the emergency room, head CT scans must be read and prioritised quickly — and the findings range from bleeds to fractures. Supervised detectors need labelled examples of every pathology; unsupervised anomaly detection (UAD) instead learns what normal anatomy looks like and flags everything else, an inexpensive way to bring triage to the clinical workflow. Most UAD work, however, addressed 2D slices of brain MRI rather than volumetric CT.

### What we did

- **UAD for volumetric head CT.** We compared two widely used reconstruction-based baselines on full 3D head CT, and improved their reconstruction quality with two recent computer-vision contributions — raising anomaly-detection AUROC from 0.70 to 0.77 for one baseline.
- **Keep the skull.** Testing on skull-stripped and unstripped volumes showed that leaving the skull in lets the model detect fractures too — to our knowledge the first comparison of this kind.
- **Open labels and code.** Supplementary labels for the public CQ500 head-CT dataset and the [code](https://github.com/pederismo/CTFSH) were released to support further research.

### Our role

Academic lead and supervision, together with Daniel Rueckert (TU Munich) and Mehmet Yigitsoy and Abhijeet Parida (deepc GmbH).
