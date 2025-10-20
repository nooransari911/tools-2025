import type { ResumeData } from './types';
import { nanoid } from 'nanoid';

export const initialResumeData: ResumeData = {
  personalInfo: {
    name: 'Noor Ansari',
    title: 'Electronics Engineering Student',
    email: 'mohammadna71@gmail.com',
    location: 'Pune, MH',
    summary:
      'Electronics Engineering student with a foundation in VLSI and power electronics.'
  },
  skills: [
    {
      id: nanoid(),
      category: 'Domains',
      technologies: 'VLSI, Embedded Systems, Power Electronics, Analog Circuit Design'
    },
    {
      id: nanoid(),
      category: 'HDLs',
      technologies: 'Verilog, SystemVerilog'
    },
    {
      id: nanoid(),
      category: 'Software Languages',
      technologies: 'C, Python'
    },
    {
      id: nanoid(),
      category: 'Microcontrollers',
      technologies: 'ESP32, Arduino'
    },
    {
      id: nanoid(),
      category: 'Protocols & Interfaces',
      technologies: 'AXI, APB, I2C, RS-485'
    },
    {
      id: nanoid(),
      category: 'EDA & Simulation Tools',
      technologies: 'Eagle CAD, LTspice, Proteus'
    },
    {
      id: nanoid(),
      category: 'Lab Skills',
      technologies: 'PCB Design, Oscilloscope, Soldering'
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
      role: 'Major Project: AXI-APB Bridge (VLSI Domain)',
      company: 'Sponsored by Iravan Technologies',
      dates: 'Jul 2025 - Present',
      description:
      `• Pioneered the initial research and proof-of-concept work that establishes the project foundation
• Designed a modular core architecture in Verilog with clear separation of concerns
• Built comprehensive testbench using SystemVerilog and modern verification practices.
• Mentored teammates through design challenges and coordinate team efforts`,
    },
    {
      id: nanoid(),
      role: 'Smart Fan Controller (High-Level Architecture only)',
      company: '',
      dates: 'Jun 2025',
      description: `• Designed high-level firmware architecture for dynamic fan speed control
• Integrated ADC, DMA, I2C, and timer peripherals
• No hardware implementation
• Target: Ti MSPM0C, I2C fan controller, Vac/Current sensors`,
    },
    {
      id: nanoid(),
      role: 'Electric Cooker Project',
      company: '',
      dates: 'Apr 2025',
      description: `• Automatically cooks food to a specific temperature and turns off
• Designed PCB with Eagle CAD
• Implemented I2C communication using ESP-IDF framework
• Components: ESP32, Relay Module, Heating Element, I2C-based Digital Temp Sensor`,
    },
    {
      id: nanoid(),
      role: 'MOSFET Half Bridge Driver Simulation',
      company: '',
      dates: 'Nov 2024 - Dec 2024',
      description: `• Simulated a MOSFET half-bridge driver capable of high-speed switching and strong drive capability
• Applied analog circuit design principles`,
    },
    {
      id: nanoid(),
      role: 'Exploration of MOSFETs & Power Inverter Design',
      company: '',
      dates: 'Nov 2024 - Dec 2024',
      description: `• Researched datasheets, application notes, and reference designs
• Investigated design challenges including functional and safety isolation, parasitic effects, and high-power driving
• Assessed high-level architectures to understand key performance and safety considerations`,
    },
    {
      id: nanoid(),
      role: 'Color Recognition and DC Motor Control using Arduino & ESP32',
      company: '',
      dates: 'Feb 2024',
      description: `• Led a team of 3 in developing an embedded system
• Built a color recognition system using ESP32 and DC motor control using Arduino
• Integrated both systems into a unified application`,
    }
  ],
  education: [
    {
      id: nanoid(),
      institution: 'nternational Institute of Information Technology (I2IT)',
      degree: 'Bachelor of Engineering, Electronics & Telecommunication',
      dates: '2026',
      gpa: '',
    },
  ],
  certificates: [],
  additionalinfo: [
    {
      id: nanoid (),
      description: "Explored aerospace engineering fundamentals including flight dynamics, orbital mechanics, and vehicle design"
    },
    // {
    //   id: nanoid (),
    //   description: 'Explored vehicle design by building rockets and fixed-wing aircrafts in Kerbal Space Program (KSP) game.'
    // },
    // {
    //   id: nanoid (),
    //   description: 'Developed a practical understanding of flight dynamics by flying rockets and fixed-wing aircrafts in KSP game.'
    // },
    // {
    //   id: nanoid (),
    //   description: 'Key accomplishments in KSP include: a moon landing, orbital rendezvous & docking, and deployment of a space-based relay network.'
    // },
    // {
    //   id: nanoid (),
    //   description: 'Explored the high-level design and specifications of real-world launch vehicles and commercial aircraft'
    // }
  ],
  font: 'Libre Baskerville',
  theme: 'dark'
};
