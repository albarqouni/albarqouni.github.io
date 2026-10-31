---
title: Deep learning for clinically significant prostate cancer in 3D mpMRI and MR Fingerprinting
project_type: collaboration
summary: This project addresses the detection and characterization of clinically significant prostate cancer (csPCa) in MRI, where diagnostic performance is limited by inter-reader variability and the complexity of multi-parametric, volumetric imaging.
date: '2023-01-01'
start: 2023-01
end: 2024-12
funders: []
pis:
- shadi-albarqouni
co_pis: []
authors:
- shadi-albarqouni
- barbara-wichtmann
- julian-luetkens
- niklas-kerkfeld
- hyun-ko
partners:
- ukb
- unimelb
work_packages: []
themes:
- computational-imaging
datasets:
- prostate-mri-mrf
tags: []
featured: false
image:
  caption: Prostate MRI with segmentation from the [prostate MRF dataset](/datasets/prostate-mri-mrf/).
  focal_point: Center
---

**Collaborators:** *Peter MacCallum Cancer Centre, Melbourne*

This project addresses the detection and characterization of clinically significant prostate cancer (csPCa) in MRI, where diagnostic performance is limited by inter-reader variability and the complexity of multi-parametric, volumetric imaging.
Together with the clinical partners, we curated an initial in-house 3D MRI cohort of 106 patients with histopathological reference, including bi-parametric MRI and quantitative MR Fingerprinting (MRF), which was subsequently extended with external and public datasets to form a multi-center cohort of approximately 500 cases.
Methodologically, we developed fully 3D deep learning models that explicitly incorporate anatomical prostate zone information, enabling interpretable and biomarker-aware csPCa detection and segmentation beyond slice-wise analysis.

A dedicated sub-project evaluated transformer-based 3D U-Net architectures for lesion segmentation. On public (PI-CAI) and in-house datasets, transformer-based models achieved Dice scores above 0.60 on detected lesions and demonstrated improved robustness under reduced training data compared to CNN-based baselines, while highlighting persistent challenges in false-positive reduction.

### Perspective

The project established a scalable research line on interpretable, anatomy-aware AI for prostate cancer imaging and contributed to early-career training through a completed Bachelor’s thesis and an ISMRM abstract. Ongoing work extends this line toward vision–language foundation models integrating 3D imaging, quantitative MRI biomarkers, and anatomical priors, forming a basis for continued multi-center collaboration and future third-party funding.
