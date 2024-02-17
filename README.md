# AiChatPoweredEcommerce: Revolutionizing Online Shopping with AI

Welcome to **AiChatPoweredEcommerce**, an innovative project that stands at the intersection of artificial intelligence and e-commerce, designed to enhance the online shopping experience with AI-driven chat support. Developed during a capstone project at Flatiron School, this platform utilizes **Natural Language Processing (NLP)** and **machine learning** techniques to offer personalized, efficient, and enjoyable shopping experiences, powered by **OpenAI**.

## Project Overview

**AiChatPoweredEcommerce** is a pioneering venture that showcases the transformative potential of AI in enhancing e-commerce platforms. By integrating advanced **AI models** with **Flask** for the backend and **React** for the frontend, this project delivers a secure, responsive, and user-centric online shopping environment. Our custom **AI chatbot**, developed with OpenAI's GPT, is designed to provide real-time, context-aware support to shoppers, setting a new standard for customer service in the digital marketplace.

## Technical Stack

- **Frontend Technologies**: Utilizing **React**, our user interface is dynamic, responsive, and tailored for an optimal user experience across all devices. Enhanced with **Tailwind CSS**, the design is both elegant and accessible.
- **Backend Technologies**: **Flask** serves as the backbone of our application, facilitating robust API endpoints, secure user authentication, and seamless data management. Our choice of **Python** for server-side logic underscores our commitment to efficiency and scalability.
- **AI Integration**: At the heart of our chat support system is **OpenAI's ChatGPT**, offering unmatched capabilities in understanding and responding to customer inquiries. This integration ensures that our platform provides personalized and insightful assistance to every user.
- **Database and Security**: With **SQLite** and **PostgreSQL**, our platform guarantees reliable data storage and management. Security is fortified with **bcrypt** for password hashing, alongside rigorous session and cookie management practices.

## Key Features

- **AI-Powered Chat Support**: Elevating customer service with our AI-driven chat system, providing instant support and personalized shopping recommendations.
- **Advanced User Session Management**: Enhancing the user experience with sophisticated session tracking, allowing for seamless conversation continuity and personalized interactions.
- **Secure Online Shopping**: Implementing industry-standard security measures to protect user data and transactions, ensuring a safe and trustworthy shopping environment.

![Collage of AIChatPoweredSite](/client/src/assets/img/chatecommercewebsiteimage.png)

## Future Enhancements

Looking ahead, **AiChatPoweredEcommerce** aims to introduce **multi-language support**, **user reviews and ratings**, and **enhanced product discovery** features. Our commitment to continuous improvement and adoption of cutting-edge technologies will drive further innovations in AI-powered e-commerce solutions.

## Platform Setup Guide

Welcome to the AiChatPoweredEcommerce Platform. This guide will walk you through the steps to clone and set up your development environment for both the backend (Flask) and frontend (React) components of the application. Be sure to use the offline-dev-env branch and not the main. As the main was reconfigured for Production Deployment.

## Directory Structure

```
├── CONTRIBUTING.md
├── LICENSE.md
├── Pipfile
├── README.md
├── client
│   ├── README.md
│   ├── package.json
│   ├── postcss.config.js
│   ├── public
│   ├── src
│   │   ├── App.js
│   │   ├── api
│   │   ├── assets
│   │   │   └── img
│   │   │       ├── VisionXHero.png
│   │   │       ├── vision_x_logo.png
│   │   │       ├── visionxhalo.png
│   │   │       └── visionxphone.png
│   │   ├── components
│   │   │   ├── CartContext.js
│   │   │   ├── CloseAccount.js
│   │   │   ├── Footer.js
│   │   │   ├── Hero.js
│   │   │   ├── InfoSection.js
│   │   │   ├── InfoSection2.js
│   │   │   ├── Login.js
│   │   │   ├── NavbarMenu.js
│   │   │   ├── Products.js
│   │   │   ├── Register.js
│   │   │   ├── ShoppingCart.js
│   │   │   └── UpdatePassword.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── pages
│   │   │   ├── AboutPage.js
│   │   │   ├── AuthPages.js
│   │   │   ├── CheckoutPage.js
│   │   │   ├── ConfirmationPage.js
│   │   │   ├── ContactPage.js
│   │   │   ├── HomePage.js
│   │   │   ├── ProductDetailPage.js
│   │   │   ├── ShoppingCartPage.js
│   │   │   ├── TechSupport.js
│   │   │   └── TechSupport2.js
│   │   └── store
│   │       ├── actions
│   │       │   ├── authActions.js
│   │       │   ├── cartActions.js
│   │       │   ├── chatActions.js
│   │       │   ├── orderActions.js
│   │       │   ├── productActions.js
│   │       │   └── shippingActions.js
│   │       ├── index.js
│   │       └── reducers
│   │           ├── authReducer.js
│   │           ├── cartReducer.js
│   │           ├── chatReducer.js
│   │           ├── messagesReducer.js
│   │           ├── orderReducer.js
│   │           ├── productReducer.js
│   │           └── shippingReducer.js
│   └── tailwind.config.js
├── package-lock.json
├── requirements.txt
└── server
    ├── ai.py
    ├── app.py
    ├── app_utils.py
    ├── config.py
    ├── data
    │   └── support_guide.txt
    ├── migrations
    ├── models.py
    ├── package-lock.json
    ├── package.json
    ├── routes.py
    ├── seed.py
    └── validations
```

## Preparing the Backend Environment (`server/`)
Before initializing the database, ensure you have a `.env` file set up in your `server` directory. This file will store essential environment variables for your Flask application.

### Generating the Secret Key
1. Open a terminal.
2. Generate a new secret key by running the following command:
    ```console
    python -c 'import secrets; print(secrets.token_hex())'
    ```
3. Copy the output; this is your secret key.

### Creating the .env File
1. In your `server` directory, create a file named `.env`.
2. Add the following lines to the `.env` file:
    ```
    SECRET_KEY=<Your Secret Key>
    DB_URI="sqlite:///app.db"
    
    OPENAI_API_KEY=<obtained from https://platform.openai.com/api-keys>
    
    ```
   Replace `<Your Secret Key>` with the key you generated.
   Replace OPENAI API KEY with the key generated on https://platform.openai.com/api-keys . 

### Installing Dependencies
After cloning the project, install backend dependencies and activate the virtual environment:
```console
pipenv install
pipenv shell
```

### Running the Flask API
To run the Flask API locally (default port 5555):
```console
python server/app.py
```

## Preparing the Frontend Environment (`client/`)
The `client/` directory contains the React frontend code.

### Installing React Dependencies
To install frontend dependencies:
```console
npm install --prefix client
```

### Starting the React App
To start the React app locally (default port 3000):
```console
npm start --prefix client
```

## Database Initialization and Seeding
After setting up your `.env` file and installing dependencies, you can initialize and seed your database. Ensure you're in the `server` directory, then run:

```sh
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555

{ flask db init && echo "DB init successful"; } || echo "DB init failed, continuing..."
{ flask db migrate -m "initial migration" && echo "DB migrate successful"; } || echo "DB migrate failed, continuing..."
{ flask db upgrade head && echo "DB upgrade successful"; } || echo "DB upgrade failed, continuing..."
{ python seed.py && echo "Seeding successful"; } || echo "Seeding failed"
```

These commands will initialize the database, perform migrations, upgrade to the latest version, and seed it with initial data. After this you should see it on your http://localhost:3000/ enjoy! ☺️

## Contributing

I welcome contributions from the community. If you wish to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
