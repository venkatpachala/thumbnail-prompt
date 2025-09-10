import React, { useState } from 'react';
import { PromptForm } from '../components/PromptForm';
import { UploadBox } from '../components/UploadBox';
import { PreviewCard } from '../components/PreviewCard';
import { uploadCutout, generateBackground, composeThumbnail } from '../lib/fetch';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [headline, setHeadline] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [bgPath, setBgPath] = useState<string>();
  const [cutoutPath, setCutoutPath] = useState<string>();
  const [thumbPath, setThumbPath] = useState<string>();

  const onGenerate = async () => {
    if (!file) return alert('Please upload an image');
    setLoading(true);
    try {
      const cutout = await uploadCutout(file);
      setCutoutPath(cutout.cutout_path);
      const bg = await generateBackground(prompt);
      setBgPath(bg.background_path);
      const thumb = await composeThumbnail({
        background_path: bg.background_path,
        cutout_path: cutout.cutout_path,
        headline,
        layout: 'subject-right',
      });
      setThumbPath(thumb.thumbnail_path);
    } catch (e) {
      console.error(e);
      alert('Generation failed');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setPrompt('');
    setHeadline('');
    setFile(null);
    setBgPath(undefined);
    setCutoutPath(undefined);
    setThumbPath(undefined);
  };

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  return (
    <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="space-y-4">
        <PromptForm prompt={prompt} setPrompt={setPrompt} headline={headline} setHeadline={setHeadline} onGenerate={onGenerate} loading={loading} />
        <UploadBox onFile={(f) => setFile(f)} />
        <button className="mt-4 text-sm text-gray-600 underline" onClick={reset}>Reset</button>
      </div>
      <div className="space-y-4">
        <PreviewCard title="Background" src={bgPath ? `${apiUrl}${bgPath}` : undefined} />
        <PreviewCard title="Cutout" src={cutoutPath ? `${apiUrl}${cutoutPath}` : undefined} />
        <PreviewCard title="Thumbnail" src={thumbPath ? `${apiUrl}${thumbPath}` : undefined} />
      </div>
    </div>
  );
}
