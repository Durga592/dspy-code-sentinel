import os
import dspy

# 1. Define DSPy Signatures
class AuditSignature(dspy.Signature):
    """Analyze source code for security flaws, CWE classifications, and risk levels."""
    
    code: str = dspy.InputField(desc="Python code snippet to audit")
    vulnerability: str = dspy.OutputField(desc="Primary vulnerability identified with CWE classification")
    risk_level: str = dspy.OutputField(desc="CRITICAL, HIGH, MEDIUM, or LOW risk level")


class PatchSignature(dspy.Signature):
    """Generate secure refactored python code addressing identified vulnerabilities."""
    
    code: str = dspy.InputField(desc="Original insecure code")
    vulnerability: str = dspy.InputField(desc="Detected security flaw to remediate")
    patched_code: str = dspy.OutputField(desc="Refactored, production-ready secure code")


# 2. Resilient Sentinel Pipeline Module
class CodeSentinelPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.auditor = dspy.ChainOfThought(AuditSignature)
        self.patcher = dspy.ChainOfThought(PatchSignature)

    def forward(self, code: str):
        # Run audit stage
        audit_res = self.auditor(code=code)
        
        # Safely extract rationale (fallback if rationale attribute is missing)
        rationale_text = getattr(audit_res, 'rationale', None)
        if not rationale_text:
            # Fallback check for alternative dspy response keys
            rationale_text = getattr(audit_res, 'reasoning', 'Chain-of-Thought analysis completed successfully.')
        
        # Run patch stage
        patch_res = self.patcher(code=code, vulnerability=audit_res.vulnerability)
        
        return dspy.Prediction(
            vulnerability=audit_res.vulnerability,
            risk_level=audit_res.risk_level,
            rationale=rationale_text,
            patched_code=patch_res.patched_code
        )


def init_dspy(api_key: str, model_name: str = "openai/gpt-4o-mini"):
    """Configure DSPy with OpenRouter provider routing."""
    
    # Prepend openrouter/ provider prefix for litellm routing compatibility
    if not model_name.startswith("openrouter/"):
        formatted_model = f"openrouter/{model_name}"
    else:
        formatted_model = model_name

    lm = dspy.LM(
        model=formatted_model,
        api_base="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.1
    )
    dspy.configure(lm=lm)
    return lm
