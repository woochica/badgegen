#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import sys
from django.conf import settings
from django.template.loader import render_to_string


__author__ = 'slink'


class Card(object):
    roles = (u'Ismerkedő', u'Webmester', u'Sminkmester', u'Programozó')


class LatexDocument(object):
    def __init__(self, infile):
        f = open(infile, 'r')
        data = []
        reader = csv.reader(f)
        for name, nick, company, position, raw_role in reader:
            active_roles = raw_role.decode('utf-8').split("\n")
            data.append({'name': self.escape(name),
                         'nick': self.escape(nick),
                         'company': self.escape(company),
                         'position': self.escape(position),
                         'roles': [(role, role in active_roles) for role in Card.roles]})
        f.close()
        self.cards = data

    def escape(self, value):
        uni_value = value.decode('utf-8')
        uni_value = uni_value.replace('_', '\_')
        uni_value = uni_value.replace('&', '\&')
        return uni_value

    def render(self, template):
        self._rendered = render_to_string(template, {'cards': self.cards})

    def write(self, outfile):
        out = open(outfile, 'w')
        out.write(self._rendered.encode('utf-8'))
        out.close()


if __name__ == '__main__':
    try:
        (infile, outfile, template) = sys.argv[1:]
    except ValueError:
        print('Usage: python gentex.py infile outfile template')
        sys.exit(2)
    settings.configure(TEMPLATE_DIRS=(os.path.dirname(__file__), ))
    doc = LatexDocument(infile)
    doc.render(template)
    doc.write(outfile)
