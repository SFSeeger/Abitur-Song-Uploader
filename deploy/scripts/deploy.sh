#!/bin/bash
git pull origin main

pip install -r requirements.txt
npm install --prefix ./src/theme

