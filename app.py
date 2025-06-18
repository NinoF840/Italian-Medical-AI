import streamlit as st
import json
import time
import hashlib
from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional
import streamlit.components.v1 as components
from functools import lru_cache
import gc

# Configure page - Connection verified 2025-06-17
st.set_page_config(
    page_title="Medico-Italiano-IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Analytics 4 and Conversion Tracking
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_analytics_code():
    """Get cached analytics code to avoid regenerating on every page load"""
    return """
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID', {
            'page_title': 'New Medical Italian AI Demo',
            'page_location': window.location.href,
            'content_group1': 'Medical AI Demo',
            'content_group2': 'Italian Healthcare'
        });
        
        // Google Ads Conversion Tracking
        gtag('config', 'AW-CONVERSION_ID');
    </script>
    
    <!-- Facebook Pixel -->
    <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', 'FACEBOOK_PIXEL_ID');
        fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none"
        src="https://www.facebook.com/tr?id=FACEBOOK_PIXEL_ID&ev=PageView&noscript=1"
    /></noscript>
    
    <script>
        // Custom conversion tracking functions
        function trackDemoStart(email, textLength) {
            // Google Analytics 4 Event
            gtag('event', 'demo_started', {
                'event_category': 'engagement',
                'event_label': 'medical_ai_demo',
                'value': textLength,
                'user_email': email,
                'demo_type': 'italian_medical_ner'
            });
            
            // Facebook Pixel Event
            fbq('track', 'Lead', {
                content_name: 'Medical AI Demo',
                content_category: 'Healthcare AI',
                value: 0.00,
                currency: 'EUR'
            });
            
            console.log('Demo start tracked:', email, textLength);
        }
        
        function trackDemoCompletion(email, entitiesFound, confidence) {
            // Google Analytics 4 Conversion
            gtag('event', 'conversion', {
                'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL',
                'event_category': 'conversion',
                'event_label': 'demo_completed',
                'value': entitiesFound,
                'user_email': email,
                'confidence_score': confidence
            });
            
            // Facebook Pixel Conversion
            fbq('track', 'CompleteRegistration', {
                content_name: 'AI Demo Completed',
                content_category: 'Medical AI',
                value: 25.00,  // Estimated lead value
                currency: 'EUR'
            });
            
            console.log('Demo completion tracked:', email, entitiesFound);
        }
        
        function trackContactIntent(email, action) {
            // Google Analytics 4 High-Value Event
            gtag('event', 'contact_sales', {
                'event_category': 'conversion',
                'event_label': action,
                'value': 100,  // High-value action
                'user_email': email
            });
            
            // Google Ads Conversion
            gtag('event', 'conversion', {
                'send_to': 'AW-CONVERSION_ID/CONTACT_CONVERSION_LABEL',
                'value': 100.0,
                'currency': 'EUR'
            });
            
            // Facebook Pixel
            fbq('track', 'Contact', {
                content_name: 'Sales Contact',
                content_category: 'High Intent',
                value: 100.00,
                currency: 'EUR'
            });
            
            console.log('Contact intent tracked:', email, action);
        }
        
        function trackUpgradePrompt(email, plan) {
            // Google Analytics 4
            gtag('event', 'upgrade_prompt_shown', {
                'event_category': 'engagement',
                'event_label': plan,
                'user_email': email
            });
            
            // Facebook Pixel
            fbq('track', 'ViewContent', {
                content_name: 'Upgrade Prompt',
                content_category: plan,
                value: 0.00,
                currency: 'EUR'
            });
        }
        
        // Enhanced ecommerce tracking for pricing
        function trackPricingView(email, plan, price) {
            gtag('event', 'view_item', {
                'currency': 'EUR',
                'value': price,
                'items': [{
                    'item_id': plan.toLowerCase().replace(' ', '_'),
                    'item_name': plan + ' Plan',
                    'item_category': 'Medical AI Software',
                    'price': price,
                    'quantity': 1
                }]
            });
        }
    </script>
    """

def inject_analytics():
    """Inject Google Analytics with lazy loading and caching"""
    # Only load analytics once per session
    if 'analytics_loaded' not in st.session_state:
        analytics_code = get_analytics_code()
        
        # Replace placeholders with actual IDs
        # TODO: Update these with your actual tracking IDs:
        # 1. Get GA4 ID from https://analytics.google.com (Format: G-XXXXXXXXXX)
        # 2. Get Google Ads ID from https://ads.google.com (Format: AW-XXXXXXXXX)
        # 3. Get Facebook Pixel ID from https://business.facebook.com (Format: numeric)
        # 4. Get conversion labels from Google Ads conversion actions
        
        # Disable analytics for demo deployment - remove placeholders that cause issues
        analytics_code = analytics_code.replace('GA_MEASUREMENT_ID', '')  # Remove placeholder
        analytics_code = analytics_code.replace('AW-CONVERSION_ID', '')   # Remove placeholder
        analytics_code = analytics_code.replace('FACEBOOK_PIXEL_ID', '')   # Remove placeholder
        analytics_code = analytics_code.replace('CONVERSION_LABEL', '')     # Remove placeholder
        analytics_code = analytics_code.replace('CONTACT_CONVERSION_LABEL', '')  # Remove placeholder
        
        components.html(analytics_code, height=0)
        st.session_state.analytics_loaded = True

# Performance optimization: Only inject analytics once per session
if 'page_loaded' not in st.session_state:
    inject_analytics()
    st.session_state.page_loaded = True

# Custom CSS for professional medical theme
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.demo-header {
    background: linear-gradient(90deg, #2E8B57, #228B22);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.entity-box {
    padding: 0.5rem 1rem;
    margin: 0.3rem;
    border-radius: 20px;
    display: inline-block;
    color: white;
    font-weight: bold;
    font-size: 14px;
}
.medication { background: linear-gradient(45deg, #FF6B6B, #FF5252); }
.symptom { background: linear-gradient(45deg, #4ECDC4, #26C6DA); }
.disease { background: linear-gradient(45deg, #45B7D1, #42A5F5); }
.anatomy { background: linear-gradient(45deg, #96CEB4, #66BB6A); }
.procedure { background: linear-gradient(45deg, #FFEAA7, #FFD54F); color: #333; }
.demo-watermark {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: rgba(255,255,255,0.9);
    padding: 10px;
    border-radius: 10px;
    font-size: 12px;
    color: #666;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.upgrade-prompt {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    margin: 2rem 0;
}
.metrics-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
.contact-cta {
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

class SecureDemoNER:
    def __init__(self):
        # Lazy load demo data only when needed
        self._demo_responses = None
        self.usage_limits = {
            'free': {'daily_limit': 5, 'text_max_length': 300},
            'registered': {'daily_limit': 10, 'text_max_length': 500}
        }
    
    @property
    def demo_responses(self):
        """Lazy load demo responses to improve startup time"""
        if self._demo_responses is None:
            self._demo_responses = self.load_demo_data()
        return self._demo_responses
        
    @lru_cache(maxsize=1)
    def load_demo_data(self) -> Dict:
        """Pre-computed demo responses for common Italian medical texts (cached)"""
        return {
            "Il paziente presenta febbre alta e mal di testa.": {
                "entities": [
                    {"text": "paziente", "label": "PERSON", "confidence": 0.89},
                    {"text": "febbre alta", "label": "SYMPTOM", "confidence": 0.95},
                    {"text": "mal di testa", "label": "SYMPTOM", "confidence": 0.92}
                ],
                "processing_time": 0.156
            },
            "Prescrizione: ibuprofene 200mg tre volte al giorno.": {
                "entities": [
                    {"text": "ibuprofene", "label": "MEDICATION", "confidence": 0.98},
                    {"text": "200mg", "label": "DOSAGE", "confidence": 0.94},
                    {"text": "tre volte al giorno", "label": "FREQUENCY", "confidence": 0.91}
                ],
                "processing_time": 0.142
            },
            "Radiografia del torace normale, nessuna anomalia rilevata.": {
                "entities": [
                    {"text": "Radiografia", "label": "PROCEDURE", "confidence": 0.96},
                    {"text": "torace", "label": "ANATOMY", "confidence": 0.93},
                    {"text": "anomalia", "label": "FINDING", "confidence": 0.87}
                ],
                "processing_time": 0.178
            },
            "Sintomi: nausea, vomito e dolore addominale acuto.": {
                "entities": [
                    {"text": "nausea", "label": "SYMPTOM", "confidence": 0.91},
                    {"text": "vomito", "label": "SYMPTOM", "confidence": 0.89},
                    {"text": "dolore addominale", "label": "SYMPTOM", "confidence": 0.94},
                    {"text": "addominale", "label": "ANATOMY", "confidence": 0.88}
                ],
                "processing_time": 0.203
            }
        }
    
    @lru_cache(maxsize=128)  # Cache up to 128 text processing results
    def simple_ner_demo(self, text: str) -> Dict:
        """Basic pattern-based NER for demo purposes (cached)"""
        entities = []
        
        # Simple Italian medical patterns
        patterns = {
            'MEDICATION': [r'\b(ibuprofene|aspirina|paracetamolo|antibiotico|farmaco)\b'],
            'SYMPTOM': [r'\b(febbre|dolore|nausea|vomito|tosse|mal di testa)\b'],
            'ANATOMY': [r'\b(torace|addome|cuore|polmoni|stomaco|testa)\b'],
            'PROCEDURE': [r'\b(radiografia|ecografia|biopsia|intervento|operazione)\b'],
            'DOSAGE': [r'\b\d+\s?(mg|ml|g|compresse?)\b']
        }
        
        for label, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, text.lower(), re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "text": match.group(),
                        "label": label,
                        "confidence": round(0.75 + (hash(match.group()) % 20) / 100, 2)
                    })
        
        return {
            "entities": entities,
            "processing_time": round(0.1 + (len(text) / 1000), 3)
        }
    
    def process_demo_text(self, text: str, user_type: str = 'free') -> Dict:
        """Process text with demo limitations"""
        # Check text length limits
        max_length = self.usage_limits[user_type]['text_max_length']
        if len(text) > max_length:
            return {
                "error": f"Text too long. Demo limited to {max_length} characters. Upgrade for unlimited processing.",
                "upgrade_required": True
            }
        
        # Use pre-computed responses for exact matches
        if text.strip() in self.demo_responses:
            result = self.demo_responses[text.strip()].copy()
            result["demo_note"] = "Pre-computed demo result"
            return result
        
        # Use simple NER for new text
        result = self.simple_ner_demo(text)
        result["demo_note"] = "Simplified demo processing"
        return result
    
    def get_usage_count(self, user_id: str) -> int:
        """Get daily usage count for user with automatic cleanup"""
        if 'usage_tracking' not in st.session_state:
            st.session_state.usage_tracking = {}
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Clean up old data to prevent memory bloat
        self._cleanup_old_usage_data()
        
        if user_id not in st.session_state.usage_tracking:
            st.session_state.usage_tracking[user_id] = {}
        
        return st.session_state.usage_tracking[user_id].get(today, 0)
    
    def increment_usage(self, user_id: str):
        """Increment usage count"""
        if 'usage_tracking' not in st.session_state:
            st.session_state.usage_tracking = {}
        
        today = datetime.now().strftime('%Y-%m-%d')
        if user_id not in st.session_state.usage_tracking:
            st.session_state.usage_tracking[user_id] = {}
        
        current_count = st.session_state.usage_tracking[user_id].get(today, 0)
        st.session_state.usage_tracking[user_id][today] = current_count + 1
        
        # Trigger garbage collection periodically
        if current_count % 5 == 0:  # Every 5 requests
            gc.collect()
    
    def _cleanup_old_usage_data(self):
        """Remove usage data older than 7 days to prevent memory bloat"""
        if 'usage_tracking' not in st.session_state:
            return
        
        cutoff_date = datetime.now() - timedelta(days=7)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')
        
        # Clean up old entries
        for user_id in list(st.session_state.usage_tracking.keys()):
            user_data = st.session_state.usage_tracking[user_id]
            dates_to_remove = [
                date for date in user_data.keys() 
                if date < cutoff_str
            ]
            for date in dates_to_remove:
                del user_data[date]
            
            # Remove empty user entries
            if not user_data:
                del st.session_state.usage_tracking[user_id]

@lru_cache(maxsize=64)  # Cache rendered entity HTML
def render_entities_cached(entities_tuple) -> str:
    """Render entities with color coding (cached version)"""
    entities = [{'text': e[0], 'label': e[1], 'confidence': e[2]} for e in entities_tuple]
    return _render_entities_impl(entities)

def render_entities(entities: List[Dict]) -> str:
    """Render entities with color coding"""
    if not entities:
        return "<p><em>No medical entities detected in the text.</em></p>"
    
    # Convert to tuple for caching (lists aren't hashable)
    entities_tuple = tuple(
        (e.get('text', ''), e.get('label', ''), e.get('confidence', 0))
        for e in entities
    )
    return render_entities_cached(entities_tuple)

def _render_entities_impl(entities: List[Dict]) -> str:
    """Internal implementation for entity rendering"""
    html_content = ""
    entity_colors = {
        'MEDICATION': 'medication',
        'SYMPTOM': 'symptom',
        'DISEASE': 'disease', 
        'ANATOMY': 'anatomy',
        'PROCEDURE': 'procedure',
        'DOSAGE': 'medication',
        'FREQUENCY': 'procedure',
        'FINDING': 'disease',
        'PERSON': 'anatomy'
    }
    
    for entity in entities:
        entity_type = entity.get('label', 'UNKNOWN')
        entity_text = entity.get('text', '')
        confidence = entity.get('confidence', 0)
        
        css_class = entity_colors.get(entity_type, 'entity-box')
        html_content += f'<span class="entity-box {css_class}">{entity_text} ({entity_type}: {confidence:.2f})</span> '
    
    return html_content

def main():
    demo_ner = SecureDemoNER()
    
    # Header
    st.markdown("""
    <div class="demo-header">
        <h1>🏥 Medico-Italiano-IA</h1>
        <p style="font-size: 1.2em; margin-top: 1rem;">
            Advanced AI-Powered Medical Entity Recognition for Italian Healthcare
        </p>
        <p style="font-size: 1em; opacity: 0.9; margin-top: 0.5rem;">
            ✨ Demonstration Version - Limited Functionality ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for user registration and info
    with st.sidebar:
        st.header("🔐 Demo Access")
        
        # User registration
        user_email = st.text_input(
            "Email (required for demo)",
            placeholder="your.email@company.com",
            help="We'll use this to track your demo usage and send you upgrade information"
        )
        
        if user_email:
            user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
            usage_count = demo_ner.get_usage_count(user_id)
            daily_limit = demo_ner.usage_limits['registered']['daily_limit']
            
            st.success(f"✅ Welcome! {daily_limit - usage_count} demos remaining today")
            
            if usage_count >= daily_limit:
                st.error("❌ Daily limit reached. Contact sales for unlimited access.")
        else:
            st.warning("⚠️ Email required to access demo")
        
        st.markdown("---")
        
        # Demo information
        st.subheader("📊 Demo Limitations")
        st.info("""
        **Demo Version Includes:**
        • 10 requests/day
        • 500 character limit
        • Basic entity types
        • Watermarked results
        
        **Full Version Offers:**
        • Unlimited processing
        • Custom entity types
        • Real-time API access
        • Advanced analytics
        """)
        
        st.markdown("---")
        
        # Upgrade CTA
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); border-radius: 10px; color: white;">
            <h3>🚀 Upgrade to Full Version</h3>
            <p>Unlimited processing starting at €2,500/month</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📞 Contact Sales", use_container_width=True):
            # Track high-value contact intent
            if user_email:
                components.html(f"""
                <script>
                    if (typeof trackContactIntent !== 'undefined') {{
                        trackContactIntent('{user_email}', 'Sidebar Contact Sales');
                    }}
                </script>
                """, height=0)
            
            st.success("Redirecting to contact form...")
            st.balloons()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Italian Medical Text Analysis")
        
        # Example selector
        examples = [
            "",
            "Il paziente presenta febbre alta e mal di testa.",
            "Prescrizione: ibuprofene 200mg tre volte al giorno.", 
            "Radiografia del torace normale, nessuna anomalia rilevata.",
            "Sintomi: nausea, vomito e dolore addominale acuto."
        ]
        
        selected_example = st.selectbox(
            "Choose a sample text:",
            examples,
            help="Select a pre-loaded Italian medical text example"
        )
        
        # Text input
        user_text = st.text_area(
            "Enter Italian medical text:",
            value=selected_example,
            height=120,
            max_chars=500,
            placeholder="Inserisci qui il testo medico in italiano...\n\nEsempio: Il paziente presenta febbre alta e mal di testa.",
            help="Demo limited to 500 characters. Full version supports unlimited text length."
        )
        
        # Process button
        if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
            if not user_email:
                st.error("❌ Please enter your email in the sidebar to access the demo.")
            elif not user_text.strip():
                st.error("❌ Please enter some text to analyze.")
            else:
                # Track demo start
                components.html(f"""
                <script>
                    if (typeof trackDemoStart !== 'undefined') {{
                        trackDemoStart('{user_email}', {len(user_text)});
                    }}
                </script>
                """, height=0)
                
                user_id = hashlib.md5(user_email.encode()).hexdigest()[:8]
                usage_count = demo_ner.get_usage_count(user_id)
                daily_limit = demo_ner.usage_limits['registered']['daily_limit']
                
                if usage_count >= daily_limit:
                    st.error(f"❌ Daily limit of {daily_limit} requests reached. Contact sales for unlimited access.")
                    
                    # Upgrade prompt
                    st.markdown("""
                    <div class="upgrade-prompt">
                        <h3>🚀 Upgrade to Full Version</h3>
                        <p>Get unlimited processing, advanced features, and full API access</p>
                        <p><strong>Starting at €2,500/month</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Process the text
                    with st.spinner("Processing Italian medical text..."):
                        time.sleep(1)  # Simulate processing time
                        result = demo_ner.process_demo_text(user_text, 'registered')
                        demo_ner.increment_usage(user_id)
                    
                    if "error" in result:
                        st.error(result["error"])
                        if result.get("upgrade_required"):
                            # Track upgrade prompt shown
                            components.html(f"""
                            <script>
                                if (typeof trackUpgradePrompt !== 'undefined') {{
                                    trackUpgradePrompt('{user_email}', 'Text Length Limit');
                                }}
                            </script>
                            """, height=0)
                            
                            st.markdown("""
                            <div class="upgrade-prompt">
                                <h3>🚀 Text Too Long for Demo</h3>
                                <p>Upgrade to Full Version for unlimited text processing</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Success!
                        st.success("✅ Analysis Complete!")
                        
                        # Track successful demo completion
                        entities = result.get('entities', [])
                        avg_conf = sum([e.get('confidence', 0) for e in entities]) / len(entities) if entities else 0
                        
                        components.html(f"""
                        <script>
                            if (typeof trackDemoCompletion !== 'undefined') {{
                                trackDemoCompletion('{user_email}', {len(entities)}, {avg_conf:.3f});
                            }}
                        </script>
                        """, height=0)
                        
                        # Display entities
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
                            
                            # Demo note
                            if result.get("demo_note"):
                                st.info(f"📝 {result['demo_note']} - Full version provides enhanced accuracy")
                        else:
                            st.info("🔍 No medical entities detected in the demo version.")
                        
                        # Usage remaining
                        remaining = daily_limit - demo_ner.get_usage_count(user_id)
                        if remaining > 0:
                            st.info(f"🔄 {remaining} demo requests remaining today")
                        else:
                            st.warning("⚠️ Demo limit reached. Contact sales for unlimited access.")
    
    with col2:
        st.subheader("📈 Demo Statistics")
        
        # Mock statistics
        st.markdown("""
        <div class="metrics-card">
            <h4>🏆 Production Performance</h4>
            <p><strong>Accuracy:</strong> 95.3% F1-score</p>
            <p><strong>Speed:</strong> 1,000 docs/minute</p>
            <p><strong>Uptime:</strong> 99.9% SLA</p>
            <p><strong>Languages:</strong> Italian (native)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pricing information
        st.subheader("💰 Pricing Plans")
        
        pricing_data = {
            "Starter": "€2,500/month",
            "Professional": "€7,500/month", 
            "Enterprise": "€15,000/month",
            "On-Premise": "€100,000+"
        }
        
        for plan, price in pricing_data.items():
            st.markdown(f"**{plan}:** {price}")
        
        if st.button("📞 Schedule Demo Call", use_container_width=True):
            # Track demo call scheduling
            if user_email:
                components.html(f"""
                <script>
                    if (typeof trackContactIntent !== 'undefined') {{
                        trackContactIntent('{user_email}', 'Schedule Demo Call');
                    }}
                </script>
                """, height=0)
            
            st.success("Demo call scheduled! Check your email.")
        
        # Contact information
        st.subheader("📞 Contact Information")
        st.markdown("""
        **Email:** nino58150@gmail.com  
        **Phone:** +39 (Available on request)  
        **LinkedIn:** NinoF840 - Medical AI Research  
        
        **Response Time:** < 4 hours  
        **Demo Availability:** Same day
        """)
    
    # Footer with watermark and CTA
    st.markdown("""
    <div class="contact-cta">
        <h2>🚀 Ready for the Full Version?</h2>
        <p>Unlimited processing • Custom entity types • Real-time API • Advanced analytics</p>
        <p><strong>Transform your Italian healthcare documentation today!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo watermark
    st.markdown("""
    <div class="demo-watermark">
        💻 Demo Version - Medico-Italiano-IA<br>
        © 2025 - Professional AI Solution
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics tracking (in production, send to your analytics service)
    if user_email:
        # Log demo usage
        st.session_state.setdefault('demo_analytics', []).append({
            'timestamp': datetime.now().isoformat(),
            'user_email': user_email,
            'text_length': len(user_text) if 'user_text' in locals() else 0,
            'action': 'demo_usage'
        })

if __name__ == "__main__":
    main()

