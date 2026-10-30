---
title: Physics and Imaging in Radiation Oncology
date: '1970-01-01'
draft: true
authors:
- Francesca De Benetti
- Nikolaos Delopoulos
- Claus Belka
- Stefanie Corradini
- nassir-navab
- Thomas Wendler
- shadi-albarqouni
- guillaume-landry
- christopher-kurz
publication_types:
- article-journal
publication:
  name: ''
venue: ''
doi: ''
abstract: 'Background and purpose: Conventionally, the contours annotated during magnetic resonance-guided radiation therapy (MRgRT) planning are manually corrected during the RT fractions, which is a time-consuming task. Deep learning-based segmentation can be helpful, but the available patient-specific approaches require training at least one model per patient, which is computationally expensive. In this work, we introduced a novel framework that integrates fraction MR volumes and planning segmentation maps to generate robust fraction MR segmentations without the need for patient-specific retraining. Materials and methods: The dataset included 69 patients (222 fraction MRs in total) treated with MRgRT for abdominal cancers with a 0.35 T MR-Linac, and annotations for eight clinically relevant abdominal structures (aorta, bowel, duodenum, left kidney, right kidney, liver, spinal canal and stomach). In the framework, we implemented two alternative models capable of generating patient-specific
  segmentations using the planning segmentation as prior information. The first one is a 3D UNet with dual-channel input (ie fraction MR and planning segmentation map) and the second one is a modified 3D UNet with double encoder for the same two inputs.Results: On average, the two models with prior anatomical information outperformed the conventional population-based 3D UNet with an increase in Dice similarity coefficient> 4%. In particular, the dual-channel input 3D UNet outperformed the one with double encoder, especially when the alignment between the two input channels is satisfactory.Conclusion: The proposed workflow was able to …'
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: source
  url: https://scholar.google.com/scholar?cluster=5576397483010103341&hl=en&oi=scholarr
  name: Publisher
slidev: ''
hugoblox: {}
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:48xauSegjOkC
  locked: []
  citations: 0
image:
  caption: ''
  focal_point: Smart
---
