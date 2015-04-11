#!/usr/bin/env python
from flask import Flask, jsonify, make_response, abort, request
from flask_cors import CORS
import shelve
from streamdownloader import StreamDownloader

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
d = shelve.open("datastore.db")
streams = []
if d.has_key("streams"):
    streams = d["streams"]

streamDownloader = StreamDownloader()
for stream in streams:
    streamDownloader.add(stream['channel'])


@app.route('/streams', methods=['GET'])
def get_streams():
    for stream in streams:
        stream['channel_status'] = streamDownloader.getChannelStatus(stream['channel'])
        if streamDownloader.contain(stream['channel']):
            stream['process_status'] = 'started'
        else:
            stream['process_status'] = 'stopped'
        
    return jsonify({'streams': streams})

@app.route('/streams/<string:channel>', methods=['GET'])
def get_stream(channel):
    stream = filter(lambda t: t['channel'] == channel, streams)
    if len(stream) == 0:
        abort(404)
    stream[0]['channel_status'] = streamDownloader.getChannelStatus(channel)
    if streamDownloader.contain():
        stream[0]['process_status'] = 'started'
    else:
        stream[0]['process_status'] = 'stopped'
    return jsonify({'stream': stream[0]})

@app.route('/streams', methods=['POST'])
def create_stream():
    if not request.json or not 'channel' in request.json:
        abort(400)
    streamDownloader.add(request.json['channel'])
    stream = {
        'channel': request.json['channel'],
        'channel_status': streamDownloader.getChannelStatus(request.json['channel']),
    }
    if streamDownloader.contain(request.json['channel']):
        stream['process_status'] = 'started'
    else:
        stream['process_status'] = 'stopped'

    streams.append(stream)
    d["streams"] = streams
    return jsonify({'stream': stream}), 201

@app.route('/streams/<string:channel>', methods=['PUT'])
def update_stream(channel):
    stream = filter(lambda t: t['channel'] == channel, streams)
    if len(stream) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'process_status' in request.json:
        action = request.json['process_status']
        if action == 'stopped' and streamDownloader.contain(channel):
            streamDownloader.delete(channel)
        elif action == 'started' and not streamDownloader.contain(channel):
            streamDownloader.add(channel)
            
    stream[0] = {
        'channel': channel,
        'channel_status': streamDownloader.getChannelStatus(channel),
    }
    if streamDownloader.contain(channel):
        stream[0]['process_status'] = 'started'
    else:
        stream[0]['process_status'] = 'stopped'


    d["streams"] = streams
    return jsonify({'stream': stream[0]})

@app.route('/streams/<string:channel>', methods=['DELETE'])
def delete_stream(channel):
    stream = filter(lambda t: t['channel'] == channel, streams)
    if len(stream) == 0:
        abort(404)
    streams.remove(stream[0])
    d["streams"] = streams
    streamDownloader.delete(channel)
    return jsonify({'result': True})



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
