---
title: Uncertainty-based graph convolutional networks for organ segmentation refinement
date: '2020-04-01'
draft: false
authors:
- roger-soberanis-mukul
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: To appear in the International Conference in Medical Imaging with Deep Learning, 2020
venue: midl
doi: ''
abstract: Organ segmentation is an important pre-processing step in many computer assisted intervention and diagnosis methods. In recent years, CNNs have dominated the state of the art in this task. Organ segmentation scenarios present a challenging environment for these methods due to high variability in shape and similarity with background. This leads to the generation of false negative and false positive regions in the output segmentation. In this context, the uncertainty analysis of the model can provide us with useful information about potentially misclassified elements. In this work we propose a method based on uncertainty analysis and graph convolutional networks as a post-processing step for segmentation. For this, we employ the uncertainty levels of the CNN to formulate a semi-supervised graph learning problem that is solved by training a GCN on the low uncertainty elements. Finally, we evaluate the full graph on the trained GCN to get the refined segmentation. We test our framework
  in refining the output of pancreas and spleen segmentation models. We show that the framework can increase the average dice score in 1% and 2% respectively for these problems. Finally, we discuss the results and current limitations of the model that lead to future work in this research direction
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
  url: https://arxiv.org/abs/1906.02191
slidev: ''
hugoblox: {}
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
---
