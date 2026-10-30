---
title: Understanding the effects of artifacts on automated polyp detection and incorporating that knowledge via learning without forgetting
date: '2020-01-01'
draft: false
authors:
- Maxime Kayser
- roger-soberanis-mukul
- Anna-Maria Zvereva
- Peter Klare
- nassir-navab
- shadi-albarqouni
publication_types:
- preprint
publication:
  name: arXiv e-prints
venue: arxiv
doi: ''
abstract: Survival rates for colorectal cancer are higher when polyps are detected at an early stage and can be removed before they develop into malignant tumors. Automated polyp detection, which is dominated by deep learning based methods, seeks to improve early detection of polyps. However, current efforts rely heavily on the size and quality of the training datasets. The quality of these datasets often suffers from various image artifacts that affect the visibility and hence, the detection rate. In this work, we conducted a systematic analysis to gain a better understanding of how artifacts affect automated polyp detection. We look at how six different artifact classes, and their location in an image, affect the performance of a RetinaNet based polyp detection model. We found that, depending on the artifact class, they can either benefit or harm the polyp detector. For instance, bubbles are often misclassified as polyps, while specular reflections inside of a polyp region can improve
  detection capabilities. We then investigated different strategies, such as a learning without forgetting framework, to leverage artifact knowledge to improve automated polyp detection. Our results show that such models can mitigate some of the harmful effects of artifacts, but require more work to significantly improve polyp detection capabilities.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: source
  url: https://arxiv.org/abs/2002.02883
  name: Publisher
slidev: ''
hugoblox:
  ids:
    arxiv: '2002.02883'
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:XD-gHx7UXLsC
  locked: []
  citations: 29
  teaser: pdf:https://arxiv.org/pdf/2002.02883
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---
