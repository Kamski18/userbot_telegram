# 1. Use a stable Python version
FROM python:3.10-slim-bookworm

# 2. Install uv directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# --- FIX: Force uv to use the system Python 3.10 ---
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PYTHON=/usr/local/bin/python3.10
ENV UV_COMPILE_BYTECODE=1
# --------------------------------------------------

# 3. Copy dependency files first
COPY pyproject.toml uv.lock ./

# 4. Install dependencies 
# We use --system to ensure it doesn't create a secondary venv inside Docker
RUN uv pip install --system --no-cache -r pyproject.toml

# 5. Copy the rest of your code
COPY . .

# 6. Run the bot directly with the system python
CMD ["python", "main.py"]