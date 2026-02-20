from similarity_engine import compute_similarity_with_all_resumes

job_description = """We are hiring a Data Scientist with strong experience in Python,
Pandas, NumPy, Scikit-learn, Machine Learning, Deep Learning,
Statistics, Data Visualization, and SQL.
The candidate should be comfortable building predictive models,
performing feature engineering, and working with large datasets.
Experience with experimentation, model evaluation, and deployment is preferred.
"""

results = compute_similarity_with_all_resumes(job_description)

for r in results:
    print(r)