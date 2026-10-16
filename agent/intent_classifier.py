"""
Naukri Support Agent - Intent Classifier

Local rule-based intent classification.
No Gemini API call is required for intent classification.
"""


def classify_intent(question: str) -> str:
    """
    Classify a user question into a supported intent.
    """

    q = question.lower().strip()

    # Notice period
    if any(word in q for word in [
        "notice period",
        "notice",
        "serving notice",
        "notice duration"
    ]):
        return "notice_period"

    # Remote work
    if any(word in q for word in [
        "remote",
        "work from home",
        "wfh",
        "hybrid",
        "work remotely"
    ]):
        return "remote_work"

    # Interview
    if any(word in q for word in [
        "interview",
        "interviews",
        "interview scheduled",
        "interview schedule"
    ]):
        return "interview"

    # Background verification
    if any(word in q for word in [
        "background verification",
        "background check",
        "verification",
        "verify employment",
        "employment verification"
    ]):
        return "background_verification"

    # Job application
    if any(word in q for word in [
        "apply",
        "application",
        "job application",
        "how can i apply",
        "apply for a job"
    ]):
        return "job_application"

    # Referral
    if any(word in q for word in [
        "referral",
        "refer",
        "referral bonus"
    ]):
        return "referral"

    # Offer negotiation
    if any(word in q for word in [
        "offer",
        "salary negotiation",
        "negotiate salary",
        "compensation"
    ]):
        return "offer_negotiation"

    # Internal transfer
    if any(word in q for word in [
        "internal transfer",
        "transfer",
        "move to another team"
    ]):
        return "internal_transfer"

    # Probation
    if any(word in q for word in [
        "probation",
        "probation period"
    ]):
        return "probation"

    # Diversity
    if any(word in q for word in [
        "diversity",
        "equal opportunity",
        "inclusive hiring"
    ]):
        return "diversity_hiring"

    # Exit interview
    if any(word in q for word in [
        "exit interview",
        "leaving interview",
        "exit process"
    ]):
        return "exit_interview"

    # Applicant data
    if any(word in q for word in [
        "applicant data",
        "personal data",
        "candidate data",
        "data retention",
        "delete my data",
        "data privacy"
    ]):
        return "applicant_data_retention"

    # General fallback
    return "general"


def test_classifier():
    """
    Test the intent classifier.
    """

    test_questions = [
        "What is the notice period policy?",
        "Can I work remotely?",
        "How are interviews scheduled?",
        "What happens during background verification?",
        "How can I apply for a job?",
        "What is the referral bonus?",
        "Can I negotiate my salary?",
        "Can I transfer to another team?",
        "How long is the probation period?",
        "What is the diversity hiring policy?",
        "What happens in an exit interview?",
        "How long is applicant data retained?",
        "Hello, I need some help."
    ]

    print("=" * 70)
    print("INTENT CLASSIFICATION TEST")
    print("=" * 70)

    for question in test_questions:
        intent = classify_intent(question)

        print()
        print("Question:")
        print(question)
        print("Intent:")
        print(intent)


if __name__ == "__main__":
    test_classifier()