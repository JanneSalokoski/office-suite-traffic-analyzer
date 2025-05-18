# Test-suite for Networking Lab 2025

This is a test suite that can be used to write text into Google Docs and
Microsoft Word documents automatically, simulating human writing speed and
capturing network traffic during the test.

## Usage

### Docs and Word setup
Firstly you must setup both Docs and Word documents with editing rights for
anyone with a link. The links for these will be referred as `<docs-link>` and `<word-link>`.

### Input text
Then you need to acquire some input data. There are pieces of lorem-ipsum
available at `input/`, but you can use whatever text file. The filepath of your
input file will be referred as `<input-file>`.

### Environment variables
There are three environment variables that need to be available inside the
docker container for the tests to run. Set these in `.env` file for docker to
load them automatically:
```env
DOCS_URL=<docs-link>
WORD_URL=<word-link>
INPUT_FILE=<input-file>
```

### Build docker environment
Install docker-compose if you don't have it and then run:
```shell
$ docker compose build
```
This will build the image and that might take a while at the first time. Once
it's done you can do
```shell
$ docker compose up --abort-on-container-exit
```
And your test will run. The text is written at ~80 wpm speed, so if your input
is long, this will take a while. The input is written twice, because there are
two documents.

### Analyzing the results
Each time running the test-suite places capture files at `captures/`. You can
then use **WireShark** or `tshark` to analyze them.


