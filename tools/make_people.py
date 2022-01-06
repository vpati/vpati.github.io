#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os
import sys

from shutil import copyfile
import pandas as pd
import jinja2

__author__ = "Noah Spahn <ncs@cs.ucsb.edu>"
__description__ = """Generates people entries from a data file"""
__version__ = "0.0.0"


def main(ppl_file, template_filename, out_directory, archive_location):

    with open(template_filename, "r") as template_file:
        template = jinja2.Template(template_file.read())

    os.makedirs(out_directory, mode=0o700, exist_ok=True)

    df = pd.read_csv(ppl_file)
    for index, record in df.iterrows():

        # Just show the current folks for now
        if record["public"]: #and record["current"]:

            key = "{}{}".format(record["first_name"][0], record["last_name"])
            key = key.lower()
            person_directory = os.path.normpath(out_directory + "/" + key)
            # Make directory
            print("making", person_directory)
            os.makedirs(person_directory, mode=0o700, exist_ok=True)

            # Find photo
            file_name = record["picture"]
            print("\tfile_path:", file_name)
            if isinstance(file_name, str):
                files_to_display = [name for name in os.listdir(archive_location)]
                if file_name in files_to_display:
                    copyfile(
                        os.path.join(archive_location, file_name),
                        os.path.join(person_directory, file_name),
                    )
                else:
                    record["picture"] = float("NaN")
                    print("\tNOT found")

            if(record["current"]):
                rank = record["rank_id"] + 10
            else:
                rank = record["rank_id"] + 60

            record["rank_id"] = str(rank) + record["rank"]

            with open("{}/{}.md".format(person_directory, "index"), "w+") as f:
                f.write(template.render(record))
                print("\t", index, record["first_name"], record["last_name"])

if __name__ == "__main__":
    pepl_file = sys.argv[1]
    template_fn = os.path.normpath(sys.argv[2])
    out_dir = os.path.normpath(sys.argv[3])
    archive_dir = os.path.normpath(sys.argv[4])
    main(pepl_file, template_fn, out_dir, archive_dir)
