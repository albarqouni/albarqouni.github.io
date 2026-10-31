---
title: Optimisation of X-ray images with respect to image quality and dose
project_type: funded
acronym: Siemens X-ray
summary: Industry project with Siemens Healthineers (Advanced Therapies, Forchheim) on lowering the X-ray dose of interventional imaging without losing image quality — noise-model-driven denoising of low-dose fluoroscopy and angiography, and a real-time learning-based denoiser trained on simulated low-dose images.
date: '2016-01-01'
start: 2016-01
end: 2019-12
status: ''
funders:
- siemens-healthineers
grant_number: ''
funding_url: ''
role: Scientific Lead (Postdoc at TUM CAMP)
pis:
- nassir-navab
co_pis:
- name: Prof. Dr. Norbert Strobel
  org: siemens-healthineers
- name: PD Dr. Markus Kowarschik
  org: siemens-healthineers
authors:
- shadi-albarqouni
- nassir-navab
- sai-gokul-hariharan
partners:
- siemens-healthineers
- tum
show_partners: true
work_packages: []
themes:
- computational-imaging
datasets: []
tags:
- X-ray
- dose reduction
- denoising
- interventional imaging
featured: true
image:
  caption: 'An angiographic head phantom acquired at 30% of the standard dose, after learning-based denoising, and at the full standard dose ([Hariharan et al., MICCAI 2019](/publications/hariharan-2019-learning/); figure tiles from [Hariharan, PhD thesis, TUM 2023](https://mediatum.ub.tum.de/1692881)).'
  focal_point: Center
---
X-ray guidance is at the heart of interventional procedures, but it exposes patients — and clinical staff, over a whole career — to ionising radiation. Following the "as low as reasonably achievable" principle, the dose can only be lowered if the image quality is kept, yet lower dose means fewer photons and noisier images, and at very low dose conventional denoisers oversmooth or create artefacts. Supervised deep learning would need aligned low- and high-dose image pairs, which cannot ethically be acquired during an intervention.

### What we did

- **Photon recycling for ultra-low-dose sequences.** A patch-based spatio-temporal denoiser with a properly parameterised Poisson–Gaussian noise model exploits non-local self-similarity across frames and low-rank approximation, without needing an initial estimate — better denoising at lower computational cost ([IJCARS 2018](/publications/hariharan-2018-photon/)).
- **Low-dose digital subtraction angiography.** Spatially aligned DSA frames vary mainly through the flow of contrast agent, so a constrained, weighted rank-1 approximation of the temporal stack denoises each frame — evaluated with an advanced neurovascular replication system towards reducing both X-ray dose and contrast agent ([IJCARS 2019](/publications/hariharan-2019-preliminary/)).
- **Learning to denoise without clean images.** A model-based simulation of realistic low-dose X-ray images — accounting for system gain, electronic noise and detector blur — generates training data from routine acquisitions, and the same imaging model normalises the input through noise-variance stabilisation. The resulting real-time network outperformed BM3D and WNNM on phantom and clinical data and was preferred by experts for sharp, artefact-free and realistic results ([MICCAI 2019](/publications/hariharan-2019-learning/)).

### Our role

Scientific lead of the project as postdoc at TUM CAMP under Nassir Navab (PI and main supervisor), and mentoring of Sai Gokul Hariharan's industrial PhD, run jointly with Norbert Strobel and Markus Kowarschik at Siemens Healthineers and completed at TU Munich in 2023.

### Perspective

The thesis concluded that the X-ray dose can be reduced substantially without sacrificing clinically relevant information; the work continued at Siemens Healthineers in patents on X-ray noise reduction.
