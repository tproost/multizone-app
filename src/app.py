import streamlit as st
from components.multizone_grid import create_multizone_grid


def main():
    st.title("MultiZone")
    create_multizone_grid()


if __name__ == "__main__":
    main()
