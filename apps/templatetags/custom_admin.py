import copy
from typing import List, Dict

from django.contrib.auth.models import User
from django.template import Context, Library
from jazzmin.settings import get_settings
from jazzmin.utils import make_menu, order_with_respect_to

register = Library()


@register.simple_tag(takes_context=True)
def get_side_menu(context: Context, using: str = "available_apps") -> List[Dict]:
    """
    Get the list of apps and models to render out in the side menu and on the dashboard page
    """
    user: User = context.get("user")
    if not user:
        return []

    options = get_settings()
    ordering = options.get("order_with_respect_to", [])
    ordering = [x.lower() for x in ordering]

    menu = []
    available_apps = copy.deepcopy(context.get(using, []))

    custom_links = {
        app_name: make_menu(user, links, options, allow_appmenus=False)
        for app_name, links in options.get("custom_links", {}).items()
    }

    for app in available_apps:
        app_label = app["app_label"].lower()
        app_custom_links = custom_links.get(app_label, [])
        app["icon"] = options["icons"].get(app_label, options["default_icon_parents"])
        app["type"] = 'regular'
        if app_label in options["hide_apps"]:
            continue

        menu_items = []
        for model in app.get("models", []):
            model_str = "{app_label}.{model}".format(app_label=app_label, model=model["object_name"]).lower()
            if model_str in options.get("hide_models", []):
                continue

            model["url"] = model["admin_url"]
            model["model_str"] = model_str
            model["icon"] = options["icons"].get(model_str, options["default_icon_children"])
            menu_items.append(model)

        menu_items.extend(app_custom_links)

        custom_link_names = [x.get("name", "").lower() for x in app_custom_links]
        model_ordering = list(
            filter(
                lambda x: x.lower().startswith("{}.".format(app_label)) or x.lower() in custom_link_names,
                ordering,
            )
        )

        if len(menu_items):
            if model_ordering:
                menu_items = order_with_respect_to(
                    menu_items,
                    model_ordering,
                    getter=lambda x: x.get("model_str", x.get("name", "").lower()),
                )
            app["models"] = menu_items
            menu.append(app)

    if ordering:
        apps_order = list(filter(lambda x: "." not in x, ordering))
        menu = order_with_respect_to(menu, apps_order, getter=lambda x: x["app_label"].lower())

    return menu
