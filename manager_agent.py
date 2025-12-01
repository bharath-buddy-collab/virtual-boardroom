from vertexai.generative_models import GenerativeModel
import logging

# Import our specialized workers
from agent_workers import FinancialAnalyst, MarketResearcher

# --- CONFIGURATION ---
logger = logging.getLogger("Manager")
MODEL_ROUTER = "gemini-2.5-flash" # Fast for classification
MODEL_CEO = "gemini-2.5-pro"      # Smart for synthesis

class BoardroomManager:
    """
    The Orchestrator (Level 3 Architecture).
    1. Router: Decides intent.
    2. Workers: Dispatches tasks with FULL CONTEXT (Currency/Location).
    3. CEO: Synthesizes a detailed directive.
    """
    def __init__(self):
        self.router_model = GenerativeModel(MODEL_ROUTER)
        self.ceo_model = GenerativeModel(MODEL_CEO)
        
        # Initialize the Specialist Workers
        self.cfo = FinancialAnalyst()
        self.cmo = MarketResearcher()

    def route_request(self, user_input):
        """Phase 1: Intent Classification"""
        prompt = f"""
        Classify this user request into exactly one category:
        - "FINANCE": Users asking specifically about numbers, profit, or data.
        - "MARKETING": Users asking specifically about ads, competitors, or brand.
        - "STRATEGY": Users asking for a plan, growth, or general help.
        - "CHAT": Users saying hello or general chit-chat.
        
        REQUEST: {user_input}
        OUTPUT ONLY THE CATEGORY WORD.
        """
        response = self.router_model.generate_content(prompt)
        return response.text.strip().upper()

    def execute_workflow(self, niche, goal, location, currency, csv_context):
        """
        Phase 2: Execution & Synthesis (The "Board Meeting")
        Now accepts 'currency' and 'location' to ensure high-fidelity outputs.
        """
        
        # A. Deploy Workers
        logger.info("👨‍💼 Manager dispatching CFO...")
        # We inject the Currency into the prompt so the CFO doesn't guess
        cfo_task = f"""
        Data Schema: Date, Category, Amount, Type.
        CURRENCY: {currency}
        TASK: Perform a detailed P&L analysis for {niche}.
        """
        cfo_report = self.cfo.run(cfo_task)
        
        logger.info("👩‍🎨 Manager dispatching CMO...")
        # We inject the Location so the CMO finds local competitors
        cmo_task = f"""
        Niche: {niche}
        Location: {location}
        TASK: Research local competitors and create a campaign.
        """
        cmo_report = self.cmo.run(cmo_task)
        
        # B. CEO Synthesis (The Critic)
        logger.info("👑 CEO Synthesizing Strategy...")
        ceo_prompt = f"""
        You are the CEO. Synthesize these reports into a Strategic Directive.
        
        [CFO REPORT - REALITY]
        {cfo_report}
        
        [CMO REPORT - AMBITION]
        {cmo_report}
        
        CONTEXT: 
        - Goal: '{goal}'
        - Currency: '{currency}'
        - Location: '{location}'
        
        TASK: Write a 3-point execution plan that aligns the budget (CFO) with the ambition (CMO).
        """
        final_strategy = self.ceo_model.generate_content(ceo_prompt).text
        
        return {
            "cfo": cfo_report,
            "cmo": cmo_report,
            "ceo": final_strategy
        }