# Plaine and Easie Grammar

This repository contains a formal grammar for [Plaine & Easie code](https://www.iaml.info/plaine-easie-code) (PAEC), the format used by [RISM](https://rism.info) for encoding musical incipits in [MARC21](https://www.loc.gov/marc/bibliographic/bd031.html). The grammar provides validation for PAEC input.

This grammar was originally written by David Rizo. It is being maintained by the [RISM Digital Center](https://rism.digital). Please see the version history for more details.

Currently this grammar is experimental. The PAEC specification has some ambiguities that need to be clarified.

## Using

An experimental Python 3 version of the PAEC parser has been built that will collect the syntax errors and grammar ambiguities, and provide them as a list of dictionaries.

It requires the ANTLR Python runtime to work: 

    $ pip3 install antlr4-python3-runtime

You can validate a single incipit on the command line:

    $ python pypaec/pypaec.py "%G-2@c$bB ''4G8D'4BG/''4.bE8F4.D({6DExF})/4G{8AB}4.At8G/4.xF8D'4.A8B/"

You can also use the parser in your own code. Assuming you have a list of incipits in `list_of_incipits`:

```python
    from pypaec.pypaec import parse_incipit
    import csv


    list_of_incipits: list = [ ... ]
    to_check: list = []
    num_incipits: int = len(list_of_incipits)
    
    for incipit in list_of_incipits:
        parse_results: dict = parse_incipit(incipit)
        is_valid: bool = parse_results.get("valid")

        if not is_valid:
            syntax_errors: dict = parse_results.get("syntax_errors")

            to_check.append({
                "incipit": incipit,
                "segment": "\n".join([serr.get("location") for serr in syntax_errors]),
                "message": "\n".join([smsg.get("msg") for smsg in syntax_errors])
            })

    with open("incipit_report.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["incipit", "segment", "message"])
        writer.writeheader()
        writer.writerows(to_check)

    num_errors = len(to_check)

    print(f"Number of incipits checked: {num_incipits}")
    print(f"Number of incipits to check: {num_errors}")
    print(f"Error rate: {(num_errors / num_incipits) * 100}%")
```

Check the source code in `pypaec/pypaec.py` for more details about the contents of the results of the `parse_incipit` function.

## Building

Libraries for using the PAEC grammar can be generated with the ANTLR command-line tools. For example, to generate the Python library:

    $ antlr -o pypaec -Dlanguage=Python3 pypaec.g4

This will generate a Python 3 library, with the source files stored in the `pypaec` directory. See the ANTLR documentation for a [list of target languages](https://github.com/antlr/antlr4/blob/master/doc/targets.md).

Don't forget to re-generate the grammar after you've made changes!

## Version History

This grammar was written primarily by David Rizo in 2013. The [details of the grammar](/docs/rizo-iñesta-2013.pdf) are published in:

Rizo, D.; and Iñesta, J. M. *A Grammar for Plaine and Easie Code*. In Roland, P.; and Kepper, J., editor(s), Music Encoding Conference Proceedings 2013 and 2014, pages 54–64, 2016. Bavarian State Library (BSB)

## License

The Plaine & Easie Code grammar and associated libraries are available under the LGPL license (see COPYING and COPYING.LESSER).
