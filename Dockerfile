# Use a standard Python image
FROM python:3.10-slim-bookworm

# 1. Install uv directly from their official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Optimize uv behavior
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 2. Copy dependency files first
# (Ensure you have both pyproject.toml and uv.lock in your repo)
COPY pyproject.toml uv.lock ./

# 3. Install dependencies
# --frozen: strictly use the lockfile (fails if lockfile is out of sync)
# --no-install-project: strictly installs dependencies, not your bot code itself yet
RUN uv sync --frozen --no-install-project --no-dev

# 4. Copy the rest of your code
COPY . .

# 5. Run the bot
# "uv run" automatically finds the virtual environment created in step 3
# CHANGE 'main.py' to your actual file name!
CMD ["uv", "run", "main.py"]