import json
import os


class JobManager:

    def read_jobs_infos(self, jobs_group_name):
        jobs_file_path = os.path.join("jobs", f"{jobs_group_name}.json")
        with open(jobs_file_path, 'r') as file:
            jobs_infos = json.load(file)

        return jobs_infos


