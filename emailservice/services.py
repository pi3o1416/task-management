
import re

def get_args_from_task_args(task_args):
    splited_task_args = re.findall("'(.+?)'", task_args)
    email_subject = splited_task_args[0]
    email_body = splited_task_args[-1]
    email_to = splited_task_args[1:-1]
    return email_subject, email_body, email_to
