
import re

def get_args_from_task_kwargs(task_kwargs):
    splited_task_args = re.findall("{(.+?)}", task_kwargs)[0]
    splited_task_args = re.findall("'(.+?)'", splited_task_args)
    email_subject = splited_task_args[1]
    email_body = splited_task_args[5]
    email_to = splited_task_args[3]
    return email_subject, email_body, email_to
