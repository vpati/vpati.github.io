#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys

import bibtexparser
import bibtexparser.bibdatabase as bibdatabase
import bibtexparser.bparser as bparser
import bibtexparser.bwriter as bwriter
import bibtexparser.customization as customization
import jinja2

__author__ = "Kevin Borgolte <kevin@borgolte.me>, Noah Spahn <ncs@ucsb.edu>"
__description__ = """BibTeX to Markdown converter"""
__version__ = "0.0.0"

FIELDS_TO_NOT_PATCH = ['author', 'booktitle', 'bibtex', 'journal', 'link',
                       'series']
FIELDS_TO_REMOVE = ['author+an', 'abstract', 'kind', 'keyword', 'timestamp',
                    'link', 'paper', 'slides', 'text', 'publishnote', 'aliases',
                    'video_url', 'urldate']
FIELD_DEFAULT_NO = ['paper', 'slides', 'text', 'video_url']
LOCAL_PDF_VAULT = 'content/files/publications/'

class Author:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return "{}, {}".format(self.lastname, self.firstname)


def customize(record):
    def fix_newlines(record):
        for key, value in record.items():
            if key in 'url':
                record[key]  = value.replace("\n", "")
            if key not in ('author', 'url', 'editor'):
                value = value.replace("\n", " ")
                record[key] = value.replace(r"\par", "\n\n")
        return record

    record = fix_newlines(record)
    record = customization.type(record)
    record = customization.convert_to_unicode(record)

    def split_author(record):
        if 'author' in record:
            authors = []
            for author in record['author']:
                lastname, firstname = author.split(", ")
                authors.append(Author(firstname, lastname))
            record['author'] = authors
        return record

    def parse_kind(kind, record):
        if kind in record and record[kind]:
            remove_translate_table = str.maketrans('', '', ', .')
            # record_id determines the name of the PDF
            # it's been hard-coded in the view:
            # layouts/partials/publications_icons.html
            # ----> this might want to be refactored
            record_id = record[kind].translate(remove_translate_table)
            record[kind] = {'name': record[kind],
                            'ID': record_id}
        return record

    record = customization.author(record)
    record = customization.journal(record)
    record = customization.keyword(record)
    record = customization.link(record)
    record = customization.doi(record)
    record = customization.page_double_hyphen(record)
    record = split_author(record)

    for kind in ('booktitle', 'series'):
        record = parse_kind(kind, record)

    def pdf_is_there(record):
        #print(record["ID"])
        filename = record["ID"]+".pdf"
        path_to_file = os.path.join(LOCAL_PDF_VAULT,filename)
        print(path_to_file)
        if os.path.isfile(path_to_file):
            print("\t PDF found!")
        else:
            print("\t NO PDF!!!")
            record["paper"] = "no"
        return record

    if ("paper" in record.keys() and record["paper"] == "yes"):
        #print(record)
        return pdf_is_there(record)

    return record


def raw_cleaned_bibtex(entry):
    bib = bibdatabase.BibDatabase()
    entry_cleaned = entry.copy()

    authors = []
    for a in entry['author']:
        authors.append(repr(a))
    entry_cleaned['author'] = " and ".join(authors)

    for k in ('journal', 'booktitle', 'series'):
        if k in entry:
            entry_cleaned[k] = entry[k]['name']

    if 'link' in entry:
        entry_cleaned['url'] = entry['link'][0]['url']

    for k in ('title',):
        if k in entry_cleaned:
            entry_cleaned[k] = "{{{}}}".format(entry_cleaned[k])

    for remove_field in FIELDS_TO_REMOVE:
        if remove_field in entry_cleaned:
            del entry_cleaned[remove_field]

    for k in entry_cleaned:
        entry_cleaned[k] = entry_cleaned[k].replace("&", "\&")

    bib.entries = [entry_cleaned]
    writer = bwriter.BibTexWriter()
    writer.align_values = True
    writer.display_order = ['title',
                            'author',
                            'booktitle',
                            'series',
                            'month',
                            'year']
    return bibtexparser.dumps(bib, writer)


def main():
    print("\n\n")
    count = 1

    publications = sys.argv[1]
    bib_filename = sys.argv[2]
    template_filename = sys.argv[3]
    out_directory = os.path.normpath(sys.argv[4])
    os.makedirs(out_directory, mode=0o700, exist_ok=True)

    # Load template
    with open(template_filename, 'r') as template_file:
        template = jinja2.Template(template_file.read())

    # Parse Bibliography
    parser = bparser.BibTexParser(ignore_nonstandard_types=False,
                                  common_strings=True,
                                  customization=customize)
    with open(bib_filename, 'r') as bib_file:
        website_bibtex = bib_file.read()
        publications = bibtexparser.loads(website_bibtex, parser)

    for key, entry in publications.entries_dict.items():
        if entry['ENTRYTYPE'] == 'unpublished':
            continue
        for default_field in FIELD_DEFAULT_NO:
            if default_field not in entry:
                entry[default_field] = 'no'
        entry['bibtex'] = re.sub(r"^ ", " " * 2,
                                 raw_cleaned_bibtex(entry),
                                 flags=re.MULTILINE)
        for k in entry:
            if k not in FIELDS_TO_NOT_PATCH:
                entry[k] = entry[k].replace("\&", "&")
            if k in ('journal', 'booktitle', 'series'):
                entry[k]['name'] = entry[k]['name'].replace("\&", "&")

        if 'aliases' in entry:
            entry['aliases'] = entry['aliases'].split(",")

        if 'link' in entry:
            entry['url'] = entry['link'][0]['url']
            del entry['link']

        with open("{}/{}.md".format(out_directory, key), 'w') as f:
            #print(count,entry['title'])
            f.write(template.render(entry))
            count+=1

    print("\n\n")

if __name__ == "__main__":
    main()
