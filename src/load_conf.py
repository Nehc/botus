import pip
from yaml import safe_load as load
#from gradio_client import Client
#from googletrans import Translator

#def import_or_install(package):
try:
    from munch import DefaultMunch
except ImportError:
    pip.main(['install', 'munch'])
    from munch import DefaultMunch 

config = DefaultMunch.fromDict(
            load(open('config.yaml')),
                object())

#translator = Translator()

#caption = Client(config.caption)
#whisper = Client(config.whisper)
#pdf_ocr = Client(config.pdf_ocr)