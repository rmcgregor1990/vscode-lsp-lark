"use strict";

import * as net from "net";
import * as path from "path";
import { ExtensionContext, workspace } from "vscode";
import { LanguageClient, LanguageClientOptions, ServerOptions } from "vscode-languageclient";

let client: LanguageClient;

function getClientOptions(): LanguageClientOptions {
  return {
    // Register the server for plain text documents
    documentSelector: [
      { scheme: "file", language: "lark-json"},
      { scheme: "untitled", language: "lark-json"},
    ],
    outputChannelName: "[pygls] lark-json-ls"
  };
}

function isStartedInDebugMode(): boolean {
  return process.env.VSCODE_DEBUG_MODE === "true";
}

function startLangServerTCP(addr: number): LanguageClient {
  const serverOptions: ServerOptions = () => {
    return new Promise((resolve, reject) => {
      const clientSocket = new net.Socket();
      clientSocket.connect(addr, "127.0.0.1", () => {
        resolve({
          reader: clientSocket,
          writer: clientSocket,
        });
      });
    });
  };

  return new LanguageClient(`tcp lang server (port ${addr})`, serverOptions, getClientOptions());
}

function startLangServer(
  command: string, args: string[], cwd: string,
): LanguageClient {
  const serverOptions: ServerOptions = {
    args,
    command,
    options: { cwd },
  };

  return new LanguageClient(command, serverOptions, getClientOptions());
}

export function activate(context: ExtensionContext) {
  if (isStartedInDebugMode()) {
    // Development - Run the server manually
    client = startLangServerTCP(2087);
  } else {
    // Production - Client is going to run the server (for use within `.vsix` package)
    // if the python in bundled within the extension otherwise you might discover a specific python packet within the current env
    const cwd = path.join(__dirname, "..", "..");

    // get the vscode python.pythonPath config variable
    const pythonPath = workspace.getConfiguration("python").get<string>("pythonPath");
    if (!pythonPath) {
      throw new Error("`python.pythonPath` is not set");
    }

    client = startLangServer(pythonPath, ["-m", "server"], cwd);
  }

  context.subscriptions.push(client.start());
}

export function deactivate(): Thenable<void> {
  return client ? client.stop() : Promise.resolve();
}
