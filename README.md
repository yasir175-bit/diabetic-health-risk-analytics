# Diabetic Neuropathy & Health Risk Analysis Dashboard

An interactive, clinical-grade Power BI dashboard engineered to evaluate patient health risks, biomarker distributions, and multi-organ diabetic complications. The system integrates cross-filtering with dynamic 3D anatomical rendering driven by custom DAX logic to simulate organ health under **Controlled Glucose** versus **Chronic Hyperglycemia** states.

---

## 📌 Executive Summary & Project Overview

Diabetic neuropathy and microvascular/macrovascular damage represent critical complications in long-term diabetes management. This project visualizes patient demographic cohorts, clinical biomarkers (HbA1c, Fasting Glucose, BP Risk), and lifestyle factors to uncover risk patterns across major target organs: **Retina**, **Heart**, **Kidneys**, **Peripheral Nerves**, and **Full Body systemic impact**.

### Key Business & Clinical Questions Answered

* How do glycemic control metrics (HbA1c) correlate with blood pressure risk tiers across specific age demographics?
* What is the longitudinal relationship between diabetes duration (in years) and daily insulin dosage requirements?
* How do modifiable lifestyle variables (smoking status, physical activity level) distribute across different organ-specific patient cohorts?
* What visual and anatomical differences manifest across target organs when toggling between controlled glucose levels and chronic hyperglycemic pathology?

---

## 🚀 Key Features

* **Dynamic 3D Anatomical Modeling:** Utilizes a decoupled DAX-driven Image URL lookup schema that renders high-fidelity 3D organ states directly on the canvas without visual breakage or manual page branching.
* **Bi-Directional Cross-Filtering:** Selecting any organ from the navigation rail isolates that specific patient sub-cohort across all demographic, risk, and treatment charts.
* **Biomarker Risk Stratification:** 100% stacked bar chart analyzing HbA1c levels mapped across age groups and segmented by blood pressure severity categories (High, Low, Normal).
* **Longitudinal Trend Analysis:** Continuous area chart mapping patient years lived with diabetes against average daily insulin unit requirements.
* **Clean Neumorphic UI Design:** Custom PowerPoint layout canvas built with modern cards, responsive visual spacing, and accessible contrast ratios.

---

## 🏗️ Data Architecture & Data Model

The data model is designed around a **Star Schema** to ensure performance and integrity across cross-filtering operations:

```text
               ┌────────────────────────┐
               │    Fact_DiabeticPatients│
               │────────────────────────│
               │ * Patient_ID (PK)      │
               │ * Age / Age_Group      │
               │ * Gender               │
               │ * HbA1c_Percent        │
               │ * Fasting_Glucose      │
               │ * Daily_Insulin_Units  │
               │ * Years_With_Diabetes  │
               │ * BP_Risk              │
               │ * Smoking_Status       │
               │ * Physical_Activity    │
               │ * Affected_Organ (FK)  │
               └───────────┬────────────┘
                           │ 1:N
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
┌────────────────────────┐           ┌────────────────────────┐
│      Dim_Organs        │           │      Image_Lookup      │
│────────────────────────│           │────────────────────────│
│ * Organ_ID (PK)        │           │ * Organ_Name           │
│ * Organ_Name           │           │ * Condition_State      │
│ * Display_Order        │           │ * Image_URL (CDN link) │
│ * Icon_URL             │           └────────────────────────┘
└────────────────────────┘

```

---

## 📐 Core DAX Measures

### 1. Dynamic 3D Organ URL Router

```dax
Selected_Organ_Display = 
VAR SelectedOrgan = SELECTEDVALUE(Dim_Organs[Organ_Name], "Full Body")
VAR SelectedCondition = SELECTEDVALUE(Fact_DiabeticPatients[Condition_State], "Controlled Glucose")
RETURN
    CALCULATE(
        MAX(Image_Lookup[Image_URL]),
        FILTER(
            Image_Lookup,
            Image_Lookup[Organ_Name] = SelectedOrgan &&
            Image_Lookup[Condition_State] = SelectedCondition
        )
    )

```

### 2. Aggregated Patient Count

```dax
Total Patients = COUNTROWS(Fact_DiabeticPatients)

```

### 3. Cohort Average HbA1c

```dax
Avg HbA1c = 
CALCULATE(
    AVERAGE(Fact_DiabeticPatients[HbA1c_Percent]),
    NOT(ISBLANK(Fact_DiabeticPatients[HbA1c_Percent]))
)

```

### 4. Mean Daily Insulin Dosage

