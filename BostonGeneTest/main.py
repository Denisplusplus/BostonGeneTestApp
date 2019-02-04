from flask import Flask
from flask import request
from redis import Redis
from rq import Queue
from rq.job import Job
from downloader import handleFile
import json

app = Flask(__name__)

queue = Queue(connection=Redis(), default_timeout=3600)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if (request.method == 'POST'):
        email   = None
        fileUrl = None    
        
        receivedData = request.values
        if (receivedData.get("email")):
            email  = receivedData['email']
        if (not receivedData.get("url")):
            return "Error", 400
        fileUrl = receivedData['url']
        filename = fileUrl.split("/")[-1]

        task = queue.enqueue_call(handleFile, args=(email, fileUrl, filename), result_ttl=86400) ### keep result for one day

        responseData = {}
        responseData["id"] = task.id
        return json.dumps(responseData)
    return "Error", 400


@app.route('/check', methods=['GET', 'POST'])
def check():
    if (request.method == 'GET'):
        receivedData = request.values
        taskId   = receivedData['id']

        try:    
            job = Job.fetch(taskId, connection=Redis())
            if job.is_finished:
                if (job.result == False):
                    responseData = {}
                    responseData["status"] = "error"
                    return json.dumps(responseData), 400
                responseData = job.result
                responseData["status"] = "done"
                return json.dumps(responseData), 200

            else:
                responseData = {}
                responseData["status"] = "running"
                return json.dumps(responseData), 202
        except:
            return "Not found", 404
    return "Error", 400


if __name__ == '__main__':
    app.run()
