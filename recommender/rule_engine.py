import json
import os
import pandas as pd

from recommender.scorer import rank_with_astar


class RecommendationEngine:
    def __init__(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(root, "data")
        self.degree_file = os.path.join(self.data_dir, "degree_rules.csv")
        self.career_file = os.path.join(self.data_dir, "career_map.csv")
        self.history_file = os.path.join(self.data_dir, "session_history.json")

    def load_degrees(self):
        return pd.read_csv(self.degree_file).fillna("")

    def load_careers(self):
        return pd.read_csv(self.career_file).fillna("")

    def recommend(self, profile):
        degrees = self.load_degrees()
        careers = self.load_careers()
        ranked = rank_with_astar(profile, degrees)

        best = ranked[0]
        matched_careers = careers[careers["degree"] == best["degree"]]

        return {
            "best": best,
            "ranked": ranked,
            "careers": matched_careers.to_dict("records"),
            "rules_used": self.explain_rules(profile, best)
        }

    def explain_rules(self, profile, best):
        rules = []
        marks = int(profile.get("marks") or 0)

        if marks >= int(best["min_marks"]):
            rules.append("eligible_by_marks")

        for skill in profile.get("skills", []):
            if skill.lower() in best["skills"].lower():
                rules.append("skill_match_" + skill.lower().replace(" ", "_"))

        for interest in profile.get("interests", []):
            if interest.lower() in best["interests"].lower():
                rules.append("interest_match_" + interest.lower().replace(" ", "_"))

        if profile.get("math_level") == best["math_level"]:
            rules.append("math_level_match")

        if not rules:
            rules.append("fallback_best_available_path")

        return rules

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file, "r") as file:
            return json.load(file)

    def save_history(self, profile, result):
        records = self.load_history()
        clean_result = {
            "best_degree": result["best"]["degree"],
            "score": result["best"]["score"],
            "careers": [career["career"] for career in result["careers"]]
        }
        records.insert(0, {"profile": profile, "result": clean_result})

        with open(self.history_file, "w") as file:
            json.dump(records[:25], file, indent=2)
