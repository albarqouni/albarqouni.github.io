---
title: CoMI-L — Summer 2026
semester: SS26
semesters:
- SS26
date: '2026-04-13'
start: '2026-04-13'
end: ''
status: ''
lecturers:
- shadi-albarqouni
authors:
- shadi-albarqouni
tutors: []
schedule: ''
room: ''
registration: ''
basis_url: ''
ecampus_url: ''
grading: []
timeline: []
funding: []
themes:
- computational-imaging
- federated-learning
projects: []
summary: The Computational Imaging Research (CoMI) Lab at the University of Bonn is a project-based lab where students carry out a semester-long research project in computational medical imaging, implementing and evaluating state-of-the-art algorithms on real medical data.
image:
  caption: Image created with assistance from DALL·E for the CoMI Lab at the University of Bonn.
  focal_point: Center
---
## Lab: Computational Medical Imaging (CoMI)

- **Lecturers:** [Prof. Dr. Shadi Albarqouni](../../../authors/shadi-albarqouni/)  
- **Tutors:**
- **Module:** MA-INF 2230  
- **Credits:** 4 SWS, 9 CP (270h workload)
- **Programme:** M.Sc. Computer Science  
- **Mode:** Optional (2. or 3. Semester)
- **Language:** English  
- **Format:** Lab (Praktikum), groups of max. 3 students
- **Frequency:** Every year

---

### Description

The **Computational Medical Imaging (CoMI) Lab** is a project-based course in which students carry out a semester-long research project in computational medical imaging. Working in small groups, students identify a well-defined problem, collect or are provided a suitable dataset, implement baseline and novel approaches, and evaluate their results both quantitatively and qualitatively.

Possible project topics (chosen or proposed by the instructors) include:

- **Anatomical Structure Segmentation** (e.g., multi-atlas, CNN-based)
- **Deformable Registration** (e.g., classic demons, learning-based registration)
- **Lesion/Anomaly Detection** (e.g., out-of-distribution detection in X-ray)
- **Radiomics & Quantitative Biomarker Extraction** (e.g., texture features, deep radiomics)
- **Uncertainty Estimation in Deep Learning** (e.g., MC-Dropout, Bayesian networks)
- **Causality & Bias Analysis in Medical Datasets** (e.g., domain shift, fairness)

---

### Learning Goals

#### Technical Skills
- Acquire a deep understanding of a selected problem in computational medical imaging: from problem identification to data processing, algorithm design, implementation, and evaluation.
- Implement, test, and validate state-of-the-art image-analysis algorithms (e.g., segmentation, registration, reconstruction, classification) on real medical data.
- Develop proficiency in using libraries and toolkits commonly used in medical imaging (e.g., ITK, SimpleITK, PyTorch for deep learning, nibabel/dipy).
- Learn to document software systematically (API documentation, code comments, unit tests) and to generate reproducible experiments (version control, containerization).

#### Soft Skills
- Collaborate effectively in small groups over the entire semester, dividing tasks (e.g., data curation, algorithmic implementation, evaluation).
- Prepare clear, concise technical documentation and design rationales.
- Present project progress and final results in oral form (midterm demo, final demo).
- Critically assess one's own results and position them within the state-of-the-art in computational medical imaging.

---

### 🗓 Project (Summer 2026)

#### Segmentation-Aware Benchmarking of Clinical, Radiomic, Deep-Learning and Foundation-Model Biomarkers for NSCLC Survival Prediction on Pretreatment CT

Can AI support reproducible imaging-biomarker discovery for non-small cell lung cancer (NSCLC)? Students benchmark zero-shot and promptable tumour-segmentation models, clinical risk models, handcrafted radiomics and pretrained CT foundation-model representations for prognosis and phenotype discovery. The central question: **do prognostic conclusions change when the tumour contour comes from an automated model instead of an expert?**

- **Dataset:** [TCIA NSCLC-Radiomics / LUNG1](https://www.cancerimagingarchive.net/collection/nsclc-radiomics/) — pretreatment thoracic CT of 422 patients with manual 3D gross-tumour-volume contours and survival data ([doi:10.7937/K9/TCIA.2015.PF0M9REI](https://doi.org/10.7937/K9/TCIA.2015.PF0M9REI)), the cohort of the landmark radiomics study by Aerts et al.
- **Team:** 4 students; all share data handling and phenotyping, each leads one experimental work package.
- **Software:** all experiments run on the lab's open [CoMI library](https://gitlab.com/albarqouni-lab/comi) for consistent pre-processing, metrics and figures.

| **WP** | **Topic** | **Lead** |
|--------|-----------|----------|
| 1 | Data handling, normalisation, harmonisation and quality control | all |
| 2 | Zero-shot / promptable segmentation benchmark (MedSAM, SAM-Med3D, FastSAM3D) | S1 |
| 3 | Clinical survival model (Cox, random survival forest, calibration) | S2 |
| 4 | Radiomics (PyRadiomics), feature selection and stability under automated contours | S3 |
| 5 | Foundation-model benchmarking (CT-CLIP, DINOv2, MedicalNet) | S4 |
| 6 | Correlation analysis, phenotyping and survival curves | all |

---

### Learning Format

Students work in **groups of up to 3** on a semester-long project. Each group will:

- Identify a well-defined problem and collect or be provided a suitable dataset (publicly available or hospital data under ethics approval).
- Perform a literature review to select baseline methods.
- Implement baseline and at least one novel or improved approach.
- Evaluate quantitatively (e.g., Dice, Hausdorff, MSE, classification accuracy) and qualitatively (expert review where possible).
- Document the software (README, API docs) and provide a reproducible environment (Docker/Singularity).
- Present **midterm progress** (oral demonstration + short written summary) and **final results** (oral + poster or full report).

---

### Assessment

**Graded Exam:**  
Oral presentation (final demo + Q&A, 20 minutes per group). Written report (12–16 pages, including background, methods, results, discussion).

**Ungraded Coursework (required for admission to the exam):**  
Project work; attendance in course sessions in accordance with the exam regulations of 2023, § 12(6).

---

### Recommended Prerequisites

At least one of the following:  
- MA-INF 2222 – *Visual Data Analysis*  
- MA-INF 2312 – *Image Acquisition and Analysis in Neuroscience*  
- MA-INF 2220 – *Lab Visualization and Medical Image Analysis* (or equivalent)

A solid background in **Python programming** (and/or C++), **linear algebra**, **calculus**, **probability theory**, and **numerical algorithms** is required. Familiarity with deep learning frameworks is highly recommended.

---

### References and Resources

**Relevant Journals:**  
- *Nature Machine Intelligence*  
- *Medical Image Analysis (MedIA)*  
- *IEEE Transactions on Medical Imaging (TMI)*  
- *Radiology: AI*, *European Radiology*, *IEEE Journal of Biomedical and Health Informatics*

**Relevant Conferences:**  
- *MICCAI* (Medical Image Computing & Computer-Assisted Intervention)  
- *CVPR* (IEEE/CVF Computer Vision and Pattern Recognition)  
- *MIDL* (Medical Imaging with Deep Learning)  
- *ISBI* (International Symposium on Biomedical Imaging)  
- *RSNA* (Radiological Society of North America Annual Meeting)

---

### Registration

Registration takes place via eCampus or by contacting [Prof. Dr. Shadi Albarqouni](../../../authors/shadi-albarqouni/).
