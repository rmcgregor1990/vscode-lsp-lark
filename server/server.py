from pygls.features import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                            TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN)
from pygls.server import LanguageServer
from pygls.types import (CompletionItem, CompletionList, CompletionParams, Diagnostic,
                         DidChangeTextDocumentParams,
                         DidCloseTextDocumentParams, DidOpenTextDocumentParams, Position, Range)

from .error_reporting_lalr import parse, JsonSyntaxError


class LarkJsonLanguageServer(LanguageServer):
    CONFIGURATION_SECTION = 'jsonServer'

    def __init__(self):
        super().__init__()


json_server = LarkJsonLanguageServer()


def _validate(ls, params):
    ls.show_message_log('Validating json...')

    text_doc = ls.workspace.get_document(params.textDocument.uri)

    source = text_doc.source
    diagnostics = _validate_json(source) if source else []

    ls.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_json(source: str):
    """Validates json file using lark and returns Diagnostics"""
    diagnostics = []

    try:
        parse(source)
    except JsonSyntaxError as e:
        msg, line, col = e.args
        msg = f"{e.__class__.__name__}:\n{msg}"

        d = Diagnostic(
            Range(
                Position(line - 1, col - 1),
                Position(line - 1, col)
            ),
            msg,
            source=type(json_server).__name__
        )
        diagnostics.append(d)
    return diagnostics


@json_server.feature(COMPLETION, trigger_characters=[','])
def completions(params: CompletionParams = None):
    """Returns completion items."""
    return CompletionList(False, [
        CompletionItem('"'),
        CompletionItem('['),
        CompletionItem(']'),
        CompletionItem('{'),
        CompletionItem('}')
    ])

@json_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    # revalidate on every change
    _validate(ls, params)


@json_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: LarkJsonLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message('Text Document Did Close')


@json_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    _validate(ls, params)
