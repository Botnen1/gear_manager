import streamlit as st
from utils.db_utils import get_session
from utils.db_setup import Gear

def app():
    st.title("🎒 Pack Weight Calculator")

    session = get_session()

    st.subheader("Select gear to pack (excludes and shoes):")

    # Fetch only owned gear that is NOT clothing or shoes
    gear_items = session.query(Gear).filter(
        Gear.status == "owned",
        Gear.category.notin_(["Shoes"])
    ).all()

    total_weight = 0.0
    selected_items = []

    if gear_items:
        col1, col2, col3 = st.columns([1, 1, 1])  # Two columns for gear, one for total weight

        # Split gear into two lists for two columns
        mid_index = len(gear_items) // 2
        gear_list_1 = gear_items[:mid_index]
        gear_list_2 = gear_items[mid_index:]

        # Left Column: First Half of Gear
        with col1:
            for gear in gear_list_1:
                selected = st.checkbox(f"{gear.name} ({gear.weight_grams} grams)", key=f"gear_{gear.id}")
                if selected:
                    total_weight += gear.weight_grams
                    selected_items.append(gear.name)

        # Middle Column: Second Half of Gear
        with col2:
            for gear in gear_list_2:
                selected = st.checkbox(f"{gear.name} ({gear.weight_grams} grams)", key=f"gear_{gear.id}")
                if selected:
                    total_weight += gear.weight_grams
                    selected_items.append(gear.name)

        # Right Column: Total Pack Weight & Selected Items
        with col3:
            st.subheader("🎒 Total Pack Weight:")
            oz = total_weight * 0.035274
            lbs = total_weight * 0.00220462

            st.markdown(f"""
            - **{total_weight:.2f} grams**
            - **{total_weight / 1000:.2f} kg**
            - **{oz:.2f} oz**
            - **{lbs:.2f} lbs**
            """)

            if selected_items:
                st.markdown("### Items Selected:")
                for item in selected_items:
                    st.write(f"- {item}")
            else:
                st.info("No gear selected yet.")

    else:
        st.info("No suitable gear found in inventory.")
