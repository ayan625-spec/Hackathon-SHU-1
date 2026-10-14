from typing import List, Dict, Any

class HealthScoreEngine:
    @staticmethod
    def calculate_score(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        # --- Counters only (no penalty logic here) ---
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        secret_leaks = 0

        for f in findings:
            sev = f.get("severity", "low").lower()
            if f.get("category") == "secrets":
                secret_leaks += 1
            elif sev == "critical":
                critical_count += 1
            elif sev == "high":
                high_count += 1
            elif sev == "medium":
                medium_count += 1
            elif sev == "low":
                low_count += 1  # count only — penalty calculated below

        # --- Penalty calculation (single source of truth, with caps) ---
        critical_penalty = min(critical_count * 15, 60)
        high_penalty     = min(high_count * 5,      30)
        medium_penalty   = min(medium_count * 2,    20)
        low_penalty      = min(low_count * 0.5,     10)
        secret_penalty   = min(secret_leaks * 20,   40)

        total_penalty = (
            critical_penalty
            + high_penalty
            + medium_penalty
            + low_penalty
            + secret_penalty
        )

        score = max(0, min(100, 100 - total_penalty))

        if score >= 90:   grade = "A"
        elif score >= 75: grade = "B"
        elif score >= 60: grade = "C"
        elif score >= 40: grade = "D"
        else:             grade = "F"

        return {
            "score": int(score),
            "grade": grade,
            "counts": {
                "critical": critical_count,
                "high":     high_count,
                "medium":   medium_count,
                "low":      low_count,
                "secrets":  secret_leaks,
            },
        }
