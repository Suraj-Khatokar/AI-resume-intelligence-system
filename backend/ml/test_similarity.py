from similarity_engine import compute_similarity_with_all_resumes

job_description = """
Looking for a Python backend developer with experience in Flask, SQL and Docker.
"""

results = compute_similarity_with_all_resumes(job_description)

for r in results:
    print(r)