# Statistics Microservice
## Overview
The Statistics Microservice is an aggregated or composite service that simplifies interactions with the job portal's underlying microservices. It provides endpoints for retrieving counts of jobs, users, and applications, adding new recruiters and jobs, and fetching all jobs and applications associated with a specific recruiter. This service streamlines the process of accessing and managing key statistics and functionalities within the job portal ecosystem.

## Features
- Get Total Counts (GET /composite/total_count)
Retrieves the total count of jobs, users, and applications in the system.
- Add Recruiter and Job (POST /composite/add_jobs)
Allows for the simultaneous addition of a new recruiter and a new job listing.
- Get Recruiter's Jobs and Applications (GET /composite/recruiter_jobs)
Fetches all jobs posted by a recruiter and all applications submitted for those jobs.