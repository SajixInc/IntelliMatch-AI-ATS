import streamlit as st
import requests

import pybase64
import io
from dotenv import load_dotenv

import pymongo
from pymongo import MongoClient
import os 

import streamlit as st
import os
from PIL import Image
import PyPDF2 as pdf
import google.generativeai as genai
import time
from database import x
import webbrowser

# Define the endpoints
SUBSCRIBE_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/Otpgenerate/"
OTP_VERIFICATION_ENDPOINT = "http://45.79.121.132:8001/SubscribeAndFeedback/OtpVerfication/"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'login' not in st.session_state:
    st.session_state.login = False

# Function to subscribe and generate OTP
def subscribe(email):
    api = SUBSCRIBE_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    mail = {"emailid": email}
    r = requests.post(api, json=mail, headers=headers)
    data = r.json()
    
    if data.get("Status") == 200:
        st.session_state.otp_sent = True
        st.success(f"OTP sent successfully to {email}")
    else:
        st.error("Failed to subscribe. Please try again.")

# Function to verify OTP
def verify_otp(email, otp):
    api = OTP_VERIFICATION_ENDPOINT
    headers = {'Content-Type': 'application/json'}
    data = {"emailid": email, "otp": otp}
    r = requests.post(api, json=data, headers=headers)
    response = r.json()
    
    return response.get("Status") == 200

if st.session_state.login == False:
    # Streamlit UI
    st.title("Unlock Free Access to IntelliMatch-AI-ATS!")
    
    if not st.session_state.logged_in:
        email = st.text_input("Enter your email:", value=st.session_state.email)
        if st.button("Subscribe"):
            if email:
                st.session_state.email = email
                subscribe(email)
            else:
                st.warning("Please enter a valid email address.")
    
        if st.session_state.otp_sent:
            otp_input = st.text_input('Enter OTP:', key='otp_input')
            if st.button('Resend OTP'):
                subscribe(st.session_state.email)
            if st.button('Login'):
                if otp_input:
                    
                    api = OTP_VERIFICATION_ENDPOINT
                    headers = {'Content-Type': 'application/json'}
                    data = {"emailid": email, "otp": otp_input}
                    r = requests.post(api, json=data, headers=headers)
                    response = r.json()
                    if response.get("Status") == 200:
                        st.success("Successfully logged in!")
                        st.session_state.login = True
                    else:
                        st.error("Invalid OTP. Please try again.")
                else:
                    st.error("Please enter OTP.")
    else:
        st.success("You are already logged in.")
    
