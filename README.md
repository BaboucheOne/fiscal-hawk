
# Finances CLI App

This project helps you plan future expenses, track incomes, and see what you can save. It provides a CLI interface and a mini dashboard summary.

## Setup

1. Create the virtual environment:
   ```sh
   python3 -m venv .venv
   ```
2. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```
3. Install dependencies (if any):
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the CLI app:
```sh
.venv/bin/python cli_app.py <command> [options]
```

### Commands

- Add an expense:
  ```sh
  .venv/bin/python cli_app.py add-expense <amount> <description>
  ```
- Add an income:
  ```sh
  .venv/bin/python cli_app.py add-income <amount> <description>
  ```
- Show dashboard summary:
  ```sh
  .venv/bin/python cli_app.py dashboard
  ```

## Project Structure
- `cli_app.py`: Main CLI application
- `main.py`: Placeholder entry point
- `requirements.txt`: Dependencies
- `finances_data.json`: Data storage for expenses and incomes
- `.venv/`: Virtual environment
- `.github/copilot-instructions.md`: Copilot instructions
