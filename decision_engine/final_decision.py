def final_decision(ats, semantic, education):

    final = (
        ats * 0.4 +
        semantic * 0.4 +
        education * 0.2
    )

    if final >= 60:
        status = "Selected"
    elif final >= 45:
        status = "Moderate"
    else:
        status = "Rejected"

    return final, status