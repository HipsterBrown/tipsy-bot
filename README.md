# Tipsy bot

Powered by [Viam](https://viam.com). Based on the [tutorial project](https://docs.viam.com/tutorials/projects/tipsy/).

## Getting started

This project assumes some knowledge of git, unix command line basics, [Homebrew](https://brew.sh), and [Python](https://www.python.org)

1. Clone this repo. I prefer the [`gh` CLI](https://cli.github.com): `gh repo clone hipsterbrown/tipsy && cd tipsy`

1. Install [`viam-server`](https://docs.viam.com/installation/#install-viam-server) manually, or run `brew bundle` in this directory

1. Install Python 3. I prefer [`rtx`](https://github.com/jdxcode/rtx#quickstart) as my tool version manager: `rtx install`

1. Install [viam-sdk](https://python.viam.dev) by running `python -m pip install -r requirements.txt`

1. Follow the SDK instructions for [creating a client application with Viam](https://python.viam.dev/#configure-a-client-application-at-app-viam-com), noting that viam-server is already installed

1. Copy the Viam app config from the app setup page: ![viam app setup](./docs/viam-config.png)

1. Rename `viam-example.json` to `viam.json` and paste app config in that file

1. Run the viam-server: `viam-server -config ./viam.json`

1. In a new terminal session, run `tipsy.py` program: `python tipsy.py`
