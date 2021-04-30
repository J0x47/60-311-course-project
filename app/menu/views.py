from flask import render_template
from app.models import MenuItem
from . import menu_blueprint as menu

@menu.route('/menu')
def list_menuitems():
    """
    List all departments
    """
    menu_items = MenuItem.query.all()
    return render_template('menu/menu_item_list.html',
                           object_list=menu_items, title="Menu")


@menu.route('/menu/<pid>')
def menuItemDetail(pid):
    """
    List all departments
    """
    menu_item = MenuItem.query.filter_by(id=pid).first()
    return render_template('menu/menu_item_detail.html',
                           food=menu_item, title="Menu item")