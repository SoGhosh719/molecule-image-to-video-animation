import os
import streamlit as st
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from tempfile import mkdtemp

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

    # Show progress bar
    progress_bar = st.progress(0)
    
    # Save as video
    clip.write_videofile(video_path, codec="libx264", progress_bar=True)
    progress_bar.progress(50)

    # Save as GIF
    clip.write_gif(gif_path, fps=fps)
    progress_bar.progress(100)
    
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
