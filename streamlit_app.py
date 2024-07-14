import streamlit as st
import pandas as pd

# Function to display the home page
def show_home():
    st.title("Welcome to the Knowledge Base")
    st.write("Select a section from the sidebar to get started.")

# Function to display processes for each section
def show_processes(section):
    st.title(f"{section} Processes")
    st.write(f"List of processes for {section} will be shown here.")
    
    # Example list of processes
    processes = [
        {"title": "Process 1", "content": "Content for process 1"},
        {"title": "Process 2", "content": "Content for process 2"},
        {"title": "Process 3", "content": "Content for process 3"},
    ]

    # Search bar
    search_query = st.text_input("Search for an article:")
    if search_query:
        processes = [p for p in processes if search_query.lower() in p['title'].lower()]

    # Display processes
    for process in processes:
        if st.checkbox(f"Edit {process['title']}"):
            new_content = st.text_area(f"Edit content for {process['title']}", process['content'])
            if st.button(f"Save {process['title']}"):
                process['content'] = new_content
                st.success(f"Saved content for {process['title']}")
        else:
            st.write(f"**{process['title']}**")
            st.write(process['content'])

# Main function to run the app
def main():
    st.sidebar.title("Menu")
    menu_options = ["Home", "Discord", "Pre-Onboarding", "Program Proper", "Post-Program"]
    choice = st.sidebar.radio("Go to", menu_options)

    if choice == "Home":
        show_home()
    else:
        show_processes(choice)

if __name__ == "__main__":
    main()
