FROM python:3.7.3-stretch

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

# Install packages from requirements.txt
RUN pip3 install -r requirements.txt

# Expose port 80
EXPOSE 80

# Run web.py at container launch
CMD ["python", "web.py"]