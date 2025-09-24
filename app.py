import streamlit as st
import pandas as pd

# Categories
colors = ["Red", "Blue", "Green", "Yellow", "White"]
nationalities = ["American", "Indian", "Mexican", "Pakistani", "German"]
pets = ["Raccoon", "Monkey", "Parrot", "Dog", "Fish"]
drinks = ["Water", "Tea", "Horchata", "Milk", "Beer"]
sports = ["Jogging", "Cricket", "Polo", "Soccer", "Swimming"]

houses = [f"House {i}" for i in range(1, 6)]

# Session state
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

# ---- Horizontal layout: 5 houses side-by-side ----
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

# ---- Full 14-rule constraint checker ----
def check_constraints(a):
    errors = {}

    # 1. Indian lives in the blue house.
    for i in range(5):
        if a["Nationality"][i] == "Indian" and a["Color"][i] not in ["", "Blue"]:
            errors[(i, "Color")] = "Indian must live in Blue house."

    # 2. Pakistani owns the parrot.
    for i in range(5):
        if a["Nationality"][i] == "Pakistani" and a["Pet"][i] not in ["", "Parrot"]:
            errors[(i, "Pet")] = "Pakistani must own the Parrot."

    # 3. Beer is drunk in the green house.
    for i in range(5):
        if a["Color"][i] == "Green" and a["Drink"][i] not in ["", "Beer"]:
            errors[(i, "Drink")] = "Beer must be drunk in Green house."

    # 4. Mexican drinks Horchata.
    for i in range(5):
        if a["Nationality"][i] == "Mexican" and a["Drink"][i] not in ["", "Horchata"]:
            errors[(i, "Drink")] = "Mexican must drink Horchata."

    # 5. Green is immediately to the right of Yellow (Yellow at i, Green at i+1).
    for i in range(4):
        if a["Color"][i] == "Yellow" and a["Color"][i + 1] not in ["", "Green"]:
            errors[(i + 1, "Color")] = "Green must be immediately right of Yellow."
    # If Green fixed at 0, it's impossible (no Yellow at -1). We only flag when Yellow set.

    # 6. Cricket player owns a monkey.
    for i in range(5):
        if a["Sport"][i] == "Cricket" and a["Pet"][i] not in ["", "Monkey"]:
            errors[(i, "Pet")] = "Cricket player must own Monkey."

    # 7. Jogging is in the red house.
    for i in range(5):
        if a["Color"][i] == "Red" and a["Sport"][i] not in ["", "Jogging"]:
            errors[(i, "Sport")] = "Jogging must be in Red house."

    # 8. Tea is drunk in the third house (index 2).
    if a["Drink"][2] not in ["", "Tea"]:
        errors[(2, "Drink")] = "Tea must be drunk in House 3."

    # 9. American lives in the first house (index 0).
    if a["Nationality"][0] not in ["", "American"]:
        errors[(0, "Nationality")] = "American must live in House 1."

    # 10. Raccoon owner lives next to Swimmer.
    for i in range(5):
        if a["Pet"][i] == "Raccoon":
            left_ok  = (i > 0 and a["Sport"][i - 1] in ["", "Swimming"])
            right_ok = (i < 4 and a["Sport"][i + 1] in ["", "Swimming"])
            if not (left_ok or right_ok):
                errors[(i, "Pet")] = "Raccoon owner must live next to Swimmer."

    # 11. Jogger lives next to the owner of a Dog.
    for i in range(5):
        if a["Sport"][i] == "Jogging":
            left_ok  = (i > 0 and a["Pet"][i - 1] in ["", "Dog"])
            right_ok = (i < 4 and a["Pet"][i + 1] in ["", "Dog"])
            if not (left_ok or right_ok):
                errors[(i, "Sport")] = "Jogger must live next to Dog owner."

    # 12. Polo player drinks Milk.
    for i in range(5):
        if a["Sport"][i] == "Polo" and a["Drink"][i] not in ["", "Milk"]:
            errors[(i, "Drink")] = "Polo player must drink Milk."

    # 13. German likes Soccer.
    for i in range(5):
        if a["Nationality"][i] == "German" and a["Sport"][i] not in ["", "Soccer"]:
            errors[(i, "Sport")] = "German must like Soccer."

    # 14. American lives next to the White house.
    for i in range(5):
        if a["Nationality"][i] == "American":
            left_ok  = (i > 0 and a["Color"][i - 1] in ["", "White"])
            right_ok = (i < 4 and a["Color"][i + 1] in ["", "White"])
            if not (left_ok or right_ok):
                errors[(i, "Nationality")] = "American must live next to White house."

    return errors

# ---- Check button & table with highlighting ----
if st.button("Check Constraints"):
    df = pd.DataFrame(st.session_state.assignments, index=houses)

    errors = check_constraints(st.session_state.assignments)

    # Map row label (e.g., "House 1") -> numeric index (0..4) to match our error keys
    def style_row(row: pd.Series):
        row_idx = houses.index(row.name)
        return [
            "background-color: #ffcccc" if (row_idx, col) in errors else ""
            for col in df.columns
        ]

    styled = df.style.apply(style_row, axis=1)
    st.subheader("📋 Your Current Input")
    st.dataframe(styled, use_container_width=True)

    if errors:
        st.error("⚠️ Some rules are broken:")
        for msg in errors.values():
            st.write(f"- {msg}")
    else:
        st.success("✅ All constraints satisfied so far!")