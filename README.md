### Rez for Projects

An example of how Rez could be used to version both software and project configurations.

![Untitled Project](https://user-images.githubusercontent.com/2152766/56455523-270d5300-6357-11e9-9f00-0e870af29372.gif)

##### Previous versions of this repository

This repo is complex; I've saved prior working versions in simpler conditions that you can checkout, whereby the README details what is available and what is missing.

| Version | Description
|:-------:|:-----------
| [**`1.0`**](../../releases/tag/1.0) | Initial working version
| [**`1.1`**](../../releases/tag/1.1) | Conditional requirements with `@late` and `private_build_requires`

```bash
$ git clone https://github.com/mottosso/rez-for-projects.git
$ cd rez-for-projects
$ git checkout 1.0
$ ./build_all
```

<br>

### Features

- Per-project environment
- Per-application environment
- Conditional requirements, e.g. `maya` and `alita` combined includes `mgear`
- External and internal packages, i.e. pip and core_pipeline
- Self-contained packages, i.e. `core_pipeline`
- Locally referenced application packages, i.e. Python and Maya
- Cross-platform application packages, i.e. Maya
- Multi-versioned application packages, i.e. Maya 2017-2019 and Python 2.7-3.6

<br>

### How it works

The project defines 3 types of Rez packages.

| Package Type    | Description           | Examples
|:----------------|:----------------------|:-------
| `software`      | Self-contained software distribution | `qt_py`, `pyblish_base`, `pip`
| `reference`     | A software package whose payload reside elsewhere | `maya`, `python`
| `bundle`        | Combines two or more packages | `alita`, `lotr`
| | | [Terminology Reference](http://mottosso.github.io/bleeding-rez/#bundles)

<br>

<table>
    <tr>
        <th>Software Package</th>
        <th>Reference Package</th>
        <th>Bundle Package</th>
    </tr>
    <tr></tr>
    <tr>
        <td>A <b>self-contained</b> Rez package, with payload and metadata residing within the package itself.</td>
        <td>A package in which metadata <b>references</b> an external payload, such as Maya or Python.</td>
        <td>A package that <b>combines</b> two or more packages, that may or may not carry a payload.</td>
    </tr>
    <tr>
        <td>

```bash
~/
  packages/
    core_pipeline/
      python/           # Payload
        core_pipeline/
          __init__.py
          lib.py
          util.py
      package.py        # Metadata
      rezbuild.py
```
</td>
        <td>

```bash
/opt
  maya2018/        # Payload
    bin/
      maya
~/
  packages/
    maya/
      2018/
        package.py # Metadata
```

</td>
    <td>

```bash
~/
  packages
    alita/
      python/     # Payload
      maya/
      package.py  # Metadata
      rezbuild.py  # Metadata
```

</td>
    </tr>
</table>

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

### Conditional Requirements

Some combinations of packages give rise to intelligent behavior.

```bash
$ re alita maya
```

```
                      ________________________
                     |                        |
$ command-line >     |      alita + maya      |
                     |________________________|
                       /   \           \      \
- - - - - - - - - - - / - - \ - - - - - \ - - -\- - - - - - - - - - - 
                    _/___   _\___    ____\____  \_______
                   |     | |     |  |         | |       |
                   | ... | | ... |  | pyblish | | mgear |   resolved
                   |_____| |_____|  |_________| |_______|
                                           
```

Because `alita` was included, `maya` is given extra requirements.

**Properties**

- Resolving an environment with only `maya` yields a "vanilla" environment whereby the *latest version* of Maya is present.
- Resolving an environment with only `alita` yields a "vanilla" environment whereby the *latest version* of this project and its environment is present.

**Additionally**

- Resolving an environment with both `maya` and `alita` yields an environment whereby:
    1. A *specific version* of `maya` is present, one compatible with `maya`, via the weak reference `~maya-2018`
    1. A specific set of requirements are included, relevant to both the project and application, such as `mGear` or `pyblish`, via the `@late` decorator of `requires()`

**Specific version of Maya to a given project**

```python
# alita/package.py
name = "alita"
version = "1.0"
requires = [
    "~maya-2018",
]
```

**Specific set of requirements to a given combination of project and application**

```python
# alita/package.py
name = "alita"
version = "1.0"

@late()
def requires():
    if in_context() and "maya" in request:
        return ["mgear-1"]

    if in_context() and "nuke" in request:
        return ["optflow-3.5"]

    return []
```

<br>

### This Repository

Below is the structure and layout of this repository.

| Directory       | Description
|:----------------|:----------
| **`.packages/`**      | Search and install path for packages
| **`bin/`**            | Convenience scripts for Windows, alias used on Linux
| **`configurations/`** | The project configurations
| **`python/`**         | Scripts available during package build
| **`software/`**       | Standard Rez software packages

**`configurations/`**

| Directory       | Description
|:----------------|:----------------
| **`alita/`**          | DCC and software requirements, and environment for the Alita project
| **`lotr/`**           | Likewise, but for Lord of the Rings

**`software/`**

| Directory       | Description
|:----------------|:----------------
| **`base/`**           | Common studio environment
| **`maya_base/`**      | Common studio environment for Maya
| **`maya/`**           | System reference to Maya-2017-2019
| **`nuke/`**           | System reference to Nuke-11v3.2
| **`python/`**         | System reference to Python-2.7 and -3.6
| **`core_pipeline/`**  | Internal project from local GitLab
| **`mgear/`**          | Internal project from local GitLab
| **`pyblish_base/`**   | External package from pip
| **`pip/`**            | Self-contained version of pip-19

<br>

### Usage

![rez_running](https://user-images.githubusercontent.com/2152766/56455060-cf201d80-6351-11e9-93af-d6ae0721bb4e.gif)

**Prerequisites**

1. Windows, Linux or OSX
1. `python` available on your PATH
1. [`rez`](https://github.com/nerdvegas/rez) available on PATH

**Install**

On either Windows or Unix, run the below.

```bash
$ git clone https://github.com/mottosso/rez-for-projects.git
$ cd rez-for-projects
$ ./build_all
```

![autobuild](https://user-images.githubusercontent.com/2152766/56460565-6d38d580-639c-11e9-8f7e-76290cde60ac.gif)

> The build script will make contained packages available for resolve

Now enter a shell.

```bash
$ ./shell
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

The shell script configures Rez to look for packages in this repository, exposes aliases `re` and `ri` for common Rez commands and provides you with a greeting message. It does not implement any custom behavior, everything is native to Rez.

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
- Combinations of two or more packages result in a specific list of requirements and environment variables via the `@late` decorator.

<br>

### Missing

Here are some of the things I'd like to happen but haven't figured out how to do yet.

- **Overrides** If `/projects/alita/rez` is on the `REZ_PACKAGE_PATH`, then the contained `maya/package.py` should override the studio-wide Maya configuration for this project.

<br>

### FAQ

#### Q: "Why Reference Packages?"

| Cons | Pros
|:----|:----
| **Out of Sync** A package can be installed, but the content it references can be missing; e.g. a user may not have Maya 2018 installed. | **Reach** Create packages out of software you wouldn't normally be able to, due to software, system or permission restrictions.
| **Lack of Granuluarity** A new version of a package doesn't affect the content, which complicates updates to the payload | **Space** Large, rigid packages like Maya build up large requirements for your file server and archiving solution.
| | **Performance** Running multi-gigabyte software from a network location isn't healthy for your fellow DevOps engineers.
| | **Iteration time** As the package contains solely requirements and environment variables, releasing a configuration package can be instantaneous.

**Reference Packages** are a way to utilise Rez for packages that are otherwise impractical or impossible to confine into a package. For example it may be too large or dependent on their native installation path, such as Maya being large or PyQt4 with absolute paths embedded in its linked library.

**How it works**

With Rez, each package consists of two parts.

1. Metadata
1. Payload

Some packages carry both definition and content, like `core_pipeline`. Such that whenever a new version of this package is made, its content is updated too.

```bash
.packages/
  core_pipeline/
    2.1.0/
      python/      # content
      package.py   # definition
```

Other packages reference something on the local system instead.

```bash
.packages/
  maya/
    2018.0.1/
      package.py ---.                           # definition
                    .
                    v
c:\program files\autodesk\maya2018\bin\maya.exe # content
```

These are referred to as Reference Packages throughout this project.

<br>

#### Q: "Why store project scripts with Package?"

I.e. why not store them with the project, and reference that?
