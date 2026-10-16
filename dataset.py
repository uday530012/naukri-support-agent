import random
from collections import Counter


# ============================================================
# NAUKRI.COM DOMAIN SUPPORT AGENT
# PART 1 - TASK 1
# DATASET GENERATOR
# ============================================================

# ------------------------------------------------------------
# 1. DATASET DESIGN CONFIGURATION
# ------------------------------------------------------------

# Fixed seed makes the dataset deterministic.
# Running the program again with the same seed produces
# the same dataset.
SEED = 42

# Number of job application records.
NUM_RECORDS = 50

# Required category vocabulary from the capstone.
CATEGORIES = [
    "Software Engineer",
    "Data Analyst",
    "Product Manager",
    "HR Executive",
    "Sales Associate"
]

# Required status vocabulary from the capstone.
STATUSES = [
    "Applied",
    "Screening",
    "Interview Scheduled",
    "Offered",
    "Rejected"
]

# Illustrative expected salary range in INR.
MIN_SALARY = 300000
MAX_SALARY = 3000000

# Salary is generated in increments of ₹50,000.
SALARY_STEP = 50000

# Priority flag probability.
# Approximately 20% of records should be priority cases.
PRIORITY_PROBABILITY = 0.20


# ------------------------------------------------------------
# 2. DATASET GENERATOR
# ------------------------------------------------------------

def generate_dataset():
    """
    Generate a deterministic list of job application records.

    Returns:
        list: JOB_APPLICATIONS containing 50 records.
    """

    # Set the seed so results are reproducible.
    random.seed(SEED)

    applications = []

    for i in range(1, NUM_RECORDS + 1):

        # Randomly select a job category.
        category = random.choice(CATEGORIES)

        # Randomly select application status.
        status = random.choice(STATUSES)

        # Generate realistic illustrative salary.
        expected_salary = random.randrange(
            MIN_SALARY,
            MAX_SALARY + 1,
            SALARY_STEP
        )

        # Application age between 0 and 30 days.
        days_since_created = random.randint(0, 30)

        # Approximately 20% of records are priority cases.
        flagged_priority_review = (
            random.random() < PRIORITY_PROBABILITY
        )

        # Create application record.
        record = {
            "record_id": f"APP{i:04d}",
            "category": category,
            "status": status,
            "expected_salary_inr": expected_salary,
            "days_since_created": days_since_created,
            "flagged_priority_review": flagged_priority_review
        }

        applications.append(record)

    return applications


# ------------------------------------------------------------
# 3. DATASET VALIDATION
# ------------------------------------------------------------

def validate_dataset(applications):
    """
    Validate the generated dataset against the capstone
    requirements.

    Raises:
        AssertionError if any requirement is not satisfied.
    """

    print("\nRunning dataset validation...")

    # --------------------------------------------------------
    # Check total number of records
    # --------------------------------------------------------

    assert len(applications) >= 40, (
        "ERROR: Dataset must contain at least 40 records."
    )

    # --------------------------------------------------------
    # Check required fields
    # --------------------------------------------------------

    required_fields = {
        "record_id",
        "category",
        "status",
        "expected_salary_inr",
        "days_since_created",
        "flagged_priority_review"
    }

    for record in applications:

        missing_fields = required_fields - set(record.keys())

        assert not missing_fields, (
            f"ERROR: Record {record.get('record_id')} "
            f"is missing fields: {missing_fields}"
        )

    # --------------------------------------------------------
    # Check record IDs are unique
    # --------------------------------------------------------

    record_ids = [
        record["record_id"]
        for record in applications
    ]

    assert len(record_ids) == len(set(record_ids)), (
        "ERROR: Duplicate record IDs found."
    )

    # --------------------------------------------------------
    # Check categories
    # --------------------------------------------------------

    category_counts = Counter(
        record["category"]
        for record in applications
    )

    for category in CATEGORIES:

        assert category_counts[category] >= 3, (
            f"ERROR: '{category}' must have at least "
            f"3 records. Found: {category_counts[category]}"
        )

    # --------------------------------------------------------
    # Check statuses
    # --------------------------------------------------------

    status_counts = Counter(
        record["status"]
        for record in applications
    )

    for status in STATUSES:

        assert status_counts[status] >= 1, (
            f"ERROR: '{status}' must appear at least once."
        )

    # --------------------------------------------------------
    # Check days_since_created
    # --------------------------------------------------------

    for record in applications:

        days = record["days_since_created"]

        assert isinstance(days, int), (
            f"ERROR: days_since_created must be an integer "
            f"for {record['record_id']}."
        )

        assert 0 <= days <= 30, (
            f"ERROR: days_since_created for "
            f"{record['record_id']} must be between 0 and 30."
        )

    # --------------------------------------------------------
    # Check salary
    # --------------------------------------------------------

    for record in applications:

        salary = record["expected_salary_inr"]

        assert MIN_SALARY <= salary <= MAX_SALARY, (
            f"ERROR: Salary for {record['record_id']} "
            f"is outside the allowed range."
        )

    # --------------------------------------------------------
    # Check priority flag
    # --------------------------------------------------------

    for record in applications:

        assert isinstance(
            record["flagged_priority_review"],
            bool
        ), (
            f"ERROR: flagged_priority_review must be "
            f"True or False for {record['record_id']}."
        )

    # --------------------------------------------------------
    # Calculate priority percentage
    # --------------------------------------------------------

    priority_count = sum(
        record["flagged_priority_review"]
        for record in applications
    )

    priority_percentage = (
        priority_count / len(applications)
    ) * 100

    assert 10 <= priority_percentage <= 30, (
        f"ERROR: Priority percentage is "
        f"{priority_percentage:.2f}%. "
        f"It must be between 10% and 30%."
    )

    print("Dataset validation: PASSED")

    return True


