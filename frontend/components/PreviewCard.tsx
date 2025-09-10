import React from 'react';

interface Props {
  src?: string;
  title: string;
}

export const PreviewCard: React.FC<Props> = ({ src, title }) => (
  <div className="border p-2">
    <h3 className="font-bold mb-2">{title}</h3>
    {src ? <img src={src} alt={title} className="max-w-full" /> : <div className="text-gray-500">No image</div>}
    {src && (
      <a href={src} download className="block mt-2 text-blue-600 underline">
        Download
      </a>
    )}
  </div>
);
