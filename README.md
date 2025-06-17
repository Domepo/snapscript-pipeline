## VENV
python -m venv venv
.venv\Scripts\activate

Strg+Shift+P > Select Interpreter > venv

docker stop video2script 2>/dev/null && docker rm video2script 2>/dev/null; docker build -t video2script . && docker run -d --name video2script --link ollama:ollama -p 8501:8501 -v $(pwd)/data:/app/data video2script

docker run -d   -v ollama:/root/.ollama   -p 11434:11434   --name ollama ollama/ollama
docker exec -it ollama ollama run gemma3:27b