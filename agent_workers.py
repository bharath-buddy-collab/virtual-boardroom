import os
import sys
import io
import pandas as pd
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    SafetySetting,
    HarmCategory,
    HarmBlockThreshold,
    Part
)
from dotenv import load_dotenv
import logging

# --- CONFIGURATION ---
load_dotenv()
logger = logging.getLogger("Workers")
MODEL_WORKER = "gemini-2.5-flash"

# ==============================================================================
# 🛠️ ADVANCED TOOLS (High-Fidelity Simulation)
# ==============================================================================

def execute_pandas_analysis(python_code: str) -> str:
    """
    Executes Python code on the financials CSV.
    Adapts to Cloud Run /tmp paths automatically.
    """
    try:
        # CLOUD FIX: Check /tmp first, then local
        file_path = "financials.csv"
        if os.path.exists("/tmp/financials.csv"):
            file_path = "/tmp/financials.csv"
        elif not os.path.exists(file_path):
            return "Error: financials.csv not found."
        
        # 1. Load Data
        df = pd.read_csv(file_path)
        
        # 2. Sandbox IO
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        # 3. Execution Scope
        local_scope = {"pd": pd, "df": df}
        exec(python_code, {}, local_scope)
        
        # 4. Restore IO
        sys.stdout = old_stdout
        return redirected_output.getvalue() or "Code executed successfully but printed nothing. Did you forget 'print()'?"
    except Exception as e:
        sys.stdout = sys.__stdout__ 
        return f"Execution Error: {e}"

def search_market_data(niche: str, location: str) -> str:
    """
    Simulates a 'Deep Dive' market research report.
    Returns rich, qualitative data so the CMO can write a better strategy.
    """
    return f"""
    [DEEP MARKET INTELLIGENCE: {niche} in {location}]
    
    1. DOMINANT COMPETITOR: 'The {location} Collective'
       - Strategy: High-end, expensive aesthetics.
       - Weakness: Slow service and intimidating menu.
       
    2. SECONDARY COMPETITOR: '{location} Express'
       - Strategy: Pure speed and drive-thru.
       - Weakness: Low quality, no community connection.
       
    3. CONSUMER PSYCHOLOGY ({location}):
       - Locals are currently valuing "Third Spaces" (places to sit and work) over grab-and-go.
       - High demand for "Hyper-Local" ingredients (consumers want to know the farm name).
       
    4. 2025 VIRAL TREND: "The Deconstructed Experience"
       - Customers want to customize the 'build' of their product.
       - Sustainability is no longer a perk; it is a requirement.
    """

# --- TOOL REGISTRY ---
TOOL_FUNCTIONS = {
    "execute_pandas_analysis": execute_pandas_analysis,
    "search_market_data": search_market_data
}

# --- TOOL SCHEMAS ---
pandas_func = FunctionDeclaration(
    name="execute_pandas_analysis",
    description="Analyze data using Python. 'df' is loaded. Use print() to output results.",
    parameters={"type": "object", "properties": {"python_code": {"type": "string"}}, "required": ["python_code"]}
)

search_func = FunctionDeclaration(
    name="search_market_data",
    description="Research competitors and trends.",
    parameters={"type": "object", "properties": {"niche": {"type": "string"}, "location": {"type": "string"}}, "required": ["niche", "location"]}
)

# ==============================================================================
# 👷 WORKER AGENT BASE CLASS
# ==============================================================================

class WorkerAgent:
    def __init__(self, name, instruction, tools):
        self.name = name
        self.safety = {HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH}
        self.model = GenerativeModel(MODEL_WORKER, system_instruction=instruction, tools=tools)

    def run(self, task):
        try:
            chat = self.model.start_chat()
            response = chat.send_message(task, safety_settings=self.safety)
            
            while response.candidates[0].content.parts[0].function_call:
                part = response.candidates[0].content.parts[0]
                fn_name = part.function_call.name
                fn_args = part.function_call.args
                
                if fn_name in TOOL_FUNCTIONS:
                    args = {k: v for k, v in fn_args.items()}
                    result = TOOL_FUNCTIONS[fn_name](**args)
                    response = chat.send_message(
                        Part.from_function_response(name=fn_name, response={"content": result})
                    )
                else:
                    break
            return response.text
        except Exception as e:
            return f"Error: {e}"

# ==============================================================================
# 🏢 SPECIALIZED WORKERS (The "Deep Thinkers")
# ==============================================================================

class FinancialAnalyst(WorkerAgent):
    def __init__(self):
        tools = [Tool(function_declarations=[pandas_func])]
        
        # UPGRADED INSTRUCTION: Wall Street Level Analysis
        instruction = """
        You are the Chief Financial Officer (CFO). You are not a strategic auditor.
        
        YOUR WORKFLOW:
        1.  **Code Execution**: Use `execute_pandas_analysis` to calculate Total Revenue, Total Expenses, Net Profit, and Profit Margin %.
        2.  **Narrative Analysis**: Do not just list numbers. Explain the *health* of the business.
            - Is the Profit Margin healthy (>20%) or dangerous?
            - What is the "Burn Rate" (Total Expenses)?
            - What is the biggest financial leak (Highest Expense Category)?
        3.  **Strategic Recommendation**: Based on the numbers, what one financial move should we make? (e.g., "Cut marketing," "Reinvest profit").
        
        CRITICAL: 
        - Use the specific CURRENCY provided in the prompt (e.g., $, ₹, €) for ALL numbers.
        - Your output must be a professional financial memo, not a bullet list.
        """
        super().__init__("CFO", instruction, tools)

class MarketResearcher(WorkerAgent):
    def __init__(self):
        tools = [Tool(function_declarations=[search_func])]
        
        # UPGRADED INSTRUCTION: Creative Director Level Strategy
        instruction = """
        You are the Chief Marketing Officer (CMO). You are a visionary Creative Director.
        
        YOUR WORKFLOW:
        1.  **Deep Research**: Use `search_market_data` to understand the *specific* location and niche.
        2.  **The "Hook"**: Don't just propose "ads." Propose a **Campaign Concept**.
            - Give the Campaign a catchy Title (e.g., "The Morning Commute Hero").
            - Define the "Target Persona" (Who are we talking to? e.g., "Stressed students," "Corporate rushing").
        3.  **Tactical Execution**: How do we launch this? (e.g., "Partner with the local gym," "Instagram Reels series").
        4.  **Why It Wins**: Explain why this beats the specific competitors found in the research.
        
        OUTPUT FORMAT:
        Write a pitch email to the CEO. Be persuasive, detailed, and creative.
        """
        super().__init__("CMO", instruction, tools)