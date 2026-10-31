---
title: Semi-Supervised Few-Shot Learning with Prototypical Random Walks
date: '2021-01-01'
draft: false
authors:
- Ahmed Ayyad
- Yuchen Li
- Raden Muaz
- shadi-albarqouni
- Mohamed Elhoseiny
publication_types:
- paper-conference
publication:
  name: AAAI Workshop on Meta Learning
venue: ''
doi: 10.48550/arxiv.1903.02164
abstract: Recent progress has shown that few-shot learning can be improved with access to unlabelled data, known as semi-supervised few-shot learning(SS-FSL). We introduce an SS-FSL approach, dubbed as Prototypical Random Walk Networks(PRWN), built on top of Prototypical Networks (PN). We develop a random walk semi-supervised loss that enables the network to learn representations that are compact and well-separated. Our work is related to the very recent development on graph-based approaches for few-shot learning. However, we show that compact and well-separated class representations can be achieved by modeling our prototypical random walk notion without needing additional graph-NN parameters or requiring a transductive setting where collective test set is provided. Our model outperforms prior art in most benchmarks with significant improvements in some cases. For example, in a mini-Imagenet 5-shot classification task, we obtain 69.65% accuracy to the 64.59% state-of-the-art. Our model,
  trained with 40% of the data as labelled, compares competitively against fully supervised prototypical networks, trained on 100% of the labels, even outperforming it in the 1-shot mini-Imagenet case with 50.89% to 49.4% accuracy. We also show that our model is resistant to distractors, unlabeled data that does not belong to any of the training classes, and hence reflecting robustness to labelled/unlabelled class distribution mismatch. We also performed a challenging discriminative power test, showing a relative improvement on top of the baseline of ≈14% on 20 classes on mini-Imagenet and ≈60% on 800 classes on Omniglot. Code will be made available.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Deep Learning
- Powerful Representation
- Meta Learning
- Semi-Supervised Learning
- Prior Knowledge
featured: false
links:
- type: pdf
  url: arxiv.org/abs/1903.02164
- type: code
  url: sites.google.com/view/mtlrl
hugoblox: {}
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:LjlpjdlvIbIC
  locked: []
  merged:
  - ayyad-2019-semi
  citations: 32
image:
  caption: ''
  focal_point: Smart
---
