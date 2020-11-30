from flask import Flask, render_template, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import gcp_utils
import uuid
from kafka import KafkaProducer

app = Flask(__name__)

BUCKET_NAME = 'datacenter_project_bucket'
producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      blob_name_uuid = str(uuid.uuid4())
      fin = f.stream.read()
      # temp2 = f.stream.read()
      # temp = secure_filename(f.filename)
      # with open(temp, 'rb') as fin:
      #    print(fin)
      # print(type(temp))
      gcp_utils.upload_blob_from_string(BUCKET_NAME, fin, blob_name_uuid)
      producer.send('foobar', fin)
      # gcp_utils.detect_document_from_file(fin)
      # f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=5000)