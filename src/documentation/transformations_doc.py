from src.util.timer import Timer
import pandas as pd


class TransformationsDoc():

    def __init__(self, description="", display=True, is_train=True):
        self.docs = []

        self.header = [
            "description",
            "n_rows",
            "diff_rows",
            "n_columns",
            "columns",
            "n_new_columns",
            "new_columns",
            "n_deleted_columns",
            "deleted_columns",
            "null_percentage",
            "time"
        ]

        self.start_description = description
        self.display = display
        self.is_train = is_train

        self.final_docs=None
        self.saved=False

    def _get_dataframe_info(self, df):
        n_rows, n_columns = df.shape
        columns = list(df.columns)
        return n_rows, n_columns, columns

    def set_description(self, text):
        self.start_description = text

    def start(self, description, df):
        self.description = description
        self.n_rows, self.n_columns, self.columns = self._get_dataframe_info(df)

        if len(self.docs) == 0:
            self.docs.append(
                [
                    "Start - " + self.start_description,
                    self.n_rows,
                    0,
                    self.n_columns,
                    self.columns,
                    0,
                    [],
                    0,
                    [],
                    [],
                    '0.0s'
                ]
            )

        # start timer
        if self.display:
            print("\n" + description)

        self.timer = Timer(self.display)

    def end(self, df):
        # stop timer
        time = self.timer.stop()

        # check differences
        n_rows, n_columns, columns = self._get_dataframe_info(df)
        diff_rows = n_rows - self.n_rows

        # set new columns
        new_columns = [x for x in columns if not x in self.columns]
        n_new_columns = len(new_columns)

        # set deleted
        deleted_columns = [x for x in self.columns if not x in columns]
        n_deleted_columns = len(deleted_columns)

        # set percentage null
        percentage_null = []
        for column in list(df.columns):
            null_percentage = df[column].isnull().sum() / len(df) * 100
            if null_percentage == 0:
                continue
            value = (column, null_percentage)
            percentage_null.append(value)

        percentage_null.sort(key=lambda x:-x[1])

        # add to docs
        self.docs.append(
            [
                self.description,
                n_rows,
                diff_rows,
                n_columns,
                columns,
                n_new_columns,
                new_columns,
                n_deleted_columns,
                deleted_columns,
                percentage_null,
                time
            ]
        )

    def save(self):
        if self.saved:
            return self.final_docs

        # sum column time
        time = [x[-1] for x in self.docs]
        seconds = 0

        for item in time:
            items = item.split()
            if len(items) == 2:
                seconds += float(items[0][:-1]) * 60
            seconds += float(items[-1][:-1])

        time = "{}m {}s".format(int(seconds / 60), seconds % 60)

        # new columns
        new_columns = [x for x in self.docs[-1][4] if not x in self.docs[0][4]]
        n_new_columns = len(new_columns)

        # delete columns
        deleted_columns = [x for x in self.docs[0][4] if not x in self.docs[-1][4]]
        n_deleted_columns = len(deleted_columns)

        # set percentage null
        percentage_null = self.docs[-1][-2]

        # add conclusion row
        self.docs.append(
            [
                "Conclusion",
                self.docs[-1][1],
                self.docs[-1][1] - self.docs[0][1],
                self.docs[-1][3],
                self.docs[-1][4],
                n_new_columns,
                new_columns,
                n_deleted_columns,
                deleted_columns,
                percentage_null,
                time
            ]
        )

        # to dataframe
        docs = {}
        for row in self.docs:
            for i, column in enumerate(self.header):
                if not column in docs:
                    docs[column] = []
                docs[column].append(row[i])

        self.final_docs = pd.DataFrame(docs)
        self.saved=True
        return self.final_docs
