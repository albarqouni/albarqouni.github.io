---
title: MRIQT — Image-Quality Transfer for Ultra-Low-Field MRI
date: 2026-10-30
weight: 2
summary: Slide between a portable ultra-low-field (0.064 T) neonatal MRI scan and its MRIQT enhancement — a physics-aware 3D diffusion model that transfers high-field image quality to bedside scans.
modality:
- MRI
demo_url: ''
embed: false
repository: https://github.com/albarqounilab/MRIQT
video: ''
themes:
- computational-imaging
- responsible-ai
projects:
- mriqt
publications:
- al-2026-mriqt
authors:
- malek-al-abed
- sebiha-demir
- anne-groteklaes
- elodie-germani
- shahrooz-faghihroohi
- hemmen-sabir
- shadi-albarqouni
sources:
- uni-bonn
- ukb
- tum
citation: |-
  @inproceedings{alabed2026mriqt,
    title     = {MRIQT: Physics-Aware Diffusion Model for Image Quality Transfer in Neonatal Ultra-Low-Field MRI},
    author    = {Al Abed, Malek and Demir, Sebiha and Groteklaes, Anne and Germani, Elodie and Faghihroohi, Shahrooz and Sabir, Hemmen and Albarqouni, Shadi},
    booktitle = {IEEE International Symposium on Biomedical Imaging (ISBI)},
    year      = {2026},
    eprint    = {2511.13232},
    archivePrefix = {arXiv}
  }
image:
  caption: Ultra-low-field input, MRIQT and the high-field reference for one case ([Al Abed et al., ISBI 2026](/publications/al-2026-mriqt/)).
  focal_point: Center
---
**Slide to compare** the portable ultra-low-field scan (uLF, right) with the MRIQT enhancement (left). Use the buttons to switch between two patients.

{{< compare before="demo_ulf_A.png|demo_ulf_B.png" after="demo_mriqt_A.png|demo_mriqt_B.png" before_label="uLF (0.064 T)" after_label="MRIQT" cases="Case A|Case B" >}}
Neonatal brain MRI from the University Hospital Bonn cohort. Ethical approval: Ethics Committee of the University of Bonn (Nr. 167/22).
{{< /compare >}}

[arXiv](https://arxiv.org/abs/2511.13232) · [PDF](https://arxiv.org/pdf/2511.13232.pdf) · [Code](https://github.com/albarqounilab/MRIQT) · Accepted at [IEEE ISBI 2026](https://biomedicalimaging.org/2026/), London

### Why it matters

Infants change fast in the first weeks of life: their brains differ from adult brains in both anatomy and tissue contrast. In **neonatal intensive care units**, many infants have neurological conditions that need repeated MRI, yet standard **high-field MRI** means disconnecting them from life support and moving them to a scanner room — slow, often requiring sedation and exposure to loud noise.

**Portable ultra-low-field MRI** (0.064 T) brings the scanner to the bedside, but with low signal-to-noise and reduced diagnostic quality. **MRIQT** closes that gap: it performs **3D image-quality transfer (uLF → high-field)** with a conditional diffusion model guided by **physics-aware k-space simulation** and an **anatomy-preserving 3D perceptual objective**. The cohort comprises neonates with an average age of two months and nine clinically relevant neurological pathologies, often occurring together.

![Ultra-low-field input, MRIQT output and high-field reference for one case](teaser.png)

### How it works

- **Physics-aware degradation:** realistic ultra-low-field scans are simulated from high-field ones in k-space.
- **3D conditional diffusion:** the model enhances the scan while preserving anatomy.
- **Guidance and an SNR-weighted 3D perceptual loss** reduce artefacts and hallucinations.

**Training** — MRIQT learns from physics-based uLF simulations to reconstruct anatomically faithful images from noisy inputs:

![MRIQT training](training_1.png)

**Inference** — given a real uLF scan, MRIQT iteratively denoises a noisy initialisation while conditioning on the uLF measurement:

![MRIQT inference](inference_1.png)

### Results

![Qualitative comparison of MRIQT with competing methods](results.png)

Compared with competing methods on PSNR, LPIPS, MAE, MS-SSIM, SSIM and Pearson correlation:

![Quantitative comparison](qresults.png)
