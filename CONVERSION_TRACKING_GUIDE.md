# 🎯 Guida Completa Conversion Tracking - New Medical Italian

## 📋 Setup Conversion Tracking per il Tuo Progetto AI Medico

### **Passo 1: Configurazione Google Analytics 4 (GA4)**

#### **A. Creazione Account Google Analytics**
1. Vai su [Google Analytics](https://analytics.google.com)
2. Clicca "Inizia gratis" e accedi con il tuo account Google
3. Crea una nuova proprietà:
   - **Nome account**: "New Medical Italian AI"
   - **Nome proprietà**: "Italian Medical AI Demo"
   - **Settore**: "Sanità e Medicina"
   - **Fuso orario**: "Italia (GMT+1)"
   - **Valuta**: "Euro (EUR)"

#### **B. Ottenere l'ID di Misurazione GA4**
1. Nel pannello GA4, vai a **Amministrazione** → **Flussi di dati**
2. Seleziona "Web" → Aggiungi il tuo URL Streamlit
3. **IMPORTANTE**: Annota l'**ID di misurazione** (formato: G-XXXXXXXXX)
4. Questo ID sostituirà `GA_MEASUREMENT_ID` nel codice

### **Passo 2: Configurazione Google Ads**

#### **A. Creazione Account Google Ads**
1. Vai su [Google Ads](https://ads.google.com)
2. Crea nuovo account:
   - **Nome azienda**: "New Medical Italian"
   - **Sito web**: il tuo URL Streamlit
   - **Paese**: Italia
   - **Valuta**: Euro

#### **B. Setup Conversion Tracking Google Ads**
1. Nel pannello Google Ads: **Strumenti** → **Conversioni** → **+ Nuova conversione**
2. Seleziona "Sito web"
3. Crea le seguenti conversioni:

**Conversione 1: Demo Completato**
- **Nome**: "Medical AI Demo Completed"
- **Categoria**: "Lead"
- **Valore**: €25 (valore stimato lead)
- **Conteggio**: "Una volta per clic"
- **Finestra conversione**: 30 giorni

**Conversione 2: Contatto Sales**
- **Nome**: "Contact Sales Intent"
- **Categoria**: "Lead"
- **Valore**: €100 (alto valore)
- **Conteggio**: "Una volta per clic"
- **Finestra conversione**: 90 giorni

4. **IMPORTANTE**: Annota gli **ID conversione** e **etichette**
   - Formato: AW-XXXXXXXXX/YYYYYYYYY

### **Passo 3: Configurazione Facebook Pixel**

#### **A. Creazione Facebook Pixel**
1. Vai su [Facebook Business Manager](https://business.facebook.com)
2. **Gestione Eventi** → **Pixel** → **Crea Pixel**
3. Nome: "New Medical Italian AI Pixel"
4. **IMPORTANTE**: Annota l'**ID Pixel** (numero a 15-16 cifre)

#### **B. Configurazione Eventi Facebook**
Gli eventi sono già configurati nel codice per:
- **PageView**: Visualizzazione pagina
- **Lead**: Inizio demo
- **CompleteRegistration**: Demo completato
- **Contact**: Contatto sales
- **ViewContent**: Prompt upgrade

### **Passo 4: Aggiornamento Codice con i Tuoi ID**

Aggiorna il file `app.py` sostituendo i placeholder con i tuoi ID reali:

```python
# Sostituisci queste righe (circa linea 163-167):
analytics_code = analytics_code.replace('GA_MEASUREMENT_ID', 'G-TUO_ID_GA4')  
analytics_code = analytics_code.replace('AW-CONVERSION_ID', 'AW-TUO_ID_GOOGLE_ADS')   
analytics_code = analytics_code.replace('FACEBOOK_PIXEL_ID', 'TUO_ID_FACEBOOK_PIXEL')   
analytics_code = analytics_code.replace('CONVERSION_LABEL', 'TUA_ETICHETTA_DEMO')     
analytics_code = analytics_code.replace('CONTACT_CONVERSION_LABEL', 'TUA_ETICHETTA_CONTATTO')
```

**Esempio con ID reali:**
```python
analytics_code = analytics_code.replace('GA_MEASUREMENT_ID', 'G-ABC123XYZ')  
analytics_code = analytics_code.replace('AW-CONVERSION_ID', 'AW-123456789')   
analytics_code = analytics_code.replace('FACEBOOK_PIXEL_ID', '123456789012345')   
analytics_code = analytics_code.replace('CONVERSION_LABEL', 'demo_completed')     
analytics_code = analytics_code.replace('CONTACT_CONVERSION_LABEL', 'contact_sales')
```

### **Passo 5: Test del Tracking**

#### **A. Verifica Google Analytics**
1. Apri il tuo sito demo
2. In GA4: **Report** → **Tempo reale**
3. Dovresti vedere:
   - Utenti attivi
   - Visualizzazioni pagina
   - Eventi personalizzati

#### **B. Test Eventi Conversione**
1. **Test Demo Start**: Inserisci email e testo, clicca "Analyze"
2. **Test Demo Completion**: Completa analisi con successo
3. **Test Contact Intent**: Clicca "Contact Sales" o "Schedule Demo"

#### **C. Verifica Facebook Pixel**
1. Installa [Facebook Pixel Helper](https://chrome.google.com/webstore/detail/facebook-pixel-helper/fdgfkebogiimcoedlicjlajpkdmockpc)
2. Visita il tuo sito e verifica che il pixel sia attivo
3. Controlla che gli eventi si attivino correttamente

### **Passo 6: Configurazione Google Ads Avanzata**

#### **A. Import Conversioni in Google Ads**
1. **Strumenti** → **Conversioni** → **Importa**
2. Seleziona "Google Analytics 4"
3. Importa gli eventi GA4 come conversioni Ads

#### **B. Collegamento GA4 e Google Ads**
1. In GA4: **Amministrazione** → **Collegamento Google Ads**
2. Collega il tuo account Google Ads
3. Abilita l'importazione automatica conversioni

### **Passo 7: Configurazione Obiettivi Avanzati**

#### **A. Obiettivi Google Analytics**
```javascript
// Eventi personalizzati già configurati:
- demo_started (quando utente inizia demo)
- demo_completed (quando demo ha successo)
- contact_sales (quando utente contatta sales)
- upgrade_prompt_shown (quando appare prompt upgrade)
- view_item (quando vede prezzi)
```

#### **B. Audience per Remarketing**
1. In GA4: **Configura** → **Audience**
2. Crea audience:
   - **Demo Users**: Utenti che hanno fatto demo
   - **High Intent**: Utenti che hanno cliccato contatto
   - **Upgrade Interested**: Utenti che hanno visto prompt

### **Passo 8: Dashboard e Reportistica**

#### **A. Dashboard Google Analytics**
Crea dashboard personalizzato con:
- Numero demo giornalieri
- Tasso conversione demo → contatto
- Tempo medio sessione
- Bounce rate
- Paesi di provenienza

#### **B. Report Automatici**
1. **Insights** → **Report personalizzati**
2. Configura report automatici via email
3. Frequenza: settimanale per performance ads

### **Passo 9: Ottimizzazione Conversioni**

#### **A. Enhanced Ecommerce**
```javascript
// Già configurato per tracking prezzi:
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
```

#### **B. Valori Conversione Dinamici**
I valori sono configurati strategicamente:
- **Demo Start**: €0 (top funnel)
- **Demo Complete**: €25 (lead qualificato)
- **Contact Sales**: €100 (alto intento)
- **Schedule Demo**: €100 (molto qualificato)

### **Passo 10: Troubleshooting**

#### **A. Problemi Comuni**
1. **Pixel non traccia**: Verifica che Streamlit permetta HTML/JS
2. **Eventi non appaiono**: Controlla console browser per errori
3. **Conversioni non registrate**: Verifica ID conversione Google Ads

#### **B. Debug Tools**
- **Chrome DevTools**: Console per errori JavaScript
- **Facebook Pixel Helper**: Verifica eventi Facebook
- **Google Tag Assistant**: Debug Google Analytics
- **GA4 DebugView**: Eventi in tempo reale

### **Passo 11: GDPR e Privacy**

#### **A. Cookie Consent** (Raccomandato)
```html
<!-- Aggiungi banner cookie consent -->
<script>
// Implementazione banner consenso cookie
// Richiedi consenso prima di attivare tracking
</script>
```

#### **B. Privacy Policy**
Aggiorna la privacy policy per includere:
- Google Analytics
- Google Ads
- Facebook Pixel
- Finalità tracking
- Diritti utente

---

## 🚀 Implementazione Immediata

### **Azioni da Fare Subito:**

1. **✅ Crea account GA4** → Ottieni ID misurazione
2. **✅ Crea account Google Ads** → Configura conversioni
3. **✅ Crea Facebook Pixel** → Ottieni ID pixel
4. **✅ Aggiorna app.py** → Sostituisci placeholder con ID reali
5. **✅ Testa tutto** → Verifica eventi e conversioni
6. **✅ Crea campagne ads** → Usa keyword e ad copy forniti
7. **✅ Monitora performance** → Dashboard e report

### **Supporto Tecnico:**
- **Email**: I tuoi riferimenti di contatto
- **Documentazione**: Questo file per riferimento
- **Test URL**: Il tuo URL Streamlit per verifiche

---

**© 2025 New Medical Italian - Tracking Configuration Guide**  
*Per supporto tecnico: ninomedical.ai@gmail.com*

