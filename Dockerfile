# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Download LanguageTool data during the build
RUN python -c "import language_tool_python; language_tool_python.LanguageTool('en-US')"

# Copy the content of the local src directory to the working directory
COPY ./app /code/app

# Specify the command to run on container startup
# Use uvicorn to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
