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
        etl_notebook = Server('Analysis Pipeline')
        csv_2_json = Server('Internal Comms Pipeline')
        data_analytics = Singer('Data Analysis')
        raw_pipe = Server('Catalog Pipeline')
        export_json = Resource('JSON Data')
        frontend = Javascript('Frontend')
        website_user = User('Stakeholder')
        source_csv >> raw_pipe >> export_json
        source_db >> source_csv >> etl_notebook >> data_analytics
        data_analytics >> csv_2_json >> export_json
        export_json >> frontend >> website_user

if __name__ == '__main__':
    main()
