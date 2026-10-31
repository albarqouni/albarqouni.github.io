---
title: An Uncertainty-Driven GCN Refinement Strategy for Organ Segmentation
date: '2020-12-01'
draft: false
authors:
- roger-soberanis-mukul
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: 'Journal of Machine Learning for Biomedical Imaging (MELBA) — Special Issue: MIDL 2020'
venue: melba
doi: 10.59275/j.melba.2020-8e2b
abstract: Organ segmentation in CT volumes is an important pre-processing step in many computer assisted intervention and diagnosis methods. In recent years, convolutional neural networks have dominated the state of the art in this task. However, since this problem presents a challenging environment due to high variability in the organ’s shape and similarity between tissues, the generation of false negative and false positive regions in the output segmentation is a common issue. Recent works have shown that the uncertainty analysis of the model can provide us with useful information about potential errors in the segmentation. In this context, we proposed a segmentation refinement method based on uncertainty analysis and graph convolutional networks. We employ the uncertainty levels of the convolutional network in a particular input volume to formulate a semi-supervised graph learning problem that is solved by training a graph convolutional network. To test our method we refine the initial
  output of a 2D U-Net. We validate our framework with the NIH pancreas dataset and the spleen dataset of the medical segmentation decathlon. We show that our method outperforms the state-of-the-art CRF refinement method by improving the dice score by 1% for the pancreas and 2% for spleen, with respect to the original U-Net’s prediction. Finally, we perform a sensitivity analysis on the parameters of our proposal and discuss the applicability to other CNN architectures, the results, and current limitations of the model for future work in this research direction. For reproducibility purposes, we make our code publicly available at https://github.com/rodsom22/gcn_refinement
themes:
- computational-imaging
projects:
- uncertainty
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Graph Convolutional Networks
- Uncertainty
- Prior Knowledge
featured: false
links:
- type: pdf
  url: https://arxiv.org/abs/2012.03352v1
hugoblox:
  ids:
    doi: 10.59275/j.melba.2020-8e2b
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked:
  - publication
  - publication_types
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 2766-905X
  source_id: ''
  source_type: ''
  merged:
  - mukul-2020-uncertainty
image:
  caption: ''
  focal_point: Smart
---
