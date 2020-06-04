FROM python:3.7.3-stretch

# Working Directory
WORKDIR /api

# Copy source code to working directory
COPY . api.py /api/

# Install packages from requirements.txt
RUN pip3 install -r requirements.txt

# Expose port 80
EXPOSE 80

# Run api.py at container launch
CMD ["python", "api.py"]