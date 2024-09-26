# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Command to run Streamlit app
CMD ["/app/.venv/bin/streamlit", "run", "chatbot.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
