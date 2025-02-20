import streamlit as st
import pandas as pd
from PIL import Image
import psycopg2
import os

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="processes_db",
        user="postgres",
        password="LOctopus",
        host="localhost"
    )

# Function to load processes data from the database
def load_processes_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT section, title, content FROM processes")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = {}
    for row in rows:
        section, title, content = row
        if section not in data:
            data[section] = []
        data[section].append({"title": title, "content": content})
    return data

# Function to save a new process to the database
def save_new_process(section, title, content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO processes (section, title, content) VALUES (%s, %s, %s)", (section, title, content))
    conn.commit()
    cur.close()
    conn.close()

# Function to update an existing process in the database
def update_process(section, old_title, new_title, new_content):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE processes SET title = %s, content = %s WHERE section = %s AND title = %s",
                (new_title, new_content, section, old_title))
    conn.commit()
    cur.close()
    conn.close()

# Function to delete a process from the database
def delete_process(section, title):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM processes WHERE section = %s AND title = %s", (section, title))
    conn.commit()
    cur.close()
    conn.close()

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

    st.write("This manual outlines the key processes and timelines for the successful execution of our program.")

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
                    update_process(section, process['title'], new_title, new_content)
                    st.session_state.processes_data = load_processes_data()
                    st.session_state[f"edit_mode_{section}_{i}"] = False
                    st.success(f"Saved changes for {process['title']}")
                    st.experimental_rerun()

            if st.session_state.get(f"confirm_delete_{section}_{i}", False):
                st.warning(f"Are you sure you want to delete {process['title']}?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Yes, delete {process['title']}", key=f"confirm_yes_{section}_{i}"):
                        delete_process(section, process['title'])
                        st.session_state.processes_data = load_processes_data()
                        st.session_state[f"confirm_delete_{section}_{i}"] = False
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
            save_new_process(section, st.session_state.new_process_title, st.session_state.new_process_content)
            st.session_state.processes_data = load_processes_data()
            # Clear the input fields after adding the process
            st.session_state.new_process_title = ""
            st.session_state.new_process_content = ""
            st.success("New process added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please provide both title and content for the new process.")

# Main function to run the app
def main():
    st.sidebar.title("Menu")
    
    menu_options = ["Home", "Discord", "Pre-Program", "Program Proper", "Post-Program", "Timelines"]
    choice = st.sidebar.radio("Go to", menu_options)

    if choice == "Home":
        show_home()
    else:
        show_processes(choice)

if __name__ == "__main__":
    main()
