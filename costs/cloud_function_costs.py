import datetime
import os

from dotenv import load_dotenv
from google.cloud import functions_v1, billing_v1, monitoring_v3
from google.cloud.billing_v1.types import ListServicesRequest
from google.cloud.functions_v1.types import ListFunctionsRequest
from google.protobuf import timestamp_pb2
from google.protobuf.timestamp_pb2 import Timestamp

load_dotenv()

project_id = 'pizzadobill-rpin'
billing_account_name = os.getenv("GOOGLE_CLOUD_BILLING_ACCOUNT_NAME")
DAYS_IN_THE_PAST = 30

# Initialize the clients
functions_client = functions_v1.CloudFunctionsServiceClient()
billing_client = billing_v1.CloudBillingClient()

now = datetime.datetime.utcnow()
end_time_seconds = int(now.timestamp())
start_time_seconds = int((now - datetime.timedelta(days=DAYS_IN_THE_PAST)).timestamp())

# Define the time interval (you can modify this according to your needs)
interval = monitoring_v3.TimeInterval(
    start_time=timestamp_pb2.Timestamp(seconds=start_time_seconds),
    end_time=timestamp_pb2.Timestamp(seconds=end_time_seconds)
)


# Initialize the Monitoring client
client = monitoring_v3.MetricServiceClient()

# Get all deployed functions in the project
request = ListFunctionsRequest(parent=f"projects/{project_id}/locations/-")
functions = functions_client.list_functions(request=request)

for function in functions:
    # Assuming each function's name has the structure: projects/*/locations/*/functions/*
    function_name = function.name.split('/')[-1]

    # Construct filter for the Cloud Monitoring API request
    filter_str = f'resource.type="cloud_function" AND resource.labels.function_name="{function_name}" AND metric.type="cloudfunctions.googleapis.com/function/execution_count"'

    results = client.list_time_series(name=f"projects/{project_id}",
                                      filter=filter_str,
                                      interval=interval,
                                      view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL)
    invocations = 0
    for result in results:
        for point in result.points:
            invocations += point.value.int64_value

    # Calculate cost based on number of invocations and any other metrics you want
    cost_per_invocation = 0.0000004  # Sample rate; adjust as per your actual pricing
    total_cost = invocations * cost_per_invocation

    print(f"Function {function_name} has been invoked {invocations} times. Estimated cost: ${total_cost:.6f}")