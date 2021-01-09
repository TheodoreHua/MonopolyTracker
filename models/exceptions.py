# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

class AlreadyChosenValue(Exception):
    """Raised when the user tries to update a value when it is already that value"""
    pass


class NotFound(Exception):
    """Raised when the user tries to access, modify, or delete something that can't be found"""
    pass


class LimitReached(Exception):
    """Raised when the user tries to purchase something that is already at the max/min number allowed"""
    pass


class PropertyNotOwned(Exception):
    """Raised when a property is modified when not owned"""
    pass


class PropertyAlreadyOwned(Exception):
    """Raised when a property is bought when already owned"""
    pass


class NotAuthorized(Exception):
    """Raised when a user tries to perform an action that it's not authorized to do"""
    pass


class NoPaymentNeeded(Exception):
    """Raised when a property is stepped on but the player is jailed or the property is mortgaged"""
    pass


class UnexpectedValue(Exception):
    """Raised when an unexpected value is loaded from data files"""
    pass
