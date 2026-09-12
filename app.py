import os
import streamlit as st
import dspy
from engine import CodeSentinelPipeline, init_dspy

st.set_page_config(page_title="DSPy Code Sentinel", page_icon="🛡️", layout="wide")

st.title("🛡️ DSPy Code Sentinel")
st.subheader("Production-Grade Declarative Code Security Auditor & Auto-Patcher")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenRouter API Key", type="password")
    selected_model = st.selectbox(
        "Target Model",
        ["openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet", "meta-llama/llama-3.3-70b-instruct"]
    )
    st.markdown("---")
    st.markdown("### Framework Architecture")
    st.info("Built with **DSPy Signatures**, **ChainOfThought Modules**, and **MIPROv2 Prompt Optimizers**.")

code_input = st.text_area(
    "Paste Code Snippet to Audit:",
    height=200,
    value="import os\ndef run_cmd(user_input):\n    os.system('ls ' + user_input)"
)

if st.button("Run Security Audit & Auto-Patch", type="primary"):
    if not api_key:
        st.error("Please enter an OpenRouter API Key in the sidebar.")
    else:
        try:
            with st.spinner("Initializing DSPy Engine and processing target code..."):
                init_dspy(api_key=api_key, model_name=selected_model)
                pipeline = CodeSentinelPipeline()
                
                # Load compiled weights/prompts if compiled artifact exists
                if os.path.exists("compiled_sentinel.json"):
                    pipeline.load("compiled_sentinel.json")
                
                result = pipeline(code=code_input)

            st.success("Analysis Complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🔍 Security Findings")
                st.metric("Risk Severity", result.risk_level)
                st.write(f"**Identified Flaw:** {result.vulnerability}")
                st.markdown("**Reasoning Steps:**")
                st.info(result.rationale)

            with col2:
                st.markdown("### 🛠️ Refactored Patch")
                st.code(result.patched_code, language="python")

        except Exception as e:
            st.error(f"Error executing pipeline: {str(e)}")
