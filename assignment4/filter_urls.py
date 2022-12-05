import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex

        r'<a[^>]+href=[\"]?([^#|\"]+)'  - [^>]+ is inspired from the "find_img_src"
                                        - ? will ensure that we stop right after the first occurrence of
                                          a # or the end of the url_link with the symbol \".
                                        - ([^#|\"]+) inspired from the "find_img_src" but adjusted it according to url.
                                          For instance, i have added an "or"/"|-symbol" so that we stop after the first
                                          occurrence of either a "#" or "|". 

    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    pattern = r'<a.*href=[\"]?([^#|\"]+)' 
    urls = re.findall(pattern, html)
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes
    i = 0
    for url in (urls):
        # Needs base_url 
        if(url[0] == "/" and url[1] != "/"):
            urls[i] = base_url + url
        # Only need to add the protocol
        elif(url[0] == "/" and url[1] == "/"):
            urls[i] = "https:" + url
        i += 1
    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        write_output_file(urls, output)
    return set(urls)


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    
    https://[a-z]{2}\.wikipedia.org.wiki.*?[^:]+       - [a-z]{2} ensures that we get all languages from 
                                                         aswell as ignore urls where the "wikipedia.org"
                                                         isn´t at at the beginning but rather at the end. 
                                                       - *?[^:]+ ensures that we end if there is a ":" but 
                                                         add everything before we meet a ":".
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = r'https://[a-z]{2}\.wikipedia.org.wiki.*?[^:]+'
    articles = []
    for url in urls:
        if(re.match(pattern, url)):
            articles.append(url)
    # Write to file if wanted
    if output:
        write_output_file(articles, output)
    return set(articles)


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string
    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set

def write_output_file(urls, output):
    """
    Procedure which writes the url link to a text file

    Args: 
        urls (list): Contains every url link
        output (str): String name for the file text 

    Return:
        None
    """
    f = open(output, "w")
    for url in (urls):
        f.write(url)
    f.close()