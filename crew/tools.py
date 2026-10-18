from datetime import datetime
from typing import Any

from crewai.tools import tool


# ============================================================
# TOOL 1 — Naukri Knowledge Base Retrieval
# ============================================================

@tool("search_naukri_knowledge_base")
def search_naukri_knowledge_base(query: str) -> str:
    """
    Search the Naukri knowledge base for recruitment and
    job-application policy information.
    """

    query_lower = query.lower()

    policy_map = {
        "notice": "notice_period",
        "notice period": "notice_period",
        "remote": "remote_work",
        "work from home": "remote_work",
        "interview": "interview_scheduling",
        "background": "background_verification",
        "referral": "referral_bonus",
        "offer": "offer_negotiation",
        "negotiat": "offer_negotiation",
        "internal transfer": "internal_transfer",
        "probation": "probation",
        "diversity": "diversity_hiring",
        "exit interview": "exit_interview",
        "retention": "applicant_data_retention",
        "data retention": "applicant_data_retention",
        "eligibility": "job_application_eligibility",
        "application": "job_application_eligibility",
    }

    matched_policy = None

    for keyword, policy in policy_map.items():
        if keyword in query_lower:
            matched_policy = policy
            break

    if matched_policy is None:
        return (
            "No directly matching Naukri policy was found in the "
            "knowledge-base tool."
        )

    responses = {
        "notice_period": (
            "Notice-period requirements depend on the employer and "
            "specific role. Candidates should review the job posting "
            "and applicable employer requirements."
        ),
        "remote_work": (
            "Remote-work availability depends on the employer and "
            "specific job role. Check the job posting for the applicable "
            "work arrangement."
        ),
        "interview_scheduling": (
            "Interview scheduling depends on the employer's recruitment "
            "process. Candidates should follow the interview instructions "
            "provided for their application."
        ),
        "background_verification": (
            "Background verification may be part of the hiring process. "
            "Employers may verify information relevant to the role before "
            "completing the hiring process."
        ),
        "referral_bonus": (
            "Referral benefits depend on the applicable referral policy "
            "and eligibility requirements."
        ),
        "offer_negotiation": (
            "Offer negotiation depends on the employer's hiring policy "
            "and the terms of the offer."
        ),
        "internal_transfer": (
            "Internal-transfer eligibility depends on the employer's "
            "internal mobility policy and employee eligibility."
        ),
        "probation": (
            "Probation terms depend on the employer and role. Candidates "
            "should review the employment terms provided by the employer."
        ),
        "diversity_hiring": (
            "Diversity hiring practices depend on the employer's "
            "recruitment practices and applicable requirements."
        ),
        "exit_interview": (
            "An exit interview is a discussion conducted when an employee "
            "leaves an organization to collect feedback about employment."
        ),
        "applicant_data_retention": (
            "Applicant-data retention is governed by the applicable "
            "recruitment and data-retention policy."
        ),
        "job_application_eligibility": (
            "Job-application eligibility depends on the requirements "
            "specified for the particular job posting."
        ),
    }

    return responses[matched_policy]


# ============================================================
# TOOL 2 — Application Status Lookup
# ============================================================

APPLICATIONS = {
    "APP1001": {
        "record_id": "APP1001",
        "status": "Applied",
        "expected_salary_inr": 600000,
        "days_since_created": 5,
        "flagged_priority_review": False,
    },
    "APP1002": {
        "record_id": "APP1002",
        "status": "Interview Scheduled",
        "expected_salary_inr": 900000,
        "days_since_created": 12,
        "flagged_priority_review": True,
    },
    "APP1003": {
        "record_id": "APP1003",
        "status": "Screening",
        "expected_salary_inr": 750000,
        "days_since_created": 18,
        "flagged_priority_review": False,
    },
}


def calculate_escalation_score(
    flagged_priority_review: bool,
    days_since_created: int,
) -> float:
    """
    Escalation score:

    0.6 × priority flag
    +
    0.4 × normalized recency

    Recency is normalized over a 30-day window.

    Score range: 0.0–1.0
    """

    priority_score = 1.0 if flagged_priority_review else 0.0

    normalized_recency = min(max(days_since_created, 0), 30) / 30.0

    score = (
        0.6 * priority_score
        + 0.4 * normalized_recency
    )

    return round(score, 3)


@tool("check_job_application_status")
def check_job_application_status(record_id: str) -> str:
    """
    Check a Naukri job application and calculate its escalation score.

    The escalation score combines:
    - priority-review flag: 60%
    - normalized application age: 40%

    Scores >= 0.60 are recommended for priority review.
    """

    record_id = record_id.strip().upper()

    application = APPLICATIONS.get(record_id)

    if application is None:
        return (
            f"No application record was found for {record_id}. "
            "Please verify the application ID."
        )

    score = calculate_escalation_score(
        flagged_priority_review=application["flagged_priority_review"],
        days_since_created=application["days_since_created"],
    )

    escalation_threshold = 0.60

    priority_review = score >= escalation_threshold

    return (
        f"Application ID: {application['record_id']}\n"
        f"Status: {application['status']}\n"
        f"Expected Salary (INR): {application['expected_salary_inr']}\n"
        f"Days Since Created: {application['days_since_created']}\n"
        f"Priority Flag: {application['flagged_priority_review']}\n"
        f"Escalation Score: {score:.3f}\n"
        f"Priority Review Required: {priority_review}\n"
        f"Escalation Formula: "
        f"0.6 × priority_flag + 0.4 × normalized_recency\n"
        f"Escalation Threshold: {escalation_threshold}"
    )