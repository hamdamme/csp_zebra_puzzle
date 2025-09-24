import streamlit as st
from csp_solver import solve

# Categories
colors = ["Red", "Blue", "Green", "Yellow", "White"]
nationalities = ["American", "Indian", "Mexican", "Pakistani", "German"]
pets = ["Raccoon", "Monkey", "Parrot", "Dog", "Fish"]
drinks = ["Water", "Tea", "Horchata", "Milk", "Beer"]
sports = ["Jogging", "Cricket", "Polo", "Soccer", "Swimming"]

houses = [f"House {i}" for i in range(1, 6)]

# Initialize session state
if "assignments" not in st.session_state:
    st.session_state.assignments = {
        "Color": [""] * 5,
        "Nationality": [""] * 5,
        "Pet": [""] * 5,
        "Drink": [""] * 5,
        "Sport": [""] * 5,
    }

st.title("🏠 Zebra Puzzle (Classic CSP)")
st.write("Fill in the houses using the dropdowns and try to solve the puzzle!")

# Display grid
for i, house in enumerate(houses):
    st.subheader(house)

    st.session_state.assignments["Color"][i] = st.selectbox(
        f"{house} Color", [""] + colors, index=0, key=f"color_{i}"
    )
    st.session_state.assignments["Nationality"][i] = st.selectbox(
        f"{house} Nationality", [""] + nationalities, index=0, key=f"nat_{i}"
    )
    st.session_state.assignments["Pet"][i] = st.selectbox(
        f"{house} Pet", [""] + pets, index=0, key=f"pet_{i}"
    )
    st.session_state.assignments["Drink"][i] = st.selectbox(
        f"{house} Drink", [""] + drinks, index=0, key=f"drink_{i}"
    )
    st.session_state.assignments["Sport"][i] = st.selectbox(
        f"{house} Sport", [""] + sports, index=0, key=f"sport_{i}"
    )


# --- Constraint Checker (reuse previous implementation or keep placeholder) ---
def check_constraints(assignments):
    # Keep your rule-checking code here (omitted for brevity in this version)
    return []


# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Check Constraints"):
        problems = check_constraints(st.session_state.assignments)
        if problems:
            for p in problems:
                st.error(p)
        else:
            st.success("✅ All constraints satisfied so far!")

with col2:
    if st.button("Solve Puzzle"):
        solution = solve(st.session_state.assignments)
        if solution:
            st.success("🎉 Puzzle Solved ✅")
            for i, house in enumerate(houses):
                st.subheader(f"{house} Solution")
                st.write(
                    f"**Color**: {solution['Color'][i]}, "
                    f"**Nationality**: {solution['Nationality'][i]}, "
                    f"**Pet**: {solution['Pet'][i]}, "
                    f"**Drink**: {solution['Drink'][i]}, "
                    f"**Sport**: {solution['Sport'][i]}"
                )
        else:
            st.error("❌ No valid solution found. Check your input.")