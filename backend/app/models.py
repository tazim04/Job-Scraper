from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    def __init__(self, title, company, location, link, salary=None, 
                 date_posted=None, description=None, workplaceType=None, 
                 employmentType=None, cardId=None,
                 matching_analysis=None, summary=None, score=None, recommendation=None
                 ):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.salary = salary
        self.date_posted = date_posted
        self.description = description
        self.workplaceType = workplaceType
        self.employmentType = employmentType
        self.cardId = cardId
        self.matching_analysis = matching_analysis
        self.summary = summary
        self.score = score
        self.recommendation = recommendation
        
    def to_dict(self):
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'link': self.link,
            'salary': self.salary,
            'date_posted': self.date_posted,
            'description': self.description,
            'workplaceType': self.workplaceType,
            'employmentType': self.employmentType,
            'matching_analysis': self.matching_analysis,
            'summary': self.summary,
            'score': self.score,
            'recommendation': self.recommendation
        } 