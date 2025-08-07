import sys
import json
import logging
from datetime import datetime
from pyspark.context import SparkContext
from pyspark.sql.functions import col, lit, udf
from pyspark.sql.types import StringType
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)



# === CONFIGURATION ===

input_path = "s3://arti-glue-temp-dev/TRUNCATED-ovd-tv-data20250417.jsonl.gz"

# Get the connection information from Glue connection
try:
    connection_name = "azure_mysql_jdbc"
    logging.info(f"Retrieving connection information from Glue connection: {connection_name}")
    connection_options = glueContext.extract_jdbc_conf(connection_name)
    
    # Log connection details (without sensitive info)
    logging.info(f"Connection options keys: {list(connection_options.keys()) if connection_options else 'None'}")
    if connection_options and 'url' in connection_options:
        logging.info(f"URL found in connection options")
    else:
        logging.error(f"URL not found in connection options")
        
    # Fallback connection options if needed
    if not connection_options or 'url' not in connection_options:
        logging.warning("Using fallback connection options")
        connection_options = {
            'url': "jdbc:mysql://ai-arti-content-db-server.mysql.database.azure.com:3306/movies_and_shows",
            'user': "articontent",
            'password': "Adminpwd1",
            'driver': "com.mysql.cj.jdbc.Driver"
        }
    
    mysql_table = "ovd_tv"
except Exception as e:
    logging.error(f"Error retrieving connection information: {str(e)}")
    raise


# === STEP 1: Read JSONL with gzip compression ===
# Use permissive mode to handle malformed records
df = spark.read.option("compression", "gzip").option("mode", "PERMISSIVE").json(input_path)
logging.info(f"Initial row count from source: {df.count()}")

# Print the schema to understand the data structure
logging.info("Initial schema from source:")
df.printSchema()

# Convert the entire dataframe to JSON format and print it
logging.info("Full dataframe as JSON:")
json_df = df.toJSON().collect()
logging.info(json.dumps(json_df, indent=2))

# === STEP 2: Rename columns ===
field_mapping = {
    'videoId': 'video_id',
    'episodeTmsId': 'episode_tms_id',
    'hostName': 'episode_streaming_platform',
    'episodeId': 'episode_id',
    'url': 'episode_streaming_url'
}

for original, new in field_mapping.items():
    if original in df.columns:
        df = df.withColumnRenamed(original, new)

# === STEP 3: Filter out rows with NULL values in key fields (NOT NULL constraints) ===
logging.info(f"Row count before filtering NULL values in key fields: {df.count()}")

# Check for NULL values in each key field separately for better logging
for key_field in ['video_id', 'episode_tms_id', 'episode_id']:
    null_count = df.filter(col(key_field).isNull()).count()
    if null_count > 0:
        logging.warning(f"Found {null_count} rows with NULL values in {key_field}")
    
    # Also check for 'null' string literals
    null_string_count = df.filter(col(key_field) == 'null').count()
    if null_string_count > 0:
        logging.warning(f"Found {null_string_count} rows with 'null' string values in {key_field}")

# Filter out rows with NULL values or 'null' string literals in any of the key fields
df = df.filter(
    col('video_id').isNotNull() & (col('video_id') != 'null') &
    col('episode_tms_id').isNotNull() & (col('episode_tms_id') != 'null') &
    col('episode_id').isNotNull() & (col('episode_id') != 'null')
)
logging.info(f"Row count after filtering out NULL values and 'null' strings in key fields: {df.count()}")

# === STEP 4: Convert `viewingOptions` to JSON string ===
if 'viewingOptions' in df.columns:
    json_udf = udf(lambda x: json.dumps(x) if x else None, StringType())
    df = df.withColumn('episode_streaming_viewing_options', json_udf(col('viewingOptions')))
    df = df.drop('viewingOptions')

# === STEP 5: Add timestamps ===
from pyspark.sql.functions import current_timestamp, when, trim, col as spark_col
# Use current_timestamp() to ensure proper timestamp format
df = df.withColumn('data_last_update_timestamp', current_timestamp())
df = df.withColumn('inserttimestamp', current_timestamp())

# === STEP 6: Ensure all required columns exist and set correct data types ===
from pyspark.sql.types import StringType, TimestampType, StructType, StructField

# Define columns in the exact order as in the MySQL table definition
# This ensures the column order matches the table definition
column_definitions = [
    ('video_id', StringType(), False),               # varchar(255) NOT NULL
    ('episode_tms_id', StringType(), False),         # varchar(255) NOT NULL
    ('episode_streaming_platform', StringType(), True), # varchar(255) NULL
    ('episode_id', StringType(), False),             # varchar(50) NOT NULL
    ('episode_streaming_url', StringType(), True),  # text NULL
    ('episode_streaming_viewing_options', StringType(), True), # text NULL
    ('data_last_update_timestamp', TimestampType(), True), # timestamp NULL
    ('inserttimestamp', TimestampType(), True)      # timestamp NULL
]

# Create dictionaries for easier access
column_types = {col_name: col_type for col_name, col_type, _ in column_definitions}
not_null_columns = [col_name for col_name, _, is_nullable in column_definitions if not is_nullable]

# Ensure all required columns exist in the exact order defined
required_columns = [col_name for col_name, _, _ in column_definitions]

# Log the current schema before transformation
logging.info("Schema before column transformation:")
df.printSchema()

