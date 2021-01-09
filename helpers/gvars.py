# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from .file import get_defaults, get_config, assert_data

assert_data()
CONFIG = get_config()
DEFAULTS = get_defaults()
VERSION = "1.0.0"
