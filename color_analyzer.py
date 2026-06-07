import streamlit
from PIL import Image
import numpy
from sklearn.cluster import KMeans

# 1. FRONTEND CONFIGURATION
streamlit.set_page_config(
    page_title="Color Palette Analyzer", layout="centered")
streamlit.title("🎨 AI-Powered Color Palette Analyzer")
streamlit.write("Upload an image, and let's extract the dominant colors!")

# File uploader component
uploaded_file = streamlit.file_uploader(
    "Choose an image", type=["jpg", "png", "jpeg"])

# 2. BACKEND: IMAGE PROCESSING & ANALYSIS
if uploaded_file is not None:

    # Display the uploaded image
    image = Image.open(uploaded_file)
    streamlit.image(image, caption="Uploaded Image", width="stretch")

    # Trigger analysis on button click
    if streamlit.button("Analyze Colors"):

        with streamlit.spinner("Scanning pixels and clustering colors..."):

            # Resize image to optimize processing speed (150x150 pixels)
            img_resized = image.convert('RGB').resize((150, 150))

            # Convert image to mathematical array
            np_img = numpy.array(img_resized)
            pixels = np_img.reshape(-1, 3)

            # Apply K-Means Machine Learning algorithm for 5 dominant colors
            kmeans = KMeans(n_clusters=5, random_state=42)
            kmeans.fit(pixels)

            # Convert color float values to integers and store in a list
            dominant_colors = kmeans.cluster_centers_.astype(int).tolist()

            # 3. DISPLAY RESULTS
            streamlit.success("Colors extracted successfully!")
            streamlit.subheader("Dominant Color Palette")

            # Create 5 equal columns
            cols = streamlit.columns(5)

            # Render each color as a UI box
            for index, color in enumerate(dominant_colors):
                # Convert RGB to HEX format
                hex_color = '#%02x%02x%02x' % tuple(color)

                with cols[index]:
                    # Draw the color box using HTML/CSS
                    streamlit.markdown(
                        f"<div style='background-color: {hex_color}; width: 100%; height: 50px; border-radius: 5px; border: 1px solid #ddd;'></div>",
                        unsafe_allow_html=True
                    )
                    streamlit.write(hex_color)

            # Placeholder for future Claude AI integration
            streamlit.subheader("🤖 AI Analysis")
            streamlit.info(
                "The extracted colors will be sent to Claude API for design and psychological analysis here.")
