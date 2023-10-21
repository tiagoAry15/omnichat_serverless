from datetime import datetime
from typing import List


def generateTimestamp():
    """This function creates a unique timestamp string based on the current time."""
    currentTime = datetime.now()
    return currentTime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def getLatestTimestamp(timestampList: List[str]):
    """This function receives a list of timestamps and returns the earliest one."""
    convertedTimestamps = [datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") for timestamp in timestampList]
    return max(convertedTimestamps)


def convert_timestamp(input_str: str):
    # Parse the input string into a datetime object
    dt = datetime.strptime(input_str, '%Y-%m-%dT%H:%M:%SZ')

    # Format the datetime object into the desired string format
    formatted_str = dt.strftime('%H:%M at %d-%b-%Y')
    return formatted_str


def __main():
    res = generateTimestamp()
    return


if __name__ == "__main__":
    __main()
