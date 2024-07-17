'''Data pipeline to pull data from local csv and load data into the DF database.'''
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv # type: ignore
import psycopg2 as psql # type: ignore
import warnings

class EnvSecrets:
    def __init__(self) -> None:
        '''Fetch all sensitive data and load into variables for later use.'''
        load_dotenv()
        self.db_name = os.getenv('DATABASE_NAME')
        self.db_host = os.getenv('DATABASE_HOST')
        self.db_port = int(os.getenv('DATABASE_PORT'))
        self.sql_user = os.getenv('SQL_USERNAME')
        self.sql_pass = os.getenv('SQL_PASSWORD')
        self.schema = os.getenv('SQL_SCHEMA')

class DatabaseConnection:
    def __init__(self, secret:EnvSecrets) -> None:
        '''Open database connection.'''
        try:
            self.connection = psql.connect(
                database = secret.db_name
                , host = secret.db_host
                , port = secret.db_port
                , user = secret.sql_user
                , password = secret.sql_pass
            )
            self.cursor = self.connection.cursor()
            self.valid = True
        except:
            '''Possible expansion for email sending, notifying database failure or invalid credentials.'''
            self.valid = False
    def close(self) -> None:
        '''Close database connection.'''
        try:
            self.connection.close()
        except:
            pass

class DataPipeline:
    def __init__(self, secret, csv_source) -> None:
        self.new_data = pd.DataFrame()
        self.secret = secret
        self.csv = csv_source
    def extract(self) -> None:
        self.new_data = pd.read_csv(self.csv)
    def transform(self) -> None:
        self.new_data = self.new_data[(self.new_data['type']=='model')]
        for column_name in self.new_data.copy().columns:
            if len(self.new_data[column_name].unique()) <= 1:
                self.new_data.drop(columns=column_name, inplace=True)
        self.new_data['model_pk'] = range(1, 1+len(self.new_data)) # primary key for model
        self.new_data['created_date'] = pd.to_datetime(self.new_data['created_date'], errors='coerce')
        _temp = self.new_data['modality'].apply(repackage_modality).apply(pd.Series)
        self.new_data[['input_modality', 'output_modality']] = _temp
        self.new_data.drop(columns='modality', inplace=True)
        self.new_data[['dependencies']] = self.new_data[['dependencies']].copy().map(
            lambda raw: [s.strip(' ').strip('\'') for s in str(raw)[1:-1].split(',')]
        )
        self.new_data = self.new_data.explode('input_modality')
        self.new_data = self.new_data.explode('output_modality')
        self.new_data = self.new_data.explode('dependencies')
        self.new_data['table_pk'] = range(1, 1+len(self.new_data))
    def load(self, database) -> None:
        table_name = 'hackathon_july24_test'
        primary_key = 'table_pk'
        self.backup(primary_key)
        varchar_length = 10000
        create_table_sql = f'''
CREATE TABLE IF NOT EXISTS {self.secret.schema}.{table_name} (
    {primary_key} int PRIMARY KEY
    , model_pk int
    , name varchar({varchar_length})
    , organization varchar({varchar_length})
    , description varchar({varchar_length})
    , created_date date
    , url varchar({varchar_length})
    , size varchar({varchar_length})
    , analysis varchar({varchar_length})
    , dependencies varchar({varchar_length})
    , quality_control varchar({varchar_length})
    , access varchar({varchar_length})
    , license varchar({varchar_length})
    , intended_uses varchar({varchar_length})
    , prohibited_uses varchar({varchar_length})
    , monitoring varchar({varchar_length})
    , feedback varchar({varchar_length})
    , model_card varchar({varchar_length})
    , training_emissions varchar({varchar_length})
    , training_time varchar({varchar_length})
    , training_hardware varchar({varchar_length})
    , input_modality varchar({varchar_length})
    , output_modality varchar({varchar_length})
);'''
        database.cursor.execute(create_table_sql)
        self.new_data = self.new_data.replace({np.nan: None})
        self.new_data['created_date'] = self.new_data['created_date'].replace({pd.NaT: None})
        query = f'SELECT {primary_key} FROM {self.secret.schema}.{table_name}'
        existing_data = pd.read_sql(query, database.connection)
        existing_set = set(existing_data[primary_key])
        non_duplicate_data = self.new_data[~self.new_data[primary_key].isin(existing_set)]
        if not non_duplicate_data.empty:
            tuples = [tuple(x) for x in non_duplicate_data.to_numpy()]
            columns = ','.join(non_duplicate_data.columns)
            values = ','.join(['%s'] * len(non_duplicate_data.columns))
            insert_query = f'INSERT INTO {self.secret.schema}.{table_name} ({columns}) VALUES ({values})'
            database.cursor.executemany(insert_query, tuples)
        database.connection.commit()
    def backup(self, primary_key) -> None:
        '''Adding to a back up csv file.'''
        file_name = '../data/processed.csv'
        try:
            existing_data = pd.read_csv(file_name)
            for column_name in existing_data.columns:
                if 'Unnamed' in column_name:
                    existing_data.drop(columns=column_name, inplace=True)
            incoming_data = pd.concat([existing_data, self.new_data], ignore_index=True)
            incoming_data.set_index(primary_key, inplace=True)
            incoming_data.drop_duplicates(keep='first', inplace=True)
            incoming_data.sort_index(inplace=True)
            incoming_data.reset_index(inplace=True)
            incoming_data.to_csv(file_name)
        except FileNotFoundError:
            self.new_data.to_csv(file_name)

def repackage_modality(raw:str) -> tuple[list[str]]:
    raw = str(raw)
    semicolon_count = raw.count(';')
    assert semicolon_count <= 1, 'LLM modality invalid.'
    if semicolon_count == 0:
        raw = raw + ';' + raw
    modal_input_str, modal_output_str = raw.split(';')
    modal_inputs = [s.strip() for s in modal_input_str.split(',')]
    modal_outputs = [s.strip() for s in modal_output_str.split(',')]
    return modal_inputs, modal_outputs


def main() -> None:
    warnings.filterwarnings('ignore', message='.*pandas only supports SQLAlchemy connectable.*')
    csv_filepath = '../data/assets.csv'
    sensitive_data = EnvSecrets()
    df_database = DatabaseConnection(sensitive_data)
    database_seeding = DataPipeline(sensitive_data, csv_filepath)
    database_seeding.extract()
    database_seeding.transform()
    try:
        database_seeding.load(df_database)
        print('Table created successfully!')
    except Exception as e:
        print(e)
    finally:
        df_database.close()

if __name__ == '__main__':
    main()
