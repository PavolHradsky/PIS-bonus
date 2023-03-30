def get_sickness(data):
    sick1, sick2, sick3, sick4, healthy = [], [], [], [], []
    sick1.append(data[1]["Žena"])
    sick2.append(data[1]["Muž"])

    healthy.append(data[0]["young"])
    sick1.append(data[0]["middle-age"])
    sick2.append(data[0]["middle-age"])
    sick3.append(data[0]["old"])
    sick4.append(data[0]["old"])

    healthy.append(data[2]["medium"])
    sick1.append(data[2]["short"])
    sick2.append(data[2]["short"])
    sick3.append(data[2]["medium"])
    sick4.append(data[2]["tall"])

    healthy.append(data[3]["average"])
    sick1.append(data[3]["thin"])
    sick2.append(data[3]["thin"])
    sick3.append(data[3]["average"])
    sick4.append(data[3]["overweight"])

    return {"sick1": max(sick1), "sick2": max(sick2), "sick3": max(sick3), "sick4": max(sick4), "healthy": max(healthy)}
