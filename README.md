# Autonomous Climate Resiliency Research Unit (ACRRU)

## Introduction

ACRRU is a multi-functional LLM-Driven research & reporting framework that automates the data collection and summarization needed to score infrastructure entities and regions with respect to the CRMM.

For a given entity, ACRRU executes a custom research plan to gather the data needed to address CRMM capabilities.

ACRRU then evaluates the collected data sources and identifies all evidence of CRMM capability criteria.

The evidence is summarized by capability into a final report for the entity, with all data sources cited. Multiple provider summaries can be further summarized into a regional report. 

## Usage 

### Setup

Use the `crmm_env.yml` file to create a conda environment for the application.

As of version 0.2.0, local usage will require licenses or accounts to the following services:
- [OpenAI](https://platform.openai.com/api-keys)
- [Tavily](https://app.tavily.com/home)
- [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python#authorize_credentials_for_a_desktop_application) if you would like to set up ACRRU logging. NOTE: If you do not wish to use this logging, please set the `gsheet_log` argument to `False`.

Please provide this information in a `.env` file at the root of the repository. Refer to `env_example.txt` for expected format.

### Running ACRRU

As of version 0.2.0, only local runs that begin with research are supported. 

Inputs are defined in text files within the `inputs` folder. Each line represents an entity and its geographic mapping, separated by a pipe. An example would be: 

```
Baltimore Gas and Electric|Maryland
Delmarva Power|Maryland
```

local ACRRU runs are performed in `main.py`.

## Outstanding Work

### 0.2.0

1. Build unit tests for all application functions
2. Build logging functionality for runtime performance monitoring
3. Move input prompt structure from config file to separate text file for easier access/editing
4. Integrate Database connections for caching ACRRU outputs
5. Implement more tools ACRRU may use

### Long Term

1. Integrate Self-Refinement post-processing
2. Geographic query front-end for user-defined region rollup
    - Integrate weighting scheme for entity contribution
    - Collect geo-coded data on non-electric infrastucture providers

This repository uses [Semanic Versioning](https://semver.org/).