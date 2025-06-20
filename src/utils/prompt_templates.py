"""
Prompt templates for OpenAI GPT-4o financial analysis
"""

import json
from typing import Dict, Any, List
from datetime import datetime

class PromptTemplates:
    """Collection of prompt templates for different types of financial analysis queries."""
    
    def __init__(self):
        """Initialize prompt templates."""
        pass
    
    def get_system_prompt(self, query_type: str) -> str:
        """Get system prompt based on query type."""
        base_context = """You are an expert Oil & Gas Financial Analyst with deep knowledge of the energy sector. 
You specialize in analyzing financial reports, market trends, and operational metrics for major oil and gas companies including Shell, BP, ExxonMobil, and Chevron.

Your expertise includes:
- Quarterly earnings analysis and interpretation
- Cash flow and capital allocation assessment
- Production metrics and operational efficiency
- Market valuation and investment analysis
- Industry trends and competitive positioning
- Risk assessment and strategic outlook

Always provide:
1. Clear, data-driven insights
2. Context about industry trends and market conditions
3. Specific numerical analysis when data is available
4. Balanced perspective on both opportunities and risks
5. Professional tone with engaging presentation

Use relevant emojis sparingly to enhance readability but maintain professional credibility."""

        query_specific_prompts = {
            "comparison": base_context + """

For comparison queries, focus on:
- Side-by-side metric analysis
- Relative performance assessment
- Competitive positioning
- Strengths and weaknesses of each company
- Market share and strategic differences""",
            
            "performance": base_context + """

For performance analysis, emphasize:
- Quarter-over-quarter and year-over-year trends
- Key performance indicators and their implications
- Operational efficiency and productivity metrics
- Financial health indicators
- Management execution and strategic progress""",
            
            "financial_metrics": base_context + """

For financial metrics analysis, provide:
- Detailed breakdown of key financial ratios
- Cash flow analysis and capital allocation
- Debt management and liquidity position
- Profitability trends and margin analysis
- Return on investment and shareholder value creation""",
            
            "operational": base_context + """

For operational analysis, cover:
- Production volumes and efficiency metrics
- Cost per barrel and operational leverage
- Asset utilization and project economics
- Geographic diversification and resource base
- Technology adoption and operational innovation""",
            
            "market_analysis": base_context + """

For market and investment analysis, include:
- Valuation metrics and peer comparison
- Dividend policy and shareholder returns
- Stock performance and market sentiment
- ESG considerations and energy transition impact
- Investment thesis and risk-reward profile""",
            
            "risk_strategy": base_context + """

For risk and strategy analysis, address:
- Key business risks and mitigation strategies
- Regulatory and environmental challenges
- Energy transition risks and opportunities
- Geographic and political risk exposure
- Strategic initiatives and future outlook""",
            
            "trend_analysis": base_context + """

For trend analysis, focus on:
- Historical performance patterns
- Industry cycle positioning
- Forward-looking indicators
- Structural changes in the sector
- Long-term growth and transformation trends"""
        }
        
        return query_specific_prompts.get(query_type, base_context)
    
    def format_user_prompt(self, user_query: str, context_data: Dict[str, Any], query_type: str) -> str:
        """Format user prompt with context data."""
        prompt = f"User Question: {user_query}\n\n"
        
        # Add relevant company data
        if context_data.get("comparison_data"):
            prompt += "=== AVAILABLE FINANCIAL DATA ===\n"
            for company, data in context_data["comparison_data"].items():
                prompt += f"\n{company} Latest Financial Report:\n"
                prompt += f"- Report Date: {data.get('report_date', 'N/A')}\n"
                prompt += f"- Quarter: {data.get('quarter', 'N/A')} {data.get('year', 'N/A')}\n"
                prompt += f"- Revenue: ${data.get('revenue', 0):,.0f} million\n"
                prompt += f"- Net Income: ${data.get('net_income', 0):,.0f} million\n"
                prompt += f"- Operating Income: ${data.get('operating_income', 0):,.0f} million\n"
                prompt += f"- Free Cash Flow: ${data.get('free_cash_flow', 0):,.0f} million\n"
                prompt += f"- Cash & Equivalents: ${data.get('cash_and_equivalents', 0):,.0f} million\n"
                prompt += f"- Total Debt: ${data.get('total_debt', 0):,.0f} million\n"
                prompt += f"- Production Volume: {data.get('production_volume', 0):,.1f} {data.get('production_unit', 'BOE/day')}\n"
                
                # Add additional metrics if available
                if data.get('raw_data'):
                    try:
                        raw_data = json.loads(data['raw_data'])
                        additional = raw_data.get('additional_metrics', {})
                        if additional:
                            prompt += f"- Additional Metrics:\n"
                            for metric, value in additional.items():
                                prompt += f"  • {metric.replace('_', ' ').title()}: {value}\n"
                    except:
                        pass
        
        # Add historical trends if available
        if context_data.get("historical_data"):
            prompt += "\n=== HISTORICAL TRENDS ===\n"
            for company, metrics in context_data["historical_data"].items():
                prompt += f"\n{company} Historical Data:\n"
                for metric, trends in metrics.items():
                    prompt += f"- {metric.replace('_', ' ').title()} Trends:\n"
                    for trend in trends:
                        prompt += f"  • {trend.get('quarter', '')} {trend.get('year', '')}: ${trend.get(metric, 0):,.0f} million\n"
        
        # Add market context
        if context_data.get("market_context"):
            market = context_data["market_context"]
            prompt += f"\n=== MARKET CONTEXT ===\n"
            prompt += f"- Oil Price Environment: {market.get('oil_price_environment', 'N/A')}\n"
            prompt += f"- Gas Price Environment: {market.get('gas_price_environment', 'N/A')}\n"
            prompt += f"- Sector Outlook: {market.get('sector_outlook', 'N/A')}\n"
            
            if market.get('key_challenges'):
                prompt += f"- Key Industry Challenges: {', '.join(market['key_challenges'])}\n"
            
            if market.get('key_opportunities'):
                prompt += f"- Key Industry Opportunities: {', '.join(market['key_opportunities'])}\n"
        
        prompt += f"\n=== ANALYSIS REQUEST ===\n"
        prompt += f"Please provide a comprehensive analysis addressing the user's question. "
        prompt += f"Use the financial data provided above to support your insights. "
        prompt += f"Focus on actionable insights and clear explanations. "
        prompt += f"Include specific numbers and calculations where relevant. "
        prompt += f"Keep the response engaging but professional.\n"
        
        return prompt
    
    def get_analysis_prompt(self, company_data: Dict[str, Any], analysis_type: str) -> str:
        """Get analysis prompt for specific company financial data."""
        company_name = company_data.get('company', 'Unknown Company')
        
        prompt = f"=== FINANCIAL ANALYSIS REQUEST ===\n"
        prompt += f"Company: {company_name}\n"
        prompt += f"Analysis Type: {analysis_type}\n\n"
        
        prompt += f"=== FINANCIAL DATA ===\n"
        if company_data.get('latest_data'):
            data = company_data['latest_data']
            prompt += f"Revenue: ${data.get('revenue', 0):,.0f} million\n"
            prompt += f"Net Income: ${data.get('net_income', 0):,.0f} million\n"
            prompt += f"Free Cash Flow: ${data.get('free_cash_flow', 0):,.0f} million\n"
            prompt += f"Total Debt: ${data.get('total_debt', 0):,.0f} million\n"
            prompt += f"Cash Position: ${data.get('cash_and_equivalents', 0):,.0f} million\n"
            prompt += f"Production: {data.get('production_volume', 0):,.1f} {data.get('production_unit', 'BOE/day')}\n"
        
        if company_data.get('key_ratios'):
            prompt += f"\n=== KEY RATIOS ===\n"
            for ratio, value in company_data['key_ratios'].items():
                prompt += f"{ratio.replace('_', ' ').title()}: {value}\n"
        
        prompt += f"\nPlease provide a {analysis_type} financial analysis of this company's performance, "
        prompt += f"highlighting key strengths, concerns, and strategic implications."
        
        return prompt
    
    def get_comparison_prompt(self, companies_data: Dict[str, Dict[str, Any]]) -> str:
        """Get comparison analysis prompt for multiple companies."""
        prompt = f"=== COMPARATIVE FINANCIAL ANALYSIS ===\n"
        prompt += f"Companies: {', '.join(companies_data.keys())}\n\n"
        
        for company, data in companies_data.items():
            prompt += f"=== {company.upper()} ===\n"
            if data:
                prompt += f"Revenue: ${data.get('revenue', 0):,.0f} million\n"
                prompt += f"Net Income: ${data.get('net_income', 0):,.0f} million\n"
                prompt += f"Free Cash Flow: ${data.get('free_cash_flow', 0):,.0f} million\n"
                prompt += f"Production: {data.get('production_volume', 0):,.1f} {data.get('production_unit', 'BOE/day')}\n"
                prompt += f"Debt: ${data.get('total_debt', 0):,.0f} million\n"
                prompt += f"Cash: ${data.get('cash_and_equivalents', 0):,.0f} million\n\n"
        
        prompt += "Please provide a comprehensive comparative analysis of these companies, "
        prompt += "including relative performance, competitive positioning, financial health, "
        prompt += "and investment attractiveness. Highlight key differentiators and strategic advantages."
        
        return prompt
    
    def get_welcome_prompt(self) -> str:
        """Get welcome message prompt for the chatbot."""
        return """Generate a warm, professional welcome message for an Oil & Gas Financial Analysis Chatbot. 
        The message should:
        1. Introduce the chatbot's capabilities
        2. Mention the companies it covers (Shell, BP, ExxonMobil, Chevron)
        3. Provide example questions users can ask
        4. Be engaging but maintain professional credibility
        5. Use appropriate emojis sparingly
        
        Keep it concise but informative."""