else: #Loggedin successfully
    load_dotenv()

    username = x['default']
    try:
        y=x['default']['CLIENT']
        myclient = pymongo.MongoClient(f"mongodb://{username['CLIENT']['username']}:{username['CLIENT']['password']}@{username['CLIENT']['host']}:27017/")
        print(myclient)
        
    except:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        print(myclient)
        

    mydb = myclient["lifeeazydb_prod"]
    collection = mydb["collect_job_role"]


    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def get_gemini_response(input):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text

    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ''  # Ensure text is not None
        return text

    ## ------- Streamlit app setup ---------
    st.set_page_config(page_title="ATSPro", page_icon="📑", layout = 'wide')

    with open( "styles/main.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    custom_sidebar_style = """
        <style>
            /* Style for the sidebar container */
            .sidebar-container {
                height: 500px; /* Adjust the height as needed */
                overflow-y: auto; /* Enable vertical scroll */
                padding: 20px; /* Add padding for better spacing */
            }

            /* Style for the sidebar title */
            .sidebar-title {
                font-size: 24px;
                color: #333333;
                margin-bottom: 10px;
            }

            /* Style for the sidebar subheader */
            .sidebar-subheader {
                font-size: 18px;
                color: #666666;
                margin-bottom: 15px;
            }

            /* Style for the sidebar text */
            .sidebar-text {
                font-size: 16px;
                color: #444444;
                margin-bottom: 10px;
            }

            /* Style for the sidebar note */
            .sidebar-note {
                font-size: 14px;
                color: #777777;
                margin-bottom: 10px;
            }
        </style>
    """

    # Display custom CSS style in the sidebar
    st.sidebar.markdown(custom_sidebar_style, unsafe_allow_html=True)

    # Wrap sidebar content in a <div> with custom styles
    st.sidebar.markdown("""
        <div class="sidebar-container">
            <div class="sidebar-title">ATSPro: The ATS-Conquering Companion</div>
            <div class="sidebar-subheader">Cross the ATS Hurdle: Unlock Your Career Potential with Precision and Insight</div>
            <div class="sidebar-text">
                <p><em>ATSPro</em> is your strategic ally in mastering the <strong>Applicant Tracking System (ATS)</strong> challenge, powered by the advanced capabilities of <em>Google Gemini Pro</em>. This ATS Expert System is crafted to refine and align your resume with precision, ensuring it resonates with both the ATS algorithms and human recruiters' expectations.</p>
                <p>It is designed to have a fixed height with a vertical scroll if the content exceeds the height.</p>
            </div>
            <div class="sidebar-note">Note: <em>ATSPro</em> can make mistakes. Consider checking important information.</div>
        </div>
    """, unsafe_allow_html=True)


    st.sidebar.write("""
        <style>
            /* Style for the buttons */
            .custom-button {
                background-color: #3CA2DB; 
                border: none;
                color: white;
                padding: 8px 15px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 8px;
            }

            /* Style when hovering over the button */
            .custom-button:hover {
                background-color: #3CA2DB;
            }

            /* Style for the star icon */
            .star-icon {
                margin-right: 5px;
                margin-botton: 5px
                fill: #FFFFFF; /* icon color */
            }
            #rating-popup {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        /* Add other styles for the popup window */
        }
        </style>

        <div style="position: fixed; bottom: 10px;">
            <button class="custom-button" style="margin-right: 10px;"><a href="https://docs.vivifyhealthcare.com/overview/solutions/intellimatch-ai-ats" style="color: inherit; text-decoration: none;">FAQ's</a></button>
            <button class="custom-button" onclick="openRatingChat()"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 16 16" class="star-icon" role="img" aria-label="Favorite Icon"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.287 1.333c.32-.91 1.68-.91 2 0l1.163 3.314c.094.268.305.481.585.557l3.43.748c.93.203 1.298 1.327.617 1.98l-2.78 2.524c-.235.214-.345.533-.292.85l.66 3.407c.09.465-.426.828-.85.582l-3.45-1.82c-.265-.14-.574-.14-.84 0l-3.45 1.82c-.426.224-.94-.117-.85-.582l.66-3.407c.053-.317-.057-.636-.292-.85L1.945 7.532c-.68-.653-.313-1.777.617-1.98l3.43-.748c.28-.076.49-.289.585-.557L7.287 1.333zM8 11.265l-2.486 1.31.473-2.44-2.02-1.837 2.638-.232 1.394-2.37 1.393 2.37 2.638.232-2.02 1.837.473 2.44L8 11.265z" fill="#FFF"/></svg>Rate this page</button>
        </div>
    """, unsafe_allow_html=True)

    # # Define the function to handle the star rating
    # def handle_rating(rating):
    #     # You can handle the rating here, such as sending it to your backend
    #     st.write(f"User rated with {rating} stars")

    # # Display the sidebar buttons
    # col1, col2 = st.sidebar.columns([2, 3])

    # with col1:
    #     if st.button("FAQ's"):
    #         faq_url = "https://docs.vivifyhealthcare.com/overview/solutions/intellimatch-ai-ats"
    #         st.markdown(f"[FAQ's]({faq_url})")

    # with col2:
    #     if st.button("Rate this page"):
    #         st.write("How would you rate this page?")
    #         # Display the star rating buttons in a row
    #         for i in range(1, 6):
    #             if st.button(label='\u2605' * i, on_click=handle_rating, args=(i,), key=f"star_button_{i}"):
    #                 break  # Stop the loop if a star button is clicked

    #Set BAckground Image

    def set_bg_image(image_file):
        with open(image_file, "rb") as file:
            # Use base64 to encode the image file
            encoded_image = pybase64.b64encode(file.read()).decode()

        # Set the background using CSS styles
        css_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """

        st.markdown(css_style, unsafe_allow_html=True)

    set_bg_image("background.JPG")


    image_path = "output (2).png"  # Replace "output.png" with the path to your image file
    st.image(image_path, width=1000)  # Adjust the width as needed

    # Role input

    role = st.text_input("**Job Role**")

    if role != '':
        st.write(f":black[You entered **{role}** as your role.]")
        # Save the job role to the MongoDB collection
        job_role_data = {'role_name': role}
        collection.insert_one(job_role_data)
        st.success(f"Job Role '{role}' saved successfully!")
    # else:
    #     st.write("Enter a Job Role")


    # Initialize session state variables for button clicks
    if 'submit1_clicked' not in st.session_state:
        st.session_state['submit1_clicked'] = False
    if 'submit2_clicked' not in st.session_state:
        st.session_state['submit2_clicked'] = False
    if 'submit3_clicked' not in st.session_state:
        st.session_state['submit3_clicked'] = False
    if 'submit4_clicked' not in st.session_state:
        st.session_state['submit4_clicked'] = False
    if 'submit5_clicked' not in st.session_state:
        st.session_state['submit5_clicked'] = False

    # Define button click callbacks to set state
    def on_submit1_clicked():
        st.session_state['submit1_clicked'] = True

    def on_submit2_clicked():
        st.session_state['submit2_clicked'] = True

    def on_submit3_clicked():
        st.session_state['submit3_clicked'] = True

    def on_submit4_clicked():
        st.session_state['submit4_clicked'] = True

    def on_submit5_clicked():
        st.session_state['submit5_clicked'] = True


    # Define column widths
    column_widths = [3, 2]

    # Display columns
    col6, col7 = st.columns(column_widths)

    # Content in the first column
    with col6:
        jd = st.text_area("**Job Description**")

    # Content in the second column
    with col7:
        uploaded_file = st.file_uploader("**Resume**", type="pdf", help="Please upload a pdf")    


    col1, col2, col3, col4, col5 = st.columns(5)


    # Define paths to your icon images

    icon_paths = {
        "Summary": "summeryicon.png",
        "Match": "percentageicon.png",
        "Suggestions": "suggestionsicon.png",
        "Customization Tips": "customizeicon.png",
        "Interview Prep Guide": "interviewicon.png"
    }

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.image(icon_paths["Summary"], width=30)
        submit1 = st.button("Summary", key="submit1", on_click=on_submit1_clicked, type="primary")
    with col2:
        st.image(icon_paths["Match"], width=30)
        submit2 = st.button("Match", key="submit2", on_click=on_submit2_clicked, type="primary")
    with col3:
        st.image(icon_paths["Suggestions"], width=30)
        submit3 = st.button("Suggestions", key="submit3", on_click=on_submit3_clicked, type="primary")
    with col4:
        st.image(icon_paths["Customization Tips"], width=30)
        submit4 = st.button("Customization Tips", key="submit4", on_click=on_submit4_clicked, type="primary")
    with col5:
        st.image(icon_paths["Interview Prep Guide"], width=30)
        submit5 = st.button("Interview Prep Guide", key="submit5", on_click=on_submit5_clicked, type="primary")


    # Process button clicks
    if submit1 and st.session_state['submit1_clicked']:
        if len(role) > 0:
            if uploaded_file is not None:
                text = input_pdf_text(uploaded_file)
                if len(jd) > 0:
                    with st.spinner('Please Wait..'):
                        prompt1 = f"""
                        You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Analyze the provided resume and job description (JD). Provide a detailed analysis (200-300 words) of how the resume aligns with the JD, highlighting key areas of strength, relevant experiences, and qualifications. Discuss any notable achievements or skills that are particularly well-matched to the job requirements.
                        
                        Here is the resume content : {text}
                        Here is the job description : {jd}
                        Your Response Should have the following structure
                        Example:
                        
                        Note: Only Mention and Analyze the content of the provided resume text. Make sure Nothing additional is added outside the provided text 
                        
                        Resume Analysis and Alignment with Job Description:

                        Overview: 
                        The resume presents a strong background in software engineering, with a particular emphasis on full-stack development and cloud technologies.
                        
                        Strengths:
                        - Technical Proficiency: Proficient in key programming languages such as Python, JavaScript, and Java, aligning well with the job's technical requirements.
                        - Project Experience: Showcases several projects that demonstrate the ability to design, develop, and deploy scalable software solutions, mirroring the JD's emphasis on hands-on experience.
                        
                        Relevant Experiences: (Highlight only the things that are present in the resume.)
                        - Lead Developer Role: Led a team in developing a SaaS application using microservices architecture, directly relevant to the job's focus on leadership and microservices.
                        - Cloud Solutions Architect: Experience in designing cloud infrastructure on AWS, aligning with the JD's requirement for cloud computing skills.
                        
                        """

                        response = get_gemini_response(prompt1)
                    st.write(response)  # Use st.write to display the response
                else:
                    st.error("No job description provided.")
                
            else:
                st.error("No job description provided.")
                st.error("Resume Not Uploaded.")
        else:
            st.error("No Job Role Specified")
            st.error("No job description provided.")
            st.error("Resume Not Uploaded.")  

    if submit2 and st.session_state['submit2_clicked']:
        if len(role) > 0:
            if uploaded_file is not None:
                text = input_pdf_text(uploaded_file)
                if len(jd) > 0:
                    with st.spinner('Please Wait..'):
                        prompt2 = f"""
                        You are a professional and experienced ATS(Application Tracking System) focused exclusively on the {role} field. Your task is to evaluate the resume strictly based on the provided job description and resume content. It is critical to only identify and list the keywords and phrases that have a direct match between the resume and the JD. Highlight any crucial keywords or skills required for the job that are absent in the resume. Based on your analysis, provide a percentage match.

                        Important: Your analysis must strictly adhere to the content provided below. Do not infer or add any keywords, skills, or technologies not explicitly mentioned in these texts. Re-evaluate the texts to ensure accuracy. Recheck before you provide your response

                        Resume Content: {text}
                        Job Description: {jd}
                        
                        Never provide anything which is neither present in resume content nor job description.
                        
                        Output should strictly follow this structure:

                        Percentage Match: [Provide percentage]

                        Matched Keywords:
                        - Skills: [List only the matched skills found in both the job description and resume content. recheck before you provide your response]
                        - Technologies: [List only the matched technologies found in both the job description and resume. Recheck before you provide your response]
                        - Methodologies: [List only the matched methodologies found in both the job description and resume. Recheck before you provide your response]

                        Missing Keywords:
                        - [List the skills or technologies crucial for the role found in the job description but not in the resume. Recheck before you provide your response]

                        Final Thoughts:
                        - [Provide a brief assessment focusing on the alignment, matched keywords, missing elements, and percentage match. Reinforce the instruction to only mention elements present in the provided texts. Recheck before you provide your response]

                        
                        """

                        response = get_gemini_response(prompt2)
                    st.subheader("Percentage Match Analysis")
                    st.write(response)  # Use st.write to display the response
                else:
                    st.error("No job description provided.")
                
            else:
                st.error("No job description provided.")
                st.error("Resume Not Uploaded.")
        else:
            st.error("No Job Role Specified")
            st.error("No job description provided.")
            st.error("Resume Not Uploaded.")

    if submit3 and st.session_state['submit3_clicked']:
        if len(role) > 0:
            if uploaded_file is not None:
                text = input_pdf_text(uploaded_file)
                if len(jd) > 0:
                    with st.spinner('Please Wait..'):
                        prompt3 = f"""
                        You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Based on the analysis of the resume and the job description, suggest specific improvements and additions to the candidate's skill set (200-300 words). Identify areas where the candidate falls short and recommend actionable steps or resources for acquiring or enhancing the necessary skills. Highlight the importance of these skills in the context of the targeted job role.
                        
                        Here is the resume content : {text}
                        Here is the job description : {jd}
                        Your Response Should have the following structure
                        Example:
                        
                        Note: Only Mention and Analyze the content of the provided resume text. Make sure Nothing additional is added outside the provided text 
                        
                        Skills Improvement and Addition Suggestions:

                        To further align your resume with the job requirements and the evolving trends in software engineering, consider the following improvements:

                        Expand Knowledge in Emerging Technologies:
                        - Dive into Machine Learning and Big Data Analytics; consider online courses or projects that demonstrate practical application.
                        - Familiarize yourself with Blockchain Technology, given its growing impact on secure and decentralized systems.
                        
                        Enhance Cloud Computing Skills:
                        - Gain deeper expertise in cloud services beyond AWS, such as Microsoft Azure or Google Cloud Platform, to showcase versatility.
                        - Strengthen Soft Skills:
                        Leadership and project management skills are highly valued; consider leading more projects or taking courses in Agile and Scrum methodologies.
                        """

                        response = get_gemini_response(prompt3)
                    st.subheader("Skills Improvement Suggestions")
                    st.write(response)
                else:
                    st.error("No job description provided.")
            else:
                st.error("No job description provided.")
                st.error("Resume Not Uploaded.")
        else:
            st.error("No Job Role Specified")
            st.error("No job description provided.")
            st.error("Resume Not Uploaded.")

    if submit4 and st.session_state['submit4_clicked']:
        if len(role) > 0:
            if uploaded_file is not None:
                text = input_pdf_text(uploaded_file)
                if len(jd) > 0:
                    with st.spinner('Please Wait..'):
                        prompt4 = f"""
                        You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Review the resume's bullet points in light of the job description. Provide targeted suggestions on how to edit existing bullet points to better align with the job requirements. Focus on enhancing clarity, relevance, and impact by incorporating keywords from the JD and emphasizing achievements and skills that are most pertinent to the job.
                        
                        Here is the resume content : {text}
                        Here is the job description : {jd}
                        Your Response Should have the following structure
                        Example:
                        
                        Note: Only Mention and Analyze the content of the provided resume text. Make sure Nothing additional is added outside the provided text 
                        
                        Resume Customization Tips for Better Alignment with Job Description:

                        Tailor Bullet Points:
                        - Current: "Developed a web application using React and Node.js."
                        - Revised: "Engineered a scalable web application using React and Node.js, incorporating microservices architecture to enhance modularity and deployability, directly supporting team objectives in agile development environments."
                        
                        Highlight Specific Achievements:
                        - Current: "Designed cloud infrastructure for various projects."
                        - Revised: "Strategically designed and deployed robust cloud infrastructure on AWS for 3 enterprise-level projects, achieving a 20% improvement in deployment efficiency and cost reduction."
                        
                        Incorporate Missing Keywords:
                        If you have experience with Machine Learning, add a bullet point like: "Implemented machine learning    algorithms to automate data processing tasks, resulting in a 30% reduction in processing times."
                        """

                        response = get_gemini_response(prompt4)
                    st.subheader("Customization Tips")
                    st.write(response)
                else:
                    st.error("No job description provided.")
            else:
                st.error("No job description provided.")
                st.error("Resume Not Uploaded.")
        else:
            st.error("No Job Role Specified")
            st.error("No job description provided.")
            st.error("Resume Not Uploaded.")

    if submit5 and st.session_state['submit5_clicked']:
        if len(role) > 0:
            if uploaded_file is not None:
                text = input_pdf_text(uploaded_file)
                if len(jd) > 0:
                    with st.spinner('Please Wait..'):
                        prompt5 = f"""
                        You are a professional and experienced ATS(Application Tracking System) with a deep understanding of {role} fields. Analyze the provided resume and job description (JD). Generate a set of interview questions and suggested answers tailored to this specific context. The questions should be designed to explore the candidate's technical skills, experiences, and personal attributes relevant to the role, as described in the JD and evidenced in the resume. Provide 5 technical interview questions (1 easy question, 2 medium questions, 3 hard questions) focusing on the key skills and technologies mentioned in the JD and resume. The technical questions should sound specific and technical. Additionally, provide 5 HR interview questions (1 easy question, 2 medium questions, 3 hard questions) that probe into the candidate's behavioral traits, problem-solving abilities, and cultural fit for the organization. For each question, include a detailed sample answer that highlights how the candidate can effectively showcase their relevant skills, experiences, and achievements from their resume in response to the job requirements outlined in the JD."

                        Here is the resume content : {text}
                        Here is the job description : {jd}
                        Instructions for Response:

                        Technical Questions:
                        Create questions that are directly related to the technical skills and experiences mentioned in the JD and resume.
                        Ensure questions cover a range of difficulties (easy, medium, hard) and are relevant to real-world scenarios the candidate might face in the role.
                        
                        HR Questions:
                        Formulate questions that assess cultural fit, teamwork, leadership, and resilience.
                        Questions should invite responses that allow the candidate to demonstrate their problem-solving approach, adaptability, and growth mindset.
                        
                        Suggested Answers:
                        Provide comprehensive sample answers for each question, guiding the candidate on how to integrate their specific experiences and achievements from the resume.
                        Highlight how each answer can align with the expectations set forth in the JD, showcasing the candidate's suitability for the role.
                        
                        Your Response Should have the following structure
                        
                        Technical Interview Questions:
                        
                        Question1: (Question here)
                        
                        Answer1: (Answer here)
                        
                        Similarly all other questions.
                        
                        HR Interview Questions:
                        
                        Question1: (Question here)
                        
                        Answer1: (Answer here)
                        
                        Similarly all other questions.
                        """

                        response = get_gemini_response(prompt5)
                    st.subheader("Interview Preperation Guide ")
                    st.write("Here are some sample Technical and HR interview questions which will help you in answering different questions faced in the interviews.")
                    st.write(response)
                else:
                    st.error("No job description provided.")
            else:
                st.error("No job description provided.")
                st.error("Resume Not Uploaded.")
        else:
            st.error("No Job Role Specified")
            st.error("No job description provided.")
            st.error("Resume Not Uploaded.")
