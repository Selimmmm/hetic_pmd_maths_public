import os
import re
import yaml

from utils import make_id

PATH_TEMPLATES = "../templates/"
PATH_TEMPLATE = os.path.join(PATH_TEMPLATES, "template.html")
PATH_CONTENT = os.path.join(PATH_TEMPLATES, "intro_proba_discretes.yaml")
PATH_CONTENT = "intro_proba_discretes.yaml"


##TODO :
# research subsection titles in following text and highlight the matched strings (lower)


##TODO : h3 and h2


class Lecturer:
    def __init__(self):

        self.load_template()
        self.load_content()
        self.mk_title()
        self.make_sections()
        self.save_doc()

    ################################
    ## Load templates and content

    def load_template(self):
        with open(PATH_TEMPLATE, "r") as f:
            self.t = f.read()

    def load_content(self):
        # Read YAML file
        with open(PATH_CONTENT, "r") as f:
            self.c = yaml.safe_load(f)

    ################################
    ## Make blocks

    def mk_title(self):
        self.t = self.t.replace("{{title}}", self.c["title"])

    ################################
    ## Make sections

    def make_sections(self):
        # All section names
        section_names = sorted([name for name in self.c if name.startswith("section")])

        # Make html for each section
        section_html = []
        for s_name in section_names:
            s_html = self.make_section(self.c[s_name])
            section_html.append(s_html)
        section_html = "\n".join(section_html)

        # Inject in template
        self.t = self.t.replace("{{block_section}}", section_html)

    def make_section(self, section):
        # Id and title
        section_title = section["title"]
        section_id = make_id(section_title)
        title = f"""<h1 id="{section_id}">{section_title}</h2>"""

        # Subsections
        subsection_html = "\n".join([title, self.make_subsections(section)])

        return subsection_html

    ################################
    ## Make subsections

    def make_subsections(self, section):
        # All subsection names
        subsection_html = []
        for subsection in section["subsections"]:
            ss_html = self.make_subsection(subsection)
            subsection_html.append(ss_html)
        subsection_html = "\n".join(subsection_html)
        return subsection_html

    def make_subsection(self, subsection):

        # Id and title
        subsection_title = subsection["title"]
        subsection_id = make_id(subsection_title)

        title = f"""<h2 id="{subsection_id}">{subsection_title}</h2>"""

        fields = subsection["fields"]
        field_html = []
        for f in fields:
            f_html = self.make_field(f)
            field_html.append(f_html)
        field_html = "\n".join(field_html)

        html = [
            """<div class="card ai-card p-5">""",
            title,
            field_html,
            """</div>""",
        ]
        html = "\n".join(html)

        return html

    ################################
    ## Make fields
    ################################

    def make_field(self, field):
        if field["type"] == "num":
            opening = "<ol>"
            closing = "</ol>"

        elif field["type"] == "bull":
            opening = "<ul>"
            closing = "</ul>"

        title = field["title"]

        print(title)

        field_id = make_id(title)

        if title:
            title = f"""<h3>{title}</h2>"""
        else:
            title = ""

        button = f"""<a class="btn btn-primary btn-sm" data-toggle="collapse" 
                     href="#{field_id}" role="button" aria-expanded="false" aria-controls="{field_id}">
                     Link with href
                    </a>"""

        if field.get("button", False):
            print("YEAH")
            line_html = [
                opening,
                button,
                f"""<div class="collapse" id="{field_id}">""",
            ]
        else:
            line_html = [opening]

        for l_content in field["content"]:
            l_html = "<li>" + l_content + "</li>"
            line_html.append(l_html)
        line_html.append(closing)

        if field.get("button", False):
            line_html.append("<div>")

        line_html = "\n".join(line_html)
        return title + "\n" + line_html

    def save_doc(self):
        path_document = PATH_CONTENT.replace(".yaml", ".html")
        with open(path_document, "w") as f:
            f.write(self.t)


if __name__ == "__main__":

    l = Lecturer()
