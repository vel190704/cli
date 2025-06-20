# Oil & Gas Financial Analysis Chatbot

## Overview

This is a Python-based CLI chatbot designed to provide intelligent financial analysis for major oil and gas companies (Shell, BP, ExxonMobil, and Chevron). The application leverages OpenAI's GPT-4o model to deliver conversational financial insights based on stored financial data.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Components
- **Main Application**: CLI-based chatbot interface (`main.py`)
- **Configuration Management**: Centralized settings and environment handling (`config.py`)
- **Database Layer**: SQLite-based data storage for financial reports
- **LLM Integration**: OpenAI GPT-4o interface for intelligent responses
- **Data Management**: Financial data retrieval and processing
- **Utilities**: Prompt templates and helper functions

### Technology Stack
- **Runtime**: Python 3.11
- **AI/ML**: OpenAI GPT-4o API, Anthropic Claude (backup)
- **Database**: SQLite
- **Deployment**: Replit with Nix package management

## Key Components

### 1. Database Architecture (`src/database/`)
- **Solution**: SQLite database for local data storage
- **Rationale**: Lightweight, serverless database suitable for prototype/demo applications
- **Tables**: Companies, financial reports, and related metadata
- **Location**: `data/financial_chatbot.db`

### 2. LLM Integration (`src/llm/`)
- **Primary**: OpenAI GPT-4o API integration
- **Model**: gpt-4o (latest model as of May 13, 2024)
- **Configuration**: Temperature 0.3 for consistent financial analysis, 2000 max tokens
- **Fallback**: Anthropic Claude support available but not actively used

### 3. Data Management (`src/data/`)
- **Approach**: Synthetic data generation for demonstration purposes
- **Companies**: Shell, BP, ExxonMobil, Chevron
- **Data Types**: Quarterly earnings, production metrics, cash flow data
- **Future**: Designed for easy integration with real financial APIs

### 4. Prompt Engineering (`src/utils/`)
- **Strategy**: Specialized prompt templates for different query types
- **Categories**: Company comparisons, performance analysis, trend analysis
- **Personality**: Professional financial analyst with engaging communication style

## Data Flow

1. **Initialization**: Application starts, checks OpenAI API availability
2. **Data Loading**: Checks for existing financial data or generates synthetic data
3. **User Interaction**: CLI-based conversational interface
4. **Query Processing**: User queries are analyzed and categorized
5. **Data Retrieval**: Relevant financial data fetched from SQLite database
6. **LLM Processing**: OpenAI GPT-4o generates intelligent responses using prompt templates
7. **Response Delivery**: Formatted financial analysis delivered to user

## External Dependencies

### APIs and Services
- **OpenAI API**: Primary LLM service requiring API key
- **Anthropic Claude**: Backup LLM service (configured but not actively used)

### Python Packages
- `openai>=1.88.0`: OpenAI API client
- `anthropic>=0.54.0`: Anthropic API client
- Built-in libraries: `sqlite3`, `asyncio`, `pathlib`, `logging`

### Environment Variables
- `OPENAI_API_KEY`: Required for OpenAI API access

## Deployment Strategy

### Development Environment
- **Platform**: Replit with Nix package management
- **Python Version**: 3.11
- **Package Management**: UV lock file for dependency management
- **Execution**: Direct Python execution via `python main.py`

### Production Considerations
- Application is designed for easy containerization
- Database can be migrated to PostgreSQL for production use
- Environment variables properly configured for different deployment environments
- Logging configured for production monitoring

### Scalability Notes
- Current SQLite implementation suitable for demo/prototype
- Architecture supports migration to PostgreSQL or other databases
- LLM integration designed for easy switching between providers
- Modular structure allows for horizontal scaling of components

## Changelog
- June 20, 2025: Initial setup
- June 20, 2025: Fixed Ollama integration issue by implementing OpenAI cloud LLM integration
- June 20, 2025: Added intelligent fallback responses with actual financial data analysis
- June 20, 2025: Enhanced comparative analytics functionality for quota-limited scenarios

## User Preferences

Preferred communication style: Simple, everyday language.