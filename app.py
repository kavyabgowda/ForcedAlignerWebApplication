from flask import Flask, render_template, request, send_from_directory
import shutil
import zipfile
from flask import send_file
import logging
import os
from textgrid import MLF
import glob

from .archive import Archive
from .utilities import resolve_opts, ALIGNED, SCORES
from .aligner import Aligner
from .corpus import Corpus

DICTIONARY = "eng.dict"
MODEL = "eng.zip"

argDict = {
    "read": "eng.zip",
    "dictionary": "eng.dict",
    "configuration":"config.yaml",
    "LOGGING_FMT" : "%(message)s",
    "epochs": 5
}
__author__ = 'Kavya B'
APP_ROUTE=os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('re-sample.html')

@app.route('/resample', methods=['GET', 'POST'])
def resample():
    soxDataTarget = os.path.join(APP_ROUTE, 'soxData')
    dataTarget = os.path.join(APP_ROUTE, 'data')
    if not os.path.isdir(soxDataTarget):
        os.mkdir(soxDataTarget)
    else:
        files = glob.glob(soxDataTarget+'/*')
        for file in files:
            os.remove(file)
    if os.path.isdir(dataTarget):
        files = glob.glob(dataTarget + '/*')
        for file in files:
            os.remove(file)
    for file in request.files.getlist('wavFiles'):
        filename=file.filename
        destination="/".join([soxDataTarget, filename])
        file.save(destination)
    os.system('./resample.sh -s 16000 -r soxData/ -w data/')
    return render_template('align.html')

@app.route('/resample/upload', methods=['GET', 'POST'])
def upload():
    dataTarget=os.path.join(APP_ROUTE, 'data')
    if not os.path.isdir(dataTarget):
        os.mkdir(dataTarget)

    for file in request.files.getlist('files'):
        filename=file.filename
        destination="/".join([dataTarget, filename])
        file.save(destination)

    config=request.files["config"]
    configFilename = config.filename
    configDestination = "/".join([APP_ROUTE, configFilename])
    config.save(configDestination)

    dict = request.files["dict"]
    dictFilename = dict.filename
    dictDestination = "/".join([APP_ROUTE, dictFilename])
    dict.save(dictDestination)

    if configFilename != 'config.yaml':
        os.rename(configDestination, "/".join([APP_ROUTE, 'config.yaml']))
    loglevel = logging.WARNING
    logging.basicConfig(format=argDict.get('LOGGING_FMT'), level=loglevel)
    logging.info("Reading aligner from '{}'.".format(argDict.get('read')))

    #Unzipping the acoustic model
    archive = Archive(argDict.get('read'))
    configuration = os.path.join(archive.dirname, argDict.get('configuration'))
    argDict.__setitem__('configuration', configuration)
    shutil.move("/".join([APP_ROUTE, 'config.yaml']), os.path.join(archive.dirname, 'config.yaml'))

    opts = resolve_opts(argDict)
    print(opts)

    # initialize aligner and set it to point to the archive data
    aligner = Aligner(opts)
    aligner.curdir = archive.dirname

    #Removing existing OOV txt file
    if os.path.exists(os.getcwd()+'OOV.txt'):
        os.remove(os.getcwd()+'/OOV.txt')
    #HDMan
    corpus = Corpus(os.getcwd()+'/data/', opts)
    if os.path.exists(os.getcwd()+'OOV.txt'):
        return render_template('downloads.html')
    else:
        logging.info("Aligning corpus '{}'.".format(os.getcwd() + '/data/'))
        aligned = os.path.join(os.getcwd() + '/data/', ALIGNED)
        scores = os.path.join(os.getcwd() + '/data/', SCORES)
        aligner.align_and_score(corpus, aligned, scores)
        logging.debug("Wrote MLF file to '{}'.".format(aligned))
        logging.debug("Wrote likelihood scores to '{}'.".format(scores))
        logging.info("Writing TextGrids.")
        size = MLF(aligned).write(os.getcwd() + '/data/')
        if not size:
            logging.error("No paths found!")
            exit(1)
        logging.debug("Wrote {} TextGrids.".format(size))
        logging.info("Success!")
        return render_template('complete.html')

@app.route('/return-files', methods=['GET'])
def return_file():
    return send_from_directory(directory=os.getcwd(), filename='OOV.txt', as_attachment=True)


@app.route('/download_textgrids', methods=['GET'])
def download_textgrids():
    zipf = zipfile.ZipFile('Name.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('data/'):
        for file in files:
            zipf.write('data/' + file)
    zipf.close()
    return send_file('Name.zip',
                     mimetype='zip',
                     attachment_filename='Name.zip',
                     as_attachment=True)
    #return send_from_directory(directory=(os.getcwd()+'/data'), filename='scores.csv', as_attachment=True)

if __name__=="__main__":
    app.debug = True
    app.run(port=4555, debug=True)
