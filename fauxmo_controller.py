import fauxmo
import logging
import time
import RPi.GPIO as GPIO
from phat_handler import DisplayPiHat, statuses

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

class device_handler(debounce_handler):
    """Triggers on/off based on GPIO 'device' selected.
       Publishes the IP address of the Echo making the request.
    """
    TRIGGERS = {
        label:port for (label, port) in zip(statuses.keys(), range(52003, 52003 + len(statuses.keys())))
    }

    def __init__(self):
        display = DisplayPiHat()
        debounce_handler.__init__(self)

    def trigger(self, status):
        logging.info(f'status: {status}')
        display.update(status)

    def act(self, client_address, state, name):
        logging.info(f'State {state} on {name} from client @ {client_address}')

        # discard state as it's unnecessary
        self.trigger(str(name))
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: " + str(e))
            break
