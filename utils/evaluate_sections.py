import json
import os

LABELED_PATH = "dataset/labeled_samples"
PREDICTED_PATH = "output/results/resume_sections.json"


def calculate_accuracy(predicted, labeled):

    correct = 0
    total = len(labeled)

    for section in labeled:
        if section in predicted and predicted[section].strip() != "":
            correct += 1

    return correct, total


def evaluate():

    scores = []
    report_lines = []

    for file in os.listdir(LABELED_PATH):

        labeled_file = os.path.join(LABELED_PATH, file)

        with open(labeled_file, encoding="utf-8") as f:
            labeled = json.load(f)

        with open(PREDICTED_PATH, encoding="utf-8") as f:
            predicted = json.load(f)

        correct, total = calculate_accuracy(predicted, labeled)

        accuracy = correct / total
        scores.append(accuracy)

        report_lines.append(
            f"{file} → {correct}/{total} = {accuracy:.2f}"
        )

    avg_accuracy = sum(scores) / len(scores)

    print("\n📊 Section Detection Accuracy:", avg_accuracy)

    # Save report
    os.makedirs("reports", exist_ok=True)

    with open("reports/section_accuracy.txt", "w", encoding="utf-8") as r:
        r.write("SECTION DETECTION REPORT\n\n")

        for line in report_lines:
            r.write(line + "\n")

        r.write(f"\nAverage Accuracy: {avg_accuracy:.2f}")


if __name__ == "__main__":
    evaluate()