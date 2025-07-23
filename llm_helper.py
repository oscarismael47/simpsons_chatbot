
from llama_cpp import Llama

class LLM:
    def __init__(self, model_name="models/bart_homer.gguf"):
        """Initialize the LLM with the specified model."""
        self.model_name = model_name
        self.llm = Llama(model_path=self.model_name)

    def invoke(self,message):
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "user", "content": message},
            ]
        )
        if "choices" not in response or len(response["choices"]) == 0:
            raise ValueError("No response from LLM")
        return response["choices"][0]["message"]["content"]