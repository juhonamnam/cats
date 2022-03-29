import datetime
import time
import websocket
import json
from src.resources import get_message
from src.websocket.upbit_api import get_target_price
from src.main.model import get_active_users_info
from src.telesk import Telesk
import threading


class UpbitWebsocket:
    def __init__(self, tickers: list, telesk_app: Telesk) -> None:
        self._tickers = tickers
        self._reset_time = datetime.datetime.now(datetime.timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0)
        self._target_prices = {ticker: None for ticker in tickers}
        self._curr_prices = {ticker: 0 for ticker in tickers}
        self._buy_sigs = {ticker: {'flag': False, 'buy_price': None}
                          for ticker in tickers}
        self._working = True
        self._tickers = tickers
        self._telesk_app = telesk_app
        self._started = False

    def _on_message(self, ws, message):
        msg: dict = json.loads(message)
        self._process_message(msg)

    def _on_error(self, ws, error):
        self._telesk_app.logger.error(error)

    def _on_close(self, ws, close_status_code, close_msg):
        self._telesk_app.logger.info(
            f"Connection Lost: {{Close Code: {close_status_code}, Close Message: {close_msg}}}")

    def _on_open(self, ws):
        if self._started:
            self._telesk_app.logger.info('Reconnect')
        else:
            self._started = True
            self._telesk_app.logger.info('Upbit Websocket Start')
        ws.send(json.dumps(
            [{"ticket": "test"}, {"type": "ticker", "codes": self._tickers}]))

    def run(self):
        try:
            url = "wss://api.upbit.com/websocket/v1"
            ws = websocket.WebSocketApp(url,
                                        on_open=self._on_open,
                                        on_message=self._on_message,
                                        on_error=self._on_error,
                                        on_close=self._on_close,)
            while True:
                ws.run_forever()
                time.sleep(10)
        except KeyboardInterrupt:
            self._telesk_app.logger.info('Upbit Websocket End')
            exit()

    def _process_message(self, msg):
        if self._working:
            now = datetime.datetime.now(datetime.timezone.utc)
            ticker = msg['code']
            curr_price = msg['trade_price']
            self._curr_prices[ticker] = curr_price

            # Sell Signal
            if now > self._reset_time:
                self._working = False

                def set_new_reset_time():
                    self._reset_time += datetime.timedelta(days=1)
                    for ticker in self._tickers:
                        self._set_target_price(ticker)
                        if self._buy_sigs[ticker]['flag']:
                            self._buy_sigs[ticker]['flag'] = False
                            buy_price = self._buy_sigs[ticker]["buy_price"]
                            sell_price = self._curr_prices[ticker]
                            interest = 100 * \
                                ((self._curr_prices[ticker] - self._buy_sigs[ticker]['buy_price'])
                                    / self._buy_sigs[ticker]['buy_price'])
                            self._send_tele_message(
                                'sellsig',
                                ticker=ticker,
                                sell_price=sell_price,
                                buy_price=buy_price,
                                interest=interest
                            )
                            self._telesk_app.logger.info(
                                f'Sell Signal: {{Ticker: {ticker}, Sell Price: {sell_price}, Buy Price: {buy_price}, Interest: {interest}}}')
                        time.sleep(0.5)
                    self._telesk_app.logger.info(
                        f'New Target Price: {self._target_prices}')
                    self._working = True

                threading.Thread(target=set_new_reset_time,
                                 daemon=True).start()

            # Buy Signal
            elif not self._buy_sigs[ticker]['flag'] and curr_price >= self._target_prices[ticker]:
                self._buy_sigs[ticker]['flag'] = True

                def buy_signal():
                    self._telesk_app.logger.info(
                        f'Buy Signal: {{Ticker:{ticker}, Current Price:{curr_price}}}')
                    self._buy_sigs[ticker]['buy_price'] = curr_price
                    self._send_tele_message(
                        'buysig', ticker=ticker, curr_price=curr_price)

                threading.Thread(target=buy_signal, daemon=True).start()

    def _set_target_price(self, ticker):
        response = get_target_price(ticker)
        if response.get('ok', False):
            self._target_prices[ticker] = response['target_price']
        else:
            self._telesk_app.logger.error(response['description'])
            time.sleep(5)
            self._set_target_price(ticker)

    def _send_tele_message(self, msg_code, **kwargs):
        users = get_active_users_info()
        for user in users:
            msg_thread = threading.Thread(target=self._telesk_app.send_message, args=[
                                          user.id, get_message(user.language)(msg_code).format(**kwargs)])
            msg_thread.start()
