def make_id(s):

    if s is None:
        s = ""

    s = s.lower()

    try:
        # Example : delete what's after the before the dot in
        # 'I. Probabilistic Vocabulary'
        s = s.split(".")[1]
    except:
        pass

    return s.strip().replace(" ", "_")


button_html = """<a class="btn btn-primary btn-lg btn-block" data-toggle="collapse" 
                     href="#{field_id}" role="button" aria-expanded="false" aria-controls="{field_id}">
                     {title}
                    </a><br>"""


svg_html = """<object>
              <!-- Your fall back here -->
              <img src="{path_svg}" style="width:100%;"/>
              </object>
            """