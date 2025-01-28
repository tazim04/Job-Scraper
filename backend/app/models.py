from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    def __init__(self, title, company, location, link, salary=None, 
                 date_posted=None, description=None, location_type=None,
                 job_type=None,matching_analysis=None, summary=None, 
                 key_technologies=None, key_skills=None, score=None, recommendations=None
                 ):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.salary = salary
        self.date_posted = date_posted
        self.description = description
        
        # from llama
        self.summary = summary
        self.key_technologies= key_technologies
        self.key_skills= key_skills
        self.location_type = location_type # remote, in-person, hybrid
        self.job_type = job_type # Internship, full-time, part-time, etc
        self.matching_analysis = matching_analysis
        self.score = score
        self.recommendations = recommendations
        
    def to_dict(self):
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'link': self.link,
            'salary': self.salary,
            'date_posted': self.date_posted,
            'description': self.description,
            
            # from llama
            'summary': self.summary,
            'key_technologies': self.key_technologies,
            'key_skills': self.key_skills,
            'location_type': self.location_type, # remote, in-person, hybrid
            'job_type': self.job_type, # Internship, full-time, part-time, etc
            'matching_analysis': self.matching_analysis,
            'score': self.score,
            'recommendations': self.recommendations
        } 