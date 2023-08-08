# STRATHBOT-API

This is a service API for a Bot backend. Speech2Text is achieved using OpenAI Whisper for audio transcription. It is limited to accept 5MB audio files ~ 3 mins of audio. 

### RUN
To run on your 
#### 1.  Local computer

```
docker-compose up
```
#### 2.  Cloud Virtual Machine
- SSH into your virtual machine
- Locate your root folder and create a new directory for the project

```
mkdir strathbot-api
```
- Clone the project into the created directory

```
git clone git@github.com:DimejiOladepo/strathbot-api.git
```
- Run the project

```
docker-compose up
```
