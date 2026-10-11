"""
Synthetic Dataset Generator for EduPulse AI
Generates 1,200 realistic student academic and engagement records for model training and demo analytics.
"""

import os
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def generate_student_dataset(n_samples=1200, seed=42):
    np.random.seed(seed)
    
    first_names = [
        "Aarav", "Alex", "Ananya", "Ben", "Chloe", "David", "Elena", "Farhan",
        "Grace", "Hassan", "Isabella", "Jack", "Kavya", "Liam", "Maya", "Noah",
        "Olivia", "Parth", "Quinn", "Rohan", "Sofia", "Tariq", "Uma", "Victor",
        "Wyatt", "Ximena", "Yusuf", "Zoe", "Aria", "Brandon", "Camila", "Daniel"
    ]
    
    last_names = [
        "Sharma", "Smith", "Patel", "Johnson", "Gupta", "Williams", "Khan", "Brown",
        "Singh", "Jones", "Rao", "Garcia", "Verma", "Miller", "Mehta", "Davis",
        "Chaudhary", "Rodriguez", "Joshi", "Martinez", "Kumar", "Hernandez", "Deshmukh", "Lopez"
    ]
    
    majors = [
        "Computer Science", "Data Science", "Cyber Security", 
        "Business Analytics", "Mechanical Engineering", "Health Sciences"
    ]
    
    grade_levels = ["Freshman", "Sophomore", "Junior", "Senior"]
    
    student_ids = [f"EDU-2026-{1001 + i}" for i in range(n_samples)]
    names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_samples)]
    selected_majors = np.random.choice(majors, size=n_samples, p=[0.25, 0.20, 0.15, 0.15, 0.15, 0.10])
    selected_grades = np.random.choice(grade_levels, size=n_samples, p=[0.30, 0.28, 0.22, 0.20])
    
    # Latent student capability / engagement index (-2 to +2)
    latent_capability = np.random.normal(0, 1, size=n_samples)
    
    # Generate realistic correlated academic metrics based on latent capability
    attendance_rate = np.clip(78 + latent_capability * 12 + np.random.normal(0, 5, n_samples), 45.0, 100.0)
    gpa = np.clip(3.0 + latent_capability * 0.5 + np.random.normal(0, 0.2, n_samples), 1.2, 4.0)
    assignment_completion_rate = np.clip(80 + latent_capability * 14 + np.random.normal(0, 6, n_samples), 40.0, 100.0)
    midterm_score = np.clip(75 + latent_capability * 13 + np.random.normal(0, 7, n_samples), 35.0, 100.0)
    study_hours_per_week = np.clip(16 + latent_capability * 6 + np.random.normal(0, 3, n_samples), 2.0, 38.0)
    lms_engagement_score = np.clip(70 + latent_capability * 15 + np.random.normal(0, 8, n_samples), 20.0, 100.0)
    participation_score = np.clip(72 + latent_capability * 12 + np.random.normal(0, 7, n_samples), 20.0, 100.0)
    
    # Stress level inversely related to support / performance (1 to 10 scale)
    stress_level = np.clip(np.round(6 - latent_capability * 1.5 + np.random.normal(0, 1.2, n_samples)), 1, 10).astype(int)
    
    tuition_status = np.random.choice(["Paid", "Pending"], size=n_samples, p=[0.82, 0.18])
    
    # Calculate Academic Risk Index (0 - 100 scale)
    # Higher score = Higher risk of academic failure
    risk_score = (
        (100 - attendance_rate) * 0.25 +
        ((4.0 - gpa) / 4.0 * 100) * 0.25 +
        (100 - assignment_completion_rate) * 0.20 +
        (100 - midterm_score) * 0.15 +
        ((35 - study_hours_per_week) / 35 * 100) * 0.10 +
        (stress_level / 10 * 100) * 0.05 +
        np.random.normal(0, 4, n_samples)
    )
    risk_score = np.clip(risk_score, 0, 100)
    
    # Classify risk level based on risk score thresholds
    def get_risk_category(score):
        if score >= 50.0:
            return "High"
        elif score >= 32.0:
            return "Medium"
        else:
            return "Low"
            
    risk_levels = [get_risk_category(s) for s in risk_score]
    
    df = pd.DataFrame({
        "student_id": student_ids,
        "name": names,
        "grade_level": selected_grades,
        "major": selected_majors,
        "attendance_rate": np.round(attendance_rate, 1),
        "gpa": np.round(gpa, 2),
        "assignment_completion_rate": np.round(assignment_completion_rate, 1),
        "midterm_score": np.round(midterm_score, 1),
        "study_hours_per_week": np.round(study_hours_per_week, 1),
        "lms_engagement_score": np.round(lms_engagement_score, 1),
        "participation_score": np.round(participation_score, 1),
        "stress_level": stress_level,
        "tuition_status": tuition_status,
        "risk_level": risk_levels
    })
    
    return df

def main():
    os.makedirs("data", exist_ok=True)
    df = generate_student_dataset(n_samples=1200)
    
    output_path = os.path.join("data", "students_1200.csv")
    df.to_csv(output_path, index=False)
    
    print(f"[SUCCESS] Generated dataset with {len(df)} student records at '{output_path}'")
    print("\nRisk Level Distribution:")
    print(df["risk_level"].value_counts(normalize=True).map("{:.1%}".format))

if __name__ == "__main__":
    main()
