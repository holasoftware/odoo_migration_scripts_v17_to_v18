import os
import logging
import ast


from lxml import etree


logger = logging.getLogger(__file__)


class DictKeyReplacer(ast.NodeTransformer):
    def __init__(self, dict_mapping, *args, **kwargs):
        self.dict_mapping = dict_mapping
        super().__init__(*args, **kwargs)

    def visit_Dict(self, node):
        new_keys = []
        for key in node.keys:
            if isinstance(key, ast.Constant) and key.value in self.dict_mapping:
                new_keys.append(ast.Constant(value=self.dict_mapping[key.value]))
            else:
                new_keys.append(key)

        node.keys = new_keys
        return node


def replace_dict_keys(source_code, dict_mapping):
    tree = ast.parse(source_code.strip())

    transformer = DictKeyReplacer(dict_mapping)
    modified_tree = transformer.visit(tree)

    return ast.unparse(modified_tree)


def replace_tree_to_list_tag(filepath):
    if not os.path.isfile(filepath):
        logger.warning("file does not exist: %s", filepath)
        return

    doc = etree.parse(filepath)
    root = doc.getroot()

    for element in doc.xpath("//record[@model='ir.ui.view']/field[@name='arch']//tree"):
        element.tag = "list"

    for element in doc.xpath("//record[@model='ir.ui.view']//field[@mode='tree']"):
        element.attrib["mode"] = "list"

    for element in doc.xpath(
        "//record[@model='ir.actions.act_window']/field[@name='view_mode']"
    ):
        element.text = ",".join(
            [
                "list" if view_mode == "tree" else view_mode
                for view_mode in element.text.split(",")
            ]
        )

    for element in doc.xpath(
        "//record[@model='ir.actions.act_window']/field[@name='context']"
    ):
        old_context = element.text
        context = replace_dict_keys(old_context, {"tree_view_ref": "list_view_ref"})
        element.text = context

    for element in doc.xpath(
        "//record[@model='ir.ui.view']/field[@name='arch' and @type='xml']//*[@context]"
    ):
        old_context = element.attrib["context"]
        context = replace_dict_keys(old_context, {"tree_view_ref": "list_view_ref"})
        element.attrib["context"] = context

    doc.write(filepath, pretty_print=True, encoding="utf-8")


if __name__ == "__main__":
    import sys

    for filepath in sys.argv[1:]:
        replace_tree_to_list_tag(filepath)
