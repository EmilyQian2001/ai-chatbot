import { openai } from '@ai-sdk/openai';
import { perplexity } from '@ai-sdk/perplexity';
import { experimental_wrapLanguageModel as wrapLanguageModel } from 'ai';
import { customMiddleware } from './custom-middleware';

export const customModel = (apiIdentifier: string) => {
  console.log('Model identifier:', apiIdentifier);
  
  const model = apiIdentifier.startsWith('sonar-')
    ? perplexity(apiIdentifier)
    : openai(apiIdentifier);

  return wrapLanguageModel({
    model,
    middleware: customMiddleware,
  });
};

export const imageGenerationModel = openai.image('dall-e-3');
