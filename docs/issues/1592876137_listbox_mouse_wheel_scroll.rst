Listbox Mouse Wheel Scroll
==========================

Listbox scrolling should be available by default using the mouse
wheel.

Validation Criteria
-------------------

- When a full listbox receives a mousewheel up event, it will offset up
  its data list contents. The minimum offset is of course zero.
- When a full listbox receives a mousewheel down event, it will offset down
  its data list contents. The maximum offset must be: len(data) - limit.
