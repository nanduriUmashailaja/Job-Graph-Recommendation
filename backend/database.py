import os
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable

URI = "bolt+s://db-9f94f265.bravo.databases.cognodb.com"
USERNAME = "cognodb"
PASSWORD = "1b0a600b53593d649f3ec325352afa20"

class JobGraphDB:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
            print("✓ Connected to CognoDB successfully!")
        except Exception as e:
            print(f"✗ Connection error: {e}")
            raise

    def get_all_people(self):
        """Get all candidates"""
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p.name as name, p.experience_years as experience")
            return [dict(record) for record in result]

    def get_all_jobs(self):
        """Get all jobs"""
        with self.driver.session() as session:
            result = session.run("MATCH (j:Job) RETURN j.title as title, j.salary as salary")
            return [dict(record) for record in result]

    def get_job_recommendations(self, person_name):
        """Find jobs where person has most of the required skills"""
        query = """
        MATCH (p:Person {name: $name})-[:HAS_SKILL]->(skill:Skill)<-[:REQUIRES]-(job:Job)
        WITH job, COUNT(skill) as matched_skills
        MATCH (job)-[:REQUIRES]->(s:Skill)
        WITH job, matched_skills, COUNT(s) as total_required
        RETURN job.title as job_title, matched_skills, total_required, 
               ROUND(100.0 * matched_skills / total_required) as match_percentage
        ORDER BY match_percentage DESC
        """
        with self.driver.session() as session:
            result = session.run(query, name=person_name)
            return [dict(record) for record in result]

    def get_candidates_for_job(self, job_title):
        """Find candidates ranked by required skills match"""
        query = """
        MATCH (job:Job {title: $title})-[:REQUIRES]->(required_skill:Skill)<-[:HAS_SKILL]-(person:Person)
        WITH person, job, COUNT(required_skill) as matched_count
        MATCH (job)-[:REQUIRES]->(skill:Skill)
        WITH person, job, matched_count, COUNT(skill) as total_required
        RETURN person.name as candidate_name, person.experience_years as experience,
               matched_count as skills_matched, total_required,
               ROUND(100.0 * matched_count / total_required) as match_percentage
        ORDER BY match_percentage DESC, experience DESC
        """
        with self.driver.session() as session:
            result = session.run(query, title=job_title)
            return [dict(record) for record in result]

    def close(self):
        self.driver.close()