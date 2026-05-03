import heapq


def split_values(value):
    return [item.strip().lower() for item in str(value).split("|") if item.strip()]


def rank_with_astar(profile, degrees):
    open_list = []
    ranked = []

    for index, row in degrees.iterrows():
        score = calculate_score(profile, row)
        missing = calculate_missing_cost(profile, row)
        priority = -(score - missing)
        heapq.heappush(open_list, (priority, index, row.to_dict(), score, missing))

    while open_list:
        priority, index, degree, score, missing = heapq.heappop(open_list)
        degree["score"] = max(0, min(100, score - missing))
        degree["missing_cost"] = missing
        degree["astar_value"] = abs(priority)
        ranked.append(degree)

    return ranked


def calculate_score(profile, degree):
    score = 0
    marks = int(profile.get("marks") or 0)
    min_marks = int(degree.get("min_marks") or 0)

    if marks >= min_marks:
        score += 25
    else:
        score += max(0, 20 - (min_marks - marks))

    profile_interests = [item.lower() for item in profile.get("interests", [])]
    degree_interests = split_values(degree.get("interests", ""))
    score += len(set(profile_interests) & set(degree_interests)) * 15

    profile_skills = [item.lower() for item in profile.get("skills", [])]
    degree_skills = split_values(degree.get("skills", ""))
    score += len(set(profile_skills) & set(degree_skills)) * 12

    if profile.get("preferred_work") == degree.get("preferred_work"):
        score += 12

    if profile.get("math_level") == degree.get("math_level"):
        score += 12

    if profile.get("goal") and profile.get("goal").lower() in degree.get("career_keywords", "").lower():
        score += 9

    return score


def calculate_missing_cost(profile, degree):
    cost = 0
    marks = int(profile.get("marks") or 0)
    min_marks = int(degree.get("min_marks") or 0)

    if marks < min_marks:
        cost += min(20, min_marks - marks)

    if profile.get("math_level") != degree.get("math_level"):
        cost += 5

    if profile.get("preferred_work") != degree.get("preferred_work"):
        cost += 4

    return cost
