import os
from pyairtable import Api

api_key = os.getenv("jobb_app_token")


class JobApplication:
    
    def __init__(self):
        self.api = Api(os.getenv('jobb_app_token'))
        self.table = self.api.table('appbapK8d4hdSJFfo', 'tblXRumv8Kv4ZNxhJ')
    
    def get_job_apps(self, sort="ASC", max_records=10):
        app_date = ["app_date"]
        if sort == "DESC":
            app_date = ["-app_date"]
        table = self.table.all(sort=app_date, max_records=max_records)
        
        return table
    
    def add_job_app(self, company, role_type, app_date, Skills, Status, Link_to_job):
        fields = {'company': company, 
                  'role_type': role_type,
                  'app_date':app_date, 
                  'Skills': Skills, 
                  'Status': Status, 
                  'Link_to_job': Link_to_job}
        self.table.create(fields=fields)

if __name__ == '__main__':
    ja = JobApplication()
#     print(ja.get_job_apps())
#     ja.add_job_app('bombora', 'Machine Learning Engineer', '2/26/2025','A/B experiments,SQL,Python,communication skills', 'recently got reply', 'None')
    get_job_apps = ja.get_job_apps(max_records=1)
    print(get_job_apps)
#     print('job added successfully!')