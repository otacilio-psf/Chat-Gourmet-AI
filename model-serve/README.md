# Model Serve

Serve open-source LLM models for free (with certain limitations).

## Models

We offer two model options:

- **phi 3.5 mini**
- **llama 3.1 8b**

For this project, we are using the **llama 3.1 8b** model. Please note that you need to accept the terms on [Hugging Face](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct) to use this model.

## Deployment

To deploy this notebook on [Kaggle](https://www.kaggle.com/):

1. **Import the Notebook**: Import this notebook into Kaggle.
2. **GPU Requirements**: Two T4 GPUs
3. **Setup secrets**: You need to configure the following secrets on Kaggle:
    - `hf_token`: Your Hugging Face token
    - `ngrok_token`: Your [Ngrok token](https://ngrok.com/pricing) - we use free tier

Ensure these secrets are set up properly for successful deployment and access.

## Built With

This project leverages the following technologies:

- [vllm-project/vllm](https://github.com/vllm-project/vllm) for a production-grade LLM backend
- [chujiezheng/chat_templates](https://github.com/chujiezheng/chat_templates) for easy chat template
- [astral-sh/uv](https://github.com/astral-sh/uv) for ultra-fast lib installation
- [Ngrok](https://ngrok.com/) to expose the model to the internet
- [Kaggle](https://www.kaggle.com/) for deploying the notebook and GPU infrastructure
- [meta-llama/Meta-Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct) as the primary model
- [microsoft/Phi-3.5-mini-instruct](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) as a backup model