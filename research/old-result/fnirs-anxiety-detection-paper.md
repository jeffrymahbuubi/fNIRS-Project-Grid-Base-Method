![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_0_seq_2.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_0_seq_4.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_0_seq_5.png)



# fNIRS Neuroimaging-Based Anxiety Detection

Department of BioMedical Engineering (BME)
National Cheng Kung University (NCKU)

Presenter : Jeffry

Advisor : Professor Che-Wei Lin

Date : 2025/06/06

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_1_seq_1.png)



1931

National Cheng Kung University

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_1_seq_4.png)



穿戴科技與行動照護實驗室

Wearable Technology and Mobile Healthcare Laboratory

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_1_seq_7.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_1_seq_8.png)



# Introduction

# Introduction: Generalized Anxiety Disorder

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_2_seq_2.png)



**Anxiety disorders—definition and sub-types:** Anxiety disorders are a group of conditions characterized by excessive fear, persistent worry and associated behavioural disturbance; the DSM-IV/5 class includes panic disorder, social anxiety disorder, specific phobias, post-traumatic stress disorder (PTSD), obsessive-compulsive disorder (OCD) and generalized anxiety disorder (GAD)¹.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_2_seq_4.png)



**Prevalence and treatment gap:** GAD is among the most common subtypes yet is frequently under-detected in clinical practice. Surveys report a 12-month GAD prevalence of roughly 7.6% and up to one-fifth of primary-care attendees fulfil criteria for at least one anxiety disorder¹. Despite this only 9.8% of affected individuals receive care, and nearly one-quarter remain entirely untreated—rates that are higher among adolescents and females.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_2_seq_6.png)



**Consequences:** The economic consequences are substantial: anxiety disorders account for an estimated US $42 billion in direct and indirect costs each year in the United States[1]. Functionally, GAD is associated with diminished dorsolateral prefrontal cortex activation, a change thought to undermine decision-making and emotional regulation. When unmanaged, the disorder increase the risk for major depression, substance misuse, cardiovascular disease and cognitive decline, and compromises academic, occupational and social functioning[2].

[1] K. Kroenke, R. L. Spitzer, J. B. W. Williams, P. O. Monahan, and B. Löwe, "Anxiety Disorders in Primary Care: Prevalence, impairment, comorbidity, and detection," Annals of Internal Medicine, vol. 146, no. 5, p. 317, Mar. 2007, doi: 10.7326/0003-4819-146-5-200703060-00004.

[2] S. Munir and V. Takov, "Generalized Anxiety Disorder," StatPearls - NCBI Bookshelf, Oct. 17, 2022. https://www.ncbi.nlm.nih.gov/books/NBK441870/

# Introduction: GAD Screening Method

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_3_seq_2.png)



The current screening method for diagnosing GAD is GAD-7, an even-item self-report scale that quantifies the frequency of core GAD symptoms over the preceding two weeks and is widely used for epidemiological screening and severity grading[3]. Nevertheless, several constraints limit its clinical and research utility:

1. Susceptibility to response bias — because all items rely on respondents' introspection, scores may be under- or over-reported, a well-recognized drawback of self-report methodology noted in recent psychometric work[4]

2. Absence of objective physiological or neural markers — the questionnaire cannot detect well-documented biological correlates of GAD such as dorsolateral prefrontal cortex hypo-activation seen on fNIRS/fMRI

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_3_seq_6.png)



These limitations underscore the need to pair the GAD-7 with clinician-administered interviews and, where feasible, with biomarker-based approaches to achieve a more objective and comprehensive assessment of generalized anxiety disorder

[3] R. L. Spitzer, K. Kroenke, J. B. W. Williams, and B. Löwe, "A brief measure for assessing generalized anxiety disorder," Archives of Internal Medicine, vol. 166, no. 10, p. 1092, May 2006, doi: 10.1001/archinte.166.10.1092

[4] M. Á. Casares, A. Díez-Gómez, A. Pérez-Albéniz, B. Lucas-Molina, and E. Fonseca-Pedrero, "Screening for anxiety in adolescents: Validation of the Generalized Anxiety Disorder Assessment-7 in a representative sample of adolescents," Journal of Affective Disorders, vol. 354, pp. 331-338, Mar. 2024, doi: 10.1016/j.jad.2024.03.047.

# Introduction: Neurological Biomarker

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_4_seq_2.png)



Functional near-infrared spectroscopy (fNIRS) is a promising biomarker for assessing generalized anxiety disorder (GAD). The technique directs near-infrared light (650-950 nm) through the scalp, skull, and superficial cortex; absorption and scattering by oxygenated and de-oxygenated haemoglobin reveal local brain activity. In anxiety disorders, the prefrontal cortex typically shows altered oxygenated-haemoglobin levels. By quantifying task- or rest-evoked haemodynamic changes, fNIRS delivers objective, real-time information that supports early diagnosis and ongoing monitoring.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_4_seq_4.png)



Compared to another neurological modality such as EEG and fMRI, fNIRS have several advantages as follows:

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_4_seq_6.png)



**Compared with fMRI:** fNIRS offer higher temporal resolution (~10Hz vs ~1 Hz) which allows finer tracking of rapid hemodynamic changes and easier separation of neural signals from physiological noise. fNIRS device also portable and comparatively inexpensive.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_4_seq_8.png)



**Compared with EEG:** Functional near-infrared spectroscopy (fNIRS) offers better spatial resolution than electroencephalography (EEG), localizing cortical activity within roughly 10–20 mm. Its main drawback is lower temporal resolution: EEG usually records at about 100 Hz, whereas fNIRS operates near 10 Hz. Even so, fNIRS is less susceptible to muscle artefacts, allowing participants more freedom of movement during data collection than EEG.

# Introduction: Literature Review

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_5_seq_2.png)



Research on AI-driven, automatic identification of anxiety disorders with fNIRS remains limited. Most studies instead focus on differentiating healthy controls (HCs) from major depressive disorder (MDD). Real-time detection systems are even rarer, because many current approaches depend on traditional machine-learning pipelines that rely on hand-crafted features and extensive experimentation to optimize feature-parameter combinations.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_5_seq_4.png)



The following is a list of studies using fNIRS for the automatic identification of HCs and Anxiety:

