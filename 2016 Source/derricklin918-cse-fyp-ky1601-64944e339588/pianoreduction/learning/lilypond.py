import os

import music21

from pianoreduction import config
"""
.. module:: lilypond
    :platform: Unix
    :synopsis: This module handles the conversion of MusicXML to .png files.

.. moduleauthor:: Derrick Lin <derricklin918@gmail.com>

"""

# TODO: module is not usable yet.
path = os.path.join(config.SCORE_DIR, 'SQ-Original-fixed.xml')

converted = music21.converter.subConverters.ConverterLilypond()
c = music21.converter.parse(path)
converted.write(c, fmt='lilypond',subformats=['png'])