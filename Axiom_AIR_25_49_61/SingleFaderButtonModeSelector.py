# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_AIR_25_49_61/SingleFaderButtonModeSelector.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from .consts import *

class SingleFaderButtonModeSelector(ModeSelectorComponent):
    u""" SelectorComponent that assigns single fader button to different functions """

    def __init__(self, mixer, fader_button):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._fader_button = fader_button
        self._mode_index = 0
        self._number_of_modes = 3
        self._flashing_button = None
        self._flashing_button_on = True
        self._flashing_reset_delay = 0
        self._register_timer_callback(self._on_timer)
        return

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        ModeSelectorComponent.disconnect(self)
        self._mixer = None
        self._fader_button = None
        self._flashing_button = None
        return

    def number_of_modes(self):
        return self._number_of_modes

    def update(self):
        super(SingleFaderButtonModeSelector, self).update()
        if self.is_enabled():
            strip = self._mixer.selected_strip()
            fader_button = self._fader_button
            self._flashing_button = None
            if self.song().view.selected_track != self.song().master_track:
                strip.set_solo_button(None)
                strip.set_arm_button(None)
                strip.set_mute_button(None)
                if self._mode_index == 0:
                    strip.set_mute_button(fader_button)
                    self._mode_toggle.send_value(AMB_FULL, True)
                elif self._mode_index == 1:
                    strip.set_solo_button(fader_button)
                    self._mode_toggle.send_value(AMB_FULL, True)
                    self._flashing_button = self._mode_toggle
                else:
                    strip.set_arm_button(fader_button)
                    self._mode_toggle.send_value(RED_FULL, True)
        return

    def _on_timer(self):
        if self._flashing_button != None:
            if self._flashing_reset_delay > 0:
                self._flashing_reset_delay -= 1
            else:
                self._flash()
                self._flashing_reset_delay = 5
        return

    def _flash(self):
        self._flashing_button.turn_off() if self._flashing_button_on else self._flashing_button.turn_on()
        self._flashing_button_on = not self._flashing_button_on