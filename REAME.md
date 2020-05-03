## Djelegram

### Yet Another Client for Telegram (YACT)

Djelegram is a web client for Telegram developed using Django on top of robust Telegram APIs.

#### Installation

First thing first, [download the archive](https://drive.google.com/open?id=1a3CHksNLevJLgEsfQZQytFKn98LkOD3x) containing Djelegram's code.To get started with Djelegram you will need to get API_ID and API_HASH from Telegram. They have beautifully mentioned all steps one needs to follow to get required two in their [documentation](https://core.telegram.org/api/obtaining_api_id).

After acquiring your API_ID and API_HASH you can follow these steps to quickly setup Djelegram on your machine.

Create a file named local\_settings.py in djelegram directory. Add following to that file

```
API_ID = <you-api-id>
API_HASH = <yur-api-hash>
```

We recommend using docker-compose to quickly spin up Djelegram for development. You can install Docker from following instructions in [Docker Documentation](https://docs.docker.com/desktop/), and similarly you can install docker-compose from it's [documentation](https://docs.docker.com/compose/install/).

##### Running Using Docker

1. Open up a terminal or power-shell, and change the working directory to the project directory, i.e. djelegram\_webclient.
2. Run following command on terminal
```
    docker-compose up 
```

For the first run, Docker will download the base image for python from Dockerhub and build an image for our project. The first run could take some time depending upon internet connectivity. Subsequent builds will be a lot faster since Docker caches intermediate steps.

After building our image, the following message will appear on the terminal depeicting that our website is available to surf on localhost.

```
app_1 | Django version 3.0.5, using settings 'djelegram.settings'
app_1 | Starting development server at http://0.0.0.0:8000/
app_1 | Quit the server **with** CONTROL-C.

```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000/) to checkout Djelegram, voila you can now chat on Djelegram.

##### Pythonic Installation

If you don't want to install Docker just for running this project, you can still install Djelegram like any other Django project. These commands will help you set up Djelegram on you machine.

1. Install Python, you find instructions at [Python's documentation](https://www.python.org/downloads/).
2. Open up a terminal or power-shell and change it's working directory to the project directory, i.e. djelegram_webclient.
3. Create a Python virtual environment
```
    python3 -m venv venv/
```

4. Activate this virtual environment
```
   source venv/bin/action #Linux
   <venv>\Scripts\Activate.ps1 #PowerShell 
```

5. Install project dependencies with pip
```
    pip install -r requirements.txt 
```

Note: This step might fail due to dependencies error, you will require to install corresponding C library according to your operating system, This is why we suggest using Docker instead. If you are on Linux, you might need the gcc package. (not exhaustive)

1. Start Django development server using
```\
    python manage.py runserver
```

You should expect an output like this

```
Django version 3.0.5, using settings 'djelegram.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server **with** CONTROL-C. 
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000/) to checkout Djelegram, voila you can now chat on Djelegram.

#### Using Djelegram

Using Djelegram is fairly straightforward, you can read about Djelegream at the [home page](http://127.0.0.1:8000/). You can [login](http://127.0.0.1:8000/login) into your Telegram account using you registered mobile number and authentication code, which you will receive on your Telegram account or SMS. After a successful login, you will be redirected to a chat webpage. Logging out is as simple as pressing the [logout](http://127.0.0.1:8000/logout) button on navigation bar,

#### Important Links

- Home Page : [http://127.0.0.1/](http://127.0.0.1/)
- Login :[http://127.0.0.1/login](http://127.0.0.1/login)
- Logout : [http://127.0.0.1/logout](http://127.0.0.1/logout)
- Chat : [http://127.0.0.1/chat](http://127.0.0.1/chat)