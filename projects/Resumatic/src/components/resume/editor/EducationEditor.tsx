import React from 'react';
import type { Education } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { PlusCircle, Trash2 } from 'lucide-react';

interface EducationEditorProps {
  education: Education[];
  onChange: (id: string, e: React.ChangeEvent<HTMLInputElement>) => void;
  onAdd: () => void;
  onRemove: (id: string) => void;
}

export function EducationEditor({ education, onChange, onAdd, onRemove }: EducationEditorProps) {
  return (
    <>
      {education.map((edu) => (
        <div key={edu.id} className="p-3 border rounded-md space-y-2 relative">
          <Button variant="ghost" size="icon" className="absolute top-1 right-1 h-7 w-7" onClick={() => onRemove(edu.id)}>
            <Trash2 className="size-4" />
          </Button>
          <Input placeholder="Institution" name="institution" value={edu.institution} onChange={(e) => onChange(edu.id, e)} />
          <Input placeholder="Degree" name="degree" value={edu.degree} onChange={(e) => onChange(edu.id, e)} />
          <Input placeholder="Dates (e.g., Dec 2026)" name="dates" value={edu.dates} onChange={(e) => onChange(edu.id, e)} />
          <Input placeholder="GPA (Optional)" name="gpa" value={edu.gpa} onChange={(e) => onChange(edu.id, e)} className="hidden" />
        </div>
      ))}
      <Button variant="outline" onClick={onAdd}>
        <PlusCircle className="mr-2" />
        Add Education
      </Button>
    </>
  );
}
