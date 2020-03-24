
import logging
import os
from subprocess import check_output
from phat_handler import DisplayPiHat, statuses
from flask import Flask, Response

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

port_ctr = 12340
def get_device(status_key):
    global port_ctr
    d = {
        "port": port_ctr,
        "on_cmd": f'http://localhost:5001/update/{status_key}',
        "off_cmd": f'http://localhost:5001/update/free',
        "method": "GET",
        "name": f'door-sign {status_key}',
        "use_fake_state": True
    }
    port_ctr = port_ctr + 1
    return d

@app.route('/')
def index():
    return "Hello from weatherpi!"

@app.route('/update/<status>')
def update_status(status):
    print(status)
    keys = list(statuses.keys())
    if status in keys:
        display.update(status)
        return Response(status=200)
    else:
        return Response(status=404)

if __name__ == "__main__":
    # build config.json
    device_list = [get_device(status_key) for status_key in statuses.keys()]
    devices_str = str(device_list).replace('\'', '\"').replace('True', 'true')
    with open("config_template.json", "rt") as fin:
        with open("config.json", "wt") as fout:
            for line in fin:
                fout.write(line.replace('[%DEVICE-LIST%]', devices_str))

    # start fauxmo in the background
    try:
        check_output('(exit "$(ps aux | grep \'[f]auxmo -c config.json\' | wc -l)")', shell=True)
        start_cmd = 'fauxmo -c config.json &'
        os.system(start_cmd)
        logging.debug('fauxmo service started')
    except Exception as e:
        logging.exception('fauxmo service already started!')

    # start flask server
    display = DisplayPiHat()
    app.run(host='0.0.0.0', port=5001)
