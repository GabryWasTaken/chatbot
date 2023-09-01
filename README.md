![ChatBot](https://cdn.discordapp.com/attachments/733391066136313879/1147239203466379286/CHATBOT.png)

![Logo](https://img.shields.io/badge/Created%20by-GabryWasTaken-blue)
 

## PREREQUISITES
![MongoDB](https://img.shields.io/badge/Install-MongoDB-orange?link=https%3A%2F%2Fwww.mongodb.com%2Ftry%2Fdownload%2Fcommunity)
![MongoDB](https://img.shields.io/badge/Install-RabbitMQ-green?link=https%3A%2F%2Fwww.rabbitmq.com%2Fdownload.html)
![Python3.10](https://img.shields.io/badge/Install-Python%203.10%20or%20greater-blue?link=https%3A%2F%2Fwww.python.org%2Fdownloads%2F) \
Install the external dependencies, they are located in
```bash
requirements.txt
```
Set the PythonPath with the folder of the packages for example
```bash
C:/chatbot/bot;C:/chatbot/database;...
```
Have an Openai API key and insert it in the .env file, example
```bash
OPENAI_KEY = "YOUR_OPENAI_API_KEY"
```
## HOW TO RUN PROGRAM

* start the rabbitmq service
* start mongodb in local with che command mongod on git bash if you set it there
* Install all of the prerequisites in your virtual environment or your machine with the following command
```bash
pip install -r requirements.txt
```
* Open chatbot.bat in this folder \
**If it doesn't start replace the venv path with your venv path in the file chatbot.bat**
```bash
@echo off
call env\Scripts\activate #Replace this if you have a venv

python main.py
```
