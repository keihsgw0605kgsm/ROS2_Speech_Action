FROM osrf/ros:humble-desktop

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    python3-setuptools \
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
# Keep setuptools on the Ubuntu 22.04 / ROS2 Humble-friendly line. Newer setuptools + pip
# can break `colcon build --symlink-install` with: setup.py: error: option --editable not recognized
RUN printf '%s\n' 'setuptools==59.6.0' > /tmp/pip_constraints.txt
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir --ignore-installed \
        -c /tmp/pip_constraints.txt \
        -r /tmp/requirements.txt && \
    python3 -m pip install --force-reinstall -c /tmp/pip_constraints.txt "setuptools==59.6.0"

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
