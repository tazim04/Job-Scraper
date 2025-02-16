export type JobResult = {
  title: string;
  company: string;
  location: string;
  date_posted: string;
  description: string;
  job_type: string;
  key_skills: string[];
  key_technologies: string[];
  link: string;
  location_type: string;
  matching_analysis: string;
  score: number;
  recommendations: string[];
  salary: string | null;
  summary: string;
};

export default JobResult;