<table><thead><tr><th>Author –Year –SCI–IF–DOI</th><th>Target Class</th><th>fNIRS Task</th><th>Classifier</th><th>Features</th><th>Metrics</th><th>Val Strategy</th><th>Result</th></tr></thead><tbody><tr><td>G. Wang – 2025 – SCI Q1 – 4.9 – https://doi.org/10.1016/j.bspc.2025.107503</td><td>HCs, Anxiety, MDD</td><td>EAMT</td><td>FNN, CFNN</td><td>Temporal Avg-HbO per channel, Functional Connectivity (Coherence + Correlation)</td><td>Accuracy, F1-Score, AUC</td><td>4-fold cross-validation, repeated three times</td><td><ul><li><u>HC vs Anxiety</u>: 96.5% Acc, 95.4 F1-Score</li><li><u>3-class (HC/Anx/Dep)</u>: 90.4% Acc, 86.7 F1-Score</li><li><u>Anxiety vs Depression</u>: 95.2%, 91 F1-Score</li></ul></td></tr><tr><td>Y. Shen – 2025 – SCI Q1 – 3.8 – https://doi.org/10.1016/j.ajp.2025.104382</td><td>HCs, GAD, MDD, CMG</td><td>Verbal Fluency</td><td>Simple Neural Network</td><td>FFT spectrum, Wavelet Coefficients, Integral (AUC), and Centre-of-gravity</td><td>Accuracy, AUC</td><td>Holdout Validation with ratio of 60% train / 40% test</td><td><ul><li><u>Four-class (GAD / MDD / CMG / HC)</u>: 60.47 %</li><li><u>Three-class (GAD / MDD / HC)</u>: 77.19 %</li></ul></td></tr></tbody></table>

# Introduction: Literature Review

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_6_seq_2.png)



The following is a list of studies using fNIRS for the automatic identification of HCs and MDD:

<table><thead><tr><td>Author - Year - SCI-IF</td><td>Target Class</td><td>fNIRS Task</td><td>Classifier</td><td>Features</td><td>Metrics</td><td>Val Strategy</td><td>Result</td></tr></thead><tbody><tr><td>K. Shao - 2024 - SCI Q2 - 4.8</td><td>HCs, MDD</td><td>Verbal Fluency</td><td>2-D CNN (ResNet-18, LeNet, CNN-GRU, ViT)</td><td>2-D topographic "activation images."</td><td>Accuracy, F1-Score, AUC</td><td>Holdout validation</td><td>• HCs vs MDD: 90.5% Acc, 94.1 F1-Score, 97% AUC</td></tr><tr><td>S. Kim - 2023 - SSCI Q1 - 4.9</td><td>HCs, MDD- SHR, MDD- LHR</td><td>Three stroop block (word, color, incongruent)</td><td>SVM</td><td>mean Δ[oxy-Hb] & Δ[deoxy-Hb]</td><td>Accuracy</td><td>LOOCV</td><td>• HCs vs MDD- SHR vs MDD-LHR: 70.3% Acc, 76.0% Sensitivity, 64.7% Specificity</td></tr><tr><td>L. Mao - 2024 - SSCI Q1 - 4.9</td><td>HCs, MDD</td><td>Verbal Fluency</td><td>LR, NB, SVM, DT, KNN, RF, GBDT, MLP</td><td>six time-domain features: GLM β, integral, centroid, mean, slope, peak</td><td>Accuracy, AUC, Sensitivity, Specificity</td><td>Nested 10-Fold CV</td><td>• HCs vs MDD: 82.9% Acc, 89.5% AUC, 91.4% Sensitivity, 68.2% Specificity</td></tr><tr><td>T. Ma et al - 2020 - SCI Q4 - 0.7</td><td>HCs, MDD</td><td>Verbal Fluency</td><td>Attention-LSTM</td><td>Normalised raw time-domain fNIRS traces (ΔHbO, ΔHbR, ΔHbT)</td><td>Accuracy</td><td>Holdout validation (70/30)</td><td>• HCs vs MDD: 96.2% Acc</td></tr><tr><td>Y. Wu et al - 2024 - SCI Q1 - 5.5</td><td>HCs, MDD</td><td>Listening audio</td><td>SVM, RF</td><td>SD, RMS amplitude/variance, peak-to-peak, kurtosis, crest &amp; waveform factors</td><td>Accuracy</td><td>5-fold cross validation 60/40 ratio</td><td>• HCs vs MDD: 90.55% Acc</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_6_seq_5.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_6_seq_7.png)



# Introduction: Motivation and Significance

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_7_seq_2.png)



This study aims to develop a deep-learning framework for the automatic detection of generalized anxiety disorder (GAD) using fNIRS data acquired during four task paradigms—Go/No-Go, Verbal Fluency (VF), 1-back working memory, and SS. A secondary goal is to determine which of these tasks yields the highest diagnostic accuracy for anxiety identification.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_7_seq_4.png)



Subject-wise validation schemes—including 5-fold cross-validation (CV), 10-fold CV, and leave-one-subject-out (LOSO) CV—were employed to assess model performance and ensure an unbiased estimate of its ability to generalize to unseen individuals

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_7_seq_6.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_7_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_8_seq_1.png)



Material and Methods

# Dataset Overview

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_9_seq_2.png)



A total of 53 adults were recruited for this study—20 individuals with clinically diagnosed generalized anxiety disorder (GAD; 15 women, 5 men) and 33 age- and sex-matched healthy controls (HC; 23 women, 10 men). On the recording day, anxiety severity was quantified with Hamilton Anxiety Rating Scale (HAM-A)[5] and the State-Trait Anxiety Inventory (state subscale=STAI-S; trait subscale =STAI-T)[6].

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_9_seq_4.png)



Table 1 presents the general statistics of the study cohort, comprising Healthy Controls (HCs) and participants with Generalized Anxiety Disorders (GAD)

<table><thead><tr><th>Group</th><th>N</th><th>Age (years)<br>Mean ± SD</th><th>Female n<br>(%)</th><th>Male n (%)</th><th>HAM-A<br>Mean ± SD</th><th>STAI-S<br>Mean ± SD</th><th>STAI-T<br>Mean ± SD</th></tr></thead><tbody><tr><td>Healthy controls (HC)</td><td>33</td><td>73.0 ± 5.6</td><td>23 (70%)</td><td>10 (30%)</td><td>– (not administered)</td><td>29.8 ± 8.1</td><td>33.4 ± 8.0</td></tr><tr><td>Anxiety disorder (GAD)</td><td>20</td><td>52.2 ± 14.6</td><td>15 (75%)</td><td>5 (25%)</td><td>23.6 ± 8.1</td><td>46.6 ± 9.4</td><td>59.0 ± 8.8</td></tr></tbody></table>

