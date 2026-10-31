---
title: 'K-MaT: Knowledge-Anchored Manifold Transport for Cross-Modal Prompt Learning in Medical Imaging'
date: '2026-09-27'
draft: false
authors:
- jiajun-zeng
- shadi-albarqouni
publication_types:
- paper-conference
publication:
  name: Medical Image Computing and Computer Assisted Intervention – MICCAI 2026, Lecture Notes in Computer Science
venue: miccai
doi: 10.1007/978-3-032-38062-3_28
abstract: Large-scale biomedical vision-language models (VLMs) adapted on high-end imaging (e.g., CT) often fail to transfer to frontline low-end modalities (e.g., radiography), collapsing into modality-specific shortcuts. We propose K-MaT (Knowledge-Anchored Manifold Transport), a prompt-learning framework that transfers decision structures to low-end modalities without requiring low-end training images. K-MaT factorizes prompts, anchors them to clinical text descriptions, and aligns the low-end prompt manifold to the visually-grounded high-end space using Fused Gromov-Wasserstein optimal transport. We evaluate K-MaT on four cross-modal benchmarks, including dermoscopy, mammography to ultrasound, and CT to chest X-ray. K-MaT achieves state-of-the-art results, improving the average harmonic mean of accuracy to 44.1% (from BiomedCoOp’s 42.0%) and macro-F1 to 36.2%. Notably, on the challenging …
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2603.06340
slidev: /talks/kmat/
hugoblox:
  ids:
    doi: 10.1007/978-3-032-38062-3_28
    arxiv: '2603.06340'
sync:
  source: legacy
  openalex: W7134243786
  scholar: CPuApzoAAAAJ:PaBasH6fAo0C
  locked:
  - date
  - publication
  - publication_types
  - title
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 0302-9743
  - 1611-3349
  source_id: S106296714
  source_type: book series
  citations: 1
  teaser: pdf:https://arxiv.org/pdf/2603.06340
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---
