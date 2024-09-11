# Model Serve

This project uses [vLLM](https://github.com/vllm-project/vllm) to serve machine learning models and make them publicly accessible via [Ngrok](https://ngrok.com/).

## Models

We offer two model options:

- **phi 3.5 mini**
- **llama 3.1 8b**

For this project, we are using the **llama 3.1 8b** model. Please note that you need to accept the terms on [Hugging Face](https://huggingface.co/) to use this model.

## Deployment

To deploy this notebook on [Kaggle](https://www.kaggle.com/):

1. **Import the Notebook**: Import this notebook into Kaggle.
2. **GPU Requirements**: Two T4 GPUs
3. **Setup secrets**: You need to configure the following secrets on Kaggle:
    - `hf_token`: Your Hugging Face token
    - `ngrok_token`: Your Ngrok token

Ensure these secrets are set up properly for successful deployment and access.
