import sys

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from pypaecLexer import pypaecLexer
from pypaecParser import pypaecParser

TEXT_WINDOW = 10
CARAT_SPACER = TEXT_WINDOW // 2  # integer division; implicit round.


class HighlightingErrorListener(ErrorListener):
    syntaxErrors: list = []
    ambiguities: list = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        input_text: str = recognizer.getInputStream().getText()
        column_num: int = int(column)
        input_len = len(input_text)
        # Get either 5 characters before the error, or the start position (if the error occurs
        # less than 5 characters from the beginning). Do the same for the end.
        line_start_pos: int = max(column_num - TEXT_WINDOW, 0)
        line_start_elipsis: str = "..." if line_start_pos != 0 else ""
        line_end_pos: int = min(column_num + TEXT_WINDOW, input_len - 1)
        line_end_elipsis: str = "..." if line_end_pos != input_len - 1 else ""
        line_start_len: int = len(line_start_elipsis)
        # Select a segment from the input text to display.
        input_error_segment: str = input_text[line_start_pos:line_end_pos]

        message: str = f"Error: {msg}: line {line}, column {column}"
        location: str = f"{line_start_elipsis}{input_error_segment}{line_end_elipsis}"
        highlight: str = f"{' ' * line_start_len}{' ' * CARAT_SPACER}{'^' * TEXT_WINDOW}"

        self.syntaxErrors.append({
            "type": "syntaxError",
            "msg": message,
            "input": input_text,
            "location": location,
            "highlight": highlight
        })

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        input_text = recognizer.getInputStream().getText()
        ambiguous_section = recognizer.getInputStream().getText()[startIndex:stopIndex]

        self.ambiguities.append({
            "type": "ambiguity",
            "msg": f"Ambiguous input: start {startIndex}, stop: {stopIndex}",
            "input": input_text,
            "location": ambiguous_section
        })


def parse_incipit(incipit: str) -> dict:
    input_stream = InputStream(incipit)
    lexer = pypaecLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(HighlightingErrorListener())

    stream = CommonTokenStream(lexer)

    parser_listener = HighlightingErrorListener()
    parser = pypaecParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(parser_listener)

    tree = parser.incipit()
    num_errors: int = tree.parser.getNumberOfSyntaxErrors()

    return {
        "valid": num_errors == 0,
        "num_errors": num_errors,
        "syntax_errors": parser_listener.syntaxErrors,
        "ambiguities": parser_listener.ambiguities
    }


if __name__ == "__main__":
    parse_results = parse_incipit(sys.argv[1])
    print(parse_results)
