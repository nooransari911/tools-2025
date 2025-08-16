import React from 'react';
import type { PersonalInfo } from '@/lib/types';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

interface PersonalInfoEditorProps {
  personalInfo: PersonalInfo;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

export function PersonalInfoEditor({ personalInfo, onChange }: PersonalInfoEditorProps) {
  return (
    <>
      <div className="space-y-1">
        <Label htmlFor="name">Full Name</Label>
        <Input id="name" name="name" value={personalInfo.name} onChange={onChange} />
      </div>
      <div className="space-y-1">
        <Label htmlFor="title">Title</Label>
        <Input id="title" name="title" value={personalInfo.title} onChange={onChange} />
      </div>
      <div className="space-y-1">
        <Label htmlFor="email">Email</Label>
        <Input id="email" name="email" value={personalInfo.email} onChange={onChange} />
      </div>
      <div className="space-y-1">
        <Label htmlFor="location">Location</Label>
        <Input id="location" name="location" value={personalInfo.location} onChange={onChange} />
      </div>
      <div className="space-y-1">
        <Label htmlFor="summary">Summary</Label>
        <Textarea id="summary" name="summary" value={personalInfo.summary} onChange={onChange} />
      </div>
    </>
  );
}
