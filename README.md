# Plaine and Easie Grammar

This repository contains a formal grammar for [Plaine & Easie code](https://www.iaml.info/plaine-easie-code) (PAEC), the format
used by [RISM](https://rism.info) for encoding musical incipits. The grammar provides validation for PAEC input.

This grammar is being maintained by the [RISM Digital Center](https://rism.digital). Please see the version history for more details.

## Using

## Building

Libraries for using the PAEC grammar can be generated with ANTLR. For example, to generate a Python library:

    $ antlr -o pypaec -Dlanguage=Python3 pypaec.g4

This will generate a Python 3 library, with the source files stored in the `pypaec` directory. See the ANTLR documentation for a [list of target languages](https://github.com/antlr/antlr4/blob/master/doc/targets.md)

## Version History

This grammar was written primarily by David Rizo in 2013. The [details of the grammar](/docs/rizo-iñesta-2013.pdf) are published in:

Rizo, D.; and Iñesta, J. M. *A Grammar for Plaine and Easie Code*. In Roland, P.; and Kepper, J., editor(s), Music Encoding Conference Proceedings 2013 and 2014, pages 54–64, 2016. Bavarian State Library (BSB)

## License

The Plaine & Easie Code grammar and associated libraries are available under the LGPL license (see COPYING and COPYING.LESSER).
