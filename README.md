# 🎨 AI-Powered Color Palette Analyzer

An intelligent web application that extracts the dominant color palette from uploaded images using Machine Learning and provides expert design analysis using Generative AI.

**Current Tech Stack:** Python · Streamlit · Scikit-Learn (K-Means) · Google Gemini API (`gemini-2.5-flash`)
**Upcoming Cloud Architecture:** AWS · Docker

🚧 Work in progress (Currently finalizing local ML/AI integration and preparing for AWS deployment)

## 🚀 Features

* **Mathematical Color Extraction:** Uses the K-Means clustering machine learning algorithm to precisely identify the top 5 dominant colors from the pixels of any uploaded image.
* **AI Design Psychologist:** Integrates with Google's latest Generative AI model to analyze the extracted colors and suggest perfect fits for brand identity, website UI, and interior design.
* **Secure Architecture:** Built with `.env` environment variables to ensure API keys and credentials are never exposed in version control.

## 💻 How to Run Locally (For Developers)

If you want to test this project on your local machine, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/AhmetKucukkoylu/color-palette-analyzer.git](https://github.com/AhmetKucukkoylu/color-palette-analyzer.git)
cd color-palette-analyzer
```

**2. Set up the virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install required libraries:**
```bash
pip install streamlit pillow numpy scikit-learn python-dotenv google-genai
```

**4. Set up the Google Gemini API Key:**
* Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
* Create a file named `.env` in the root directory.
* Add your key inside the `.env` file exactly like this (no quotes, no spaces):
```text
GEMINI_API_KEY=your_api_key_here
```

**5. Launch the application:**
```bash
streamlit run color_analyzer.py
```