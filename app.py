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

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Check Constraints"):
        st.info("Constraint checking will be added here.")

with col2:
    if st.button("Solve Puzzle"):
        st.success("Solver integration will be added here.")