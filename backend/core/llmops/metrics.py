"""
LLMOps Telemetry, Latency, Token Cost, and Hallucination Risk Tracking.
"""
import time
from typing import Dict, Any, List


class TelemetryTracker:
    """Tracks latency, token usage, cost estimations, and drift/hallucination indicators."""

    def __init__(self):
        self.step_timings: Dict[str, float] = {}
        self.start_times: Dict[str, float] = {}
        self.token_metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        self.rates = {
            # Standard frontier model rates per 1M tokens ($)
            "prompt_per_1m": 3.00,
            "completion_per_1m": 15.00
        }

    def start_phase(self, phase_name: str):
        self.start_times[phase_name] = time.perf_counter()

    def end_phase(self, phase_name: str) -> float:
        start = self.start_times.get(phase_name, time.perf_counter())
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        self.step_timings[phase_name] = elapsed_ms
        return elapsed_ms

    def record_tokens(self, prompt_text: str, completion_text: str):
        # Approximation: ~4 chars per token for English & code
        p_tokens = max(1, len(prompt_text) // 4)
        c_tokens = max(1, len(completion_text) // 4)
        self.token_metrics["prompt_tokens"] += p_tokens
        self.token_metrics["completion_tokens"] += c_tokens
        self.token_metrics["total_tokens"] = (
            self.token_metrics["prompt_tokens"] + self.token_metrics["completion_tokens"]
        )

    def calculate_cost(self) -> float:
        p_cost = (self.token_metrics["prompt_tokens"] / 1_000_000) * self.rates["prompt_per_1m"]
        c_cost = (self.token_metrics["completion_tokens"] / 1_000_000) * self.rates["completion_per_1m"]
        return round(p_cost + c_cost, 6)

    def compute_hallucination_risk(self, code_syntactically_valid: bool, tests_passed: int, total_tests: int, security_score: int) -> Dict[str, Any]:
        """
        Calculates an objective risk score (0-100%, lower is safer).
        Considers syntax validity, test pass ratio, and security score.
        """
        risk = 0
        factors: List[str] = []

        if not code_syntactically_valid:
            risk += 50
            factors.append("AST compilation error in generated code")

        if total_tests > 0:
            failed_ratio = (total_tests - tests_passed) / total_tests
            test_penalty = int(failed_ratio * 40)
            risk += test_penalty
            if test_penalty > 0:
                factors.append(f"{total_tests - tests_passed}/{total_tests} unit tests failed")
        else:
            risk += 25
            factors.append("Zero automated test coverage generated")

        if security_score < 70:
            risk += 20
            factors.append(f"Security score below threshold ({security_score}/100)")

        risk = min(100, risk)
        return {
            "risk_score_pct": risk,
            "status": "LOW" if risk < 20 else "MODERATE" if risk < 50 else "HIGH",
            "contributing_factors": factors
        }

    def get_summary(self) -> Dict[str, Any]:
        total_latency = round(sum(self.step_timings.values()), 2)
        return {
            "total_latency_ms": total_latency,
            "phase_latencies_ms": self.step_timings,
            "token_usage": self.token_metrics,
            "estimated_cost_usd": self.calculate_cost()
        }
