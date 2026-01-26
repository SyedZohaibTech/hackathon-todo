FROM python:3.13-slim

WORKDIR /app

COPY agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent/ .

CMD ["python", "-m", "src.agents.todo_agent"]