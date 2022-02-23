### 1. Get Linux
FROM python:3.9-bullseye

### 3. Set working directory
WORKDIR /code

### 5. Copy code
ADD . /code/

### 5. Install build deps and download modules
RUN pip3 install --user --no-cache-dir -e .

### 6. Run
CMD [ "python3", "-m", "discord_bot" ]