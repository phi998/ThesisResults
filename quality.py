import csv
import json
import os

from filesystem import DataReader
from job.JobManager import JobManager
from quality.QualityMeasurer import QualityMeasurer


def main(jobs_group_name):
    folder_name = "datasets/"

    qm = QualityMeasurer()
    jm = JobManager()

    with open("config/experiments.json", 'r') as json_file:
        experiments_dict = json.load(json_file)

    metrics_dict = {}

    jobs_infos = jm.read_jobs_infos(jobs_group_name)
    ontology_group = jobs_infos["ontologyGroup"]
    ontology_format = jobs_infos["ontologyFormat"]
    dataset_group = jobs_infos["datasetsGroup"]

    dr = DataReader.DataReader(folder_name)

    cases_metrics = {}

    for case_name, case_data in experiments_dict.items():

        ontology_enabled = case_data["ontology"]
        shots = case_data["shots"]
        fusion = case_data["fusion"]

        case_prec_tot = 0
        case_rec_tot = 0
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for job in jobs_infos["jobs"]:

            job_name = job["name"]
            dataset_name = job["datasetName"]
            ontology_name = job["ontologyName"]

            if dr.exists_dataset(dataset_name, case_name):
                expected_df = dr.read_expected(dataset_name, case_name)
                output_df = dr.read_output(dataset_name, case_name)

                if len(output_df.columns) == len(expected_df.columns):
                    print(f"getting metrics of:{dataset_name}")
                    metrics = qm.get_metrics(output_df, expected_df)

                    numeric_columns_len = len(output_df.select_dtypes(include=['number']).columns)

                    metrics["datasetName"] = dataset_name
                    metrics["output_columns"] = output_df.shape[1]
                    metrics["numeric_columns"] = numeric_columns_len
                    metrics["rows"] = output_df.shape[0]
                    metrics["has_ontology"] = ontology_enabled
                    metrics["shots"] = shots
                    metrics["fusion"] = fusion
                    metrics["case"] = case_name
                    metrics["ontology"] = ontology_name

                    case_prec_tot += metrics["p"]
                    case_rec_tot += metrics["r"]

                    tp += metrics["tp"]
                    tn += metrics["tn"]
                    fp += metrics["fp"]
                    fn += metrics["fn"]

                    metrics_dict[dataset_name] = metrics

        p = tp / (tp + fp)
        r = tp / (tp + fn)
        f1 = 2 * (p * r) / (p + r)

        cases_metrics[case_name] = {
            "case": case_name, "p": p, "r": r, "f1": f1,
            "tp": tp, "tn": tn, "fp": fp, "fn": fn}

        write_dict_to_file(metrics_dict, f'results/cases/metrics_{case_name}.csv')

    write_dict_to_file(cases_metrics, f'results/cases/metrics_{jobs_group_name}.csv')


def write_dict_to_file(dictionary, filename):
    fieldnames = dictionary[list(dictionary.keys())[0]].keys()
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(dictionary.values())


if __name__ == "__main__":
    main(jobs_group_name="jobs_all")
