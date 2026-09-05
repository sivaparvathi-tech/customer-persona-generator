import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import json
translations = {
    "English": {
        "product_description": "Product Description",
        "target_market": "Target Market",
        "number_personas": "Number of Personas",
        "generate": "Generate Personas",
        "demographics": "Demographics",
        "pain_points": "Pain Points",
        "goals": "Goals",
        "channels": "Preferred Channels"
    },

    "Hindi": {
        "product_description": "उत्पाद विवरण",
        "target_market": "लक्षित बाजार",
        "number_personas": "व्यक्तित्वों की संख्या",
        "generate": "व्यक्तित्व बनाएं",
        "demographics": "जनसांख्यिकी",
        "pain_points": "समस्याएँ",
        "goals": "लक्ष्य",
        "channels": "पसंदीदा चैनल"
    },

    "Telugu": {
        "product_description": "ఉత్పత్తి వివరణ",
        "target_market": "లక్ష్య మార్కెట్",
        "number_personas": "పర్సనాల సంఖ్య",
        "generate": "పర్సనాలను రూపొందించండి",
        "demographics": "జనాభా వివరాలు",
        "pain_points": "సమస్యలు",
        "goals": "లక్ష్యాలు",
        "channels": "ఇష్టపడే ఛానెల్‌లు"
    },

    "Tamil": {
        "product_description": "தயாரிப்பு விளக்கம்",
        "target_market": "இலக்கு சந்தை",
        "number_personas": "பெர்சோனாக்களின் எண்ணிக்கை",
        "generate": "பெர்சோனாக்களை உருவாக்கவும்",
        "demographics": "மக்கள்தொகை விவரங்கள்",
        "pain_points": "சிக்கல்கள்",
        "goals": "இலக்குகள்",
        "channels": "விருப்பமான சேனல்கள்"
    },

    "Kannada": {
        "product_description": "ಉತ್ಪನ್ನ ವಿವರಣೆ",
        "target_market": "ಗುರಿ ಮಾರುಕಟ್ಟೆ",
        "number_personas": "ಪರ್ಸೋನಾಗಳ ಸಂಖ್ಯೆ",
        "generate": "ಪರ್ಸೋನಾಗಳನ್ನು ರಚಿಸಿ",
        "demographics": "ಜನಸಂಖ್ಯಾ ವಿವರಗಳು",
        "pain_points": "ಸಮಸ್ಯೆಗಳು",
        "goals": "ಗುರಿಗಳು",
        "channels": "ಆದ್ಯತೆಯ ಚಾನೆಲ್‌ಗಳು"
    },

    "Malayalam": {
        "product_description": "ഉൽപ്പന്ന വിവരണം",
        "target_market": "ലക്ഷ്യ വിപണി",
        "number_personas": "പേഴ്സണകളുടെ എണ്ണം",
        "generate": "പേഴ്സണകൾ സൃഷ്ടിക്കുക",
        "demographics": "ജനസംഖ്യാ വിവരങ്ങൾ",
        "pain_points": "പ്രശ്നങ്ങൾ",
        "goals": "ലക്ഷ്യങ്ങൾ",
        "channels": "ഇഷ്ടപ്പെട്ട ചാനലുകൾ"
    }
}
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if api_key:
    st.success("Gemini API key loaded successfully!")
else:
    st.error("Gemini API key not found.")

