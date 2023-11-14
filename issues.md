## Websocket Issues
<hr class="close">

#### SocketIO does not accept "/" as a connected namespace

- Reason: The websocket has to send too many sockets in a short period of time.
- Fix (Temporary):
  - Change the Judging Method (Judging Function). From line-by-line to default judger.

## Judges Issues
<hr class="close">

#### The first test-case sometimes consumes a huge amount of time to compile, run and let the judge communicate with

- The first test-case is the first interaction with the Processor, so it can't avoid taking a seriously enormous amount of time to communicate with the judge and ProcessID. Can't do anything tho.
- Fix (Approved):
  - Add an additional (optional) setting, which is `SAFE_FIRST_START_AFTER_COMPILING`. The judge would take the first test-case, run and communicate with the prompt without saving any information (just compile and run to start the execution of the child-processor).