import os
import requests


def run(data, topic = "default", echo = "0"):
    c_uri = os.environ["PLC_BASE_URI"]
    data.update({"topic": topic, "echo": echo})
    return(requests.post(c_uri, data = data))
