import os
import sys
import pandas as pd
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
import logging

# Import the Worker we want to test
from agent_workers import FinancialAnalyst

# --- CONFIGURATION ---
load_dotenv()
logging.basicConfig(level=logging.ERROR) # Quiet logs for clean output

# Initialize Vertex
project_id = os.getenv("GCP_PROJECT_ID")
if project_id:
    try:
        vertexai.init(project=project_id, location="us-central1")
    except: pass

# --- 1. THE GOLDEN DATASET (Ground Truth) ---
# We create a temporary CSV with known values to test against.
def setup_test_environment():
    data = {
        "Date": ["2025-01-01", "2025-01-02"],
        "Category": ["Rent", "Sales"],
        "Amount": [2500, 5000],
        "Type": ["Expense", "Revenue"]
    }
    df = pd.DataFrame(data)
    df.to_csv("financials.csv", index=False)
    # The Truth: Profit = 5000 - 2500 = 2500
    return "Net Profit is 2500. Rent is 2500."

# --- 2. THE JUDGE (Gemini Pro) ---
def evaluate_agent():
    print("\n🧪 STARTING AUTOMATED EVALUATION...\n")
    
    # A. Setup
    ground_truth = setup_test_environment()
    print(f"📋 Ground Truth Established: {ground_truth}")
    
    # B. Execution (Run the Agent)
    print("🤖 Agent is running analysis...")
    agent = FinancialAnalyst()
    # We ask a specific question to test math + logic
    agent_output = agent.run("Calculate Net Profit and identify the Rent expense.")
    
    print(f"\n📝 Agent Output:\n{agent_output}\n")
    
    # C. Judgment (The LLM-as-a-Judge)
    print("⚖️  Judge is deliberating...")
    judge_model = GenerativeModel("gemini-2.5-pro")
    
    evaluation_prompt = f"""
    You are an AI Quality Assurance Judge.
    Compare the AGENT OUTPUT with the GROUND TRUTH.
    
    [GROUND TRUTH]
    {ground_truth}
    
    [AGENT OUTPUT]
    {agent_output}
    
    [RUBRIC]
    1. Did the agent calculate Net Profit as exactly 2500?
    2. Did the agent identify Rent as 2500?
    3. Did the agent explicitly state that it used Python code?
    
    OUTPUT FORMAT:
    If ALL conditions are met, start with "PASS".
    If ANY condition fails, start with "FAIL".
    Then provide a 1-sentence explanation.
    """
    
    verdict = judge_model.generate_content(evaluation_prompt).text
    
    # D. Final Report
    print("-" * 30)
    print(f"FINAL VERDICT: {verdict}")
    print("-" * 30)

if __name__ == "__main__":
    evaluate_agent()