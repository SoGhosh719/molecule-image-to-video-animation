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
    # General Questions
    "What does this app do?": "This app converts a series of molecule images into a smooth video or GIF.",
    "Who can use this app?": "Anyone! Researchers, students, and professionals working with molecule animations.",
    "Do I need to install anything to use this app?": "No, the app runs entirely on Streamlit Cloud.",
    "Is this app free to use?": "Yes! It is completely free to use.",
    "Can I use this app on mobile devices?": "Yes, but for better experience, use it on a desktop or tablet.",

    # File Upload Questions
    "What file types are supported for uploading?": "PNG, JPG, and JPEG formats are supported.",
    "How many images can I upload at once?": "There is no strict limit, but too many images may slow down processing.",
    "What should I do if my images are not uploading?": "Check your internet connection and try re-uploading.",
    "Can I upload images in any order?": "The app sorts images alphabetically, so rename them (1.png, 2.png, etc.).",
    "Do I need to rename my images before uploading?": "It's recommended to rename them in order for a proper sequence.",

    # Video & GIF Creation Questions
    "How does this app convert images into a video?": "It stitches your images together using MoviePy.",
    "How long does it take to create a video?": "Processing time depends on the number of images and FPS settings.",
    "What does FPS mean?": "Frames Per Second (FPS) controls animation speed. Higher FPS = faster animation.",
    "What FPS should I choose for a smooth animation?": "12-24 FPS is ideal for smooth animations.",
    "What happens if I set a very high FPS?": "The animation will be too fast, making it hard to see details.",
    "What is the difference between a video and a GIF?": "Videos are MP4 format with better quality, while GIFs are more compressed.",
    "Can I create both a video and a GIF at the same time?": "Yes, the app generates both simultaneously.",

    # Download & Storage Questions
    "How do I download my video or GIF?": "Click the download button after processing is complete.",
    "Where is my downloaded file saved?": "It is saved in your default 'Downloads' folder.",
    "Can I share my video or GIF directly from the app?": "Not directly, but you can download and share manually.",
    "Is there a limit to how many videos I can create?": "No, you can create as many as you want.",
    "Will my uploaded images be stored on the server?": "No, uploaded images are processed temporarily and not stored.",

    # Troubleshooting Questions
    "Why is my video not generating?": "Check if you uploaded images and selected FPS properly.",
    "Why does my video appear blurry?": "Use high-quality images for the best results.",
    "Why is the animation too fast or too slow?": "Adjust the FPS settings in the sidebar.",
}

user_query = st.sidebar.text_input("Ask a question:")
if user_query:
    response = faq_responses.get(user_query, "🤖 I'm not sure about that. Try asking something else!")
    st.sidebar.write(f"🤖 Chatbot: {response}")
