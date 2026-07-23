import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    'data' is a list of dictionaries containing the assignment records.
    Implements grade validation, weight validation, GPA calculation,
    pass/fail decision, and resubmission logic.
    """
    print("\n--- Processing Grades ---")

    # ------------------------------------------------------------------
    # Handle the case of an empty CSV (e.g. right after organizer.sh runs)
    # ------------------------------------------------------------------
    if not data:
        print("Error: No assignment records found. The CSV file appears to be empty.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # a) Grade Validation: every score must be between 0 and 100
    # ------------------------------------------------------------------
    invalid_scores = [row for row in data if not (0 <= row['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have an invalid score (must be 0-100):")
        for row in invalid_scores:
            print(f"  - {row['assignment']}: {row['score']}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # b) Weight Validation: Total = 100, Summative = 40, Formative = 60
    # ------------------------------------------------------------------
    total_weight = sum(row['weight'] for row in data)
    summative_weight = sum(row['weight'] for row in data if row['group'] == 'Summative')
    formative_weight = sum(row['weight'] for row in data if row['group'] == 'Formative')

    errors = []
    if abs(total_weight - 100) > 1e-9:
        errors.append(f"Total weight must equal 100, but got {total_weight}.")
    if abs(summative_weight - 40) > 1e-9:
        errors.append(f"Summative weights must sum to 40, but got {summative_weight}.")
    if abs(formative_weight - 60) > 1e-9:
        errors.append(f"Formative weights must sum to 60, but got {formative_weight}.")

    if errors:
        print("Error: Weight validation failed.")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # c) GPA Calculation
    #    Total Grade = sum(score * weight) / 100   (weighted overall score)
    #    GPA = (Total Grade / 100) * 5.0
    # ------------------------------------------------------------------
    total_grade = sum(row['score'] * row['weight'] for row in data) / 100
    gpa = (total_grade / 100) * 5.0

    # ------------------------------------------------------------------
    # Category percentages (used for the 50% pass rule in EACH category)
    # percentage = weighted points earned in group / total weight of group * 100
    # ------------------------------------------------------------------
    summative_points = sum(row['score'] * row['weight'] for row in data if row['group'] == 'Summative') / 100
    formative_points = sum(row['score'] * row['weight'] for row in data if row['group'] == 'Formative') / 100

    summative_pct = (summative_points / summative_weight) * 100
    formative_pct = (formative_points / formative_weight) * 100

    # ------------------------------------------------------------------
    # d) Final Decision: must be >= 50% in BOTH categories
    # ------------------------------------------------------------------
    passed = summative_pct >= 50 and formative_pct >= 50
    status = "PASSED" if passed else "FAILED"

    # ------------------------------------------------------------------
    # e) Resubmission Logic: failed formative assignments (score < 50)
    #    Only the one(s) with the HIGHEST weight among the failed
    #    formative assignments are eligible. Ties are all included.
    # ------------------------------------------------------------------
    failed_formatives = [
        row for row in data
        if row['group'] == 'Formative' and row['score'] < 50
    ]

    resubmission_candidates = []
    if failed_formatives:
        max_weight = max(row['weight'] for row in failed_formatives)
        resubmission_candidates = [
            row['assignment'] for row in failed_formatives if row['weight'] == max_weight
        ]

    # ------------------------------------------------------------------
    # f) Print the final report
    # ------------------------------------------------------------------
    print(f"Summative Score: {summative_pct:.2f}% (weight check: {summative_weight})")
    print(f"Formative Score: {formative_pct:.2f}% (weight check: {formative_weight})")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"Final GPA: {gpa:.2f} / 5.0")
    print(f"Final Status: {status}")

    if resubmission_candidates:
        print("Eligible for resubmission (highest-weight failed formative assignment(s)):")
        for name in resubmission_candidates:
            print(f"  - {name}")
    else:
        print("No formative assignments are eligible for resubmission.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
