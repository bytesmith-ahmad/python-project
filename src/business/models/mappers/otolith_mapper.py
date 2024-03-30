class OtolithMapper:
    @staticmethod
    def rows_as_otoliths(rows): # where rows is a list of sqlite3 Row
        otoliths = []
        for row in rows:
            model = Model(*row)
            models.append(model)
        return models