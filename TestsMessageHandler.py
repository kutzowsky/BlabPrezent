#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from MessageHandler import MessageHandler


class TestsMessageHandler(object):
    def test_handle_should_not_throw(self):
        MessageHandler.handle('some mesage ofiejfoiewniWBW')
