import React from 'react';
import {
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

interface SectionWrapperProps {
  value: string;
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

export function SectionWrapper({ value, title, icon, children }: SectionWrapperProps) {
  return (
    <AccordionItem value={value}>
      <AccordionTrigger className="font-headline">
        {icon}
        {title}
      </AccordionTrigger>
      <AccordionContent className="space-y-4 px-1">{children}</AccordionContent>
    </AccordionItem>
  );
}
