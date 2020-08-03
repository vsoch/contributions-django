"""

Copyright (c) 2020, Vanessa Sochat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

CONTRIBUTIONS_DJANGO = {
    'gradient0': "",
    'gradient1': ""
}

"""

from django.conf import settings

DEFAULTS = {
    # Gradients (0 or weak to stronger)
    "GRADIENT0": "#eee",
    "GRADIENT1": "#d6e685",
    "GRADIENT2": "#8cc665",
    "GRADIENT3": "#44a340",
    "GRADIENT4": "#1e6823",
    # The name to appear in tooltips (e.g., 12 contributions)
    "ITEM_NAME": "contributions",
    # Include bootstrap style for outer part of template
    # set this to false if you already have it on your page
    "INCLUDE_BOOTSTRAP": True,
    "INCLUDE_FONTAWESOME": True,
    # The icon to show next to title. Set to None to remove.
    "ICON_CLASSES": "fa fa-calendar",
}

# The user can define a section for CONTRIBUTIONS_DJANGO
updates = getattr(settings, "CONTRIBUTIONS_DJANGO", DEFAULTS)

include_bootstrap = updates.get("INCLUDE_BOOTSTRAP", DEFAULTS["INCLUDE_BOOTSTRAP"])
include_fontawesome = updates.get(
    "INCLUDE_FONTAWESOME", DEFAULTS["INCLUDE_FONTAWESOME"]
)
icon_classes = updates.get("ICON_CLASSES", DEFAULTS["ICON_CLASSES"])

item_name = updates.get("ITEM_NAME", DEFAULTS["ITEM_NAME"])
gradient0 = updates.get("GRADIENT0", DEFAULTS["GRADIENT0"])
gradient1 = updates.get("GRADIENT1", DEFAULTS["GRADIENT1"])
gradient2 = updates.get("GRADIENT2", DEFAULTS["GRADIENT2"])
gradient3 = updates.get("GRADIENT3", DEFAULTS["GRADIENT3"])
gradient4 = updates.get("GRADIENT4", DEFAULTS["GRADIENT4"])
gradients = [gradient0, gradient1, gradient2, gradient3, gradient4]
