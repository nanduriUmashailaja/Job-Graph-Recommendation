# Job Graph Recommender

A graph database application that matches candidates with jobs using AI-powered skill matching.

## Use Case

This application solves the talent-matching problem by leveraging a **graph database** to model the complex relationships between:
- **Candidates** and their **Skills**
- **Jobs** and their **Skill Requirements**
- **Companies** and their **Postings**

### Why a Graph Database?

Graph databases excel at relationship queries. Traditional relational databases require expensive joins to find candidates matching job requirements. Our graph queries use **multi-hop traversals** to instantly:
1. Find jobs for a candidate based on skill overlap
2. Rank candidates for a job by skill match + experience
3. Discover skill gaps preventing recommendations

This is inherently a graph problem — graphs answer it elegantly.

## Data Model

**Nodes:**
- `Person`: name, experience_years
- `Skill`: name
- `Job`: title, salary
- `Company`: name, industry

**Relationships:**
- `HAS_SKILL`: Person has a skill
- `REQUIRES`: Job requires a skill
- `POSTED_BY`: Job posted by company

## Key Queries

### Multi-hop Query 1: Job Recommendations
```cypher
MATCH (p:Person {name: 'Alice'})-[:HAS_SKILL]->(skill:Skill)<-[:REQUIRES]-(job:Job)
WITH job, COUNT(skill) as matched_skills
MATCH (job)-[:REQUIRES]->(s:Skill)
WITH job, matched_skills, COUNT(s) as total_required
RETURN job.title, ROUND(100.0 * matched_skills / total_required) as match_percentage
```

### Multi-hop Query 2: Best Candidates for Job
```cypher
MATCH (job:Job {title: 'Senior Python Developer'})-[:REQUIRES]->(skill:Skill)<-[:HAS_SKILL]-(person:Person)
WITH person, COUNT(skill) as matched_count
MATCH (job)-[:REQUIRES]->(s:Skill)
RETURN person.name, ROUND(100.0 * matched_count / COUNT(s)) as match_percentage
ORDER BY match_percentage DESC, person.experience_years DESC
```

## Tech Stack

- **Database**: CognoDB (Neo4j-compatible graph database)
- **Backend**: Flask + Python Neo4j driver
- **Frontend**: React
- **Hosting**: TBD

## Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- CognoDB Cloud account (free tier)

### Installation

1. **Backend Setup**
```bash
cd backend
pip install flask flask-cors python-dotenv neo4j
python database.py  # Test connection
python app.py       # Start Flask on http://127.0.0.1:5000
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start           # Start React on http://localhost:3000
```

3. **CognoDB Setup**
   - Create free instance at https://console.cognodb.com
   - Update credentials in `backend/database.py`

## Features

✓ Multi-hop graph queries for smart matching
✓ Skill-based candidate ranking
✓ Experience-weighted recommendations
✓ Real-time search and filtering
✓ Match percentage visualization

## Screenshots

[Frontend showing candidates and jobs with match percentages]

## API Endpoints

- `GET /api/candidates` - All candidates
- `GET /api/jobs` - All jobs
- `GET /api/recommendations/<name>` - Jobs for candidate
- `GET /api/candidates-for-job/<title>` - Candidates for job

## Future Enhancements

- Add more candidates/jobs
- Skill similarity matching (Python ≈ Cython)
- Salary negotiation insights
- Career path recommendations