Table 1

[5] M. Hamilton, "THE ASSESSMENT OF ANXIETY STATES BY RATING," British Journal of Medical Psychology, vol. 32, no. 1, pp. 50-55, Mar. 1959, doi: 10.1111/j.2044-8341.1959.tb00467.x.

[6] C. D. Spielberger, R. L. Gorsuch, and R. E. Lushene, "Manual for the State-Trait Anxiety Inventory (Form Y)*. Palo Alto, CA: Consulting Psychologists Press, 1983.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_9_seq_10.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_9_seq_12.png)



# Dataset Overview

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_2.png)



The descriptive numbers and hypothesis tests tell us three key things about our sample

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_4.png)



1. **Gender is balanced between groups:** The $\chi^2 = 0.01$ (p = 0.92) compares the proportion of women (70%) in the healthy-control (HC) group with that (75%) in the anxiety (GAD) group. Because the p-value greatly exceeds the conventional threshold of 0.05, the conclusion is that any observed difference could easily have arisen by chance. In practical terms, sex is unlikely to bias future comparisons of brain signals or model performance.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_6.png)



2. **Age differs substantially** : Welch's t = -6.13 (p = $3.3 \times 10^{-6}$) shows that HCs. (73.0 ± 5.6 yrs) are, on average, 21 years older than GAD participants (52.2 ± 14.6 yrs). The standardized effect size is very large (Cohen's d ≈ 2.1), meaning the groups are separated by roughly two pooled standard deviations.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_8.png)



3. **Clinical anxiety scales sharply discriminate the groups** :

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_10.png)



**HAM-A.** The GAD mean of $23.6 \pm 8.1$ falls in the "moderate anxiety" range ($\ge 18$), confirming clinically significant symptoms.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_12.png)



**STAI-S.** A mean of $46.6 \pm 9.4$ vs. $29.8 \pm 8.1$ in HCs ($t = 6.11, p = 4.3 \times 10^{-7}$) indicates that patients felt markedly more anxious in the moment of recording.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_14.png)



**STAI-T.** The trait score ($59.0 \pm 8.8$ vs. $33.4 \pm 8.0$; $t = 9.74, p < 10^{-11}$) shows a stable, enduring tendency toward anxiety in the clinical group. For context, values $\ge 55$ are typically interpreted as clinically elevated, whereas our HC means sit comfortably within the normative adult range (<40).

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_10_seq_16.png)



Together, these findings confirm that (a) the study successfully recruited a clinically anxious cohort exhibiting pronounced state and trait anxiety, (b) the sex distribution between groups is comparable, thus reducing potential confounding factors, and (c) the age difference between groups is substantial enough to warrant statistical adjustment

# Experimental Settings – Channel Placements

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_2.png)



This study employed a 23-channel functional near-infrared spectroscopy (fNIRS) device comprising eight pairs of emitters and detectors arranged according to the international 10-20 EEG placement system.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_4.png)



The fNIRS system emitted near-infrared light at two distinct wavelengths (760 nm and 850 nm). Each channel (Ch) was defined by the separation distance of 2.49–4.19 cm between an emitter-detector pair.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_6.png)



Figure 1 illustrates (a) the distribution of channels across the prefrontal cortex, and (b) the specific optode arrangement indicating source and detector positions relative to the measured channels.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_8.png)



(a)

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_10.png)



(b)

Figure 1

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_13.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_11_seq_15.png)



# Experimental Settings – Cognitive Task

Each participant completed four distinct cognitive tasks—Go/No-Go (GNG), 1-back working memory (1backWM), Serial Subtraction (SS), and verbal fluency (VF)—and performed four separate trials of every task, yielding 16 experimental blocks per person. Immediately after each trial, participants rated their momentary anxiety on a 0–10 visual-analogue scale (VAS). The primary aim was to determine which cognitive task yields the most effective performance for assessing anxiety disorders.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_12_seq_3.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_12_seq_6.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_12_seq_7.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_12_seq_9.png)



# Experimental Settings – Go/No-Go

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_13_seq_2.png)



Figure 2 illustrates the experimental procedure for the Go/No-Go task.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_13_seq_4.png)



Participants performed a Go/No-Go task in which each photograph was presented for 600 ms, followed by a 200-ms fixation period. Angry or smiling faces served as "Go" signals, prompting participants to press the "2" key on the numeric keypad, while neutral faces served as "No-Go" signals, requiring them to withhold a response. Each trial lasted approximately 35 seconds, beginning with a 3-second rest period, followed by 40 consecutive image-fixation cycles (40 × 0.6 s + 0.2 s = 32 s).

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_13_seq_6.png)



Figure 2 - Go/No-Go Cognitive Tasks

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_13_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_13_seq_10.png)



# Experimental Settings – SS

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_14_seq_2.png)



Figure 3 illustrates the experimental procedure for the SS task

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_14_seq_4.png)



In the Serial Subtraction (SS) task, each trial begin with a 7-s preparation period during which a target equation (e.g., "500 – 7") was displayed while participants remained silent, followed by 60 s of continuous calculation. During this active phase, the participant vocally subtracted the stated decrement as rapidly and accurately as possible (for example: 500, 493, 486, and so on) until the minute elapsed. The procedure was then repeated for three additional trials using new starting numbers and decrements (950 – 17, 800 – 13, and 650 – 8).

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_14_seq_6.png)



Figure 3 – *Serial Subtraction Cognitive Tasks*

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_14_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_14_seq_10.png)



Experimental Settings – 1backWM

Figure 4 illustrates the experimental procedure for the 1backWM task

In the 1-back working memory (1backWM) task, each trial began with a 5-second preparation period. The task consisted of a rapid sequence of 1-second sample events followed by 2-second response windows. During each sample event, a face photograph appeared in one of the nine cells of a 3×3 grid, accompanied by a spoken word. Participants were instructed to remember both the position of the image and the spoken word. When the response screen appeared, they compared the current stimuli with those presented in the immediately preceding sample (a "1-back" comparison). If the image appeared in the same location, they pressed the "Picture" key; if the spoken word was identical, they pressed the "Voice" key; if both the image and word matched, they pressed both keys simultaneously; if neither matched, they refrained from responding. Each full trial lasted 120 seconds (5 seconds preparation plus 115 seconds of task time), allowing for 38 picture-word cycles at 3 seconds per cycle.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_15_seq_4.png)



