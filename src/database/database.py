"""
Database manager for storing and retrieving financial data
"""

import sqlite3
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from config import Config

# Setup logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database for financial data storage."""
    
    def __init__(self):
        """Initialize database manager."""
        Config.ensure_directories()
        self.db_path = Config.DATABASE_PATH
        self._init_database()
        logger.info(f"Database initialized at: {self.db_path}")
    
    def _init_database(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Companies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    symbol TEXT,
                    sector TEXT DEFAULT 'Oil & Gas',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Financial reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS financial_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    report_type TEXT NOT NULL,
                    quarter TEXT,
                    year INTEGER,
                    report_date DATE,
                    revenue REAL,
                    net_income REAL,
                    operating_income REAL,
                    free_cash_flow REAL,
                    total_debt REAL,
                    cash_and_equivalents REAL,
                    production_volume REAL,
                    production_unit TEXT,
                    raw_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (id)
                )
            """)
            
            # Key metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS key_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    metric_unit TEXT,
                    period TEXT,
                    report_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (id)
                )
            """)
            
            # Market data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    stock_price REAL,
                    market_cap REAL,
                    pe_ratio REAL,
                    dividend_yield REAL,
                    data_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (id)
                )
            """)
            
            conn.commit()
            
        # Initialize default companies
        self._init_default_companies()
    
    def _init_default_companies(self):
        """Initialize default oil & gas companies."""
        companies = [
            ("Shell", "SHEL", "Oil & Gas"),
            ("BP", "BP", "Oil & Gas"),
            ("ExxonMobil", "XOM", "Oil & Gas"),
            ("Chevron", "CVX", "Oil & Gas")
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for name, symbol, sector in companies:
                cursor.execute("""
                    INSERT OR IGNORE INTO companies (name, symbol, sector)
                    VALUES (?, ?, ?)
                """, (name, symbol, sector))
            conn.commit()
    
    def get_company_id(self, company_name: str) -> Optional[int]:
        """Get company ID by name."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM companies WHERE name = ?", (company_name,))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def store_financial_report(self, company_name: str, report_data: Dict[str, Any]) -> bool:
        """Store financial report data."""
        try:
            company_id = self.get_company_id(company_name)
            if not company_id:
                logger.error(f"Company {company_name} not found")
                return False
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO financial_reports (
                        company_id, report_type, quarter, year, report_date,
                        revenue, net_income, operating_income, free_cash_flow,
                        total_debt, cash_and_equivalents, production_volume,
                        production_unit, raw_data, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    company_id,
                    report_data.get('report_type', 'quarterly'),
                    report_data.get('quarter'),
                    report_data.get('year'),
                    report_data.get('report_date'),
                    report_data.get('revenue'),
                    report_data.get('net_income'),
                    report_data.get('operating_income'),
                    report_data.get('free_cash_flow'),
                    report_data.get('total_debt'),
                    report_data.get('cash_and_equivalents'),
                    report_data.get('production_volume'),
                    report_data.get('production_unit'),
                    json.dumps(report_data)
                ))
                conn.commit()
            
            logger.info(f"Stored financial report for {company_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing financial report for {company_name}: {e}")
            return False
    
    def get_latest_financial_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Get latest financial data for a company."""
        company_id = self.get_company_id(company_name)
        if not company_id:
            return None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM financial_reports 
                WHERE company_id = ? 
                ORDER BY report_date DESC, created_at DESC 
                LIMIT 1
            """, (company_id,))
            
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
        
        return None
    
    def get_financial_comparison_data(self, companies: List[str]) -> Dict[str, Any]:
        """Get financial data for multiple companies for comparison."""
        comparison_data = {}
        
        for company in companies:
            data = self.get_latest_financial_data(company)
            if data:
                comparison_data[company] = data
        
        return comparison_data
    
    def get_historical_trends(self, company_name: str, metric: str, periods: int = 4) -> List[Dict[str, Any]]:
        """Get historical trends for a specific metric."""
        company_id = self.get_company_id(company_name)
        if not company_id:
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT quarter, year, {metric}, report_date
                FROM financial_reports 
                WHERE company_id = ? AND {metric} IS NOT NULL
                ORDER BY report_date DESC
                LIMIT ?
            """, (company_id, periods))
            
            results = cursor.fetchall()
            columns = ['quarter', 'year', metric, 'report_date']
            return [dict(zip(columns, row)) for row in results]
    
    def search_companies_by_metric(self, metric: str, min_value: float = None, max_value: float = None) -> List[Dict[str, Any]]:
        """Search companies by specific metric criteria."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT c.name, c.symbol, fr.{} as metric_value, fr.report_date
                FROM companies c
                JOIN financial_reports fr ON c.id = fr.company_id
                WHERE fr.{} IS NOT NULL
            """.format(metric, metric)
            
            params = []
            if min_value is not None:
                query += f" AND fr.{metric} >= ?"
                params.append(min_value)
            if max_value is not None:
                query += f" AND fr.{metric} <= ?"
                params.append(max_value)
            
            query += " ORDER BY fr.report_date DESC"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            columns = ['company', 'symbol', 'metric_value', 'report_date']
            return [dict(zip(columns, row)) for row in results]
    
    def has_recent_data(self, company_name: str, days: int = 90) -> bool:
        """Check if we have recent data for a company."""
        company_id = self.get_company_id(company_name)
        if not company_id:
            return False
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM financial_reports 
                WHERE company_id = ? AND created_at > ?
            """, (company_id, cutoff_date.isoformat()))
            
            count = cursor.fetchone()[0]
            return count > 0
    
    def get_all_companies(self) -> List[Dict[str, str]]:
        """Get all companies in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, symbol, sector FROM companies ORDER BY name")
            results = cursor.fetchall()
            columns = ['name', 'symbol', 'sector']
            return [dict(zip(columns, row)) for row in results]
