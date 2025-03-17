# Belaster

## Presentation

Belaster is a suite of tools to manage file making. It is intuitive, versatile and user-friendly.

To use Belaster, the User writes scripts in Python3 and can take advantage of any Python3 library. No need to learn any new language nor any new file format to use Belaster.

The bash autocompleter is provided in the suite and helps with writing command lines: the full name of a target is a couple of tabs away.

The symbols presented by the module `belaster` are purely declarative from the point of view of file making. The User Belaster script declares Rules and their dependencies, Belaster takes care of the rest.


## Motivation behind creating Belaster

There are several build suites available, but for managing small projects, they all lack something that I find essential. They can lack ease of use, flexibility, extensibility, or they make strong assumptions on the dev environment, or they are built around outdated principles and paradigms.

One motivation for having created Belaster is to provide the essentials of file making without assumptions on the dev or build environments.

I created Belaster to fit my needs. Maybe it will fit yours as well.

> [!NOTE]
> I am in the process of transfering pieces of the code I use for my personnal projects into this repository.


## Quick How-To

### Write a Belaster script for creating and deleting a file

In a directory of your choice, create a file called `Belaster` with the following content:
```
from belaster import *
from pathlib import Path


filename = "blank"


def touch_file():
	Path(filename).touch()

Rule(
	targets={File(filename)},
	prerequisites=[],
	recipe=[touch_file]
)


def remove_file():
	Path(filename).unlink()

Rule(
	targets={Abstract("clean")},
	recipe=[remove_file]
)
```
Then, in that directory, run `belaster blank` and notice the file is created. Run `belaster clean` to delete it.


## Structure of the suite of tools Belaster

Belaster provides the following:
- the command-line `belaster`: given goals as input it does the file making.
- the Python module `belaster`: provides to the User all the symbols to use in their Belaster script.
- the `bash-completer`: called by bash when performing autocomplete, it calls `bash-completer-helper`.
- the `bash-completer-helper`: called by `bash-completer`, it gives the list of possibilities for autocompletion.

> [!NOTE]
> Inside the Python module `belaster` there is the submodule `engine`. It contains most of the internals of Belaster. Using the classes located there might modify the behaviour of Belaster.

## How to install and setup the dev environment

Belaster comes with the Makefile for installation and for managing the dev environment.


### How to install

Clone this repository then run at the root of the local copy of the repository:
```
make install
```
The User's password is needed to install the module and `bash-completer`.


### How to uninstall

The uninstallation should be done by hand.

> [!IMPORTANT]
> As the time of writing this README, using the Makefile to uninstall implies writing commands similar to `sudo rm -rf $(something)` (for the python module). That makes me extremely uncomfortable, thus I prefer that the uninstallation is done by hand.

Once Belaster is integrated into a python package manager, uninstallation will then be safely scripted.


### How to manage the dev environment

**Create the dev environment**
```
make dev-env
```
The dev environment relies on symlinks to bring the executables and the module into the Python environment. Except for the script `bash-completer`.
> [!TIP]
> Developing on `bash-completer` demands to overwrite the `bash-completer` possibly installed. I have not yet found a better solution. But I expect changes on `bash-completer` to rarely occur in the future since the heavy lifting is done by `bash-completer-helper`.


**Run the unit-tests and the end-to-end tests**
```
make
```
It creates the dev environment if needed.


**Clean the dev environment**
```
make clean-dev-env
```
It deletes the resources created by the target `dev-env`. It does not touch the installation neither the local repository.


## More detailed How-to

### Name and location of the User Belaster file

The name of a User Belaster file is `Belaster`. The casing is important.

The User Belaster file can be anywhere on the system. It can be inside the project, or outside. It can be at the root of the project or somewhere else.


### Import

Every User Belaster script should start with
```
from belaster import *
```
That line loads all the symbols needed in a regular usage of Belaster.

> [!TIP]
> The module `belaster` has a submodule called `engine`. It contains the classes for the internals of Belaster. Modifying that part of the code can be needed to add new features to Belaster or to alter its behaviour.


### Declare rules

The class Rule is central to Belaster. It gathers the targets, the prerequisites and the callbacks to create the targets.

> [!WARNING]
> It is up to the User to make sure that a Rule is consistent between the targets, the prerequisites and the callbacks: the targets are created by the recipe, the targets depend on the prerequisites.

A Rule needs the following types:
- the targets are a **set** of Atoms,
- the prerequisites are a **list** of Atoms,
- the recipe is a **list** of callbacks of type `dict -> None`.

The targets of a Rule are a set since their order is not needed.

The callbacks in the recipe of the rule take a dictionary and return `None`. The dictionary can be called `env` by convention. It is the dictionary of values calculated from the options given to `belaster` in the command-line. More details below, when presenting the tools for creating options.

> [!CAUTION]
> The distinction between **set** and **list** is essential to the proper execution of `belaster`.

For each target, there is at most one rule generating it.

> [!CAUTION]
> A target being generated by more than one rule will raise an error when `belaster` is run.

The prerequisites of a Rule are a list. They are processed sequentially thus their order is needed. They are processed from the first item of the list to the last.

> [!NOTE]
> For now, the rules are run sequentially. I plan on adding parallelism in the future, and a stronger mathematical base to Belaster. I think mathematical soundness will bring a strong frame to Belaster.

> [!CAUTION]
> If in the User Belaster script some rules form a loop, making their targets dependent in a cycle, then `belaster` detects that loop, raises an error and stops immediately the execution, even if the goals given are independent from the loop.


### Execution of the recipes

