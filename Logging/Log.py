def writeFile(error, string):
    with open('log.txt', 'a+', encoding="utf-8") as file:
        file.write(f"{error.upper()}  - {string}\n")