Figure 4 – *Serial Subtraction Cognitive Tasks*

# Experimental Settings – VF

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_16_seq_2.png)



Figure 5 illustrates the experimental procedure for the VF task.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_16_seq_4.png)



In the verbal fluency (VF) task, each trial began with a 7-second preparation period during which a target category (e.g., "flower") was displayed while participants remained silent. This was followed by a 60-second active phase during which participants were instructed to verbally generate as many words as possible that fit the given semantic category. The categories used were vegetables, furniture, fruit, and animals, with one category presented per trial. Participants spoke their responses aloud (for example, category "flower": "cherry blossoms, plum blossoms...").

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_16_seq_6.png)



Figure 5 – Serial Subtraction Cognitive Tasks

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_16_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_16_seq_10.png)



# Overall Workflow Pipeline

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_17_seq_2.png)



**Figure 6 – Overall Workflow of Proposed Methodology**

*Note*: 5fold-CV: 5-fold Cross-Validation, 10fold-CV: 10-fold Cross-Validation, LOSO-CV: Leave One Subject Out Cross Validation

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_17_seq_5.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_17_seq_7.png)



# 1D Signals to 3D Data

## 1. Epoch extraction:

Each HbO, HbR, HbT concentration yields 23 × T matrices. Let $H^{(k)}$, haemodynamic-concentration matrix of epoch $k$ after the modified Beer-Lambert conversion. Where,

$$
H^{(k)} = [h_t]_{t \in \tau_k} \in \mathbb{R}^{C \times L}
$$

$C = 23$ is the number of measurements channels,

$L$ is the number of time samples in that epoch, and

The column vector $h_t = [\Delta HbO_{1t}, \dots, \Delta HbO_{Ct}]^T$ contains the concentration change at time $t$ for every channel.

## 2. Baseline correction:

Baseline correction was applied to each epoch by extracting the first 5-s rest window $B$, computing its channel-wise mean, and subtracting this mean from every sample within the epoch. The baseline corrected epoch denoted as $\tilde{h}_t^{(k)} = h_t - \mu$ where $\mu = \frac{1}{|B|} \sum_{t \in B} h_t$

## 3. Z-Score Normalization:

To remove residual scale differences and place all channels on a common footing, a per-epoch z-score normalization is implemented. Specifically for each baseline-corrected epoch of $\tilde{h}^{(k)} \in \mathbb{R}^{C \times L}$, a channel-wise mean vector $\mu_k$ and standard-deviation vector $\sigma_k$ across its $L$ time samples. Every sample vector $\tilde{h}^{(k)}$ to a z-score vector denoted as $\hat{h}_t^{(k)} = \frac{\tilde{h}^{(k)} - \mu_k}{\sigma_k}$, $t \in T_k$. This operation centers channel's distribution at zero and rescales it to unit variances.

# 1D Signals to 3D Data

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_20_seq_2.png)



## 4. Mapping to a 5 × 7 channels grid:

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_20_seq_4.png)



Following a z-score normalization, each 23-channel sample vector $\hat{h}_t^{(k)} \in \mathbb{R}^{23}$ was mapped in a 5 × 7 channels grid that mirrors the physical layout of sources and detectors on the scalp. Let,

$$
M: \{1, \dots, 23\} = \{1, \dots, 5\} \times \{1, \dots, 7\}, \text{ where } M(c) = (i_c, j_c)
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_20_seq_7.png)



Be a fixed bijection that assigns channel $c$ to row $i_c$ and column $j_c$ of the grid. For a given time, sample $t$ then a constructed two-dimensional frame was made,

$$
F_t(i, j) = \begin{cases} \hat{h}_{c,t}, & (i,j) = M(c), \quad i = 1 \dots 5, j = 1 \dots 7, \\ 0, & \text{otherwise,} \end{cases}
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_20_seq_10.png)



Where $\hat{h}_{c,t}$ denotes the normalized concentration in channel $c$ at time $t$.

$$
F_t(i, j) = \begin{bmatrix} 0 & \hat{h}_{23,t} & \hat{h}_{22,t} & \hat{h}_{20,t} & \hat{h}_{19,t} & \hat{h}_{17,t} & 0 \\ \hat{h}_{15,t} & \hat{h}_{21,t} & \hat{h}_{12,t} & 0 & \hat{h}_{18,t} & \hat{h}_{9,t} & \hat{h}_{16,t} \\ 0 & \hat{h}_{14,t} & \hat{h}_{11,t} & \hat{h}_{10,t} & \hat{h}_{8,t} & \hat{h}_{7,t} & 0 \\ 0 & \hat{h}_{13,t} & \hat{h}_{5,t} & 0 & \hat{h}_{6,t} & \hat{h}_{2,t} & 0 \\ 0 & 0 & \hat{h}_{3,t} & \hat{h}_{4,t} & \hat{h}_{1,t} & 0 & 0 \end{bmatrix}
$$

Figure 7 – 2D Haemoglobin Concentration Matrix

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_20_seq_14.png)



Figure 8 – 2D Representation of 1D Haemoglobin Concentration matrix at time t (Empty values are represented as white)

# 1D Signals to 3D Data

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_2.png)



## 5. Radial-basis interpolation:

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_4.png)



Since the initial 5 × 7 grid contains measurements values only at the 23 channels locations, the remaining cell are zero. To transform this sparse grid $F_t$ into dense frame, a Gaussian radial-basis interpolation was applied to fill the empty pixels with values estimated from the known data.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_6.png)



The coordinates of known pixels $\{(x_m, y_m)\}_{m=1}^{23}$ and their corresponding z-scored concentrations $z_m = F_t(x_m, y_m)$ served as interpolation centers. For any grid point $(x, y)$ lacking data, its value was computed as a weighted sum of radial kernels centered on the known channel locations:

$$
\hat{F}_t(x, y) = \sum_{m=1}^{23} w_m \exp[-\varepsilon^2 \|(x, y) - (x_m, y_m)\|^2]
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_9.png)



The weights $w_m$ were determined by solving the linear system $\Phi w = z$, where the kernel matrix is defined as $\Phi_{mn} = \exp[-\varepsilon^2 \|(x, y) - (x_m, y_m)\|^2]$. This operation smoothly propagates each channel's influence on its immediate neighborhood while respecting anatomical proximity, resulting a fully populated 5 × 7 image $\hat{F}_t$ that preserves the original array's topographical structure.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_11.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_21_seq_13.png)



