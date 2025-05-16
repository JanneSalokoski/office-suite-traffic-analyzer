FROM python:3.12-slim

# install tshark, chrome & dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    tshark \
    wget gnupg2 unzip \
    ca-certificates \
    xvfb \
    libnss3 libgconf-2-4 libxss1 libatk-bridge2.0-0 libgtk-3-0 \
 && rm -rf /var/lib/apt/lists/*

# install Google Chrome
RUN wget -q -O /tmp/google-chrome.deb \
     https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && apt-get update \
 && apt-get install -y /tmp/google-chrome.deb \
 && rm /tmp/google-chrome.deb

RUN useradd -m user \
    && mkdir -p /home/user/.cache/selenium \
    && chown -R user:user /home/user

# copy your selenium script
COPY . /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# make the capture‐wrapper entrypoint executable
COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN chmod +x /usr/local/bin/entrypoint.sh

RUN mkdir -p /tmp/selenium-cache && chmod 777 /tmp/selenium-cache
RUN mkdir -p /tmp/.config/google-chrome /tmp/.cache && chmod -R a+rwx /tmp/*

# CMD ["google-chrome", "--version"]
ENTRYPOINT ["entrypoint.sh"]
