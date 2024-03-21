# imports
import colorlog
import logging
import sys
from   typing import Dict

# LOGS
# set logger name = module name
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# stream handler. date format is ISO-8601
streamHandler: colorlog.StreamHandler = colorlog.StreamHandler(stream=sys.stdout)  # send logs to stdout instead of stderr
fmtStream: colorlog.ColoredFormatter = colorlog.ColoredFormatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)  # stream format
streamHandler.setFormatter(fmtStream)
streamHandler.setLevel(logging.DEBUG)  # set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.addHandler(streamHandler)

# coverage calculator
def minion_sequencing_calculator() -> Dict[str, float | str]:
    
    # Constants
    genome_length:    int = 5000000   # genome length (bases)
    coverage:         int = 30        # Desired coverage (e.g., 30x)
    read_length:      int = 5000      # Average read length (bases)
    reads_per_hour:   int = 20000     # Generation rate of reads by sequencer (per hour)
    max_run_hours:    int = 72        # Max run time for MinION flowcell (hours)
    
    # Lander-Waterman equation for coverage.  Not strictly applicable to long-reads but good to first-order approximation.
    # C = (N*L) / G
    # C = coverage
    # N = number of reads
    # L = read length (average; bases)
    # G = genome length (bases)

    # Number of reads
    # N = (G*C) / L
    number_of_reads: int = int((genome_length * coverage) / read_length)
    logger.info(f"Number of reads required for {coverage}X coverage = {number_of_reads:,}.")

    # Calculate number of hours to run sequencer
    total_hours: float = round(number_of_reads / reads_per_hour, 1)
    result_str: str = f"Estimated run time (hours): {total_hours}"
    
    # Check if the required time exceeds the maximum run time
    if total_hours > max_run_hours:
        logger.warning("Warning: the desired coverage requires more time than the maximum run time of the MinION flowcell.")
    
    return result_str

if __name__ == "__main__":
    
    # print results
    result_str: str = minion_sequencing_calculator()
    print(result_str)