# Print the dataframe with key -> value -> datatype
logging.info("Dataframe with key -> value -> datatype:")
sample_data = df.limit(5).collect()
for row in sample_data:
    row_dict = row.asDict()
    for key, value in row_dict.items():
        data_type = type(value).__name__
        logging.info(f"{key} -> {value} -> {data_type}")

# Handle each column with special care to ensure proper conversion
for col_name in required_columns:
    if col_name not in df.columns:
        logging.info(f"Adding missing column: {col_name}")
        df = df.withColumn(col_name, lit(None).cast(column_types[col_name]))
    else:
        # For string columns, handle potential null values and ensure proper trimming
        if isinstance(column_types[col_name], StringType):
            # Replace any 'null' strings with actual NULL values first
            df = df.withColumn(col_name, 
                              when(col(col_name) == 'null', lit(None))
                              .when(col(col_name) == '', lit(None))
                              .otherwise(trim(col(col_name))))
            
            # Then cast to the correct type
            df = df.withColumn(col_name, col(col_name).cast(column_types[col_name]))
            
            # For NOT NULL columns, verify we don't have any nulls after conversion
            if col_name in not_null_columns:
                null_count = df.filter(col(col_name).isNull()).count()
                if null_count > 0:
                    logging.warning(f"Found {null_count} NULL values in NOT NULL column {col_name} after conversion")
        else:
            # For non-string columns, just cast to the correct type
            df = df.withColumn(col_name, col(col_name).cast(column_types[col_name]))

# === STEP 7: Reorder columns and create a schema with NOT NULL constraints ===
df = df.select(required_columns)

# Create a schema with proper nullable settings and correct order
schema_fields = []
for col_name, col_type, is_nullable in column_definitions:
    schema_fields.append(StructField(col_name, col_type, nullable=is_nullable))

# Create a new DataFrame with the correct schema
new_schema = StructType(schema_fields)
df = spark.createDataFrame(df.rdd, new_schema)

# === STEP 8: Write to Azure MySQL using Glue connection ===
try:
    logging.info(f"Writing {df.count()} records to {mysql_table}")
    
    # Make sure all required connection options are available
    required_keys = ['url', 'user', 'password']
    for key in required_keys:
        if key not in connection_options:
            raise ValueError(f"Missing required connection option: {key}")
    
    
    
    # Log the JDBC URL (without credentials)
    jdbc_url_parts = connection_options['url'].split('://')
    if len(jdbc_url_parts) > 1:
        logging.info(f"JDBC URL protocol: {jdbc_url_parts[0]}, target: {jdbc_url_parts[1].split('@')[-1] if '@' in jdbc_url_parts[1] else jdbc_url_parts[1]}")
    
    # Print the first 2 rows of the dataframe to verify data
    logging.info("Showing first 2 rows of the dataframe:")
    first_rows = df.limit(2).collect()
    for row in first_rows:
        logging.info(f"Row: {row.asDict()}")
    
   
    
    
    logging.info("Setting up JDBC writer")
    writer = df.write\
      .format("jdbc")
      
    logging.info("Adding connection options")
    writer = writer\
      .option("url", connection_options['url'])\
      .option("dbtable", mysql_table)\
      .option("user", connection_options['user'])\
      .option("password", connection_options['password'])\
      .option("driver", connection_options['driver'])\
      .option("stringtype", "unspecified")\
      .mode("append")
      
    # Log schema before saving to help with debugging
    logging.info("DataFrame schema before saving:")
    df.printSchema()
    
    # Verify NOT NULL fields are properly set
    for field in ['video_id', 'episode_tms_id', 'episode_id']:
        nullable = df.schema[field].nullable
        logging.info(f"Field {field} nullable status: {nullable} (should be False)")
        
    # Check for any remaining 'null' string values in key fields
    for field in ['video_id', 'episode_tms_id', 'episode_id']:
        null_string_count = df.filter(col(field) == 'null').count()
        if null_string_count > 0:
            logging.error(f"CRITICAL: Still found {null_string_count} rows with 'null' string values in {field} after filtering")
            # Don't attempt to write if we still have 'null' strings in key fields
            raise ValueError(f"Found {null_string_count} rows with 'null' string values in {field} which would violate NOT NULL constraints")
    
    # Check for empty strings in key fields
    for field in ['video_id', 'episode_tms_id', 'episode_id']:
        empty_string_count = df.filter(col(field) == '').count()
        if empty_string_count > 0:
            logging.error(f"CRITICAL: Found {empty_string_count} rows with empty string values in {field}")
            # Don't attempt to write if we have empty strings in key fields
            raise ValueError(f"Found {empty_string_count} rows with empty string values in {field} which would violate NOT NULL constraints")
    
    # Log row count one more time before saving
    row_count = df.count()
    logging.info(f"Final row count before saving: {row_count}")
    
    # Try to save with more detailed error handling
    try:
        # Collect a small sample for debugging if save fails
        debug_sample = df.limit(5).collect()
        
        # Save the data
        writer.save()
    except Exception as e:
        # Log detailed error information
        logging.error(f"Error during save operation: {str(e)}")
        logging.error("Debug sample of data that failed to save:")
        for i, row in enumerate(debug_sample):
            logging.error(f"Sample row {i}: {row.asDict()}")
        
        # Re-raise the exception
        raise
    
    logging.info("Successfully wrote data to database")
except Exception as e:
    logging.error(f"Error writing to database: {str(e)}")
    raise

job.commit()
