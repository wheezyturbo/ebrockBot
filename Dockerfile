FROM python:3.9

ENV DISCORD_KEY b'gAAAAABlCvHY-kPq1VIJurDUg4fovZpVHcdfMxvMKUTEYwlgDkImCbma2n6g15u8Yh2IVnulcpzNUMna6e4hhGKEmrMkBjpcUWqcldsR2ywZNeBCT0tpIqwu2pSVFw50FpSQdbpJQv0M8GGqdvQrAg3Tv3ik8ihKs4ztxFXmswYhzlKTRcZWrgc='
# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
RUN pip install cryptography discord yt_dlp ffmpeg pynacl

# Copy the bot code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the bot's port
EXPOSE 8080

# Start the bot
CMD ["python", "bot.py"]
