---
title: MRIQT
summary: 'Code for “MRIQT: Physics-Aware Diffusion Model for Image Quality Transfer in Neonatal Ultra-Low-Field MRI”. Portable ultra-low-field MRI (uLF-MRI, 0.064 T) offers accessible neuroimaging for neonatal care but suffers from low signal-to-noise ratio and poor diagnostic quality compared to high-field (…'
date: '2025-11-02'
lastmod: '2026-06-02'
repository: https://github.com/albarqounilab/MRIQT
homepage: ''
language: Python
stars: 4
license: ''
topics: []
code_type: research
course: ''
publications:
- al-2026-mriqt
themes:
- computational-imaging
- responsible-ai
projects:
- mriqt
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/MRIQT
  locked: []
image:
  caption: Teaser figure of the accompanying paper.
  focal_point: Center
---
### About the method

From the abstract of [MRIQT: Physics-Aware Diffusion Model for Image Quality Transfer in Neonatal Ultra-Low-Field MRI](/publications/al-2026-mriqt/):

> Portable ultra-low-field MRI (uLF-MRI, 0.064 T) offers accessible neuroimaging for neonatal care but suffers from low signal-to-noise ratio and poor diagnostic quality compared to high-field (HF) MRI. We propose MRIQT, a 3D conditional diffusion framework for image quality transfer (IQT) from uLF to HF MRI. MRIQT combines realistic K-space degradation for physics-consistent uLF simulation, v-prediction with classifier-free guidance for stable image-to-image generation, and an SNR-weighted 3D perceptual loss for anatomical fidelity. The model denoises from a noised uLF input conditioned on the same scan, leveraging volumetric attention-UNet architecture for structure-preserving translation. Trained on a neonatal cohort with diverse pathologies, MRIQT surpasses recent GAN and CNN baselines in PSNR 15.3% with 1.78% over the state of the art, while physicians rated 85% of its outputs as good quality with clear pathology present. MRIQT enables high-fidelity, diffusion-based enhancement of portable ultra-low-field (uLF) MRI for deliable neonatal brain assessment.

### Using the code

The repository README covers setup, test on a data sample, train on your own dataset, prepare your data in [bids format](https://bids.neuroimaging.io/index.html)., generate your own transfer function from your paired data. See [the repository on GitHub](https://github.com/albarqounilab/MRIQT#readme) for step-by-step instructions.
