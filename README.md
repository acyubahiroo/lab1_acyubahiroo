# Lab 1: Grade Evaluator & Archiver

A small Python application that evaluates a student's final academic standing
from a CSV of course grades, plus a Bash script that archives that CSV and
resets the workspace for the next batch.

## Files

- `grade-evaluator.py` – reads a grades CSV, validates it, calculates GPA,
  determines PASS/FAIL, and reports formative assignments eligible for
  resubmission.
- `organizer.sh` – archives `grades.csv` into `archive/` with a timestamped
  name, creates a fresh empty `grades.csv`, and logs the action to
  `organizer.log`.
- `grades.csv` – sample input data (assignment, group, score, weight).

## Requirements

- Python 3
- Bash (Linux/macOS/WSL)

## 1. Running the Python Grade Evaluator

From the project directory, run:

```bash
python3 grade-evaluator.py
```

You will be prompted to enter the filename to process:

```
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

The script will then print:

- The Summative and Formative percentage scores (each must reach 50% to pass)
- The overall Total Grade and final GPA (`GPA = (Total Grade / 100) * 5.0`)
- The final status: `PASSED` or `FAILED`
- Any formative assignment(s) eligible for resubmission — this is the
  failed formative assignment (score < 50) with the highest weight; if
  several failed assignments tie for the highest weight, all are listed

### Error handling

- If the file you enter does not exist, the script prints an error and exits.
- If the CSV file is empty (e.g. right after `organizer.sh` resets it), the
  script prints an error instead of crashing.
- If any score is outside the 0–100 range, or the weights don't sum to
  100 total / 40 Summative / 60 Formative, the script reports the problem
  and exits without producing incorrect results.

### CSV format expected

```csv
assignment,group,score,weight
Quiz,Formative,85,20
...
```

## 2. Running the Organizer Shell Script

Make the script executable (only needed once) and run it from the same
directory as `grades.csv`:

```bash
chmod +x organizer.sh
./organizer.sh
```

Each run will:

1. Create an `archive/` directory if it doesn't already exist.
2. Rename `grades.csv` by appending the current timestamp
   (e.g. `grades_20251105-170000.csv`) and move it into `archive/`.
3. Create a brand-new, empty `grades.csv` in the current directory.
4. Append a line to `organizer.log` recording the timestamp, the original
   filename, and the new archived filename.

You can run it as many times as you like — `organizer.log` accumulates one
entry per run, and each archived file gets its own unique timestamp.

## Typical Workflow

```bash
python3 grade-evaluator.py   # evaluate the current grades.csv
./organizer.sh                # archive it and reset grades.csv for the next batch
```
