# Ortelius XRPL Architecture and Design

## Current Architecture - January 2023

### Monolith + Microservices = Hybrid

- Monolith
  - Backend is written in Java and JSP and runs on Tomcat/Jetty app server in a docker container.
    The main goal of the backend is to handle http requests from the JavaScript running
    in the browser and from the Ortelius CLI.  A small set of "Rest APIs" have been exposed
    for public access to the data in the Postgres database.
  - JavaScript and JQuery for the frontend client, browser UI.  The JavaScript and static files
    are served up using JSP that runs on a second Tomcat/Jetty app server in a docker container.
    The JavaScript and JSPs are responsible for the UI in the browser.  Additional JS Packages
    such as [vis.js](https://visjs.org/) and [datatables.net](https://datatables.net/), are used for the dependency graphs and list tables.

- Microservices
  - Python FastAPI programs that expose RestAPI endpoint for a specific task. These microservices use SqlAlchemy to connect to the Postgres DB
    and perform SQL queries.

  - Current Microservices:
    - **ms-validate-user:** Checks to see if the current transaction has a validate user associated with it, i.e. logged in user.  This services receives a cookie with the JWT token produced by the login.  The JWT token is used to determine if the user is logged in or not.

    - **ms-compitem-crud:** Creates/Retrieves/Updates/Deletes the component detail data for a component version.

    - **ms-depkg-cud:** Handles the upload of the SBOM (Spdx or Cyclone) file for a component version.

    - **ms-deppkg-r:** Retrieves the SBOM for a component version.

    - **ms-textfile-crud:** Creates/Retrieves/Updates/Deletes the readme and license files for a component version.

    - **ms-scorecard:** Creates a scorecard web page showing the compliance scorecard for component versions and application versions.

- Database
  - Postgres DB is used for all data.  Both the Monolith and Microservices read/write to the database over JDBC and PyODBC respectively.

[Existing Architecture Diagram](existingarch.md)

## New Architecture


### Functional Requirements

Ortelius must enable end users to gather data from their CD/CI pipeline and non-derived data, such as Service Owner, and persist that data for data analytics. The analytics comprises dependency relationships navigation, version history, verification services, and vulnerability exposure.

Data persisted and analyzed (not limited to this list):

- Application Version
- Component Version
- Dependency Packages (SBOMs)
- License File
- Readme File
- OWNERS file
- MAINTAINERS file
- Governance Doc
- Contributor Doc
- Contact
- Git Repo 2FA
- Git Repo Location
- Git Repo Branch
- Git Repo Commit
- Git Commit Signing
- Git Commit Signature
- Git Line Added/Deleted
- Git Commit Date
- Repo Scan
- Dependabot
- Automated Build
- Build SBOM Generation
- Post Build SBOM Generation
- Image Signing
- Provenance
- Attestation
- Component Version Creation
- Component Aggregation (Logical Application)

### Non-Functional Requirements - How it Works

The Web front-end is where the end user will interact to persist and consume the data stored in the back-end databases. The user can create, retrieve, and update the data using the front end. However, deleting data is impossible since the blockchain ledger keeps all transactions. Therefore, the end user will use an Archived Tag to delete data, which hides the old data.

The front end will send data to the NGINX reverse proxy using HTTPS with a JSON payload. The NGINX reverse proxy will route the transaction to the appropriate back-end microservice based on the end-point URL.   The microservice then normalizes the JSON to prevent redundant data from being stored in the database. Next, the microservice calls the database abstraction handler Python function to persist the data in Arango, NFT Storage, and XRPL. Finally, a Push-Through Cache is used to handle the slowness of NFT Storage and provide fast responses back to the end user. See [Transaction Flow](#transaction-flow) for further details.

The Ortelius CLI is where end users will hook in Ortelius into the CI/CD pipeline. The Ortelius CLI is used to persist data from the pipeline into the Ortelius database. The CLI uses the same steps as the front end for persisting data.

The front end will send the request over HTTPS with appropriate parameters to the NGINX reverse proxy for retrieving data. The NGINX reverse proxy will route the transaction to the appropriate
back-end microservice based on the end-point URL. Next, the microservice calls the database abstraction handler Python function to find the data in the Arango Cache. If the data is not found, the database abstraction handler will pull it from NFT Storage and XRPL, return it, and add it to the cache.

The database abstraction handler Python function encapsulates the database interaction enabling the replacement of XRPL and NFT Storage for an OCI-based registry.  The Arango database for searching and caching remains in place.


### Technical Decisions

1. Why switch from Postgres to a graph database?
  Postgres, being a relational database, does not handle dependency relationships in an easy manner.  The database schema becomes very complicated.  A graph database does this natively allowing for a simpler database schema.

2. Why not store the denormalized JSON in a database?
  Denormalized data, especially SBOMs, are mostly redundant data.  For example, multiple packages use the Apache license.  Normalizing the JSON enables storing of the redundant data once and then have that one copy referenced multiple times.

3. Why ArangoDB for the graph database?
  ArangoDB natively stores JSON documents as a document store and enables graph dependencies without requiring formal object schemas. Looking at other graph databases, we found that pre-defined schemas are needed, resulting in too much overhead.

4. Why use blockchain when a database will do fine?
  The XRP Ledger blockchain provides a decentralized network that eliminates a single point of failure.  Secondly, it gives an immutable history of the transactions, in our case, versioning.  Also, XRPL is based on "Proof of Consensus" which is very low cost to preform since the current state is known to each block.  The state knowledge eliminates the need to traverse the whole blockchain to perform a new transaction.

5. Why use NFT Storage?
  The NFT Storage is a first-class object in XRPL that provides direct access from XRPL to NFT Storage without requiring extra coding steps.  Also, the NFT Storage is cheap for long-term data persistence, ~$4/TB/month, compared to AWS S3 at ~$20/TB/month.

### Components

- Monolith
  - Retire Monolith and replace with new microservices and new frontend framework, such as https://kit.svelte.dev/ or https://riot.js.org/.

- Microservices
  - Migrate needed RestAPIs from the monolith to Python FastAPI or NodeJS microservices as appropriate.
  - New RestAPIs with an abstract layer for the database.
  - Microservice for serving up frontend framework and static content.

- Database

  - XRPL
    The database will be migrated to `nft.storage` (IPFS) for storing of objects as JSON.  Since IPFS does not have built in search capabilities a searchable cache will be created in ArangoDB.  ArangoDB will also act as a cache for denormalized JSON objects.  The idea is to have the search cache based on indexes that are needed by the RestAPIs.  The matching search results are then added to the ArangoDB as denormalized JSON for easy document retrieval.  The ArangoDB is an ephemeral database and can be recreated from objects stored in IPFS and the XRP Ledger.

    > ArangoDB is flexible to handle any type of JSON without the need to provide a schema.  Indexes and graph connections maybe needed for performance.

  - OCI Registry
    OCI Registry will be another database we can use when Redhat extends the OCI Registry 1.1 Specification to handle additional schemas.  The OCI Registry should be treated similar to the `nft.storage` in which an ArangoDB searchable cache is maintained and also stores the denormalized JSON objects.  The ArangoDB is an ephemeral database and can be recreated from the OCI registry.

  - Abstraction Layer for IPFS and OCI
    In order to keep the microservices small, two sets of services should be created.  One for retrieving/storing to IPFS and another for OCI.  Both types of database services should return the same result providing an abstraction layer to the data consumers.

  - Interim Postgres DB
    Postgres may still be needed to persist data that is outside of the scope for XRPL and OCI.  Items such as users, groups, access control and domain may initial still reside in Postgres until a full data migration is completed.

#### Rest APIs

| Microservice          | Create  | Retrieve | Update | Delete  | List  | Description |
| ------------          | ------  | -------- | ------ | ------  | ----  | ----------- |
| ms-app-tag            | X       |  X       | X      | X       | X     | Handle tags for an application version |
| ms-appver             | X       |  X       | X      | X       | X     | Handle base application and application versions |
| ms-comp-tag           | X       |  X       | X      | X       | X     | Handle tags for an component version |
| ms-compver            | X       |  X       | X      | X       | X     | Handle base component and component versions |
| ms-vulnerability      | X       |          | X      | X       |       | Handle saving CVEs from osv.dev |
| ms-deployment         | X       |  X       | X      | X       | X     | Handle deployment |
| ms-deppkg             | X       |          | X      | X       |       | Handle saving the SBOM for a component version |
| ms-domain             | X       |  X       | X      | X       |       | Handle domain |
| ms-environment        | X       |  X       | X      | X       |       | Handle environment |
| ms-group              | X       |  X       | X      | X       |       | Handle group |
| ms-scorecard          |         |  X       |        |         | X     | Handle scorecard for Application and Components |
| ms-textfile           | X       |  X       | X      | X       |       | Handle readme and license for a component version |
| ms-user               | X       |  X       | X      | X       |       | Handle user |
| ms-usergroup          | X       |          | X      | X       |       | Assign user to a group |
| ms-validate-provenance|         |  X       |        |         |       | Validate the provenance for a package |
| ms-validate-signing   |         |  X       |        |         |       | Validate the signature for a package |
| ms-validate-user      |         |  X       |        |         |       | Validate the JWT cookie for a user |


[New Architecture Diagram](newarch.md)

#### Object Definitions

See the class definitions in [Ortelius Commons Python Module](https://github.com/ortelius/ortelius-commons/blob/main/ortelius_common.py)

#### Persisting Data

In order to persist redundant data only once, we must normalize it and then reference the normalized data.

For example, the denormalized json:

```json
  {
    "Domain": {
      "_key": 1,
      "name": "GLOBAL"
    }
  },
  {
    "User": {
      "_key": 1,
      "name": "admin",
      "domain": {
        "_key": 1,
        "name": "GLOBAL"
      },
      "email": "admin@ortelius.io",
      "phone": "505-444-5566",
      "realname": "Ortelius Admin"
    }
```

gets transposed into its normalized json format:

```json
  {
    "0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8": {
      "_type": "domain",
      "name": "GLOBAL"
    },
    "42e4b2274ee658dd0bf1f83a278a273e9191c08d": {
      "_type": "user",
      "domain": "0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8",
      "email": "admin@ortelius.io",
      "name": "admin",
      "phone": "505-444-5566",
      "realname": "Ortelius Admin"
    }
  }
```

In order to distinguish the normalized objects from one another, we add the _type field.  The key for the object, i.e. `0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8`
is the SHA256/IPFS CID for the data in the object.

> Note: The keys in the object should be sorted prior to calculating the SHA256/CID. This is done to ensure that different
programming languages (Nodejs vs Python) are handling the data in the exact same ways.  Different ordering of the keys will
cause different SHAs to be calculated.

##### Storing on nft.storage

The normalized data can be stored directly on nft.storage.  We need to ensure the key being created is identical to the IPFS CID.

Using the IPFS CID as the key will enable the easy storage and retrieval from ntf.storage while minimizing duplication of data in IPFS.

##### Storing on ArangoDB

The normalized data is transformed slightly for storing in ArangoDB.  ArangoDB uses a _key field in the object for the index.  ArangoDB can
generate a _key for us or you can supply one.  In our case, we will supply the _key as the SHA256/IPFS CID.   The object transformation for
ArangoDB is as follows:

nft.storage object

```json
    "0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8": {
      "_type": "domain",
      "name": "GLOBAL"
    }
```

is transposed for ArangoDB to

```json
    {
      "_key": "0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8",
      "_type": "domain",
      "name": "GLOBAL"
    }
```

> Note: Removing the key from the ArangoDB object will enable the SHA256/IPFS CID calculation to return the correct value, i.e. the _key value.

#### ArangoDB as a push through cache

nft.storage and IPFS objects (NFTs) do not have any search capabilities.  You can only find objects based on their CID.  Loading all of the NFTs into
ArangoDB is too much data, terra-bytes worth.  Instead, ArangoDB will contain a sparse view of nft.storage.  This sparse data will enable searching
based on common fields, i.e. Domain Name, Object Type, and Object Name.  The returned data from the search will include cached and un-cached objects.

The microservice doing the database retrieval will loop through the search results pulling together the denormalized version of the object requested.
When it comes across an un-cached version it will use the CID supplied, retrieve the object and add it to ArangoDB as a cached object.  The existence of the `cache` field is used to distinguish between cached and un-cached objects.

un-cached User

```json
     {
      "_key": "42e4b2274ee658dd0bf1f83a278a273e9191c08d",
      "_type": "user",
      "domain": "GLOBAL",
      "name": "admin",
      "cached": "false"
    }
```

cached User

```json
     {
      "_key": "42e4b2274ee658dd0bf1f83a278a273e9191c08d",
      "_type": "user",
      "domain": {
        "_key": "0ca02cc4cf8fbb3e3b2b29af3e7495f9b0f78bb8",
        "_type": "domain",
        "name": "GLOBAL"
      },
      "email": "admin@ortelius.io",
      "name": "admin",
      "phone": "505-444-5566",
      "realname": "Ortelius Admin"
    }
```

> Note: ArangoDB enable you to update an object and replace or merge the contents based on the _key and update options.


#### Transaction Flow

Since nft.storage is slow, a push through cache will be utilized for storing the data.  This means that the cache will be updated first so read transactions can access the data while it is being persisted to long term storage in nft.storage.  The microservices will using the following
transaction flows:

[Write Transaction Flow](writecache.md)

[Read Tranaction Flow](readcache.md)


#### Example Schemas for all classes

##### Denormalized

[All Denormalized Objects](denormalized.json) based on classes in [ortelius-commons](https://github.com/ortelius/ortelius-commons/blob/main/ortelius_common.py)
