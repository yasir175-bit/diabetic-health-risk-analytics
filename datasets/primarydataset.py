import numpy as np
import pandas as pd

np.random.seed(42)
n_records = 1500

# 1. Demographics
age = np.random.randint(22, 82, size=n_records)
gender = np.random.choice(["Male", "Female"], size=n_records, p=[0.51, 0.49])
bmi = np.round(np.random.normal(loc=28.6, scale=4.6, size=n_records), 1)
bmi = np.clip(bmi, 18.5, 45.0)

# 2. Disease Progression & Biomarkers
years_with_diabetes = np.random.randint(1, 36, size=n_records)

# Higher duration & BMI increase HbA1c
hba1c_noise = np.random.normal(0, 0.65, size=n_records)
hba1c = np.round(
    5.4 + (years_with_diabetes * 0.11) + ((bmi - 25) * 0.08) + hba1c_noise, 1
)
hba1c = np.clip(hba1c, 5.2, 13.5)

# Fasting Glucose correlated with HbA1c
fasting_glucose = np.round(
    hba1c * 21.0 + np.random.normal(12, 10, size=n_records), 0
).astype(int)
fasting_glucose = np.clip(fasting_glucose, 75, 320)

# Daily Insulin units (Uncontrolled patients scale higher)
daily_insulin = np.where(
    hba1c >= 7.0,
    np.clip(
        np.round(
            years_with_diabetes * 1.7 + np.random.normal(12, 6, size=n_records)
        ),
        10,
        95,
    ),
    np.where(np.random.rand(n_records) > 0.65, np.random.randint(0, 18), 0),
).astype(int)

# 3. Clinical & Behavioral Factors
bp_risk = np.random.choice(
    ["High", "Normal", "Low"], size=n_records, p=[0.44, 0.40, 0.16]
)
physical_activity = np.random.choice(
    ["Sedentary", "Moderate", "High"], size=n_records, p=[0.52, 0.33, 0.15]
)
smoking_status = np.random.choice(
    ["Never", "Former", "Current"], size=n_records, p=[0.50, 0.26, 0.24]
)

# Binary Condition State based on ADA standard (HbA1c >= 7.0% is Uncontrolled/Chronic)
condition_state = np.where(
    hba1c >= 7.0, "Chronic Hyperglycemia", "Controlled Glucose"
)

# Organ selection logic
organs = ["Full Body", "Retina", "Kidney", "Heart", "Peripheral Nerves"]
primary_organ = np.random.choice(
    organs, size=n_records, p=[0.28, 0.18, 0.18, 0.18, 0.18]
)

# Age bins for grouping
age_bins = [18, 28, 38, 48, 58, 68, 100]
age_labels = ["18-28", "29-38", "39-48", "49-58", "59-68", "69+"]
age_group = pd.cut(
    age, bins=age_bins, labels=age_labels, right=True, include_lowest=True
)

# Build Fact DataFrame
df_patients = pd.DataFrame(
    {
        "Patient_ID": [f"PID_{i+1:04d}" for i in range(n_records)],
        "Age": age,
        "Age_Group": age_group,
        "Gender": gender,
        "BMI": bmi,
        "Years_With_Diabetes": years_with_diabetes,
        "Fasting_Glucose_mg_dL": fasting_glucose,
        "HbA1c_Percent": hba1c,
        "Daily_Insulin_Units": daily_insulin,
        "BP_Risk": bp_risk,
        "Physical_Activity": physical_activity,
        "Smoking_Status": smoking_status,
        "Condition_State": condition_state,
        "Affected_Organ": primary_organ,
    }
)

df_patients.to_csv("Fact_DiabeticPatients.csv", index=False)

# Build Dim_Organs
df_organs = pd.DataFrame(
    {
        "Organ_ID": [1, 2, 3, 4, 5],
        "Organ_Name": [
            "Full Body",
            "Retina",
            "Kidney",
            "Heart",
            "Peripheral Nerves",
        ],
        "Display_Order": [1, 2, 3, 4, 5],
    }
)
df_organs.to_csv("Dim_Organs.csv", index=False)

# Build Image_Lookup Table (10 combinations)
image_rows = []
for organ in df_organs["Organ_Name"]:
  for state in ["Controlled Glucose", "Chronic Hyperglycemia"]:
    organ_slug = organ.lower().replace(" ", "_")
    state_slug = "controlled" if state == "Controlled Glucose" else "damaged"
    # Placeholder URLs - we will link exact asset paths in Phase 2
    img_url = f"https://raw.githubusercontent.com/assets/diabetic_dashboard/{organ_slug}_{state_slug}.png"
    image_rows.append(
        {"Organ_Name": organ, "Condition_State": state, "Image_URL": img_url}
    )

df_images = pd.DataFrame(image_rows)
df_images.to_csv("Image_Lookup.csv", index=False)

print(f"Phase 1 Complete: 3 CSV files generated successfully.")