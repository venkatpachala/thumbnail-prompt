import React from 'react';

interface Props {
  prompt: string;
  setPrompt: (v: string) => void;
  headline: string;
  setHeadline: (v: string) => void;
  onGenerate: () => void;
  loading: boolean;
}

export const PromptForm: React.FC<Props> = ({ prompt, setPrompt, headline, setHeadline, onGenerate, loading }) => (
  <div className="space-y-4">
    <textarea className="w-full border p-2" rows={3} value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Prompt" />
    <input className="w-full border p-2" value={headline} onChange={(e) => setHeadline(e.target.value)} placeholder="Headline" />
    <button className="bg-blue-600 text-white px-4 py-2" onClick={onGenerate} disabled={loading}>
      {loading ? 'Generating...' : 'Generate'}
    </button>
  </div>
);
