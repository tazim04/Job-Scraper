export type JobResult = {
  title: string;
  company: string;
  location: string;
  date_posted: string;
  description: string;
  job_type: string;
  key_skills: {
    skill: string;
    has_skill: boolean;
  }[];
  key_technologies: {
    technology: string;
    has_technology: boolean;
  }[];
  link: string;
  location_type: string;
  matching_analysis: string;
  score: number;
  recommendations: string[];
  salary: string;
  summary: string;
  error?: any;
  reason?: any;
};

export default JobResult;
