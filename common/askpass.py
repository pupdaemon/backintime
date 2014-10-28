#!/usr/bin/env python3
#    Copyright (C) 2012-2014 Germar Reitze
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys
import base64
try:
    import gtk
except:
    pass

import password
import password_ipc
import tools
import config

if __name__ == '__main__':
    """
    return password.
    """
    cfg = config.Config()
    tools.load_env(cfg.get_cron_env_file())

    profile_id = os.getenv('ASKPASS_PROFILE_ID', '1')
    mode = os.getenv('ASKPASS_MODE', 'local')

    temp_file = os.getenv('ASKPASS_TEMP')
    if temp_file is None:
        #normal mode, get password from module password
        pw = password.Password(cfg)
        print(pw.get_password(None, profile_id, mode))
        sys.exit(0)

    #temp mode
    fifo = password_ipc.FIFO(temp_file)
    pw_base64 = fifo.read(5)
    if pw_base64:
        print(base64.decodebytes(pw_base64.encode()).decode())
