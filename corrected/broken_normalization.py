def normalize_scores(scores):
    # As per the bug report, for absolute grading with scores already on a 0-100 scale,
    # the scores should be used directly without relative normalization based on min/max of the current set.
    # This ensures that absolute grade cutoffs (e.g., 90 for A) are applied to the actual score values.
    return list(scores)


def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def class_average(scores):
    if not scores:
        return 0
    total = 0
    for s in scores:
        total = total + s
    return total / len(scores)


def build_report(scores):
    normalized = normalize_scores(scores)
    report = []

    for i in range(len(scores)):
        grade = assign_grade(normalized[i])
        report.append({
            "original": scores[i],
            "normalized": normalized[i],
            "grade": grade
        })

    return report


def print_report(report):
    print("Student Report")
    print("------------------")

    for r in report:
        print("Score:", r["original"],
              "Normalized:", round(r["normalized"], 2),
              "Grade:", r["grade"])

    avg = class_average([r["normalized"] for r in report])
    print("Class Average:", round(avg, 2))


def main():
    scores = [72, 88, 95, 63, 79, 84, 91, 55]

    report = build_report(scores)
    print_report(report)

    # Calculate avg in main scope for the conditional check
    normalized_scores_for_avg = [r["normalized"] for r in report]
    avg = class_average(normalized_scores_for_avg)

    if avg > 85:
        print("Great class performance!")
    else:
        print("Needs improvement.")


if __name__ == "__main__":
    main()