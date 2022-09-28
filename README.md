# email-service
> A service that enables a user to register with a name and email address then confirm their email address.

<p align="center">
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/feature-development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/development-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/staging-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/release-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://github.com/twyle/user-management-service/actions/workflows/production-workflow.yml/badge.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/security-bandit-yellow.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Made%20with- Python-1f425f.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Medium-12100E?style=flat&logo=medium&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=flat&logo=visual-studio-code&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
  <img title="Bandit badge" alt="Bandit badge" src="https://img.shields.io/badge/gunicorn-%298729.svg?style=flat&logo=gunicorn&logoColor=white" />
</p>

![](assets/images/email_service.png)

## Project Overview
This is a simple web application that makes the sending of account confirmation email easier. A user registers with their name and email address. They then have to click on the link sent to their email address to activate their account.

## Working 

To use it, you need an email provider such as Google or Amazon SES. Then:

 1. Register for an account using the auth/register route (provide a username and email address)
 2. Send a confirmation email using the send email route (provide your user id and email)
 3. Confirm your email address (paste the activation token through the confirm route or click on the link in your email).
 4. Your account is then activated.

 <p align=center>
  <img src="assets/videos/email-service.gif" />
</p>

 ## Features

This application has several features including:

1. Deployed to an AWS EBS.
2. Versioned using git and Hosted on GitHub.
3. Auto-deployed to AWS EBS using Github actions.
4. Uses gunicorn as the application servers.
5. Uses an Application Load Balancer to redirect traffic to the frontend
6. Uses AWS SES to send confirmation emails.

## Local Setup

Here is how to set up the application locally:

  1. Clone the application repo:</br>

      ```sh
      git clone https://github.com/twyle/email-service.git
      ```

  2. Navigate into the cloned repo:

      ```sh
      cd email-service
      ```

  3. Create a Virtual environment:

      ```sh
      python3 -m venv venv
      ```

  4. Activate the virtual environmnet:

      ```sh
      source venv/bin/activate
      ```

  5. Install the project dependancies:

      ```sh
      pip install --upgrade pip # update the package manager
      pip install -r requirements.txt  
      ```

  6. Create the environment variables for each service:

      ```sh
      touch .env
      ```

      Then paste the following into the file:

      ```sh

        FLASK_APP=manage.py
        FLASK_DEBUG=True
        FLASK_ENV=development

        POSTGRES_HOST=db
        POSTGRES_DB=email-service
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle

        MAIL_USERNAME=<mail-username>
        MAIL_PASSWORD=<mail-password>
        MAIL_SERVER=<mail-server>
        MAIL_PORT=465
        MAIL_USE_SSL=True

        CELERY_RESULT_BACKEND=redis://redis:6379/0
        CELERY_BROKER_URL=redis://redis:6379/0

        SERVER_NAME=localhost:5000
        PREFERRED_URL_SCHEME=http

      ```
      Then create the database secrets:

      ```sh
      cd database
      touch .env
      ```

      Then paste the following into the file:
      ```sh
      POSTGRES_HOST=localhost
      POSTGRES_USER=lyle
      POSTGRES_PASSWORD=lyle
      POSTGRES_DB=email-service    
      ```  

  7. Start the services:

      ```sh
      docker-compose -f docker-compose-dev.yml up --build
      ```

  8. Create the database:

      ```sh
      docker-compose -f docker-compose-dev.yml exec email-service python manage.py create_db
      ```

  9. View the running application

      Head over to http://0.0.0.0:5000/apidocs 

## Development

 #### 1. Application Design

  1. **Services**

      The application consists of one service that send account activation emails to users:

      1. Email Service 

      ![](assets/images/email_service.png)
        
        This service is resposible for sending account activation emails. The routes include:

        | Route                   | Method  | Description                 |
        | ------------------------| ------- |---------------------------- |
        | 'api/v1/email/send'     | POST    | Send confirmation email.    |
        | 'api/v1/auth/confirm'   | GET     | Activate account.           |
        | 'api/v1/auth/register'  | POST    | Register for a ccount.      |
        
        1. Register as a new user with a unique email address and password as well as name.(Generates a uniques token) 
        2. Proceed to your email address and click on the link given within 24 hours to activate your account. (marks account as activated)
        3. Log into your account using your email and password. (You get a unique token for authorization)

        This service uses the Postgres Database to store the user info. It uses AWS SES to send emails using celery.

 #### 2. Project Management

   1. **Coding standards** </br>

      The application had to adhere to the following coding standards:
      1. Variable names
      2. Function names
      3. Test driven development
      4. Individual modules need 60% coverage and an overall coverage of 60%.
      5. CI/CD pipeline has to pass before deployments.
      6. Commit messages format has to be adhered to.
      7. Only push code to github using development branches.
      8. Releases have to be tagged.
      9. Use pre-commit to run code quality checks
      10. Use comitizen to format commit messages

   2. **Application development process management** </br>

      The project uses GitHub Projects for management.

 #### 3. Development Workflow

 The application uses atleast 5 branches:

  1. Features branch used to develop new features.
  2. Development branch used to hold the most upto date features that are yet to be deployed.
  3. Staging branch holds the code that is currently being tested for production.
  4. The release branch holds all the assets used when creating a release.
  5. The production branch holds the code for the currently deployed application.

The development workflow follows the following steps:

  1. A feature branch is created for the development of a new feature.
  2. The code is then pushed to GitHub, triggering the feature-development-workflow.yml workflow. If all the tests pass, the feature is reviewde and merged into the development branch.
  3. The code in the development branch is then deployed to the development environment. If the deployment is succesful, the development branch is merged into the staging branch.
  4. This triggers the staging workflow. If all the tests are succesful, this branch is reviewed and deployed to a staging environment.
  5. For creatinga release, the staging branch is merged into the release branch. This happens when a tag is pushed to GitHub.
  6. Once a release is created, the release branch is merged into the production branch, which is deployed into production.

The workflows require a couple of secrets to work:

      ```sh
        FLASK_APP=manage.py
        FLASK_DEBUG=True
        FLASK_ENV=development

        POSTGRES_HOST=db
        POSTGRES_DB=email-service
        POSTGRES_PORT=5432
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=lyle

        MAIL_USERNAME=<mail-username>
        MAIL_PASSWORD=<mail-password>
        MAIL_SERVER=<mail-server>
        MAIL_PORT=465
        MAIL_USE_SSL=True

        CELERY_RESULT_BACKEND=redis://redis:6379/0
        CELERY_BROKER_URL=redis://redis:6379/0

        SERVER_NAME=localhost:5000
        PREFERRED_URL_SCHEME=http

      ```

The workflows also require the followingenvironments to work:

  1. Test
  2. Staging
  3. Development
  4. Production

And within each environment, create a secret that indicates the environment type i.e

  1. Test -> ```FLASK_ENV=test```
  2. Staging -> ```FLASK_ENV=stage```
  3. Development -> ```FLASK_ENV=development```
  4. Production -> ```FLASK_ENV=production```

  ## Contribution

1. Fork it https://github.com/twyle/email-service/fork
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Developer

Lyle Okoth – [@lylethedesigner](https://twitter.com/lylethedesigner) on twitter </br>

[lyle okoth](https://medium.com/@lyle-okoth) on medium </br>

My email is lyceokoth@gmail.com </br>

Here is my [GitHub Profile](https://github.com/twyle/)

You can also find me on [LinkedIN](https://www.linkedin.com/in/lyle-okoth/)

## License

Distributed under the MIT license. See ``LICENSE`` for more information.
