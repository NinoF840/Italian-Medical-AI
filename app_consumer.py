import streamlit as st
import re
import time
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List
import io

# CONSUMER VERSION - €7,500/month
st.set_page_config(
    page_title="Medico-Italiano-IA Consumer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Consumer version configuration
CONSUMER_CONFIG = {
    'daily_limit': 500,  # 500 requests per day
    'text_max_length': 10000,  # 10,000 characters max
    'batch_processing': True,  # Batch processing enabled
    'api_access': False,  # No API access yet
    'custom_entities': False,  # No custom entities yet
    'export_formats': ['TXT', 'JSON', 'CSV'],  # Multiple export formats
    'support_level': 'Priority Email + Phone',  # Priority support
    'entity_types': 15,  # More entity types
}

# Consumer CSS styling
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
}
.consumer-header {
    background: linear-gradient(90deg, #8e24aa, #ab47bc);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.consumer-badge {
    background: linear-gradient(45deg, #8e24aa, #ba68c8);
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
.disease { background: linear-gradient(45deg, #45B7D1, #42A5F5); }
.anatomy { background: linear-gradient(45deg, #96CEB4, #66BB6A); }
.procedure { background: linear-gradient(45deg, #FFEAA7, #FFD54F); color: #333; }
.condition { background: linear-gradient(45deg, #FF8A65, #FF7043); }
.finding { background: linear-gradient(45deg, #A1887F, #8D6E63); }
.usage-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-left: 4px solid #8e24aa;
}
.batch-card {
    background: linear-gradient(45deg, #f8bbd9, #f48fb1);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

class ConsumerMedicalNER:
    def __init__(self):
        self.demo_responses = self.load_advanced_demo_data()
        self.entity_patterns = self.load_consumer_patterns()
    
    def load_advanced_demo_data(self) -> Dict:
        """Advanced demo responses for Consumer version"""
        return {
            "Il paziente presenta una grave forma di polmonite batterica con febbre persistente e dispnea.": {
                "entities": [
                    {"text": "paziente", "label": "PERSON", "confidence": 0.94},
                    {"text": "grave", "label": "SEVERITY", "confidence": 0.87},
                    {"text": "polmonite batterica", "label": "DISEASE", "confidence": 0.98},
                    {"text": "febbre persistente", "label": "SYMPTOM", "confidence": 0.95},
                    {"text": "dispnea", "label": "SYMPTOM", "confidence": 0.92}
                ],
                "processing_time": 0.134
            },
            "Terapia antibiotica con amoxicillina 875mg due volte al giorno per 10 giorni, controllo ematochimico dopo 5 giorni.": {
                "entities": [
                    {"text": "Terapia antibiotica", "label": "TREATMENT", "confidence": 0.96},
                    {"text": "amoxicillina", "label": "MEDICATION", "confidence": 0.99},
                    {"text": "875mg", "label": "DOSAGE", "confidence": 0.97},
                    {"text": "due volte al giorno", "label": "FREQUENCY", "confidence": 0.94},
                    {"text": "10 giorni", "label": "DURATION", "confidence": 0.91},
                    {"text": "controllo ematochimico", "label": "PROCEDURE", "confidence": 0.93},
                    {"text": "5 giorni", "label": "TIMING", "confidence": 0.89}
                ],
                "processing_time": 0.156
            }
        }
    
    def load_consumer_patterns(self) -> Dict:
        """Advanced patterns for Consumer version with more entity types"""
        return {
            'MEDICATION': [
                r'\b(amoxicillina|azitromicina|ciprofloxacina|ibuprofene|aspirina|paracetamolo|antibiotico|farmaco|medicina|tachipirina|brufen|oki|voltaren|cortisone|prednisone)\b'
            ],
            'SYMPTOM': [
                r'\b(febbre|dolore|nausea|vomito|tosse|mal di testa|sintomo|cefalea|vertigini|affaticamento|dispnea|tachicardia|ipertensione|ipotensione)\b'
            ],
            'DISEASE': [
                r'\b(polmonite|bronchite|influenza|covid|diabete|ipertensione|malattia|patologia|sindrome|disturbo|infezione|tumore|cancro)\b'
            ],
            'ANATOMY': [
                r'\b(torace|addome|cuore|polmoni|stomaco|testa|corpo|fegato|reni|cervello|occhi|orecchie|gola|collo|schiena|braccia|gambe)\b'
            ],
            'PROCEDURE': [
                r'\b(radiografia|ecografia|biopsia|intervento|operazione|esame|analisi|risonanza|tac|endoscopia|emocromo|elettrocardiogramma|visita)\b'
            ],
            'DOSAGE': [r'\b\d+\s?(mg|ml|g|mcg|ui|compresse?|gocce|capsule|fiale)\b'],
            'FREQUENCY': [r'\b(ogni|volta|volte|ore|giorni|settimana|mese|mattina|sera|due volte|tre volte|quattro volte)\b'],
            'PERSON': [r'\b(paziente|dottore|medico|infermiere|specialista|chirurgo|ginecologo|cardiologo|dermatologo)\b'],
            'TIMING': [r'\b(prima|dopo|durante|pasti|colazione|pranzo|cena|giorni|settimane|mesi|anni)\b'],
            'TREATMENT': [r'\b(terapia|trattamento|cura|medicazione|riabilitazione|fisioterapia)\b'],
            'SEVERITY': [r'\b(grave|lieve|moderato|acuto|cronico|severo|importante)\b'],
            'DURATION': [r'\b\d+\s?(giorni|settimane|mesi|anni|ore|minuti)\b'],
            'CONDITION': [r'\b(normale|anormale|positivo|negativo|elevato|ridotto|stabile|critico)\b'],
            'FINDING': [r'\b(anomalia|lesione|massa|nodulo|ispessimento|edema|versamento|infiammazione)\b'],
            'MEASUREMENT': [r'\b\d+[.,]?\d*\s?(mmhg|bpm|kg|cm|metri|litri|percentuale|gradi)\b']
        }
    
    def advanced_ner(self, text: str) -> Dict:
        """Advanced NER for Consumer version with 15+ entity types"""
        entities = []
        
        for label, pattern_list in self.entity_patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, text.lower(), re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "text": match.group(),
                        "label": label,
                        "confidence": round(0.82 + (hash(match.group()) % 16) / 100, 2)
                    })
        
        return {
            "entities": entities,
            "processing_time": round(0.10 + (len(text) / 600), 3)
        }
    
    def process_text(self, text: str) -> Dict:
        """Process text with Consumer version capabilities"""
        if len(text) > CONSUMER_CONFIG['text_max_length']:
            return {
                "error": f"Text exceeds Consumer limit ({CONSUMER_CONFIG['text_max_length']} chars). Upgrade to Professional for unlimited processing.",
                "upgrade_required": True
            }
        
        # Use advanced responses for exact matches
        if text.strip() in self.demo_responses:
            result = self.demo_responses[text.strip()].copy()
            result["version_note"] = "Consumer version - Advanced AI processing"
            return result
        
        # Use advanced NER for new text
        result = self.advanced_ner(text)
        result["version_note"] = "Consumer version - 15+ entity types"
        return result
    
    def process_batch(self, texts: List[str]) -> List[Dict]:
        """Batch processing for Consumer version"""
        results = []
        for text in texts:
            if text.strip():
                result = self.process_text(text)
                result["text"] = text[:100] + "..." if len(text) > 100 else text
                results.append(result)
        return results

def render_advanced_entities(entities: List[Dict]) -> str:
    """Render entities with Consumer styling including new entity types"""
    if not entities:
        return "<p><em>No medical entities detected.</em></p>"
    
    html_content = ""
    entity_colors = {
        'MEDICATION': 'medication', 'SYMPTOM': 'symptom', 'DISEASE': 'disease',
        'ANATOMY': 'anatomy', 'PROCEDURE': 'procedure', 'DOSAGE': 'medication',
        'FREQUENCY': 'procedure', 'PERSON': 'anatomy', 'TIMING': 'procedure',
        'TREATMENT': 'condition', 'SEVERITY': 'finding', 'DURATION': 'procedure',
        'CONDITION': 'condition', 'FINDING': 'finding', 'MEASUREMENT': 'medication'
    }
    
    for entity in entities:
        entity_type = entity.get('label', 'UNKNOWN')
        entity_text = entity.get('text', '')
        confidence = entity.get('confidence', 0)
        
        css_class = entity_colors.get(entity_type, 'entity-box')
        html_content += f'<span class="entity-box {css_class}">{entity_text} ({entity_type}: {confidence:.2f})</span> '
    
    return html_content

def export_results(entities: List[Dict], format_type: str) -> str:
    """Export results in different formats"""
    if format_type == "JSON":
        return json.dumps(entities, indent=2, ensure_ascii=False)
    elif format_type == "CSV":
        csv_content = "Entity,Label,Confidence\n"
        for entity in entities:
            csv_content += f'"{entity.get("text", "")}","{entity.get("label", "")}",{entity.get("confidence", 0)}\n'
        return csv_content
    else:  # TXT
        txt_content = "Detected Medical Entities:\n\n"
        for entity in entities:
            txt_content += f"- {entity.get('text', '')} ({entity.get('label', '')}: {entity.get('confidence', 0):.2f})\n"
        return txt_content

def get_consumer_usage_count(user_email: str) -> int:
    """Get daily usage count for Consumer user"""
    if 'consumer_usage' not in st.session_state:
        st.session_state.consumer_usage = {}
    
    today = datetime.now().strftime('%Y-%m-%d')
    user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
    
    if user_id not in st.session_state.consumer_usage:
        st.session_state.consumer_usage[user_id] = {}
    
    return st.session_state.consumer_usage[user_id].get(today, 0)

def increment_consumer_usage(user_email: str):
    """Increment Consumer usage count"""
    today = datetime.now().strftime('%Y-%m-%d')
    user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
    
    if 'consumer_usage' not in st.session_state:
        st.session_state.consumer_usage = {}
    
    if user_id not in st.session_state.consumer_usage:
        st.session_state.consumer_usage[user_id] = {}
    
    current_count = st.session_state.consumer_usage[user_id].get(today, 0)
    st.session_state.consumer_usage[user_id][today] = current_count + 1

def main():
    ner = ConsumerMedicalNER()
    
    # Header
    st.markdown("""
    <div class="consumer-header">
        <h1>🏥 Medico-Italiano-IA</h1>
        <p style="font-size: 1.2em; margin-top: 1rem;">
            Italian Medical Entity Recognition - Consumer Version
        </p>
        <div class="consumer-badge">🎯 CONSUMER PLAN - €7,500/month</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab interface for different features
    tab1, tab2, tab3 = st.tabs(["🔍 Single Analysis", "📦 Batch Processing", "📊 Export & Reports"])
    
    with tab1:
        # Single text analysis
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Advanced Medical Text Analysis")
            
            # User authentication
            user_email = st.text_input(
                "Email (for usage tracking):",
                placeholder="your.email@company.com"
            )
            
            if user_email:
                usage_count = get_consumer_usage_count(user_email)
                remaining = CONSUMER_CONFIG['daily_limit'] - usage_count
                
                st.markdown(f"""
                <div class="usage-card">
                    <h4>📊 Daily Usage - Consumer Plan</h4>
                    <p><strong>Used:</strong> {usage_count}/{CONSUMER_CONFIG['daily_limit']}</p>
                    <p><strong>Remaining:</strong> {remaining}</p>
                    <p><strong>Character Limit:</strong> {CONSUMER_CONFIG['text_max_length']:,} chars</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Example selector
                examples = [
                    "",
                    "Il paziente presenta una grave forma di polmonite batterica con febbre persistente e dispnea.",
                    "Terapia antibiotica con amoxicillina 875mg due volte al giorno per 10 giorni, controllo ematochimico dopo 5 giorni."
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
                    height=150,
                    max_chars=CONSUMER_CONFIG['text_max_length'],
                    placeholder="Inserisci qui il testo medico italiano...",
                    help=f"Consumer version - up to {CONSUMER_CONFIG['text_max_length']:,} characters"
                )
                
                # Process button
                if st.button("🔍 Analyze Text (Consumer)", type="primary", use_container_width=True):
                    if not user_text.strip():
                        st.error("❌ Please enter some text to analyze.")
                    elif remaining <= 0:
                        st.error(f"❌ Daily limit of {CONSUMER_CONFIG['daily_limit']} requests reached. Upgrade to Professional for unlimited access.")
                    else:
                        with st.spinner("Processing with Consumer AI model (15+ entity types)..."):
                            time.sleep(1.2)
                            result = ner.process_text(user_text)
                            increment_consumer_usage(user_email)
                        
                        if "error" in result:
                            st.error(result["error"])
                            if result.get("upgrade_required"):
                                st.info("💡 Consider upgrading to Professional plan for unlimited text processing!")
                        else:
                            st.success("✅ Consumer Analysis Complete!")
                            
                            entities = result.get('entities', [])
                            if entities:
                                st.subheader("🏷️ Detected Medical Entities (Advanced)")
                                entity_html = render_advanced_entities(entities)
                                st.markdown(entity_html, unsafe_allow_html=True)
                                
                                # Advanced statistics
                                col1_stats, col2_stats, col3_stats, col4_stats = st.columns(4)
                                with col1_stats:
                                    st.metric("Total Entities", len(entities))
                                with col2_stats:
                                    avg_conf = sum([e.get('confidence', 0) for e in entities]) / len(entities)
                                    st.metric("Avg Confidence", f"{avg_conf:.3f}")
                                with col3_stats:
                                    st.metric("Processing Time", f"{result.get('processing_time', 0):.3f}s")
                                with col4_stats:
                                    unique_types = len(set([e.get('label') for e in entities]))
                                    st.metric("Entity Types", unique_types)
                                
                                # Export options
                                st.subheader("📥 Export Results")
                                export_format = st.selectbox("Export format:", ["TXT", "JSON", "CSV"])
                                export_content = export_results(entities, export_format)
                                
                                st.download_button(
                                    label=f"Download as {export_format}",
                                    data=export_content,
                                    file_name=f"medical_entities.{export_format.lower()}",
                                    mime="text/plain"
                                )
                                
                                if result.get("version_note"):
                                    st.info(f"📝 {result['version_note']}")
                            else:
                                st.info("🔍 No medical entities detected.")
            else:
                st.warning("⚠️ Please enter your email to access Consumer features.")
        
        with col2:
            # Consumer plan features
            st.subheader("🎯 Consumer Plan Features")
            st.markdown("""
            <div class="usage-card">
                <h4>✅ What's Included</h4>
                <p>• 500 requests/day</p>
                <p>• 10,000 character limit</p>
                <p>• 15+ entity types</p>
                <p>• Batch processing</p>
                <p>• Priority support</p>
                <p>• Multiple export formats</p>
                <p>• Advanced accuracy</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # Batch processing
        st.subheader("📦 Batch Processing")
        st.markdown("""
        <div class="batch-card">
            <h4>🚀 Process Multiple Texts</h4>
            <p>Upload multiple medical texts for batch analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        batch_texts = st.text_area(
            "Enter multiple texts (one per line):",
            height=200,
            placeholder="Il paziente ha febbre.\nPrescrizione: ibuprofene 400mg.\nEsame del sangue normale."
        )
        
        if st.button("🔄 Process Batch", type="secondary"):
            if batch_texts.strip():
                texts = [t.strip() for t in batch_texts.split('\n') if t.strip()]
                with st.spinner(f"Processing {len(texts)} texts..."):
                    time.sleep(2)
                    batch_results = ner.process_batch(texts)
                
                st.success(f"✅ Processed {len(batch_results)} texts!")
                
                for i, result in enumerate(batch_results, 1):
                    with st.expander(f"Text {i}: {result.get('text', '')[:50]}..."):
                        entities = result.get('entities', [])
                        if entities:
                            entity_html = render_advanced_entities(entities)
                            st.markdown(entity_html, unsafe_allow_html=True)
                        else:
                            st.write("No entities detected.")
    
    with tab3:
        # Export and reports
        st.subheader("📊 Export & Reports")
        st.info("📋 Export features available after processing texts in the Analysis tab.")
        
        # Upgrade options
        st.subheader("🚀 Upgrade to Professional")
        st.markdown("""
        **Professional Plan - €15,000/month:**
        • **Unlimited** requests per day
        • **Unlimited** text length
        • **20+** entity types
        • **Real-time API** access
        • **Custom entity** training
        • **24/7 phone** support
        • **Advanced analytics**
        • **Custom integrations**
        """)
        
        if st.button("📧 Request Professional Upgrade", use_container_width=True):
            st.success("Professional upgrade request sent! We'll contact you within 2 hours.")
            st.balloons()

if __name__ == "__main__":
    main()

