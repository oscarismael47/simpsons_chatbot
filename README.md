# simpsons_chatbot

This repository contains a Streamlit-based chatbot that uses a fine-tuned Large Language Model (LLM) to respond in the style of Homer Simpson. Users can interact as Bart Simpson or other characters, and the chatbot will reply accordingly.

## Features

- Chatbot interface built with Streamlit
- Custom avatars for user (Bart) and assistant (Homer)
- Messages styled for clear distinction between user and assistant
- LLM backend powered by [llama.cpp](https://github.com/abetlen/llama-cpp-python)
- Easily switch between characters for both user and assistant

## Dataset

The chatbot is trained on conversations between Bart and Homer Simpson:
- [Bart & Homer Simpson Conversations Dataset](https://huggingface.co/datasets/OscarIsmael47/Bart_Simpson_and_Homer_Simpson_conversations)

## Model

The chatbot uses a fine-tuned Llama 3.1 model specifically adapted for Bart and Homer Simpson conversations.  
Download the model here:  
- [Meta-Llama-3.1-8B-q4_k_m-Bart_Simpson_and_Homer_Simpson-GGUF](https://huggingface.co/OscarIsmael47/Meta-Llama-3.1-8B-q4_k_m-Bart_Simpson_and_Homer_Simpson-GGUF)


## Getting Started

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/simpsons_chatbot.git
   cd simpsons_chatbot
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Download the model**
   - Place the GGUF model file in the `models/` directory (default: `models/bart_homer.gguf`).

4. **Run the app**
   ```sh
   streamlit run app.py
   ```

## File Structure

- `app.py` — Streamlit UI and chat logic
- `llm_helper.py` — LLM wrapper for chat completion
- `icons/` — Avatar images for Bart and Homer
- `models/` — GGUF model files

## Customization

- To add more characters, update the avatars and modify the chat logic in `app.py`.
- You can fine-tune your own models using the provided dataset.



