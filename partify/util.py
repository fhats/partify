# Copyright 2011 Fred Hatfull
#
# This file is part of Partify.
#
# Partify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Partify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Partify.  If not, see <http://www.gnu.org/licenses/>.

"""Utilities that are useful elsewhere."""
import os

from flask import render_template as render_flask_template
from flask import request
from flask import session
import useragent


def render_template(template_path, **kwargs):
    """Designed to be a drop-in wrapper around :func:`flask.render_template`.

    Provides user-agent detection and redirects to mobile template versions if
    the user-agent matches a mobile device.

    :param template_path: The template name to use
    :type template_path: string
    """

    raw_ua = request.headers.get('User-Agent', '')
    ua = useragent.detect(raw_ua)

    if 'mobile' in request.args:
        session['force_mobile'] = True
    if 'full' in request.args:
        session['force_mobile'] = False

    if ua.device.family or session.get('force_mobile', False):
        template_path = os.path.join("mobile", template_path)
    return render_flask_template(template_path, **kwargs)
