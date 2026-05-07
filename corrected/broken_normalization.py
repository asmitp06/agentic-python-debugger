# Task: Given a list of student scores, normalize them (0–100 scale),
# assign letter grades, and print a summary report.

def normalize_scores(scores, max_possible_raw_score=100):
    # Assuming scores are already on a 0-100 scale and no curving is intended.
    # Return scores as floats.
    return [(s / max_possible_raw_score) * 100 for s in scores]


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


def build_report(scores, max_possible_raw_score=100):
    normalized = normalize_scores(scores, max_possible_raw_score)
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


def main():
    scores = [72, 88, 95, 63, 79, 84, 91, 55]

    report = build_report(scores, max_possible_raw_score=100)
    print_report(report)

    avg = class_average([r["normalized"] for r in report])
    print("Class Average:", round(avg, 2)) # Print average here as well

    if avg > 85:
        print("Great class performance!")
    else:
        print("Needs improvement.")


if __name__ == "__main__":
    main()