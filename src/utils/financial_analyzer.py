"""
Advanced financial analysis engine that provides intelligent insights
without requiring external AI APIs
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from src.database.database import DatabaseManager
from config import Config

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class FinancialIntelligenceEngine:
    """Advanced financial analysis engine with built-in intelligence."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize the intelligence engine."""
        self.db_manager = db_manager
        self.companies = Config.TRACKED_COMPANIES
        
        # Financial analysis knowledge base
        self.analysis_frameworks = {
            'profitability': {
                'metrics': ['profit_margin', 'roe', 'roa'],
                'benchmarks': {'excellent': 20, 'good': 15, 'fair': 10, 'poor': 5}
            },
            'liquidity': {
                'metrics': ['cash_ratio', 'current_ratio'],
                'benchmarks': {'excellent': 2.0, 'good': 1.5, 'fair': 1.0, 'poor': 0.5}
            },
            'efficiency': {
                'metrics': ['asset_turnover', 'cash_conversion'],
                'benchmarks': {'excellent': 0.8, 'good': 0.6, 'fair': 0.4, 'poor': 0.2}
            },
            'growth': {
                'metrics': ['revenue_growth', 'income_growth'],
                'benchmarks': {'excellent': 15, 'good': 10, 'fair': 5, 'poor': 0}
            }
        }
        
        # Industry-specific insights
        self.oil_gas_insights = {
            'Shell': {
                'strengths': ['Integrated business model', 'Strong cash generation', 'Energy transition leadership'],
                'challenges': ['High capital requirements', 'Environmental regulations', 'Oil price volatility'],
                'strategic_focus': ['LNG expansion', 'Renewable energy', 'Digital transformation']
            },
            'BP': {
                'strengths': ['Portfolio optimization', 'Low-carbon investments', 'Geographic diversification'],
                'challenges': ['Legacy asset management', 'Transition costs', 'Regulatory pressure'],
                'strategic_focus': ['Beyond petroleum strategy', 'Bioenergy', 'Electric vehicle charging']
            },
            'ExxonMobil': {
                'strengths': ['Technological innovation', 'Upstream efficiency', 'Chemical integration'],
                'challenges': ['Climate activism', 'Stranded assets risk', 'Capital allocation'],
                'strategic_focus': ['Permian Basin', 'Low-carbon solutions', 'Advanced recycling']
            },
            'Chevron': {
                'strengths': ['Conservative balance sheet', 'Consistent dividends', 'Operational excellence'],
                'challenges': ['Limited growth options', 'ESG pressure', 'Portfolio concentration'],
                'strategic_focus': ['Lower carbon intensity', 'Higher returns', 'Traditional energy']
            }
        }
    
    def analyze_investment_opportunity(self, query: str) -> str:
        """Provide comprehensive investment analysis."""
        companies_data = {}
        
        for company in self.companies:
            data = self.db_manager.get_latest_financial_data(company)
            if data:
                companies_data[company] = self._calculate_financial_metrics(data)
        
        if not companies_data:
            return "No financial data available for analysis."
        
        # Perform comprehensive analysis
        rankings = self._rank_companies_by_investment_score(companies_data)
        top_pick = rankings[0] if rankings else None
        
        analysis = "INVESTMENT ANALYSIS REPORT\n\n"
        
        # Investment rankings
        analysis += "INVESTMENT RANKINGS:\n"
        for i, (company, score, metrics) in enumerate(rankings, 1):
            analysis += f"{i}. {company} (Score: {score:.1f}/100)\n"
            analysis += f"   Profit Margin: {metrics['profit_margin']:.1f}%\n"
            analysis += f"   Financial Strength: {self._assess_financial_strength(metrics)}\n"
            analysis += f"   Cash Generation: {self._assess_cash_generation(metrics)}\n\n"
        
        if top_pick:
            company, score, metrics = top_pick
            analysis += f"TOP RECOMMENDATION: {company}\n\n"
            analysis += "INVESTMENT THESIS:\n"
            
            # Add company-specific insights
            if company in self.oil_gas_insights:
                insights = self.oil_gas_insights[company]
                analysis += f"Strengths: {', '.join(insights['strengths'])}\n"
                analysis += f"Key Focus Areas: {', '.join(insights['strategic_focus'])}\n"
            
            # Financial reasoning
            analysis += f"\nFinancial Highlights:\n"
            if metrics['profit_margin'] > 20:
                analysis += f"- Exceptional profitability ({metrics['profit_margin']:.1f}% margin)\n"
            elif metrics['profit_margin'] > 10:
                analysis += f"- Strong profitability ({metrics['profit_margin']:.1f}% margin)\n"
            
            if metrics.get('cash_conversion', 0) > 0.7:
                analysis += "- Excellent cash conversion efficiency\n"
            
            if metrics.get('debt_ratio', 0) < 1.5:
                analysis += "- Conservative debt management\n"
            
            analysis += f"\nRisk Considerations:\n"
            if company in self.oil_gas_insights:
                challenges = self.oil_gas_insights[company]['challenges']
                for challenge in challenges[:2]:  # Show top 2 risks
                    analysis += f"- {challenge}\n"
        
        analysis += "\nThis analysis is based on latest financial reports and industry knowledge."
        return analysis
    
    def analyze_company_performance(self, company: str, query: str) -> str:
        """Analyze specific company performance."""
        data = self.db_manager.get_latest_financial_data(company)
        if not data:
            return f"No financial data available for {company}."
        
        metrics = self._calculate_financial_metrics(data)
        
        analysis = f"{company.upper()} PERFORMANCE ANALYSIS\n\n"
        
        # Financial overview
        analysis += "FINANCIAL OVERVIEW:\n"
        analysis += f"Revenue: ${data.get('revenue', 0):,.0f}M\n"
        analysis += f"Net Income: ${data.get('net_income', 0):,.0f}M\n"
        analysis += f"Free Cash Flow: ${data.get('free_cash_flow', 0):,.0f}M\n"
        analysis += f"Production: {data.get('production_volume', 0):,.1f} {data.get('production_unit', 'BOE/day')}\n\n"
        
        # Performance assessment
        analysis += "PERFORMANCE ASSESSMENT:\n"
        analysis += f"Profitability: {self._assess_profitability(metrics)}\n"
        analysis += f"Financial Strength: {self._assess_financial_strength(metrics)}\n"
        analysis += f"Cash Generation: {self._assess_cash_generation(metrics)}\n\n"
        
        # Company-specific insights
        if company in self.oil_gas_insights:
            insights = self.oil_gas_insights[company]
            analysis += "STRATEGIC INSIGHTS:\n"
            analysis += f"Core Strengths: {', '.join(insights['strengths'][:2])}\n"
            analysis += f"Strategic Focus: {', '.join(insights['strategic_focus'][:2])}\n"
            analysis += f"Key Challenges: {', '.join(insights['challenges'][:2])}\n\n"
        
        # Investment perspective
        investment_grade = self._determine_investment_grade(metrics)
        analysis += f"INVESTMENT GRADE: {investment_grade}\n"
        
        return analysis
    
    def compare_companies(self, query: str) -> str:
        """Provide detailed company comparison."""
        companies_data = {}
        
        for company in self.companies:
            data = self.db_manager.get_latest_financial_data(company)
            if data:
                companies_data[company] = data
        
        if len(companies_data) < 2:
            return "Insufficient data for comparison."
        
        analysis = "COMPREHENSIVE COMPANY COMPARISON\n\n"
        
        # Financial metrics comparison
        analysis += "FINANCIAL METRICS COMPARISON:\n\n"
        for company, data in companies_data.items():
            metrics = self._calculate_financial_metrics(data)
            analysis += f"{company}:\n"
            analysis += f"  Revenue: ${data.get('revenue', 0):,.0f}M\n"
            analysis += f"  Net Income: ${data.get('net_income', 0):,.0f}M\n"
            analysis += f"  Profit Margin: {metrics['profit_margin']:.1f}%\n"
            analysis += f"  Free Cash Flow: ${data.get('free_cash_flow', 0):,.0f}M\n"
            analysis += f"  Production: {data.get('production_volume', 0):,.1f} thousand BOE/day\n\n"
        
        # Rankings
        revenue_leader = max(companies_data.items(), key=lambda x: x[1].get('revenue', 0))
        profit_leader = max(companies_data.items(), key=lambda x: x[1].get('net_income', 0))
        cashflow_leader = max(companies_data.items(), key=lambda x: x[1].get('free_cash_flow', 0))
        
        analysis += "PERFORMANCE LEADERS:\n"
        analysis += f"Revenue Leader: {revenue_leader[0]} (${revenue_leader[1].get('revenue', 0):,.0f}M)\n"
        analysis += f"Profit Leader: {profit_leader[0]} (${profit_leader[1].get('net_income', 0):,.0f}M)\n"
        analysis += f"Cash Flow Leader: {cashflow_leader[0]} (${cashflow_leader[1].get('free_cash_flow', 0):,.0f}M)\n\n"
        
        # Strategic positioning
        analysis += "STRATEGIC POSITIONING:\n"
        for company in companies_data.keys():
            if company in self.oil_gas_insights:
                insights = self.oil_gas_insights[company]
                analysis += f"{company}: {insights['strategic_focus'][0]} focus\n"
        
        return analysis
    
    def _calculate_financial_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate key financial metrics."""
        revenue = data.get('revenue', 0) or 1  # Avoid division by zero
        net_income = data.get('net_income', 0) or 0
        free_cash_flow = data.get('free_cash_flow', 0) or 0
        total_debt = data.get('total_debt', 0) or 0
        cash = data.get('cash_and_equivalents', 0) or 1
        
        return {
            'profit_margin': (net_income / revenue) * 100,
            'cash_conversion': free_cash_flow / max(net_income, 1),
            'debt_ratio': total_debt / cash,
            'revenue_per_boe': revenue / max(data.get('production_volume', 1), 1) * 1000
        }
    
    def _rank_companies_by_investment_score(self, companies_data: Dict[str, Dict]) -> List[Tuple[str, float, Dict]]:
        """Rank companies by comprehensive investment score."""
        ranked = []
        
        for company, data in companies_data.items():
            raw_data = self.db_manager.get_latest_financial_data(company)
            if not raw_data:
                continue
            metrics = self._calculate_financial_metrics(raw_data)
            
            # Calculate composite score
            profitability_score = min(metrics['profit_margin'] * 2, 40)
            cash_score = min(abs(metrics['cash_conversion']) * 30, 30)
            debt_score = max(30 - metrics['debt_ratio'] * 10, 0)
            
            total_score = profitability_score + cash_score + debt_score
            ranked.append((company, total_score, metrics))
        
        return sorted(ranked, key=lambda x: x[1], reverse=True)
    
    def _assess_profitability(self, metrics: Dict[str, float]) -> str:
        """Assess profitability level."""
        margin = metrics['profit_margin']
        if margin > 25: return "Exceptional"
        elif margin > 15: return "Strong"
        elif margin > 10: return "Good"
        elif margin > 5: return "Fair"
        else: return "Weak"
    
    def _assess_financial_strength(self, metrics: Dict[str, float]) -> str:
        """Assess overall financial strength."""
        debt_ratio = metrics.get('debt_ratio', 0)
        if debt_ratio < 1: return "Very Strong"
        elif debt_ratio < 1.5: return "Strong"
        elif debt_ratio < 2.5: return "Moderate"
        else: return "Weak"
    
    def _assess_cash_generation(self, metrics: Dict[str, float]) -> str:
        """Assess cash generation capability."""
        conversion = metrics.get('cash_conversion', 0)
        if conversion > 0.8: return "Excellent"
        elif conversion > 0.6: return "Good"
        elif conversion > 0.4: return "Fair"
        else: return "Poor"
    
    def _determine_investment_grade(self, metrics: Dict[str, float]) -> str:
        """Determine investment grade based on metrics."""
        profit_margin = metrics['profit_margin']
        debt_ratio = metrics.get('debt_ratio', 0)
        
        if profit_margin > 20 and debt_ratio < 1.5:
            return "BUY - Strong fundamentals"
        elif profit_margin > 15 and debt_ratio < 2:
            return "HOLD - Good fundamentals"
        elif profit_margin > 10:
            return "HOLD - Fair fundamentals"
        else:
            return "CAUTION - Weak fundamentals"