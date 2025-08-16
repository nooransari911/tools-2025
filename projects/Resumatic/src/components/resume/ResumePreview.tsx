'use client';

import React from 'react';
import type { ResumeData } from '@/lib/types';
import { grayShadeL8xx, grayShadeL7xx, grayShadeL6xx, grayShadeL5xx, grayShadeL4xx, grayShadeL3xx, grayShadeL2xx, grayShadeL1xx } from '@/lib/GrayShades';

export const ResumePreview = React.forwardRef<HTMLDivElement, { resume: ResumeData }>(
  ({ resume }, ref) => {
    const fontClassMap: { [key: string]: string } = {
      'Inter': 'font-inter',
      'Lora': 'font-lora',
      'Baskervville': 'font-baskervville',
      'Libre Baskerville': 'font-libre-baskerville',
      'Times New Roman': 'font-times-new-roman',
  };

  const selectedFontClass = fontClassMap[resume.font] || 'font-inter';

  const themeClassMap: { [key: string]: string } = {
    'dark': 'bg-black text-gray-100',
    'light': 'bg-white text-black',
  };
  
  const selectedThemeClass = themeClassMap[resume.theme] || 'bg-black text-gray-100';
  const themeName = resume.theme === 'dark' ? 'dark' : '';
  const defaultBgColor   = themeName === 'dark' ? 'bg-black' : 'bg-white';
  const defaultTextColor = themeName === 'dark' ? 'text-white' : 'text-black';




    return (
      <div
        ref={ref}
        className={`w-full max-w-4xl text-sm shadow-lg
          print:aspect-[8.5/11] print:h-auto print:min-h-0 print:p-12 p-12 relative print:shadow-none print:bg-white print:text-black
          
          ${selectedFontClass}
          ${defaultBgColor}
          ${defaultTextColor} 
          ${selectedThemeClass}
          ${themeName}
          `}
        id="resume-preview"
      >
        {/*V1: className="w-full max-w-4xl h-auto min-h-[11in] aspect-[8.5/11]
                  shadow-lg
                  print-area bg-white text-black font-sans text-sm
                  p-12" */}
        {/*V2: className="w-full max-w-4xl bg-white text-black font-sans text-sm
                  shadow-lg 
                  print:aspect-[8.5/11] print:h-auto print:min-h-0 print:p-12
                  p-12"*/}

        {/* Header */}
        <header className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl italic font-bold font-headline">{resume.personalInfo.name}</h1>
            <p className={`text-xl italic ${grayShadeL6xx (themeName)} mt-1 font-headline`}>{resume.personalInfo.title}</p>
          </div>
          <div className={`${grayShadeL6xx (themeName)} text-right text-sm italic`}>
            <p>{resume.personalInfo.email}</p>
            <p className="mt-1">{resume.personalInfo.location}</p>
          </div>
        </header>

        {/* Summary */}
        <section className="mb-5 w-3/4">
          <p className={`leading-relaxed ${grayShadeL8xx (themeName)} text-sm`}>{resume.personalInfo.summary}</p>
        </section>

        <section className="mb-5">
          <h2 className="text-xl font-bold mb-2 font-headline">Technical Skills</h2>
          <hr className="border-t border-gray-400 my-1" />
          <div className="mt-2">
            {resume.skills.map((skill) => (
              // Each skill category is a flex row
              <div key={skill.id} className="flex items-start mb-1">
                {/* 1. The Category Title (The "Key") */}
                <div className="w-1/3 pr-4">
                  <p className={`font-semibold ${grayShadeL7xx (themeName)}`}>{skill.category}</p>
                </div>
                {/* 2. The List of Skills (The "Value") */}
                <div className="w-2/3">
                  <p className={`leading-relaxed ${grayShadeL6xx (themeName)}`}>{skill.technologies}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Projects */}
        <section className="mb-5">
          <h2 className="text-xl font-bold mb-2 font-headline">Projects</h2>
          <hr className="border-t border-gray-400 my-1" />
          {resume.experience.map((proj) => (
            <div key={proj.id} className="mb-3 print:break-inside-avoid-page">
              <div className="flex justify-between items-baseline mb-1">
                <h3 className={`font-bold text-lg font-headline ${grayShadeL7xx (themeName)}`}>{proj.role}</h3>
                <p className={`font-medium ${grayShadeL6xx (themeName)}`}>{proj.dates}</p>
              </div>
              <p className="text-lg font-headline">{proj.company}</p>
              <p className={`mt-1 ${grayShadeL6xx (themeName)} whitespace-pre-wrap leading-relaxed w-3/4`}>
                {proj.description}
              </p>
            </div>
          ))}
        </section>

        {/* Education */}
        <section className="mb-5 print:break-inside-avoid-page">
          <h2 className="text-xl font-bold mb-2 font-headline">Education</h2>
          <hr className="border-t border-gray-400 my-3" />
          {resume.education.map((edu) => (
            <div key={edu.id} className="mt-3">
              <h3 className={`text-lg font-headline ${grayShadeL7xx (themeName)}`}>{edu.institution}</h3>
              <div className="flex justify-between items-baseline">
                <p className={`italic ${grayShadeL6xx (themeName)}`}>{edu.degree}</p>
                <p className={`${grayShadeL6xx (themeName)} font-medium`}>{edu.dates}</p>
              </div>
            </div>
          ))}
        </section>

        {/* Certificates */}
        <section className="mb-5 print:break-inside-avoid-page">
          {resume.certificates?.length ? <div><h2 className="text-xl font-bold mb-2 font-headline">Certificates</h2> <hr className="border-t border-gray-400 my-1" /> </div> : ""}
          {resume.certificates ? resume.certificates.map((cert) => (
            <div>
              <div key={cert.id} className={`mb-1 ${grayShadeL7xx (themeName)}`}>
                <p>{cert.name}</p>
              </div>
            </div>
          )) : ""}
        </section>




        {/* Additional Knowledge & Interests */}
        <section className="mb-5">
          {resume.additionalinfo && resume.additionalinfo.length > 0 && (
            <>
              <h2 className="text-xl font-bold mb-2 font-headline">Additional Knowledge & Interests</h2>
              <hr className="border-t border-gray-400 my-1" />
              <ul className="list-disc list-outside pl-5 mt-2">
                {resume.additionalinfo.map((item) => (
                  <li key={item.id} className={`mb-1 ${grayShadeL6xx (themeName)} leading-relaxed print:break-inside-avoid`}>
                    {item.description}
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>



      </div>
    );
  }
);

ResumePreview.displayName = 'ResumePreview';
