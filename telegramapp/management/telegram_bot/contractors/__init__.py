from .state import ContractorState as State

from . import handlers, send, keyboards, storage


def entrypoint_with_no_role(context, chat_id, message_id):
    send.tos(context, chat_id, message_id)
    send.resume_request(context, chat_id)
    return State.RESUME_REQUEST.value


def entrypoint_with_role(context, chat_id, message_id):
    is_active = storage.is_active(chat_id)
    if not is_active:
        send.account_on_review(context, chat_id, message_id)
        return State.ACCOUNT_ON_REVIEW.value

    send.home(context, chat_id, message_id)
    return State.HOME.value
