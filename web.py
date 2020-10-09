#-*- coding:utf-8 -*-
#!/usr/bin/python
from flask import Flask
import rq_dashboard
import rq_scheduler_dashboard


app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/")

app.config.from_object(rq_scheduler_dashboard.default_settings)
app.register_blueprint(rq_scheduler_dashboard.blueprint,  url_prefix="/sched")


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=333)