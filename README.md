* **CSP formulation of Zebra Puzzle**
* Solved with **Backtracking + MRV heuristic**
* Output: *Who drinks water? Who owns the fish?*

# Zebra Puzzle (CSP) – Classic 5 Houses

An interactive **Constraint Satisfaction Problem (CSP)** version of the classic Zebra Puzzle.  
Goal: assign a unique **Color, Nationality, Pet, Drink, and Sport** to each of the five houses so that **all clues are satisfied**.

> No spoilers here. The app is meant to be played — you’ll validate your own solution!


## The Clues
1. The Indian lives in the blue house.  
2. The Pakistani owns the parrot.  
3. Beer is drunk in the green house.  
4. The Mexican drinks Horchata.  
5. The green house is immediately to the right of the yellow house.  
6. The cricket player owns a monkey.  
7. Jogging is the preferred sport in the red house.  
8. Tea is drunk in the third house.  
9. The American lives in the first house.  
10. The person with a raccoon lives next to the swimmer.  
11. The jogger lives next to the owner of a dog.  
12. The Polo player drinks milk.  
13. The German likes soccer.  
14. The American lives next to the white house.

> Each house has a different **color, nationality, pet, drink, and sport**.  
> “Right” in clue #5 means “to the viewer’s right”.


## How to Play
- Open the web app and fill the 5×5 grid using dropdowns.  
- Click **Check Constraints** to see if your current choices are valid.  
- When every clue is satisfied, the app will show **Puzzle Solved**.

## Tech
- Python **backtracking CSP** with **MRV** (Minimum Remaining Values) and forward checking.  
- **Streamlit** web UI (interactive grid with validation).

## Run Locally
```bash
git clone https://github.com/hamdamme/csp-zebra-puzzle.git
cd csp-zebra-puzzle
pip install -r requirements.txt
streamlit run app.py

##  Project Structure
csp\_zebra/
├── csp\_solver.py      # Backtracking + MRV CSP solver
├── app.py             # Streamlit interface
├── requirements.txt   # Dependencies
└── README.md          # Project documentation