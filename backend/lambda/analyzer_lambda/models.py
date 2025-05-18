from dataclasses import dataclass
from typing import Optional, List, Dict, Union

@dataclass
class Job:
    def __init__(self, title: str, company: str, location: str, link: str,
                 salary: Optional[str] = None, date_posted: Optional[str] = None,
                 description: Optional[str] = None, location_type: Optional[str] = None,
                 job_type: Optional[str] = None, matching_analysis: Optional[str] = None,
                 summary: Optional[str] = None, key_technologies: Optional[List[Dict[str, Union[str, bool]]]] = None,
                 key_skills: Optional[List[Dict[str, Union[str, bool]]]] = None,
                 score: Optional[Union[int, float]] = None, recommendations: Optional[List[str]] = None):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.date_posted = date_posted
        self.description = description

        # From LLM
        self.summary = summary
        self.salary = salary
        self.key_technologies = key_technologies
        self.key_skills = key_skills  # List of dicts with "skill" and "has_skill"
        self.location_type = location_type
        self.job_type = job_type
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
            'summary': self.summary,
            'key_technologies': self.key_technologies,
            'key_skills': self.key_skills,
            'location_type': self.location_type,
            'job_type': self.job_type,
            'matching_analysis': self.matching_analysis,
            'score': self.score,
            'recommendations': self.recommendations
        }
