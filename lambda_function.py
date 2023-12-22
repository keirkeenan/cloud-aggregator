import requests
import aiohttp
import asyncio
from random import randint
from time import sleep
import json
from flask import Flask, jsonify, request
import awsgi

app = Flask(__name__)
# def lambda_handler(event, context):
#     url_app0 = 'http://18.227.21.205:8012/jobs/1'
#     url_app1 = 'http://18.191.72.159:5001/userinfo/total_count'
#     url_app2 = 'http://18.227.21.205:8012/jobs/total_count'
#     url_app3 = 'https://application-microservice.uc.r.appspot.com/application/total_count'

#     data_app0 = requests.get(url_app0).json()
#     print(data_app0)
#     data_app1 = requests.get(url_app1).json()
#     print(data_app1)
#     data_app2 = requests.get(url_app2).json()
#     print(data_app2)
#     data_app3 = requests.get(url_app3).json()
#     print(data_app3)

#     aggregated_data = {
#         "app0": data_app0,
#         "app1": data_app1,
#         "app2": data_app2,
#         "app3": data_app3
#     }

#     return aggregated_data

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)
            # if randint(0,1)==1:
            #     sleep(0.5)
            return await response
            
async def run_async():
    url_app1 = 'http://18.226.185.252:5001/userinfo/total_count'
    url_app2 = 'http://18.223.237.70:8012/jobs/total_count'
    url_app3 = 'https://application-microservice.uc.r.appspot.com/application/total_count'

    # Use asyncio.gather to asynchronously fetch data from multiple endpoints
    data_app0, data_app1, data_app2, data_app3 = await asyncio.gather(
        fetch_data(url_app1),
        fetch_data(url_app2),
        fetch_data(url_app3)
    )
    aggregated_data = {
        "app1": data_app1,
        "app2": data_app2,
        "app3": data_app3
    }

    return aggregated_data
@app.route('/composite')
def index():
    return jsonify({"message":"Hello World"}),200

@app.route('/composite/total_count')
def total_count():
    return jsonify(asyncio.get_event_loop().run_until_complete(run_async())),200

#called when a new recruiter posts a new job
@app.route('/composite/add_jobs',methods=['POST'])
def add_jobs():
    url_app1 = 'http://18.223.237.70:8012/jobs'
    url_app2 = 'http://18.226.185.252:5001/userinfo'

    request_data = request.get_json()
    title = request_data['title']
    description = request_data['description']
    requirements=request_data['requirements']
    postedBy=request_data['postedBy']
    company=request_data['company']
    isVerified=request_data['isVerified']
    recruiterEmail=request_data['recruiterEmail']
    request_app1={'title':title,'description':description,'requirements':requirements,'postedBy':postedBy,'company':company,'isVerified':isVerified,"recruiterEmail":recruiterEmail}
    job=requests.post(url_app1,json=request_app1)
    job=job.get_json()

    name = request_data['postedBy']
    email=request_data['recruiterEmail']
    picture_url=request_data['picture_url']
    request_app2={'name':name,'email':email,'picture_url':picture_url}
    user:requests.post(url_app2,json=request_app2)
    user=user.get_json()

    return jsonify({"recruiterID":user,"jobID":job}),200

#get all jobs and applications posted by the recruiter
@app.route('/composite/recruiter_jobs')
def recruiter_jobs():
    url_app1 = 'http://18.223.237.70:8012/jobs'

    recruiterName = request.args.get('recruiterName')
    recruiterEmail = request.args.get('recruiterEmail')
    request_app1={'recruiterName':recruiterName,"recruiterEmail":recruiterEmail}
    url_app2 = 'https://application-microservice.uc.r.appspot.com/application/recruiter/'+recruiterEmail
    data1=requests.get(url_app1,request_app1)
    data2=requests.get(url_app2)
    data1=jsonify(data1)
    data2=jsonify(data2)

    return jsonify({"jobs":data1,"applications":data2}),200
    
            
def lambda_handler(event, context):
    
    return awsgi.response(app, event, context, base64_content_types={"image/png"})