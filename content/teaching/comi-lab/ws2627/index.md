---
title: CoMI-L — Winter 2026/27
semester: WS2627
semesters:
- WS2627
date: '2026-10-15'
start: '2026-10-15'
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
draft: false
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

### 🗓 Project (Winter 2026/27)

#### Who Does the Model See? Bias of Ultrasound Foundation Models across Countries and Income Settings in Fetal Ultrasound

Ultrasound is the imaging modality of antenatal care worldwide, and in low- and middle-income countries scans are increasingly done by non-specialists on low-cost devices. Ultrasound foundation models promise label-efficient AI support exactly there — but they are pretrained almost entirely on data from high-income hospitals. Students build a **harmonised benchmark from 12 openly licensed fetal-ultrasound releases (13 countries, four World Bank income groups)** and test whether frozen foundation models work equally well for fetuses scanned in Malawi, Uganda, Sierra Leone, Ghana, Egypt, Algeria, Brazil and China as in Spain, the Netherlands, Romania and the UK.

- **Bias metrics:** worst-group performance, between-group gaps and calibration, with patient-level confidence intervals.
- **Clinical highlight:** a measurement study — do errors in the cephalic index, abdominal circumference and cardiothoracic ratio, and so the share of fetuses flagged as abnormal, differ by site, device and income group?
- **Models:** FetalCLIP, USFM, SonoNet-64 (USF-MAE secondary).
- **Team:** 3 students; all share data harmonisation and the final synthesis, each leads one experimental work package. Students implement their own toolkit (*fusbias*) against a provided specification and acceptance tests.

| **WP** | **Topic** | **Lead** |
|--------|-----------|----------|
| 1 | Data harmonisation, de-duplication, patient-level splits and quality control | all |
| 2 | Zero-shot and training-free standard-plane recognition | S1 |
| 3 | Frozen-feature probing and bias audit | S2 |
| 4 | Clinical measurements: cephalic index, abdominal circumference, cardiothoracic ratio | S3 |
| 5 | Representation analysis, synthesis and report | all |

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
