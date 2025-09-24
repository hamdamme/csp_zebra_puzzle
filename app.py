import streamlit as st
import pandas as pd
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
cols = st.columns(5)

for i, house in enumerate(houses):
    with cols[i]:
        st.markdown(f"### {house}")

        st.session_state.assignments["Color"][i] = st.selectbox(
            "Color", [""] + colors, index=0, key=f"color_{i}"
        )
        st.session_state.assignments["Nationality"][i] = st.selectbox(
            "Nationality", [""] + nationalities, index=0, key=f"nat_{i}"
        )
        st.session_state.assignments["Pet"][i] = st.selectbox(
            "Pet", [""] + pets, index=0, key=f"pet_{i}"
        )
        st.session_state.assignments["Drink"][i] = st.selectbox(
            "Drink", [""] + drinks, index=0, key=f"drink_{i}"
        )
        st.session_state.assignments["Sport"][i] = st.selectbox(
            "Sport", [""] + sports, index=0, key=f"sport_{i}"
        )

# ---------------- Constraint Checker ---------------- #
def check_constraints(assignments):
    errors = {}

    # Rule 1: The Indian lives in the blue house.
    for i in range(5):
        if assignments["Nationality"][i] == "Indian" and assignments["Color"][i] not in ["", "Blue"]:
            errors[(i, "Color")] = "Indian must live in Blue house."

    # Rule 2: The Pakistani owns the parrot.
    for i in range(5):
        if assignments["Nationality"][i] == "Pakistani" and assignments["Pet"][i] not in ["", "Parrot"]:
            errors[(i, "Pet")] = "Pakistani must own the Parrot."

    # Rule 3: Beer is drunk in the green house.
    for i in range(5):
        if assignments["Color"][i] == "Green" and assignments["Drink"][i] not in ["", "Beer"]:
            errors[(i, "Drink")] = "Beer must be drunk in Green house."

    # Rule 4: The Mexican drinks Horchata.
    for i in range(5):
        if assignments["Nationality"][i] == "Mexican" and assignments["Drink"][i] not in ["", "Horchata"]:
            errors[(i, "Drink")] = "Mexican must drink Horchata."

    # Rule 5: The green house is immediately to the right of the yellow house.
    for i in range(4):
        if assignments["Color"][i] == "Yellow" and assignments["Color"][i + 1] not in ["", "Green"]:
            errors[(i + 1, "Color")] = "Green house must be right of Yellow house."

    # Rule 6: The cricket player owns a monkey.
    for i in range(5):
        if assignments["Sport"][i] == "Cricket" and assignments["Pet"][i] not in ["", "Monkey"]:
            errors[(i, "Pet")] = "Cricket player must own Monkey."

    # Rule 7: Jogging is the preferred sport in the red house.
    for i in range(5):
        if assignments["Color"][i] == "Red" and assignments["Sport"][i] not in ["", "Jogging"]:
            errors[(i, "Sport")] = "Jogging must be in Red house."

    # Rule 8: Tea is drunk in the third house.
    if assignments["Drink"][2] not in ["", "Tea"]:
        errors[(2, "Drink")] = "Tea must be drunk in House 3."

    # Rule 9: The American lives in the first house.
    if assignments["Nationality"][0] not in ["", "American"]:
        errors[(0, "Nationality")] = "American must live in House 1."

    # Rule 10: The person with a raccoon lives next to the swimmer.
    for i in range(5):
        if assignments["Pet"][i] == "Raccoon":
            if not (
                (i > 0 and assignments["Sport"][i - 1] in ["", "Swimming"])
                or (i < 4 and assignments["Sport"][i + 1] in ["", "Swimming"])
            ):
                errors[(i, "Pet")] = "Raccoon must be next to Swimmer."

    # Rule 11: The jogger lives next to the owner of a dog.
    for i in range(5):
        if assignments["Sport"][i] == "Jogging":
            if not (
                (i > 0 and assignments["Pet"][i - 1] in ["", "Dog"])
                or (i < 4 and assignments["Pet"][i + 1] in ["", "Dog"])
            ):
                errors[(i, "Sport")] = "Jogger must be next to Dog owner."

    # Rule 12: The Polo player drinks milk.
    for i in range(5):
        if assignments["Sport"][i] == "Polo" and assignments["Drink"][i] not in ["", "Milk"]:
            errors[(i, "Drink")] = "Polo player must drink Milk."

    # Rule 13: The German likes soccer.
    for i in range(5):
        if assignments["Nationality"][i] == "German" and assignments["Sport"][i] not in ["", "Soccer"]:
            errors[(i, "Sport")] = "German must like Soccer."

    # Rule 14: The American lives next to the White house.
    for i in range(5):
        if assignments["Nationality"][i] == "American":
            if not (
                (i > 0 and assignments["Color"][i - 1] in ["", "White"])
                or (i < 4 and assignments["Color"][i + 1] in ["", "White"])
            ):
                errors[(i, "Nationality")] = "American must live next to White house."

    return errors


def highlight_errors(val, row, col, errors):
    """Return background color if (row, col) violates a constraint."""
    return "background-color: #ff9999" if (row, col) in errors else ""


# ---------------- UI ---------------- #
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


col1, col2 = st.columns(2)

with col1:
    if st.button("Check Constraints"):
        df = pd.DataFrame(st.session_state.assignments, index=houses)
        st.subheader("📋 Your Current Input")

        errors = check_constraints(st.session_state.assignments)

        # Apply styling
        styled_df = df.style.apply(
            lambda row: [
                highlight_errors(row[col], row.name, col, errors)
                for col in df.columns
            ],
            axis=1
        )

        st.dataframe(styled_df, use_container_width=True)

        if errors:
            st.error("⚠️ Some rules are broken:")
            for msg in errors.values():
                st.write("- " + msg)
        else:
            st.success("✅ All constraints satisfied so far!")