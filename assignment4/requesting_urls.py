from typing import Dict, Optional

import requests as req

## -- Task 1 -- ##


def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    if params == None: 
        response = req.get(url) # url is only given
    else:
        response = req.get(url, params=params) # url and parameter/(key/value) is given

    assert response.status_code == 200 # Assert that the html response went well

    html_str = response.url + "\n" + response.text
    if output:
        # if output is specified, the response txt and url get printed to a
        # txt file with the name in `output`
        f = open(output, "w")
        f.write(html_str)
        f.close()
    return html_str
