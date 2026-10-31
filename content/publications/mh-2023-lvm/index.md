---
title: 'Lvm-med: Learning large-scale self-supervised vision models for medical imaging via second-order graph matching'
date: '2023-01-01'
draft: false
authors:
- Duy M. H. Nguyen
- Hoang Nguyen
- Nghiem Diep
- Tan Ngoc Pham
- Tri Cao
- Binh Nguyen
- Paul Swoboda
- Nhat Ho
- shadi-albarqouni
- Pengtao Xie
- daniel-sonntag
- Mathias Niepert
publication_types:
- paper-conference
publication:
  name: Advances in Neural Information Processing Systems
venue: neurips
doi: 10.52202/075280-1212
abstract: 'Obtaining large pre-trained models that can be fine-tuned to new tasks with limited annotated samples has remained an open challenge for medical imaging data. While pre-trained deep networks on ImageNet and vision-language foundation models trained on web-scale data are prevailing approaches, their effectiveness on medical tasks is limited due to the significant domain shift between natural and medical images. To bridge this gap, we introduce LVM-Med, the first family of deep networks trained on large-scale medical datasets. We have collected approximately 1.3 million in medical images from 55 publicly available datasets, covering a large number of organs and modalities such as CT, MRI, X-ray, and Ultrasound. We benchmark several state-of-the-art self-supervised algorithms on this dataset and propose a novel self-supervised contrastive learning algorithm using a graph matching formulation. The proposed approach makes three contributions: (i) it integrates prior pair-wise image
  similarity metrics based on local and global information; (ii) it captures the structural constraints of feature embeddings through a loss function constructed via a combinatorial graph-matching objective; and (iii) it can be trained efficiently end-to-end using modern gradient-estimation techniques for black-box solvers. We thoroughly evaluate the proposed LVM-Med on 15 downstream medical tasks ranging from segmentation and classification to object detection, and both for the in and out-of-distribution settings. LVM-Med empirically outperforms a number of state-of-the-art supervised, self-supervised, and foundation models. For challenging tasks such as Brain Tumor Classification or Diabetic Retinopathy Grading, LVM-Med improves previous vision-language models trained on 1 billion masks by 6-7% while using only a ResNet-50. We release pre-trained models at this link https://github.com/duyhominhnguyen/LVM-Med.'
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags: []
featured: true
links:
- type: pdf
  url: https://proceedings.neurips.cc/paper_files/paper/2023/file/58cc11cda2a2679e8af5c6317aed0af8-Paper-Conference.pdf
- type: code
  url: https://github.com/duyhominhnguyen/LVM-Med
hugoblox:
  ids:
    doi: 10.52202/075280-1212
sync:
  source: legacy
  openalex: W7133205424
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1049-5258
  source_id: S4363606243
  source_type: conference
  merged:
  - mh-2024-lvm
  citations: 38
image:
  caption: ''
  focal_point: Smart
---
