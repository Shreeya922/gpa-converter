

def calculate_weighted_gpa(subjects):
    total_points = 0
    total_credits = 0

    for subject in subjects:
        grade_point = subject["grade_point"]
        credit = subject["credit"]

        total_points += grade_point * credit
        total_credits += credit

    if total_credits == 0:
        return 0

    return total_points / total_credits
