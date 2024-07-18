from diagrams import Cluster, Diagram
from diagrams.aws.database import RDS
from diagrams.onprem.compute import Server
from diagrams.onprem.analytics import Singer
from diagrams.generic.storage import Storage
from diagrams.azure.general import Resource
from diagrams.programming.language import Javascript
from diagrams.onprem.client import Client, User

def main():
    with Diagram(' ', filename='data_flow_diagram', show=True):
        source_db = RDS('Stanford Source')
        source_csv = Resource('Downloadable CSV')
        with Cluster('Back End'):
            etl_notebook = Server('Incoming Pipeline')
            data_analytics = Singer('Data Analysis')
            csv_2_json = Server('Outgoing Pipeline')
        export_json = Resource('JSON Data')
        with Cluster('Front End'):
            express_backend = Javascript('Express')
            react_frontend = Javascript('React')
            nodejs_server = Javascript('Node')
        website_user = User('Stakeholder')
        source_db >> source_csv >> etl_notebook >> data_analytics
        data_analytics >> csv_2_json >> export_json
        export_json >> express_backend >> react_frontend >> nodejs_server >> website_user

if __name__ == '__main__':
    main()
