export interface PersonalInfo {
  name: string;
  title: string;
  email: string;
  location: string;
  summary: string;
}

export interface Experience {
  id: string;
  role: string;
  company: string;
  dates: string;
  description: string;
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  dates: string;
  gpa: string;
}

export interface Certificate {
  id: string;
  name: string;
}

export type Skills = {
  id: string;
  category: string;
  technologies: string;
};

export type AdditionalKnowledgeInterests = {
  id: string,
  description: string
}


export type WorkExperience = {
  id: string;
  position: string;
  company: string;
  location?: string;
  dates: string;
  description: string[];
}

export interface ResumeData {
  personalInfo: PersonalInfo;
  workExperience?: WorkExperience []; // actual work experience
  experience: Experience[];          // Projects only, not actual work experience
  education: Education[];
  certificates: Certificate[];
  skills: Skills[];
  additionalinfo?: AdditionalKnowledgeInterests [];
  font: string;
  theme: 'dark' | 'light';
}
