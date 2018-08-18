import sys
import os
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

debug = 0
PDFDocument.debug = debug
PDFParser.debug = debug
CMapDB.debug = debug
PDFResourceManager.debug = debug
PDFPageInterpreter.debug = debug
PDFDevice.debug = debug


def convertfile(outfile,fname):
    rsrcmgr = PDFResourceManager(caching = True)

    outfp = open(outfile, 'w')
    device = TextConverter(rsrcmgr, outfp, codec = 'utf-8', laparams = LAParams(), imagewriter = None)

    fp = open(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    for page in PDFPage.get_pages(fp, pagenos = set(), maxpages = 0, password = '', caching = True, check_extractable = True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    
if __name__=='__main__':
    file_path = './'
    file_list = os.listdir(file_path)
    for file in file_list:
        name = file.split('.')
        if name[1].lower() == 'pdf':
            print(name[0]+'.txt')
            if not os.path.exists(os.path.join(file_path,name[0]+'.txt')):
                convertfile(name[0]+'.txt',file)
