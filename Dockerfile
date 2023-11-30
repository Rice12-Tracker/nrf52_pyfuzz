# Use the official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install necessary packages including git, sudo, gcc, make, python3-pip, automake, autoconf
RUN apt-get update && apt-get install -y git sudo gcc make python3-pip automake autoconf

# Allow passwordless sudo for all users (not recommended for production environments)
RUN echo "ALL ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Create a working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/Rice12-Tracker/nrf52_pyfuzz.git /app/nrf52_pyfuzz

# Change ownership of the directory to the non-root user
RUN adduser --disabled-password --gecos '' myuser && \
    chown -R myuser:myuser /app/nrf52_pyfuzz

# Switch to the non-root user
USER myuser

# Set the working directory to nrf52_pyfuzz
WORKDIR /app/nrf52_pyfuzz

# Run the build script
RUN ./build.sh

# Start a bash shell when the container is run
CMD ["bash"]
