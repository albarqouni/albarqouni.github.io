---
title: 6D Camera Relocalization in Ambiguous Scenes via Continuous Multimodal Inference
date: '2020-08-01'
draft: false
authors:
- mai-bui
- Tolga Birdal
- Haowen Deng
- shadi-albarqouni
- Leonidas Guibas
- Slobodan Ilic
- nassir-navab
publication_types:
- article-journal
publication:
  name: 16th European Conference on Computer Vision (ECCV)
venue: eccv
doi: 10.1007/978-3-030-58523-5_9
abstract: We present a multimodal camera relocalization framework that captures ambiguities and uncertainties with continuous mixture models defined on the manifold of camera poses. In highly ambiguous environments, which can easily arise due to symmetries and repetitive structures in the scene, computing one plausible solution (what most state-of-the-art methods currently regress) may not be sufficient. Instead we predict multiple camera pose hypotheses as well as the respective uncertainty for each prediction. Towards this aim, we use Bingham distributions, to model the orientation of the camera pose, and a multivariate Gaussian to model the position, with an end-to-end deep neural network. By incorporating a Winner-Takes-All training scheme, we finally obtain a mixture model that is well suited for explaining ambiguities in the scene, yet does not suffer from mode collapse, a common problem with mixture density networks. We introduce a new dataset specifically designed to foster camera
  localization research in ambiguous environments and exhaustively evaluate our method on synthetic as well as real data on both ambiguous scenes and on non-ambiguous benchmark datasets.
themes:
- computational-imaging
projects: []
datasets: []
tags:
- Computer Vision
- Pose Estimation
- Uncertainty
featured: false
links:
- type: pdf
  url: https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123630137.pdf
slidev: ''
hugoblox:
  ids:
    doi: 10.1007/978-3-030-58523-5_9
sync:
  source: legacy
  openalex: W3118099906
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 0302-9743
  - 1611-3349
  source_id: S106296714
  source_type: book series
  citations: 23
  merged:
  - bui-6-d
image:
  caption: ''
  focal_point: Smart
---
