import torch

from transformers import Pipeline, pipeline
class m_text :
    

    def load_text_model(device_name):
        pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype=torch.bfloat16,
            device= device_name
        
        )
        return pipe


    def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:

        system_prompt = """
        Your name is ML bot and you are a helpful
        chatbot responsible for teaching  machine learning system to your users.
        Always respond in markdown.
        """


        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ] 
        prompt = pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        predictions = pipe(
            prompt,
            temperature=temperature,
            max_new_tokens=256,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        ) 
        output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
        return output

