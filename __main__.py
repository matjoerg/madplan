import sys
import os
mainpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mainpath+'/madplan')
import madplan.console
from flask import Flask

app = Flask(__name__)

print(madplan.console.print_madplan())
