from urllib.parse import ParseResult, urlunparse


class Story(object):
    def __init__(self, url: ParseResult,
                 comment_url: ParseResult,
                 title: str):
        self.url = url
        self.comment_url = comment_url
        self.title = title
        self.str_url = urlunparse(url)
        self.str_comment_url = urlunparse(comment_url)

    def __repr__(self):
        return """Title: {}
URL: {}
Comment URL: {}""".format(self.title, str(self.str_url), str(self.str_comment_url))
