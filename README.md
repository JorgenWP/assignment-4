# OpenID Authentication
This is a simple flask app that demonstrates how to use OpenID authentication. The app also demonstrates how to deploy it using docker and how to make use of certificates to enable HTTPS encryption.

## How to run
It is possible to both run the app directly using python or using docker. 

### Running the app using python

1. Set up a python virtual environment and activate it
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the flask app
    ```bash
    flask run --debug --host=localhost --port=5000
    ```

### Running the app using docker

1. Build the docker image
    ```bash
    docker build -t <docker-image-name> .
    ```

2. Run the docker container
    > **Note:** This approach will result in an error due to the [dockerfile](dockerfile) configuration. The error is due to the fact that the app is trying to use HTTPS and the certificates are not present in the container. To fix this, you can either remove the HTTPS configuration from the dockerfile or add the certificates before staring the container.
    ```bash
    docker run -p 5000:80 <docker-image-name>
    ```

#### Removing the HTTPS configuration from the dockerfile
To remove the HTTPS configuration from the dockerfile, you can simply edit the last line of the [dockerfile](dockerfile) from this:
```dockerfile
CMD ["flask", "run", "--port", "443", "--cert", "/etc/letsencrypt/live/jpe130.x310.net/fullchain.pem", "--key", "/etc/letsencrypt/live/jpe130.x310.net/privkey.pem"]
```

Into this:
```dockerfile
CMD ["flask", "run", "--port", "80"]
```