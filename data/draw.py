from diagrams import Cluster, Diagram
from diagrams.aws.general import General, GenericDatabase
from diagrams.aws.database import RDS
from diagrams.onprem.client import Client
from diagrams.generic.storage import Storage
from diagrams.onprem.client import User
from diagrams.programming.language import Javascript

def main():
    with Diagram('Data Flow Diagram', show=True):
        source_db = GenericDatabase('Standford DB')
        export_csv = Storage('Exported CSV')
        etl_notebook = Client('ETL Pipeline')
        postgres_db = RDS('DF In-house DB')
        export_json = General('JSON Export')
        with Cluster('ERN Stack'):
            react_frontend = Javascript('React')
            express_backend = Javascript('Express')
            nodejs_server = Javascript('Node.js')
        website_user = User('User')
        source_db >> export_csv >> etl_notebook >> postgres_db
        postgres_db >> export_json
        export_json >> express_backend >> react_frontend >> nodejs_server >> website_user

if __name__ == '__main__':
    main()
