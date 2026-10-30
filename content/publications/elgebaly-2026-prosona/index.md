---
title: 'ProSona: Prompt-Guided Personalization for Multi-Expert Medical Image Segmentation'
date: '2026-01-01'
draft: false
authors:
- aya-elgebaly
- Nikolaos Delopoulos
- Juliane Hörner‐Rieber
- Carolin Rippke
- Sebastian Klüter
- Luca Boldrini
- Lorenzo Placidi
- Riccardo Dal Bello
- Nicolaus H. Andratschke
- Michael Baumgartl
- Claus Belka
- christopher-kurz
- guillaume-landry
- shadi-albarqouni
publication_types:
- paper-conference
publication:
  name: 2026 IEEE 23rd International Symposium on Biomedical Imaging (ISBI)
venue: isbi
doi: 10.1109/isbi61048.2026.11515434
abstract: Automated medical image segmentation suffers from high interobserver variability, particularly in tasks such as lung nodule delineation, where experts often disagree. Existing approaches either collapse this variability into a consensus mask or rely on separate model branches for each annotator. We introduce ProSona, a two-stage framework that learns a continuous latent space of annotation styles, enabling controllable personalization via natural language prompts. A probabilistic U-Net backbone captures diverse expert hypotheses, while a prompt-guided projection mechanism navigates this latent space to generate personalized segmentations. A multi-level contrastive objective aligns textual and visual representations, promoting disentangled and interpretable expert styles. Across the LIDC-IDRI lung nodule and multi-institutional prostate MRI datasets, ProSona reduces the Generalized Energy Distance by 17 % and improves mean Dice by more than one point compared with DPersona. These
  results demonstrate that natural-language prompts can provide flexible, accurate, and interpretable control over personalized medical image segmentation. Our implementation is available online1https://github.com/albarqounilab/ProSona.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2511.08046
slidev: ''
hugoblox:
  ids:
    doi: 10.1109/isbi61048.2026.11515434
    arxiv: '2511.08046'
sync:
  source: legacy
  openalex: W4416190284
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn: []
  source_id: S4363605129
  source_type: conference
  citations: 0
  teaser: pdf:https://arxiv.org/pdf/2511.08046
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---
