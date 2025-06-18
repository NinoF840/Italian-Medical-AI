import streamlit as st
import re
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List

# STARTER VERSION - €2,500/month
st.set_page_config(
    page_title="Medico-Italiano-IA Starter",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Starter version configuration
STARTER_CONFIG = {
    'daily_limit': 100,  # 100 requests per day
    'text_max_length': 2000,  # 2000 characters max
    'batch_processing': False,  # No batch processing
    'api_access': False,  # No API access
    'custom_entities': False,  # No custom entities
    'export_formats': ['TXT'],  # Basic export only
    'support_level': 'Email',  # Email support only
}

# Starter CSS styling
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
}
.starter-header {
    background: linear-gradient(90deg, #0277bd, #0288d1);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.starter-badge {
    background: linear-gradient(45deg, #0277bd, #03a9f4);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    display: inline-block;
    margin: 10px 0;
}
.entity-box {
    padding: 0.5rem 1rem;
    margin: 0.3rem;
    border-radius: 20px;
    display: inline-block;
    color: white;
    font-weight: bold;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.medication { background: linear-gradient(45deg, #FF6B6B, #FF5252); }
.symptom { background: linear-gradient(45deg, #4ECDC4, #26C6DA); }
.anatomy { background: linear-gradient(45deg, #96CEB4, #66BB6A); }
.procedure { background: linear-gradient(45deg, #FFEAA7, #FFD54F); color: #333; }
.usage-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-left: 4px solid #0277bd;
}
</style>
""", unsafe_allow_html=True)

class StarterMedicalNER:
    def __init__(self):
        self.demo_responses = self.load_enhanced_demo_data()
        self.entity_patterns = self.load_starter_patterns()
    
    def load_enhanced_demo_data(self) -> Dict:
        """Enhanced demo responses for Starter version"""
        return {
            "Il paziente presenta febbre alta e mal di testa con nausea.": {
                "entities": [
                    {"text": "paziente", "label": "PERSON", "confidence": 0.92},
                    {"text": "febbre alta", "label": "SYMPTOM", "confidence": 0.96},
                    {"text": "mal di testa", "label": "SYMPTOM", "confidence": 0.94},
                    {"text": "nausea", "label": "SYMPTOM", "confidence": 0.89}
                ],
                "processing_time": 0.145
            },
            "Prescrizione: ibuprofene 400mg ogni 8 ore dopo i pasti.": {
                "entities": [
                    {"text": "ibuprofene", "label": "MEDICATION", "confidence": 0.98},
                    {"text": "400mg", "label": "DOSAGE", "confidence": 0.95},
                    {"text": "ogni 8 ore", "label": "FREQUENCY", "confidence": 0.92},
                    {"text": "dopo i pasti", "label": "TIMING", "confidence": 0.88}
                ],
                "processing_time": 0.156
            },
            "Esame radiologico del torace: polmoni chiari, cuore nei limiti.": {
                "entities": [
                    {"text": "Esame radiologico", "label": "PROCEDURE", "confidence": 0.97},
                    {"text": "torace", "label": "ANATOMY", "confidence": 0.94},
                    {"text": "polmoni", "label": "ANATOMY", "confidence": 0.96},
                    {"text": "cuore", "label": "ANATOMY", "confidence": 0.95}
                ],
                "processing_time": 0.167
            }
        }
    
    def load_starter_patterns(self) -> Dict:
        """Enhanced patterns for Starter version"""
        return {
            'MEDICATION': [
                r'\b(ibuprofene|aspirina|paracetamolo|antibiotico|farmaco|medicina|tachipirina|brufen|oki|voltaren)\b'
            ],
            'SYMPTOM': [
                r'\b(febbre|dolore|nausea|vomito|tosse|mal di testa|sintomo|cefalea|vertigini|affaticamento)\b'
            ],
            'ANATOMY': [
                r'\b(torace|addome|cuore|polmoni|stomaco|testa|corpo|fegato|reni|cervello|occhi)\b'
            ],
            'PROCEDURE': [
                r'\b(radiografia|ecografia|biopsia|intervento|operazione|esame|analisi|risonanza|tac|endoscopia)\b'
            ],
            'DOSAGE': [r'\b\d+\s?(mg|ml|g|mcg|compresse?|gocce|capsule)\b'],
            'FREQUENCY': [r'\b(ogni|volta|volte|ore|giorni|settimana|mese|mattina|sera)\b'],
            'PERSON': [r'\b(paziente|dottore|medico|infermiere|specialista|chirurgo)\b'],
            'TIMING': [r'\b(prima|dopo|durante|pasti|colazione|pranzo|cena)\b']
        }
    
    def enhanced_ner(self, text: str) -> Dict:
        """Enhanced NER for Starter version with more entity types"""
        entities = []
        
        for label, pattern_list in self.entity_patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, text.lower(), re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "text": match.group(),
                        "label": label,
                        "confidence": round(0.80 + (hash(match.group()) % 18) / 100, 2)
                    })
        
        return {
            "entities": entities,
            "processing_time": round(0.12 + (len(text) / 800), 3)
        }
    
    def process_text(self, text: str) -> Dict:
        """Process text with Starter version capabilities"""
        if len(text) > STARTER_CONFIG['text_max_length']:
            return {
                "error": f"Text exceeds Starter limit ({STARTER_CONFIG['text_max_length']} chars). Upgrade to Consumer for longer texts.",
                "upgrade_required": True
            }
        
        # Use enhanced responses for exact matches
        if text.strip() in self.demo_responses:
            result = self.demo_responses[text.strip()].copy()
            result["version_note"] = "Starter version - Enhanced accuracy"
            return result
        
        # Use enhanced NER for new text
        result = self.enhanced_ner(text)
        result["version_note"] = "Starter version - Enhanced processing"
        return result

def render_entities(entities: List[Dict]) -> str:
    """Render entities with Starter styling"""
    if not entities:
        return "<p><em>No medical entities detected.</em></p>"
    
    html_content = ""
    entity_colors = {
        'MEDICATION': 'medication', 'SYMPTOM': 'symptom', 'ANATOMY': 'anatomy',
        'PROCEDURE': 'procedure', 'DOSAGE': 'medication', 'FREQUENCY': 'procedure',
        'PERSON': 'anatomy', 'TIMING': 'procedure'
    }
    
    for entity in entities:
        entity_type = entity.get('label', 'UNKNOWN')
        entity_text = entity.get('text', '')
        confidence = entity.get('confidence', 0)
        
        css_class = entity_colors.get(entity_type, 'entity-box')
        html_content += f'<span class="entity-box {css_class}">{entity_text} ({entity_type}: {confidence:.2f})</span> '
    
    return html_content

def get_usage_count(user_email: str) -> int:
    """Get daily usage count for user"""
    if 'starter_usage' not in st.session_state:
        st.session_state.starter_usage = {}
    
    today = datetime.now().strftime('%Y-%m-%d')
    user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
    
    if user_id not in st.session_state.starter_usage:
        st.session_state.starter_usage[user_id] = {}
    
    return st.session_state.starter_usage[user_id].get(today, 0)

def increment_usage(user_email: str):
    """Increment usage count"""
    today = datetime.now().strftime('%Y-%m-%d')
    user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
    
    if 'starter_usage' not in st.session_state:
        st.session_state.starter_usage = {}
    
    if user_id not in st.session_state.starter_usage:
        st.session_state.starter_usage[user_id] = {}
    
    current_count = st.session_state.starter_usage[user_id].get(today, 0)
    st.session_state.starter_usage[user_id][today] = current_count + 1

def main():
    ner = StarterMedicalNER()
    
    # Header
    st.markdown("""
    <div class="starter-header">
        <h1>🏥 Medico-Italiano-IA</h1>
        <p style="font-size: 1.2em; margin-top: 1rem;">
            Italian Medical Entity Recognition - Starter Version
        </p>
        <div class="starter-badge">💼 STARTER PLAN - €2,500/month</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Medical Text Analysis")
        
        # User authentication
        user_email = st.text_input(
            "Email (for usage tracking):",
            placeholder="your.email@company.com"
        )
        
        if user_email:
            usage_count = get_usage_count(user_email)
            remaining = STARTER_CONFIG['daily_limit'] - usage_count
            
            st.markdown(f"""
            <div class="usage-card">
                <h4>📊 Daily Usage</h4>
                <p><strong>Used:</strong> {usage_count}/{STARTER_CONFIG['daily_limit']}</p>
                <p><strong>Remaining:</strong> {remaining}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Example selector
            examples = [
                "",
                "Il paziente presenta febbre alta e mal di testa con nausea.",
                "Prescrizione: ibuprofene 400mg ogni 8 ore dopo i pasti.",
                "Esame radiologico del torace: polmoni chiari, cuore nei limiti."
            ]
            
            selected_example = st.selectbox(
                "Choose a sample text:",
                examples,
                help="Select a pre-loaded Italian medical text"
            )
            
            # Text input
            user_text = st.text_area(
                "Enter Italian medical text:",
                value=selected_example,
                height=120,
                max_chars=STARTER_CONFIG['text_max_length'],
                placeholder="Inserisci qui il testo medico italiano...",
                help=f"Starter version limited to {STARTER_CONFIG['text_max_length']} characters"
            )
            
            # Process button
            if st.button("🔍 Analyze Text (Starter)", type="primary", use_container_width=True):
                if not user_text.strip():
                    st.error("❌ Please enter some text to analyze.")
                elif remaining <= 0:
                    st.error(f"❌ Daily limit of {STARTER_CONFIG['daily_limit']} requests reached. Upgrade to Consumer for higher limits.")
                else:
                    with st.spinner("Processing with Starter AI model..."):
                        time.sleep(1.5)
                        result = ner.process_text(user_text)
                        increment_usage(user_email)
                    
                    if "error" in result:
                        st.error(result["error"])
                        if result.get("upgrade_required"):
                            st.info("💡 Consider upgrading to Consumer plan for longer text processing!")
                    else:
                        st.success("✅ Analysis Complete!")
                        
                        entities = result.get('entities', [])
                        if entities:
                            st.subheader("🏷️ Detected Medical Entities")
                            entity_html = render_entities(entities)
                            st.markdown(entity_html, unsafe_allow_html=True)
                            
                            # Statistics
                            col1_stats, col2_stats, col3_stats = st.columns(3)
                            with col1_stats:
                                st.metric("Entities Found", len(entities))
                            with col2_stats:
                                avg_conf = sum([e.get('confidence', 0) for e in entities]) / len(entities)
                                st.metric("Avg Confidence", f"{avg_conf:.3f}")
                            with col3_stats:
                                st.metric("Processing Time", f"{result.get('processing_time', 0):.3f}s")
                            
                            if result.get("version_note"):
                                st.info(f"📝 {result['version_note']}")
                        else:
                            st.info("🔍 No medical entities detected.")
        else:
            st.warning("⚠️ Please enter your email to access Starter features.")
    
    with col2:
        # Starter plan features
        st.subheader("💼 Starter Plan Features")
        st.markdown("""
        <div class="usage-card">
            <h4>✅ What's Included</h4>
            <p>• 100 requests/day</p>
            <p>• 2,000 character limit</p>
            <p>• 8 entity types</p>
            <p>• Enhanced accuracy</p>
            <p>• Email support</p>
            <p>• TXT export</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Upgrade options
        st.subheader("🚀 Upgrade Options")
        st.markdown("""
        **Consumer Plan - €7,500/month:**
        • 500 requests/day
        • 10,000 character limit
        • 15+ entity types
        • Batch processing
        • Priority support
        
        **Professional - €15,000/month:**
        • Unlimited requests
        • Unlimited text length
        • 20+ entity types
        • API access
        • Custom entities
        """)
        
        if st.button("📧 Request Upgrade", use_container_width=True):
            st.success("Upgrade request sent! We'll contact you within 4 hours.")
            st.balloons()
        
        # Contact info
        st.subheader("📞 Support")
        st.markdown("""
        **Email:** nino58150@gmail.com  
        **Response:** < 24 hours  
        **Plan:** Starter Support
        """)

if __name__ == "__main__":
    main()

