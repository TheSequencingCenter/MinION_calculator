# imports
from typing import Dict, Union
from utilities.loggerUtil import logger 

# coverage calculator
def minion_sequencing_calculator() -> Dict[str, Union[float, str]]:
    
    # Constants
    genome_length:    int = 5000000   # genome length (bases)
    coverage:         int = 50        # Desired coverage (e.g., 30x)
    read_length:      int = 5000      # Average read length (bases)
    reads_per_hour:   int = 20000     # Generation rate of reads by sequencer (per hour)
    max_run_hours:    int = 72        # Max run time for MinION flowcell (hours)
    
    # Lander-Waterman equation for coverage. Not strictly applicable to long-reads but good to first-order approximation.
    # C = (N*L) / G
    # C = coverage
    # N = number of reads
    # L = read length (average; bases)
    # G = genome length (bases)

    # Number of reads
    number_of_reads: int = int((genome_length * coverage) / read_length)
    logger.info(f"Number of reads required for {coverage}X coverage = {number_of_reads:,}.")

    # Calculate number of hours to run sequencer
    total_hours: float = round(number_of_reads / reads_per_hour, 1)
    result: str = f"Estimated run time (hours): {total_hours}"
    
    # Check if the required time exceeds the maximum run time
    if total_hours > max_run_hours:
        logger.warning("Warning: the desired coverage requires more time than the maximum run time of the MinION flowcell.")
    
    return {"Estimated run time (hours)": total_hours, "Message": result}

if __name__ == "__main__":
    
    # print results
    result = minion_sequencing_calculator()
    print(result)
