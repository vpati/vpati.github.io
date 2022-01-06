# Hugo framework for the Seclab Website

This project utilized the [Hugo framework](https://gohugo.io/) to generate a static website. 
It is automatically built and deployed using github pages (via actions). For more details on how to accomlplish a build with Hugo in GitHub, see [their docs](https://gohugo.io/hosting-and-deployment/hosting-on-github/).

The artifacts are generated by scripts in the `tools` directory via the commands 
invoked from the **Makefile**.

The website is _published_ automatically on every commit to the master branch.


## Getting started (serving locally)
#### pre-requisites:
 - pipenv
 - python 3.8

#### setup
navigate to the directory then run `pipenv install`. 

If there are no problems, run`pipenv shell` and you should be all set to proceed.

Try `make` the project and install necessary dependencies. The generated artifacts are in `public/`. 
If everything looks fine, do `hugo serve` to spin up the server on your local machine for inspection.

Most (if not all) data you may care about is under `content/`. 


## Adding/editing members

1.  add/edit a line to the datafile `content/members.csv` with the appropriate affiliation
2.  add a photo to `content/headshots/` and reference it in the datafile

## Adding Publications

Add publication bib info to `content/publications.bib` file.

### if you would like to add a PDF
 - add the file to `content/files/publications`
 - **must** have the same name as string following the opening { on the first line (with a .pdf extension)
 - BibTeX for publications **must** be of a particular format (see below)
 - `make publications` does not throw an error if the bibtex is not processed correctly
 - running `make publications | less` will provide output about the processed publications
    - if you don't see your publication in the list, it was not processed


## Example Publication BibTeX Entry

    @InProceedings{ecs2000-system,                                              (PDF name must match this name. For example: ecs2000-system.pdf)
        # required
        title     = {{System: The Title of the Paper}},                         (important: title case)
        author    = {Lastname, Firstname and Second Lastname, Second Firstname},
        booktitle = {Proceedings of the 21st Example Conference on Security},
        series    = {ECS},
        month     = aug,
        year      = {2000},
        kind      = {conference/journal/magazine},                              (used to split on website)
        timestamp = {2000-08-01},                                               (day of publication)

        #  optional
        abstract  = {},                                                         (defaults to empty)
        paper     = {yes/no},                                                   (creates link to paper if there is a file with the right name, defaults to no)
        slides    = {yes/no},                                                   (creates slides link, defaults to no)
        url       = {},                                                         (creates link to publisher, defaults to none)
        video_url = {},                                                         (creates link to video, defaults to none)
    }