# ------------------------------------------------------------
# 4. DATASET REPORT
# ------------------------------------------------------------

def print_report(applications):
    """
    Print dataset statistics required by the capstone.
    """

    # Count records by category.
    category_counts = Counter(
        record["category"]
        for record in applications
    )

    # Count records by status.
    status_counts = Counter(
        record["status"]
        for record in applications
    )

    # Count priority records.
    priority_count = sum(
        record["flagged_priority_review"]
        for record in applications
    )

    # Calculate priority percentage.
    priority_percentage = (
        priority_count / len(applications)
    ) * 100

    print("\n")
    print("=" * 70)
    print("NAUKRI.COM JOB APPLICATION DATASET")
    print("=" * 70)

    print("\nDATASET DESIGN")
    print("-" * 70)

    print(f"Random seed: {SEED}")
    print(f"Number of records: {len(applications)}")

    print(
        f"Salary range: "
        f"₹{MIN_SALARY:,} - ₹{MAX_SALARY:,}"
    )

    print(
        f"Days since created: "
        f"0 - 30 days"
    )

    print(
        f"Priority probability: "
        f"{PRIORITY_PROBABILITY * 100:.0f}%"
    )

    # --------------------------------------------------------
    # Category report
    # --------------------------------------------------------

    print("\n")
    print("CATEGORY COUNTS")
    print("-" * 70)

    for category in CATEGORIES:

        count = category_counts[category]

        print(
            f"{category:<25} : {count}"
        )

    # --------------------------------------------------------
    # Status report
    # --------------------------------------------------------

    print("\n")
    print("STATUS COUNTS")
    print("-" * 70)

    for status in STATUSES:

        count = status_counts[status]

        print(
            f"{status:<25} : {count}"
        )

    # --------------------------------------------------------
    # Priority report
    # --------------------------------------------------------

    print("\n")
    print("PRIORITY REVIEW")
    print("-" * 70)

    print(
        f"Priority records     : {priority_count}"
    )

    print(
        f"Priority percentage  : "
        f"{priority_percentage:.2f}%"
    )

    # --------------------------------------------------------
    # Sample records
    # --------------------------------------------------------

    print("\n")
    print("FIRST 5 SAMPLE RECORDS")
    print("-" * 70)

    for record in applications[:5]:

        print(record)

    # --------------------------------------------------------
    # Dataset design reasoning
    # --------------------------------------------------------

    print("\n")
    print("SALARY RANGE REASONING")
    print("-" * 70)

    print(
        "The ₹3,00,000 to ₹30,00,000 illustrative salary range "
        "was selected to cover entry-level through experienced "
        "roles across the five job categories used in this "
        "capstone."
    )

    # --------------------------------------------------------
    # Reproducibility information
    # --------------------------------------------------------

    print("\n")
    print("REPRODUCIBILITY")
    print("-" * 70)

    print(
        f"Seed = {SEED}"
    )

    print(
        "Categories use uniform random selection."
    )

    print(
        "Statuses use uniform random selection."
    )

    print(
        f"Priority review uses approximately "
        f"{PRIORITY_PROBABILITY * 100:.0f}% probability."
    )

    print("\n")
    print("=" * 70)


# ------------------------------------------------------------
# 5. OPTIONAL: PRINT ALL RECORDS
# ------------------------------------------------------------

def print_all_records(applications):
    """
    Print every generated application record.
    """

    print("\n")
    print("=" * 70)
    print("ALL JOB APPLICATION RECORDS")
    print("=" * 70)

    for record in applications:
        print(record)


# ------------------------------------------------------------
# 6. MAIN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":

    # Generate the dataset.
    JOB_APPLICATIONS = generate_dataset()

    # Validate the dataset.
    validate_dataset(JOB_APPLICATIONS)

    # Print required statistics.
    print_report(JOB_APPLICATIONS)

    # Uncomment the following line if you want to see
    # all 50 records.
    #
    # print_all_records(JOB_APPLICATIONS)