### Rez for Projects

An example of how Rez could be used to version both software and project configurations.

![rez_running](https://user-images.githubusercontent.com/2152766/56455060-cf201d80-6351-11e9-93af-d6ae0721bb4e.gif)

<br>

### Features

- Per-project environment
- Per-application environment
- External and internal packages, i.e. pip and core_pipeline
- Locally referenced application packages, i.e. Python and Maya
- Cross-platform application packages, i.e. Maya
- Multi-versioned application packages, i.e. Maya 2017-2019 and Python 2.7-3.6

<br>

### Requirement Network

Here's and example of how one request is resolved.

```bash
$ re alita maya
```

```
                             _______
                            |       |
                          . | ~2018 | .  
                         .  |_______|  .  weak reference
                         .             .
                      ___.___         _.____
                     |       |       |      |
$ command-line >     | alita |       | maya |
                     |_______|       |______|
                       /   \             \
- - - - - - - - - - - / - - \ - - - - - - \ - - - - - - - - - - - - - 
                  ___/__    _\______     __\________
                 |      |  |        |   |           |
                 | base |  | python |   | maya_base |    resolved
                 |______|  |________|   |___________|
                             __|__        ____\__________
                            |     |      |               |
                            | pip |      | core_pipeline |
                            |_____|      |_______________|
```

<br>

### This Repository

| Directory       | Description
|:----------------|:----------
| .packages/      | Search and install path for packages
| bin/            | Convenience scripts for Windows, alias used on Linux
| configurations/ | The project configurations
| python/         | Scripts available during package build
| software/       | Standard Rez software packages

**configurations/**

| Directory       | Description
|:----------------|:----------------
| alita/          | DCC and software requirements, and environment for the Alita project
| lotr/           | Likewise, but for Lord of the Rings

**software/**

| Directory       | Description
|:----------------|:----------------
| base/           | Common studio environment
| maya_base/      | Common studio environment for Maya
| maya/           | System reference to Maya-2017-2019
| nuke/           | System reference to Nuke-11v3.2
| python/         | System reference to Python-2.7 and -3.6
| core_pipeline/  | Internal project
| pyblish_base/   | External package from pip
| pip/            | Self-contained version of pip-19

<br>

### Usage

**Prerequisites**

1. A recent install of Rez
1. Windows, Linux or OSX
1. `rez` available on PATH

The project comes a shell script for each OS, double-click `.bat` for Windows and call or source `.sh` for Linux and OSX, and you will be greeted by the welcome sign.

```bash
 ==============================

  Welcome to rez-for-projects!

 This demo illustrates how projects
 and software can happily co-exist
           with Rez.

 ==============================

 Usage
 -----
 
 $ rez env         # Establish a Rez environment
 $ re              # ..using an alias
 $ re alita        # In a given project
 $ re alita maya   # With a given application

 $ rez build --install  # Edit and release new package
 $ ri                   # ..using an alias

$ 
```

> If `rez` wasn't found, a helpful message is printed.

<br>

### Building

Both software and configurations are plain Rez packages, and are installed with the `rez build --install` command, or `ri` for short.

![rez_building](https://user-images.githubusercontent.com/2152766/56455059-ce878700-6351-11e9-98b7-8ee9c44b9a52.gif)

<br>

### Architecture

- `base` is required by every project, and defines general variables accessible to all projects and DCCs, such as `PROJECTS_PATH` which is an absolute path to where projects are stored relative a given platform, e.g. `/mnt/projects` on Linux
- `maya`, `nuke` are standalone DCCs, installed on the local system and referenced by a packge
- `core_pipeline` represents a shared, common library used on all shows and all DCCs
- `maya_base` likewise, represents shared Maya requirements and environment variables
- `alita` and `lotr` are "configurations", in that they represent a project, rather than software
- `alita` is associated to version 2018 of Maya, via a "weak reference"

<br>

### Missing

Here are some of the things I'd like to happen but haven't figured out how to do yet.

- **Dynamic Requirements** I'd like to associate Pyblish with Maya, but only when run alongside `alita`, not `lotr`.
- **Overwriting Installs** Every install overwrites a prior install, that's bad. I'd like for an argument to be passed to `rez build` to explicitly allow overwriting.
- **Rezutils requirement** I'd like for standalone packages, like Pyblish, to not depend on an internal `rezutils` package to be built.
