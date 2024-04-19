import streamlit as st
import random
import time
import glob
import os

st.title('Grouping Knowledge Test')

# Initialize the session state variables if not already present
if 'pic_list' not in st.session_state:
    st.session_state['pic_list'] = []
if 'directory' not in st.session_state:
    st.session_state["directory"] = None
if 'new_question' not in st.session_state:
    st.session_state['new_question'] = True  # Flag to trigger loading new images

def load_images():
    directory = f"score_pic/simple44/set_{random.randint(1, 3)}"
    file_names = os.listdir(directory)
    png_files = [file for file in file_names if file.endswith(".png")]
    pic_list = [os.path.basename(file) for file in png_files]
    random.shuffle(pic_list)
    print(pic_list)
    return pic_list, directory

def display_images(pic_list, directory):
    for idx, pic in enumerate(pic_list):
        col1, col2 = st.columns([3, 1])  # Adjust column ratios as needed
        with col1:
            image_path = os.path.join(directory, pic)
            st.image(image_path, use_column_width=True)
        with col2:
            if st.button('Choose this', key=pic):
                if pic == 'cropped_score_correct.png':
                    st.success("Correct!")
                    st.session_state['new_question'] = True
                else:
                    st.error("Incorrect! Try again.")
                

if st.session_state['new_question']:
    st.session_state['pic_list'], st.session_state["directory"] = load_images()
    st.session_state['new_question'] = False  # Reset the flag after loading images

if st.session_state["directory"] is not None :
    display_images(st.session_state['pic_list'], st.session_state["directory"])
else:
    st.warning("Click 'New Question' to load images.")

if st.button('New Question') and st.session_state['new_question']==True:
    st.session_state['new_question'] = True  # Set the flag to load new images