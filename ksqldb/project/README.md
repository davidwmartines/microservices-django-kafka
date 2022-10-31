# ksql project

This directory contains the ksql migration scripts
for creating connectors and streams in ksqldb.

Typlically each microservice would define its own project
containing the ksql connectors and streams private to it's own ksqldb-server instance.

For the purposes of this demo, a single ksqldb-server is used and all
the scripts for each microservice are defined within this single project.