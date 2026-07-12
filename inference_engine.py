from dataclasses import dataclass, field

@dataclass
class DiagnosisResult:
    """Represents one ranked diagnosis returned by the inference engine."""
    rule_id: str
    diagnosis: str
    explanation: str
    advice: str
    confidence: float                 # 0.0 - 1.0
    matched_symptoms: set = field(default_factory=set)
    missing_symptoms: set = field(default_factory=set)

    @property
    def confidence_percent(self) -> str:
        return f"{round(self.confidence * 100)}%"


class ExpertSystemEngine:
    """
    A lightweight forward-chaining inference engine.

    Usage:
        engine = ExpertSystemEngine(RULES)
        results = engine.diagnose({"no_power"})
    """

    def __init__(self, rules):
        if not rules:
            raise ValueError("Rule base cannot be empty.")
        self.rules = rules

    def diagnose(self, reported_symptoms: set) -> list:
        """
        Compare the reported symptoms against every rule and return a
        list of DiagnosisResult objects sorted best-match-first.

        Args:
            reported_symptoms: a set of symptom codes the user selected.

        Returns:
            A list of DiagnosisResult, possibly empty if nothing matched
            at all.
        """
        if not reported_symptoms:
            return []

        results = []
        for rule in self.rules:
            required = rule["symptoms"]
            matched = required & reported_symptoms
            if not matched:
                continue  # this rule does not apply at all

            confidence = len(matched) / len(required)
            results.append(
                DiagnosisResult(
                    rule_id=rule["id"],
                    diagnosis=rule["diagnosis"],
                    explanation=rule["explanation"],
                    advice=rule["advice"],
                    confidence=confidence,
                    matched_symptoms=matched,
                    missing_symptoms=required - matched,
                )
            )

        # Rank: highest confidence first; for ties, more specific rules
        # (more required symptoms) rank higher, since they are backed by
        # more corroborating evidence.
        results.sort(
            key=lambda r: (r.confidence, len(r.matched_symptoms)),
            reverse=True,
        )
        return results

    def top_result(self, reported_symptoms: set, min_confidence: float = 0.5):
        """Convenience helper: return only the single best diagnosis, or
        None if no rule reaches the minimum confidence threshold."""
        results = self.diagnose(reported_symptoms)
        if results and results[0].confidence >= min_confidence:
            return results[0]
        return None