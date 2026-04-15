{ pkgs ? import <nixpkgs> { } }:

let
  pythonEnv = pkgs.python3.withPackages(p: [
    # Add Python packages needed for your project
    p.pygame

    # Add the Python Language Server package
    p.python-lsp-server
    # Optional: other language server related packages
    # p.jedi-language-server
    # p.python-lsp-flake8
    # p.python-lsp-mypy
  ]);

in
pkgs.mkShell {
  # The packages available in the shell, including the custom Python environment
  packages = [
    pythonEnv

  ];

  # Optional: shellHook runs commands when you enter the shell
  shellHook = ''
    echo "Welcome to the Nix-powered Python development shell!"
    # Ensure the LSP server is in the PATH and discoverable by your editor
    export PYTHONPATH=$PWD/src:$PYTHONPATH
  '';
}
