
from llama_cpp import Llama

class LLM:
    def __init__(self, model_name="models/bart_homer.gguf"):
        """Initialize the LLM with the specified model."""
        self.model_name = model_name
        self.llm = Llama(model_path=self.model_name)


    def invoke(self,message):
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "assistant", "content": "I’m Homer Simpson! I work at the Springfield Nuclear Power Plant (don’t ask me what I do there, I mostly push buttons and hope nothing explodes). I love beer, donuts, sleeping at work, and watching TV… Mmm… TV… "},
                {"role": "user", "content": message},
            ]
        )
        if "choices" not in response or len(response["choices"]) == 0:
            raise ValueError("No response from LLM")
        return response["choices"][0]["message"]["content"]