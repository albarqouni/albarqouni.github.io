---
title: 'MRIQT: Physics-Aware Diffusion Model for Image Quality Transfer in Neonatal Ultra-Low-Field MRI'
date: '2025-11-17'
draft: false
authors:
- malek-al-abed
- sebiha-demir
- anne-groteklaes
- elodie-germani
- shahrooz-faghihroohi
- hemmen-sabir
- shadi-albarqouni
publication_types:
- paper-conference
publication:
  name: 2026 IEEE 23rd International Symposium on Biomedical Imaging (ISBI)
venue: isbi
doi: 10.48550/arxiv.2511.13232
abstract: Portable ultra-low-field MRI (uLF-MRI, 0.064 T) offers accessible neuroimaging for neonatal care but suffers from low signal-to-noise ratio and poor diagnostic quality compared to high-field (HF) MRI. We propose MRIQT, a 3D conditional diffusion framework for image quality transfer (IQT) from uLF to HF MRI. MRIQT combines realistic K-space degradation for physics-consistent uLF simulation, v-prediction with classifier-free guidance for stable image-to-image generation, and an SNR-weighted 3D perceptual loss for anatomical fidelity. The model denoises from a noised uLF input conditioned on the same scan, leveraging volumetric attention-UNet architecture for structure-preserving translation. Trained on a neonatal cohort with diverse pathologies, MRIQT surpasses recent GAN and CNN baselines in PSNR 15.3% with 1.78% over the state of the art, while physicians rated 85% of its outputs as good quality with clear pathology present. MRIQT enables high-fidelity, diffusion-based enhancement
  of portable ultra-low-field (uLF) MRI for deliable neonatal brain assessment.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2511.13232
hugoblox:
  ids:
    doi: 10.48550/arxiv.2511.13232
    arxiv: '2511.13232'
sync:
  source: legacy
  openalex: W4416378505
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2331-8422
  source_id: S4306400194
  source_type: repository
  citations: 0
  teaser: pdf:https://arxiv.org/pdf/2511.13232
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---
