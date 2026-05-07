# Agentic Python Debugger

An AI-powered automated code debugging and refactoring system that uses a multi-agent architecture to identify, fix, and optimize Python code. This system leverages Google's Gemini API to provide intelligent code analysis and corrections.

## 📋 Overview

The Agentic Python Debugger is a sophisticated debugging framework that orchestrates multiple AI agents to automatically:
- **Execute** code and capture runtime errors, syntax errors, and test failures
- **Analyze** execution results to identify root causes and pinpoint errors
- **Fix** identified issues iteratively until the code runs correctly
- **Critique** passing code to ensure quality, optimization, and best practices

This project implements an agentic workflow pattern where specialized agents collaborate to progressively improve code quality through multiple iterations.

## 🏗️ Architecture

The system follows a 4-agent pipeline architecture:

### 1. **Executor Agent**
   - Runs the provided Python code in a sandbox environment
   - Captures compilation errors, runtime exceptions, and output
   - Generates test cases based on code and context
   - Returns structured execution results with error details

### 2. **Analyzer Agent**
   - Analyzes execution results and identifies all errors
   - Categorizes errors (syntax, runtime, logic)
   - Pinpoints exact line numbers and error locations
   - Provides concrete fix suggestions
   - Returns assessment of code correctness

### 3. **Fixer Agent**
   - Receives analysis report with identified issues
   - Generates corrected code addressing all issues
   - Maintains original code intent while fixing errors
   - Prepares code for re-execution and validation

### 4. **Critic Agent**
   - Reviews functionally correct code
   - Evaluates code quality, structure, and optimization
   - Checks for readability and best practices
   - Approves code for production or flags improvements needed

### **Iterative Loop**
The pipeline iterates through Executor → Analyzer → Fixer until code is functionally correct (max 3 iterations). Once correct, the Critic reviews the code. If Critic flags issues, code returns to Fixer for optimization.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Generative AI API key (free tier available)

### Setup Instructions

#### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/asmitp06/agentic-python-debugger
cd agentic-python-debugger

# Install required packages
pip install -r requirements.txt
```

#### 2. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
touch .env
```

Edit the `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

**To get a free Gemini API key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key and paste it in the `.env` file

### Dependencies

The project requires the following packages (see `requirements.txt`):
- `google-genai` - Google Generative AI client
- `python-dotenv` - Environment variable management
- `langchain` - LLM framework
- `langchain-google-genai` - Gemini integration for LangChain

## 📖 Usage

### Running the Debugger

#### Command Line

```bash
python main.py <file_path> <context_file>
```

**Arguments:**
- `<file_path>` - Path to the Python file you want to debug (e.g., `./samples/broken_logic.py`)
- `<context_file>` - Path to a text file containing context about the code (e.g., expected behavior, requirements)

**Example:**
```bash
python main.py ./samples/broken_logic.py ./context.txt
```

#### Interactive GUI Mode

If no arguments are provided, the system will open file dialogs:

```bash
python main.py
```

The system will prompt you to:
1. Select a Python file to debug
2. Select a context file with additional information

### Example Workflow

1. **Create a context file** (optional but recommended):
```
# context.txt
The function should calculate the factorial of a number.
Input: 5
Expected output: 120
```

2. **Run the debugger**:
```bash
python main.py samples/broken_logic.py context.txt
```

3. **Monitor the output**: The system will display:
   - Execution results
   - Analysis of errors
   - Fixes applied
   - Final code review

## 📁 Project Structure

```
agentic-python-debugger/
├── main.py                 # Entry point - orchestrates the pipeline
├── state.py                # AgentState dataclass for pipeline state management
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── agents/
│   ├── __init__.py
│   ├── executor.py         # Executes code and captures errors
│   ├── analyzer.py         # Analyzes execution results
│   ├── fixer.py            # Fixes identified issues
│   └── critic.py           # Reviews code quality and optimization
├── utils/
│   ├── __init__.py
│   └── llm_client.py       # LLM integration with LangChain and Gemini
├── samples/                # Sample broken code files for testing
│   ├── broken_logic.py
│   ├── broken_normalization.py
│   ├── broken_runtime.py
│   └── broken_syntax.py
└── corrected/              # Reference corrected versions of samples
    ├── broken_logic.py
    ├── broken_normalization.py
    ├── broken_runtime.py
    └── broken_syntax.py
```

## 🔍 Sample Files

The `samples/` directory contains test cases with intentional bugs for demonstration:

- **broken_syntax.py** - Code with syntax errors
- **broken_runtime.py** - Code that crashes at runtime
- **broken_logic.py** - Code with incorrect logic
- **broken_normalization.py** - Code with data handling issues

Use these to test the debugging pipeline:
```bash
python main.py samples/broken_syntax.py context.txt
```

## 🛠️ Configuration

### Agent Parameters

The system behavior can be configured in `state.py`:
- `max_fix_attempts` - Maximum iterations for the fix loop (default: 3)
- `max_critic_attempts` - Maximum iterations for critic review (default: 1)

### LLM Settings

Configure the Gemini model in `utils/llm_client.py`:
- **Model**: `gemini-2.5-flash` (optimized for speed and cost)
- **Temperature**: `0.0` (deterministic responses for debugging)

## 📊 Output

The system produces detailed logs for each stage:

```
============================================================
  AUTOMATED CODE DEBUGGER & REFACTORING AGENT
============================================================

── Iteration 1 ──────────────────────────────
Executor Result:
{
  "compiled": true,
  "ran": false,
  "error_type": "ValueError",
  ...
}

Analyzer Result:
{
  "is_correct": false,
  "issues": [...],
  ...
}
```

## 🎯 Use Cases

- **Educational**: Learn how code breaks and how to fix it
- **Development**: Automatically debug broken code during development
- **Code Review**: Get AI-powered code quality feedback
- **Testing**: Validate code against test cases and fix failures
- **Refactoring**: Improve code structure and optimization

## ⚠️ Limitations

- Maximum 3 fix attempts per execution (prevents infinite loops)
- Best suited for Python code debugging
- Requires valid API key with sufficient quota
- May not handle extremely complex code structures
- Context file should clearly describe expected behavior

## 📝 Submission Details
- Created By: Asmit Patidar, Xhaiden D'Souza, and Shashank Karra
- CS 301: Project Track 2: Agentic AI System Design and Multi-Step Workflow Implementation