'use client';

import React, { useState, useRef, useEffect } from 'react';
import type { ResumeData } from '@/lib/types';
import { initialResumeData as softwareData } from '@/lib/data-software';
import { initialResumeData as hardwareData } from '@/lib/data-hardware';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { EditorSidebar } from '@/components/resume/EditorSidebar';
import { ResumePreview } from '@/components/resume/ResumePreview';

export default function ResumaticPage() {
  const [resumeType, setResumeType] = useState<'software' | 'hardware'>('software');
  const [resume, setResume] = useState<ResumeData>(softwareData);
  const previewRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [theme, setTheme] = useState<string | null>(null);

  useEffect(() => {
    if (resumeType === 'software') {
      setResume(softwareData);
    } else {
      setResume(hardwareData);
    }
  }, [resumeType]);

  const handleExportJson = () => {
    const jsonString = JSON.stringify(resume, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleResumeChange = (newData: ResumeData) => {
    setResume(newData);
  };

  const handleImportJson = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const content = e.target?.result;
          if (typeof content === 'string') {
            const parsedData = JSON.parse(content);
            // Add validation here if needed
            setResume(parsedData);
          }
        } catch (error) {
          console.error('Error parsing JSON file:', error);
          alert('Invalid JSON file.');
        }
      };
      reader.readAsText(file);
    }
  };
  
  const triggerJsonImport = () => {
    fileInputRef.current?.click();
  };

  return (
    <SidebarProvider>
      <EditorSidebar
        resume={resume}
        setResume={handleResumeChange}
        onExportJson={handleExportJson}
        onImportJson={triggerJsonImport}
        resumeType={resumeType}
        setResumeType={setResumeType}
      />
      <SidebarInset className="bg-background text-foreground">
        <div className="flex-1 overflow-y-auto p-4 sm:p-8">
          <ResumePreview ref={previewRef} resume={resume} />
        </div>
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept="application/json"
          onChange={handleImportJson}
        />
      </SidebarInset>
    </SidebarProvider>
  );
}
