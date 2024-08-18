# Genetic_algorithm
Network Design Case Study

We have a new airline that wish to operate out of south Indian cities/locations in four states viz., Andhra Pradesh, Kerala, Karnataka and Tamil Nadu. The airline plans to operate its fleet with two types of aircraft viz., 170-and 300-seater aircraft. The locations chosen are state capitals and 5 other major airports in these 4 states which are Cochin, Mangalore, Trichy, Coimbatore, and Vijayawada.

The daily demand for travel between any two state capitals is about 1200 passengers in both directions while between a city in a state and its state capital is about 450 passengers in either direction. The daily demand between Coimbatore and Trichy (as well as otherwise) is about 300 passengers per day. Only flights are operated between state capitals and not between other cities across states.

Kindly design an airline operational network with frequencies of flights between all possible pairs of locations you wish to operate. If you were given a choice between point-to-point operation or hub and spoke operation, for selection of network design which one would you choose. In hub and spoke operations, the airline must bring back all the flights to its hub location. If so, how many hubs would you wish to select in case you recommend hub and spoke model.
Note: You can assume a travel time of 1 hr between any two locations for distance more than 400 kms and otherwise it may be 30 min. The flight turnaround time is 30 mins for smaller aircraft and 45 mins for larger aircraft.

Above can be solved using Genetic algorithm
Create possible solutions(chromosomes)
Create population
define fitness function
define mutation and cross over function
check fitness and iterate this over generations
