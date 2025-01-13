
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
    """Analyze resume using Gemini API."""
    import google.generativeai as genai
    
    # Configure the API
    GEMINI_API_KEY = "AIzaSyCa2JbASfiR8nGPT5BV09K9N43H002daEI"
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Define the prompt with explicit instructions to return JSON
    prompt = f"""You must respond with ONLY a valid JSON object, no other text.
    Analyze this resume and return a JSON object with exactly this structure:
    {{
        "Primary job role": "string" (don't add words like student or studying),
        "Key skills": ["string"],
        "Years of experience": "string",
        "Key achievements": ["string"],
        "Preferred job titles": ["string"]
    }}

    Resume text:
    {resume_text}
    """

    try:
        # Generate response
        response = model.generate_content(prompt)
        
        
        
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove any markdown code block indicators if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        response_text = response_text.strip()
        
        # Debug: Print cleaned response
        st.write("Cleaned Response:", response_text)
        
        # Parse JSON
        parsed_response = json.loads(response_text)
        return parsed_response

    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        st.write("Failed to parse response:", response_text)
        return {}
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return {}


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
    st.title("🎯 JobHunt Ai")
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
