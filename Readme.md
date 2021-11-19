## Project Structure 

We decide to migrate the current app toward Azure for :
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

For that we have decoupled the Azure function with App service for reducing error due to http timeout. Decied to go for PostgreSQL database backup to an Azure Postgres database instance and web app to an Azure App Service for high-performance horizontal scaling and maintenance service cost.

## Cost Analysis

The cost for each resources that we have used for developing this project are :

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* | Basic    |   35* |
| *Azure Service Bus*   | Basic  | 0.01              |
|  *Azure App Service* |   F1      |  Free            |
| *Azure Function* | Basic | Free |
| *Azure Sass (SendGrid)* | Basic | Free |

*29,054/month for 1 vCore and 6 dollars for 50GB. For detail click [here](https://azure.microsoft.com/fr-fr/pricing/details/postgresql/server/)

My total cost of this project for 5 days was 4.32 euros. [More Info](screenshots/cost.jpg)

If we had this app in real case production level environment,
The cost for each resources would have been :

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* | General Use (4 vCore, 20 memory, 200 GB)    |   324,2 [more info](https://azure.microsoft.com/fr-fr/pricing/details/postgresql/server/) |
| *Azure Service Bus*   | Standard  | 9,92              |
|  *Azure App Service* |   S2      | 146 [more info](https://azure.microsoft.com/fr-fr/pricing/calculator/?service=service-bus)            |
| *Azure Function* | Premium | 150 [more info](https://azure.microsoft.com/fr-fr/pricing/details/functions/)|
| *Azure Sass (SendGrid)* | Essential | 14,95 [more info](https://sendgrid.com/pricing/) |