```dax
Avg Daily Insulin = AVERAGE(Fact_DiabeticPatients[Daily_Insulin_Units])

```

---

## 📊 Dashboard Visuals & Breakdown

| Visual Component | Chart Type | Key Metrics Analyzed |
| --- | --- | --- |
| **KPI Scorecards** | Card Visuals | Total Active Patients, Cohort Mean HbA1c (%) |
| **Organ Navigation Rail** | Slicer / Custom Card Rail | Full Body, Heart, Kidney, Peripheral Nerves, Retina |
| **HbA1c by Age & BP Risk** | 100% Stacked Column | Age Groups (18–35, 36–48, 49–60, 60+) × Blood Pressure Tiers |
| **Smoking Demographics** | Donut Chart | Patient distribution by Never, Former, and Current smoking status |
| **Insulin Progression Curve** | Area Chart | Daily Insulin Units required vs. Years living with Diabetes |
| **Gender & Activity Levels** | Clustered Horizontal Bars | Patient counts segmented by Gender & Physical Activity Tiers |
| **Dynamic Showcase** | Simple Image / Card (new) | High-resolution 3D medical renders switching on condition selection |

---

## 📂 Repository File Structure

```text
diabetic-neuropathy-risk-analysis/
│
├── Diabetic_Neuropathy_Health_Risk_Analysis.pbix  # Complete Power BI project file
├── README.md                                      # Documentation and architecture guide
│
├── dataset/
│   ├── Fact_DiabeticPatients.csv                  # Core patient cohort data
│   ├── Dim_Organs.csv                             # Dimension table for organ entities
│   └── Image_Lookup.csv                           # URL routing matrix for 3D renders
│
├── assets/
│   ├── background/
│   │   └── dashboard_canvas_layout.png            # Neumorphic background template
│   ├── icons/
│   │   ├── heart.svg
│   │   ├── kidney.svg
│   │   ├── nerves.svg
│   │   ├── retina.svg
│   │   └── full_body.svg
│   └── 3d_renders/
│       ├── full_body_controlled.png
│       ├── full_body_hyperglycemia.png
│       ├── heart_controlled.png
│       ├── heart_hyperglycemia.png
│       ├── kidney_controlled.png
│       ├── kidney_hyperglycemia.png
│       ├── nerves_controlled.png
│       ├── nerves_hyperglycemia.png
│       ├── retina_controlled.png
│       └── retina_hyperglycemia.png
│
└── screenshots/
    ├── full_dashboard_overview.png
    ├── kidney_hyperglycemia_view.png
    └── retina_controlled_view.png

```

---

## 💻 Setup & Reproduction Guide

### Prerequisites

* [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (Latest Version)
* Git installed on your local machine

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/<your-username>/diabetic-neuropathy-risk-analysis.git
cd diabetic-neuropathy-risk-analysis

```


2. **Open the Project:**
* Double-click `Diabetic_Neuropathy_Health_Risk_Analysis.pbix` to launch the dashboard in Power BI Desktop.


3. **Verify Data Source Paths (If Prompted):**
* In Power BI Desktop, navigate to **Home** $\rightarrow$ **Transform data** $\rightarrow$ **Data source settings**.
* If the CSV paths need relinking, point them to the files inside your local `/dataset` directory.
* Click **Apply changes**.


4. **Verify Image Category Settings:**
* Go to the **Data View** $\rightarrow$ select the `Image_Lookup` table.
* Click the `Image_URL` column header.
* Under the **Column tools** tab, ensure **Data category** is set to `Image URL`.



---

## 🔍 Key Clinical Insights Uncovered

1. **HbA1c & Blood Pressure Synergy:** Patients in older age brackets (49–60 and 60+) with high HbA1c metrics show a significantly higher proportion of severe BP risk categories compared to younger groups.
2. **Insulin Dependency Escalation:** A direct positive curve exists between years living with diabetes and required daily insulin units, with accelerated dosage surges after year 15 of diagnosis.
3. **Organ Complication Density:** Renal (Kidney) and Peripheral Neuropathic conditions demonstrate higher average HbA1c baselines compared to systemic cohort averages, highlighting the vulnerability of microvascular capillary networks to sustained glycemic stress.

---

## 🛠️ Tools & Technologies Used

* **Business Intelligence & ETL:** Microsoft Power BI Desktop, Power Query
* **Analytical Querying:** DAX (Data Analysis Expressions)
* **UI/UX Design:** Microsoft PowerPoint (Vector Canvas & Container Design)
* **Version Control & Hosting:** Git, GitHub, GitHub Pages (Iframe embed ready)