# 1D Signals to 3D Data

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_22_seq_2.png)



## 6. Stacking to a 3-D volume:

* The sequence of dense 5 × 7 images $\{\hat{F}_t\}_{t \in T_k}$ generated through radial basis function interpolation now provides anatomically complete "snapshots" of cortical hemodynamics at each sampling instant within epoch $k$. By concatenating these images along the temporal axis, a spatiotemporal tensor was constructed.

$$
S^{(k)} = [\hat{F}_t]_{t \in T_k} \in \mathbb{R}^{L \times 5 \times 7}
$$

* Here, the first-dimension indexes the $L$ time points, while the remaining two dimensions preserve the topographic layout of the channels. This stacking process transforms a sequence of 2D frames into a 3D volume that jointly captures when (temporal dynamics) and where (spatial distribution) hemodynamic fluctuations occur. The resulting tensor provides a natural input format for 3D deep learning architectures, enabling the models to exploit correlations across both spatial and temporal dimensions.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_22_seq_7.png)



**Figure 9 – 2D Haemoglobin Concentration**
**Frame $\hat{F}_t$ from sparse $F_t$ by interpolation**

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_22_seq_9.png)



**Figure 10 – 3D Haemoglobin**
**Concentration $S^{(k)}$ with the length of $L$**

# 1D Signals to 3D Data

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_23_seq_2.png)



## 7. 3D Data Sampling:

* From the dense spatio-temporal tensor of $S^{(k)} = [\hat{F}_t]_{t \in T_k} \in \mathbb{R}^{L \times 5 \times 7}$, a method called UniformTemporalSubsample was implemented, instead of the conventional sliding-window strategy widely used in time-series learning. Sliding windows generate dozens of overlapping segments for each recording, which substantially increases memory usage. In contrast, UniformTemporalSubsample selects $T^*$ uniformly spaced indices,

$$
idx_i = \left\lfloor \frac{(i-1)(L-1)}{T^*-1} \right\rfloor, i = 1, \dots, T^*,
$$

* And gathers the corresponding frames, yielding $S^* \in \mathbb{R}^{T^* \times 5 \times 7}$. A set of configurations for $T^*$ was implemented was tested as follows:: $T^* = 32$, $T^* = 64$, $T^* = 128$, and $T^* = 256$ to determine which configuration achieved the best performance for anxiety disorder classification.

* Therefore, UniformTemporalSubsample satisfies the following design goals: (i) It preserves the full chronological order of each cognitive block from beginning to end, and (ii) It reduces memory consumption compared to traditional windowing methods.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_23_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_23_seq_10.png)



# 3D Deep Learning Models

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_2.png)



## 1. 3-D Vision Transformer Architecture

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_4.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_5.png)



Tokenization is calculated based on the *Frame (Time Samples) and Image (Height × Width) patch size*

### Token Computation Calculations

Total Tokens

$$
= \underbrace{\left( \frac{H}{p_h} \times \frac{W}{p_w} \right)}_{\text{spatial tokens per frame}} \times \underbrace{\left( \frac{T}{p_t} \right)}_{\text{temporal tokens}}
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_10.png)



$\frac{H}{p_h}$ = patches along height

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_12.png)



$\frac{H}{p_w}$ = patches along width

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_14.png)



$\frac{H}{p_h}$ = patches along time dimensions

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_16.png)



The Video Vision Transformer (ViViT) is adopted as the backbone for fNIRS anxiety disorder classification, as its patch-based self-attention mechanism can model long-range spatiotemporal dependencies more effectively than 3D convolutions[9]. Each pre-processed tensor $S^* \in \mathbb{R}^{T^* \times 5 \times 7}$ is first divided into non-overlapping tubelets of size $(p_t, p_h, p_w)$ along the time, height, and width dimensions.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_18.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_24_seq_20.png)



# 3D Deep Learning Models

Each pre-processed tensor $S^* \in \mathbb{R}^{T^* \times 5 \times 7}$ is first divided into non-overlapping tubelets of size $(p_t, p_h, p_w)$ along the time, height, and width dimensions. Each tubelet is then flattened and linearly projected into a $d$-dimensional token vector. A learnable class token and sine-cosine spatiotemporal positional embeddings are subsequently added. The resulting sequence of $N$ tokens is computed as,

$$
N = \frac{T^*}{p_t} \times \frac{H}{p_h} \times \frac{W}{p_w}
$$

The token sequence is then processed by $L$ Transformer blocks (comprising multi-head self-attention and MLP layers), and the final CLS token representation is passed to a two-class MLP head to classify between Healthy and Anxiety groups.

## 2. Patch sizes and the 2:1 design rule

To balance temporal resolution with GPU memory constraints, we adopted a 2:1 ratio between temporal and spatial dimensions prior to patching. For example, with $T^* = 256$ and $H = W = 128$, and tubelet size $(p_t, p_h, p_w) = (16, 8, 8)$ the number of tokens is computed as $(\frac{128}{8})^2 \times \frac{256}{16} = 16 \times 16 \times 16 = 4096$ tokens. This configuration approaches the practical memory ceiling of our 48 GB GPU but remains feasible for a single forward pass. The motivation for using smaller tubelets (and hence generating more tokens) follows the original ViViT paper[9], which reports that denser tokenization consistently improves performance until GPU memory or compute resources become the limiting factor.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_25_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_25_seq_10.png)



# 3D Deep Learning Models

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_26_seq_2.png)



## 3. Hyperparameter Configuration

