# directional-survey-converter

Convert directional surveys to their respective latitude longitude survey points










# Dependencies

## Configure and Manage Your Environment with Anaconda

Per the Anaconda [docs](http://conda.pydata.org/docs):

> Conda is an open source package management system and environment management system 
for installing multiple versions of software packages and their dependencies and 
switching easily between them. It works on Linux, OS X and Windows, and was created 
for Python programs but can package and distribute any software.

## Overview
Using Anaconda consists of the following:

1. Install [`miniconda`](http://conda.pydata.org/miniconda.html) on your computer, by selecting the latest Python version for your operating system. If you already have `conda` or `miniconda` installed, you should be able to skip this step and move on to step 2.
2. Create and activate * a new `conda` [environment](http://conda.pydata.org/docs/using/envs.html).

\* Each time you wish to work on any exercises, activate your `conda` environment!

---


**Now, we're ready to create our local environment**

1. Clone the repository, and navigate to the downloaded folder.


2. Create (and activate) a new environment, named `dir-survey` with Python 3.6. If prompted to proceed with the install `(Proceed [y]/n)` type y.

	- __Linux__ or __Mac__: 
	```
	conda create -n dir-survey python=3.8
	source activate dir-survey
	```
	- __Windows__: 
	```
	conda create --name dir-survey python=3.8
	activate dir-survey
	```
	
	At this point your command line should look something like: `(dir-survey) <User>:directional-survey-converter <user>$`. The `(dir-survey)` indicates that your environment has been activated, and you can proceed with further package installations.