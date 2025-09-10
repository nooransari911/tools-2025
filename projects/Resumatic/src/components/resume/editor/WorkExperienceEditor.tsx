import React from 'react';
import type { WorkExperience } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { PlusCircle, Trash2, Plus } from 'lucide-react';

interface WorkExperienceEditorProps {
  workExperience?: WorkExperience[];
  onChange: (id: string, field: string, value: string | string[]) => void;
  onAdd: () => void;
  onRemove: (id: string) => void;
  onAddDescriptionPoint: (id: string) => void;
  onDescriptionChange: (expId: string, index: number, value: string) => void;
  onRemoveDescriptionPoint: (expId: string, index: number) => void;
}

export function WorkExperienceEditor({ 
  workExperience, 
  onChange, 
  onAdd, 
  onRemove,
  onAddDescriptionPoint,
  onDescriptionChange,
  onRemoveDescriptionPoint
}: WorkExperienceEditorProps) {
  return (
    <>
      {workExperience?.map((exp) => (
        <div key={exp.id} className="p-3 border rounded-md space-y-2 relative">
          <Button 
            variant="ghost" 
            size="icon" 
            className="absolute top-1 right-1 h-7 w-7" 
            onClick={() => onRemove(exp.id)}
          >
            <Trash2 className="size-4" />
          </Button>
          
          <Input 
            placeholder="Position" 
            value={exp.position} 
            onChange={(e) => onChange(exp.id, 'position', e.target.value)} 
          />
          <Input 
            placeholder="Company" 
            value={exp.company} 
            onChange={(e) => onChange(exp.id, 'company', e.target.value)} 
          />
          <Input 
            placeholder="Location" 
            value={exp.location} 
            onChange={(e) => onChange(exp.id, 'location', e.target.value)} 
          />
          <Input 
            placeholder="Dates (e.g., Jun 2024 - Present)" 
            value={exp.dates} 
            onChange={(e) => onChange(exp.id, 'dates', e.target.value)} 
          />
          
          <div className="space-y-2">
            <label className="text-sm font-medium">Responsibilities/Achievements</label>
            {exp.description.map((point, index) => (
              <div key={index} className="flex items-center gap-2">
                <Input
                  placeholder={`Description point ${index + 1}`}
                  value={point}
                  onChange={(e) => onDescriptionChange(exp.id, index, e.target.value)}
                />
                {exp.description.length > 1 && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => onRemoveDescriptionPoint(exp.id, index)}
                  >
                    <Trash2 className="size-3" />
                  </Button>
                )}
              </div>
            ))}
            <Button
              variant="outline"
              size="sm"
              onClick={() => onAddDescriptionPoint(exp.id)}
              className="mt-1"
            >
              <Plus className="mr-1 size-3" />
              Add Point
            </Button>
          </div>
        </div>
      ))}
      <Button variant="outline" onClick={onAdd}>
        <PlusCircle className="mr-2" />
        Add Work Experience
      </Button>
    </>
  );
}