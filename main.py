# import streamlit as st
# import PyPDF2
# import openai
# import requests
# import json


# jobhuntkey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWpsa2JhcnNoaWthckBnbWFpbC5jb20iLCJwZXJtaXNzaW9ucyI6InVzZXIifQ.7I9IZ-edUtm6byVMa8oIBMUmHjErhe4D0fff-mBppIY"
# st.set_page_config(page_title="Smart Job Matcher", layout="wide")

# if 'resume_analysis' not in st.session_state:
#     st.session_state.resume_analysis = None
# if 'jobs' not in st.session_state:
#     st.session_state.jobs = None

# def extract_text_from_pdf(pdf_file):
#     """Extract text from uploaded PDF file"""
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text

# def analyze_resume(resume_text):
#     """Analyze resume using OpenAI API"""
#     openai.api_key = "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"

#     system_prompt = """You are a professional resume analyzer. Your task is to analyze resumes and return information in valid JSON format.
#     Always ensure your response is a properly formatted JSON object with the exact structure specified."""

#     user_prompt = f"""Analyze this resume and return a JSON object with exactly this structure:
#     {{
#         "Primary job role": "string"(dont add words like student or studying),
#         "Key skills": ["string"],
#         "Years of experience": "string",
#         "Key achievements": ["string"],
#         "Preferred job titles": ["string"]
#     }}

#     Resume text:
#     {resume_text}
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-4-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )

#     return json.loads(response.choices[0].message['content'])

# def fetch_theirstack_jobs(job_title, location=None, page=1):
#     """Alternative implementation using different endpoint"""

#     url = "https://api.theirstack.com/v1/jobs"
#     headers = {
#         "Authorization": f"Bearer {jobhuntkey}",
#         "Content-Type": "application/json"
#     }

#     # Query parameters
#     params = {
#         "q": job_title,
#         "page": page,
#         "per_page": 10
#     }

#     if location:
#         params["location"] = location

#     try:
#         response = requests.get(url, headers=headers, params=params)

#         st.text(f"Response Content: {response.text[:500]}...")  # First 500 chars

#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching TheirStack jobs: {str(e)}")
#         return {"jobs": []}

# def main():
#     st.title("🎯 Smart Job Matcher")
#     st.write("Upload your resume and let AI find the perfect job matches for you!")

#     # File upload
#     uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

#     # Location filter
#     location = st.text_input("Enter location (optional)", "")

#     if uploaded_file:
#         with st.spinner("Analyzing your resume..."):
#             # Extract text from PDF and analyze
#             resume_text = extract_text_from_pdf(uploaded_file)
#             if not st.session_state.resume_analysis:
#                 st.session_state.resume_analysis = analyze_resume(resume_text)

#             col1, col2 = st.columns(2)

#             with col1:
#                 st.subheader("📄 Resume Analysis")
#                 st.write("**Primary Role:**", st.session_state.resume_analysis['Primary job role'])
#                 st.write("**Years of Experience:**", st.session_state.resume_analysis['Years of experience'])
#                 st.write("**Key Skills:**")
#                 for skill in st.session_state.resume_analysis['Key skills']:
#                     st.write(f"- {skill}")

#             with col2:
#                 st.subheader("🏆 Key Achievements")
#                 for achievement in st.session_state.resume_analysis['Key achievements']:
#                     st.write(f"• {achievement}")

#             st.subheader("🔍 Job Matches")

#             if st.button("Find Matching Jobs"):
#                 with st.spinner("Searching for jobs..."):
#                     # Fetch jobs from TheirStack
#                     jobs_response = fetch_theirstack_jobs(
#                         st.session_state.resume_analysis['Primary job role'],
#                         location
#                     )
#                     st.session_state.jobs = jobs_response.get('jobs', [])

#             if st.session_state.jobs:
#                 for job in st.session_state.jobs:
#                     with st.container():
#                         st.markdown("""---""")
#                         st.markdown(f"### {job['title']}")
#                         st.write(f"**Company:** {job['company_name']}")
#                         st.write(f"**Location:** {job.get('location', 'Remote/Not specified')}")
#                         st.write(f"**Employment Type:** {job.get('employment_type', 'Not specified')}")

#                         # Show job description in an expander
#                         with st.expander("Show Job Description"):
#                             st.write(job.get('description', 'No description available'))

#                         # Add apply button
#                         if st.button(f"Apply for {job['title']}", key=job['id']):
#                             st.markdown(f"[Apply Now]({job['url']})")

#                 # Pagination controls
#                 col1, col2, col3 = st.columns([1, 2, 1])
#                 with col2:
#                     if st.button("Load More Jobs"):
#                         current_page = len(st.session_state.jobs) // 10 + 1
#                         more_jobs = fetch_theirstack_jobs(
#                             st.session_state.resume_analysis['Primary job role'],
#                             location,
#                             page=current_page
#                         )
#                         if more_jobs.get('jobs'):
#                             st.session_state.jobs.extend(more_jobs['jobs'])

# if __name__ == "__main__":
#     main()

import streamlit as st
import PyPDF2
import openai
import requests
import json
from datetime import datetime

# Add RapidAPI configuration
RAPIDAPI_KEY = "c5ac9d5e75msh0ad1714a2260ef0p12bea4jsn6b409a897083"  # Replace with your RapidAPI key

