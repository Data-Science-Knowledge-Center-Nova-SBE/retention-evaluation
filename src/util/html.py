from IPython.display import display, HTML


def set_cols(html):
    cols = [
        ("Transformation", 12),
        ("Rows", 3),
        ("Diff. rows", 3),
        ("N columns", 3),
        ("Columns", 20),
        ("N new cols", 3),
        ("New cols", 10),
        ("N deleted cols", 3),
        ("Deleted cols", 10),
        ("Null %", 30),
        ("Time", 3),
    ]
    html += "<thead><tr>"

    for col, width in cols:
        html += f"<th style='border:1px solid black;width: {width}%'>{col}</th>"
    html += "</tr></thead>"

    return html


def add_col(html, value, font_size=1):
    html += f"<td style='border:1px solid black;font-size: {font_size}em;'>{value}</td>"
    return html


def add_row(html, row):
    html = add_col(html, row["description"])
    html = add_col(html, row["n_rows"])
    html = add_col(html, row["diff_rows"])
    html = add_col(html, row["n_columns"])
    html = add_col(html, row["columns"], font_size=0.5)
    html = add_col(html, row["n_new_columns"])
    html = add_col(html, row["new_columns"], font_size=0.8)
    html = add_col(html, row["n_deleted_columns"])
    html = add_col(html, row["deleted_columns"], font_size=0.8)
    html = add_col(html, row["null_percentage"], font_size=0.7)
    html = add_col(html, row["time"])

    return html


def add_data(html, df):
    html += "<tbody>"
    for i, row in df.iterrows():
        html += "<tr>"
        html = add_row(html, row)
        html += "</tr>"
    html += "</tbody>"
    return html


def save_to_file(html):
    with open("outputs/docs.html", "w") as file:
        file.write(html)


def docs_to_html(df):
    # start table
    html = """
    <style>
    .tableFixHead{ overflow: auto; height: 100px; }
    .tableFixHead thead th { position: sticky; top: 0; z-index: 1; }
    table  { border-collapse: collapse; width: 100%; }
    th, td { padding: 8px 16px; }
    th     { background:#eee; }
    </style>
    <table class='tableFixHead'>
    """

    # add columns
    html = set_cols(html)

    # add data
    html = add_data(html, df)

    # end table
    html += "</table>"

    # save into outputs
    save_to_file(html)

    # display
    html = HTML(html)
    display(html)
