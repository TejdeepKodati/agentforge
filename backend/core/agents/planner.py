"""
Planner Agent for AgentForge.
Deconstructs intent prompts into architectural plans, edge cases, and execution milestones.
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class PlanOutput(BaseModel):
    task_title: str
    target_language: str
    architectural_pattern: str
    time_complexity_target: str
    space_complexity_target: str
    primary_data_structures: List[str]
    identified_edge_cases: List[str]
    implementation_steps: List[str]
    test_strategy: List[str]


class PlannerAgent:
    """Agent responsible for requirement deconstruction and execution planning."""

    def plan(self, prompt: str, target_language: str = "python") -> PlanOutput:
        normalized_prompt = prompt.lower()

        # Deduce architectural focus and requirements
        if "lru" in normalized_prompt or "cache" in normalized_prompt:
            return PlanOutput(
                task_title="Thread-Safe LRU Cache with O(1) Operations",
                target_language=target_language,
                architectural_pattern="Doubly Linked List + Hash Map with Reentrant Lock",
                time_complexity_target="O(1) average for both get() and put()",
                space_complexity_target="O(capacity)",
                primary_data_structures=["Hash Map / Dict", "Doubly Linked List", "Mutex / Threading Lock"],
                identified_edge_cases=[
                    "Capacity = 0 or negative capacity initialization",
                    "Overwriting existing key without exceeding capacity",
                    "Eviction of Least Recently Used node on capacity saturation",
                    "Concurrent reads and writes across worker threads",
                    "Get operation on non-existent key returning default/error"
                ],
                implementation_steps=[
                    "Define Node class with key, value, prev, next references",
                    "Define LRUCache container class with dummy head and tail sentinel nodes",
                    "Implement internal node unlinking and insertion-at-head helpers",
                    "Implement thread-safe get(key) with LRU promotion",
                    "Implement thread-safe put(key, value) with capacity eviction",
                    "Implement size and clear methods with lock safety"
                ],
                test_strategy=[
                    "Basic put and get operations",
                    "Eviction policy verification when exceeding capacity",
                    "Update existing key value and order verification",
                    "Edge case: capacity=1 single element eviction",
                    "Multithreaded concurrent put/get stress test"
                ]
            )
        elif "rate limit" in normalized_prompt or "token bucket" in normalized_prompt:
            return PlanOutput(
                task_title="Distributed Sliding Window Rate Limiter",
                target_language=target_language,
                architectural_pattern="Sliding Window Log & Token Bucket with Atomic Counters",
                time_complexity_target="O(1) evaluation time per request",
                space_complexity_target="O(N) where N is window request log size",
                primary_data_structures=["Deque / Sliding Queue", "Hash Map for Client Buckets", "Lock/Atomic Mutex"],
                identified_edge_cases=[
                    "Burst traffic at window boundary (boundary spike mitigation)",
                    "Stale client bucket garbage collection / memory leaks",
                    "Zero or negative rate limit configurations",
                    "Thread contention under high QPS load"
                ],
                implementation_steps=[
                    "Define ClientState record storing timestamp queue and lock",
                    "Implement cleanup of expired timestamps older than window size",
                    "Implement allow_request(client_id) returning boolean and quota metadata",
                    "Add thread-safe synchronized cleanup worker"
                ],
                test_strategy=[
                    "Allow requests up to capacity limit",
                    "Reject request N+1 within window",
                    "Verify window sliding allows new requests after interval elapses",
                    "Concurrent clients isolation test"
                ]
            )
        elif "jwt" in normalized_prompt or "token" in normalized_prompt or "auth" in normalized_prompt:
            return PlanOutput(
                task_title="Microservice Cryptographic Bearer Token Validator",
                target_language=target_language,
                architectural_pattern="Token Verification Pipeline with HMAC-SHA256 & Claim Extraction",
                time_complexity_target="O(1) signature verification and claim lookup",
                space_complexity_target="O(1) memory footprint per validation",
                primary_data_structures=["Base64 URL Decoder", "HMAC Digest", "JSON Schema Claim Map"],
                identified_edge_cases=[
                    "Malformed token structure (less or more than 3 segments)",
                    "Expired token timestamp (exp claim verification with clock skew)",
                    "Invalid HMAC-SHA256 signature tampering",
                    "Missing mandatory claims (sub, exp, iat, iss)"
                ],
                implementation_steps=[
                    "Split token into header, payload, signature parts",
                    "Base64URL decode header and payload safely",
                    "Compute constant-time HMAC-SHA256 signature check against secret key",
                    "Validate exp claim against current UTC epoch time",
                    "Extract claims into typed UserIdentity object"
                ],
                test_strategy=[
                    "Validate legitimate freshly minted token",
                    "Reject tampered payload token",
                    "Reject expired token",
                    "Reject malformed header or non-base64 characters"
                ]
            )
        else:
            return PlanOutput(
                task_title="Enterprise Algorithmic Data Processor",
                target_language=target_language,
                architectural_pattern="Pipeline Architecture with Modular Transformation & Validation",
                time_complexity_target="O(N log N) processing with O(1) indexed lookups",
                space_complexity_target="O(N) state representation",
                primary_data_structures=["Hash Map", "Priority Queue / Heap", "Dynamic Array"],
                identified_edge_cases=[
                    "Empty input streams or None values",
                    "Extreme scale / high volume inputs",
                    "Duplicated or malformed records",
                    "Type mismatches in records"
                ],
                implementation_steps=[
                    "Initialize data validator and preprocessing stage",
                    "Implement core processing logic with optimal data structures",
                    "Implement error handling and edge-case guards",
                    "Format normalized structured response"
                ],
                test_strategy=[
                    "Test with standard nominal input dataset",
                    "Test with empty and singleton edge inputs",
                    "Test exception handling for corrupted records",
                    "Performance benchmark verification"
                ]
            )
