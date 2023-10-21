from datetime import datetime
now = datetime.now()

def writeFile(error, string, traceback):
    with open('log.txt', 'a+', encoding="utf-8") as file:
        file.write(f"{now} - {error.upper()}  - {string} - \n{str(traceback)}\n\n")