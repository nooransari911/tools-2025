import React from 'react';
import type { Experience } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { PlusCircle, Trash2 } from 'lucide-react';

interface ExperienceEditorProps {
  experience: Experience[];
  onChange: (id: string, e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  onAdd: () => void;
  onRemove: (id: string) => void;
}

export function ExperienceEditor({ experience, onChange, onAdd, onRemove }: ExperienceEditorProps) {
  return (
    <>
      {experience.map((exp) => (
        <div key={exp.id} className="p-3 border rounded-md space-y-2 relative">
          <Button variant="ghost" size="icon" className="absolute top-1 right-1 h-7 w-7" onClick={() => onRemove(exp.id)}>
            <Trash2 className="size-4" />
          </Button>
          <Input placeholder="Project Name" name="role" value={exp.role} onChange={(e) => onChange(exp.id, e)} />
          <Input placeholder="Company" name="company" value={exp.company} onChange={(e) => onChange(exp.id, e)} className="hidden" />
          <Input placeholder="Dates (e.g., Jun 2025)" name="dates" value={exp.dates} onChange={(e) => onChange(exp.id, e)} />
          <Textarea placeholder="Description (use • for bullet points)" name="description" value={exp.description} onChange={(e) => onChange(exp.id, e)} />
        </div>
      ))}
      <Button variant="outline" onClick={onAdd}>
        <PlusCircle className="mr-2" />
        Add Project
      </Button>
    </>
  );
}
