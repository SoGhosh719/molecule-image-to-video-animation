import os
import streamlit as st
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from tempfile import mkdtemp
import time

# 🎨 Streamlit Page Config
st.set_page_config(page_title="Molecule Animation Creator", page_icon="🎥")

# 📌 Sidebar: User Settings
st.sidebar.header("⚙️ Settings")
fps = st.sidebar.slider("🎞️ Frames Per Second (FPS)", min_value=1, max_value=30, value=12)

# 📌 Main Title & Welcome Message
st.title("🎥 Molecule Image to Video & GIF Converter")
st.markdown(
    """
    Welcome to the **Molecule Animation Creator**!  
    Convert multiple **molecule images** into a **smooth video or GIF** in just a few clicks.  
    Follow the instructions below to get started! 🚀
    """
)

# 📌 Instructions Section
st.subheader("📌 How to Use:")
st.markdown(
    """
    1️⃣ **Upload your images**: Select multiple **PNG, JPG, or JPEG** files.  
    2️⃣ **Ensure correct order**: Images are processed alphabetically. Rename them (`1.png`, `2.png`, etc.) if needed.  
    3️⃣ **Set FPS (Frames Per Second)**: Adjust in the sidebar (higher FPS = faster animation).  
    4️⃣ **Click 'Create Video & GIF'**: The app will generate both a video and a GIF.  
    5️⃣ **Download your files**: Use the buttons below to save your animation.  
    """
)

# 📂 File Upload
uploaded_files = st.file_uploader("📂 Upload Images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# Function to save uploaded images
def save_uploaded_files(uploaded_files):
    folder_path = mkdtemp()
    for uploaded_file in uploaded_files:
        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
    return folder_path

# Function to create both video & GIF using MoviePy
def create_video_and_gif(folder_path, video_path="output_video.mp4", gif_path="output_animation.gif", fps=12):
    images = sorted(
        [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith((".png", ".jpg", ".jpeg"))]
    )

    if not images:
        st.error("⚠️ No valid images found. Please upload PNG, JPG, or JPEG files.")
        return None, None

    clip = ImageSequenceClip(images, fps=fps)

    # Create a Streamlit progress bar
    progress_bar = st.progress(0)
    progress_text = st.empty()

    # Save as video
    st.info("🎬 Creating Video... This may take a few seconds.")
    clip.write_videofile(video_path, codec="libx264")

    # Manually update progress
    for percent_complete in range(0, 101, 20):
        progress_text.text(f"Processing Video... {percent_complete}%")
        progress_bar.progress(percent_complete)
        time.sleep(0.5)

    # Save as GIF
    st.info("🖼️ Creating GIF... Please wait.")
    clip.write_gif(gif_path, fps=fps)

    # Update progress to 100%
    progress_bar.progress(100)
    progress_text.text("✅ Video & GIF Creation Complete!")

    return video_path, gif_path

# 🎬 Video & GIF Creation
if st.button("🎬 Create Video & GIF"):
    if uploaded_files:
        st.info("⏳ Processing images... This may take a few seconds.")
        folder_path = save_uploaded_files(uploaded_files)
        video_path, gif_path = create_video_and_gif(folder_path, fps=fps)

        if video_path and gif_path:
            st.success("✅ Video & GIF Created Successfully! 🎉")

            # Download Video
            with open(video_path, "rb") as f:
                st.download_button("⬇️ Download Video", f, file_name="molecule_animation.mp4", mime="video/mp4")

            # Download GIF
            with open(gif_path, "rb") as f:
                st.download_button("🖼️ Download GIF", f, file_name="molecule_animation.gif", mime="image/gif")
    else:
        st.warning("⚠️ Please upload images first.")

# 📌 Sidebar Chatbot (FAQ)
st.sidebar.subheader("💬 Ask the Chatbot")

faq_responses = {
    "What is this app for?": "This app converts a series of molecule images into a smooth video or GIF.",
    "What file types are supported?": "You can upload PNG, JPG, and JPEG files.",
    "How do I ensure correct image order?": "Rename your files numerically (e.g., 1.png, 2.png) to ensure the correct order.",
    "What does FPS mean?": "FPS (Frames Per Second) controls the speed of the animation. A higher FPS means a faster video.",
    "Can I download both video and GIF?": "Yes! After processing, you can download both formats."
}

user_query = st.sidebar.text_input("Ask a question:")
if user_query:
    response = faq_responses.get(user_query, "I'm not sure about that. Try asking something else!")
    st.sidebar.write(f"🤖 Chatbot: {response}")
