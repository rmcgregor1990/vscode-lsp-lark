# vscode lark ls example

An example vscode language server extension which uses lark to provide diagnostics on json documents with the extension `.lark-json`.

[pygls](https://github.com/openlawlibrary/pygls) is used provide the language server protocol interface and lark to provide diagnostics.

This example is heavily based on the pygls [example](https://github.com/openlawlibrary/pygls/tree/master/examples/json-extension) with lark slotted in.

## Install Server Dependencies
To run the server you need a python venv with `pygls` (from pypi) and `lark-parser` (from git master) installed.
You then need the vscode python path set to this venv:
- Create `.vscode/settings.json` file and set `python.pythonPath` to point to your python environment `python` executable 

*the vscode python extension also has some automatic venv discovery which may do this for you if you create a virtual venv in the root dir*

## Install Client Dependencies
The client requires node and npm.

-  run `npm install` in the root directory.
-  Compile the client extension via `npm run compile`


## Run the example from vscode

- Open this directory in VS Code
- Open debug view (shortcut = `ctrl + shift + D`)
- Select `Server + Client` and press `F5` or click on the green arrow (Start Debugging).
- This will only a vscode extension host with client and server both run under the debugger.
- Within the extension host vscode instance create a file with the `.lark-json` extension or select the Language Mode (bottom right) to `lark-json`.
- If you type some invalid json, lark will provide syntax errors
