import streamlit as st
from utils.db_utils import get_session
from utils.db_setup import Gear


def app():
    st.title("🎒 Pack Weight Calculator")

    session = get_session()

    st.subheader("Select gear to pack (excludes clothing and shoes):")

    gear_items = session.query(Gear).filter(
        Gear.status=="owned",
        Gear.category.notin_(["Clothing", "Shoes"])
    ).all()

    total_weight = 0.0
    selected_items = []
    

    if gear_items:
        for gear in gear_items:
            selected = st.checkbox(f"{gear.name} ({gear.weight_grams} grams)", key=gear.id)
            if selected:
                total_weight += gear.weight_grams
                selected_items.append(gear.name)

        st.markdown("---")
        st.subheader("🎒 Total Pack Weight:")
        oz = total_weight * 0.035274
        lbs = total_weight * 2.20462
        
        st.write(f"**{total_weight:.2f} grams** ({total_weight/1000:.2f} kg) **{oz:.2f} oz** **{lbs/1000:.2f} lbs**")

        if selected_items:
            st.markdown("### Items selected:")
            for item in selected_items:
                st.write(f"- {item}")
        else:
            st.info("No gear selected yet.")
    else:
        st.info("No suitable gear found in inventory.")
