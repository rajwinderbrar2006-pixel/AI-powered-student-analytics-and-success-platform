"""
Academic Support Recommendation Engine for EduPulse AI
Generates personalized, actionable interventions based on risk level and specific student metrics.
"""

def generate_recommendations(student_data, risk_pred, placement_pred=None):
    """
    Generate customized academic & career recommendations for a student based on their profile.
    """

    predicted_risk = risk_pred["predicted_risk"]
    attendance = float(student_data["attendance_rate"])
    gpa = float(student_data["gpa"])
    assignment = float(student_data["assignment_completion_rate"])
    midterm = float(student_data["midterm_score"])
    study_hours = float(student_data["study_hours_per_week"])
    lms = float(student_data["lms_engagement_score"])
    stress = int(student_data["stress_level"])
    tuition = str(student_data.get("tuition_status", "Paid"))

    recommendations = []

    # Tier 1: Emergency & Priority Risk Interventions
    if predicted_risk == "High":
        recommendations.append({
            "category": "Emergency Intervention",
            "priority": "🔥 High Priority",
            "action": "Schedule Mandatory Academic Advisor Intake",
            "details": "Assign an academic success coach for bi-weekly 1-on-1 progress monitoring and individualized recovery roadmap."
        })
    elif predicted_risk == "Medium":
        recommendations.append({
            "category": "Proactive Support",
            "priority": "⚡ Medium Priority",
            "action": "Mid-Semester Success Check-in",
            "details": "Schedule a 30-minute academic consultation to review course load and study strategy before final exams."
        })

    # Tier 2: Specific Metric-Driven Interventions
    if attendance < 75.0:
        recommendations.append({
            "category": "Attendance Recovery",
            "priority": "⚠️ Critical Action",
            "action": "Attendance Contract & Absence Tracking",
            "details": f"Current attendance ({attendance}%) is below requirement (75%). Mandate lecture check-ins and provide access to recorded lectures."
        })

    if gpa < 2.5:
        recommendations.append({
            "category": "Academic Tutoring",
            "priority": "📚 Skill Building",
            "action": "Subject-Matter Peer Tutoring Enrollment",
            "details": f"GPA ({gpa:.2f}) indicates subject difficulty. Enroll student in 2 hours/week guided peer tutoring."
        })

    if assignment < 70.0:
        recommendations.append({
            "category": "Task Management",
            "priority": "📝 Habits",
            "action": "Time Management & Assignment Tracker Workshop",
            "details": f"Assignment completion rate ({assignment}%) is low. Provide digital organizer tools and assignment deadline reminders."
        })

    if midterm < 60.0:
        recommendations.append({
            "category": "Exam Remediation",
            "priority": "🎯 Academic Recovery",
            "action": "Remedial Study Session & Midterm Review",
            "details": f"Midterm score ({midterm}%) was below passing. Coordinate professor office hours and review practice exams."
        })

    if study_hours < 12.0:
        recommendations.append({
            "category": "Study Habits",
            "priority": "⏰ Efficiency",
            "action": "Structured Campus Study Group Placement",
            "details": f"Study hours ({study_hours} hrs/week) are insufficient. Recommend 15+ hours/week with peer study pods."
        })

    if lms < 60.0:
        recommendations.append({
            "category": "Digital Engagement",
            "priority": "💻 Tech Support",
            "action": "LMS Portal Orientation & Notification Setup",
            "details": f"LMS activity score ({lms}) is low. Assist student in configuring course notifications and mobile app access."
        })

    if stress >= 7:
        recommendations.append({
            "category": "Wellness & Health",
            "priority": "💚 Mental Health",
            "action": "Student Wellness & Counseling Referral",
            "details": f"Reported stress level ({stress}/10) is elevated. Offer confidential counseling services and stress management workshops."
        })

    if tuition.lower() == "pending":
        recommendations.append({
            "category": "Financial Services",
            "priority": "💳 Administrative",
            "action": "Financial Aid & Emergency Micro-Grant Counseling",
            "details": "Connect student with financial aid advisors to explore payment plans or emergency grant funding."
        })

    # Placement & Career Readiness Interventions
    if placement_pred is None:
        from src.model_utils import predict_placement_risk
        placement_pred = predict_placement_risk(student_data)

    p_risk = placement_pred.get("placement_risk", "Low")
    grade_level = str(student_data.get("grade_level", ""))

    if p_risk == "High":
        recommendations.append({
            "category": "Career Placement",
            "priority": "💼 Priority Action",
            "action": "Career Services Intake & Technical Portfolio Audit",
            "details": f"Placement readiness risk is High (Score: {placement_pred.get('placement_score', 0)}/100). Mandate resume review, portfolio audit, and mock interview coaching."
        })
    elif p_risk == "Medium" and grade_level in ["Junior", "Senior"]:
        recommendations.append({
            "category": "Career Placement",
            "priority": "🎯 Career Prep",
            "action": "Industry Mock Interview & Skill Bootcamp Enrollment",
            "details": f"Student in {grade_level} year shows moderate placement readiness ({placement_pred.get('placement_score', 0)}/100). Enroll in campus career bootcamp & interview prep."
        })

    # Default positive reinforcement for low risk / strong performers
    if predicted_risk == "Low" and len(recommendations) == 0:
        recommendations.append({
            "category": "Enrichment",
            "priority": "🌟 Growth",
            "action": "Honors & Leadership / Research Opportunity",
            "details": "Student is performing strongly across all metrics. Recommend peer mentoring roles, undergraduate research, or honors programs."
        })

    return recommendations
