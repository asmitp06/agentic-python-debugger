def normalize_scores(scores):
    # Fix for line 6: If scores are already within the 0-100 range,
    # assume they are pre-normalized and return them directly.
    # Removed the block to ensure consistent normalization.

    min_score = min(scores)
    max_score = max(scores)
    normalized = []

    # Handle the case where min_score == max_score to avoid division by zero
    if (max_score - min_score) == 0:
        return [100.0 for _ in scores] # All scores are the same, normalize to 100

    for s in scores:
        norm = (s - min_score) / (max_score - min_score) * 100
        normalized.append(norm)

    return normalized


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
    # Class average calculation and printing moved to main
    # avg = class_average([r["normalized"] for r in report])
    # print("Class Average:", avg)


def main():
    scores = [72, 88, 95, 63, 79, 84, 91, 55]

    report = build_report(scores)
    print_report(report)

    normalized_scores_for_avg = [r["normalized"] for r in report]
    avg = class_average(normalized_scores_for_avg)
    print("Class Average:", avg) # Print average here

    if avg > 85:
        print("Great class performance!")
    else:
        print("Needs improvement.")


if __name__ == "__main__":
    main()