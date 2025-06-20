#!/usr/bin/env python3
"""
Oil & Gas Financial Analysis Chatbot
Main entry point for the CLI-based chatbot
"""

import sys
import os
import argparse
import asyncio
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import DatabaseManager
from src.llm.openai_interface import OpenAIInterface
from src.data.financial_data import FinancialDataManager
from config import Config

class FinancialChatbot:
    def __init__(self):
        """Initialize the chatbot with all required components."""
        print("🛢️  Oil & Gas Financial Analysis Chatbot")
        print("=" * 50)
        print("🚀 Starting conversational interface...")
        
        # Initialize components
        self.config = Config()
        self.db_manager = DatabaseManager()
        self.llm_interface = OpenAIInterface()
        self.data_manager = FinancialDataManager(self.db_manager)
        
        # Check if we can connect to OpenAI
        if not self.llm_interface.is_available():
            print("⚠️ OpenAI API has limited availability. Running with basic responses.")
            print("💡 For full intelligent analysis, check your API credits at platform.openai.com/billing")
        else:
            print("✅ OpenAI API connected successfully")
        
    async def initialize_data(self, full_update=False):
        """Initialize or update financial data."""
        print("\n🔍 Checking for latest financial reports...")
        
        if full_update:
            print("📥 Downloading latest reports...")
            await self.data_manager.update_all_reports()
            print("✅ Reports updated successfully")
        else:
            # Check if we have existing data
            companies = ['Shell', 'BP', 'ExxonMobil', 'Chevron']
            has_data = all(self.data_manager.has_recent_data(company) for company in companies)
            
            if has_data:
                print("✅ Found existing reports. Use 'refresh' command to update.")
            else:
                print("📥 No recent data found. Downloading initial reports...")
                await self.data_manager.update_all_reports()
                print("✅ Initial data loaded successfully")
    
    def display_welcome_message(self):
        """Display welcome message and instructions."""
        print("\n" + "=" * 60)
        print("🛢️  Oil & Gas Financial Analysis Chatbot")
        print("=" * 60)
        
        print("\nHey there! 👋\n")
        print("I'm your Oil & Gas Financial Analyst, and I'm here to help you dive deep into the latest quarterly earnings from the major energy companies.\n")
        print("I have access to the most recent financial reports from Shell, BP, ExxonMobil, and Chevron, and I can help you understand everything from revenue trends to production metrics, cash flow analysis, and strategic insights.\n")
        print("What would you like to explore? You could ask me something like:")
        print("• \"How did the oil majors perform this quarter?\"")
        print("• \"Compare Shell and BP's latest results\"")
        print("• \"What's driving ExxonMobil's cash flow?\"")
        print("• \"Show me production trends across companies\"")
        print("• \"What are the key risks facing these companies?\"")
        print("• Or anything else that's on your mind about these companies!\n")
        print("Special commands:")
        print("• 'refresh' - Update financial data")
        print("• 'companies' - List available companies")
        print("• 'exit' or 'quit' - End conversation\n")
        print("What interests you most?\n")
    
    async def process_query(self, user_input: str) -> str:
        """Process user query and return intelligent response."""
        user_input = user_input.strip()
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit']:
            return "exit"
        elif user_input.lower() == 'refresh':
            print("📥 Updating financial reports...")
            await self.data_manager.update_all_reports()
            return "✅ Financial reports updated successfully!"
        elif user_input.lower() == 'companies':
            companies = self.data_manager.get_available_companies()
            return f"📊 Available companies: {', '.join(companies)}"
        
        # Get relevant financial data for context
        context_data = self.data_manager.get_context_for_query(user_input)
        
        # Generate intelligent response
        print("🤔 Analyzing your question...")
        response = await self.llm_interface.generate_response(user_input, context_data)
        
        return response
    
    async def run_interactive_mode(self):
        """Run the chatbot in interactive mode."""
        self.display_welcome_message()
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                response = await self.process_query(user_input)
                
                if response == "exit":
                    print("\n👋 Thanks for using the Oil & Gas Financial Analysis Chatbot!")
                    print("Stay informed and make great investment decisions! 📈")
                    break
                
                print(f"\n🤖 Assistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using the Oil & Gas Financial Analysis Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'exit' to quit.\n")

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Oil & Gas Financial Analysis Chatbot')
    parser.add_argument('--full-update', action='store_true', 
                       help='Download latest reports before starting')
    parser.add_argument('--query', type=str, 
                       help='Ask a single question and exit')
    
    args = parser.parse_args()
    
    try:
        # Initialize chatbot
        chatbot = FinancialChatbot()
        
        # Initialize data
        await chatbot.initialize_data(full_update=args.full_update)
        
        if args.query:
            # Single query mode
            response = await chatbot.process_query(args.query)
            print(f"\n🤖 Assistant: {response}")
        else:
            # Interactive mode
            await chatbot.run_interactive_mode()
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
