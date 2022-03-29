import requests
import datetime


def _request(method, endpoint, **kwargs):
    base_api = "https://api.upbit.com/v1/{endpoint}"
    endpoint = base_api.format(endpoint=endpoint)

    try:
        response = method(endpoint,
                          data=kwargs.get('data', None),
                          params=kwargs.get('params', {}),
                          headers=kwargs.get('headers', None))

        data = response.json()

        if type(data) == dict and data.get('error'):
            return {
                'ok': False,
                'description': data.get('error', {}).get('message', 'Unknown Error')
            }

        return {
            'ok': True,
            'data': data
        }

    except requests.exceptions.ConnectionError:
        return {
            'ok': False,
            'description': 'Connection Error'
        }
    except Exception as e:
        return {
            'ok': False,
            'description': str(e),
        }


def _get_endpoint_ohlcv(interval):
    if interval in ["day", "days"]:
        endpoint = "candles/days"
    elif interval in ["minute1", "minutes1"]:
        endpoint = "candles/minutes/1"
    elif interval in ["minute3", "minutes3"]:
        endpoint = "candles/minutes/3"
    elif interval in ["minute5", "minutes5"]:
        endpoint = "candles/minutes/5"
    elif interval in ["minute10", "minutes10"]:
        endpoint = "candles/minutes/10"
    elif interval in ["minute15", "minutes15"]:
        endpoint = "candles/minutes/15"
    elif interval in ["minute30", "minutes30"]:
        endpoint = "candles/minutes/30"
    elif interval in ["minute60", "minutes60"]:
        endpoint = "candles/minutes/60"
    elif interval in ["minute240", "minutes240"]:
        endpoint = "candles/minutes/240"
    elif interval in ["week",  "weeks"]:
        endpoint = "candles/weeks"
    elif interval in ["month", "months"]:
        endpoint = "candles/months"
    else:
        endpoint = "candles/days"

    return endpoint


def _get_ohlcv(ticker="KRW-BTC", interval="day", count=1):

    to = datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    endpoint = _get_endpoint_ohlcv(interval)

    headers = {"Accept": "application/json"}

    params = {"market": ticker, "count": count, "to": to}

    response = _request(requests.get, endpoint, params=params, headers=headers)

    if response.get('data') and to[:10] != response['data'][0]['candle_date_time_utc'][:10]:
        return {
            'ok': False,
            'description': 'New trade_price is not out yet'
        }

    return response


def get_target_price(ticker='KRW-BTC'):
    response = _get_ohlcv(ticker=ticker, count=21)
    if not response.get('ok', False):
        return response
    data = response['data']
    vol_list = []
    for i in data[1:]:
        vol = 1 - abs(i['trade_price'] - i['opening_price']) / \
            (i['high_price'] - i['low_price'])
        vol_list.append(vol)
    k = sum(vol_list) / len(vol_list)
    volatility = (data[1]['high_price'] - data[1]['low_price']) * k
    target_price = data[0]['opening_price'] + volatility
    return {
        'ok': True,
        'target_price': target_price
    }
