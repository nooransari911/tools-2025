'use client';

import React from 'react';
import type { ResumeData } from '@/lib/types';
import {
	Sidebar,
	SidebarHeader,
	SidebarContent,
	SidebarFooter,
	SidebarTrigger,
} from '@/components/ui/sidebar';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Accordion } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import {
	User,
	Briefcase,
	GraduationCap,
	Award,
	Download,
	FileUp,
	FileDown,
	FileText,
	FileCode,
	ChevronDown
} from 'lucide-react';
import { nanoid } from 'nanoid';
import { SectionWrapper } from './editor/SectionWrapper';
import { PersonalInfoEditor } from './editor/PersonalInfoEditor';
import { ExperienceEditor } from './editor/ExperienceEditor';
import { EducationEditor } from './editor/EducationEditor';
import { CertificatesEditor } from './editor/CertificatesEditor';

interface EditorSidebarProps {
	resume: ResumeData;
	setResume: React.Dispatch<React.SetStateAction<ResumeData>>;
	onExportJson: () => void;
	onImportJson: () => void;
	resumeType: 'software' | 'hardware';
	setResumeType: (type: 'software' | 'hardware') => void;
}

const getFormattedDate = () => {
	const date = new Date();
	const day = date.getDate();
	const month = date.toLocaleString('default', { month: 'short' });
	const year = date.getFullYear().toString().slice(-2);
	return `${day} ${month} ${year}`;
};

