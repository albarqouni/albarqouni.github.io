---
title: 'MRIQT: Image-quality transfer from ultra-low-field to high-field neonatal MRI'
project_type: collaboration
summary: This project addresses the limited diagnostic usability of portable ultra-low-field MRI (0.064 T) in neonatal neuroimaging, where reduced signal-to-noise ratio constrains clinical interpretation despite bedside accessibility.
date: '2024-01-01'
start: 2024-01
end: ''
funders: []
pis:
- shadi-albarqouni
co_pis:
- name: Sebiha Demir
- name: Anne Groteklae
- name: Hemmen Sabir
authors:
- shadi-albarqouni
- malek-al-abed
- elodie-germani
- sebiha-demir
- anne-groteklaes
- hemmen-sabir
partners:
- ukb
work_packages: []
themes:
- computational-imaging
- responsible-ai
datasets:
- neonatal-ulf-mri
tags: []
featured: false
image:
  caption: Ultra-low-field input, MRIQT output and high-field reference ([Al Abed et al., ISBI 2026](/publications/al-2026-mriqt/)).
  focal_point: Center
---

This project addresses the limited diagnostic usability of portable ultra-low-field MRI (0.064 T) in neonatal neuroimaging, where reduced signal-to-noise ratio constrains clinical interpretation despite bedside accessibility.
Together with the clinical partners, we curated a unique in-house cohort comprising 50 paired ultra-low-field and high-field 3D neonatal brain MRI scans, complemented by 230 additional unpaired scans across nine pathologies.
Building on this paired–unpaired data structure, we developed *MRIQT*, a 3D conditional diffusion framework for structure-preserving image quality transfer from ultra-low-field to high-field MRI. The method integrates physics-consistent k-space degradation, classifier-free guided diffusion, and an SNR-weighted volumetric perceptual loss.

MRIQT outperformed CNN- and GAN-based baselines, achieving up to 15.3% improvement in PSNR, while expert clinicians rated 85% of generated images as diagnostically useful with preserved pathology.

### Perspective

The project provides a methodological foundation for automated MRI quality enhancement and modality-agnostic quality control. Building on the current results, the work is prepared for translational follow-up and prospective validation, with a planned submission to the *Go-Bio Initial* funding program.
