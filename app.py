#coding=utf-8
from rockpi_detection import fname
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def states():
    content = '<pre>'
    with open(fname) as f:
        lines = f.readlines()
    content += "".join(lines)
    content += '</pre>'


    # return content
    return content

if __name__ == '__main__':
    app.run(host="10.214.211.208", port="9999")