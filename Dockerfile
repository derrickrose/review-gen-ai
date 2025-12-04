FROM python:3.11-slim

WORKDIR /app

#RUN pip install --no-cache-dir requests fastapi uvicorn[standard] watchgod gradio_client gradio ollama pezzo ramda
#RUN pip install --no-cache-dir scipy==1.10.1
#RUN pip uninstall --no-cache-dir openai -y
#RUN pip install --no-cache-dir openai
#RUN pip install --no-cache-dir streamlit gradio
#RUN pip install --no-cache-dir datasets transformers
#RUN pip install --no-cache-dir librosa soundfile
#RUN pip install --no-cache-dir torch
#RUN pip install --no-cache-dir outlines
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
