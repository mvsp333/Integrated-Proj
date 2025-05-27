FROM python:3.12-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# This copies your Streamlit configuration file into the .streamlit directory you just created.
RUN cp config.toml ~/.streamlit/config.toml

# Similar to the previous step, this copies your Streamlit credentials file into the .streamlit directory.
RUN cp credentials.toml ~/.streamlit/credentials.toml

# This sets the default command for the container to run the app with Streamlit.
ENTRYPOINT ["streamlit", "run"]

# This command tells Streamlit to run your app.py script when the container starts.
CMD ["app3.py"]

# FROM python:3.12-slim

# # Install required tools (Node.js for localtunnel)
# RUN apt-get update && apt-get install -y curl gnupg && \
#     curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
#     apt-get install -y nodejs && \
#     apt-get clean

# # Copy app files into container
# COPY . /app
# WORKDIR /app

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose Streamlit's default port
# EXPOSE 80

# # Set Streamlit environment configs
# RUN mkdir -p ~/.streamlit
# ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
# RUN cp config.toml ~/.streamlit/config.toml
# RUN cp credentials.toml ~/.streamlit/credentials.toml

# # Run Streamlit and LocalTunnel in parallel
# CMD ["sh", "-c", "streamlit run app2.py & npx localtunnel --port 80 --print-requests"]
