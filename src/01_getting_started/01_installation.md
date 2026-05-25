---
title: Installation
kind: guide
keywords: install, installation, build, source, clone, git, make, samples, tests, online tool, build configuration, compile-flags, linker-flags
---

# Installation

BuildIt is an open-source C++ library available under the MIT license. This page
covers how to fetch the source, build the library, run the included tests, and
use BuildIt from another C++ project.

## Requirements

BuildIt is a lightweight C++ library and does not require a special compiler.
You need:

- Linux or macOS
- A C and C++ compiler with C++11 support
- GNU Make
- Git

## Project Template

If you want to start an application that uses BuildIt, the quickest path is the
[buildit-dep-template](https://github.com/BuildIt-lang/buildit-dep-template)
repository.

It is a template project that builds BuildIt as a submodule, pulls the required
compiler and linker flags from BuildIt's Makefile, and provides a starting point
for applications built on top of BuildIt.

## Clone The Repository

Clone BuildIt recursively so submodules are fetched as well:

```sh
git clone --recursive https://github.com/BuildIt-lang/buildit.git
```

## Build From Source

From the cloned repository, run:

```sh
make -j $(nproc)
```

On systems where `nproc` is unavailable, replace `$(nproc)` with the number of
parallel build jobs you want to use.

Build-time options such as `DEBUG`, `RECOVER_VAR_NAMES`, and `ENABLE_D2X` are
documented on the [Build Configuration](02_build-configuration.md) page.

## Run Samples And Tests

The repository samples also serve as test cases. Run them with:

```sh
make run
```

The build system runs the samples and reports failures.

See [Samples](05_samples.md) for a short description of what each sample in the
repository is intended to exercise.

## Use BuildIt In A Project

After building BuildIt, note the path to the cloned repository. The supported way
to get compiler and linker flags is through the BuildIt Makefile targets
`compile-flags` and `linker-flags`.

This is recommended because BuildIt's build-time configuration affects the
include paths, compiler definitions, and linker flags that downstream programs
should use.

For a C++ file named `foo.cpp`:

```sh
g++ $(make --no-print-directory -C <path-to-buildit-repo> compile-flags) \
    foo.cpp \
    $(make --no-print-directory -C <path-to-buildit-repo> linker-flags) \
    -O3 -o foo
```

## Try BuildIt Online

You can try BuildIt without installing it by using the online tool:

[https://buildit.so/tryit](https://buildit.so/tryit)

The online tool lets you edit a BuildIt program, run it, and inspect generated
stages. It includes sample programs and can generate a shareable link for the
currently opened stage.

Because the code runs on BuildIt's web server, the online environment is
restricted:

1. File-system access and other restricted system calls are blocked.
2. Execution time and memory use are limited, so examples should be small.
