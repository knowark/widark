Detect Shift, Ctrl and Alt Keys in Events
=========================================

:estimark:
    state=cancelled

Mouse and Keyboard Events should know if the Shift, Ctrl and Alt keys 
are being pressed.


Validation Criteria
-------------------

- When the shift, ctrl or alt keys are hold while clicking or typing, they
  will be reported as individual elements in event instances.

Notes
-----

Apparently this is not an easy task in ncurses. There might be workarounds,
like the one proposed in https://stackoverflow.com/questions/9750588/\
how-to-get-ctrl-shift-or-alt-with-getch-ncurses, but still this might suppose
a great effort for too little gain in real applications. If the need arises
again in the future, this issue might be reopened.