const exportWithDynamicallyEmbeddedCSS = async () => {
	const element = document.getElementById('resume-preview');
	if (!element) {
		console.error("Could not find the element with id 'resume-preview'.");
		return;
	}

	const stylesheetLinks = document.querySelectorAll('link[rel="stylesheet"]');
	const cssFetchPromises = Array.from(stylesheetLinks).map(link =>
		fetch(link.href)
			.then(response => {
				if (!response.ok) {
					console.error(`Failed to fetch stylesheet: ${link.href}`);
					return '';
				}
				return response.text();
			})
			.catch(err => {
				console.error(`Error fetching stylesheet ${link.href}:`, err);
				return '';
			})
	);

	const cssTexts = await Promise.all(cssFetchPromises);
	const combinedCssText = cssTexts.join('/* --- Next Stylesheet --- */');

	const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Resume</title>
  <style>
    ${combinedCssText}
  </style>
</head>
<body>
  ${element.outerHTML}
</body>
</html>`;

	const blob = new Blob([html], { type: 'text/html' });
	const url = URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = 'resume.html';
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
};

const handlePrint = async (resumeType: 'software' | 'hardware', font: string) => {
	const element = document.getElementById('resume-preview');
	if (!element) {
		console.error("Could not find the element with id 'resume-preview'.");
		return;
	}

	const stylesheetLinks = document.querySelectorAll('link[rel="stylesheet"]');
	const cssFetchPromises = Array.from(stylesheetLinks).map(link =>
		fetch(link.href)
			.then(response => {
				if (!response.ok) {
					console.error(`Failed to fetch stylesheet: ${link.href}`);
					return '';
				}
				return response.text();
			})
			.catch(err => {
				console.error(`Error fetching stylesheet ${link.href}:`, err);
				return '';
			})
	);

	const cssTexts = await Promise.all(cssFetchPromises);
	const combinedCssText = cssTexts.join('/* --- Next Stylesheet --- */');
	const resumeTypeChar = resumeType === 'software' ? 'S' : 'H';
	const formattedDate = getFormattedDate();
	const title = `Resume ${resumeTypeChar} ${formattedDate}`;


	const fontMap: { [key: string]: string } = {
		'Inter': 'Inter, sans-serif',
		'Lora': 'Lora, serif',
		'Baskervville': 'Baskervville, serif',
		'Libre Baskerville': '"Libre Baskerville", serif',
		'Times New Roman': '"Times New Roman", serif',
	};
	const selectedFontFamily = fontMap[font] || 'Inter, sans-serif';


	const printWindow = window.open('', '_blank');
	if (printWindow) {
		printWindow.document.write(`
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>${title}</title>
                <style>
                    ${combinedCssText}
					body {
						font-family: ${selectedFontFamily};
					}
                    #resume-preview { margin-left: 0 !important; }

					@media print {
  .dark {
    background-color: white !important;
    color: black !important;
  }
  
  .dark * {
    background-color: transparent !important;
    color: black !important;
    border-color: #d1d5db !important; /* gray-300 */
  }
}
                </style>
            </head>
            <body>
                ${element.outerHTML}
            </body>
            </html>
        `);
		printWindow.document.close();
		printWindow.onload = () => {
			printWindow.print();
		}
	}
}


export function EditorSidebar({
	resume,
	setResume,
	onExportJson,
	onImportJson,
	resumeType,
	setResumeType,
}: EditorSidebarProps) {
	const handlePersonalInfoChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		const { name, value } = e.target;
		setResume((prev) => ({ ...prev, personalInfo: { ...prev.personalInfo, [name]: value } }));
	};

	const handleExperienceChange = (id: string, e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
		const { name, value } = e.target;
		setResume((prev) => ({
			...prev,
			experience: prev.experience.map((exp) => (exp.id === id ? { ...exp, [name]: value } : exp)),
		}));
	};

	const addExperience = () => {
		setResume((prev) => ({
			...prev,
			experience: [...prev.experience, { id: nanoid(), role: '', company: '', dates: '', description: '' }],
		}));
	};

	const removeExperience = (id: string) => {
		setResume((prev) => ({ ...prev, experience: prev.experience.filter((exp) => exp.id !== id) }));
	};

	const handleEducationChange = (id: string, e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target;
		setResume((prev) => ({
			...prev,
			education: prev.education.map((edu) => (edu.id === id ? { ...edu, [name]: value } : edu)),
		}));
	};

	const addEducation = () => {
		setResume((prev) => ({
			...prev,
			education: [...prev.education, { id: nanoid(), institution: '', degree: '', dates: '', gpa: '' }],
		}));
	};

	const removeEducation = (id: string) => {
		setResume((prev) => ({ ...prev, education: prev.education.filter((edu) => edu.id !== id) }));
	};

	const handleCertificateChange = (id: string, e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target;
		setResume((prev) => ({
			...prev,
			certificates: prev.certificates.map((cert) => (cert.id === id ? { ...cert, [name]: value } : cert)),
		}));
	};

	const addCertificate = () => {
		setResume((prev) => ({
			...prev,
			certificates: [...prev.certificates, { id: nanoid(), name: '' }],
		}));
	};

	const removeCertificate = (id: string) => {
		setResume((prev) => ({ ...prev, certificates: prev.certificates.filter((cert) => cert.id !== id) }));
	};

	const handleFontChange = (value: string) => {
		setResume((prev) => ({ ...prev, font: value }));
	};

	const handleThemeChange = (value: 'dark' | 'light') => {
		setResume((prev) => ({ ...prev, theme: value }));
	};

	const handleExportMarkdown = () => {
		const { personalInfo, experience, education, certificates } = resume;

		let markdownContent = `# ${personalInfo.name}\n\n`;
		if (personalInfo.email) markdownContent += `Email: ${personalInfo.email}\n`;
		if (personalInfo.phone) markdownContent += `Phone: ${personalInfo.phone}\n`;
		if (personalInfo.linkedin) markdownContent += `LinkedIn: ${personalInfo.linkedin}\n`;
		if (personalInfo.github) markdownContent += `GitHub: ${personalInfo.github}\n`;
		if (personalInfo.website) markdownContent += `Website: ${personalInfo.website}\n`;

		markdownContent += `\n# Experience\n\n`;
		experience.forEach(exp => {
			markdownContent += `## ${exp.role} ${exp.company}\n`;
			markdownContent += `*${exp.dates}*\n\n`;
			markdownContent += `${exp.description}\n\n`;
		});

		markdownContent += `# Education\n\n`;
		education.forEach(edu => {
			markdownContent += `## ${edu.institution}\n`;
			markdownContent += `*${edu.dates}*\n`;
			markdownContent += `${edu.degree}\n\n`;
		});

		markdownContent += `# Certificates\n\n`;
		certificates.forEach(cert => {
			markdownContent += `*   ${cert.name}\n`;
		});

		const blob = new Blob([markdownContent], { type: 'text/markdown' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `resume.md`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	};

	return (
		<Sidebar collapsible="icon" className="no-print" id="editor-sidebar">
			<SidebarHeader className="flex flex-col gap-2 items-stretch justify-between p-2">
				<div className="flex items-center justify-between">
					<div className="flex items-center gap-2">
						<FileText className="text-primary" />
						<span className="font-headline text-lg font-semibold">Resumatic</span>
					</div>
					<SidebarTrigger />
				</div>
				<DropdownMenu>
					<DropdownMenuTrigger asChild>
						<Button variant="outline" className="w-full justify-between">
							<span>{resumeType === 'software' ? 'Software Resume' : 'Hardware Resume'}</span>
							<ChevronDown className="h-4 w-4" />
						</Button>
					</DropdownMenuTrigger>
					<DropdownMenuContent className="w-[--radix-dropdown-menu-trigger-width]">
						<DropdownMenuItem onClick={() => setResumeType('software')}>
							Software
						</DropdownMenuItem>
						<DropdownMenuItem onClick={() => setResumeType('hardware')}>
							Hardware
						</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
				<Select onValueChange={handleFontChange} value={resume.font}>
					<SelectTrigger className="w-full">
						<SelectValue placeholder="Select a font" />
					</SelectTrigger>
					<SelectContent>
						<SelectItem value="Inter">Inter</SelectItem>
						<SelectItem value="Lora">Lora</SelectItem>
						<SelectItem value="Baskervville">Baskervville</SelectItem>
						<SelectItem value="Libre Baskerville">Libre Baskerville</SelectItem>
						<SelectItem value="Times New Roman">Times New Roman</SelectItem>
					</SelectContent>
				</Select>
				<Select onValueChange={handleThemeChange} value={resume.theme}>
					<SelectTrigger className="w-full">
						<SelectValue placeholder="Select theme" />
					</SelectTrigger>
					<SelectContent>
						<SelectItem value="dark">Dark</SelectItem>
						<SelectItem value="light">Light</SelectItem>
					</SelectContent>
				</Select>
			</SidebarHeader>
			<SidebarContent>
				<Accordion type="multiple" defaultValue={['personal-info']} className="w-full">
					<SectionWrapper value="personal-info" title="Personal Info" icon={<User className="mr-2" />}>
						<PersonalInfoEditor
							personalInfo={resume.personalInfo}
							onChange={handlePersonalInfoChange}
						/>
					</SectionWrapper>

					<SectionWrapper value="projects" title="Projects" icon={<Briefcase className="mr-2" />}>
						<ExperienceEditor
							experience={resume.experience}
							onChange={handleExperienceChange}
							onAdd={addExperience}
							onRemove={removeExperience}
						/>
					</SectionWrapper>

					<SectionWrapper value="education" title="Education" icon={<GraduationCap className="mr-2" />}>
						<EducationEditor
							education={resume.education}
							onChange={handleEducationChange}
							onAdd={addEducation}
							onRemove={removeEducation}
						/>
					</SectionWrapper>

					<SectionWrapper value="certificates" title="Certificates" icon={<Award className="mr-2" />}>
						<CertificatesEditor
							certificates={resume.certificates}
							onChange={handleCertificateChange}
							onAdd={addCertificate}
							onRemove={removeCertificate}
						/>
					</SectionWrapper>
				</Accordion>
			</SidebarContent>
			<SidebarFooter className="flex-col gap-2 border-t p-2">
				<Button variant="outline" onClick={() => handlePrint(resumeType, resume.font)}><Download className="mr-2" />Export to PDF</Button>
				<div className="grid grid-cols-2 gap-2">
					<Button variant="outline" onClick={onImportJson}><FileUp className="mr-2" />Import JSON</Button>
					<Button variant="outline" onClick={onExportJson}><FileDown className="mr-2" />Export JSON</Button>
					<Button variant="outline" onClick={exportWithDynamicallyEmbeddedCSS}><FileCode className="mr-2" />Export HTML</Button>
					<Button variant="outline" onClick={handleExportMarkdown}><FileText className="mr-2" />Export Markdown</Button>
				</div>
			</SidebarFooter>
		</Sidebar>
	);
}
