---
title: Seamless Virtual Whole Slide Image Synthesis and Validation Using Perceptual Embedding Consistency
date: '2020-02-19'
draft: false
authors:
- amal-lahiani
- Irina Klaman
- nassir-navab
- shadi-albarqouni
- Eldad Klaiman
publication_types:
- article-journal
publication:
  name: IEEE Journal of Biomedical and Health Informatics
venue: ''
doi: 10.1109/jbhi.2020.2975151
abstract: Stain virtualization is an application with growing interest in digital pathology allowing simulation of stained tissue images thus saving lab and tissue resources. Thanks to the success of Generative Adversarial Networks (GANs) and the progress of unsupervised learning, unsupervised style transfer GANs have been successfully used to generate realistic, clinically meaningful and interpretable images. The large size of high resolution Whole Slide Images (WSIs) presents an additional computational challenge. This makes tilewise processing necessary during training and inference of deep learning networks. Instance normalization has a substantial positive effect in style transfer GAN applications but with tilewise inference, it has the tendency to cause a tiling artifact in reconstructed WSIs. In this paper we propose a novel perceptual embedding consistency (PEC) loss forcing the network to learn color, contrast and brightness invariant features in the latent space and hence substantially
  reducing the aforementioned tiling artifact. Our approach results in more seamless reconstruction of the virtual WSIs. We validate our method quantitatively by comparing the virtually generated images to their corresponding consecutive real stained images.We compare our results to state-of-the-art unsupervised style transfer methods and to the measures obtained from consecutive real stained tissue slide images. We demonstrate our hypothesis about the effect of the PEC loss by comparing model robustness to color, contrast and brightness perturbations and visualizing bottleneck embeddings. We validate the robustness of the bottleneck feature maps by measuring their sensitivity to the different perturbations and using them in a tumor segmentation task. Additionally, we propose a preliminary validation of the virtual staining application by comparing interpretation of 2 pathologists on real and virtual tiles and inter-pathologist agreement
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Stain Normalization
- Histology
- Powerful Representation
- Domain Adaptation
- Style Transfer
featured: true
links:
- type: pdf
  url: https://www.ncbi.nlm.nih.gov/pubmed/32086223
slidev: ''
hugoblox:
  ids:
    doi: 10.1109/jbhi.2020.2975151
sync:
  source: legacy
  openalex: W3008693315
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2168-2194
  - 2168-2208
  source_id: S2495854775
  source_type: journal
  citations: 47
---
