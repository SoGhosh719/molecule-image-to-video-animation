# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uzI6uVp8fhfQQPGuNx2Y-fUepgv7oW0d
"""

!pip install streamlit opencv-python-headless pyngrok

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import os
# import cv2
# import shutil
# import streamlit as st
# from tempfile import mkdtemp
# 
# def save_uploaded_files(uploaded_files):
#     folder_path = mkdtemp()
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(folder_path, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.read())
#     return folder_path
# 
# def create_video_from_images(folder_path, output_path="output_video.mp4", fps=12):
#     images = sorted([img for img in os.listdir(folder_path) if img.endswith((".png", ".jpg", ".jpeg"))])
#     if not images:
#         st.error("No valid images found.")
#         return None
# 
#     first_image_path = os.path.join(folder_path, images[0])
#     frame = cv2.imread(first_image_path)
#     height, width, _ = frame.shape
# 
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
# 
#     for image_name in images:
#         image_path = os.path.join(folder_path, image_name)
#         frame = cv2.imread(image_path)
#         video.write(frame)
# 
#     video.release()
#     return output_path
# 
# st.title("Molecule Animation Video Creator")
# uploaded_files = st.file_uploader("Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
# 
# if st.button("Create Video"):
#     if uploaded_files:
#         st.info("Processing images...")
#         folder_path = save_uploaded_files(uploaded_files)
#         video_path = create_video_from_images(folder_path)
# 
#         if video_path:
#             st.success("Video created successfully!")
#             with open(video_path, "rb") as f:
#                 st.download_button("Download Video", f, file_name="molecule_animation.mp4", mime="video/mp4")
#     else:
#         st.warning("Please upload images first.")
#