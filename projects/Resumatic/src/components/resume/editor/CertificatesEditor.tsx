import React from 'react';
import type { Certificate } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { PlusCircle, Trash2 } from 'lucide-react';

interface CertificatesEditorProps {
  certificates: Certificate[];
  onChange: (id: string, e: React.ChangeEvent<HTMLInputElement>) => void;
  onAdd: () => void;
  onRemove: (id: string) => void;
}

export function CertificatesEditor({ certificates, onChange, onAdd, onRemove }: CertificatesEditorProps) {
  return (
    <>
      {certificates.map((cert) => (
        <div key={cert.id} className="p-3 border rounded-md space-y-2 relative">
          <Button variant="ghost" size="icon" className="absolute top-1 right-1 h-7 w-7" onClick={() => onRemove(cert.id)}>
            <Trash2 className="size-4" />
          </Button>
          <Input placeholder="Certificate Name" name="name" value={cert.name} onChange={(e) => onChange(cert.id, e)} />
        </div>
      ))}
      <Button variant="outline" onClick={onAdd}>
        <PlusCircle className="mr-2" />
        Add Certificate
      </Button>
    </>
  );
}