st.set_page_config(
    page_title="AI Customer Persona Generator",
    page_icon="👤",
    layout="wide"
)
st.markdown(
    """
    <style>

    .persona-card {
        background-color: white;
        color: #1f2937;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 22px;
        margin-top: 20px;
        min-height: 500px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    }

    .persona-name {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 22px;
    }

    .persona-section {
        margin-bottom: 20px;
    }

    .persona-heading {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .persona-card ul {
        padding-left: 20px;
        margin-top: 5px;
    }

    .persona-card li {
        margin-bottom: 6px;
        font-size: 14px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align:center; padding: 10px 0 25px 0;">
        <h1 style="font-size:42px; margin-bottom:8px;">
            ✨ AI Customer Persona Generator
        </h1>
        <p style="font-size:18px; color:#6b7280;">
            Turn your product and target market into realistic customer personas.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write(
    "Generate detailed customer personas based on your product "
    "and target market."
)

st.subheader("Interaction Language")

interaction_language = st.selectbox(
    "Choose the language for AI-generated personas",
    ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam"]
)

t = translations[interaction_language]

st.subheader(t["product_description"])

product_description = st.text_area(
    t["product_description"],
    placeholder="Describe your product..."
)
st.subheader(t["target_market"])

target_market = st.text_area(
    t["target_market"],
    placeholder="Describe your target market..."
)

st.subheader(t["number_personas"])

number_of_personas = st.number_input(
    t["number_personas"],
    min_value=2,
    max_value=5,
    value=3,
    step=1
)

if st.button(t["generate"]):

    if not product_description.strip():

        st.warning("Please enter a product description.")

    elif not target_market.strip():

        st.warning("Please enter your target market.")

    else:

        prompt = f"""
You are an expert customer research and marketing assistant.

The selected interaction language is: {interaction_language}

The user may provide the product description and target market
in the selected interaction language.

Understand the user's input even if it is written in that language.

Generate all customer persona content in the selected interaction language.
Persona names must be written in the selected interaction language's script.

Based on the following information, generate exactly
{number_of_personas} distinct customer personas.
PRODUCT DESCRIPTION:
{product_description}

TARGET MARKET:
{target_market}

For each persona, provide:

1. Persona Name
2. Demographics
3. Pain Points
4. Goals
5. Preferred Channels

All text values must be written in {interaction_language}.
Do not translate the user's input into English before generating the personas.

Make each persona realistic and clearly different
from the others.

Do not create a marketing strategy.
Focus only on describing the customers.

Return the result as a JSON array.

Each persona must have exactly these fields:

- name
- demographics
- pain_points
- goals
- preferred_channels

The value of demographics should be a list of short strings.
The value of pain_points should be a list of short strings.
The value of goals should be a list of short strings.
The value of preferred_channels should be a list of short strings.

Return only valid JSON.
Do not include markdown code fences.
"""

        with st.spinner("Generating customer personas..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            st.subheader(t["generated_personas"])

        try:

            personas = json.loads(response.text)

            columns = st.columns(len(personas))

            for i, persona in enumerate(personas):

                with columns[i]:

                    st.markdown(
    f"""<div class="persona-card">
<div class="persona-name">
👤 {persona["name"]}
</div>

<div class="persona-section">
<div class="persona-heading">
{t["demographics"]}
</div>
<ul>
{"".join(
    f"<li>{item}</li>"
    for item in persona["demographics"]
)}
</ul>
</div>

<div class="persona-section">
<div class="persona-heading">
😣 {t["pain_points"]}
</div>
<ul>
{"".join(
    f"<li>{item}</li>"
    for item in persona["pain_points"]
)}
</ul>
</div>

<div class="persona-section">
<div class="persona-heading">
🎯 {t["goals"]}
</div>
<ul>
{"".join(
    f"<li>{item}</li>"
    for item in persona["goals"]
)}
</ul>
</div>

<div class="persona-section">
<div class="persona-heading">
📱 {t["channels"]}
</div>
<ul>
{"".join(
    f"<li>{item}</li>"
    for item in persona["preferred_channels"]
)}
</ul>
</div>

</div>""",
    unsafe_allow_html=True
)           
            st.subheader("Persona Comparison")

            comparison_html = f"""
            <table style="width:100%; border-collapse:collapse;">
            <tr>
                <th style="border:1px solid #ddd; padding:10px; text-align:left;">Persona</th>
                <th style="border:1px solid #ddd; padding:10px; text-align:left;">{t["demographics"]}</th>
                <th style="border:1px solid #ddd; padding:10px; text-align:left;">{t["pain_points"]}</th>
                <th style="border:1px solid #ddd; padding:10px; text-align:left;">{t["goals"]}</th>
                <th style="border:1px solid #ddd; padding:10px; text-align:left;">{t["channels"]}</th>
            </tr>
            """

            for persona in personas:

                comparison_html += f"""
            <tr>
                <td style="border:1px solid #ddd; padding:10px;">
                    <strong>{persona["name"]}</strong>
                </td>

                <td style="border:1px solid #ddd; padding:10px;">
                    {"<br>".join(persona["demographics"])}
                </td>

                <td style="border:1px solid #ddd; padding:10px;">
                    {"<br>".join(persona["pain_points"])}
                </td>

                <td style="border:1px solid #ddd; padding:10px;">
                    {"<br>".join(persona["goals"])}
                </td>

                <td style="border:1px solid #ddd; padding:10px;">
                    {"<br>".join(persona["preferred_channels"])}
                </td>
            </tr>
            """
            comparison_html += "</table>"

            st.html(comparison_html)

        except json.JSONDecodeError:

            st.error(
                "The AI returned an invalid response. Please try again."
            )
# Export personas as shareable one-page cards

if "personas" in locals():

    st.subheader("Export Persona Cards")

    export_html = """
    <html>
    <head>
        <title>Customer Persona Cards</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f7fb;
                margin: 0;
                padding: 30px;
            }

            .persona-card {
                background: white;
                max-width: 700px;
                margin: 0 auto 30px auto;
                padding: 35px;
                border-radius: 18px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                page-break-after: always;
            }

            h1 {
                text-align: center;
                margin-bottom: 30px;
            }

            h2 {
                margin-bottom: 25px;
            }

            h3 {
                margin-top: 22px;
                margin-bottom: 8px;
            }

            li {
                margin-bottom: 7px;
            }

            @media print {
                body {
                    background: white;
                    padding: 0;
                }

                .persona-card {
                    box-shadow: none;
                    margin: 0;
                    max-width: none;
                    min-height: 90vh;
                }
            }
        </style>
    </head>
    <body>

    <h1>Customer Persona Cards</h1>
    """

    for persona in personas:

        export_html += f"""
        <div class="persona-card">

            <h2>👤 {persona["name"]}</h2>

            <h3>👥 Demographics</h3>
            <ul>
                {"".join(f"<li>{item}</li>" for item in persona["demographics"])}
            </ul>

            <h3>😣 Pain Points</h3>
            <ul>
                {"".join(f"<li>{item}</li>" for item in persona["pain_points"])}
            </ul>

            <h3>🎯 Goals</h3>
            <ul>
                {"".join(f"<li>{item}</li>" for item in persona["goals"])}
            </ul>

            <h3>📱 Preferred Channels</h3>
            <ul>
                {"".join(f"<li>{item}</li>" for item in persona["preferred_channels"])}
            </ul>

        </div>
        """

    export_html += """
    </body>
    </html>
    """

    st.download_button(
        label="📥 Download Persona Cards",
        data=export_html,
        file_name="customer_persona_cards.html",
        mime="text/html"
    )

