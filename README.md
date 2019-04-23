### Rez for Projects

An example and exploration of how and if [Rez](https://github.com/nerdvegas/rez) could be used to version both software and project configurations.

- [Conversation on Google Groups](https://groups.google.com/forum/#!topic/rez-config/ni5CK2pxj38)

![Untitled Project](https://user-images.githubusercontent.com/2152766/56455523-270d5300-6357-11e9-9f00-0e870af29372.gif)

**Table of contents**

- [Prelude](#prelude)
  - [What is Rez](#what-is-rez)
  - [Warnings](#warnings)
  - [Motivation](#motivation)
- [Features](#Features)
- [How it works](#how-it-works)
    - [Build versus Runtime Requirements](#build-versus-runtime-requirements)
- [Requirement Network](#requirement-network)
- [Conditional Requirements](#conditional-requirements)
- [This Repository](#this-repository)
- [Usage](#usage)
- [Building](#building)
- [Architecture](#architecture)
- [Missing](#missing)
- [FAQ](#faq)
    - [Q: "Why Reference Packages?"](#q-why-reference-packages)
    - [Q: "Why store project scripts with Package?"](#q-why-store-project-scripts-with-package)

<br>

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

## Prelude

##### What is Rez

Broadly speaking, Rez is used to optimise parallelism amongst humans in a collaborative endeavors, especially those in visual effects. Every human added to a project comes with some amount of overhead to tooling and communication. At a certain scale - beyond 10-50 humans - that overhead needs management and that's where Rez comes in.

<details>
  <summary>User Stories</summary>

These are some specific scenarios that Rez, in particular through this project, addresses.

1. As a **DEVELOPER**, I would like to publish updates to my software, so that artists can use it
1. As a **DEVELOPER**, I would like to preserve prior updates, so that I can rollback if necessary
1. As a **DEVELOPER**, I would like to indicate which versions are stable, so that artists can choose between latest or safest
1. As a **DEVELOPER**, I would like to indicate which package depends on which other package, so that I can ensure compatibility
1. As a **DEVELOPER**, I would like to resolve an environment whereby all version requirements are fulfilled, so that I can develop tools that depend on it
1. As a **DEVELOPER**, I would like to be able to work in parallel with another developer on the same project, so that neither of us have to wait for the other
1. As an ARTIST, I want pipeline to get out of my way, so that I can focus on my work
1. As an ARTIST, I want software to run fast, so that I can focus on my work
1. As a **SUPERVISOR**, I want multiple developers able to work on a software project in parallel, so I can get the most bang for the buck
1. As a **SUPERVISOR**, I would like to track who published what and when, so that I know who to ask about updates or issues
1. As a **DEVELOPER**, I would like Git tags associated with software version numbers, so as to provide a single source of truth as to what is released and what is not
1. As a **SUPERVISOR**, I would like to have my show locked off from pipeline updates, so that nothing new gets broken during a crunch
1. As a **DEVELOPER**, I would like to add a comment to a published package, so as to communicate to others what the changes were and why
1. As a **DEVELOPER**, I would like to release packages on a per-show basis, so that other shows are unaffected by potentially breaking changes
1. As a **DEVELOPER**, I would like to group related packages on disk, so that they are more easily browsed through via e.g. Windows Explorer or Nautilus
1. As a **TD**, I would like to share scripts with my colleagues without having to know Git or Rez, so that I can avoid a Phd in pipeline to share my work

</details>

<br>

> This repo assumes an experienced-level of familiarity with [Rez](https://github.com/nerdvegas/rez).

Rez is primarily a framework for resolving dependencies required for building software; which help explain why a build step is required per default, why a `CMakeLists.txt` is presumed to reside alongside a package definition, and why requirements default to being [resolved at build-time](#build-versus-runtime-requirements) rather than run-time; `x` can't be built without `y` having been built first.

This repo is different. It (mis)uses Rez primarily for resolving *environments*, in particular those involved in launching software for an appropriate context given some VFX project or asset within that project.

It's not all upside down however; a lot of packages do contain Python modules or compiled Maya plug-ins in which case build system muscles are flexed in full.

##### Warnings

The community explicitly points out that Rez is not well suited for this purpose.

- ["Rez is not a production environment management system"](http://mottosso.github.io/bleeding-rez/#what-is-rez-not) (Old, Rez-1 documentation)
- ["Rez was not designed to manage production environments"](https://groups.google.com/d/msg/rez-config/ni5CK2pxj38/WREAh0XRBgAJ) (Allan, Google Groups conversation)
- ["Rez makes a clear distinction between configuration management and package management"](https://groups.google.com/d/msg/rez-config/gnwd7EuOzmM/rh6KeSHV5pwJ) (Allan, Google Groups conversation)

But if someone told you "ice cream wasn't designed for chocolate lava cake", would you listen? :)

##### Motivation

So why do it? Because:

1. Complex use of a single system > simple use of multiple systems
1. Complex use of a simple system > simple use of a complex system
1. Complex use of an established system > simple use of an ad-hoc system
1. Complex use of a system with a community > simple use of a solo-developed system

So with all that out of the way, let's have a look at what's possible!

<br>

### Features

<details>
    <summary>Studio-wide environment</summary>
    <table>
        <tr>
            <th align="left"><code>base</code></th>
        </tr>
        <tr>
            <td>

A top-level package represents the studio itself; containing environment and requirements passed down to every software and project package.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Per-project environment</summary>
    <table>
        <tr>
            <th align="left"><code>alita</code></th>
        </tr>
        <tr>
            <td>

Every show is represented by a Project Package that encapsulates each unique requirement and environment variable, augmenting the studio-wide package `base`.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Free-form Overrides</summary>
    <table>
        <tr>
            <th align="left"><code>alita</code></th>
        </tr>
        <tr>
            <td>

Every project provides "free-form overrides" which are read/write directories of scripts, plug-ins and shelves etc. for DCCs like Maya. Any artist may add or share scripts this way and is a way for those not involved with Rez or Git to contribute and share code with co-workers.

**alita/package.py**

```python
def commands():
    if "maya" in request:
        # Refers to location outside of package, that may or may not exist
        env["PYTHONPATH"].prepend("{env.PROJECTPATH}/maya/scripts")
        env["PYTHONPATH"].prepend("{env.PROJECTPATH}/maya/shelves")
```

This idea is mostly relevant to studios in the 1-100 size, where there aren't enough developers to justify a release-cycle for any minor change, and less suitable in the 100-1,000 range where reliability trumps speed.

**A word of caution** A consequence of this feature is that you can never be sure that what works today, given a fixed set of project requirements and versions, will work tomorrow; as there is only ever 1 version of these globally accessible free-form overrides.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Third-party services</summary>
    <table>
        <tr>
            <th align="left"><code>ftrack</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

This project refers to [ftrack](http://ftrack.com) for production tracking, but applies to any external or internal service; the package merely includes appropriate environment variables that point to the remote URI. For security, the API key necessary for actually logging in and reading/writing information is provided separately at the OS level. This also helps when the key needs to change or refresh for whatever reason; there is only ever 1 valid key at any point in time, so no versioning is required.<br><br>The `package.commands()` validates that this key exists, as the package is of no use without it.

```bash
$ set FTRACK_API_KEY=xyz123
$ re ...
```

</td>
        </tr>
        <tr></tr>
        <tr>
            <td><code><b>gitlab</b></code></td>
        </tr>
        <tr></tr>
        <tr>
            <td>

Like `ftrack`, a package for a self-hosted GitLab instance is also included, providing access to its Python and Ruby API via command-line and DCC, along with also requiring an API key to be of any use.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Per-package combination environment</summary>
    <table>
        <tr>
            <th align="left"><code>alita</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

Some requirements only make sense in conjunction with two or more packages. For example, requesting `maya` gets you one environment, `alita` gets you another one but both `maya` and `alita` doesn't just get you their combined requirements and environment, but also `pyblish` and `mgear`; packages only relevant to `maya`, and only within the context of `alita`

- See [Conditional Requirements](#conditional-requirements) for more

</td>
        </tr>
    </table>
</details>

<details>
    <summary>External and internal packages</summary>
    <table>
        <tr>
            <th align="left"><code>pip</code>, <code>core_pipeline</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

Packages developed internally are managed on GitLab, cloned onto the local disk of a developer, and released on creating a new tag via the GitLab web-based UI.

External packages from `pip` are released via `rez pip --install`.

```bash
$ rez pip --install Qt.py
```

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Self-contained packages</summary>
    <table>
        <tr>
            <th align="left"><code>core_pipeline</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

Some packages in this project reference an external payload, like `maya`. Others are self-contained and can be copy/pasted between Rez repositories, even between studios.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Reference packages</summary>
    <table>
        <tr>
            <th align="left"><code>maya</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

To save on disk space and avoid accessing static or large files over a potentially slow network connection, some packages carry their payload separate from their metadata.

See [Reference Packages](#q-why-reference-packages) for more.

</td>
        </tr>
    </table>
</details>


<details>
    <summary>Cross-platform application packages</summary>
    <table>
        <tr>
            <th align="left"><code>maya</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

The `maya` package looks the same on both Windows and Linux.

</td>
        </tr>
    </table>
</details>

<details>
    <summary>Multi-versioned application packages</summary>
    <table>
        <tr>
            <th align="left"><code>maya</code></th>
        </tr>
        <tr></tr>
        <tr>
            <td>

Because major versions of DCCs update independently, packages like `maya` differs from other packages; it consists of an individual package for each major version of Maya.

```
software/
  maya/
    2017/
    2018/
    2019/
      package.py
```

Which means `maya-2017` may be updated to `maya-2017.5` despite not being latest.

> **Developer Note** This isn't ideal; preferably there would only be 1 `maya` package, but I wasn't able to figure out how to go about it.

</td>
        </tr>
    </table>
</details>

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

Because `maya` was included, `alita` imbues it with extra requirements.

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

## This Repository

This repository combines several aspects normally separate in an actual Rez-ified production environment. For example, the `dev/` directory is typically local to a developer's machine. The `local_packages_path/` is typically `~/packages`. And so forth. See the below table or README's contained in each sub-directory for details.

| Directory       | Description
|:----------------|:----------
| **`.rez/`**           | Private files to this repo
| **`dev/`**            | Representation of a local development directory
| **`local_packages_path/`** | Representation of the default `~/packages` directory
| **`remote_packages_path/`**  | Representation of a shared location for released packages

**`dev/`**

Local development directory.

| Directory            | Description
|:---------------------|:----------------
| **`core-pipeline/`** | Representation of an internal project, hosted on e.g. GitLab
| **`maya-base/`**     |
| **`mgear/`**         | Representation of an external project, hosted on [GitHub](https://github.com/mgear-dev)
| **`pip/`**           | External project, temporarily hosted locally for release
| **`rez-bundles/`**   | Internal project, containing all projects and applications

**`dev/rez-bundles/`**

Internal mono-repo of projects and applications.

| Directory             | Description
|:----------------------|:----------------
| **`alita/`**          | DCC and software requirements, and environment for the Alita project
| **`lotr/`**           | Likewise, but for Lord of the Rings
| **`base/`**           | Common studio environment
| **`maya_base/`**      | Common studio environment for Maya
| **`maya/`**           | System reference to Maya-2017-2019
| **`nuke/`**           | System reference to Nuke-11v3.2
| **`python/`**         | System reference to Python-2.7 and -3.6

<br>

## Usage

![rez_running](https://user-images.githubusercontent.com/2152766/56455060-cf201d80-6351-11e9-93af-d6ae0721bb4e.gif)

**Prerequisites**

1. Windows, Linux or OSX
1. [bleeding-rez](https://github.com/mottosso/bleeding-rez)
1. `python` available on your PATH
1. `rez` available on PATH

**Install**

On either Windows or Unix, run the below.

> Don't forget about **`--recursive`**, due to the `rez-bundles` submodule.

```bash
$ set PATH=<-- path/to/rez/Scripts/rez -->;%PATH%
$ git clone --recursive https://github.com/mottosso/rez-for-projects.git
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

#### Build versus Runtime Requirements

Rez resolves requirements during build per default, because Rez is primarily designed to build software that depend on other software having been built first. It can also be made to resolve requirements when calling `rez env`, which I'll refer to as run-time requirements in this repo.

All packages in this project are *run-time* requirements, unless:

1. It is used by another package during build

The only package where this exception currently applies is `rezutils`

<br>

## Missing

Here are some of the things I'd like to happen but haven't figured out how to do yet.

- **Cascading Overrides** If `/projects/alita/rez` is on the `REZ_PACKAGE_PATH`, then the contained `maya/package.py` should *add to* the studio-wide Maya configuration for this project. Similar to how CSS works.
    - Could potentially be implemented by having every project require a stub `project_override` package, that per default does nothing, but can be implemented elsewhere and added to the `REZ_PACKAGES_PATH`.
    - Another, less appealing way, is by "subclassing" a project e.g. `alita_override` of whichthe original `alita` package is a requirement along with additional requirements and environment variables. The downside of this is (a) you need one package for each permutation and (b) the user would need to stop typing `alita maya` and start typing `alita_override maya` which is error prone and tedious on both developer and user ends.

<br>

## FAQ

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

<br>

#### Q: "Why store project scripts with Package?"

I.e. why not store them with the project, and reference that?

By keeping a Rez package self-contained:

1. You enable versioning of project-specific payload
1. You avoid package and payload from getting out of sync
2. You enable re-use of a package

Consider the following example.

```
packages/
  alita/
    package.py

/
  projects/
    alita/
      scripts/
        maya/
```

```python
# package.py
def commands():
    env["PYTHONPATH"] = "${PROJECT_PATH}/scripts/maya"
```

This package cannot exist without an externally set `PROJECT_PATH` environment variable. Without it, the environment cannot be entered, and yet the package can still exist on your `REZ_PACKAGES_PATH`, sending mixed messages about its availability.

If instead scripts for Maya were contained within the package itself..

```
packages/
  alita/
    scripts/
      maya/
```

```python
# package.py
def commands():
    env["PYTHONPATH"] = "{root}/scripts/maya"
```

Then a package being available means payload being available too, and if you wanted to reuse this package in some other project, you could.
