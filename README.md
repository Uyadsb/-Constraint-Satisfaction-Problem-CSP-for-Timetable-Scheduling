# Constraint Satisfaction Problem (CSP) for Timetable Scheduling

This project builds a weekly timetable using a Constraint Satisfaction Problem (CSP) approach.

## Overview

The solver assigns course sessions (lectures, TD, TP) to time slots for groups G1, G2, and G3 while respecting hard constraints.

It uses:
- Backtracking search
- MRV (Minimum Remaining Values) heuristic
- Degree heuristic (tie-break)
- AC-3 style domain pruning

Main script: `tp2.py`

## Time Model

Available slots per day:
- Sun: 5
- Mon: 5
- Tue: 3
- Wed: 5
- Thu: 5

Total modeled slots: 23

## Hard Constraints Implemented

1. No overlap for the same group at the same time.
2. A teacher cannot teach two sessions at the same time.
3. Maximum 3 consecutive sessions per day per group.
4. Maximum 2 lectures per day per group.

## How to Run

Requirements:
- Python 3.8+

Run:

```bash
python tp2.py
```

The script will:
1. Generate a valid timetable (if one exists).
2. Print separate weekly schedules for each group (G1, G2, G3).

## Output

If a solution is found, the program prints formatted tables by group.
If not, it prints:

`No valid timetable could be found with these constraints.`

## Repository

GitHub: https://github.com/Uyadsb/-Constraint-Satisfaction-Problem-CSP-for-Timetable-Scheduling
