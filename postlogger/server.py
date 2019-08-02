import os
from urllib.parse import parse_qs
import json
from datetime import datetime
import time

def app(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])
    request_method = env["REQUEST_METHOD"]
    log_path = os.environ["POSTLOGGER_LP"]
    if request_method == "POST":
        wsgi_data = env["wsgi.input"].read(0)
        post_content_pre = wsgi_data.decode('unicode_escape')
        post_content = parse_qs(post_content_pre)
        post_content_post = {}
        for k in post_content:
            post_content_post[k] = post_content[k][0]
        if "topic" not in post_content_post:
            post_content_post["topic"] = "default"
        if "echo" not in post_content_post:
            post_content_post["echo"] = "0"
        post_content_post["datetime"] = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")[:-3] + " " + time.tzname[0]
        e = post_content_post.pop("echo")
        r_string = json.dumps(post_content_post, ensure_ascii=False)
        with open(log_path, "a+") as f:
            f.write(r_string + "\n")
        if e != "0":
            return(r_string.encode("utf-8"))