<table><thead><tr><th>Hyper-parameter</th><th>Setting(s)</th><th>Notes</th></tr></thead><tbody><tr><td>Optimizer</td><td>Adam</td><td>β<sub>1</sub> = 0.9, β<sub>2</sub> = 0.999</td></tr><tr><td>Learning-rate scheduler</td><td>Cosine Warm-up</td><td>10-epoch warm-up → cosine decay over 100 epochs</td></tr><tr><td>Initial learning rate</td><td>1 × 10<sup>-3</sup></td><td>Tuned on validation loss</td></tr><tr><td>Epochs</td><td>100</td><td>—</td></tr><tr><td>Batch size</td><td>8</td><td>Per GPU (48 GB VRAM)</td></tr><tr><td>UniformTemporalSubsample</td><td>64, 128, 256 frames</td><td>Determines T* before patching</td></tr><tr><td>Resize (H × W)</td><td>32 × 32, 64 × 64, 128 × 128</td><td>Keeps 2 : 1 temporal-spatial ratio (e.g., 256 × 128 × 128)</td></tr><tr><td>Frame patch size <i>p</i><sub>t</sub></td><td>4, 8, 16</td><td>Temporal tubelet depth</td></tr><tr><td>Image patch size (<i>p</i><sub>h</sub>, <i>p</i><sub>w</sub>)</td><td>(2,2), (4,4), (8,8)</td><td>Spatial tubelet size</td></tr><tr><td>Token count</td><td>4096</td><td>(T*/pt) × (H/p<sub>h</sub>) × (W/p<sub>w</sub>)</td></tr><tr><td>Transformer depth <i>L</i></td><td>6</td><td>Encoder layers</td></tr><tr><td>Attention heads <i>h</i></td><td>8</td><td>8 × 8 − dim head size</td></tr><tr><td>Embedding dim <i>d</i></td><td>64</td><td>Token dimension</td></tr><tr><td>MLP hidden dim</td><td>512</td><td>4 × d expansion</td></tr><tr><td>Data augmentation</td><td>Gaussian noise (μ = 0, σ = 0.05)</td><td>Training only</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_26_seq_5.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_26_seq_7.png)



# Evaluation Framework

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_27_seq_2.png)



## 1. Performance Metrics

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_27_seq_4.png)



Model output was evaluated with accuracy, sensitivity (recall for the anxiety class) and specificity (recall for the healthy class), and F1-Score. For every validation run, the calculation was implemented by first aggregated the raw predictions from all trials in each subjects into a single confusion matrix of C

$$
C = \begin{bmatrix} TN & FP \\ FN & TP \end{bmatrix}
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_27_seq_7.png)



Where TP, FN, FP, and TN are counted across all subjects. The metrics are then computed once from that matrix:

<table><thead><tr><td>Metric</td><td>Formula</td></tr></thead><tbody><tr><td>Accuracy</td><td>(TP + TN)/(TP + TN + FP + FN)</td></tr><tr><td>Sensitivity (Recall<sub>Anxiety</sub>)</td><td>TP/(TP + FN)</td></tr><tr><td>Specificity (Recall<sub>Healthy</sub>)</td><td>TN/(TN + FP)</td></tr><tr><td>F1-score</td><td>2TP/(2TP + FP + FN)</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_27_seq_10.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_27_seq_12.png)



# Evaluation Framework

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_28_seq_2.png)



## 2. Cross-validation strategies

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_28_seq_4.png)



A subject-level split is implemented, in which all four trials from each subject are kept entirely within either the training or validation set, preventing data leakage from having the same subject appear in both. In *k* - fold subject cross validation (*k* = 5 and *k* = 10), the complete subject set *S* is partitioned into *k* equally sized, non-overlapping folds; when *k* = 5 each fold contains roughly 20% of the subjects (an 80%/20% train-validation split), whereas *k* = 10 yields folds about 10% each (a 90%/10% split). In each iteration one-fold *S*<sub>val</sub> is used for validation, while the remaining *k* − 1 folds *S*<sub>train</sub> are used for training. This ensures that each subject appears in the validation set exactly once.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_28_seq_6.png)



Leave-One-Subject-Out is a special case where *k* = |*S*|: for every subject *s*<sub>*i*</sub> ∈ *S*, all trials of *s*<sub>*i*</sub> were withheld for validation, and the model was trained on the remaining subject *S*\{*s*<sub>*i*</sub>}; This procedure is repeated until every subject has been used once as the validation set.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_28_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_28_seq_10.png)



# Results and Discussion

# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_30_seq_2.png)



## 1. Finding the best hyperparameter configuration

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_30_seq_4.png)



To identify the optimal patching strategy for the ViViT backbone, an ablation study was conducted on the image-patch size ($p_h, p_w$) and the frame-patch size $p_t$, while all other hyperparameters were held constant ($depth = 6, heads = 8, d = 64, MLP = 512$). Nineteen participants from the Go/No-Go task (10 healthy, 9 anxiety; 76 trials) were included. A single 80%/20% subject-level split was applied, and classification performance was averaged over five random initializations for each configuration. The values of $p_t, p_h, p_w$ were varied while keeping the total number of ViViT input tokens fixed at

$$
N = \frac{T^*}{p_t} \times \frac{H}{p_h} \times \frac{W}{p_w} = 16 \times 16 \times 16 = 4096
$$

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_30_seq_7.png)



To ensure consistent spatiotemporal scaling, the ratio between temporal and spatial resolution was maintained at 2:1.

<table><thead><tr><th>Configuration</th><th>Clip size (T, H, W)</th><th>Patch sizes (p<sub>t</sub>, p<sub>h</sub>, p<sub>w</sub>)</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1-score</th></tr></thead><tbody><tr><td>A</td><td>(64, 32, 32)</td><td>(4, 2, 2)</td><td>78.33 %</td><td>79.17 %</td><td>77.50 %</td><td>77.08 %</td></tr><tr><td>B</td><td>(128, 64, 64)</td><td>(8, 4, 4)</td><td>73.75 %</td><td>73.12 %</td><td>77.50 %</td><td>74.62 %</td></tr><tr><td>C</td><td>(256, 128, 128)</td><td>(16, 8, 8)</td><td><strong>82.08 %</strong></td><td><strong>79.61 %</strong></td><td><strong>87.50 %</strong></td><td><strong>82.08 %</strong></td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_30_seq_10.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_30_seq_12.png)



# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_31_seq_2.png)



## 1. Finding the best hyperparameter configuration

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_31_seq_4.png)



Although all experiments utilized exactly 4096 transformer tokens, increasing the temporal depth from 64 to 256 frames (with proportional downscaling of spatial dimensions) significantly improved model performance. Specifically, configuration C outperformed other tested configurations by approximately 3% to 8% across all evaluation metrics.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_31_seq_6.png)



This finding aligns with the original ViViT study[9], which similarly indicated that increasing the temporal context—while keeping the total token budget fixed—consistently enhances classification accuracy. These results suggest that capturing an extended hemodynamic response period is more beneficial than having finer spatial detail given the same token budget. Consequently, configuration C ($p_t = 16, p_h = p_w = 8; 256 \times 128 \times 128$ clip) was adopted as the default configuration for all subsequent analyses.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_31_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_31_seq_10.png)



# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_32_seq_2.png)



## 2. Performance across HbO, HbR, and HbT in the Go/No-Go task

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_32_seq_4.png)



