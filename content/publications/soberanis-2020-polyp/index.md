---
title: Polyp-artifact relationship analysis using graph inductive learned representations
date: '2020-01-01'
draft: false
authors:
- roger-soberanis-mukul
- shadi-albarqouni
- nassir-navab
publication_types:
- preprint
publication:
  name: arXiv preprint arXiv:2009.07109
venue: arxiv
doi: ''
abstract: The diagnosis process of colorectal cancer mainly focuses on the localization and characterization of abnormal growths in the colon tissue known as polyps. Despite recent advances in deep object localization, the localization of polyps remains challenging due to the similarities between tissues, and the high level of artifacts. Recent studies have shown the negative impact of the presence of artifacts in the polyp detection task, and have started to take them into account within the training process. However, the use of prior knowledge related to the spatial interaction of polyps and artifacts has not yet been considered. In this work, we incorporate artifact knowledge in a post-processing step. Our method models this task as an inductive graph representation learning problem, and is composed of training and inference steps. Detected bounding boxes around polyps and artifacts are considered as nodes connected by a defined criterion. The training step generates a node classifier
  with ground truth bounding boxes. In inference, we use this classifier to analyze a second graph, generated from artifact and polyp predictions given by region proposal networks. We evaluate how the choices in the connectivity and artifacts affect the performance of our method and show that it has the potential to reduce the false positives in the results of a region proposal network.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: source
  url: https://arxiv.org/abs/2009.07109
  name: Publisher
slidev: ''
hugoblox:
  ids:
    arxiv: '2009.07109'
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:lmc2jWPfTJgC
  locked: []
  teaser: pdf:https://arxiv.org/pdf/2009.07109
  citations: 3
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---
