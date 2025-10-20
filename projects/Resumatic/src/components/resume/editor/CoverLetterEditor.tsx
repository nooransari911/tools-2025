'use client';

import React from 'react';
import { Textarea } from '@/components/ui/textarea';

interface CoverLetterEditorProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
}

export function CoverLetterEditor({ value, onChange }: CoverLetterEditorProps) {
  return (
    <div className="space-y-2">
      <Textarea
        placeholder="Write your optional cover letter here..."
        value={value}
        onChange={onChange}
        rows={6}
      />
    </div>
  );
}