Using the best patch configuration identified (256 × 128 × 128 clip; 4096 tokens), we trained the ViT-3D network on three separate concentration channels —oxy-haemoglobin (HbO), deoxy-haemoglobin (HbR), and their sum, total haemoglobin (HbT)—and evaluated each channel with both 5-fold and 10-fold subject cross-validation. All participants from the Go/No-Go task (31 healthy, 20 anxiety; 204 trials) were included. A single 80%/20% subject-level split was applied. The results are summarized below:

<table><thead><tr><th>Concentration</th><th>CV scheme</th><th>Accuracy</th><th>Sensitivity</th><th>Specificity</th><th>Precision</th><th>F1-score</th></tr></thead><tbody><tr><td rowspan="2">HbT</td><td>5-fold</td><td>80.4 %</td><td>77.5 %</td><td>82.3 %</td><td>73.8 %</td><td>75.6 %</td></tr><tr><td>10-fold</td><td>89.7 %</td><td>86.3 %</td><td>91.9 %</td><td>87.3 %</td><td>86.8 %</td></tr><tr><td rowspan="2">HbO</td><td>5-fold</td><td>54.4 %</td><td>50.0 %</td><td>57.3 %</td><td>43.0 %</td><td>46.2 %</td></tr><tr><td>10-fold</td><td>73.0 %</td><td>67.5 %</td><td>76.6 %</td><td>65.1 %</td><td>66.3 %</td></tr><tr><td rowspan="2">HbR</td><td>5-fold</td><td>63.2 %</td><td>46.3 %</td><td>74.2 %</td><td>53.6 %</td><td>49.7 %</td></tr><tr><td>10-fold</td><td>64.7 %</td><td>52.5 %</td><td>72.6 %</td><td>55.3 %</td><td>53.9 %</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_32_seq_7.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_32_seq_9.png)



# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_33_seq_2.png)



## 2. Performance across HbO, HbR, and HbT in the Go/No-Go task

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_33_seq_4.png)



Across both validation protocols, total hemoglobin (HbT) markedly outperforms the individual chromophores (HbO and HbR). A plausible explanation for this observation lies in the underlying physiology of the fNIRS signal: task engagement elicits simultaneous but opposite-direction changes in oxyhemoglobin (HbO, increase) and deoxyhemoglobin (HbR, decrease). Summing these complementary signals yields a larger net amplitude relative to baseline, effectively enhancing the signal-to-noise ratio available to the model at each optode location.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_33_seq_6.png)



Furthermore, motion artifacts and systemic physiological oscillations typically influence HbO and HbR signals similarly, producing correlated fluctuations. By combining these two signals into total hemoglobin (HbT), common-mode fluctuations are attenuated, resulting in a clearer representation of cortical blood-volume dynamics. These findings justify selecting HbT as the default input concentration measure for subsequent experiments.

# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_34_seq_2.png)



## 3. Comparison Performance across different task type

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_34_seq_4.png)



Using the ViViT model trained on HbT data with 256-frame clips, classification performance varied significantly according to the cognitive task. Under 5-fold subject-level cross-validation, the Go/No-Go task yielded the highest overall performance (80.4% accuracy, 77.5% sensitivity, 82.3% specificity, and 75.6% F1-score). The Serial Subtraction task ranked second (69.9% accuracy, 66.7% sensitivity, 71.2% specificity, and 57.8% F1-score), while the Verbal Fluency (60.7% accuracy, 44.4% sensitivity) and 1-back working memory (1-back WM) tasks (59.2% accuracy, 34.1% sensitivity) showed comparatively weaker results.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_34_seq_6.png)



When validation granularity was increased to 10-fold subject-level cross-validation, all task performances improved; however, the relative ranking of tasks remained consistent. The Go/No-Go task again led (89.7% accuracy, 86.3% sensitivity, 91.9% specificity, and 86.8% F1-score), followed by 1-back WM (82.7% accuracy, 71.1% sensitivity, 90.0% specificity, 76.1% F1-score), Serial Subtraction (79.6% accuracy, 77.8% sensitivity, 80.7% specificity, 73.7% F1-score), and finally Verbal Fluency (75.5% accuracy, 63.9% sensitivity, 82.3% specificity, 65.7% F1-score)

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_34_seq_8.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_34_seq_10.png)



# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_35_seq_2.png)



## 3. Comparison Performance across different task type

<table><thead><tr><th>Task type</th><th>Subjects (HC / GAD)</th><th>CV scheme</th><th>Accuracy</th><th>Sensitivity</th><th>Specificity</th><th>F1-score</th></tr></thead><tbody><tr><td rowspan="2">Go/No-Go</td><td rowspan="2">31 / 20 (51)</td><td>5-fold</td><td>80.39 %</td><td>77.50 %</td><td>82.26 %</td><td>75.61 %</td></tr><tr><td>10-fold</td><td>89.71 %</td><td>86.25 %</td><td>91.94 %</td><td>86.79 %</td></tr><tr><td rowspan="2">1-back WM</td><td rowspan="2">30 / 19 (49)</td><td>5-fold</td><td>59.18 %</td><td>34.12 %</td><td>75.00 %</td><td>46.43 %</td></tr><tr><td>10-fold</td><td>82.65 %</td><td>71.05 %</td><td>90.00 %</td><td>76.06 %</td></tr><tr><td rowspan="2">Verbal Fluency</td><td rowspan="2">31 / 18 (49)</td><td>5-fold</td><td>60.71 %</td><td>44.44 %</td><td>70.16 %</td><td>46.38 %</td></tr><tr><td>10-fold</td><td>75.51 %</td><td>63.89 %</td><td>82.26 %</td><td>65.71 %</td></tr><tr><td rowspan="2">Serial Subtraction</td><td rowspan="2">31 / 18 (49)</td><td>5-fold</td><td>69.90 %</td><td>66.67 %</td><td>71.17 %</td><td>57.83 %</td></tr><tr><td>10-fold</td><td>79.59 %</td><td>77.78 %</td><td>80.65 %</td><td>73.68 %</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_35_seq_5.png)



**NOTE:** A statistical analysis will be included to provide more context on why the Go/No-Go separate classes perform better than the others.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_35_seq_7.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_35_seq_9.png)



# Experimental Results

## 4. Go/No-Go Validated Across 5-fold, 10-fold, and LOSO

The following table summarizes the classifier's performance on the Go/No-Go task under three progressively stricter subject-level validation schemes—5-fold CV, 10-fold CV, and Leave-One-Subject-Out (LOSO)—for the same cohort of 31 healthy controls and 20 anxiety participants.

