from typing import List, Dict, Any

class HealthScoreEngine:
    @staticmethod
    def calculate_score(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        penalty = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        secret_leaks = 0
        
        # Penalties as per Constitution Section 6
        for f in findings:
            sev = f.get("severity", "low").lower()
            if f.get("category") == "secrets":
                secret_leaks += 1
                penalty += 20
            elif sev == "critical":
                critical_count += 1
                penalty += min(15, 60 / (critical_count or 1)) # Simplified cap logic for MVP
            elif sev == "high":
                high_count += 1
                penalty += 5
            elif sev == "medium":
                medium_count += 1
                penalty += 2
            elif sev == "low":
                low_count += 0.5
                low_count += 1 # Tracking count
        
        # Cap logic refinement
        critical_penalty = min(critical_count * 15, 60)
        high_penalty = min(high_count * 5, 30)
        medium_penalty = min(medium_count * 2, 20)
        low_penalty = min(int(low_count) * 0.5, 10)
        secret_penalty = secret_leaks * 20
        
        total_penalty = critical_penalty + high_penalty + medium_penalty + low_penalty + secret_penalty
        score = max(0, min(100, 100 - total_penalty))
        
        # Grade mapping
        grade = "F"
        if score >= 90: grade = "A"
        elif score >= 75: grade = "B"
        elif score >= 60: grade = "C"
        elif score >= 40: grade = "D"
        
        return {
            "score": int(score),
            "grade": grade,
            "counts": {
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": int(low_count),
                "secrets": secret_leaks
            }
        }
