"""
You must shut down all apps(Flask) when you run testing psql-module.

Usage :
python test.py True|False
"""
from subprocess import run

print(__doc__)

if __name__ == "__main__":
    print(f"\nFlask is running...?\nEnter 0(=False) or 1(=True) ")
    while True:
        try:
            v = int(input())
        except Exception as e:
            print(f"Please enter correctly.")
        else:
            apps_running = bool(v)
            break

    if apps_running:
        run("python -m unittest pychall/test/client.py", shell=True, check=True)
    else:
        run("python -m unittest pychall/test/psql.py", shell=True, check=True)
