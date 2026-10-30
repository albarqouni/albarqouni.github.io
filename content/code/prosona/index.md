---
title: ProSona
summary: 'Code for “ProSona: Prompt-Guided Personalization for Multi-Expert Medical Image Segmentation”. Automated medical image segmentation suffers from high interobserver variability, particularly in tasks such as lung nodule delineation, where experts often disagree. Existing approaches either collapse th…'
date: '2025-11-02'
lastmod: '2025-11-10'
repository: https://github.com/albarqounilab/ProSona
homepage: ''
language: Python
stars: 1
license: ''
topics: []
code_type: research
course: ''
publications:
- elgebaly-2026-prosona
themes:
- computational-imaging
projects:
- radiotherapy
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/ProSona
  locked: []
image:
  caption: Figure from the [ProSona README](https://github.com/albarqounilab/ProSona).
  focal_point: Center
---
### About the method

From the abstract of [ProSona: Prompt-Guided Personalization for Multi-Expert Medical Image Segmentation](/publications/elgebaly-2026-prosona/):

> Automated medical image segmentation suffers from high interobserver variability, particularly in tasks such as lung nodule delineation, where experts often disagree. Existing approaches either collapse this variability into a consensus mask or rely on separate model branches for each annotator. We introduce ProSona, a two-stage framework that learns a continuous latent space of annotation styles, enabling controllable personalization via natural language prompts. A probabilistic U-Net backbone captures diverse expert hypotheses, while a prompt-guided projection mechanism navigates this latent space to generate personalized segmentations. A multi-level contrastive objective aligns textual and visual representations, promoting disentangled and interpretable expert styles. Across the LIDC-IDRI lung nodule and multi-institutional prostate MRI datasets, ProSona reduces the Generalized Energy Distance by 17 % and improves mean Dice by more than one point compared with DPersona. These results demonstrate that natural-language prompts can provide flexible, accurate, and interpretable control over personalized medical image segmentation. Our implementation is available online1https://github.com/albarqounilab/ProSona.

### Using the code

The repository README covers requirements, quick start (lidc), data, training. See [the repository on GitHub](https://github.com/albarqounilab/ProSona#readme) for step-by-step instructions.
