# ksqldb project

This directory contains the ksql migration scripts
for creating connectors, streams, and tables in ksqldb.

Typically each microservice would define its own project
containing the ksql migrations for its own private ksqldb-server instance.

For the purposes of this demo, a single ksqldb-server is used and all
the scripts for each microservice are defined within this single project.