# QwiKart ~ Just In Time Store 

QwiKart is an innovative e-commerce platform designed to provide an exceptional shopping experience with an emphasis on achieving a ~ 98% Fulfillment Rate. The platform leverages cutting-edge Python and API-based systems to ensure real-time inventory management, seamless order processing, and timely delivery. At the heart of QwiKart’s philosophy is the concept of “Just-in-Time” fulfillment — providing customers with exactly what they need, when they need it, without any delays or overstocking.

## **Vision & Mission**

**Vision:**

To revolutionize the retail experience by offering customers seamless, on-demand access to the products they need, with zero compromise on availability or delivery speed.

**Mission:**

Achieve a ~ **98% fulfillment rate** by combining advanced technologies and streamlined operational strategies. Deliver products to customers on time, every time, using an API-based system designed for efficiency and scalability.

## **Key Strategies**

1. **Real-Time Inventory Management**
    
    QwiKart’s backend operates on a **dynamic inventory management system** that ensures products are updated in real time. This allows for the most accurate product availability data, reducing out-of-stock situations and overstocking.
    
2. **Advanced API Integration**
    
    Leveraging Python and robust APIs, QwiKart integrates with suppliers, warehouses, and shipping providers to synchronize stock levels and order statuses in real-time. This connectivity drives accuracy and efficiency in the fulfillment process.
    
3. **Demand Forecasting**
    
    By analyzing purchase patterns and market trends, QwiKart implements advanced predictive algorithms that forecast demand at a granular level. This enables QwiKart to prepare stock levels and fulfill customer orders precisely when needed.
    
4. **Just-in-Time Fulfillment**
    
    QwiKart eliminates excess inventory, reducing waste and ensuring that products are available only when necessary. This "Just-in-Time" system reduces storage costs and ensures that customers receive products at the right time, without delay.
    
5. **Seamless User Experience**
    
    The website and mobile platforms are built with a focus on simplicity and usability. The intuitive UI/UX design makes it easy for customers to browse, order, and track their purchases with minimal friction.
    

---

## **Key Differentiators**

1. **~ 98% Fulfillment Rate**
    
    The core differentiator of QwiKart is its **unmatched fulfillment rate**. Unlike many other e-commerce platforms that may suffer from out-of-stock items or delayed deliveries, QwiKart’s integration with real-time systems ensures that every order is fulfilled on time.
    
2. **Python & API-Based Architecture**
    
    Most e-commerce platforms rely on outdated, monolithic systems. QwiKart utilizes modern **Python-based frameworks** and **API-first architecture** to ensure agility, scalability, and flexibility in meeting customer needs.
    
3. **Zero Overstocking**
    
    The use of **Just-in-Time fulfillment** eliminates the problem of overstocking and unsold inventory, helping to create a leaner and more cost-efficient supply chain. This approach not only reduces waste but also passes on cost savings to the customer.
    
4. **Dynamic Product Availability**
    
    Unlike traditional stores that rely on fixed inventory data, QwiKart’s real-time product availability system is constantly updated via APIs from suppliers and warehouses. Customers get a transparent view of exactly what’s in stock.
    
5. **Predictive Supply Chain Optimization**
    
    The system uses **advanced machine learning algorithms** to forecast demand with high accuracy. This predictive capability ensures that products are always available based on demand patterns, reducing both overstocking and stockouts.
    
6. **Frictionless Checkout & Delivery**
    
    With a streamlined checkout process and seamless integration with delivery partners, QwiKart ensures that the customer journey from browsing to delivery is smooth and quick.
    
7. **Scalability & Flexibility**
    
    Thanks to its API-based architecture and Python backend, QwiKart can easily scale with growing demand, add new product categories, integrate additional suppliers, and support new delivery methods.
    

---

## **How It Works**

1. **Browse & Order**
    
    Customers browse products via an intuitive interface, choosing from a wide range of categories. Each product page displays real-time stock levels and estimated delivery times based on location.
    
2. **Real-Time API Synchronization**
    
    Once an order is placed, the platform connects with suppliers and warehouses through APIs to confirm product availability and shipping details. Inventory levels are updated in real time.
    
3. **Just-in-Time Fulfillment**
    
    Products are picked and packed only when an order is confirmed, reducing the storage time of inventory. This ensures freshness and eliminates overstock.
    
4. **Delivery**
    
    Using dynamic shipping algorithms, QwiKart selects the fastest and most cost-effective delivery option to ensure timely arrival, based on customer location.
    
5. **Post-Purchase Support**
    
    Customers receive real-time tracking information and updates, ensuring a transparent and reliable post-purchase experience.

# Tech Stack Used:

Langauge: Python
Packages: FastAPI, pydantic, SQLAlchemy, uvicorn, Psycopg 2
Tools: Postman API, PostgreSQL (pgAdmin4, psql)

# Tech Stack Used:

- ***FastAPI*** is used for easier API development. It is a very high performance API-System and it is on par with Node.js and Go Language. This library helps the developers to use the REST interface for thier applications. The best part of FastAPI is that it can handle creation of databases as well its schemas. It also creates documentation for the API implementation. This is one of the best features of FastAPI.

- ***SQLAlchemy*** is a database toolkit for Python. It is an open-source tool kit and object relational mapper (ORM) for Python programming. SQLAlchemy can be used to automatically load tables from a database using something called reflection. Reflection is the process of reading the database and building the metadata based on that information. The queries written in SQLAlchemy is very much similar to the Normal SQL. The syntax is a little bit different. This blogs explains the entire working of SQLAlchemy. I have used it as a reference. 

***[SQLAlchemy — Python Tutorial - Medium](https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91)***

- PostgreSQL is one fot he most widely used database management tools. PostgreSQL comes under the SQL category but it is a bit different from the Normal SQL Database Management. It uses the concept of Classes and Objects. It combines the advantages of OOPS and SQL together. It comes in very handy when we are dealing with API/RESTFUL Architectures. Also, PostgreSQL provides wide range of supported functionality so that developers can easily make use of libraries to connect the database to the code. For this application, each and every criteria was matching to use PostgreSQL. Hence, I have used PostgreSQL as the database.

***[IBM's Introduction to PostgreSQL](https://www.ibm.com/topics/postgresql)***

- ***uvicorn*** is a ASGI web implementation library in Python. It is a low-level server application interface for async frameworks. Before this library there was no module which catered to this need. We had to create huge code base for creation of interfaces.

***[PyPI Installation of uvicorn](https://pypi.org/project/uvicorn/)***

- ***Psycopg 2*** is a PostgreSQL adapter for Python. It is designed to perform heavily multi-threaded applications that usually create and destroy lots of cursors and make a large number of simultaneous INSERTS or UPDATES. Psycopg features client-side and server-side cursors, asynchronous communication, and notification. Psycopg 2 is both Unicode and Python 3 friendly.

***[Psycopg 2 Geeks For Geeks Introduction](https://www.geeksforgeeks.org/introduction-to-psycopg2-module-in-python/)***

- ***Postman API***, if we have to test the API Architecture, we can make use of Postman API. One of the best and most simple tools available to test API Architectures. It provides features to make new requests, create environmental variables inside the application itself, Bearer Token Authentication etc. These are very crucial when we are creating a REST API architecture.

- ***Pydantic*** is a data-modelling library that has efficient error handling functionalities. Along with that, JSON parsing and validation is provided which makes it a crucial library for this project. 

***[Beginners Guide to Pydantic - Medium](https://betterprogramming.pub/the-beginners-guide-to-pydantic-ba33b26cde89)***
