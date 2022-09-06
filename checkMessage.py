def checkMessage(text,official_devices):
    finalAnswer = ""
    for codeName in official_devices:
        if text == "/release "+ codeName:
            finalAnswer = codeName
    if finalAnswer:
        return finalAnswer
    else:
        return False