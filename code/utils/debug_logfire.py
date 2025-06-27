import logfire
# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='test', token='pylf_v1_us_bf1ZYDy0pFrLVvDFmTHDxFvsS53bRY1VdTzXKfN2dSR8')
logfire.instrument_pydantic_ai()

#logfire.info('found {flight_count} flights', flight_count=len(result.output))
