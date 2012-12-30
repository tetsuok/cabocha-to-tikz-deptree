#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Tetsuo Kiso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

'''
A converter from Cabocha's output to tikz-dependency.

Cabocha is a popular japanese dependecy parser
(http://code.google.com/p/cabocha/).

Usage:
  $ ./converter.py [options] file

or
  $ cat file | ./converter.py

I assume that input data format is the output of 'cabocha -f1'.
See http://code.google.com/p/cabocha/ for details.

Please note that you should install XeLaTeX to compile the generated
latex file by this script.

Limitation:
Currently, I support only UTF-8.
'''

import exceptions
import optparse
import os
import sys

# In the future I might use this variable.
#ENCODE = 'utf-8'

class Error(exceptions.StandardError):
  pass

class FormatError(Error):
  pass

class Segment(object):

  def __init__(self):
    self.morphs = []
    self.id = None
    self.head = None

  def add(self, m):
    self.morphs.append(m)

  def is_root(self):
    return self.head == '-1'

  def to_str(self):
    return ''.join([m.split('\t')[0].encode('utf-8') for m in self.morphs])

  def __str__(self):
    return '\n'.join([m.encode('utf-8') for m in self.morphs])

  def __iter__(self):
    self.index = 0
    return self

  def next(self):
    if self.index >= len(self.morphs):
      self.index = 0
      raise StopIteration
    res = self.morphs[self.index]
    self.index += 1
    return res

def pp(sent):
  return ' '.join([seg.to_str() for seg in sent])

def sentence_to_deptext(sent):
  return ' \& '.join([seg.to_str() for seg in sent]) + ' \\\\'

def read_deptree(f):
  sentences = []
  sent = []
  segment = Segment()
  for l in f:
    if l.startswith('EOS'):
      sent.append(segment)
      sentences.append(sent)
      segment = Segment()
      sent = []
    # Parse a line to get information about a segment ID and head.
    elif l.startswith('*'):
      if segment.id is not None:
        sent.append(segment)
      segment = Segment()

      lis = l.rstrip().split(' ')
      if len(lis) != 5:
        raise FormatError('Illegal format:' + l)
      segment.id = lis[1]

      if lis[2].endswith('D'):
        segment.head = lis[2][:-1]
      else:
        raise FormatError('Illegal format:' + l)
    else:
      segment.add(l.rstrip().decode('utf-8'))
  return sentences

def wrap_depedge(h, m):
    return '\depedge{%d}{%d}{}' % (int(h)+1, int(m)+1)

def wrap_depedges(sent):
    return '\n'.join([wrap_depedge(seg.id, seg.head) for seg in sent if not seg.is_root()])

class LaTeXFormatter(object):

    def __init__(self, doc_opt, font, tikz_dep_opt, tikz_deptxt_opt):
        self.doc_opt = doc_opt
        self.font = font
        self.tikz_dep_opt = tikz_dep_opt
        self.tikz_deptxt_opt = tikz_deptxt_opt

    def latex_header(self):
        return '''\documentclass{%s}
\usepackage{tikz-dependency}
\usepackage{zxjatype}
\setjamainfont[Scale=0.8]{%s}
\\begin{document}''' % (self.doc_opt, self.font)

    def latex_footer(self):
        return '''\end{document}'''

    def print_tikz_dep(self, sent):
        print '''\\begin{dependency}[%s]
\\begin{deptext}[%s]
%s
\end{deptext}
%s
\end{dependency}''' % (self.tikz_dep_opt, self.tikz_deptxt_opt,
                       sentence_to_deptext(sent), wrap_depedges(sent))

# TODO: only tested on Mac OS X. Make sure the choice of default fonts
# on Windows and Linux is fine.
def set_default_font():
  '''Set up default font according to major platforms
  (Windows, Mac OS X, Linux).
  '''
  # Windows
  if os.name == 'nt':
    return 'Meiryo' # メイリオ
  # Mac OS X
  elif os.name == 'posix' and os.uname()[0] == 'Darwin':
    return 'Hiragino Kaku Gothic Pro W3'
  elif os.name == 'posix' and os.uname()[0] == 'Linux':
    return 'IPAPGothic'
  else:
    return 'IPAPGothic'

def parse_options():
  default_font = set_default_font()

  parser = optparse.OptionParser(usage='%prog [options] data')
  parser.add_option('--doc-option', dest='doc_opt', default='standalone',
                    help='the options of documentclass')
  parser.add_option('--font', dest='font', default=default_font,
                    help='Japanese font')
  parser.add_option('--dep-option', dest='dep_opt', default='theme = simple',
                    help='the option of the dependency environment')
  parser.add_option('--deptxt-option', dest='deptxt_opt', default='column sep=1em',
                    help='the option of the deptext environment')
  (options, unused_args) = parser.parse_args()
  return (options, unused_args)

def main():
  opts, unused_args = parse_options()
  tex_formatter = LaTeXFormatter(opts.doc_opt, opts.font, opts.dep_opt, opts.deptxt_opt)

  if len(unused_args) == 0:
    sents = read_deptree(sys.stdin)
  else:
    with open(unused_args[0]) as f:
      sents = read_deptree(f)

  for sent in sents:
    print tex_formatter.latex_header()
    tex_formatter.print_tikz_dep(sent)
    print tex_formatter.latex_footer()
    print

if __name__ == '__main__':
  main()
