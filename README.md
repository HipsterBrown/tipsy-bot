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

1. Rename `.env.example` to `.env` and fill out the environment variables with the expected info, only the `ROBOT_SECRET` and `ROBOT_ADDRESS` are required if following the [tutorial project](https://docs.viam.com/tutorials/projects/tipsy/)

1. In a new terminal session, run `tipsy.py` program: `python tipsy.py`

## Expected functionality

- [X] Look for people, and move towards them using the camera and a machine learning model
- [X] Avoid bumping into obstacles using ultrasonic sensors.  This includes both not starting movement that will create a collision, but also stopping movement when something unexpectedly enters Tipsy’s path
- [ ] Pauses near people to allow them to choose to grab drinks
- [ ] Not get “stuck” next to the same person, mingle! (but don’t over-engineer it, randomness is OK, no need to track individual people or where Tipsy has been)
- [ ] Attempt to not get stuck and/or tipping backwards when impacting an undetected object
- [X] Make the number of ultrasonic sensors configurable, e.g. allow one to have a config variable that says it should use X number of ultrasonic sensors

