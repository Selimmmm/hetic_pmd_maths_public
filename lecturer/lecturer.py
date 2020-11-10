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
        if subsection["type"] == "card":
            html = self.make_card(subsection)
        elif subsection["type"] == "exercice":
            html = self.make_exercice(subsection)
        return html

    ## TODO more in common card and exercice
    def make_card(self, subsection):
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

        ## Add card
        html = [
            """<div class="card ai-card p-5">""",
            title,
            field_html,
            """</div>""",
        ]
        html = "\n".join(html)
        return html

    def make_exercice(self, subsection):
        # Id and title
        subsection_title = subsection["title"]
        subsection_id = make_id(subsection_title)

        title = f"""<h2 id="{subsection_id}">{subsection_title}</h2>"""

        for f_name in field_names[1:]:
            f_html = self.make_field(subsection[f_name])
            field_html.append(f_html)
        field_html = "\n".join(field_html)

        ## Add card
        html = [
            """<div class="card ai-card p-5">""",
            title,
            field_html,
            """</div>""",
        ]
        html = "\n".join(html)
        return "None"

    ################################
    ## Make fields
    ################################

    def make_field(self, field):
        print(field)
        # print(field)
        title = f"""<h3>{field["title"]}</h2>"""
        line_html = ["<ul>"]
        for l_content in field["content"]:
            print(l_content)
            l_html = "<li>" + l_content + "</li>"
            line_html.append(l_html)
        line_html.append("</ul>")
        line_html = "\n".join(line_html)
        return title + "\n" + line_html

    def save_doc(self):
        path_document = PATH_CONTENT.replace(".yaml", ".html")
        with open(path_document, "w") as f:
            f.write(self.t)


if __name__ == "__main__":

    l = Lecturer()
