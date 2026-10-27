"""
Input and Code Guardrails for AgentForge
Detects prompt injection, PII, and unsafe code patterns.
"""
import re
from typing import Dict, List, Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"you\s+are\s+now\s+(an\s+unrestricted|DAN|a\s+hacker)",
    r"system\s*:\s*override",
    r"forget\s+everything\s+you\s+were\s+told",
    r"bypass\s+all\s+filters",
    r"output\s+the\s+system\s+prompt",
    r"reveal\s+your\s+hidden\s+rules",
]

PII_PATTERNS = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "[EMAIL_REDACTED]"),
    (r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE_REDACTED]"),
    (r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,40}\b", "[GITHUB_TOKEN_REDACTED]"),
    (r"\b(?:sk-[a-zA-Z0-9]{20,48})\b", "[API_KEY_REDACTED]"),
    (r"\b(?:AKIA[0-9A-Z]{16})\b", "[AWS_ACCESS_KEY_REDACTED]"),
]

DANGEROUS_CODE_PATTERNS = [
    (r"\b(os\.system|subprocess\.call|subprocess\.Popen|subprocess\.run)\b", "CRITICAL", "Arbitrary shell command execution detected"),
    (r"\b(eval|exec|__import__)\b", "HIGH", "Dynamic code execution via eval/exec/__import__"),
    (r"\b(socket\.socket|urllib\.request\.urlopen|requests\.get)\b.*http", "MEDIUM", "Unvalidated outbound network socket/HTTP request"),
    (r"\b(rmdir|unlink|remove|shutil\.rmtree)\b", "HIGH", "Direct filesystem deletion operation"),
    (r"(password|secret|api_key|token)\s*=\s*['\"][^'\"]{8,}['\"]", "HIGH", "Hardcoded credential or API secret"),
]


class GuardrailEngine:
    """Enterprise guardrail engine enforcing Responsible AI policies."""

    @staticmethod
    def inspect_prompt(prompt: str) -> Tuple[bool, str, List[str]]:
        """
        Inspects input prompt for injection attacks and sanitizes PII.
        Returns: (is_safe, sanitized_prompt, violations)
        """
        violations = []
        is_safe = True

        # Check prompt injection
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                violations.append(f"Prompt injection pattern detected: '{pattern}'")
                is_safe = False

        # Redact PII
        sanitized = prompt
        for pattern, replacement in PII_PATTERNS:
            if re.search(pattern, sanitized):
                sanitized = re.sub(pattern, replacement, sanitized)
                violations.append("PII detected and redacted from prompt")

        return is_safe, sanitized, violations

    @staticmethod
    def inspect_code_safety(code: str) -> Tuple[int, List[Dict[str, str]]]:
        """
        Scans code for dangerous primitives and anti-patterns.
        Returns: (safety_score 0-100, findings)
        """
        findings = []
        deductions = 0

        for pattern, severity, description in DANGEROUS_CODE_PATTERNS:
            matches = list(re.finditer(pattern, code))
            if matches:
                penalty = 35 if severity == "CRITICAL" else 20 if severity == "HIGH" else 10
                deductions += penalty * len(matches)
                findings.append({
                    "severity": severity,
                    "description": description,
                    "count": len(matches),
                    "instances": [m.group(0) for m in matches[:3]]
                })

        safety_score = max(0, 100 - deductions)
        return safety_score, findings
