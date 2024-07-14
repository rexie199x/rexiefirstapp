import streamlit as st
import pandas as pd
from PIL import Image
import json
import os

# Custom CSS for dark and light themes
dark_theme_css = """
<style>
body {
    background-color: #2E2E2E;
    color: white;
}
.sidebar .sidebar-content {
    background-color: #3E3E3E;
}
a.link-button {
    color: white;
    text-decoration: none;
    cursor: pointer;
}
a.link-button:hover {
    text-decoration: underline;
}
</style>
"""

light_theme_css = """
<style>
body {
    background-color: #FFFFFF;
    color: black;
}
.sidebar .sidebar-content {
    background-color: #F8F9FA;
}
a.link-button {
    color: black;
    text-decoration: none;
    cursor: pointer;
}
a.link-button:hover {
    text-decoration: underline;
}
</style>
"""


# File path for storing the processes data
data_file = "processes_data.json"

# Function to load processes data from the JSON file
def load_processes_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return {
        "Discord": [
            {"title": "Process 1", "content": "Content for process 1"},
            {"title": "Process 2", "content": "Content for process 2"},
            {"title": "Process 3", "content": "Content for process 3"},
        ],
        "Pre-Onboarding": [
            {"title": "Process 1", "content": "Content for process 1"},
            {"title": "Process 2", "content": "Content for process 2"},
        ],
        "Program Proper": [
            {"title": "Process 1", "content": "Content for process 1"},
        ],
        "Post-Program": [
            {"title": "Process 1", "content": "Content for process 1"},
            {"title": "Process 2", "content": "Content for process 2"},
        ]
    }

# Function to save processes data to the JSON file
def save_processes_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

# Initialize the processes data in session state
if 'processes_data' not in st.session_state:
    st.session_state.processes_data = load_processes_data()

# Initialize new process fields in session state
if 'new_process_title' not in st.session_state:
    st.session_state.new_process_title = ""
if 'new_process_content' not in st.session_state:
    st.session_state.new_process_content = ""

# Function to display the home page
def show_home():

    # Display the saved image if exists
    try:
        image = Image.open("company_logo.png")
        st.image(image, caption="Company Logo", use_column_width=True)
    except FileNotFoundError:
        st.write("No logo uploaded yet. Please upload a logo.")

    # Discreet button to reveal upload section
    if st.button("Upload New Logo"):
        with st.expander("Upload Company Logo"):
            uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Company Logo", use_column_width=True)
                # Save the image
                with open("company_logo.png", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("Logo uploaded successfully!")

    st.write("This manual outlines the key processes and timelines for the successful execution of our program. ")

# Function to display processes for each section
def show_processes(section):
    st.title(f"{section} Processes")
    st.write(f"List of processes for {section} will be shown here.")
    
    processes = st.session_state.processes_data.get(section, [])

    # Search bar
    search_query = st.text_input("Search for an article:")
    if search_query:
        processes = [p for p in processes if search_query.lower() in p['title'].lower()]

    # Display processes
    for i, process in enumerate(processes):
        expander = st.expander(f"{process['title']}", expanded=False)
        with expander:
            st.write(process['content'])

            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("Edit", key=f"edit_{section}_{i}"):
                    st.session_state[f"edit_mode_{section}_{i}"] = True
            with col2:
                if st.button("Delete", key=f"delete_{section}_{i}"):
                    st.session_state[f"confirm_delete_{section}_{i}"] = True

            if st.session_state.get(f"edit_mode_{section}_{i}", False):
                new_title = st.text_input(f"Edit title for {process['title']}", process['title'], key=f"title_{section}_{i}")
                new_content = st.text_area(f"Edit content for {process['title']}", process['content'], key=f"content_{section}_{i}")
                if st.button(f"Save {process['title']}", key=f"save_{section}_{i}"):
                    st.session_state.processes_data[section][i]['title'] = new_title
                    st.session_state.processes_data[section][i]['content'] = new_content
                    st.session_state[f"edit_mode_{section}_{i}"] = False
                    save_processes_data(st.session_state.processes_data)  # Save changes
                    st.success(f"Saved changes for {process['title']}")
                    st.experimental_rerun()

            if st.session_state.get(f"confirm_delete_{section}_{i}", False):
                st.warning(f"Are you sure you want to delete {process['title']}?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Yes, delete {process['title']}", key=f"confirm_yes_{section}_{i}"):
                        processes.pop(i)
                        st.session_state.processes_data[section] = processes
                        st.session_state[f"confirm_delete_{section}_{i}"] = False
                        save_processes_data(st.session_state.processes_data)  # Save changes
                        st.success(f"Deleted {process['title']}")
                        st.experimental_rerun()
                with col2:
                    if st.button("No, cancel", key=f"confirm_no_{section}_{i}"):
                        st.session_state[f"confirm_delete_{section}_{i}"] = False

    # Add new process
    st.write("### Add New Process")
    st.session_state.new_process_title = st.text_input("New Process Title", key=f"new_title_{section}")
    st.session_state.new_process_content = st.text_area("New Process Content", key=f"new_content_{section}")
    if st.button("Add Process", key=f"add_{section}"):
        if st.session_state.new_process_title and st.session_state.new_process_content:
            processes.append({"title": st.session_state.new_process_title, "content": st.session_state.new_process_content})
            st.session_state.processes_data[section] = processes
            # Clear the input fields after adding the process
            st.session_state.new_process_title = ""
            st.session_state.new_process_content = ""
            save_processes_data(st.session_state.processes_data)  # Save changes
            st.success("New process added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please provide both title and content for the new process.")

# Main function to run the app
def main():
    st.sidebar.title("Menu")
    
    # Theme selection
    theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])
    apply_theme(theme)
    
    menu_options = ["Home", "Discord", "Pre-Program", "Program Proper", "Post-Program"]
    choice = st.sidebar.radio("Go to", menu_options)

    if choice == "Home":
        show_home()
    else:
        show_processes(choice)

if __name__ == "__main__":
    main()
