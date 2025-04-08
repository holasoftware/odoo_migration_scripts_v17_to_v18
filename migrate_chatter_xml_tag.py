import os
import logging


from lxml import etree


logger = logging.getLogger(__file__)


def replace_to_chatter_tag(filepath):
    if not os.path.isfile(filepath):
        logger.warning("file does not exist: %s", filepath)
        return

    doc = etree.parse(filepath)
    root = doc.getroot()

    for element in doc.xpath(
        "//record[@model='ir.ui.view']/field[@name='arch' and @type='xml']//div[@class='oe_chatter ' or starts-with(@class, 'oe_chatter ') or ends-with(@class, 'oe_chatter ')"
    ):
        parent = element.getparent()
        parent.replace(element, etree.Element("chatter"))


if __name__ == "__main__":
    import sys

    for filepath in sys.argv[1:]:
        replace_to_chatter_tag(filepath)
