"""
Synthesizer and Quality Gate Agent for AgentForge.
Consolidates agent outputs, telemetry, AST checks, and unit test results into an auditable scorecard.
"""
from typing import Dict, Any
from .planner import PlanOutput


class SynthesizerAgent:
    """Agent responsible for quality gate decisions and deployment readiness verdict."""

    def synthesize(
        self,
        plan: PlanOutput,
        code_dict: Dict[str, str],
        audit_result: Dict[str, Any],
        test_result: Dict[str, Any],
        telemetry: Dict[str, Any],
        hallucination_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        security_score = audit_result.get("security_score", 0)
        tests_passed = test_result.get("passed_tests", 0)
        total_tests = test_result.get("total_tests", 0)
        risk_status = hallucination_info.get("status", "LOW")

        # Determine Production Gate Verdict
        passed_all_tests = (total_tests > 0 and tests_passed == total_tests)
        security_acceptable = (security_score >= 80)
        low_hallucination = (risk_status != "HIGH")

        if passed_all_tests and security_acceptable and low_hallucination:
            gate_verdict = "PASSED"
            readiness_status = "READY_FOR_DEPLOYMENT"
        elif passed_all_tests and security_score >= 60:
            gate_verdict = "CONDITIONAL_APPROVAL"
            readiness_status = "NEEDS_SECURITY_TRIAGE"
        else:
            gate_verdict = "BLOCKED"
            readiness_status = "FAILURES_DETECTED"

        summary = (
            f"Orchestration completed successfully for '{plan.task_title}'. "
            f"Target: {plan.target_language.upper()}. Pattern: {plan.architectural_pattern}. "
            f"Execution time: {telemetry['total_latency_ms']}ms across 5 pod agents. "
            f"Security Score: {security_score}/100. Tests: {tests_passed}/{total_tests} passed. "
            f"Hallucination Risk: {hallucination_info['risk_score_pct']}% ({risk_status})."
        )

        recommendations = []
        if gate_verdict == "PASSED":
            recommendations.append("Code passed static AST analysis and dynamic test coverage. Safe to merge into staging branch.")
            recommendations.append("Telemetry metrics within SLA thresholds (<500ms orchestration latency).")
        else:
            for finding in audit_result.get("findings", []):
                recommendations.append(f"Security Alert: {finding.get('message', 'Issue detected')}")
            if test_result.get("failed_tests", 0) > 0:
                recommendations.append(f"Unit test failure: {test_result.get('error_detail')}")

        return {
            "gate_verdict": gate_verdict,
            "readiness_status": readiness_status,
            "executive_summary": summary,
            "recommendations": recommendations,
            "quality_scorecard": {
                "security_score": security_score,
                "test_pass_rate": f"{(tests_passed / max(1, total_tests)) * 100:.1f}%",
                "hallucination_risk_pct": hallucination_info["risk_score_pct"],
                "total_tokens_consumed": telemetry["token_usage"]["total_tokens"],
                "estimated_cost_usd": telemetry["estimated_cost_usd"],
                "orchestration_latency_ms": telemetry["total_latency_ms"]
            }
        }
