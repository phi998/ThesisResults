

class QualityMeasurer:

    def __init__(self):
        self.default_negative_labels = ["other", "unknown", ".", "", " "]

    def get_metrics(self, output_df, expected_df):
        quality_dict = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}

        output_columns_names = output_df.columns.tolist()
        expected_columns_names = expected_df.columns.tolist()

        assert len(output_columns_names) == len(expected_columns_names)

        columns_size = len(output_columns_names)
        for i in range(0, columns_size, 1):
            expected = expected_columns_names[i]
            actual = output_columns_names[i]

            quality_dict[self.compare_results(actual, expected)] += 1

        precision = quality_dict["tp"]/(quality_dict["tp"] + quality_dict["fp"])
        recall = quality_dict["tp"]/(quality_dict["tp"] + quality_dict["fn"])
        accuracy = (quality_dict["tp"] + quality_dict["tn"])/(quality_dict["tp"] + quality_dict["tn"] + quality_dict["fp"] + quality_dict["fn"])

        return {"a": accuracy, "p": precision, "r": recall, "f1": 2*(precision*recall)/(precision+recall), "tp": quality_dict["tp"],
                "tn": quality_dict["tn"], "fp": quality_dict["fp"], "fn": quality_dict["fn"]}

    def compare_results(self, actual, expected):
        actual_ = actual.lower()
        expected_ = expected.lower()

        if expected_ == actual_:
            if expected_ in self.default_negative_labels and actual_ in self.default_negative_labels:
                return "tn"
            return "tp"
        else:
            if expected_ in self.default_negative_labels and actual_ not in self.default_negative_labels:
                return "fp"
            return "fn"