The recipe of a rule is executed if:
- one of the non-abstract targets does not exist,
- one of the non-abstract targets is older than one of the non-abstract prerequisites,
- one of the abstract prerequisites has been executed.


### Atoms

An atom is either a target or a prerequisite of a rule. Being an atom is modelled by being an instance of the class `Atom`. All the targets and all the prerequisites of all the rules should be instances of subclasses of the class `Atom`.

There are several classes for the atoms:
- `Abstract` models an abstract atom,
- `File` models a file atom,
- `Directory` models a directory atom,
- etc.

The complete list of atoms is found in the file `atom.py`.

In the command line arguments given to `belaster`, the goals are designated by their respective strings. These goals are targets, they are atoms. Thus the atoms should not collide by their string designations. An error would be raised by `belaster` if it occurs, and the bash autocompleter might not work.

> [!CAUTION]
> Two atoms cannot have the same string designations, regardless of their types. `belaster` will raise an error and the bash autocompleter might not work if it happens.

There are different string designations for an atom identified by its path. An atom identified by its path should be defined and used. When the atom is defined in the User Belaster script, the path is based on the location of the User Belaster script. When the atom is used in the command line, the path is based on the current working directory.

> [!IMPORTANT]
> If an atom has a path P, that path P has two representations:
> - P defined in the User Belaster script is written relative to the User Belaster script,
> - P used in the command line is written relative to the current working directory of the console.

Atoms may be defined without being used.


### Declare options

Belaster comes with a rich toolkit for creating options of diverse types so as to customize the building process even further. That toolkit aims at fulfilling most use-cases.

The options declared in the User Belaster script can be given to the command line `belaster` in the usual way. Belaster captures the values of the options given in the command line then, with these values, populates a dictionary called the **environment**. Then Belaster gives the environment to the recipes' callbacks when they are executed.

> [!NOTE]
> The same environment **object** is given to each callback when called. Thus if a callback modifies the environment object, these modifications are seen by the callbacks called afterwards. The environment allows the callbacks to communicate one with another.


The options that Belaster provides are defined in the file `option.py`.

> [!CAUTION]
> The classes for the options have a big hierarchy. Only the leaf classes can be used.


An example, in the User Belaster script:
```
OptionFlag(names={"-f"}, variable_name="Flag")
```
enables `belaster` to capture the option `-f` when given and to populate the entry `"Flag"` in the environment. When running
```
belaster -f
```
Belaster will create the following environment:
```
{ "Flag": True }
```


- Options start with a symbol. Any symbol is accepted.
```
OptionFlag(names={"-f"}, variable_name="F")
OptionFlag(names={"+g"}, variable_name="G")
OptionFlag(names={":h"}, variable_name="H")
```
allows to write
```
belaster -f +g :h
```


- Options can be given as many names as wished (a single symbol at the beginning of the name of an option does not necessarily means that it is a short name):
```
OptionEnum(
	names={"-e", "-p", "--enum1", "-other"},
	enum=EnumSample1, symbol_for_key="=", symbol_for_value=")", is_default_key=True,
	variable_name="VAR"
)
```
allows to use `-e`, `-p`, `--enum1` and `-other` interchangeably, they are synonymous.


- Short options can be chained, as long as they start with the same symbol. An option is short if it has only one character after one occurrence of its starting symbol.
```
OptionCount(names={"-f", "+g"}, variable_name="F")
OptionCount(names={"+f", "-g"}, variable_name="G")
```
with
```
belaster -fgg +fffgg
```
gives
```
{
	"F": 3
	"G": 5
}
```
Of course it is better to avoid obfuscating the usage of `belaster`.


- Chaining short options is possible:
```
OptionCount(names={"-b"}, variable_name="Count")
OptionContainer(
	names={"-c"}, separator_first="=", separator_middle=",",
	type_container=list, type_scalar=int, variable_name="Container"
)
```
with
```
belaster -bc=7,5,3
```
will give the following environment:
```
{
	"Container": [7, 5, 3],
	"Count": 1
}
```


- Signaling the end of options is possible with `OptionEnd`:
```
OptionCount(names={"+a"}, variable_name="Count")
OptionEnd(names={"++"})
```
with
```
belaster +aa+
```
will give
```
{
	"Count": 2,
}
```
The `+aa+` translates into `+a +a ++`, which is twice the option count followed by the end-of-option marker.

After the end-of-options marker only goals can be provided:
```
belaster +aa+ +a
```
will raise an error.


- Goals and options can be intertwined (except for the intervention of the end-of-option marker):
```
Abstract("all")
Abstract("clean")
OptionCount(names={"-b"}, variable_name="Count")
```
can be used as
```
belaster -b clean -bb all
```
The goals are
```
[clean, all]
```
and the environment is:
```
{
	"Count": 3,
}
```


## How to integrate into automation

There are two main ways to integrate Belaster into automation:
- by calling the command line executable `belaster`,
- by using the module `belaster`.

> [!WARNING]
> One should be careful when mixing the command line and the module.
> Some elements are declared globally and might not transfer from the domain of the executable to the domain of the module.
> One such element is the global instance of `ApplicationContext` that is attached to the class `ApplicationContextBinder`, it references all the Rules, Targets, etc of the User Belaster script given.

> [!TIP]
> When integrating the module `belaster` one may take inspiration from the source code of the executable `belaster` and find useful to run
> ```
> context = ApplicationContext()
> ApplicationContextBinder.application_context = context
> ```
> before anything else related to Belaster.


# Why the name "Belaster"

The name derives from the name of the genus of plants "aster", picked for aesthetic purposes.
