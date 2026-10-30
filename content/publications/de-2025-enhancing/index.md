---
title: 'Enhancing patient-specific deep learning based segmentation for abdominal magnetic resonance imaging-guided radiation therapy: a framework conditioned on prior segmentation'
date: '2025-01-01'
draft: false
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
  name: Physics and Imaging in Radiation Oncology
venue: ''
doi: 10.1016/j.phro.2025.100766
abstract: 'Background and purpose: Conventionally, the contours annotated during magnetic resonance-guided radiation therapy (MRgRT) planning are manually corrected during the RT fractions, which is a time-consuming task. Deep learning-based segmentation can be helpful, but the available patient-specific approaches require training at least one model per patient, which is computationally expensive. In this work, we introduced a novel framework that integrates fraction MR volumes and planning segmentation maps to generate robust fraction MR segmentations without the need for patient-specific retraining. Materials and methods: The dataset included 69 patients (222 fraction MRs in total) treated with MRgRT for abdominal cancers with a 0.35 T MR-Linac, and annotations for eight clinically relevant abdominal structures (aorta, bowel, duodenum, left kidney, right kidney, liver, spinal canal and stomach). In the framework, we implemented two alternative models capable of generating patient-specific
  segmentations using the planning segmentation as prior information. The first one is a 3D UNet with dual-channel input (i.e. fraction MR and planning segmentation map) and the second one is a modified 3D UNet with double encoder for the same two inputs. Results: . In particular, the dual-channel input 3D UNet outperformed the one with double encoder, especially when the alignment between the two input channels is satisfactory. Conclusion: The proposed workflow was able to generate accurate patient-specific segmentations while avoiding training one model per patient and allowing for a seamless integration into clinical practice.'
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: true
links:
- type: pdf
  url: https://www.phiro.science/article/S2405-6316(25)00071-5/pdf
slidev: ''
hugoblox:
  ids:
    doi: 10.1016/j.phro.2025.100766
sync:
  source: legacy
  openalex: W4409528521
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2405-6316
  source_id: S2898405426
  source_type: journal
  citations: 7
image:
  caption: ''
  focal_point: Smart
---
