# ConstraintLab

An interactive constraint satisfaction application built with Python and Streamlit. It demonstrates backtracking search, the Minimum Remaining Values (MRV) heuristic, and constraint validation using a five-house Zebra example.

## Current scope

- Assign values in an interactive grid and validate a complete assignment.
- Complete a partial assignment with the solver, or report when no solution exists.
- Enforce unique values in each category and all 14 example constraints.
- Inspect the example constraints and resulting assignment in the interface.

The current model is specific to the five-house example. A configurable model for scheduling or resource allocation is future work, not an implemented feature.

## Architecture

`csp_solver.py` defines domains, fixed clues, consistency checks, and backtracking with MRV variable selection. Category values are removed from other houses after assignment. `app.py` uses the same validator and solver, so manual validation and search follow the same rules. Streamlit session state stores the current grid.

## Requirements and setup

Use Python 3.12 or later.

```sh
git clone https://github.com/hamdamme/constraintlab.git
cd constraintlab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Testing

```sh
python3 -m unittest discover -s tests
```

Regression tests cover valid solutions, duplicate values, incomplete grids, contradictions with fixed clues, invalid complete assignments, and unknown values.

## Deployment

`render.yaml` defines a Python web service with a Streamlit start command that uses Render's assigned port. The existing demo URL is https://csp-zebra-puzzle.onrender.com/. Repository branding does not change the existing service URL.

## Project files

- `app.py`: interactive interface
- `csp_solver.py`: search and validation
- `tests/test_solver.py`: solver regression tests
- `requirements.txt`: application dependencies
- `render.yaml`: deployment configuration
- `ROADMAP.md`: scope and progress

See `LICENSE` for license terms.

After a repository rename, verify the linked repository and branch in Render settings before deploying the latest commit. The live interface should display ConstraintLab.
