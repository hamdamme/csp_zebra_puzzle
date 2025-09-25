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

# ---- Horizontal layout ----
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


# ---- Constraint Checker (all 14 rules) ----
def check_constraints(a):
    # return True if all rules satisfied, False otherwise

    # 1. Indian lives in the blue house.
    for i in range(5):
        if a["Nationality"][i] == "Indian" and a["Color"][i] != "Blue":
            return False

    # 2. Pakistani owns the parrot.
    for i in range(5):
        if a["Nationality"][i] == "Pakistani" and a["Pet"][i] != "Parrot":
            return False

    # 3. Beer is drunk in the green house.
    for i in range(5):
        if a["Color"][i] == "Green" and a["Drink"][i] != "Beer":
            return False

    # 4. Mexican drinks Horchata.
    for i in range(5):
        if a["Nationality"][i] == "Mexican" and a["Drink"][i] != "Horchata":
            return False

    # 5. Green is immediately to the right of Yellow.
    for i in range(4):
        if a["Color"][i] == "Yellow" and a["Color"][i + 1] != "Green":
            return False

    # 6. Cricket player owns a monkey.
    for i in range(5):
        if a["Sport"][i] == "Cricket" and a["Pet"][i] != "Monkey":
            return False

    # 7. Jogging is in the red house.
    for i in range(5):
        if a["Color"][i] == "Red" and a["Sport"][i] != "Jogging":
            return False

    # 8. Tea is drunk in the third house (index 2).
    if a["Drink"][2] != "Tea":
        return False

    # 9. American lives in the first house (index 0).
    if a["Nationality"][0] != "American":
        return False

    # 10. Raccoon owner lives next to Swimmer.
    for i in range(5):
        if a["Pet"][i] == "Raccoon":
            if not (
                (i > 0 and a["Sport"][i - 1] == "Swimming")
                or (i < 4 and a["Sport"][i + 1] == "Swimming")
            ):
                return False

    # 11. Jogger lives next to Dog owner.
    for i in range(5):
        if a["Sport"][i] == "Jogging":
            if not (
                (i > 0 and a["Pet"][i - 1] == "Dog")
                or (i < 4 and a["Pet"][i + 1] == "Dog")
            ):
                return False

    # 12. Polo player drinks Milk.
    for i in range(5):
        if a["Sport"][i] == "Polo" and a["Drink"][i] != "Milk":
            return False

    # 13. German likes Soccer.
    for i in range(5):
        if a["Nationality"][i] == "German" and a["Sport"][i] != "Soccer":
            return False

    # 14. American lives next to White house.
    for i in range(5):
        if a["Nationality"][i] == "American":
            if not (
                (i > 0 and a["Color"][i - 1] == "White")
                or (i < 4 and a["Color"][i + 1] == "White")
            ):
                return False

    return True


# ---- Button ----
if st.button("Check Constraints"):
    df = pd.DataFrame(st.session_state.assignments, index=houses)
    st.subheader("📋 Your Current Input")
    st.dataframe(df, use_container_width=True)

    if check_constraints(st.session_state.assignments):
        st.success("🎉 Puzzle Solved! ✅")
    else:
        st.error("❌ Incorrect – some rules are not satisfied.")