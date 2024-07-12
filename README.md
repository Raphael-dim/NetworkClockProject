# Network Clock Project

## Introduction

This project is a Network Clock (NC) application that displays the current date and time to an interactive user and allows remote users to request the current date and time in a specified format. Additionally, it provides functionality for an interactive user to set the system time.

## Project Structure

NetworkClockProject/<br>
│<br>
├── ts/<br>
│ ├── set_system_time.py<br>
│ ├── server.py<br>
│<br>
├── config/<br>
│ ├── port.txt<br>
│<br>
├── README.md<br>
└── client.py<br>

## Setup and Installation

1. Clone the repository:<br>
   git clone https://github.com/yourusername/NetworkClockProject.git

2. Navigate to the project directory:<br>
    cd NetworkClockProject

3. Install the required dependencies:<br>
    pip install -r requirements.txt

## Usage

- Running the Network Clock Server
Configure the TCP port by editing the config/port.txt file.

- Start the server:
python server.py