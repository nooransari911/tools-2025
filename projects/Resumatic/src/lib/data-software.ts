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
    //summary: 'Aspiring software engineer with experience in working with cloud services and AI models. I have developed AI applications for processing documents. I have strong foundation in Python development and cloud services integration.',
    //summary: 'Aspiring backend engineer with a passion for building applications from scratch. I have hands-on experience in developing REST APIs and server-side logic using Python (Flask) and TypeScript (NestJS). My work is supported by a strong foundation in cloud platforms (AWS) and databases (both SQL and NoSQL). Eager to apply my skills to solve real-world engineering challenges',

    // summary: 'Aspiring backend engineer with a passion for building applications from scratch. I have hands-on experience in developing REST APIs and server-side logic using Python (Flask) and TypeScript (NestJS). My work is supported by a strong foundation in cloud platforms (AWS) and databases (both SQL and NoSQL). Eager to apply my skills to solve real-world engineering challenges',

    // summary: "Aspiring data scientist with a passion for extracting insights from complex datasets and building intelligent data processing systems.\n\nI have hands-on experience in developing predictive models, automating data workflows, and creating interactive visualizations using Python and SQL. My work demonstrates proficiency in statistical modeling, building AI-based processing platforms, and translating raw data into actionable business intelligence.\n\nEager to apply my analytical skills and technical expertise to solve real-world data challenges and drive data-driven decision making."
    // summary: 'Backend engineer with hands-on experience building high-performance, concurrent systems. Designed multi-threaded pipelines optimized for throughput and reliability. Proficient in Spring Boot for developing REST APIs, dependency injection, and application configuration.\n\nMy work is supported by a strong foundation in databases (SQL and NoSQL) and cloud platforms (AWS). Eager to apply my Java development skills to solve complex engineering challenges',
    // summary: 'Backend Engineer with a strong foundation in Java and SQL. Developed a multi-threaded data processing application that leverages concurrency to improve throughput. Leveraged the Spring Framework for dependency injection (IoC) and to manage application components.\n\nEager to apply my problem-solving abilities to build reliable and scalable backend systems.',
    // Data science: summary: 'I build high-throughput data systems and leverage AI to solve complex problems.\n\n I have engineered a scalable, multi-threaded system that processes data at over 300 MB/sec. I\'ve also designed an AI-based platform to automate file processing.\n\nI am eager to apply my skills in data engineering and system design to tackle real-world challenges.'
    summary: 'Backend Developer with a strong foundation in Java. Developed a high-performance pipeline for verifying data integrity that achieves throughput of over 300 MB/sec.\n\nEager to apply my problem-solving abilities to build reliable and scalable backend systems.',
  },

  //coverLetter: "I'm excited to apply for the backend internship at Hue Logics. My hands-on experience building REST APIs with modern backend frameworks (FastAPI, NestJS) and deep AWS expertise align well with your tech stack requirements. I also have practical experience with NoSQL databases (DynamoDB).\n\nWhile I have limited experience in Go and MongoDB, my projects demonstrate a strong foundation in modular, maintainable server-side development. I look forward to contributing to your team.",

  skillsReference: [
    {
      id: nanoid(),
      category: 'Domains',
      technologies: 'AI, Data Engineering, System Design'
    },
    {
      id: nanoid(),
      category: 'Languages',
      // technologies: 'Python, JavaScript, TypeScript'
      technologies: 'Java, Python'
    },
    {
      id: nanoid(),
      category: 'Cloud Computing',
      technologies: 'AWS (S3, EC2, Lambda, API Gateway)'
      // category: 'Cloud Platforms',
      // technologies: 'BigQuery, Athena'
    },
    {
      id: nanoid(),
      category: "Databases",
      technologies: "Postgres, DynamoDB (NoSQL)"
    },
    {
      id: nanoid(),
      category: 'AI & Data Engineering',
      // technologies: 'LLMs Integration, Document Processing, Data Visualization'
      technologies: 'Statistical Models, AI Platforms, Data Visualization'
    },
    {
      id: nanoid(),
      category: 'Java smth smth',
      // technologies: 'LLMs Integration, Document Processing, Data Visualization'
      technologies: 'Smth smth on java/jvm'
    },
    // {
    //   id: nanoid(),
    //   category: 'Development & Tools',
    //   technologies: 'Linux, Shell Scripting, Hugo (Static Site Generator), REST APIs, HTTP'
    // },
    // {
    //   id: nanoid(),
    //   category: 'Web Development',
    //   technologies: 'React, Next.js, Tailwind, Flask, Fast API'
    // }
  ],


  skills: [
    // {
    //   id: nanoid(),
    //   category: 'Domains',
    //   technologies: 'Data Engineering, AI, System Design'
    // },
    {
      id: nanoid(),
      category: 'Domains',
      technologies: 'Backend Development, Data Engineering'
    },
    // {
    //   id: nanoid(),
    //   category: 'Data Engineering',
    //   technologies: 'High-Throughput Pipelines, Asynchronous Data Processing'
    // },
    // {
    //   id: nanoid(),
    //   category: 'Data Science & AI',
    //   technologies: 'Statistical Modeling, AI Integration, Data Visualization'
    // },
    {
      id: nanoid(),
      category: 'Languages',
      technologies: 'Java, SQL'
    },
    {
      id: nanoid(),
      category: 'Core Java',
      technologies: 'Concurrent, Stream, Security'
    },
    {
      id: nanoid(),
      category: 'Frameworks',
      technologies: 'Spring Boot (Core, Web), Java AWS SDK'
    },
    {
      id: nanoid(),
      category: 'Databases',
      technologies: 'Postgres, AWS DynamoDB'
    },
    // {
    //   id: nanoid(),
    //   category: 'Cloud',
    //   technologies: 'AWS (S3, Lambda, API Gateway)'
    // },
    // {
    //   id: nanoid(),
    //   category: 'Developer Tools',
    //   technologies: 'Git, Linux Shell'
    // },
  ],

  workExperience: [
    {
      id: nanoid(),
      position: 'Backend Development Intern',
      company: 'Big Impact',
      // location: 'Pune, MH',
      dates: 'Sep 2025 - Present',
      description: [
        "Developed a full-stack business review platform on Next.js",
        "Engineered an intelligent Redux store to guarantee zero data loss in OAuth flow",
        "Unified server-side (SSR) and client-side states into a single Redux store",
        "Developed a service-controller architecture to enforce a strict separation of concerns",
      ]
    }
  ],

  experience: [
    //     {
    //       id: nanoid (),
    //       role: "Predicting Compound Interest",
    //       company: '',
    //       dates: "Aug 2025",
    //       description: '',
    //       descriptionLs: [
    // 'Engineered a linear model to approximate compound interest',
    // 'Tuned for upto 10% p.a. rate and upto 10 year timeframe',
    // 'Achieved accuracy upto 3% under target range',
    //       ],
    //     },
    //     {
    //       id: nanoid(),
    //       role: 'Dynamic Resume Generation Engine',
    //       company: '',
    //       dates: 'Jul 2025',
    //       description:
    // `•  Objective: To eliminate manual formatting and guarantee a robust, pixel-perfect layout.
    // •  Engineered a Next.js application to generate resume PDFs.
    // •  Designed a clean, modern layout for optimal clarity
    // •  Decoupled data from presentation, guaranteeing layout integrity
    // •  Live switching between fonts and themes for enhanced user experience`,
    //     },
    {
      id: nanoid(),
      role: 'Data Integrity Sentinel in Java',
      company: '',
      dates: 'Aug 2025',
      description: ``,
      descriptionLs: [
        "Developed a scalable system for large-scale data integrity verification",
        "Achieved a processing throughput of over 300 MB/sec",
        "Implemented a robust, multi-threaded concurrency model",
        "Implemented a decoupled Producer-Consumer pipeline to maximize throughput",
        "Used Spring IoC and Factory patterns to build a modular and maintainable system",
      ],
    },
    
    {
      id: nanoid(),
      role: 'AI-Based Platform to Process Files',
      company: '',
      dates: 'Apr 2025',
      description: '',
      descriptionLs: [
        `Engineered an AI-based platform to automate file processing`,
        `Architected with clean separation of concerns to maximize maintainability and extensibility`,
        `Special features: parallel processing, interactive chat, supports different providers, flexible output options, file operations pipeline`,
        // `Engineered an automated workflow for file loading, versioning, and updates, enhancing performance and reliability.`,
        // `Integrated dynamic configuration and created a serverless REST API (API Gateway, DynamoDB) for logging`,
      ],
    },
    //     {
    //       id: nanoid(),
    //       role: 'Personal Website',
    //       company: '',
    //       dates: 'May 2025',
    //       description:
    // `•  Tech stack: Static site generator (Hugo), AWS (S3, Cloudfront, Lambda)
    // •  Developed dynamic redirects and page migrations, SEO optimizations, automated search indexing and cache refresh, invalidations
    // •  Created a serverless RESTFul API (API Gateway, Lambda) to trigger Cloudfront cache invalidation`,
    //     },
    //     {
    //         id: nanoid(),
    //         role: 'NestJS CRUD App',
    //         company: '',
    //         dates: 'Mar 2025',
    //         description: 
    // `•  Developed a server-side backend NestJS application
    // •  Highly modular with custom routes for database batch operations
    // •  Partial integration with Supabase Postgres database`,
    //     },
    {
      id: nanoid(),
      role: 'Automated Backup Solution with AWS S3',
      company: '',
      dates: 'Feb 2025',
      description: '',
      descriptionLs: [
        `Automated durable system for backups to AWS S3`,
        `Optimized backup performance with an incremental approach`,
        `Native integration with Git-tracked projects`,
        `Analyzed operational metrics and costs using Athena and SQL`,
      ],
    },
    // {
    //   id: nanoid(),
    //   role: 'Visualize Bank Statements',
    //   company: '',
    //   dates: 'Sep 2024',
    //   description: '',
    //   descriptionLs: [
    //     `Platform that generates interactive visualizations`,
    //     `Developed SQL queries to analyze spending trends`,
    //     `Ingest data into SQL Warehouse (BigQuery)`,
    //   ],
    // }
  ],
  education: [
    {
      id: nanoid(),
      institution: 'International Institute of Information Technology (I2IT)',
      degree: 'Bachelor of Engineering, Electronics & Telecommunication',
      dates: '2026',
      gpa: '',
    },
  ],
  certificates: [
    { id: nanoid(), name: 'AWS Academy Cloud Foundations' },
    { id: nanoid(), name: 'AWS Academy Cloud Architecting' }
  ],

  font: 'Libre Baskerville',
  theme: 'dark'
};
