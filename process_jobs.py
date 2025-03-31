import json

JOBS_FILE = "D:\\solutyics.chatbot\\data\\job.json"

def process_jobs():
    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    job_chunks = []
    for job in jobs:
        job_text = f"""
        Job Title: {job['title']}
        Location: {job['location']}
        Employment Type: {job['employment_type']}
        Description: {job['description']}
        Responsibilities: {", ".join(job['responsibilities'])}
        Requirements: {", ".join(job['requirements'])}
        Salary Range: {job['salary_range']}
        """
        job_chunks.append(job_text.strip())

    return job_chunks

if __name__ == "__main__":
    jobs = process_jobs()
    print(f"Processed {len(jobs)} job openings.")
