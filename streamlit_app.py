import streamlit as st
import pandas as pd
from PIL import Image
import io

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

# Initialize the processes data in session state
if 'processes_data' not in st.session_state:
    st.session_state.processes_data = {
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

    st.write("This manual outlines the key processes and timelines for the successful execution of our program. Our goal is to deliver high-quality education and support to our students while ensuring the financial sustainability of the program.")

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

            edit_link = f'<a href="#" id="edit_{section}_{i}">Edit</a>'
            delete_link = f'<a href="#" id="delete_{section}_{i}">Delete</a>'
            st.markdown(f"{edit_link} | {delete_link}", unsafe_allow_html=True)

            if f"edit_{section}_{i}" in st.session_state and st.session_state[f"edit_{section}_{i}"]:
                new_content = st.text_area(f"Edit content for {process['title']}", process['content'], key=f"content_{section}_{i}")
                if st.button(f"Save {process['title']}", key=f"save_{section}_{i}"):
                    st.session_state.processes_data[section][i]['content'] = new_content
                    st.success(f"Saved content for {process['title']}")
                    st.experimental_rerun()

            if f"delete_{section}_{i}" in st.session_state and st.session_state[f"delete_{section}_{i}"]:
                processes.pop(i)
                st.session_state.processes_data[section] = processes
                st.success(f"Deleted {process['title']}")
                st.experimental_rerun()

    # Add new process
    st.write("### Add New Process")
    new_process_title = st.text_input("New Process Title", key=f"new_title_{section}")
    new_process_content = st.text_area("New Process Content", key=f"new_content_{section}")
    if st.button("Add Process", key=f"add_{section}"):
        if new_process_title and new_process_content:
            processes.append({"title": new_process_title, "content": new_process_content})
            st.session_state.processes_data[section] = processes
            st.success("New process added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please provide both title and content for the new process.")

# Function to handle JavaScript click events
def handle_js_click_events():
    st.write('<script>document.querySelectorAll("a").forEach(a => a.onclick = (e) => {e.preventDefault(); window.parent.postMessage(a.id, "*");})</script>', unsafe_allow_html=True)

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

    handle_js_click_events()

    # JavaScript message handling
    js_msg = st.experimental_get_query_params().get("js_msg", [""])[0]
    if js_msg:
        st.session_state[js_msg] = True
        st.experimental_rerun()

if __name__ == "__main__":
    main()
