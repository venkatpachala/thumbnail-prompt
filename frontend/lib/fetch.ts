import axios from 'axios';

const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

export async function uploadCutout(file: File) {
  const form = new FormData();
  form.append('image', file);
  const { data } = await api.post('/cutout/remove', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data as { cutout_path: string };
}

export async function generateBackground(prompt: string) {
  const { data } = await api.post('/background/generate', {
    prompt,
    width: 768,
    height: 512,
  });
  return data as { background_path: string };
}

export async function composeThumbnail(params: {
  background_path: string;
  cutout_path: string;
  headline: string;
  layout: string;
}) {
  const { data } = await api.post('/compose/thumbnail', {
    ...params,
    output_size: [1280, 720],
  });
  return data as { thumbnail_path: string };
}
