"""
OpenAI interface for intelligent financial analysis responses
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from config import Config
from src.utils.prompt_templates import PromptTemplates

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class OpenAIInterface:
    """Interface for OpenAI GPT-4o API integration."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized successfully")
        
        self.model = Config.OPENAI_MODEL  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.temperature = Config.OPENAI_TEMPERATURE
        self.prompt_templates = PromptTemplates()
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        if not self.client:
            return False
        
        try:
            # Test with a simple API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI API not available: {e}")
            return False
    
    async def generate_response(self, user_query: str, context_data: Dict[str, Any]) -> str:
        """Generate intelligent response based on user query and financial context."""
        if not self.client:
            return self._fallback_response(user_query)
        
        try:
            # Determine query type and select appropriate prompt
            query_type = self._classify_query(user_query)
            system_prompt = self.prompt_templates.get_system_prompt(query_type)
            user_prompt = self.prompt_templates.format_user_prompt(user_query, context_data, query_type)
            
            logger.info(f"Generating response for query type: {query_type}")
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            generated_response = response.choices[0].message.content
            if generated_response:
                generated_response = generated_response.strip()
            else:
                generated_response = "No response generated"
            
            # Post-process response
            final_response = self._post_process_response(generated_response, query_type)
            
            logger.info("Response generated successfully")
            return final_response
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            return self._fallback_response(user_query)
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query to select appropriate prompt template."""
        query_lower = query.lower()
        
        # Company comparison queries
        if any(word in query_lower for word in ['compare', 'vs', 'versus', 'between']):
            return "comparison"
        
        # Performance analysis queries
        elif any(word in query_lower for word in ['perform', 'performance', 'results', 'earnings']):
            return "performance"
        
        # Financial metrics queries
        elif any(word in query_lower for word in ['revenue', 'income', 'profit', 'cash flow', 'debt', 'financial']):
            return "financial_metrics"
        
        # Production and operational queries
        elif any(word in query_lower for word in ['production', 'volume', 'output', 'operational', 'operations']):
            return "operational"
        
        # Market and investment queries
        elif any(word in query_lower for word in ['market', 'stock', 'investment', 'valuation', 'dividend']):
            return "market_analysis"
        
        # Risk and strategy queries
        elif any(word in query_lower for word in ['risk', 'challenge', 'strategy', 'outlook', 'future']):
            return "risk_strategy"
        
        # Trend analysis queries
        elif any(word in query_lower for word in ['trend', 'growth', 'decline', 'change', 'over time']):
            return "trend_analysis"
        
        # Default to general analysis
        else:
            return "general"
    
    def _post_process_response(self, response: str, query_type: str) -> str:
        """Post-process the generated response based on query type."""
        # Add appropriate emojis and formatting based on query type
        if query_type == "comparison":
            if "📊" not in response:
                response = "📊 " + response
        elif query_type == "performance":
            if "📈" not in response and "📉" not in response:
                response = "📈 " + response
        elif query_type == "financial_metrics":
            if "💰" not in response:
                response = "💰 " + response
        elif query_type == "operational":
            if "🛢️" not in response:
                response = "🛢️ " + response
        elif query_type == "market_analysis":
            if "📊" not in response:
                response = "📊 " + response
        elif query_type == "risk_strategy":
            if "⚠️" not in response and "🎯" not in response:
                response = "🎯 " + response
        elif query_type == "trend_analysis":
            if "📈" not in response and "📉" not in response:
                response = "📊 " + response
        
        return response
    
    def _fallback_response(self, user_query: str) -> str:
        """Generate fallback response when OpenAI is not available."""
        query_lower = user_query.lower()
        
        # Provide basic responses based on query patterns
        # Check for comparison queries first (before individual company analysis)
        if any(word in query_lower for word in ["compare", "vs", "versus", "better", "best", "analytics", "perform", "competitors"]):
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return "📊 " + analyzer.compare_companies(user_query)
        
        elif "shell" in query_lower:
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return analyzer.analyze_company_performance("Shell", user_query)
            
        elif "bp" in query_lower:
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return analyzer.analyze_company_performance("BP", user_query)
            
        elif "exxonmobil" in query_lower or "exxon" in query_lower:
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return analyzer.analyze_company_performance("ExxonMobil", user_query)
            
        elif "chevron" in query_lower:
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return analyzer.analyze_company_performance("Chevron", user_query)
            
        elif any(word in query_lower for word in ["compare", "vs", "versus", "better", "best", "analytics", "perform", "competitors"]):
            # Advanced comparison analysis using intelligence engine
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return "📊 " + analyzer.compare_companies(user_query)
            
        elif any(word in query_lower for word in ["invest", "investment", "buy", "recommend", "which", "whom"]):
            # Advanced investment analysis using intelligence engine
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            return "💼 " + analyzer.analyze_investment_opportunity(user_query)
            
        else:
            # Enhanced responses using intelligence engine
            from src.utils.financial_analyzer import FinancialIntelligenceEngine
            from src.database.database import DatabaseManager
            
            db = DatabaseManager()
            analyzer = FinancialIntelligenceEngine(db)
            
            # Try to extract company name from query
            mentioned_company = None
            for company in ["Shell", "BP", "ExxonMobil", "Chevron"]:
                if company.lower() in query_lower:
                    mentioned_company = company
                    break
            
            if mentioned_company:
                return analyzer.analyze_company_performance(mentioned_company, user_query)
            
            # Check if it's a comparison query
            if any(word in query_lower for word in ["compare", "comparison"]):
                return analyzer.compare_companies(user_query)
            
            return """I can provide comprehensive analysis using financial data from Shell, BP, ExxonMobil, and Chevron.

Try asking:
- "Which company should I invest in?" - for investment recommendations
- "Compare Shell vs BP" - for detailed comparisons  
- "How is Chevron performing?" - for specific company analysis
- "Show me the best cash flow generator" - for specific metrics

I analyze real financial data to provide actionable insights."""

    async def analyze_financial_data(self, company_data: Dict[str, Any], analysis_type: str = "comprehensive") -> str:
        """Analyze financial data for a specific company."""
        if not self.client:
            return "OpenAI API not available for analysis."
        
        try:
            prompt = self.prompt_templates.get_analysis_prompt(company_data, analysis_type)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt_templates.get_system_prompt("financial_metrics")},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "No response generated"
            
        except Exception as e:
            logger.error(f"Error in financial data analysis: {e}")
            return f"Error analyzing financial data: {str(e)}"

    async def generate_comparison_analysis(self, companies_data: Dict[str, Dict[str, Any]]) -> str:
        """Generate comparative analysis between multiple companies."""
        if not self.client:
            return "OpenAI API not available for comparison analysis."
        
        try:
            prompt = self.prompt_templates.get_comparison_prompt(companies_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt_templates.get_system_prompt("comparison")},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else "No response generated"
            
        except Exception as e:
            logger.error(f"Error in comparison analysis: {e}")
            return f"Error generating comparison analysis: {str(e)}"
