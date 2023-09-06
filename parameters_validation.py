def title_validation(data):
    status = 0
    title = ["inv.", "invoice", "gst"]
    for parameter in title:
        if parameter in data or parameter.upper() in data or parameter.capitalize() in data :
            status = 1
    return [status, data]