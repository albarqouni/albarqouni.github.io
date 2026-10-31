---
title: 'Virtual staining in digital pathology: GAN-based stain virtualization of whole slide images'
project_type: funded
acronym: Roche Virtual Staining
summary: Industry project with Roche Diagnostics on virtual staining in digital pathology — generating immunohistochemistry stains from tissue images with unsupervised GANs, seamlessly across gigapixel whole slide images, and segmenting multistain slides for biomarker research (2016–2020).
date: '2016-01-01'
start: 2016-01
end: 2020-12
status: ''
funders:
- roche
grant_number: ''
funding_url: ''
role: Scientific Lead (Postdoc at TUM CAMP)
pis:
- nassir-navab
co_pis:
- name: Dr. Eldad Klaiman
  org: roche
authors:
- shadi-albarqouni
- amal-lahiani
- nassir-navab
partners:
- roche
- tum
work_packages: []
themes:
- computational-imaging
datasets: []
tags:
- digital pathology
- virtual staining
- generative models
featured: false
---
Histopathological evaluation is central to diagnosis and drug development, especially in oncology. Beyond the standard H&E stain, target-specific stains such as immunohistochemistry (IHC) are often needed — but tissue is scarce, staining is slow and costly, and every additional stain consumes another tissue section. Cancer-immunotherapy biomarker research adds the burden of manually annotating multistain slides.

### What we did

- **Segmenting multistain slides from one shot.** A fully convolutional network with one-shot colour deconvolution segments digitised slides with multiple stainings into tumour, healthy tissue, necrosis and background, generalising across immunohistochemistry stains to reduce pathologists' annotation workload ([IET Image Processing 2019](/publications/lahiani-2018-generalizing/)).
- **Virtualizing the stain.** Unsupervised style-transfer GANs generate realistic, clinically meaningful images of stained tissue — for example FAP-CK immunofluorescence from other stainings — opening the way to in-silico multiplexing of several stains on the same tissue section ([European Congress on Digital Pathology 2019](/publications/lahiani-2019-virtualization/)).
- **Seamless at gigapixel scale.** Whole slide images must be processed tile by tile, and instance normalization leaves visible tiling artifacts when the tiles are stitched back together. A perceptual embedding consistency loss removes these artifacts ([MICCAI 2019](/publications/lahiani-2019-perceptual/)), and the full framework was validated for seamless virtual whole-slide synthesis ([IEEE JBHI 2020](/publications/lahiani-2020-seamless/)).

### Our role

Scientific lead as a postdoc at the Chair for Computer Aided Medical Procedures (TU Munich, PI: Nassir Navab), and co-supervision — with Eldad Klaiman (Roche Diagnostics, Penzberg) — of Amal Lahiani's industrial PhD (2016–2020).

### Perspective

The project showed that virtual staining can be made clinically interpretable and seamless at whole-slide scale, and seeded our later work on trustworthy digital staining in hematology.
