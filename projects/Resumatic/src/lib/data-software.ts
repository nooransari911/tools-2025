import type { ResumeData } from './types';
import { nanoid } from 'nanoid';



// full
export const initialResumeDatav1: ResumeData = {
  personalInfo: {
    name: 'Noor Ansari',
    title: 'Student',
    email: 'mohammadna71@gmail.com',
    location: 'Pune, MH',
    summary: 'Aspiring software engineer with experience in working with cloud services and AI models. I have developed AI applications for processing documents. I have strong foundation in Python development and cloud services integration.',
  },

  skills: [
    {
      id: nanoid(),
      category: 'Domains',
      technologies: 'Cloud Architecture, AI & Data, DevOps & Automation'
    },
    {
      id: nanoid(),
      category: 'Languages',
      technologies: 'C, Python, JavaScript'
    },
    {
      id: nanoid(),
      category: 'Cloud Computing',
      technologies: 'AWS (S3, EC2, Lambda), GCP'
    },
    {
      id: nanoid(),
      category: 'AI & Data',
      technologies: 'LLMs Integration, Document Processing, Data Visualization'
    },
    {
      id: nanoid(),
      category: 'Development & Tools',
      technologies: 'Linux, Shell Scripting, Hugo (Static Site Generator), REST APIs'
    }
  ],

  experience: [
    {
      id: nanoid(),
      role: 'Dynamic Resume Generation Engine',
      company: '',
      dates: 'Jul 2025',
      description:
`• Objective: To eliminate manual formatting and guarantee a robust, pixel-perfect layout.
• Engineered a Next.js application to programmatically generate resume PDFs.
• Designed a clean, modern layout for optimal clarity
• Decoupled data from presentation, guaranteeing layout integrity.
• Additional features: use of different resume profiles and fonts, one-click PDF export.`,
    },
    {
      id: nanoid(),
      role: 'AI Document Processing in Python',
      company: '',
      dates: 'Jun 2025',
      description:
`• Objective: To automate and streamline processing of documents with AI
• Developed AI application to process documents with Claude and Gemini models
• Architected as a highly modular system with clean seperation of concerns to maximize maintainability and extensibility
• Built on a foundation of robust error handling, comprehensive logging, & dynamic configuration for resilient operation and maintainable system
• Automated workflow: context preparation, versioned outputs, automatic file updates from generated content
• Special features: parallel processing, interactive chat, supports different providers, structured output with flexible schema options, multimodal capability, sourcing prompts from files, integrated DynamoDB for logs`,
    },
    {
      id: nanoid(),
      role: 'Personal Website',
      company: '',
      dates: 'May 2025',
      description:
`• Tech stack: Static site generator (Hugo), AWS (S3, CloudFront, Lambda, API Gateway)
• Developed dynamic redirects and page migrations, SEO optimizations, automated search indexing and cache refresh, invalidations
• Custom program to create a new page with boilerplate metadata and front matter`,
    },
    {
        id: nanoid(),
        role: 'Automated Backup Solution with AWS S3',
        company: '',
        dates: 'Nov 2024',
        description: 
`• Developed backup solution with S3
• Bucket lifecycle policy, incremental nature, git-integrated, highly automated
• Analyzed logs using SQL queries to get operational insights`,
    },
    {
        id: nanoid(),
        role: 'Bank Statement Visualization',
        company: '',
        dates: 'Sep 2024',
        description: 
`• Loaded bank statement file (CSV) into GCP BigQuery
• Developed SQL queries to analyze spending trends
• Generate interactive visualizations (pie charts, bar charts, tables)`,
    }
  ],
  education: [
    {
      id: nanoid(),
      institution: 'I2IT',
      degree: 'Bachelor of Engineering, Electronics & Telecommunication',
      dates: 'Dec 2026',
      gpa: '',
    },
  ],
  certificates: [
    { id: nanoid(), name: 'AWS Academy Cloud Foundations' },
    { id: nanoid(), name: 'AWS Academy Cloud Architecting' }
  ],
  font: 'Inter',
  theme: 'dark'
};




