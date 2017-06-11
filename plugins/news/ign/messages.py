class IGNNewsMessage:

    def __init__(self, row_data: dict):
        self.row_data = row_data

    def make_me_pretty(self):
        articles = []
        articles.append('`[Latest gaming news!]`')
        for item in self.row_data:
            article = (
                f"""*{item['title']}*\n{item['url']}
                """
            )
            articles.append(article)

        return '\n'.join(articles)
