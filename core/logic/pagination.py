from django.core.paginator import InvalidPage

import logging
logger = logging.getLogger('monkeyladder')


def get_page(paginator, page_number):
    """
    Returns the requested page from the paginator

    If any errors occur the first page is returned
    """
    try:
        return paginator.page(page_number)
    except InvalidPage:
        return paginator.page(1)


def get_page_with_item(paginator, item_id):
    for page_number in range(1, paginator.num_pages + 1, 1):
        page = paginator.page(page_number)
        if int(item_id) in [item.pk for item in page]:
            return page
    logger.debug("Could not find page with object id: %s" % item_id)
    return paginator.page(1)
