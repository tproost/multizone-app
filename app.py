import streamlit as st
from src.components.multizone_grid import create_multizone_grid

# Configure page
st.set_page_config(
    page_title="MultiZone",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Main app
def main():
    st.title("MultiZone")
    create_multizone_grid()


if __name__ == "__main__":
    main()
