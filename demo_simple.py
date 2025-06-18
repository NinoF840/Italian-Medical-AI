import streamlit as st
import re
import time

# Simple Demo Version - Public Access
st.set_page_config(
    page_title="Medico-Italiano-IA Demo",
    page_icon="🏥",
    layout="centered"
)

# Simple styling
st.markdown("""
<style>
.demo-header {
    background: linear-gradient(90deg, #2E8B57, #228B22);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
}
.entity-box {
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
    border-radius: 15px;
    display: inline-block;
    color: white;
    font-weight: bold;
    font-size: 13px;
}
.medication { background: #FF6B6B; }
.symptom { background: #4ECDC4; }
.anatomy { background: #96CEB4; }
.procedure { background: #FFEAA7; color: #333; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="demo-header">
    <h2>🏥 Medico-Italiano-IA</h2>
    <p>Italian Medical AI - Demo Version</p>
</div>
""", unsafe_allow_html=True)

# Simple demo functionality
class SimpleDemo:
    def __init__(self):
        self.examples = {
            "Il paziente ha febbre alta.": [
                {"text": "paziente", "label": "PERSON"},
                {"text": "febbre", "label": "SYMPTOM"}
            ],
            "Prende ibuprofene 200mg.": [
                {"text": "ibuprofene", "label": "MEDICATION"},
                {"text": "200mg", "label": "DOSAGE"}
            ]
        }
    
    def analyze(self, text):
        if text in self.examples:
            return self.examples[text]
        
        # Basic pattern matching
        entities = []
        patterns = {
            'MEDICATION': r'\b(ibuprofene|aspirina|paracetamolo)\b',
            'SYMPTOM': r'\b(febbre|dolore|nausea|tosse)\b',
            'PERSON': r'\b(paziente|dottore)\b'
        }
        
        for label, pattern in patterns.items():
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                entities.append({"text": match.group(), "label": label})
        
        return entities

def render_simple_entities(entities):
    if not entities:
        return "<p><em>No entities detected in demo version.</em></p>"
    
    html = ""
    colors = {'MEDICATION': 'medication', 'SYMPTOM': 'symptom', 'PERSON': 'anatomy', 'DOSAGE': 'procedure'}
    
    for entity in entities:
        color_class = colors.get(entity['label'], 'entity-box')
        html += f'<span class="entity-box {color_class}">{entity["text"]} ({entity["label"]})</span> '
    
    return html

# Main demo interface
demo = SimpleDemo()

st.subheader("📝 Try the Demo")

# Example selector
examples = [
    "",
    "Il paziente ha febbre alta.",
    "Prende ibuprofene 200mg."
]

selected = st.selectbox("Choose example:", examples)

# Text input
user_text = st.text_area(
    "Enter Italian medical text:",
    value=selected,
    height=100,
    max_chars=200,
    placeholder="Inserisci testo medico italiano..."
)

# Analyze button
if st.button("🔍 Analyze (Demo)", type="primary"):
    if user_text.strip():
        if len(user_text) > 200:
            st.error("❌ Demo limited to 200 characters. Contact us for full version.")
        else:
            with st.spinner("Analyzing..."):
                time.sleep(1)
                entities = demo.analyze(user_text)
            
            st.success("✅ Demo Analysis Complete!")
            
            if entities:
                st.subheader("🏷️ Found Entities")
                entity_html = render_simple_entities(entities)
                st.markdown(entity_html, unsafe_allow_html=True)
                
                st.metric("Entities", len(entities))
                st.info("📝 Demo version - Limited functionality")
            else:
                st.info("🔍 No entities detected in demo.")
    else:
        st.error("❌ Please enter some text.")

# Demo limitations
st.markdown("---")
st.subheader("⚠️ Demo Limitations")
st.info("""
**Demo Version includes:**
• 200 character limit
• Basic entity types only
• Simple pattern matching
• Limited examples

**Full Version offers:**
• Unlimited text processing
• 20+ entity types
• Advanced AI accuracy
• Real-time API access
""")

# Contact for full version
st.subheader("🚀 Get Full Version")
st.markdown("""
**Contact for Professional Version:**
- 📧 Email: nino58150@gmail.com
- 💰 Starting at €2,500/month
- 📞 Response time: < 4 hours
""")

if st.button("📞 Contact Sales"):
    st.success("Request sent! We'll contact you soon.")
    st.balloons()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666; font-size: 12px;">
🏥 Medico-Italiano-IA Demo © 2025 NinoF840
</div>
""", unsafe_allow_html=True)

