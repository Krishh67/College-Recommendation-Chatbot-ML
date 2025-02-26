import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
from pandasql import sqldf
import google.generativeai as genai
import random
import base64
from html import escape
import warnings
import os

# Set the environment variable for suppressing logs
os.environ['STREAMLIT_LOG_LEVEL'] = 'error'

# Suppress the specific deprecation warning
warnings.filterwarnings("ignore")
# Your existing code here

# Alternatively, you can set up warnings filtering directly
warnings.filterwarnings("ignore", category=DeprecationWarning)

# CSS Styles
st.markdown("""
<style>
    .college-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .ranking-badge {
        background: #e8f4ff;
        color: #1a73e8;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    .stat-item {
        padding: 12px;
        background: #f8f9fa;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Configure Google Gemini API
genai.configure(api_key='YOUR API KEY')


def render_college_card(college):
    """Create HTML card for a college"""
    return f"""
    <div class="college-card">
        <div class="card-header">
            <h3>🏛️ {(college['university_name'])}</h3>
            <div class="ranking-badge">
                🌍 #{(str(college.get('Global_Ranking', 'N/A')))}
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-item">
                📍 <div><strong>Location</strong><br>{college.get('Country', 'N/A')}</div>
            </div>
            <div class="stat-item">
                💰 <div><strong>Avg Package</strong><br>{college.get('Average_Placement_(LPA)[5-19.94]', 'N/A')} LPA</div>
            </div>
            <div class="stat-item">
                🎯 <div><strong>Acceptance Rate</strong><br>{college.get('Acceptance_Rate(%)', 'N/A')}%</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Aptitude Tests</strong><br>{college.get('Aptitude_Test_Requirements', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Tuition Fees</strong><br>{college.get('Tuition_Fees (USD)[10076-49933]', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Language Requirements</strong><br>{college.get('Language_Requirements', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Application deadline</strong><br>{college.get('Application Deadlines', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Currency used</strong><br>{college.get('Currency Used', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Letter of Recommendation</strong><br>{college.get('Recommendation Letters Requirement', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Degree_Recognition</strong><br>{college.get('Degree_Recognition', 'N/A')}</div>
            </div>
        </div>
    </div>
    """

# Load dataset
df = pd.read_csv('finalmark1_sample.csv')

def add_logo():
    try:
        with open("download.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" width="120">
            </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo image missing!")

def sidebar_slideshow():
    with st.sidebar:
        st.header("Featured Colleges")
        if 'slide_index' not in st.session_state:
            st.session_state.slide_index = 0
        
        
        
        colleges_with_images = [
            "Harvard university",
            "Stanford university",
            "Cambridge_university",
            "Princeton University",
            "Massachusetts Institute of Technology"
        ]

        # Select one college from the list (not randomly from all colleges)
        college = random.choice(colleges_with_images)
        #college = random.choice(df['university_name'].tolist())
        try:
            st.image(f"assets/{college.replace(' ', '_')}.jpg", 
                    caption=college, use_column_width=True)
        except:
            st.image("assets/placeholder.jpg", caption=college)

        if st.button("Next College"):
            st.session_state.slide_index += 1
def sidebar2():
    with st.sidebar:
        st.header("Featured Colleges")
        if 'slide_index' not in st.session_state:
            st.session_state.slide_index = 0
        
        college = random.choice(df['university_name'].tolist())
        try:
            st.image(f"assets/{college.replace(' ', '_')}.jpg", 
                    caption=college, use_column_width=True)
        except:
            st.image("assets/placeholder.jpg", caption=college)

        if st.button("Next College"):
            st.session_state.slide_index += 1

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'main_page'
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Main page
if st.session_state.page == 'main_page':
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        lottie_animation = json.load(open("Animation - 1740082275350.json"))
        st_lottie(lottie_animation, height=300, width=300)
        
    if st.button("FIND MY CAMPAS ➡️", use_container_width=True):
        st.session_state.page = 'code_page'
        st.rerun()

# Code page
elif st.session_state.page == 'code_page':
    add_logo()
    sidebar_slideshow()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask about colleges (e.g. 'SHOW TOP COLLEGES IN CANADA WITH AVERAGE PACKAGE MORE THAN 10LPA')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.spinner("Finding best options..."):
            try:
                # Generate SQL query
                schema = {
                    'columns': df.columns.tolist(),
                    'sample_data': df.head(3).to_dict(orient='records')
                }
                print(schema)
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"""
                    Convert to SQL: {prompt}
                    - Columns available: {schema['columns']}
                    - Always select [world_rank,university_name,Average_Placement_(LPA)[5-19.94],Country,Global_Ranking,Aptitude_Test_Requirements,Acceptance_Rate(%),Tuition_Fees (USD)[10076-49933],Degree_Recognition,Recommendation Letters Requirement,Currency Used,Application Deadlines,Language_Requirements] in any condition 
                    - Look mostly noun as conditions and there can be more than 1 conditions so use "AND" operator
                    - Table: df
                    - Return only SQL query 
                """)
                
                sql_query = response.text.split('```sql')[-1].split('```')[0].strip()
                print(sql_query)
                results = sqldf(sql_query, {'df': df})
                print(results)
                # Build HTML response
                response_html = """
                <div class="scroll-container">
                    <h2 style="color: #1a237e; margin-bottom: 1rem;">🎓 Recommended Colleges ({count} Found)</h2>
                """.format(count=len(results))

                for _, row in results.iterrows():
                    college_data = df[df['university_name'] == row['university_name']].iloc[0].to_dict()
                    
                    # Data validation
                    ranking = college_data.get('Global_Ranking')
                    ranking = ranking if pd.notna(ranking) else 'N/A'
                    
                    package = college_data.get('Average_Placement_(LPA)[5-19.94]', 'N/A')
                    package = f"{package} LPA" if pd.notna(package) else 'N/A'
                    
                    acceptance = college_data.get('Acceptance_Rate(%)', 'N/A')
                    acceptance = f"{acceptance}%" if pd.notna(acceptance) else 'N/A'
                    print(sql_query,'\n',results)
                     # Build response
                response_html = f"""
                <div class="main-container">
                    <div style="margin: 2rem 0;">
                        <h2 style="color: #1a237e;">🎓 Found {len(results)} Matching Colleges</h2>
                        {"".join([render_college_card(row.to_dict()) for _, row in results.iterrows()])}
                    </div>
                </div>
                """


                # Display response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_html
                })
                with st.chat_message("assistant"):
                    st.markdown(response_html, unsafe_allow_html=True)

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)

    # Back button
    if st.button("⬅️ Back to Main"):
        st.session_state.page = 'main_page'
        st.session_state.messages = []
        st.rerun()