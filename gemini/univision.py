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


# Configure the page
st.set_page_config(
    page_title="UNIVISION",
    layout="wide"
)

# Set the environment variable for suppressing logs
os.environ['STREAMLIT_LOG_LEVEL'] = 'error'

# Suppress the specific deprecation warning
warnings.filterwarnings("ignore")
# Your existing code here

# Alternatively, you can set up warnings filtering directly
warnings.filterwarnings("ignore", category=DeprecationWarning)
st.markdown("""
<style>
    .college-card {
        background: #1a1a1a;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #2d2d2d;
        color: white;
        transition: transform 0.2s ease;
    }
    
    .college-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.1);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #333;
    }

    .ranking-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9em;
        letter-spacing: 0.5px;
    }

    .stats-grid {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-top: 1.2rem;
    }

    .stat-item {
        padding: 12px 20px;
        background: #2d2d2d;
        border-radius: 10px;
        color: white;
        min-width: 180px;
        border: 1px solid #3d3d3d;
    }

    .stat-item h4 {
        color: #4ecdc4;
        margin: 0 0 8px 0;
        font-size: 0.9em;
    }

    .stat-item p {
        margin: 0;
        font-weight: 600;
        font-size: 1.1em;
    }

    .university-name {
        font-size: 1.8em;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.5px;
    }

    .program-name {
        color: #4ecdc4;
        font-size: 1.2em;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)
# Configure Google Gemini API
api_key = st.secrets["general"]["GOOGLE_GEMINI_API_KEY"]

# Configure Google Gemini API
genai.configure(api_key=api_key)


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
                📋 <div><strong>Aptitude Tests</strong><br>{college.get('Aptitude_Test_Requirements', 'N/A')}</div>
            </div>
            <div class="stat-item">
                💵 <div><strong>Tuition Fees</strong><br>{college.get('Tuition_Fees (USD)[10076-49933]', 'N/A')}</div>
            </div>
            <div class="stat-item">
                🗣️ <div><strong>Language Requirements</strong><br>{college.get('Language_Requirements', 'N/A')}</div>
            </div>
            <div class="stat-item">
                🔜 <div><strong>Application Deadlines</strong><br>{college.get('Application_Deadlines', 'N/A')}</div>
            </div>
            <div class="stat-item">
                💱 <div><strong>Currency used</strong><br>{college.get('Currency Used', 'N/A')}</div>
            </div>
            <div class="stat-item">
                🎓 <div><strong>Scholarship Program</strong><br>{college.get('Scholarship_Program', 'N/A')}</div>
            </div>
            <div class="stat-item">
                💱 <div><strong>Course Flexibility</strong><br>{college.get('Course_Flexibility', 'N/A')}</div>
            </div>
            <div class="stat-item">
                🏫  <div><strong>Placement Rate (%)</strong><br>{college.get('Internship_Placement_Rate(%)', 'N/A')}</div>
            </div>
            <div class="stat-item">
                📝 <div><strong>Top Hiring Industries</strong><br>{college.get('Top_Hiring_Industries', 'N/A')}</div>
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
df = pd.read_csv('assets/finalmark1_sample.csv')

def add_logo():
    try:
        with open("assets/image1.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{data}" width="150">
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
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        

        

        st.markdown(
    """
    <style>
    /* Hide the default Streamlit header */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Main app container */
    [data-testid="stAppViewContainer"] {
        background-color: black !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: black !important;
    }
    
    /* Footer */
    footer {visibility: hidden;}
    
    /* Add the fadeIn animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)
    # Custom title section
        st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-family: 'Arial Black', sans-serif; 
                   font-size: 2.8em; 
                   color: linear-gradient(90deg, #ff6b6b, #4ecdc4);
                   text-transform: uppercase;
                   letter-spacing: 3px;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                   animation: fadeIn 1.5s ease-in;">
            <span style="color: #ff6b6b;">🌍UNI</span>
            <span style="color: #4ecdc4;">VISION</span>
        </h1>
        <p style="font-size: 1.2em; color: #666; margin-top: -10px;">
            AI-Powered University Matching System
        </p>
        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
            <div style="width: 7px; height: 2px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4);"></div>
            <div style="width: 15px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 15px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 7px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

        # Now create your custom title section
        

        # The rest of your Streamlit app content can go below...
        #st.write("")
        #st.write("Here is where you can continue building your page.")




        lottie_animation = json.load(open("assets/c.json"))
        st_lottie(lottie_animation, height=450, width=650)
        
    if st.button("FIND MY DREAM CAMPAS 🌍➡️", use_container_width=True):
        st.session_state.page = 'code_page'
        st.rerun()

# Code page
elif st.session_state.page == 'code_page':
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-family: 'Arial Black', sans-serif; 
                   font-size: 2.8em; 
                   color: linear-gradient(90deg, #ff6b6b, #4ecdc4);
                   text-transform: uppercase;
                   letter-spacing: 3px;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                   animation: fadeIn 1.5s ease-in;">
            <span style="color: #ff6b6b;">🌍UNI</span>
            <span style="color: #4ecdc4;">VISION</span>
        </h1>
        <p style="font-size: 1.2em; color: #666; margin-top: -10px;">
            AI-Powered University Matching System
        </p>
        <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
            <div style="width: 7px; height: 2px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4);"></div>
            <div style="width: 15px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 30px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 15px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
            <div style="width: 7px; height: 2px; background: linear-gradient(90deg, #4ecdc4, #ff6b6b);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
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
                    - Always select [world_rank,university_name,Average_Placement_(LPA)[5-19.94],Country,Global_Ranking,Aptitude_Test_Requirements,Acceptance_Rate(%),Tuition_Fees (USD)[10076-49933],Degree_Recognition,Recommendation Letters Requirement,Currency Used,Application_Deadlines,Language_Requirements,Top_Hiring_Industries,Internship_Placement_Rate(%),Course_Flexibility,Scholarship_Program] in any condition 
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
