// Define your models here.

export interface Model {
  id: string;
  label: string;
  apiIdentifier: string;
  description: string;
}

// lib/ai/models.ts
export const models: Array<Model> = [
  {
    id: 'gpt-4o-mini',
    label: 'GPT 4o mini',
    apiIdentifier: 'gpt-4o-mini',
    description: 'Small model for fast, lightweight tasks',
  },
  {
    id: 'gpt-4o',
    label: 'GPT 4o',
    apiIdentifier: 'gpt-4o',
    description: 'For complex, multi-step tasks',
  },
  {
    id: 'pplx-70b-online',
    label: 'Perplexity 70B',
    apiIdentifier: 'pplx-70b-online',
    description: 'Fast and powerful large language model',
  },
  {
    id: 'pplx-7b-online',
    label: 'Perplexity 7B',
    apiIdentifier: 'pplx-7b-online', 
    description: 'Efficient model for general tasks',
  }
] as const;

export const DEFAULT_MODEL_NAME: string = 'gpt-4o-mini';
