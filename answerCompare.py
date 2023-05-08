def answerMatch(answer,modAnswer):
    #TODO:complicated match

    #simple == match:
    if (answer==modAnswer) or (answer in modAnswer) or (modAnswer in answer):
        return True
    else:
        return False