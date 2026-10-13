import pandas as pd
import streamlit as st

from csp_solver import (
    COLORS, NATIONALITIES, PETS, DRINKS, SPORTS, check_constraints, solve,
)

st.set_page_config(
    page_title="ConstraintLab", page_icon="assets/favicon.png", layout="wide"
)
st.markdown('<a href="https://www.hamdam.me/#projects" target="_self">← Back to portfolio</a>', unsafe_allow_html=True)
st.title("ConstraintLab")
st.caption("Interactive constraint satisfaction with backtracking and MRV search")
st.write("Explore the five-house Zebra example. Assign values manually, validate the grid, or complete your assignments with the solver.")

categories = {
    "Color": (COLORS, "color"),
    "Nationality": (NATIONALITIES, "nat"),
    "Pet": (PETS, "pet"),
    "Drink": (DRINKS, "drink"),
    "Sport": (SPORTS, "sport"),
}

def current_assignment():
    return {
        category: [st.session_state.get(f"{prefix}_{i}", "") for i in range(5)]
        for category, (_, prefix) in categories.items()
    }

def complete_assignment():
    result = solve(current_assignment())
    if result is None:
        st.session_state["solver_message"] = "No solution satisfies these assignments. Revise your selections and try again."
        return
    for category, (_, prefix) in categories.items():
        for i, value in enumerate(result[category]):
            st.session_state[f"{prefix}_{i}"] = value
    st.session_state["solver_message"] = ""

with st.expander("Example constraints"):
    st.markdown("""
Each category uses every value exactly once.

1. The Indian lives in the blue house.
2. The Pakistani owns the parrot.
3. Beer is drunk in the green house.
4. The Mexican drinks Horchata.
5. Green is immediately to the right of yellow.
6. The cricket player owns a monkey.
7. Jogging is the sport in the red house.
8. Tea is drunk in the third house.
9. The American lives in the first house.
10. The raccoon owner lives next to the swimmer.
11. The jogger lives next to the dog owner.
12. The polo player drinks milk.
13. The German likes soccer.
14. The American lives next to the white house.
""")

for i, column in enumerate(st.columns(5)):
    with column:
        st.subheader(f"House {i + 1}")
        for category, (values, prefix) in categories.items():
            st.selectbox(category, [""] + values, key=f"{prefix}_{i}")

validate = st.button("Validate assignment", type="primary")
st.button("Complete with solver", on_click=complete_assignment)
if st.session_state.get("solver_message"):
    st.warning(st.session_state["solver_message"])

assignment = current_assignment()
st.subheader("Current assignment")
st.dataframe(pd.DataFrame(assignment, index=[f"House {i + 1}" for i in range(5)]), width="stretch")
if validate:
    if check_constraints(assignment):
        st.success("Valid assignment: every category and all 14 constraints are satisfied.")
    else:
        st.error("Invalid assignment: complete every field, use each category value once, and satisfy all 14 constraints.")
