FROM osrf/ros:humble-desktop

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    python3-venv \
    ffmpeg \
    portaudio19-dev \
    alsa-utils \
    pulseaudio \
    nano \
    tree \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /root/ros2_ws

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir --ignore-installed -r /tmp/requirements.txt

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
