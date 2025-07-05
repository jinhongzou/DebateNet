import logfire
import os


# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
if os.getenv('LOGFILE_API_KEY')=='':
    logfire.configure()
else:
    logfire.configure(send_to_logfire='test', token=os.getenv('LOGFILE_API_KEY', 'sk-xxx') )
    logfire.instrument_pydantic_ai()
