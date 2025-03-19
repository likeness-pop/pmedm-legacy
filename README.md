# Python-R Bridge to [PMEDMrcpp](https://bitbucket.org/jovtc/pmedmrcpp/src/master/)

[![pipeline status](https://code.ornl.gov/likeness/pmedm_legacy/badges/develop/pipeline.svg?job=karma&key_text=pipeline:+develop&key_width=110)](https://code.ornl.gov/likeness/pmedm_legacy/-/commits/develop)
[![pipeline status](https://code.ornl.gov/likeness/pmedm_legacy/badges/main/pipeline.svg?job=karma&key_text=pipeline:+main&key_width=110)](https://code.ornl.gov/likeness/pmedm_legacy/-/commits/main)
[![coverage report](https://code.ornl.gov/likeness/pmedm_legacy/badges/develop/coverage.svg)](https://code.ornl.gov/likeness/pmedm_legacy/-/commits/develop)
[![Latest Release](https://code.ornl.gov/likeness/pmedm_legacy/-/badges/release.svg)](https://code.ornl.gov/likeness/pmedm_legacy/-/releases)


The included conda environment (`environment.yml`) currently comprises:

* Required:
  * `jovtc/pmedmrcpp` - R/C++ from [BitBucket](https://bitbucket.org/jovtc/pmedmrcpp/src/master/)
     * This is a reinstance of [`nnnagle/pmedmrcpp`](https://bitbucket.org/nnnagle/pmedmrcpp/src/master/)
  * `likeness/pmedmrcpp-pal` – R (our wrapper of `jovtc/pmedmrcpp`)
* Extras for notebooks
  * `likeness/livelive` – Python
  * `likeness/likeness-vitals` – Python

## OS Compatibility

| OS                        | Compatible            |  
| ---                       | ---                   |
| GNU/Linux (Ubuntu 20.04)  | :white_check_mark:    |  
| OSX (Intel)               | :white_check_mark:    |
| OSX (ARM64)               | :white_check_mark:    |
| Windows                   | :x: (broken)          |

## Prerequisites

1. One of the following installers:

    * [`miniforge`](https://github.com/conda-forge/miniforge) (***highly recommended***)
      * use the [`mamba`](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) command
    * [`miniconda`](https://docs.conda.io/projects/miniconda/en/latest/)
      * use the [`conda`](https://conda.io/projects/conda/en/latest/commands/index.html) command

2. Generate an SSH key for package installs from Gitlab:

    * Make a new SSH key for your machine `ssh-keygen -t ed25519 -C "<key_name>"`. Other settings may be left default. 
    * Copy the local key using the instructions [here](https://code.ornl.gov/help/user/ssh.md#add-an-ssh-key-to-your-gitlab-account). On Windows, you can also open `C:/Users/<user_id>/.ssh/id_ed25519.pub` in a text editor and copy the contents. 
    * On the upper-right panel of GitLab, click on your icon and choose `Preferences`. On the sidebar, choose `SSH Keys`. Copy your public key into the `Key` dialog and then save it with `Add key`.

3. Navigate to your project parent directory and clone `pmedm_legacy` locally: 

    ```
    git clone ssh://git@code.ornl.gov/likeness/pmedm_legacy.git@main
    ```
4. Navigate to `pmedm_legacy`

    ```
    cd pmedm_legacy
    ```

## Setup

* Create the Mamba or Conda environment (we recommend `mamba`):

    ```
    mamba env create -f environment.yml 
    mamba activate py312_pmedm_legacy_latest
    ```

### Additional Likeness synthetic population stack and additional R libraries

#### Linux & macOS

* In the `bash` shell, enter:
    ```
    bash post.sh
    ```
