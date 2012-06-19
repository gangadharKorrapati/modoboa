from django import template
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from modoboa import userprefs
from modoboa.lib import events
from modoboa.lib.webutils import static_url

register = template.Library()

@register.simple_tag
def uprefs_menu(selection, user):
    entries = [
        {"name" : "profile",
         "url" : reverse("modoboa.userprefs.views.profile"),
         "label" : _("Profile")},
        {"name" : "preferences",
         "url" : reverse("modoboa.userprefs.views.preferences"),
         "label" : _("Preferences")},
        ]
    if user.group == 'SimpleUsers':
        entries.insert(0, {"name" : "forward",
                           "url" : reverse("modoboa.userprefs.views.forward"),
                           "modalcb" : "forwardform_cb",
                           "label" : _("Forward")})

    entries += events.raiseQueryEvent("UserMenuDisplay", "uprefs_menu", user)
    entries = sorted(entries, key=lambda e: e["label"])
    return render_to_string('common/menu.html', {
            "entries" : entries, 
            "css" : "nav nav-list",
            "selection" : selection,
            "user" : user
            })


@register.simple_tag
def user_menu(user, selection):
    entries = [
        {"name" : "user",
         "img" : "icon-user icon-white",
         "label" : user.fullname,
         "menu" : [
                {"name" : "settings",
                 "img" : "icon-list",
                 "label" : _("Settings"),
                 "url" : reverse("modoboa.userprefs.views.index")}
                ]}
        ]

    entries[0]["menu"] += \
        events.raiseQueryEvent("UserMenuDisplay", "options_menu", user) \
        + [{"name" : "logout",
            "url" : reverse("modoboa.auth.views.dologout"),
            "label" : _("Logout"),
            "img" : "icon-off"}]

    return render_to_string("common/menulist.html",
                            {"selection" : selection, "entries" : entries, "user" : user})

@register.simple_tag
def loadextmenu(selection, user):
    menu = events.raiseQueryEvent("UserMenuDisplay", "top_menu", user)
    return render_to_string('common/menulist.html', 
                            {"selection" : selection, "entries" : menu, "user" : user})
