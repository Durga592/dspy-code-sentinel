import os
import dspy
from dataset import TRAIN_DATA, VAL_DATA
from engine import CodeSentinelPipeline, init_dspy

def security_metric(example, pred, trace=None):
    """Custom metric to check vulnerability detection and safe refactoring."""
    vuln_match = example.vulnerability.split("(")[0].lower() in pred.vulnerability.lower()
    has_patch = len(pred.patched_code.strip()) > 10
    
    # Return numerical quality score
    if vuln_match and has_patch:
        return 1.0
    elif vuln_match or has_patch:
        return 0.5
    return 0.0

def run_optimization():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable missing!")
        
    init_dspy(api_key=api_key)
    
    print("Compiling program using MIPROv2 Optimizer...")
    uncompiled_program = CodeSentinelPipeline()
    
    optimizer = dspy.MIPROv2(
        metric=security_metric,
        auto="light",
        num_candidates=3
    )
    
    compiled_program = optimizer.compile(
        student=uncompiled_program,
        trainset=TRAIN_DATA,
        valset=VAL_DATA,
        max_bootstrapped_demos=2,
        max_labeled_demos=2
    )
    
    compiled_program.save("compiled_sentinel.json")
    print("Program compiled and saved successfully to 'compiled_sentinel.json'!")

if __name__ == "__main__":
    run_optimization()
