#!/bin/bash

sudo dnf install python3 python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt