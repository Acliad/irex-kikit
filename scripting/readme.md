# Overview
This folder contains scripting/automation kikit_tools. 

## Python Environment
The tools in this folder are designed to use a `python` environment. The required packages are listed in `requirements.txt`. To make the environment simple and reliable, it is required that you use a virtual environment. To set this up:
- Install Python 3.13
  - It's recommended to use either `pyenv` or install via homebrew if on macOS. Either way, you just need python available
- Create a virtual environment
    ```bash
    python -m venv ./python-kikit
    ```
- Install the required packages
    ```bash
    ./python-kikit/bin/pip install -r requirements.txt
    ```

The current KiCad `execute command` environment is extremely fragile and fails silently with many of the traditional path and environment variable tricks. The current workaround is to use a shell script that activates the virtual environment and then runs the desired tool. Thus, when using scripts from within KiCad, you should use the following command, which sets up the environment and runs python
```bash
${IREX_KIKIT_ROOT_DIR}/scripting/execute-command-python.sh -m kikit_tools.<module> <arguments to module>
```
When running from a regular user environment, you can just `source` the venv activate script and run python directly.
```bash
source ./python-kikit/bin/activate
python -m kikit_tools.<module> <arguments to module>
```
Note when doing this that some expected KiCad environment variables will not be set, so some tools may not work as expected. You can add them to your shell environment adhoc if just testing.

## Releaser
The Releaser folder contains tooling for automated releasing of a finished design. This includes on-click generation of PDF documents, gerbers, BOM, placement, and mechanical exports from the KiCad jobset. It also maintains a script for locally installing a python bundle that contains all necessary dependencies.

### Setup
The Releaser requires a couple environment variables to be set. In KiCad, go to Preferences -> Configure Paths and add the following variables:
- `IREX_KIKIT_VENV_DIR`: **TODO**
- `IREX_KIKIT_ROOT_DIR`: **TODO**

**TODO: Expand with images**
You may also need to enable KiCad API in settings
**TODO: Add images**