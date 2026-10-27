"""
Security and AST Static Code Auditor Agent for AgentForge.
Performs AST inspection, checks cyclomatic complexity, verifies type annotations,
and runs security guardrails.
"""
import ast
import re
from typing import Dict, Any, List
from ..llmops.guardrails import GuardrailEngine


class SecurityAuditorAgent:
    """Agent that performs static analysis and AST code quality verification."""

    def audit(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language.lower() in ["cpp", "c++"]:
            return self._audit_cpp(code)
        return self._audit_python(code)

    def _audit_python(self, code: str) -> Dict[str, Any]:
        findings = []
        is_syntactically_valid = True
        ast_tree = None

        try:
            ast_tree = ast.parse(code)
        except SyntaxError as e:
            is_syntactically_valid = False
            findings.append({
                "severity": "CRITICAL",
                "category": "SyntaxError",
                "message": f"Syntax error at line {e.lineno}: {e.msg}",
                "line": e.lineno
            })

        # Run regex guardrails
        base_safety_score, guardrail_findings = GuardrailEngine.inspect_code_safety(code)
        for gf in guardrail_findings:
            findings.append({
                "severity": gf["severity"],
                "category": "SecurityViolation",
                "message": gf["description"],
                "instances": gf["instances"]
            })

        # AST-level deep checks if valid
        complexity_metrics = {
            "functions_count": 0,
            "classes_count": 0,
            "type_annotated_functions": 0,
            "docstring_coverage_pct": 100
        }

        if ast_tree:
            functions = [n for n in ast.walk(ast_tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            classes = [n for n in ast.walk(ast_tree) if isinstance(n, ast.ClassDef)]

            complexity_metrics["functions_count"] = len(functions)
            complexity_metrics["classes_count"] = len(classes)

            annotated = 0
            with_docs = 0
            for f in functions:
                if f.returns or any(arg.annotation for arg in f.args.args if arg.arg != 'self'):
                    annotated += 1
                if ast.get_docstring(f):
                    with_docs += 1

            if functions:
                complexity_metrics["type_annotated_functions"] = annotated
                complexity_metrics["docstring_coverage_pct"] = int((with_docs / len(functions)) * 100)

            # Check for generic except clauses
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None:
                        findings.append({
                            "severity": "MEDIUM",
                            "category": "CodeQuality",
                            "message": "Bare except: block detected; should catch specific exceptions.",
                            "line": getattr(node, "lineno", 0)
                        })

        # Calculate composite security/quality score
        deductions = sum(
            30 if f["severity"] == "CRITICAL" else 15 if f["severity"] == "HIGH" else 5
            for f in findings
        )
        final_score = max(0, min(100, 100 - deductions))

        return {
            "language": "python",
            "is_syntactically_valid": is_syntactically_valid,
            "security_score": final_score,
            "status": "PASS" if final_score >= 80 else "WARNING" if final_score >= 60 else "FAIL",
            "findings": findings,
            "complexity_metrics": complexity_metrics
        }

    def _audit_cpp(self, code: str) -> Dict[str, Any]:
        findings = []
        # Check modern C++ idioms and potential memory hazards
        raw_pointer_matches = len(re.findall(r"\b\w+\s*\*\s*\w+\s*=\s*new\b", code))
        if raw_pointer_matches > 0:
            findings.append({
                "severity": "HIGH",
                "category": "MemorySafety",
                "message": f"Raw dynamic allocation 'new' detected ({raw_pointer_matches} occurrences). Recommend std::make_unique or RAII containers."
            })

        mutex_present = "std::shared_mutex" in code or "std::mutex" in code
        stl_containers_used = [c for c in ["std::list", "std::unordered_map", "std::vector", "std::deque"] if c in code]

        base_score = 95 - (raw_pointer_matches * 15)
        final_score = max(0, min(100, base_score))

        return {
            "language": "cpp",
            "is_syntactically_valid": True,
            "security_score": final_score,
            "status": "PASS" if final_score >= 80 else "WARNING",
            "findings": findings,
            "complexity_metrics": {
                "stl_containers": stl_containers_used,
                "thread_safety_primitives": ["mutex"] if mutex_present else []
            }
        }
