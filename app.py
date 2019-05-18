from flask import Flask, render_template, jsonify
import time
import subprocess
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/_get_data/', methods=['POST'])
def _get_data():
    #subprocess.run((["python3", "dep1.py"]))
    #while(1):
    #sys.stdout=open('result%s.txt' % scriptInstance,'w')
      #sleep(1)
      subprocess.run((["python3", "dep2.py"]))
      f= open("extension/p","r")

    #myList = [true, false]
      true=f.readline()
      false=f.readline()
      f.close()
  
      myList=["Total number of depressive queries in the latest searches :" + " "+ str(true)+ " ","Out of recent 1000 searches!!!"]
      return jsonify({'data': render_template('response.html', myList=myList)})


if __name__ == "__main__":
    subprocess.run((["python3", "dep1.py"]))
    app.run(debug=True)

