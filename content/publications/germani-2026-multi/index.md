---
title: When multi-institutional dataset aggregation masks shortcut-like behavior in Foundation Models for medical imaging
date: '2026-09-01'
draft: false
authors:
- elodie-germani
- Fatima Zeineddine
- charbel-mourad
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: Medical Image Analysis
venue: media
doi: 10.1016/j.media.2026.104258
abstract: Foundation Models are increasingly used in medical imaging, yet their behavior under severe domain heterogeneity remains poorly understood. We study pretrained image encoders as feature extractors for mammography classification across ten datasets spanning diverse acquisition pipelines, populations, and geographic regions. Classifiers trained on aggregated heterogeneous data exhibit dataset-dependent failure modes, with substantial disparities in error rates, confidence, and calibration across datasets. At the representation level, dataset identity is readily recoverable from Foundation Model embeddings, whereas clinical labels are less separable, indicating a low task-to-dataset signal ratio. These findings are consistent with shortcut-like behavior, where dataset-associated structure is more accessible to downstream classifiers than transferable clinical signal. Sequential vector decomposition further shows that much of the linearly recoverable task signal lies in dataset-aligned
  subspaces, limiting the task information that remains after suppressing dataset-related directions. An exploratory metadata-guided analysis identifies age-associated, label-dependent shifts in predicted probabilities, suggesting cohort-level candidate mediators of dataset-dependent behavior. Dataset-adversarial training, worst-group optimization, and balanced fine-tuning reduce some dataset-level disparities, but robustness gains often come at the expense of aggregate performance. Together, our results show that classifiers trained on Foundation Model features from aggregated datasets can exhibit shortcut-like behavior, highlighting the need for evaluation protocols and representation-learning objectives that explicitly assess and reduce entanglement between spurious and clinical signals.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: true
links:
- type: pdf
  url: https://inserm.hal.science/inserm-05727793
slidev: /talks/mammography/
hugoblox:
  ids:
    doi: 10.1016/j.media.2026.104258
sync:
  source: legacy
  openalex: W7203971661
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1361-8415
  - 1361-8423
  - 1361-8431
  source_id: S116571295
  source_type: journal
  citations: 1
image:
  caption: ''
  focal_point: Smart
---
