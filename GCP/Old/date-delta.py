from datetime import timedelta, date, time, datetime
import subprocess
import json

today = "{:%Y-%m-%d}".format(datetime.now())
past_str = "2017-05-16T01:49:27.988-07:00"
past = datetime.strptime(past_str, '%Y-%m-%d')

    # datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    # stopped_on = datetime.strptime( inst.tags['StoppedOn'], "%B %d, %Y at %H:%M:%S")

delta = today - past
print(detla)

<ryonagana> MaximB:  you just need to pay attention in json fiile what is list and what is  a dict..

import os
import sys

from datetime import timedelta, date, time, datetime


if __name__ == "__main__":

    past_str = "2017-05-14"
    past = datetime.strptime(past_str, '%Y-%m-%d')

    today = datetime.strptime("{:%Y-%m-%d}".format(datetime.now()), "%Y-%m-%d")

    diff = abs((today - past).days)

    if diff > 5:
        print ("Success?")
    else:
        print("Fail")



   with open("data.json", encoding="utf-8", mode="r") as f:
        data = json.load(f)

        data = data[0]
        interfaces = data['networkInterfaces'][0]
        print (interfaces['networkIP'])
