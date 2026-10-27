"""
Multi-Agent Orchestrator for AgentForge.
Coordinates pod execution across Planner, Generator, Security Auditor, Test Runner, and Synthesizer.
"""
from typing import Dict, Any, Optional
from .agents.planner import PlannerAgent
from .agents.generator import GeneratorAgent
from .agents.security_auditor import SecurityAuditorAgent
from .agents.test_runner import TestRunnerAgent
from .agents.synthesizer import SynthesizerAgent
from .llmops.guardrails import GuardrailEngine
from .llmops.metrics import TelemetryTracker


class MultiAgentOrchestrator:
    """
    Pod Orchestrator executing multi-agent workflow with stateful telemetry,
    observability gates, and automated code quality verification.
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.generator = GeneratorAgent()
        self.auditor = SecurityAuditorAgent()
        self.test_runner = TestRunnerAgent()
        self.synthesizer = SynthesizerAgent()

    def run_pipeline(self, prompt: str, target_language: str = "python") -> Dict[str, Any]:
        telemetry = TelemetryTracker()

        # Step 1: Input Guardrails
        is_safe, sanitized_prompt, guardrail_warnings = GuardrailEngine.inspect_prompt(prompt)
        if not is_safe:
            return {
                "status": "BLOCKED",
                "error": "Input prompt triggered security guardrail violation.",
                "warnings": guardrail_warnings,
                "sanitized_prompt": sanitized_prompt
            }

        # Step 2: Planning Phase
        telemetry.start_phase("planning")
        plan = self.planner.plan(sanitized_prompt, target_language=target_language)
        plan_ms = telemetry.end_phase("planning")

        # Step 3: Code Generation Phase
        telemetry.start_phase("code_generation")
        code_dict = self.generator.generate(plan)
        gen_ms = telemetry.end_phase("code_generation")
        telemetry.record_tokens(sanitized_prompt, code_dict["code"])

        # Step 4: Security and Static AST Audit Phase
        telemetry.start_phase("security_audit")
        audit_result = self.auditor.audit(code_dict["code"], language=code_dict["language"])
        audit_ms = telemetry.end_phase("security_audit")

        # Step 5: Test Generation and Sandboxed Execution Phase
        telemetry.start_phase("test_execution")
        test_result = self.test_runner.generate_and_run_tests(plan, code_dict)
        test_ms = telemetry.end_phase("test_execution")
        telemetry.record_tokens(code_dict["code"], test_result.get("test_code", ""))

        # Step 6: Observability, Drift, and Hallucination Evaluation
        hallucination_info = telemetry.compute_hallucination_risk(
            code_syntactically_valid=audit_result["is_syntactically_valid"],
            tests_passed=test_result["passed_tests"],
            total_tests=test_result["total_tests"],
            security_score=audit_result["security_score"]
        )

        telemetry_summary = telemetry.get_summary()

        # Step 7: Synthesis and Quality Gate Phase
        telemetry.start_phase("synthesis")
        synthesis_report = self.synthesizer.synthesize(
            plan=plan,
            code_dict=code_dict,
            audit_result=audit_result,
            test_result=test_result,
            telemetry=telemetry_summary,
            hallucination_info=hallucination_info
        )
        synth_ms = telemetry.end_phase("synthesis")
        # Update summary with final synthesis timing
        telemetry_summary["phase_latencies_ms"]["synthesis"] = synth_ms
        telemetry_summary["total_latency_ms"] = round(sum(telemetry_summary["phase_latencies_ms"].values()), 2)

        return {
            "status": "SUCCESS",
            "task_id": f"pod-{id(plan)}",
            "prompt": prompt,
            "sanitized_prompt": sanitized_prompt,
            "guardrail_warnings": guardrail_warnings,
            "plan": plan.model_dump() if hasattr(plan, "model_dump") else plan.dict(),
            "code": code_dict,
            "audit": audit_result,
            "test_results": test_result,
            "hallucination_evaluation": hallucination_info,
            "telemetry": telemetry_summary,
            "synthesis": synthesis_report
        }
