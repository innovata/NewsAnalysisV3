import subprocess


def run():
    # subprocess.run("python -m unittest inews/test/mongo.py", shell=True, check=True)
    subprocess.run("python -m unittest inews/test/models.py", shell=True, check=True)
    # subprocess.run("python -m unittest inews/test/newspage.py", shell=True, check=True)
    # subprocess.run("python -m unittest inews/test/snapshot.py", shell=True, check=True)
    # subprocess.run("python -m unittest inews/test/iter.py", shell=True, check=True)
    # subprocess.run("python -m unittest inews/test/press/naver.py", shell=True, check=True)


if __name__ == "__main__":
    run()
