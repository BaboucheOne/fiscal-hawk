
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

## finances.yml example and usage

The app now reads `finances.yml` (YAML) from the project root. Create a `finances.yml` file with the following structure as an example:

```yaml
incomes:
  - name: Salary
    value: 1500
    time: MONTH
    future_value: 1800
    future_date: "2025-05"

expenses:
  - name: Rent
    value: 350
    time: MONTH
  - name: Spotify
    value: 16
    time: MONTH

saving:
   warning_percentage: 75
   items:
    - name: Vacation
      target: 2000

market:
  etf:
    - name: "VGRO"
      price: 10000

simulation:
    runs: 100
    until_year: 2050
    max_annual_rate: 0.1
    min_annual_rate: -0.1
```

Notes:
- `time` accepts `DAY`, `MONTH`, or `ANNUAL`.
- `value` and `target` are numeric. Monthly values are used in the TUI summary.

