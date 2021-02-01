# crypto-dom

Modeling of crypto exchanges domains

For each endpoint, we provide the full URL path, URL method, a Request model (to validate query parameters) and a Response model.

<br>

### Basic Usage

```python
from crypto_dom.binance.market_data.klines import Response

# instantiate model
resp_model = Response()

# pass decoded JSON response content to model to validate
# Note: do not unpack as you usually would for pydantic models !
valid_resp = resp_model(data)
```