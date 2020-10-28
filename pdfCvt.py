import sys
import subprocess
import re


def convert_to( source, timeout=None):
    args = ['soffice/program/soffice.com', '--headless', '--convert-to', 'pdf',  source]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    return filename.group(1)
