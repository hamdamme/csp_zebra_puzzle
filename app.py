import streamlit as st

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


# --- Constraint Checker ---
def check_constraints(assignments):
    errors = []

    # Rule examples (not exhaustive yet):
    # 1. Indian lives in the blue house
    for i in range(5):
        if assignments["Nationality"][i] == "Indian" and assignments["Color"][i] not in ["", "Blue"]:
            errors.append(f"Rule broken: Indian must live in the Blue house (House {i+1}).")

    # 2. Pakistani owns the parrot
    for i in range(5):
        if assignments["Nationality"][i] == "Pakistani" and assignments["Pet"][i] not in ["", "Parrot"]:
            errors.append(f"Rule broken: Pakistani must own the Parrot (House {i+1}).")

    # 3. Beer is drunk in the green house
    for i in range(5):
        if assignments["Color"][i] == "Green" and assignments["Drink"][i] not in ["", "Beer"]:
            errors.append(f"Rule broken: Beer must be drunk in the Green house (House {i+1}).")

    # 8. Tea is drunk in the third house
    if assignments["Drink"][2] not in ["", "Tea"]:
        errors.append("Rule broken: Tea must be drunk in House 3.")

    # 9. American lives in the first house
    if assignments["Nationality"][0] not in ["", "American"]:
        errors.append("Rule broken: American must live in House 1.")

    return errors


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
        st.info("Solver integration will be added here.")