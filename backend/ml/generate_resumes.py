import psycopg2
import random
from faker import Faker

fake = Faker()

# --------------------------
# DATABASE CONFIG
# --------------------------
conn = psycopg2.connect(
    dbname="ai_resume_dg",
    user="postgres",
    password="user",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# --------------------------
# DOMAIN SKILLS
# --------------------------
domains = {
    "Data Scientist": [
        "Python", "Pandas", "NumPy", "Scikit-learn",
        "Machine Learning", "Data Visualization",
        "SQL", "Statistics", "Deep Learning"
    ],
    "ML Engineer": [
        "TensorFlow", "PyTorch", "Model Deployment",
        "Feature Engineering", "Docker", "MLOps",
        "Python", "Cloud ML"
    ],
    "Backend Python Developer": [
        "Python", "Flask", "Django",
        "REST APIs", "PostgreSQL",
        "Microservices", "Docker"
    ],
    "Frontend React Developer": [
        "React", "JavaScript", "HTML", "CSS",
        "Redux", "UI Design", "Responsive Design"
    ],
    "DevOps Engineer": [
        "CI/CD", "Jenkins", "Docker",
        "Kubernetes", "AWS", "Linux", "Terraform"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "GCP",
        "Cloud Architecture", "Networking",
        "Infrastructure as Code"
    ],
    "Cybersecurity Analyst": [
        "Network Security", "Penetration Testing",
        "SIEM", "Threat Analysis",
        "Cryptography", "Firewall"
    ],
    "Full Stack Developer": [
        "JavaScript", "React", "Node.js",
        "Express", "MongoDB", "SQL",
        "API Development"
    ]
}

TOTAL_PER_DOMAIN = 30
insert_count = 0

all_skills_flat = []
for skill_list in domains.values():
    all_skills_flat.extend(skill_list)

for domain, skills_list in domains.items():
    for _ in range(TOTAL_PER_DOMAIN):

        name = fake.name()
        email = fake.email()
        years = random.randint(1, 10)

        # 4 primary skills
        primary_skills = random.sample(skills_list, 4)

        # 2 noise skills from other domains
        other_skills = random.sample(
            [s for s in all_skills_flat if s not in skills_list], 2
        )

        combined_skills = primary_skills + other_skills
        random.shuffle(combined_skills)

        skills_text = ", ".join(combined_skills)

        resume_text = f"""
        {name} is a {domain} with {years} years of professional experience.
        Experienced in {skills_text}.
        Worked on enterprise-grade systems, collaborated with cross-functional teams,
        and contributed to scalable production deployments.
        Strong analytical thinking and ability to adapt to new technologies.
        """

        cursor.execute("""
    INSERT INTO resumes (name, email, skills, resume_text, domain)
    VALUES (%s, %s, %s, %s, %s)
""", (name, email, skills_text, resume_text, domain))

        insert_count += 1

conn.commit()
cursor.close()
conn.close()

print(f"Inserted {insert_count} resumes successfully!")