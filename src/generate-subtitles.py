from datetime import timedelta
import os
import whisper
import logging
import sys
from googletrans import Translator

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
#    filename='../data/birthday.log',
    level=logging.INFO
)


model = whisper.load_model("base") # Change this to your desired model
logging.info("Whisper model loaded.")
filePath = "/media"

files = os.listdir(path=filePath)

for path, subdirs, files in os.walk(filePath):
    for name in files:
        fileName = os.path.join(path, name)
        pre, ext = os.path.splitext(fileName)
        srtFilenamePT = pre + ".pt-BR.srt"
        srtFilenameEN = pre + ".en.srt"

        if 'mkv' in fileName or 'mp4' in fileName: None
        else: 
            logging.info(fileName + " ignored")
            continue

        if srtFilenameEN in files or srtFilenamePT in files:
            logging.info(fileName + " already processed. Ingoring")
            continue
        else:
            logging.info(fileName + " found a new file")

        transcribe = model.transcribe(audio=fileName)
        logging.info("transcribe done")
        segments = transcribe['segments']
        logging.info("transcribe segments")

        translator = Translator()

        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            segmentId = segment['id']+1
            textEN = text[1:] if text[0] == ' ' else text
            translation = translator.translate(textEN, src='en', dest='pt')
            textPT = translation.text


            with open(srtFilenameEN, 'a+', encoding='utf-8') as srtFile:
                srtFile.write(f"{segmentId}\n{startTime} --> {endTime}\n{textEN}\n\n")

            with open(srtFilenamePT, 'a+', encoding='utf-8') as srtFile:
                srtFile.write(f"{segmentId}\n{startTime} --> {endTime}\n{textPT}\n\n")

logging.info("all done")