<table><thead><tr><th>Validation scheme</th><th>Subjects (HC / ANX)</th><th>Accuracy</th><th>Sensitivity</th><th>Specificity</th><th>F1-score</th></tr></thead><tbody><tr><td>5-fold CV</td><td>31 / 20 (51)</td><td>80.39 %</td><td>77.50 %</td><td>82.26 %</td><td>75.61 %</td></tr><tr><td>10-fold CV</td><td>31 / 20 (51)</td><td>89.71 %</td><td>86.25 %</td><td>91.94 %</td><td>86.79 %</td></tr><tr><td>LOSO</td><td>31 / 20 (51)</td><td><strong>97.55 %</strong></td><td><strong>100.00 %</strong></td><td><strong>95.97 %</strong></td><td><strong>96.97 %</strong></td></tr></tbody></table>

Leave-One-Subject-Out (LOSO) validation ensures that recordings from the test subject never influence model training. Therefore, predictions are made exclusively on subjects whose individual signal characteristics, motion artifacts, and probe placement variations are completely unknown to the model. The observed near-perfect recall (100%) and high specificity (95.9%) indicate that the Go/No-Go paradigm elicits a hemodynamic signature that is both robust and highly consistent across different individuals. As a result, the model effectively differentiates anxiety-related from healthy brain patterns, even when encountering entirely new participants.

Importantly, the fact that model performance is highest under LOSO validation—strongly suggests that the model does not rely on memorizing subject-specific features but instead learns anxiety-specific neural dynamics directly linked to the task, thereby generalizing successfully to previously unseen individuals.

# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_37_seq_2.png)



## 4. Go/No-Go Validated Across 5-fold, 10-fold, and LOSO

<table><caption>Leave-One-Out-Subject-Out Cross Validation Healthy Subjects</caption><thead><tr><th>Subject</th><th>Acc. (%)</th><th>Sens. (%)</th><th>Spec. (%)</th><th>F1 (%)</th><th>Healthy</th><th>Anxiety</th></tr></thead><tbody><tr><td>AH014</td><td>25</td><td>0</td><td>25</td><td>0</td><td>1</td><td>3</td></tr><tr><td>AH015</td><td>75</td><td>0</td><td>75</td><td>0</td><td>3</td><td>1</td></tr><tr><td>AH017</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH018</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH019</td><td>75</td><td>0</td><td>75</td><td>0</td><td>3</td><td>1</td></tr><tr><td>AH020</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH021</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH022</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH023</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH025</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH026</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH027</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH028</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH030</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH031</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH033</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH034</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH035</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH036</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH037</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr></tbody></table>

# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_38_seq_2.png)



## 4. Go/No-Go Validated Across 5-fold, 10-fold, and LOSO

Leave-One-Out-Subject-Out Cross Validation Healthy Subjects

<table><thead><tr><th>Subject</th><th>Acc. (%)</th><th>Sens. (%)</th><th>Spec. (%)</th><th>F1 (%)</th><th>Healthy</th><th>Anxiety</th></tr></thead><tbody><tr><td>AH038</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH039</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH040</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH043</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH044</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH045</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH046</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH047</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH048</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH049</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr><tr><td>AH050</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td><td>0</td></tr></tbody></table>

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_38_seq_6.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_38_seq_8.png)



# Experimental Results

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_39_seq_2.png)



## 4. Go/No-Go Validated Across 5-fold, 10-fold, and LOSO

<table><caption>Leave-One-Out-Subject-Out Cross Validation GAD Subjects</caption><thead><tr><th>Subject</th><th>Acc. (%)</th><th>Sens. (%)</th><th>Spec. (%)</th><th>F1 (%)</th><th>Healthy</th><th>Anxiety</th></tr></thead><tbody><tr><td>EA012</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>EA016</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>EA055</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>EA060</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>AA011</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>AA013</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>AA041</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>AA056</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>AA064</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>EA061</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>EA062</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA042</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA051</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA052</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA053</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA054</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA057</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA058</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA059</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr><tr><td>LA063</td><td>100</td><td>100</td><td>0</td><td>100</td><td>0</td><td>4</td></tr></tbody></table>

# Conclusions

# Key Findings Summary

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_41_seq_2.png)



This study aimed to establish a fNIRS-based pipeline capable of reliably distinguishing GAD participants from healthy controls across multiple cognitive tasks and validation approaches. Four experiments summarized by the following key findings:

1. **Patch granularity significantly influences model performance:** Among ViViT model configurations that used a fixed token count (4096 tokens), the configuration with a 256-frame temporal window and 128 × 128 spatial resolution—divided into tubelets of size (16, 8, 8) produced the highest accuracy. This result indicates that capturing a longer temporal context is more than focusing finer spatial detail.
2. **Total haemoglobin (HbT) is the most discriminative chromophore:** In the Go/No-Go task, HbT consistently outperformed oxyhaemoglobin (HbO) and deoxyhaemoglobin (HbR) by 15-25 percentage points in accuracy. This highlights that measuring blood-volume changes, which integrate both oxygenated and deoxygenated components, yields a superior signal-to-noise ratio for anxiety detection.
3. **Task selection is crucial for anxiety classification:** When the ViViT model was evaluated across four cognitive tasks, the Go/No-Go task delivered the highest performance metrics (80% accuracy in 5-fold and approximately 90% in 10-fold cross-validation). Serial Subtraction ranked second, followed by 1-back working memory task, and finally Verbal Fluency.
4. **Leave-One-Subject-Out (LOSO) validation confirms generalizability:** LOSO validation using the Go/No-Go dataset (31 healthy controls, 20 GAD participants) resulted in high performance—97.6% accuracy, 100% sensitivity, and 96% specificity. This outcome demonstrates conclusively that the trained model captures robust anxiety-specific brain dynamics directly associated with task execution, rather than relying on subject-specific patterns or artifacts.

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_1.png)



1931

National Cheng Kung University

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_4.png)



穿戴科技與行動照護實驗室

Wearable Technology and Mobile Healthcare Laboratory

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_7.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_8.png)



Thanks for your attention~

![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_10.png)



![](https://netmind-public-files.s3.us-west-2.amazonaws.com/v2-quality_b064d76f600b45c1b0e099b184f6b258/v2-quality_b064d76f600b45c1b0e099b184f6b258_page_42_seq_11.png)
