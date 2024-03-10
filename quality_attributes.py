import csv
import json
import os

from filesystem import DataReader
from job.JobManager import JobManager
from ontology.OntologyManager import OntologyManager

def get_metrics_for_attributes(output_df, expected_df, results):
    actual_colnames = output_df.columns.tolist()
    expected_colnames = expected_df.columns.tolist()

    assert len(actual_colnames) == len(expected_colnames)

    for i in range(0, len(actual_colnames), 1):
        actual_colname = actual_colnames[i].split(".")[0]
        expected_colname = expected_colnames[i].split(".")[0]

        if actual_colname not in results:
            results[actual_colname] = {}
            results[actual_colname]["positive"] = 0
            results[actual_colname]["negative"] = 0
            results[actual_colname]["occurrences"] = 0

        if actual_colname.lower() == expected_colname.lower():
            results[actual_colname]["positive"] += 1
        else:
            results[actual_colname]["negative"] += 1

        results[actual_colname]["occurrences"] += 1

        i += 1

    return results


def get_job_metrics(job, case_name, results):
    job_name = job["name"]
    job_dataset_name = job["datasetName"]
    job_ontology_name = job["ontologyName"]
    job_ignore_columns = job["ignore"]

    print(f"Get metrics for attributes in job {job_name}, {case_name}")

    dr = DataReader.DataReader("datasets/")
    output_df = dr.read_output(job_dataset_name, case_name)
    expected_df = dr.read_expected(job_dataset_name, case_name)

    results = get_metrics_for_attributes(output_df, expected_df, results)

    return results


def write_results_to_file(results, case_name):
    fieldnames = results[list(results.keys())[0]].keys()
    with open(f'results/attrs/metrics_attr_{case_name}.csv', 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(results.values())


def main(jobs_group_name):
    jm = JobManager()
    jobs_infos = jm.read_jobs_infos(jobs_group_name)
    ontology_group = jobs_infos["ontologyGroup"]
    ontology_format = jobs_infos["ontologyFormat"]
    dataset_group = jobs_infos["datasetsGroup"]

    with open("config/experiments.json", 'r') as file:
        experiments_cases = json.load(file)

    om = OntologyManager(ontology_group, ontology_format)

    for case_name, case_data in experiments_cases.items():
        results = {}

        for job in jobs_infos["jobs"]:
            results = get_job_metrics(job, case_name, results)

            ontologies_attrs = om.get_ontologies_items_details(om.read_ontologies())

            for attr_name, attr_res in results.items():
                results[attr_name]["attr_name"] = attr_name

                if attr_name not in ontologies_attrs:
                    results[attr_name]["type"] = "TITLE"
                    results[attr_name]["importance"] = 0
                else:
                    results[attr_name]["type"] = ontologies_attrs[attr_name]["type"]
                    results[attr_name]["importance"] = ontologies_attrs[attr_name]["importance"]

                positive = attr_res["positive"]
                negative = attr_res["negative"]
                occurrences = attr_res["occurrences"]
                results[attr_name]["negative_perc"] = negative / occurrences
                results[attr_name]["positive_perc"] = positive / occurrences

        write_results_to_file(results, case_name)


if __name__ == "__main__":
    main(jobs_group_name="jobs_all")
