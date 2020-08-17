from .services import main_page_content, create_message_context_to_publish


def main_page(request):
    return main_page_content(request)


def create_and_publish_message(request):
    return create_message_context_to_publish(request)


