# Odoo migration scripts from v17 to v18
Scripts for the migration of odoo version 17 to 18.

`migrate_tree_to_list_xml_tag.py`: Change tree tag to list tag.

`migrate_chatter_xml_tag.py`: Change the tag `<div class="oe_chatter">...</div>` to `<chatter/>` tag.


## Installation
Install `lxml`:
```
pip install lxml
```

## Usage
Run the python migration scripts with the file paths to the xml view files intended to change as command line arguments. For example:
```
python migrate_tree_to_list_xml_tag.py file1.xml file2.xml ...
```
Or also:
```
python migrate_tree_to_list_xml_tag.py views/*.xml
```

## Some changes from v17 to v18
- Instead of tree tag in xml views, odoo 18 uses list tag
- Odoo makes more simple to use the chatter widget. Now it's only necessary to use `<chatter/>` instead of `<div class="oe_chatter">...</div>`.
- Removed `numbercall` field from model `ir.cron`
- Operator 'inselect' for domains does not exists. Instead, use 'in' and create a Select expression inside an SQL odoo instance (odoo.tools.SQL)
- In class IrBinary, there is an extra parameter `field` in the instance method `_find_record_check_access`.