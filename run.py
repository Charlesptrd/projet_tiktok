# run.py
import sys
import os

if len(sys.argv) < 2:
    print("Usage : python run.py [script]")
    sys.exit(1)

target = sys.argv[1]

os.system(f"python {target}")