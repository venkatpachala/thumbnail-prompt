import React from 'react';

interface Props {
  onFile: (file: File) => void;
}

export const UploadBox: React.FC<Props> = ({ onFile }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFile(file);
  };

  return (
    <div className="border p-4 rounded">
      <input type="file" accept="image/png,image/jpeg" onChange={handleChange} />
    </div>
  );
};
