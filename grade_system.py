
# grade_system.py

# Example grading scale.
# These are configurable example values,
# not the official rules of every university.

DEFAULT_SCALE = [
    {"grade": "A", "minimum": 90, "point": 4.0},
    {"grade": "A-", "minimum": 85, "point": 3.7},
    {"grade": "B+", "minimum": 80, "point": 3.3},
    {"grade": "B", "minimum": 75, "point": 3.0},
    {"grade": "B-", "minimum": 70, "point": 2.7},
    {"grade": "C+", "minimum": 65, "point": 2.3},
    {"grade": "C", "minimum": 60, "point": 2.0},
    {"grade": "C-", "minimum": 55, "point": 1.7},
    {"grade": "D", "minimum": 50, "point": 1.0},
    {"grade": "F", "minimum": 0, "point": 0.0},
]


def validate_scale(scale):

    if not scale:
        raise ValueError("Grading scale cannot be empty.")

    grades = []
    minimums = []

    for item in scale:
        grade = str(item["grade"]).strip()
        minimum = float(item["minimum"])
        point = float(item["point"])

        if not grade:
            raise ValueError("Grade name cannot be empty.")

        if not 0 <= minimum <= 100:
            raise ValueError("Minimum percentage must be between 0 and 100.")

        if not 0 <= point <= 5:
            raise ValueError("Grade point must be between 0 and 5.")

        if grade in grades:
            raise ValueError("Duplicate grade names are not allowed.")

        if minimum in minimums:
            raise ValueError("Minimum percentages must be unique.")

        grades.append(grade)
        minimums.append(minimum)

    if 0 not in minimums:
        raise ValueError("A grade range must start at 0%.")

    return True


def get_grade(percentage, scale):

    validate_scale(scale)

    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")

    sorted_scale = sorted(
        scale,
        key=lambda item: float(item["minimum"]),
        reverse=True
    )

    for item in sorted_scale:

        if percentage >= float(item["minimum"]):
            return item["grade"], float(item["point"])

    raise ValueError("No matching grade found.")


def percentage_to_gpa(percentage, maximum_gpa=4.0):

    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")

    if not 0 < maximum_gpa <= 5:
        raise ValueError("Invalid GPA scale.")

    return (percentage / 100) * maximum_gpa
