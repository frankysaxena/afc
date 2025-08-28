import streamlit as st
import pandas as pd
import json
import re

# Configure page - Force light theme
st.set_page_config(
    page_title="AFC - Braze + Snowflake Integration",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme at app level
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Custom CSS for AFC branding - Bright and clean theme
st.markdown("""
<style>
    /* Force light theme everywhere and remove dark elements */
    .stApp {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    
    /* Force light sidebar */
    .stSidebar {
        background-color: #F8F9FA !important;
    }
    
    .stSidebar > div:first-child {
        background-color: #F8F9FA !important;
    }
    
    /* Override any dark themes */
    .main .block-container {
        background-color: #FFFFFF !important;
    }
    
    /* AFC Color Scheme - Bright and clean only */
    :root {
        --afc-red: #D71920;
        --afc-light-red: #FDF2F3;
        --afc-accent-red: #E8424A;
        --afc-lightest-gray: #FAFBFC;
        --afc-light-gray: #F8F9FA;
        --afc-medium-gray: #E9ECEF;
        --afc-text: #495057;
        --afc-blue: #0066CC;
        --afc-light-blue: #F0F8FF;
        --afc-border: #DEE2E6;
    }
    
    /* Header styling - bright and clean */
    .main-header {
        background: linear-gradient(135deg, var(--afc-light-red), var(--afc-lightest-gray));
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid var(--afc-red);
        text-align: center;
        box-shadow: 0 4px 15px rgba(215, 25, 32, 0.1);
    }
    
    .main-header h1 {
        color: var(--afc-red) !important;
        margin-bottom: 0.5rem;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: none;
    }
    
    .main-header p {
        color: var(--afc-text) !important;
        font-size: 1.3rem;
        margin: 0;
        font-weight: 500;
    }
    
    /* Card styling - bright and clean */
    .integration-card {
        background: #FFFFFF !important;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(215, 25, 32, 0.08);
        border: 1px solid var(--afc-border);
        border-left: 5px solid var(--afc-red);
        margin-bottom: 1.5rem;
    }
    
    .integration-card h3 {
        color: var(--afc-red) !important;
        margin-top: 0;
        font-weight: 600;
        font-size: 1.4rem;
    }
    
    .integration-card h4 {
        color: var(--afc-text) !important;
        margin-top: 0;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .integration-card p {
        color: var(--afc-text) !important;
        line-height: 1.7;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    .integration-card ul {
        color: var(--afc-text) !important;
    }
    
    .integration-card li {
        color: var(--afc-text) !important;
        margin-bottom: 0.5rem;
    }
    
    /* Benefit cards - bright and clean */
    .benefit-card {
        background: var(--afc-light-blue) !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid var(--afc-blue);
        border: 1px solid rgba(0, 102, 204, 0.15);
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.05);
    }
    
    .benefit-card h4 {
        color: var(--afc-blue) !important;
        margin-top: 0;
        margin-bottom: 0.7rem;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .benefit-card p {
        color: var(--afc-text) !important;
        margin-bottom: 0;
        line-height: 1.6;
        font-size: 1.05rem;
    }
    
    /* Highlight boxes - bright and noticeable */
    .highlight-box {
        background: var(--afc-light-red) !important;
        padding: 1.3rem;
        border-radius: 10px;
        border-left: 5px solid var(--afc-red);
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(215, 25, 32, 0.05);
    }
    
    .highlight-box p {
        color: var(--afc-text) !important;
        margin: 0;
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--afc-red);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .stButton button:hover {
        background-color: var(--afc-accent-red);
        transform: translateY(-1px);
    }
    
    /* Iframe container */
    .iframe-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid var(--afc-medium-gray);
        margin: 1rem 0;
    }
    
    .iframe-container h4 {
        color: var(--afc-red);
        margin-top: 0;
    }
    
    /* Force light theme overrides for all Streamlit components */
    .stApp, .main, .block-container, .element-container {
        background-color: #FFFFFF !important;
        color: var(--afc-text) !important;
    }
    
    /* Sidebar bright theme */
    .stSidebar, .stSidebar > div, .stSidebar .stSelectbox {
        background-color: #F8F9FA !important;
        color: var(--afc-text) !important;
    }
    
    .stSidebar .stSelectbox > div {
        background-color: #FFFFFF !important;
        border: 1px solid var(--afc-border) !important;
    }
    
    /* Override any dark text */
    .stMarkdown, .stMarkdown *, .stText, p, span, div {
        color: var(--afc-text) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--afc-red) !important;
    }
    
    /* Info/warning boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        background-color: #F0F8FF !important;
        border: 1px solid var(--afc-blue) !important;
        color: var(--afc-text) !important;
    }
    
    /* Step boxes for CDI section */
    .step-box {
        background: #FFFFFF !important;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid var(--afc-border);
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .step-box strong {
        color: var(--afc-red) !important;
        font-size: 1.1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border: 1px solid var(--afc-border) !important;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid var(--afc-border) !important;
    }
    
    /* Code blocks */
    .stCodeBlock, pre, code {
        background-color: var(--afc-lightest-gray) !important;
        border: 1px solid var(--afc-border) !important;
        color: var(--afc-text) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="main-header">
    <h1>🏥 American Family Care</h1>
    <p>Patient Engagement Analytics: Braze + Snowflake Integration</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["Overview", "Integration Benefits", "Data Schema Explorer", "Snowflake CDI Setup", "Technical Documentation", "Use Cases"]
)

if page == "Overview":
    st.markdown("## 🚀 Integration Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="integration-card">
            <h3>🔄 What This Does</h3>
            <p>Connects <strong>Braze</strong> (patient messaging) with <strong>Snowflake</strong> (data warehouse) 
            so AFC can see how patients interact with appointments, health tips, and care reminders.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box">
            <p><strong>💡 AFC Example:</strong> Patient with high BP gets 90-day check reminder → 
            Braze tracks if they respond → Data flows back to Snowflake → AFC optimizes BP monitoring campaigns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="integration-card">
            <h3>📊 What AFC Gets</h3>
            <ul>
                <li>🩺 <strong>Track BP monitoring</strong> every 90 days automatically</li>
                <li>🏥 <strong>Monitor time since last visit</strong> for all patients</li>
                <li>💊 <strong>Automate prescription refill</strong> reminders with 120-day testing</li>
                <li>🔒 <strong>Keep patient data secure</strong> and HIPAA-compliant</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "Integration Benefits":
    st.markdown("## 🎯 Benefits for American Family Care")
    
    benefits = [
        {
            "title": "🩺 Automated BP Monitoring",
            "description": "Automatically track high blood pressure patients and send 90-day check reminders without manual tracking."
        },
        {
            "title": "🏥 Visit Gap Identification", 
            "description": "Instantly see which patients haven't visited the clinic recently and trigger appropriate outreach campaigns."
        },
        {
            "title": "💊 Smart Prescription Management",
            "description": "Automate prescription refill reminders with 120-day testing alerts through lifecycle canvas campaigns."
        },
        {
            "title": "📊 Complete Health Journey View",
            "description": "Combine visit history, BP readings, and prescription data with patient engagement for complete care insights."
        },
        {
            "title": "🔒 HIPAA-Compliant Health Data",
            "description": "All patient health data stays secure and follows healthcare regulations with zero-copy data sharing."
        },
        {
            "title": "🎯 Optimized Health Campaigns",
            "description": "Use engagement data to improve BP monitoring campaigns, visit reminders, and medication compliance."
        }
    ]
    
    for benefit in benefits:
        st.markdown(f"""
        <div class="benefit-card">
            <h4>{benefit['title']}</h4>
            <p>{benefit['description']}</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Data Schema Explorer":
    st.markdown("## 📋 Braze Data Tables in Snowflake")
    
    st.info("🔍 **Explore the comprehensive data schemas** available through Braze's Snowflake Data Sharing integration.")
    
    # Parse Braze schema data
    @st.cache_data
    def parse_braze_schemas():
        """Parse the Braze Snowflake schemas from the provided content"""
        
        # Key schema tables for healthcare use cases
        tables = {
            "USERS_BEHAVIORS_APP_FIRSTSESSION_SHARED": {
                "name": "USERS_BEHAVIORS_APP_FIRSTSESSION_SHARED",
                "description": "when a user has their first session",
                "fields": [
                    {"name": "USER_ID", "type": "VARCHAR", "description": "Braze user ID of the user who performed this event"},
                    {"name": "EXTERNAL_USER_ID", "type": "VARCHAR", "description": "[PII] External ID of the user"},
                    {"name": "APP_GROUP_ID", "type": "VARCHAR", "description": "BSON ID of the app group this user belongs to"},
                    {"name": "TIME", "type": "NUMBER", "description": "UNIX timestamp at which the event happened"},
                    {"name": "SESSION_ID", "type": "VARCHAR", "description": "UUID of the session"},
                    {"name": "GENDER", "type": "VARCHAR", "description": "[PII] Gender of the user"},
                    {"name": "COUNTRY", "type": "VARCHAR", "description": "[PII] Country of the user"},
                    {"name": "TIMEZONE", "type": "VARCHAR", "description": "Time zone of the user"},
                    {"name": "LANGUAGE", "type": "VARCHAR", "description": "[PII] Language of the user"}
                ]
            },
            "USERS_BEHAVIORS_CUSTOMEVENT_SHARED": {
                "name": "USERS_BEHAVIORS_CUSTOMEVENT_SHARED", 
                "description": "when a user performs a custom event",
                "fields": [
                    {"name": "USER_ID", "type": "VARCHAR", "description": "Braze user ID of the user who performed this event"},
                    {"name": "EXTERNAL_USER_ID", "type": "VARCHAR", "description": "[PII] External ID of the user"},
                    {"name": "TIME", "type": "NUMBER", "description": "UNIX timestamp at which the event happened"},
                    {"name": "NAME", "type": "VARCHAR", "description": "Name of the custom event"},
                    {"name": "PROPERTIES", "type": "VARCHAR", "description": "Custom properties stored as a JSON encoded string"},
                    {"name": "DEVICE_ID", "type": "VARCHAR", "description": "ID of the device on which the event occurred"},
                    {"name": "PLATFORM", "type": "VARCHAR", "description": "Platform of the device"}
                ]
            },
            "USERS_MESSAGES_EMAIL_SEND_SHARED": {
                "name": "USERS_MESSAGES_EMAIL_SEND_SHARED",
                "description": "when an email is sent to a user",
                "fields": [
                    {"name": "USER_ID", "type": "VARCHAR", "description": "Braze user ID of the user who performed this event"},
                    {"name": "EMAIL_ADDRESS", "type": "VARCHAR", "description": "[PII] Email address of the user"},
                    {"name": "TIME", "type": "NUMBER", "description": "UNIX timestamp at which the event happened"},
                    {"name": "CAMPAIGN_ID", "type": "VARCHAR", "description": "BSON ID of the campaign this event belongs to"},
                    {"name": "CANVAS_ID", "type": "VARCHAR", "description": "BSON ID of the Canvas this event belongs to"},
                    {"name": "MESSAGE_VARIATION_API_ID", "type": "VARCHAR", "description": "API ID of the message variation"},
                    {"name": "SEND_ID", "type": "VARCHAR", "description": "Message send ID this message belongs to"}
                ]
            },
            "USERS_MESSAGES_SMS_SEND_SHARED": {
                "name": "USERS_MESSAGES_SMS_SEND_SHARED",
                "description": "when an SMS is sent to a user",
                "fields": [
                    {"name": "USER_ID", "type": "VARCHAR", "description": "Braze user ID of the user who performed this event"},
                    {"name": "TO_PHONE_NUMBER", "type": "VARCHAR", "description": "[PII] Phone number of the user receiving the message"},
                    {"name": "TIME", "type": "NUMBER", "description": "UNIX timestamp at which the event happened"},
                    {"name": "CAMPAIGN_ID", "type": "VARCHAR", "description": "BSON ID of the campaign this event belongs to"},
                    {"name": "FROM_PHONE_NUMBER", "type": "VARCHAR", "description": "Phone number used to send"},
                    {"name": "SUBSCRIPTION_GROUP_API_ID", "type": "VARCHAR", "description": "Subscription group API ID"},
                    {"name": "SEND_ID", "type": "VARCHAR", "description": "Message send ID this message belongs to"}
                ]
            },
            "USERS_MESSAGES_EMAIL_OPEN_SHARED": {
                "name": "USERS_MESSAGES_EMAIL_OPEN_SHARED",
                "description": "when a user opens an email",
                "fields": [
                    {"name": "USER_ID", "type": "VARCHAR", "description": "Braze user ID of the user who performed this event"},
                    {"name": "EMAIL_ADDRESS", "type": "VARCHAR", "description": "[PII] Email address of the user"},
                    {"name": "TIME", "type": "NUMBER", "description": "UNIX timestamp at which the event happened"},
                    {"name": "CAMPAIGN_ID", "type": "VARCHAR", "description": "BSON ID of the campaign this event belongs to"},
                    {"name": "USER_AGENT", "type": "VARCHAR", "description": "User agent of the device/browser"}
                ]
            }
        }
        
        return tables
    
    schemas = parse_braze_schemas()
    
    # Table selector
    table_names = list(schemas.keys())
    selected_table = st.selectbox("📊 Select a Braze data table to explore:", table_names)
    
    if selected_table:
        table_info = schemas[selected_table]
        
        # Display table information
        st.markdown(f"""
        <div class="integration-card">
            <h3>📋 {selected_table}</h3>
            <p><strong>Description:</strong> {table_info['description']}</p>
            <p><strong>Field Count:</strong> {len(table_info['fields'])} columns</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display table schema
        if table_info['fields']:
            st.markdown("### 🗂️ Table Schema")
            
            schema_df = pd.DataFrame(table_info['fields'])
            st.dataframe(
                schema_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": st.column_config.TextColumn("Field Name", width="medium"),
                    "type": st.column_config.TextColumn("Data Type", width="small"),
                    "description": st.column_config.TextColumn("Description", width="large")
                }
            )
        
        # AFC-specific healthcare use cases
        st.markdown("### 🏥 AFC Healthcare Use Cases")
        healthcare_use_cases = {
            "USERS_BEHAVIORS_APP_FIRSTSESSION_SHARED": [
                "Track new patients setting up health monitoring",
                "Identify patients who need help with BP tracking app",
                "Monitor patient onboarding for visit scheduling"
            ],
            "USERS_BEHAVIORS_CUSTOMEVENT_SHARED": [
                "Monitor BP check appointment bookings",
                "Track prescription refill request behaviors", 
                "Analyze overdue visit patient actions"
            ],
            "USERS_MESSAGES_EMAIL_SEND_SHARED": [
                "Monitor 90-day BP check reminder delivery",
                "Track 120-day prescription testing email campaigns",
                "Analyze overdue clinic visit email outreach"
            ],
            "USERS_MESSAGES_SMS_SEND_SHARED": [
                "Ensure critical BP alerts reach high-risk patients",
                "Monitor urgent overdue visit reminders",
                "Track prescription refill SMS notifications"
            ],
            "USERS_MESSAGES_EMAIL_OPEN_SHARED": [
                "Measure BP monitoring campaign engagement",
                "Optimize timing for prescription refill reminders",
                "Track overdue visit outreach effectiveness"
            ]
        }
        
        if selected_table in healthcare_use_cases:
            for use_case in healthcare_use_cases[selected_table]:
                st.markdown(f"• {use_case}")

elif page == "Snowflake CDI Setup":
    st.markdown("## ❄️ Braze Cloud Data Ingestion Setup")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🔧 Braze Cloud Data Ingestion for AFC</h3>
        <p>Set up automated patient data sync from Braze to your Snowflake warehouse following the standard Braze CDI workflow.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CDI Workflow Overview
    st.markdown("### 🔄 CDI Workflow Overview")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="step-box">
            <strong>1. 📊 Snowflake Tables</strong><br>
            Your existing Snowflake data tables
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-box">
            <strong>2. 🔄 Braze Sync</strong><br>
            Import patient data to Braze
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-box">
            <strong>3. 📤 Data Export</strong><br>
            Enhanced data back to Snowflake
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1: Your Snowflake Tables
    with st.expander("📊 **Step 1: Your Existing Snowflake Tables**", expanded=True):
        st.markdown("#### 🗄️ AFC Patient Data in Snowflake")
        
        # Sample table showing existing AFC data focused on key use cases
        sample_data = {
            "Table Name": ["PATIENTS", "CLINIC_VISITS", "BLOOD_PRESSURE_READINGS", "PRESCRIPTION_REFILLS"],
            "Description": ["Patient demographics & contact info", "Clinic visit history & time tracking", "BP monitoring & 90-day follow-ups", "Prescription refills & 120-day testing"],
            "Key Fields": ["patient_id, email, phone, last_clinic_visit", "visit_id, patient_id, visit_date, days_since_last", "patient_id, bp_reading, reading_date, next_check_due", "patient_id, medication, refill_date, next_test_due"],
            "Key Use Case": ["Time since last clinic visit tracking", "Visit frequency & follow-up scheduling", "High BP monitoring every 90 days", "BP medication refill & 120-day testing"],
            "Row Count": ["125,000", "450,000", "89,000", "45,000"],
            "Last Updated": ["2024-08-28", "2024-08-28", "2024-08-27", "2024-08-26"]
        }
        
        df_tables = pd.DataFrame(sample_data)
        st.dataframe(df_tables, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="highlight-box">
            <p><strong>💡 Key AFC Use Cases:</strong> Track time since last clinic visit → Automate BP monitoring every 90 days → 
            Manage prescription refills with 120-day testing reminders via lifecycle canvas campaigns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Step 2: Create Braze Sync
    with st.expander("🔄 **Step 2: Create Import Sync to Braze**"):
        st.markdown("#### 📥 Set Up Patient Data Import")
        
        st.markdown("""
        **In your Braze Dashboard:**
        1. Go to **Technology Partners** → **Snowflake**
        2. Click **Create new import sync** 
        3. Configure your import settings:
        """)
        
        # Configuration table focused on AFC use cases
        config_data = {
            "Setting": ["Sync Name", "Source Table", "External ID Field", "Email Field", "Update Type", "Frequency"],
            "AFC Configuration": ["AFC Health Monitoring", "PUBLIC.PATIENTS", "patient_id", "email", "Upsert", "Every 12 hours"],
            "Description": ["Health monitoring sync for BP & visits", "Patient table with visit & BP data", "Unique patient identifier", "Patient email for health reminders", "Create or update profiles", "Twice daily for health monitoring"]
        }
        
        df_config = pd.DataFrame(config_data)
        st.dataframe(df_config, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Select Fields to Import for AFC Use Cases:**
        - ✅ `patient_id` (External ID) 
        - ✅ `email` (Email address)
        - ✅ `phone` (Phone number for SMS reminders)
        - ✅ `first_name`, `last_name` (Personalization)
        - ✅ `last_clinic_visit` (Time since last visit tracking)
        - ✅ `blood_pressure_status` (High BP monitoring)
        - ✅ `next_bp_check_due` (90-day BP follow-up scheduling)
        - ✅ `prescription_refill_due` (120-day testing reminders)
        - ✅ `medication_list` (BP medication management)
        """)
    
    # Step 3: Sync Status & Monitoring
    with st.expander("📈 **Step 3: Monitor Import Sync Status**"):
        st.markdown("#### 🔍 Track Your Data Sync Performance")
        
        # Sample sync status table focused on health monitoring
        sync_data = {
            "Sync Name": ["AFC Health Monitoring"] * 5,
            "Status": ["Success", "Success", "Success", "Success", "Failed"],
            "Rows Synced": ["47,394", "47,401", "46,884", "47,205", "0"],
            "BP Patients Updated": ["8,234", "8,401", "8,156", "8,329", "0"],
            "Overdue Visits Flagged": ["1,205", "1,189", "1,234", "1,276", "0"],
            "Refill Reminders Queued": ["456", "489", "423", "467", "0"],
            "Run Duration": ["37 minutes", "35 minutes", "42 minutes", "38 minutes", "2 minutes"]
        }
        
        df_sync = pd.DataFrame(sync_data)
        st.dataframe(df_sync, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="highlight-box">
            <p><strong>🩺 Health Monitoring Success:</strong> Tracking ~8.4K BP patients, identifying 1.2K overdue visits, 
            and queueing 450+ prescription refill reminders every 12 hours!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Step 4: Export Enhanced Data Back
    with st.expander("📤 **Step 4: Export Enhanced Data to Snowflake**"):
        st.markdown("#### 🔄 Get Patient Engagement Data Back")
        
        st.markdown("""
        **What Braze Adds for AFC Health Monitoring:**
        - 🩺 **BP Reminder Engagement**: Track who opens 90-day BP check reminders
        - 💊 **Prescription Refill Response**: Monitor 120-day testing reminder effectiveness  
        - 🏥 **Visit Scheduling**: Canvas journey performance for overdue clinic visits
        - 📊 **Lifecycle Canvas Analytics**: Complete patient journey from reminder to action
        """)
        
        # Benefits table focused on AFC use cases
        benefit_data = {
            "Data Type": ["BP Check Reminders", "Prescription Refill Alerts", "Overdue Visit Outreach", "Lifecycle Canvas Performance"],
            "What You Get": ["90-day reminder open/click rates", "120-day testing reminder response", "Visit scheduling conversion rates", "End-to-end patient journey metrics"],
            "AFC Use Case": ["Optimize BP monitoring cadence", "Improve medication compliance", "Reduce overdue visit gaps", "Perfect health reminder campaigns"],
            "Sync Frequency": ["Real-time", "Real-time", "Daily", "Campaign completion"]
        }
        
        df_benefits = pd.DataFrame(benefit_data)
        st.dataframe(df_benefits, use_container_width=True, hide_index=True)
        
        st.success("""
        ✅ **READ ONLY Access** - Braze data flows to Snowflake automatically  
        ✅ **Only updating changes** - No duplicate data, just new insights  
        ✅ **No ETL tools required** - Direct integration with your warehouse  
        """)
    
    # Step 5: View Your Enhanced Data
    st.markdown("### 📊 Your Enhanced Patient Data")
    
    # Sample enhanced data view focused on AFC use cases
    enhanced_data = {
        "Patient ID": ["P001", "P002", "P003", "P004", "P005"],
        "Name": ["John Smith", "Sarah Johnson", "Mike Brown", "Lisa Davis", "Tom Wilson"],
        "Days Since Last Visit": ["45", "120", "8", "90", "180"],
        "BP Status": ["High - Due for Check", "Normal", "High - Overdue", "High - Monitored", "Normal"],
        "Next BP Check Due": ["2024-09-15", "2024-12-01", "2024-08-20", "2024-10-01", "2025-01-15"],
        "Prescription Refill": ["Due in 30 days", "Not applicable", "Overdue", "Due in 60 days", "Not applicable"],
        "Lifecycle Canvas Status": ["BP Reminder Sent", "Visit Reminder Sent", "Urgent Follow-up", "Monitoring Active", "Wellness Check"],
        "Last Engagement": ["Opened SMS", "No response", "Clicked email", "Scheduled visit", "Opened email"]
    }
    
    df_enhanced = pd.DataFrame(enhanced_data)
    st.dataframe(df_enhanced, use_container_width=True, hide_index=True)
    


elif page == "Technical Documentation":
    st.markdown("## 📚 Technical Documentation")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🔗 Official Braze Data Schemas</h3>
        <p>Access the complete raw table schemas documentation directly from Braze:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Iframe section
    st.markdown("""
    <div class="iframe-container">
        <h4>📋 Complete Schema Reference</h4>
        <p>This document contains all available Braze data tables and their field definitions for Snowflake Data Sharing:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display iframe
    iframe_url = "https://www.braze.com/docs/assets/download_file/data-sharing-raw-table-schemas.txt?dadd92e90dc27e8a5066e9eea327c65e"
    
    components_html = f"""
    <iframe 
        src="{iframe_url}" 
        width="100%" 
        height="600" 
        style="border: 1px solid #ddd; border-radius: 8px;"
        title="Braze Snowflake Data Schemas">
    </iframe>
    """
    
    st.components.v1.html(components_html, height=650)
    
    st.markdown("""
    ### 🛠️ Integration Setup Guide
    
    #### 1. Snowflake Configuration
    ```sql
    -- Create database and schema for Braze data
    CREATE DATABASE BRAZE_DATA;
    CREATE SCHEMA BRAZE_DATA.PATIENT_ENGAGEMENT;
    
    -- Grant access to Braze share
    GRANT USAGE ON DATABASE BRAZE_DATA TO ROLE BRAZE_ROLE;
    GRANT USAGE ON SCHEMA BRAZE_DATA.PATIENT_ENGAGEMENT TO ROLE BRAZE_ROLE;
    ```
    
    #### 2. Data Access Patterns
    ```sql
    -- Example: Patient engagement summary
    SELECT 
        DATE_TRUNC('day', TO_TIMESTAMP(time)) as engagement_date,
        COUNT(DISTINCT user_id) as active_patients,
        COUNT(*) as total_interactions
    FROM BRAZE_DATA.PATIENT_ENGAGEMENT.USERS_BEHAVIORS_CUSTOMEVENT_SHARED
    WHERE name IN ('appointment_booked', 'health_survey_completed')
    GROUP BY engagement_date
    ORDER BY engagement_date DESC;
    ```
    """)

elif page == "Use Cases":
    st.markdown("## 🎯 American Family Care Use Cases")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🏥 Health Monitoring & Care Optimization</h3>
        <p>Discover how AFC uses Braze + Snowflake for critical health monitoring scenarios:</p>
    </div>
    """, unsafe_allow_html=True)
    
    use_cases = [
        {
            "title": "🩺 High Blood Pressure Monitoring (90-Day Cycle)",
            "description": "Automatically track patients with high BP and send personalized reminders every 90 days for check-ups, monitoring engagement and optimizing timing.",
            "metrics": ["90-day reminder compliance tracking", "BP check appointment booking rates", "High-risk patient engagement analysis"],
            "tables": ["USERS_MESSAGES_SMS_SEND_SHARED", "USERS_BEHAVIORS_CUSTOMEVENT_SHARED", "USERS_MESSAGES_EMAIL_OPEN_SHARED"]
        },
        {
            "title": "🏥 Time Since Last Clinic Visit Tracking", 
            "description": "Monitor patient visit frequency using Snowflake data, trigger outreach campaigns for overdue patients, and track response effectiveness.",
            "metrics": ["Days since last visit analysis", "Overdue patient identification", "Visit scheduling conversion rates"],
            "tables": ["CLINIC_VISITS (Snowflake)", "USERS_MESSAGES_EMAIL_SEND_SHARED", "USERS_BEHAVIORS_CUSTOMEVENT_SHARED"]
        },
        {
            "title": "💊 Prescription Refill with 120-Day Testing",
            "description": "Manage blood pressure medication refills with automated 120-day testing reminders through Braze lifecycle canvas campaigns.",
            "metrics": ["Prescription refill compliance", "120-day testing reminder effectiveness", "Medication adherence tracking"],
            "tables": ["PRESCRIPTION_REFILLS (Snowflake)", "USERS_CANVAS_ENTRY_SHARED", "USERS_MESSAGES_SMS_SEND_SHARED"]
        },
        {
            "title": "🔄 Lifecycle Canvas Performance Analysis",
            "description": "Analyze end-to-end patient journey performance across all three health monitoring use cases using Canvas analytics.",
            "metrics": ["Canvas completion rates", "Patient journey optimization", "Health outcome improvements"],
            "tables": ["USERS_CANVAS_ENTRY_SHARED", "USERS_CANVAS_EXIT_SHARED", "USERS_BEHAVIORS_CUSTOMEVENT_SHARED"]
        }
    ]
    
    for i, use_case in enumerate(use_cases):
        with st.expander(f"📋 {use_case['title']}", expanded=(i==0)):
            st.write(use_case['description'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 Key Metrics:**")
                for metric in use_case['metrics']:
                    st.markdown(f"• {metric}")
            
            with col2:
                st.markdown("**🗃️ Data Sources:**")
                for table in use_case['tables']:
                    st.markdown(f"• `{table}`")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏥 <strong>American Family Care</strong> | Powered by Braze + Snowflake Integration</p>
    <p>🔒 HIPAA Compliant | 📊 Real-time Analytics | 🎯 Patient-Centered Care</p>
</div>
""", unsafe_allow_html=True)
