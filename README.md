![image](https://user-images.githubusercontent.com/2152766/56589571-6e0c7a00-65dd-11e9-8635-cf6c236718fd.png)

An example and exploration of how and if [Rez](https://github.com/nerdvegas/rez) could be used to version both software and project configurations, on Windows, Linux and MacOS.

- [Conversation on Google Groups](https://groups.google.com/forum/#!topic/rez-config/ni5CK2pxj38)

![Untitled Project](https://user-images.githubusercontent.com/2152766/56455523-270d5300-6357-11e9-9f00-0e870af29372.gif)

**Table of contents**

- [History](#previous-versions-of-this-repository)
- [Prelude](#prelude)
  - [What is Rez](#what-is-rez)
  - [Warnings](#warnings)
  - [Motivation](#motivation)
- [Features](#Features)
- [How it works](#how-it-works)
- [Requirement Network](#requirement-network)
- [Conditional Requirements](#conditional-requirements)
- [This Repository](#this-repository)
- [Usage](#usage)
    - [Install](#install)
    - [Workflow](#workflow)
    - [Development](#development)
    - [Terminal](#terminal)
- [Architecture](#architecture)
- [Missing](#missing)
- [FAQ](#faq)
    - [Q: "Why Reference Packages?"](#q-why-reference-packages)
    - [Q: "Why store project scripts with Package?"](#q-why-store-project-scripts-with-package)

<br>

##### Previous versions of this repository

This repo is complex; I've saved prior working versions in simpler conditions that you can checkout, whereby the README details what is available and what is missing.

```bash
$ git clone https://github.com/mottosso/rez-for-projects.git
$ cd rez-for-projects
$ git checkout 1.0
```

| Version | Description
|:-------:|:-----------
| [**`1.0`**](../../releases/tag/1.0) | Initial working version
| [**`1.1`**](../../releases/tag/1.1) | Conditional requirements with `@late` and `private_build_requires`
| [**`1.2`**](../../releases/tag/1.2) | Got rid of `rezbuild.py` dependency, in favor of `build_command`
| [**`1.3`**](../../releases/tag/1.3) | Added Workflow section and refactored directory layout

<br>
<br>
<br>
<br>
<br>

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56588385-2258d100-65db-11e9-89f9-f1f0aafccf6a.png></div>

<h3 align="center">Usage</h3>

**Prerequisites**

1. Windows, Linux or OSX
1. [bleeding-rez](https://github.com/mottosso/bleeding-rez)
1. `python` available on your PATH
1. `rez` available on PATH

**Install**

If you haven't got Rez installed, start here:

```bash
pip install bleeding-rez -U
```

<br>

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

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56455060-cf201d80-6351-11e9-93af-d6ae0721bb4e.gif></div>

<br>
<br>
<br>
<br>

## Prelude

<img align="right" height=250 src=https://user-images.githubusercontent.com/2152766/56585426-b32cae00-65d5-11e9-995e-b3f9115004da.png>

##### What is Rez

Broadly speaking, Rez is used to optimise parallelism amongst humans in a collaborative endeavors, especially those in visual effects. Every human added to a project comes with some amount of overhead to tooling and communication. At a certain scale - beyond 10-50 humans - that overhead needs management and that's where Rez fits in; it can help increase parallelism between one human having a software issue and another addressing it, with minimal impact on the remaining 48 humans.

<details>
  <summary>User Stories</summary>

These are some specific scenarios that Rez, in particular through this project, addresses.

|   | As a.. | I want.. | So that..
|:--|:-------|:---------|:-------
| 1 | developer | to publish updates to my software | artists can use it
| 2 | developer | to preserve prior updates | I can rollback if necessary
| 3 | developer | to indicate which versions are stable | artists can choose between latest or safest
| 4 | developer | to indicate which package depends on which other package | I can ensure compatibility
| 5 | developer | to resolve an environment whereby all version requirements are fulfilled | I can develop tools that depend on it
| 6 | developer | to be able to work in parallel with another developer on the same project | neither of us have to wait for the other
| 7 | artist | pipeline to get out of my way | I can focus on my work
| 8 | artist | software to run fast | I can focus on my work
| 9 | supervisor | multiple developers able to work on a software project in parallel | I can get the most bang for the buck
| 10 | supervisor | to track who published what and when | I know who to ask about updates or issues
| 11 | developer | Git tags associated with software version numbers | there is a single source of truth as to what is released and what is not
| 12 | supervisor | to have my show locked off from pipeline updates | nothing new gets broken during a crunch
| 13 | developer | to add a comment to a published package | I can communicate to others what the changes were and why
| 14 | developer | to release packages on a per-show basis | other shows are unaffected by potentially breaking changes
| 15 | developer | to group related packages on disk | they are more easily browsed through via e.g. Windows Explorer or Nautilus
| 16 | td | to share scripts with my colleagues without having to know Git or Rez | I can avoid a Phd in pipeline to share my work

</details>

<br>

> This repo assumes an experienced-level of familiarity with [Rez](https://github.com/nerdvegas/rez).

Rez is primarily a framework for resolving dependencies required for building software; which help explain why a build step is required per default, why a `CMakeLists.txt` is presumed to reside alongside a package definition, and why requirements default to being [resolved at build-time](#build-versus-runtime-requirements) rather than run-time; `x` can't be built without `y` having been built first.

This repo is different. It (mis)uses Rez primarily for resolving *environments*, in particular those involved in launching software for an appropriate context given some VFX project or asset within that project.

It's not all upside down however; a lot of packages do contain Python modules or compiled Maya plug-ins in which case build system muscles are flexed in full.

<details>
  <summary>Warnings</summary>

The community explicitly points out that Rez is not well suited for this purpose.

- ["Rez is not a production environment management system"](http://mottosso.github.io/bleeding-rez/#what-is-rez-not) (Old, Rez-1 documentation)
- ["Rez was not designed to manage production environments"](https://groups.google.com/d/msg/rez-config/ni5CK2pxj38/WREAh0XRBgAJ) (Allan, Google Groups conversation)
- ["Rez makes a clear distinction between configuration management and package management"](https://groups.google.com/d/msg/rez-config/gnwd7EuOzmM/rh6KeSHV5pwJ) (Allan, Google Groups conversation)

But if someone told you "ice cream wasn't designed for chocolate lava cake", would you listen? :)

</details>

<details>
  <summary>Motivation</summary>

So why do it? Because:

1. Complex use of a single system > simple use of multiple systems
1. Complex use of a simple system > simple use of a complex system
1. Complex use of an established system > simple use of an ad-hoc system
1. Complex use of a system with a community > simple use of a solo-developed system

So with all that out of the way, let's have a look at what's possible!

</details>

<br>
<br>
<br>
<br>

<div align="center"><img height=250 src=https://user-images.githubusercontent.com/2152766/56585877-904ec980-65d6-11e9-84cd-3b689947889c.png></div>

<h3 align="center">Features</h3>

<details>
    <summary align="center">Studio-wide environment</summary>
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
    <summary align="center">Per-project environment</summary>
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
    <summary align="center">Free-form Overrides</summary>
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
    <summary align="center">Third-party services</summary>
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
    <summary align="center">Per-package combination environment</summary>
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
    <summary align="center">External and internal packages</summary>
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
    <summary align="center">Self-contained packages</summary>
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
    <summary align="center">Reference packages</summary>
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
    <summary align="center">Cross-platform application packages</summary>
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
    <summary align="center">Multi-versioned application packages</summary>
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
<br>
<br>
<br>

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56584470-b161eb00-65d3-11e9-975e-17c266d2f8c4.png></div>

<h3 align="center">Workflow</h3>

The following documents how developer and artists interact with Rez and each other. Every release is accompanied by a mandatory develop stage. That is, no developer works directly towards the files accessible to Rez and the wider audience.

<table>
  <tr>
    <th width="50%">Develop</th>
    <th>Release</th>
  </tr>
  <tr></tr>
  <tr>
<td>

Every Rez package ends up in the `release_package_path/` directory, which is an example of where you host shared packaged within a single local area network.

</td>
<td>

- Every Rez package is developed in 1 of 3 ways:
  1. GitLab Tagging
  2. `rez build --install --prefix`
  3. `rez pip --install --release`

</td>
</tr>
</table>

<details>
  <summary><b>1. Releasing via GitLab</b></summary>

<table>
<tr><td>

In most cases, you'll be editing an internal project. In this example, we'll pretend `rez-internal-example` is an internal project at your company.

</td></tr>
<tr><td>

**1.1 Prerequisites**

1. Your studio uses self-hosted GitLab for version control and continuous integration
1. Developer has access to GitLab web UI
1. GitLab has write-access to your `REZ_RELEASE_PACKAGES_PATH`

</td></tr>
<tr><td>

**1.2 Develop**

Getting started on fixing a bug or implementing a feature involves an edit-and-install cycle.

1. Clone `https://gitlab.com/mottosso/rez-internal-example.git`
1. Edit `python/internal_example.py`
1. Install `rez build --install`
1. Repeat 2-3 until happy

Whenever `--install` is called, the updated package can be found in the `local_packages_path` and is accessible to Rez during resolve.

</td></tr>
<tr><td>

**1.3 Release**

Once happy, you're ready to release.

> Because this is read-only example, you can't actually run these steps yourself unless you (1) self-host GitLab and (2) fork this repository. But hopefully they can prove useful to get some sense of.

1. Update `version` in `package.py` from `1.1.0` to `1.2.0`
1. Add, commit and push changes
1. Log in to GitLab and create a tag `1.2.0`
1. Continuous Integration kicks in, triggering a release

A [`.gitlab-ci.yml`](https://gitlab.com/mottosso/rez-internal-example/blob/master/.gitlab-ci.yml) example is provided in the source repo, though keep in mind it won't work as-is because `gitlab.com` doesn't have write-access to your local release path, but should at least hint towards how to do achieve the effect.

</table>
</details>

<details>
  <summary><b>2. Releasing without GitLab</b></summary>

<table>
<tr><td>

The `rez-bundles` repository contains a number of packages that to Git is versioned together, but to Rez is released separately. This next section demonstrates how to release a package without using tags.

</td></tr>
<tr><td>

**2.1 Develop**

Developing works remains unchanged from the previous tutorial, except:

1. Clone `https://github.com/mottosso/rez-bundles.git`
2. Edit one of the packages, such as `alita`

The package is available in your `REZ_LOCAL_PACKAGES_PATH`.

</td></tr>
<tr><td>

**2.2 Release**

Again, similar to the previous tutorial.

1. Update `version` in `package.py` of the package you've edited
2. Add, commit and push
3. Call `rez build --install --prefix %REZ_RELEASE_PACKAGES_PATH%`

> Replace `%` with `$` on Linux and MacOS

The package is now available in your `REZ_RELEASE_PACKAGES_PATH`

</td></tr>
</table>
</details>

<details>
  <summary><b>3. Releasing <code>pip</code> packages</b></summary>

<table>
<tr><td>

**3.1 Develop**

Install any package from `pip` using the `rez pip --install` command.

```bash
$ rez pip --install Qt.py
```

The package is available in your `REZ_LOCAL_PACKAGES_PATH`.

**3.2 Release**

Just append `--release`.

```bash
$ rez pip --install --release Qt.py
```

The package is now available in your `REZ_RELEASE_PACKAGES_PATH`

</td></tr>
</table>
</details>

<br>
<br>
<br>
<br>

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56585131-1ec24b80-65d5-11e9-8f6e-05ce7449925f.png></div>

<h3 align="center">How it Works</h3>

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
<br>
<br>
<br>
<br>

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56587717-e6713c00-65d9-11e9-967a-b2e741addab3.png></div>

<h3 align="center">Requirement Network</h3>

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
<br>
<br>
<br>
<br>

<div align="center"><img src=https://user-images.githubusercontent.com/2152766/56588014-76af8100-65da-11e9-97df-55c7ff1ee460.png></div>

<h3 align="center">This Repository</h3>

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

### Terminal

Rez works on Windows and Linux (and probably OSX), but on Windows the integration with `cmd.exe` and `powershell` has one critical flaw: no history. Which means that hitting that up-arrow doesn't get you a previous command, instead it does nothing. It also lacks the color Linux users enjoy.

Until that has been addressed, here are some options that solve this problem.

- [ConEmu](https://conemu.github.io/)
- [cmder](https://cmder.net/)
- [Alacritty](https://github.com/jwilm/alacritty)

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
