import logging


def common_task(item):
    item["msgs"] = []
    message = item.get("message", "")
    if message:
        rendered_message = "\n\t{}\n\n".format(message)
        logging.info(rendered_message)
        print(rendered_message)
        item["msgs"].append({"text": message})
    else:
        item["failed"] = True
