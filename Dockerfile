# Use a base Python image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code and the cron job file into the container
COPY fetch_news.py .
COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/cronjob

# Apply the cron job
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run cron and the application on container startup
CMD cron && tail -f /var/log/cron.log