Listbox Mouse Wheel Scroll
==========================

Listbox scrolling should be available by default using the mouse
wheel.

Validation Criteria (*Deprecated*)
----------------------------------

- When a full listbox receives a mousewheel up event, it will offset up
  its data list contents. The minimum offset is of course zero.
- When a full listbox receives a mousewheel down event, it will offset down
  its data list contents. The maximum offset must be: len(data) - limit.


Negotiation
-----------

Considering that the Python implementation of curses doesn't handle mouse
scrolling properly, it was decided to instead use the **Page Up** and 
**Page Down** keys for pagination.


New Validation Criteria
-----------------------

- [X] When a full listbox receives a **page up keydown** event, it will 
  offset up its data list contents. The minimum offset is of course zero.
- [X] When a full listbox receives a **page down keydown**, it will offset down
  its data list contents. The maximum offset must be: len(data) - limit.
