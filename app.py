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

    # 1. Indian lives in the blue house
    for i in range(5):
        if assignments["Nationality"][i] == "Indian" and assignments["Color"][i] not in ["", "Blue"]:
            errors.append("Indian must live in the Blue house.")

    # 2. Pakistani owns the parrot
    for i in range(5):
        if assignments["Nationality"][i] == "Pakistani" and assignments["Pet"][i] not in ["", "Parrot"]:
            errors.append("Pakistani must own the Parrot.")

    # 3. Beer is drunk in the green house
    for i in range(5):
        if assignments["Color"][i] == "Green" and assignments["Drink"][i] not in ["", "Beer"]:
            errors.append("Beer must be drunk in the Green house.")

    # 4. Mexican drinks Horchata
    for i in range(5):
        if assignments["Nationality"][i] == "Mexican" and assignments["Drink"][i] not in ["", "Horchata"]:
            errors.append("Mexican must drink Horchata.")

    # 5. Green house is immediately to the right of the yellow house
    for i in range(4):  # house 1–4 can be yellow
        if assignments["Color"][i] == "Yellow" and assignments["Color"][i+1] not in ["", "Green"]:
            errors.append("Green house must be immediately to the right of Yellow.")

    # 6. Cricket player owns a monkey
    for i in range(5):
        if assignments["Sport"][i] == "Cricket" and assignments["Pet"][i] not in ["", "Monkey"]:
            errors.append("Cricket player must own a Monkey.")

    # 7. Jogging is the preferred sport in the red house
    for i in range(5):
        if assignments["Color"][i] == "Red" and assignments["Sport"][i] not in ["", "Jogging"]:
            errors.append("Jogging must be in the Red house.")

    # 8. Tea is drunk in the third house
    if assignments["Drink"][2] not in ["", "Tea"]:
        errors.append("Tea must be drunk in House 3.")

    # 9. American lives in the first house
    if assignments["Nationality"][0] not in ["", "American"]:
        errors.append("American must live in House 1.")

    # 10. Person with a raccoon lives next to the swimmer
    for i in range(5):
        if assignments["Pet"][i] == "Raccoon":
            if (i > 0 and assignments["Sport"][i-1] == "Swimming") or (i < 4 and assignments["Sport"][i+1] == "Swimming"):
                pass
            else:
                errors.append("Raccoon owner must live next to a Swimmer.")

    # 11. Jogger lives next to the owner of a dog
    for i in range(5):
        if assignments["Sport"][i] == "Jogging":
            if (i > 0 and assignments["Pet"][i-1] == "Dog") or (i < 4 and assignments["Pet"][i+1] == "Dog"):
                pass
            else:
                errors.append("Jogger must live next to the owner of a Dog.")

    # 12. Polo player drinks milk
    for i in range(5):
        if assignments["Sport"][i] == "Polo" and assignments["Drink"][i] not in ["", "Milk"]:
            errors.append("Polo player must drink Milk.")

    # 13. German likes soccer
    for i in range(5):
        if assignments["Nationality"][i] == "German" and assignments["Sport"][i] not in ["", "Soccer"]:
            errors.append("German must like Soccer.")

    # 14. American lives next to the white house
    for i in range(5):
        if assignments["Nationality"][i] == "American":
            if (i > 0 and assignments["Color"][i-1] == "White") or (i < 4 and assignments["Color"][i+1] == "White"):
                pass
            else:
                errors.append("American must live next to the White house.")

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