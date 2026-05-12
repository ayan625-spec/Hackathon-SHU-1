class SeverityClassifier:
    @staticmethod
    def classify(severity_str: str) -> str:
        s = severity_str.lower()
        if s in ["critical", "error"]: return "critical"
        if s in ["high", "warning"]: return "high"
        if s in ["medium", "info"]: return "medium"
        return "low"
