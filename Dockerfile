# 1. Use a specific, stable version of Python on Bullseye
FROM python:3.10-slim-bullseye

# 2. Set environment to prevent prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# 3. Combine update and install, and add a "fix-missing" flag
RUN apt-get update --fix-missing && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 4. The rest of your file stays the same
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]