# this whole thing should be redone with https://pyyaml.org/wiki/PyYAMLDocumentation

from toc import Book

def output_yaml(book):

    # all tocs must begin with these headers
    headers = ["format: jb-book", "root: intro", "parts:"]
    with open("new_toc.yml", "w") as outfile:
        outfile.write("\n".join(headers))

    # iterate thru chapters
    for chpt in book.chapters:
        # we'll collect the lines to write out in a list
        # note: makes it easy to do a "\n".join(lines)
        lines = []

        # caption = chapter name
        lines.append(f"\n  - caption: {chpt.name}")
        lines.append("    chapters:")


        # start with topics
        for topic in chpt.topics:
            lines.append(f"    - file:  {topic.md_path}")
            lines.append("      sections:")
            for nb in topic.nbs:
                lines.append(f"        - file:  {nb.nb_file}")
        
        # then do plain notebooks
        for nb in chpt.nbs:
            lines.append(f"    - file:  {nb.nb_file}")

        with open("new_toc.yml", "a") as outfile:
            outfile.write("\n".join(lines))
        
    
# need to run where you see the "notebooks" folder
output_yaml(Book("./notebooks"))