# Technology Justification and Back-of-the-Envelope Calculation

## Chosen Technologies and Justifications

| Technology   | Justification                                                                                                            |
|--------------|--------------------------------------------------------------------------------------------------------------------------|
| **FastAPI**  | - High-performance, asynchronous Python framework ideal for real-time APIs and high-concurrency applications.            |
|              | - Built-in support for OAuth2/JWT enables secure authentication and authorization.                                       |
|              | - Automatic data validation and interactive API documentation streamline development.                                    |
|              |                                                                                                                          |
| **MySQL**    | - Widely used relational database, simple to administer and offering strong ACID compliance for reliable data integrity. |
|              | - While horizontal scaling is challenging, our service requirements do not demand such scale.                            |
|              | - Delivers fast and efficient performance for complex queries.                                                           |
|              |                                                                                                                          |
|              |                                                                                                                          |
| **Redis**    | - In-memory data store (with optional persistence), ideal for caching and real-time leaderboard or score updates.        |
|              | - Supports a variety of data structures.                                                                                 |
|              | - Horizontal scaling via clustering ensures high throughput and availability.                                            |
|              |                                                                                                                          |
|              |                                                                                                                          |
| **RabbitMQ** | - Reliable message broker that supports asynchronous communication and service decoupling.                               |
|              | - Handles multiple consumers efficiently and provides strong message durability.                                         |


---

## Assumptions for Back-of-the-Envelope Calculation

- Assumming each user submits 1 answer every 5 seconds and the following system component capacities estimation: 
- **FastAPI** can handle ~1000 concurrent requests per worker.  
- System has **4 FastAPI workers** → total 4000 requests/sec capacity.  
- **Redis** can handle ~100,000 operations per second.  
- **RabbitMQ** can handle ~50,000 messages per second.  
- **MySQL** can handle ~10,000 writes per second.  


The maximum number of users each component can handle is calculated as:
$$
\text{Max users} = \frac{\text{Component Capacity (ops/sec)}}{\text{Requests per user per second}}
$$

| Component    | Capacity (ops/sec) | Max Users Supported |
|--------------|--------------------|--------------------|
| FastAPI      | 4,000              | 20,000             |
| Redis        | 100,000            | 500,000            |
| RabbitMQ     | 50,000             | 250,000            |
| MySQL        | 10,000             | 50,000             |

**Calculation results:**
- **FastAPI:** 4,000 / 0.2 = 20,000 users
- **Redis:** 100,000 / 0.2 = 500,000 users
- **RabbitMQ:** 50,000 / 0.2 = 250,000 users
- **MySQL:** 10,000 / 0.2 = 50,000 users


**Max supported users = minimum of all components = 20,000 users**

---

