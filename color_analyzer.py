import streamlit
from PIL import Image
import numpy
from sklearn.cluster import KMeans
import os
import time
from dotenv import load_dotenv
from google import genai

# 1. LOAD SECRET API KEY (Read the secret from the .env vault)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Authorize Gemini AI with the new GenAI client
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

# 2. FRONTEND CONFIGURATION
streamlit.set_page_config(
    page_title="Color Palette Analyzer", layout="centered")
streamlit.title("🎨 AI-Powered Color Palette Analyzer")
streamlit.write("Upload an image, and let's extract the dominant colors!")

# File uploader component
uploaded_file = streamlit.file_uploader(
    "Choose an image", type=["jpg", "png", "jpeg"])

# 3. BACKEND: IMAGE PROCESSING & ANALYSIS
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

            # 4. DISPLAY COLOR RESULTS
            streamlit.success("Colors extracted successfully!")
            streamlit.subheader("Dominant Color Palette")

            # Create 5 equal columns
            cols = streamlit.columns(5)

            # Store the extracted HEX codes in a list to send to the AI
            extracted_hex_codes = []

            # Render each color as a UI box
            for index, color in enumerate(dominant_colors):
                # Convert RGB to HEX format
                hex_color = '#%02x%02x%02x' % tuple(color)
                extracted_hex_codes.append(hex_color)

                with cols[index]:
                    # Draw the color box using HTML/CSS
                    streamlit.markdown(
                        f"<div style='background-color: {hex_color}; width: 100%; height: 50px; border-radius: 5px; border: 1px solid #ddd;'></div>",
                        unsafe_allow_html=True
                    )
                    streamlit.write(hex_color)

            # 5. AI ANALYSIS (GEMINI INTEGRATION)
            streamlit.subheader("🤖 AI Design Analysis")

            if not GEMINI_API_KEY:
                streamlit.error(
                    "API Key is missing! Please check your .env file.")
            else:
                with streamlit.spinner("Asking Google Gemini for design insights..."):
                    # Prepare the prompt to ask the AI
                    palette_string = ", ".join(extracted_hex_codes)
                    prompt = f"Act as an expert designer. Analyze this color palette: {palette_string}. 1. Psychological Mood: Explain in maximum 2 sentences. 2. Perfect Fits: Provide exactly 3 short bullet points (one for Brand Identity, one for Website, one for Interior). Keep the entire response extremely concise, punchy, and easy to read at a glance."

                    # --- YENİ EKLENEN RETRY (YENİDEN DENEME) MANTIĞI ---
                    retries = 3
                    for i in range(retries):
                        try:
                            # Call the NEW Gemini AI model explicitly and get the response
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=prompt,
                            )

                            # Display the AI's response on the screen
                            streamlit.write(response.text)

                            # BAŞARILI OLURSA DÖNGÜDEN ÇIK! (Gereksiz yere 3 kez çalışmasını engeller)
                            break

                        except Exception as e:
                            # Eğer hata alırsak ve hala deneme hakkımız varsa:
                            if i < retries - 1:
                                time.sleep(2)  # 2 saniye bekle
                                continue       # Döngünün başına dön ve tekrar dene
                            # Eğer 3 hakkımızı da doldurduysak ve hala hata varsa:
                            else:
                                streamlit.error(
                                    f"Google Gemini servisi şu an yoğunluktan dolayı yanıt veremiyor. (Hata Detayı: {e})")
