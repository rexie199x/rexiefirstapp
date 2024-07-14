import streamlit as st
import pandas as pd

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
</style>
"""

# Function to apply the selected theme
def apply_theme(theme):
    if theme == "Dark":
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(light_theme_css, unsafe_allow_html=True)

# Example list of processes
processes_data = {
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

# Function to display the home page
def show_home():
    st.title("The Lonely Octopus Manual")
    st.write("This manual outlines the key processes and timelines for the successful execution of our program. Our goal is to deliver high-quality education and support to our students while ensuring the financial sustainability of the program.")

# Function to display processes for each section
def show_processes(section):
    st.title(f"{section} Processes")
    st.write(f"List of processes for {section} will be shown here.")
    
    processes = processes_data.get(section, [])

    # Search bar
    search_query = st.text_input("Search for an article:")
    if search_query:
        processes = [p for p in processes if search_query.lower() in p['title'].lower()]

    # Display processes
    for i, process in enumerate(processes):
        if st.checkbox(f"Edit {process['title']}", key=f"edit_{section}_{i}"):
            new_content = st.text_area(f"Edit content for {process['title']}", process['content'], key=f"content_{section}_{i}")
            if st.button(f"Save {process['title']}", key=f"save_{section}_{i}"):
                processes_data[section][i]['content'] = new_content
                st.success(f"Saved content for {process['title']}")
        else:
            st.write(f"**{process['title']}**")
            st.write(process['content'])

    # Add new process
    st.write("### Add New Process")
    new_process_title = st.text_input("New Process Title", key=f"new_title_{section}")
    new_process_content = st.text_area("New Process Content", key=f"new_content_{section}")
    if st.button("Add Process", key=f"add_{section}"):
        if new_process_title and new_process_content:
            processes_data[section].append({"title": new_process_title, "content": new_process_content})
            st.success("New process added successfully!")
        else:
            st.error("Please provide both title and content for the new process.")

# Main function to run the app
def main():
    st.sidebar.title("Menu")
    
    # Theme selection
    theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])
    apply_theme(theme)
    
    menu_options = ["Home", "Discord", "Pre-Onboarding", "Program Proper", "Post-Program"]
    choice = st.sidebar.radio("Go to", menu_options)

    if choice == "Home":
        show_home()
    else:
        show_processes(choice)

if __name__ == "__main__":
    main()
