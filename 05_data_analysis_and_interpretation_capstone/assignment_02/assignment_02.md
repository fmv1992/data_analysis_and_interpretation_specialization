# Assignment 02

* Format: Blog entry
    * *url*: https://pydataexplorer.tumblr.com/post/161197349233/capstone-project-module-2-data-management
* Deliverables:
    * Draft of a *methods section*.
    * Samples:
        * Describe sample
        * Population
        * Describe selection criteria
        * Sample size
    * Measures:
        * Definitions and units
            * Input and response variable
        * How variables were managed
    * Statistical analyses:
        * Summary of statistical methods and purpose
            * Start with the simplest analyses
            * Eg: split into training/test sets, cross validation

## Samples

The sample is a collection of weather phenomenae including hurricanes, tornadoes, thunderstorms, hail, floods, drought conditions, lightning, high winds, snow, temperature extremes, etc.

The population is the population of all weather phenomenae. The collection of information of the events are gathered either by the National Weather Service or from "sources outside the National Weather Service (NWS), such as the media, law enforcement and/or other government agencies, private companies, individuals, etc."

The selection criteria do form the sample from the population is the availability of information and personnel do process the information.

The sample consists of N=166,049 weather events.

## Measures

* *Time*: years, months, days, hours, seconds depending on the context.
* *Time intervals*: years, months, days, hours, seconds depending on the context.
* *Injuries/deaths*: count of injuries/deaths. Adimensional.
* *Damage*: material losses in current (time of the report) USD.
* *Magnitude*: EG = Wind Estimated Gust; ES = Estimated Sustained Wind; MS = Measured Sustained Wind; MG = Measured Wind Gust (no magnitude is included for instances of hail).
* *Tornado scale*: Enhanced Fujita Scale describes the strength of the tornado based on the amount and type of damage caused by the tornado.
* *Tornado length*: The tornado path length in miles.
* *Tornado width*: The tornado path width while on the ground in feets.
* *Latitude/Longitude*: degrees.

## Statistical analyses

The statistical analyses will be executed after some data exploration. They may include:

* Variable reduction (Random Forests, PCA, LASSO, etc).
* Mean comparison (ANOVA).
* Regression (LASSO, Linear/Non-linear regression, etc).

This is not an exhaustive list. One should look at the final report to have the exact techniques described.

[comment]: # ( vim: set filetype=markdown fileformat=unix nowrap spell spelllang=en_us: )
