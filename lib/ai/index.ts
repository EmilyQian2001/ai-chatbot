import { openai } from '@ai-sdk/openai';
import { perplexity, createPerplexity } from '@ai-sdk/perplexity';
import { experimental_wrapLanguageModel as wrapLanguageModel } from 'ai';

import { customMiddleware } from './custom-middleware';

// 创建perplexity实例
const pplx = createPerplexity({
  apiKey: process.env.PERPLEXITY_API_KEY
});

export const customModel = (apiIdentifier: string) => {
  if (apiIdentifier.startsWith('pplx-')) {
    return wrapLanguageModel({
      model: pplx(apiIdentifier),
      middleware: customMiddleware,
    });
  }

  return wrapLanguageModel({
    model: openai(apiIdentifier),
    middleware: customMiddleware,
  });
};

export const imageGenerationModel = openai.image('dall-e-3');