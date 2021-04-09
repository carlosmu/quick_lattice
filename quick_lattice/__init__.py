# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Quick Lattice",
    "author" : "carlosmu <carlos.damian.munoz@gmail.com>",    
    "blender" : (2, 83, 0),
    "version" : (0, 8, 0),
    "category" : "User",
    "location" : "3D View > Object Right-Click Context Menu",
    "description" : "Automating the process of warping an object in a lattice cage.",
    "warning" : "",
    "doc_url" : "https://blendermarket.com/products/quick-lattice",
    "tracker_url" : "https://blendermarket.com/creators/carlosmu",
}

import bpy

from . import draw_button
from . import op_quick_lattice
from . import pt_quick_lattice
from . import user_prefs

####################################
# REGISTER/UNREGISTER
####################################
def register():
    draw_button.register()
    op_quick_lattice.register() 
    pt_quick_lattice.register() 
    user_prefs.register()   
        
def unregister():
    draw_button.unregister()
    op_quick_lattice.unregister() 
    pt_quick_lattice.unregister() 
    user_prefs.unregister() 