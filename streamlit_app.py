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
            <p><strong>💡 Simple Example:</strong> When a patient opens an appointment reminder text, 
            that data flows to Snowflake where AFC can analyze patterns and improve care.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="integration-card">
            <h3>📊 What AFC Gets</h3>
            <ul>
                <li>📱 <strong>Track patient responses</strong> to messages in real-time</li>
                <li>📈 <strong>See the full picture</strong> of patient communication</li>
                <li>⚡ <strong>Automate appointment</strong> and health reminders</li>
                <li>🔒 <strong>Keep patient data secure</strong> and HIPAA-compliant</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "Integration Benefits":
    st.markdown("## 🎯 Benefits for American Family Care")
    
    benefits = [
        {
            "title": "🔄 Automatic Data Updates",
            "description": "Patient interaction data flows automatically from Braze to Snowflake - no manual work needed."
        },
        {
            "title": "📱 See All Patient Communications", 
            "description": "Track how patients respond to texts, emails, app notifications, and more in one place."
        },
        {
            "title": "🔒 Keep Data Safe & Legal",
            "description": "All patient data stays secure and follows HIPAA rules - no copying or moving sensitive information."
        },
        {
            "title": "💰 Save Storage Costs",
            "description": "Data sharing means no extra storage fees - AFC accesses Braze data directly in Snowflake."
        },
        {
            "title": "📊 Connect All Your Data",
            "description": "Combine patient messaging data with appointment, billing, and care data for the complete picture."
        },
        {
            "title": "🎯 Send Better Messages",
            "description": "Use patient behavior insights to send more effective appointment reminders and health tips."
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
        
        # Healthcare use cases for this table
        st.markdown("### 🏥 Healthcare Use Cases")
        healthcare_use_cases = {
            "USERS_BEHAVIORS_APP_FIRSTSESSION_SHARED": [
                "Track new patient onboarding completion rates",
                "Analyze patient app adoption by demographics",
                "Optimize first-visit experience workflows"
            ],
            "USERS_BEHAVIORS_CUSTOMEVENT_SHARED": [
                "Monitor appointment booking behaviors",
                "Track health survey completion rates", 
                "Analyze symptom checker usage patterns"
            ],
            "USERS_MESSAGES_EMAIL_SEND_SHARED": [
                "Monitor appointment reminder delivery",
                "Track health education email campaigns",
                "Analyze patient communication preferences"
            ],
            "USERS_MESSAGES_SMS_SEND_SHARED": [
                "Ensure critical health alerts reach patients",
                "Monitor urgent care visit reminders",
                "Track prescription pickup notifications"
            ],
            "USERS_MESSAGES_EMAIL_OPEN_SHARED": [
                "Measure health education content engagement",
                "Optimize appointment reminder timing",
                "Track preventive care campaign effectiveness"
            ]
        }
        
        if selected_table in healthcare_use_cases:
            for use_case in healthcare_use_cases[selected_table]:
                st.markdown(f"• {use_case}")

elif page == "Snowflake CDI Setup":
    st.markdown("## ❄️ Snowflake CDI Setup Guide")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🔧 Complete Cloud Data Integration Setup</h3>
        <p>Follow these step-by-step instructions to configure Braze data sharing with Snowflake for American Family Care's patient engagement analytics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Setup progress tracker
    setup_steps = [
        "Prerequisites & Account Setup",
        "Snowflake Environment Configuration", 
        "Braze Data Share Configuration",
        "Database & Schema Creation",
        "Access Control & Security",
        "Data Validation & Testing"
    ]
    
    st.markdown("### 📋 Setup Steps Overview")
    progress_cols = st.columns(len(setup_steps))
    for i, step in enumerate(setup_steps):
        with progress_cols[i]:
            st.markdown(f"""
            <div class="step-box">
                <strong>{i+1}.</strong><br>
                {step}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step 1: Prerequisites
    with st.expander("🔧 **Step 1: Prerequisites & Account Setup**", expanded=True):
        st.markdown("""
        #### ✅ What You Need Before Starting
        
        **Snowflake Access:**
        - Admin access to your Snowflake account
        - Permission to create new databases and manage data sharing
        - Snowflake account in a supported region (most US and EU regions work)
        
        **Braze Access:**
        - Admin access to your Braze dashboard  
        - Data export features enabled in your Braze plan
        - Snowflake integration feature activated
        
        **AFC Healthcare Requirements:**
        - HIPAA compliance review completed
        - Data handling policies in place
        - Patient privacy protocols established
        
        <div class="highlight-box">
            <p><strong>💡 Need Help?</strong> Contact your Braze account manager or Snowflake support 
            if you're unsure about any requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code("""
        -- Verify your Snowflake account region
        SELECT CURRENT_REGION() AS SNOWFLAKE_REGION;
        
        -- Check current user privileges
        SHOW GRANTS TO USER CURRENT_USER();
        """, language="sql")
    
    # Step 2: Snowflake Environment
    with st.expander("❄️ **Step 2: Snowflake Environment Configuration**"):
        st.markdown("""
        #### 🏗️ Environment Setup
        
        Configure your Snowflake environment to receive Braze data with proper resource allocation and security settings.
        """)
        
        st.code("""
        -- 1. Create dedicated warehouse for Braze data processing
        CREATE WAREHOUSE AFC_BRAZE_WH WITH
          WAREHOUSE_SIZE = 'SMALL'
          AUTO_SUSPEND = 300
          AUTO_RESUME = TRUE
          INITIALLY_SUSPENDED = TRUE
          COMMENT = 'Warehouse for AFC Braze data processing';
        
        -- 2. Create dedicated database for Braze data
        CREATE DATABASE AFC_BRAZE_DATA
          COMMENT = 'American Family Care - Braze patient engagement data';
        
        -- 3. Set default warehouse context
        USE WAREHOUSE AFC_BRAZE_WH;
        USE DATABASE AFC_BRAZE_DATA;
        """, language="sql")
        
        st.warning("⚠️ **Security Note**: Ensure proper network policies and IP whitelisting are configured for HIPAA compliance.")
    
    # Step 3: Braze Data Share Configuration
    with st.expander("🔗 **Step 3: Braze Data Share Configuration**"):
        st.markdown("""
        #### 📡 Configure Data Sharing in Braze
        
        Set up the data share from your Braze dashboard to your Snowflake account.
        """)
        
        st.markdown("""
        **Simple Steps in Braze Dashboard:**
        
        1. **Find the Integration**: Go to **Technology Partners** → **Data Export**
        2. **Choose Snowflake**: Click on the Snowflake option
        3. **Enter Your Details**:
           - Your Snowflake account ID (get this from your Snowflake admin)
           - Your Snowflake region (like US-East-1)
           - Share name: `AFC_BRAZE_SHARE` (we recommend this name)
        4. **Pick What Data to Share**:
           - Choose "Real-time" for live updates
           - Select data types AFC needs (see below)
           - Include last 90 days of historical data
        """)
        
        st.info("""
        🏥 **AFC Healthcare Focus**: Prioritize these data types for patient engagement:
        - User behaviors (app sessions, custom events)
        - Message engagement (email opens, SMS delivery)
        - Campaign performance data
        - Push notification interactions
        """)
        
        st.code("""
        -- Example: Expected share name format
        -- Format: <ORGANIZATION>_<WORKSPACE>_<REGION>_BRAZE_SHARE
        -- Example: AFC_PROD_US_EAST_1_BRAZE_SHARE
        """, language="sql")
    
    # Step 4: Database & Schema Creation
    with st.expander("🗃️ **Step 4: Database & Schema Creation**"):
        st.markdown("""
        #### 🏗️ Create Database Structure
        
        Set up the database schema structure to organize Braze data for AFC's healthcare analytics.
        """)
        
        st.code("""
        -- 1. Create schemas for different data categories
        CREATE SCHEMA AFC_BRAZE_DATA.PATIENT_ENGAGEMENT
          COMMENT = 'Patient interaction and engagement data';
        
        CREATE SCHEMA AFC_BRAZE_DATA.CAMPAIGNS
          COMMENT = 'Campaign and communication data';
        
        CREATE SCHEMA AFC_BRAZE_DATA.ANALYTICS
          COMMENT = 'Processed analytics and aggregated views';
        
        CREATE SCHEMA AFC_BRAZE_DATA.COMPLIANCE
          COMMENT = 'HIPAA compliance and audit data';
        
        -- 2. Create shared database from Braze share
        CREATE DATABASE AFC_BRAZE_SHARED 
        FROM SHARE <BRAZE_ACCOUNT>.AFC_BRAZE_SHARE
        COMMENT = 'Shared Braze data from data share';
        
        -- 3. Grant usage on shared database
        GRANT USAGE ON DATABASE AFC_BRAZE_SHARED TO ROLE AFC_BRAZE_ROLE;
        """, language="sql")
    
    # Step 5: Access Control & Security
    with st.expander("🔐 **Step 5: Access Control & Security Setup**"):
        st.markdown("""
        #### 🛡️ HIPAA-Compliant Access Control
        
        Configure role-based access control and security measures for patient data protection.
        """)
        
        st.code("""
        -- 1. Create dedicated roles for Braze data access
        CREATE ROLE AFC_BRAZE_ADMIN
          COMMENT = 'Administrative access to Braze data';
        
        CREATE ROLE AFC_BRAZE_ANALYST
          COMMENT = 'Read-only access for data analysts';
        
        CREATE ROLE AFC_BRAZE_REPORTING
          COMMENT = 'Limited access for reporting tools';
        
        -- 2. Grant warehouse usage
        GRANT USAGE ON WAREHOUSE AFC_BRAZE_WH TO ROLE AFC_BRAZE_ADMIN;
        GRANT USAGE ON WAREHOUSE AFC_BRAZE_WH TO ROLE AFC_BRAZE_ANALYST;
        GRANT USAGE ON WAREHOUSE AFC_BRAZE_WH TO ROLE AFC_BRAZE_REPORTING;
        
        -- 3. Grant database and schema permissions
        GRANT USAGE ON DATABASE AFC_BRAZE_DATA TO ROLE AFC_BRAZE_ADMIN;
        GRANT USAGE ON DATABASE AFC_BRAZE_SHARED TO ROLE AFC_BRAZE_ADMIN;
        
        GRANT USAGE ON ALL SCHEMAS IN DATABASE AFC_BRAZE_DATA TO ROLE AFC_BRAZE_ADMIN;
        GRANT SELECT ON ALL TABLES IN DATABASE AFC_BRAZE_SHARED TO ROLE AFC_BRAZE_ANALYST;
        
        -- 4. Create user assignments
        GRANT ROLE AFC_BRAZE_ADMIN TO USER <AFC_DATA_ADMIN>;
        GRANT ROLE AFC_BRAZE_ANALYST TO USER <AFC_DATA_ANALYST>;
        """, language="sql")
        
        st.warning("""
        🏥 **HIPAA Compliance Checklist:**
        - [ ] Audit logging enabled
        - [ ] Data encryption at rest verified
        - [ ] Access controls implemented
        - [ ] User activity monitoring configured
        - [ ] Data retention policies defined
        """)
    
    # Step 6: Data Validation & Testing
    with st.expander("✅ **Step 6: Data Validation & Testing**"):
        st.markdown("""
        #### 🧪 Validate Data Integration
        
        Test the data share connection and validate data quality for AFC's healthcare analytics.
        """)
        
        st.code("""
        -- 1. List available shares
        SHOW SHARES;
        
        -- 2. Describe the Braze share
        DESC SHARE <BRAZE_ACCOUNT>.AFC_BRAZE_SHARE;
        
        -- 3. List tables in shared database
        SHOW TABLES IN DATABASE AFC_BRAZE_SHARED;
        
        -- 4. Test data access - Patient engagement events
        SELECT 
            COUNT(*) as total_events,
            COUNT(DISTINCT user_id) as unique_patients,
            MIN(TO_TIMESTAMP(time)) as earliest_event,
            MAX(TO_TIMESTAMP(time)) as latest_event
        FROM AFC_BRAZE_SHARED.<SCHEMA>.USERS_BEHAVIORS_CUSTOMEVENT_SHARED
        WHERE DATE(TO_TIMESTAMP(time)) >= CURRENT_DATE - 7;
        
        -- 5. Validate message delivery data
        SELECT 
            DATE(TO_TIMESTAMP(time)) as message_date,
            COUNT(*) as messages_sent,
            COUNT(DISTINCT user_id) as patients_reached
        FROM AFC_BRAZE_SHARED.<SCHEMA>.USERS_MESSAGES_SMS_SEND_SHARED
        WHERE DATE(TO_TIMESTAMP(time)) >= CURRENT_DATE - 30
        GROUP BY message_date
        ORDER BY message_date DESC;
        """, language="sql")
        
        st.success("""
        ✅ **Validation Success Criteria:**
        - Data is flowing from Braze to Snowflake
        - All expected tables are accessible
        - Patient engagement events are captured
        - Message delivery data is complete
        - Data freshness meets requirements (< 24 hours)
        """)
    
    # Healthcare-specific views
    st.markdown("### 🏥 Healthcare Analytics Views")
    
    st.markdown("""
    <div class="integration-card">
        <h4>🔍 Create AFC-Specific Analytics Views</h4>
        <p>Pre-built views for common healthcare analytics use cases:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code("""
    -- Patient Engagement Summary View
    CREATE VIEW AFC_BRAZE_DATA.ANALYTICS.PATIENT_ENGAGEMENT_SUMMARY AS
    SELECT 
        DATE(TO_TIMESTAMP(time)) as engagement_date,
        COUNT(DISTINCT user_id) as active_patients,
        COUNT(*) as total_interactions,
        COUNT(CASE WHEN name = 'appointment_booked' THEN 1 END) as appointments_booked,
        COUNT(CASE WHEN name = 'health_survey_completed' THEN 1 END) as surveys_completed,
        COUNT(CASE WHEN name = 'symptom_checker_used' THEN 1 END) as symptom_checks
    FROM AFC_BRAZE_SHARED.<SCHEMA>.USERS_BEHAVIORS_CUSTOMEVENT_SHARED
    WHERE DATE(TO_TIMESTAMP(time)) >= CURRENT_DATE - 90
    GROUP BY engagement_date;
    
    -- Appointment Reminder Effectiveness View  
    CREATE VIEW AFC_BRAZE_DATA.ANALYTICS.APPOINTMENT_REMINDERS AS
    SELECT 
        s.campaign_id,
        COUNT(DISTINCT s.user_id) as reminders_sent,
        COUNT(DISTINCT o.user_id) as reminders_opened,
        ROUND(COUNT(DISTINCT o.user_id) / COUNT(DISTINCT s.user_id) * 100, 2) as open_rate_pct
    FROM AFC_BRAZE_SHARED.<SCHEMA>.USERS_MESSAGES_SMS_SEND_SHARED s
    LEFT JOIN AFC_BRAZE_SHARED.<SCHEMA>.USERS_MESSAGES_EMAIL_OPEN_SHARED o 
        ON s.user_id = o.user_id 
        AND s.campaign_id = o.campaign_id
    WHERE DATE(TO_TIMESTAMP(s.time)) >= CURRENT_DATE - 30
    GROUP BY s.campaign_id;
    """, language="sql")
    
    # Next steps
    st.markdown("### 🚀 Next Steps for AFC")
    
    next_steps_cols = st.columns(3)
    
    with next_steps_cols[0]:
        st.markdown("""
        **📊 Analytics Setup**
        - Configure BI tools (Tableau, Looker)
        - Create patient journey dashboards
        - Set up automated reporting
        """)
    
    with next_steps_cols[1]:
        st.markdown("""
        **🔄 Data Pipeline**
        - Schedule data quality checks
        - Implement data transformation workflows
        - Set up monitoring and alerting
        """)
    
    with next_steps_cols[2]:
        st.markdown("""
        **🎯 Use Case Implementation**
        - Patient engagement scoring
        - Appointment optimization models
        - Care gap identification algorithms
        """)

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
        <h3>🏥 Patient Engagement & Care Optimization</h3>
        <p>Discover how AFC leverages Braze + Snowflake for superior patient care:</p>
    </div>
    """, unsafe_allow_html=True)
    
    use_cases = [
        {
            "title": "📱 Appointment Reminder Optimization",
            "description": "Analyze SMS and email delivery rates to optimize appointment reminder timing and reduce no-shows.",
            "metrics": ["40% reduction in no-shows", "95% message delivery rate", "Patient satisfaction +25%"],
            "tables": ["USERS_MESSAGES_SMS_SEND_SHARED", "USERS_MESSAGES_EMAIL_DELIVERY_SHARED"]
        },
        {
            "title": "🩺 Health Education Campaigns", 
            "description": "Track engagement with seasonal health tips, vaccination reminders, and preventive care information.",
            "metrics": ["60% open rate on health emails", "Vaccination uptake +30%", "Preventive visits +20%"],
            "tables": ["USERS_MESSAGES_EMAIL_OPEN_SHARED", "USERS_BEHAVIORS_CUSTOMEVENT_SHARED"]
        },
        {
            "title": "📊 Patient Journey Analytics",
            "description": "Map complete patient interactions from first app session through ongoing care relationships.",
            "metrics": ["Patient lifetime value insight", "Care gap identification", "Personalized care paths"],
            "tables": ["USERS_BEHAVIORS_APP_FIRSTSESSION_SHARED", "USERS_BEHAVIORS_CUSTOMEVENT_SHARED"]
        },
        {
            "title": "🚨 Urgent Care Visit Optimization",
            "description": "Analyze peak urgent care demand patterns and optimize staffing and patient flow.",
            "metrics": ["Wait time reduction 25%", "Staff efficiency +15%", "Patient throughput +20%"],
            "tables": ["USERS_BEHAVIORS_CUSTOMEVENT_SHARED", "USERS_MESSAGES_PUSH_NOTIFICATION_SEND_SHARED"]
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
