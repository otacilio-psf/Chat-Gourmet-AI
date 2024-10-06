# King of the Free-Tier Cloud Deployment

This project aims to deploy a Chat Gourmet AI to the cloud using the free tier offerings from various cloud services.

You can access the app at [chat-gourmet-ai.streamlit.app](https://chat-gourmet-ai.streamlit.app)

As it use free tier the app can be un-available some times due rate limits.

## Services Used

### [Groq Cloud](https://console.groq.com/docs/quickstart)

Groq Cloud offers a free tier with a generous rate limit for several open-source models, including Llama 3.1.

### [Qdrant Cloud](https://qdrant.tech/pricing/)

Qdrant Cloud provides a sufficient free tier where we can host our vector database.

### [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)

Streamlit Community Cloud allows you to publish public Streamlit apps for free.

## Python Dependencies

To manage Python dependencies efficiently, we created a link for the chatbot files in the `ui` directory and prepared a dedicated `pyproject.toml` file (exported to requirements.txt) for cloud deployment.
