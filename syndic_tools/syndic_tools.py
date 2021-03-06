from random import randint
import random
import locale
import logging
import io
from PyPDF2 import PdfFileWriter, PdfFileReader

_logger = logging.getLogger(__name__)


class SyndicTools:
    def pass_generator(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw += alphabet[next_index]
        return mypw

    def login_generator(self, name):
        login = name.replace(' ', '')
        login = login.replace('-', '')
        rand = str(randint(0, 99))
        return login[:8]+rand

    def french_date(self, tr_date):
        try:
            locale.setlocale(locale.LC_ALL, 'fr_BE.utf8')
        except locale.Error:
            _logger.error('Local not settable')

        return tr_date.strftime('%A %d %B %Y')

    def merge_pdf(self, pdf_data):
        ''' Merge a collection of PDF documents in one
        :param list pdf_data: a list of PDF datastrings
        :return: a unique merged PDF datastring
        '''
        writer = PdfFileWriter()
        for document in pdf_data:
            reader = PdfFileReader(io.BytesIO(document), strict=False)
            for page in range(0, reader.getNumPages()):
                writer.addPage(reader.getPage(page))
        _buffer = io.BytesIO()
        writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()
        return merged_pdf