if 'resume_analysis' not in st.session_state:
    st.session_state.resume_analysis = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = None

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text):
    """Analyze resume using OpenAI API"""
    openai.api_key = "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"

    system_prompt = """You are a professional resume analyzer. Your task is to analyze resumes and return information in valid JSON format.
    Always ensure your response is a properly formatted JSON object with the exact structure specified."""

    user_prompt = f"""Analyze this resume and return a JSON object with exactly this structure:
    {{
        "Primary job role": "string"(dont add words like student or studying),
        "Key skills": ["string"],
        "Years of experience": "string",
        "Key achievements": ["string"],
        "Preferred job titles": ["string"]
    }}

    Resume text:
    {resume_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return json.loads(response.choices[0].message['content'])


def fetch_jobs_rapidapi(job_title, location=None, page=1):
    """Fetch jobs using RapidAPI JSearch"""
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    query = job_title
    if location:
        query += f" in {location}"

    params = {
        "query": query,
        "page": str(page),
        "num_pages": "1"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return {"data": []}

def display_job_card(job):
    """Display a single job posting in a card format"""
    with st.container():
        st.markdown("---")

        # Job header
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {job['job_title']}")
            st.markdown(f"**Company:** {job['employer_name']}")
            location_str = f"{job.get('job_city', '')}, {job.get('job_country', '')}"
            st.markdown(f"**Location:** {location_str.strip(', ')}")

            if job.get('job_min_salary') and job.get('job_max_salary'):
                st.markdown(f"**Salary Range:** ${job['job_min_salary']:,} - ${job['job_max_salary']:,}")

        with col2:
            st.markdown(f"**Type:** {job.get('job_employment_type', 'Not specified')}")
            if job.get('job_posted_at_datetime_utc'):
                posted_date = datetime.strptime(job['job_posted_at_datetime_utc'][:10], '%Y-%m-%d')
                st.markdown(f"**Posted:** {posted_date.strftime('%Y-%m-%d')}")

        # Job details
        with st.expander("Show Job Description"):
            st.markdown(job.get('job_description', 'No description available'))

            # Highlights section
            if job.get('job_highlights'):
                if 'Qualifications' in job['job_highlights']:
                    st.markdown("**Required Qualifications:**")
                    for qual in job['job_highlights']['Qualifications']:
                        st.markdown(f"- {qual}")

                if 'Benefits' in job['job_highlights']:
                    st.markdown("**Benefits:**")
                    for benefit in job['job_highlights']['Benefits']:
                        st.markdown(f"- {benefit}")

        # Apply button
        if job.get('job_apply_link'):
            st.markdown(f"[Apply Now]({job['job_apply_link']})")

def main():
    st.title("🎯 Smart Job Matcher")
    st.write("Upload your resume and let AI find the perfect job matches for you!")

    # File upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    # Location filter
    location = st.text_input("Enter location (optional)", "")

    if uploaded_file:
        with st.spinner("Analyzing your resume..."):
            # Extract text from PDF and analyze
            resume_text = extract_text_from_pdf(uploaded_file)
            if not st.session_state.resume_analysis:
                st.session_state.resume_analysis = analyze_resume(resume_text)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📄 Resume Analysis")
                st.write("**Primary Role:**", st.session_state.resume_analysis['Primary job role'])
                st.write("**Years of Experience:**", st.session_state.resume_analysis['Years of experience'])
                st.write("**Key Skills:**")
                for skill in st.session_state.resume_analysis['Key skills']:
                    st.write(f"- {skill}")

            with col2:
                st.subheader("🏆 Key Achievements")
                for achievement in st.session_state.resume_analysis['Key achievements']:
                    st.write(f"• {achievement}")

            # Job search section
            st.subheader("🔍 Job Matches")

            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                employment_type = st.selectbox(
                    "Employment Type",
                    ["All", "FULLTIME", "PARTTIME", "CONTRACTOR", "INTERN"]
                )
            with col2:
                date_posted = st.selectbox(
                    "Date Posted",
                    ["All", "Today", "3 days", "Week", "Month"]
                )

            if st.button("Find Matching Jobs"):
                with st.spinner("Searching for jobs..."):
                    jobs_response = fetch_jobs_rapidapi(
                        st.session_state.resume_analysis['Primary job role'],
                        location
                    )

                    if jobs_response and 'data' in jobs_response:
                        jobs = jobs_response['data']

                        # Apply filters
                        if employment_type != "All":
                            jobs = [job for job in jobs 
                                   if job.get('job_employment_type', '').upper() == employment_type]

                        st.success(f"Found {len(jobs)} matching jobs")

                        # Display jobs
                        for job in jobs:
                            display_job_card(job)

                        # Pagination
                        if len(jobs) >= 10:
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col2:
                                if st.button("Load More Jobs"):
                                    current_page = len(jobs) // 10 + 1
                                    more_jobs = fetch_jobs_rapidapi(
                                        st.session_state.resume_analysis['Primary job role'],
                                        location,
                                        page=current_page
                                    )
                                    if more_jobs.get('data'):
                                        jobs.extend(more_jobs['data'])
                    else:
                        st.error("No jobs found matching your criteria")

if __name__ == "__main__":
    main()