// streamlined, condensed, highly refined
export const initialResumeData: ResumeData = {
  personalInfo: {
    name: 'Noor Ansari',
    title: 'Student',
    email: 'mohammadna71@gmail.com',
    location: 'Pune, MH',
    summary: 'Aspiring software engineer with experience in working with cloud services and AI models. I have developed AI applications for processing documents. I have strong foundation in Python development and cloud services integration.',
  },

  skills: [
    {
      id: nanoid(),
      category: 'Domains',
      technologies: 'Cloud Architecture, AI & Data, DevOps & Automation'
    },
    {
      id: nanoid(),
      category: 'Languages',
      technologies: 'C, Python, JavaScript'
    },
    {
      id: nanoid(),
      category: 'Cloud Computing',
      technologies: 'AWS (S3, EC2, Lambda), GCP'
    },
    {
      id: nanoid(),
      category: 'AI & Data',
      technologies: 'LLMs Integration, Document Processing, Data Visualization'
    },
    {
      id: nanoid(),
      category: 'Development & Tools',
      technologies: 'Linux, Shell Scripting, Hugo (Static Site Generator), REST APIs'
    }
  ],

  // workExperience: [
  //   {
  //     id: nanoid(),
  //     position: 'Team Member',
  //     company: 'Major Project: AXI-APB Bridge (VLSI Domain)',
  //     //location: 'Pune, MH',
  //     dates: 'Jul 2025 - Present',
  //     description: [
  //       "Part of 3-member team for our final year project",
  //       "Project involves connecting various subsystems within a processor",
  //       "Design the core architecture and protocol logic and coordinate team efforts.",
  //       "Pioneer the initial research and proof-of-concept work that establishes the project foundation for the team.",
  //       "Mentor teammates through design challenges and code reviews."
  //      ]
  //   }
  // ],

  experience: [
    {
      id: nanoid(),
      role: 'Dynamic Resume Generation Engine',
      company: '',
      dates: 'Jul 2025',
      description:
`•  Objective: To eliminate manual formatting and guarantee a robust, pixel-perfect layout.
•  Engineered a Next.js application to generate resume PDFs.
•  Designed a clean, modern layout for optimal clarity
•  Decoupled data from presentation, guaranteeing layout integrity.`,
    },
    {
      id: nanoid(),
      role: 'AI Document Processing in Python',
      company: '',
      dates: 'Jun 2025',
      description:
`•  Objective: To automate document processing using latest AI models
•  Architected as a highly modular system with clean seperation of concerns to maximize maintainability and extensibility
•  Automated workflow: loading files, versioned outputs, automatic file updates
•  Special features: parallel processing, interactive chat, supports different providers, flexible output options
•  Integrated robust error handling, logging, & dynamic configuration`,
    },
    {
      id: nanoid(),
      role: 'Personal Website',
      company: '',
      dates: 'May 2025',
      description:
`•  Tech stack: Static site generator (Hugo), AWS (S3, Cloudfront, Lambda)
•  Developed dynamic redirects and page migrations, SEO optimizations, automated search indexing and cache refresh, invalidations
•  Created custom program to automate creation of new page`,
    },
    {
        id: nanoid(),
        role: 'Automated Backup Solution with AWS S3',
        company: '',
        dates: 'Nov 2024',
        description: 
`•  Developed backup solution with S3
•  Bucket lifecycle policy, incremental nature, git-integrated, highly automated
•  Analyzed logs using SQL queries to get operational insights`,
    },
    {
        id: nanoid(),
        role: 'Bank Statement Visualization',
        company: '',
        dates: 'Sep 2024',
        description: 
`•  Loaded bank statement file (CSV) into GCP BigQuery
•  Developed SQL queries to analyze spending trends
•  Generate interactive visualizations (pie charts, bar charts, tables)`,
    }
  ],
  education: [
    {
      id: nanoid(),
      institution: 'I2IT',
      degree: 'Bachelor of Engineering, Electronics & Telecommunication',
      dates: 'Dec 2026',
      gpa: '',
    },
  ],
  certificates: [
    { id: nanoid(), name: 'AWS Academy Cloud Foundations' },
    { id: nanoid(), name: 'AWS Academy Cloud Architecting' }
  ],

  font: 'Inter',
  theme: 'dark'
};
