# hacktrack

This package provides a Python interface for quantifying hackathons.
It was designed during [Neurohackademy 2018](https://neurohackademy.org/) and was heavily inspired by the amazing work from the [BIDS Docathon](https://docathon.github.io/docathon/) team (see the [credits](#credits) section for more details).

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/rmarkello/hacktrack/master?filepath=notebook%2Fhacktrack.ipynb)

## Table of Contents

If you know where you're going, feel free to jump ahead:

* [Purpose](#purpose)
  * [Overview](#overview)
  * [Background](#background)
  * [Development](#development)
* [Getting started](#getting-started)
  * [Installation](#installation)
  * [Setup](#setup)
* [Example usage](#usage)
* [How to get involved](#how-to-get-involved)
* [Credits](#credits)

## Purpose

### Overview

This package provides a Python interface for tracking and plotting GitHub statistics, originally intended for use during hackathons or design sprints.

### Background

Hackathons and design sprints&mdash;sessions that bring together communities to work towards some collective goal&mdash;are becoming increasingly common; however, their outcomes and ultimate success are often difficult to quantify.
First created during [Neurohackademy 2018](https://neurohackademy.org/), this project was designed as a fun way to visualize the development of the the GitHub projects from that event.

### Development

While initial development of this project happened over the course of a few days, there are plans to continue development.
Currently, `hacktrack` can only measure information on commits and issues from GitHub repositories&mdash;but that is not enough!
We hope to expand the functionality of this package to provide a set of easy-to-use resources for quantifying _all_ aspects of hackathons and design sprints.
If you have some suggestions or want to help, take a look at our instructions on [how to get involved](#how-to-get-involved).

## Getting started

### Installation

You can install this package using [`conda`](http://conda.io/) with the [`environment.yml`](binder/environment.yml) inside the `binder` directory.
Assuming you have [installed `conda`](https://conda.io/docs/user-guide/install/index.html), the following should create a new environment with `hacktrack` installed:

```bash
git clone https://github.com/rmarkello/hacktrack
cd hacktrack
conda env create -f binder/environment.yml
source activate hacktrack
```

Other methods of installation (e.g., `pip install`) are not yet supported due to reliance on unstable upstream packages.

### Setup

If you are going to be _collecting_ data rather than simply analyzing / plotting pre-collected data, you will want to generate a GitHub personal access token.
`hacktrack` makes requests to [GitHub](https://developer.github.com/v3/) to get information on the repositories of interest; if a personal access token is not provided to these requests then you can be throttled (or temporarily banned!) for making too many.
Creating a personal access token to avoid this fate is mostly straightforward:

1. Sign in to your GitHub account,
2. Navigate to [https://github.com/settings/tokens](https://github.com/settings/tokens),
3. Select "Create new token",
4. Pick the relevant options for what this token should have access to (at the very least, check the box next to `repo`), and
5. Save the generated token somewhere private and secure (don't upload it to GitHub or share it with anyone!)

For ease of use with `hacktrack`, you can export the token as an environmental variable named `GITHUB_API` in the form username:key, as in:

```bash
export GITHUB_API=username:1234567890123456789012345678901234567890
```

`hacktrack` will check for the existence of this environmental variable in the event that a token is not provided directly to functions calls.

## Usage

Currently, this package is limited in its functionality (though there are plans to make it more general and flexible).
As it was originally designed to track GitHub activity over the course of the Neurohackademy 2018 hackathon, that is all it currently does!
To examine that data, you can load it directly by:

```python
>>> from hacktrack import PROJECT_LIST, get_project_info
>>> commits, issues = get_project_info(PROJECT_LIST, update=True)
```

The generated `commits` and `issues` are `pandas.DataFrame` objects with a whole bunch of information about commits and issues from the Neurohackademy 2018 projects.
You can feed these dataframes into the functions in `hacktrack.plotting` to do some fun plotting things!

To get an idea for the sorts of plots that can be generated, check out our [demo notebook](notebook/hacktrack.ipynb) or play around with an interactive version on [binder](https://mybinder.org/v2/gh/rmarkello/hacktrack/master?filepath=notebook%2Fhacktrack.ipynb).

## How to get involved

We're thrilled to welcome new contributors!
If you're interesting in getting involved, you should start by reading our [contributing guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

Once you're done with that, you can take a look at our list of active [issues](https://github.com/rmarkello/hacktrack/issues) and let us know if there's something you'd like to begin working on.

If you've found a bug, are experiencing a problem, or have a question, create a new issue with some information about it!
Someone will work on getting back to you as soon as possible.

## Credits

The backend for this repository relies on code from the [`watchtower`](https://github.com/docathon/watchtower) project created by the Berkeley Institute for Data Science (BIDS) for their [Docathon](https://docathon.github.io/docathon/) event, originally hosted in March 2017.
