# Standard Library
import logging

# Third Party Library
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException
from urllib3.util.retry import Retry

# Project Library
from project.configs.project_config import config

logger = logging.getLogger(__name__)

error_codes = config.get(section="rest_session", key="error_codes")
error_codes = tuple([int(i) for i in error_codes.split(",")])
backoff_factor = int(config.get(section="rest_session", key="backoff_factor"))
max_retries = int(config.get(section="rest_session", key="max_retries"))
verify = config.get(section="rest_session", key="secure") == "true"


class RestUtility:
    def __init__(self, **kwargs):
        self.retries = Retry(
            total=kwargs.get("max_retries") or max_retries,
            read=kwargs.get("max_retries") or max_retries,
            connect=kwargs.get("max_retries") or max_retries,
            backoff_factor=kwargs.get("backoff_factor") or backoff_factor,
            status_forcelist=kwargs.get("error_codes") or error_codes,
            raise_on_status=kwargs.get("raise_on_status") or False,
        )
        self.token_generator = kwargs.get("token_generator")
        self.access_token = None
        self.session = requests.Session()
        self.max_retries = HTTPAdapter(max_retries=self.retries)
        self.timeout = kwargs.get("timeout") or 300
        self.authorization_via_tokens = kwargs.get("authorization_via_tokens")
        self._request_id = kwargs.get("request_id")
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-Request-ID": self._request_id,
        }
        self.verify_token()
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        if self.username is not None and self.password is not None:
            logger.info(f"Using username and password for authentication")
            self.session.auth = (self.username, self.password)
            self.session.client = kwargs.get("ssl_cert", None)
        self.session.verify = kwargs.get("verify") or verify

    def get_headers(self):
        return self.headers

    def set_headers(self, headers):
        self.headers = headers

    def update_headers(self, headers):
        self.headers.update(headers)

    def verify_token(self):
        if self.authorization_via_tokens and self.token_generator:
            self.access_token, headers = self.token_generator(self.access_token)
            self.update_headers(headers)

    def get(self, url, params=None, timeout=None, headers=None, **kwargs):
        """
        :param headers:
        :param url: REST URL
        :param params: any parameters
        :param timeout:
        :return: @response as json
        """
        logger.debug(f"Error Codes considered for retry: {error_codes}")
        logger.debug(f"Retries with back-off time: {self.retries.get_backoff_time()}")
        self.session.mount(url, self.max_retries)
        try:
            timeout = timeout or self.timeout
            logger.info(f"Get request to server URL: {url}")
            headers = headers or self.headers
            content_type = kwargs.get("content_type")
            if content_type and headers.get("Content-Type") is not None:
                del headers["Content-Type"]
            self.verify_token()
            response = self.session.get(url=url, params=params, timeout=timeout, headers=headers)
            logger.debug(f"Request header in GET method is : {headers}")
            logger.debug(f"Response from Target: {response}")
            logger.debug(f"Response Code from Target: {response.status_code}")
            logger.debug(f"Response from target in TEXT format : {response.text}")
            api_status = True if response.status_code in (kwargs.get("expected_response_codes") or [200]) else False
            response_code = response.status_code
            try:
                out_json = response.json()
            except ValueError:
                out_json = {"detail": response.text}
            return api_status, response_code, out_json, response
        except (RequestException, HTTPError) as err:
            logger.exception(err)
            return False, "000", {}, None

    def post(self, url, data, params=None, timeout=None, headers=None, files=None, **kwargs):
        """
        :param headers:
        :param params:
        :param url: REST URL
        :param data:
        :param timeout:
        :param files:
        :return: @response as json

        Args:

        """
        logger.debug(f"Error Codes considered for retry: {error_codes}")
        logger.debug(f"Retries with back-off time: {self.retries.get_backoff_time()}")
        self.session.mount(url, self.max_retries)
        try:
            timeout = timeout or self.timeout
            logger.info(f"Post request to server URL: {url}")
            headers = headers or self.headers
            content_type = kwargs.get("content_type")
            if content_type and headers.get("Content-Type") is not None:
                del headers["Content-Type"]
            self.verify_token()
            response = self.session.post(
                url=url, params=params, data=data, timeout=timeout, headers=headers, files=files
            )
            logger.debug(f"Request header in POST method : {headers}")
            logger.debug(f"Response from target: {response}")
            logger.debug(f"Response Code from target: {response.status_code}")
            logger.debug(f"Response from target in TEXT format : {response.text}")
            api_status = True if response.status_code == (kwargs.get("expected_response_codes") or [201]) else False
            response_code = response.status_code
            try:
                out_json = response.json()
            except ValueError:
                out_json = {"detail": response.text}
            return api_status, response_code, out_json, response
        except (RequestException, HTTPError) as err:
            logger.exception(err)
            return False, "000", {}, None

    def put(self, url, data, params=None, timeout=None, headers=None, **kwargs):  # noqa: C901
        """
        :param params:
        :param headers:
        :param url: REST URL
        :param data:
        :param timeout:
        :return: @response as json
        """
        logger.debug(f"Error Codes considered for retry: {error_codes}")
        logger.debug(f"Retries with back-off time: {self.retries.get_backoff_time()}")
        self.session.mount(url, self.max_retries)
        try:
            timeout = timeout or self.timeout
            logger.info(f"Put request to server URL: {url}")
            headers = headers or self.headers
            content_type = kwargs.get("content_type")
            if content_type and headers.get("Content-Type") is not None:
                del headers["Content-Type"]
            self.verify_token()
            response = self.session.put(url=url, params=params, data=data, timeout=timeout, headers=headers)
            logger.debug(f"Request header in PUT method is : {headers}")
            logger.debug(f"Response from target: {response}")
            logger.debug(f"Response Code from target: {response.status_code}")
            logger.debug(f"Response from target in TEXT format : {response.text}")
            api_status = True if response.status_code == (kwargs.get("expected_response_codes") or [201]) else False
            response_code = response.status_code
            try:
                out_json = response.json()
            except ValueError:
                out_json = {"detail": response.text}
            return api_status, response_code, out_json, response
        except (RequestException, HTTPError) as err:
            logger.exception(err)
            return False, "000", {}, None

    def delete(self, url, data, params=None, timeout=None, headers=None, **kwargs):  # noqa: C901
        """
        :param params:
        :param headers:
        :param url: REST URL
        :param data:
        :param timeout:
        :return: @response as json
        """
        logger.debug(f"Error Codes: {error_codes}")
        logger.debug(f"Retries with urlib3 in back-off time: {self.retries.get_backoff_time()}")
        self.session.mount(url, self.max_retries)
        try:
            timeout = timeout or self.timeout
            logger.info(f"DELETE request to server URL: {url}")
            headers = headers or self.headers
            content_type = kwargs.get("content_type")
            if content_type and headers.get("Content-Type") is not None:
                del headers["Content-Type"]
            self.verify_token()
            response = self.session.delete(url=url, params=params, data=data, timeout=timeout, headers=headers)
            logger.debug(f"Request header in DELETE method is : {headers}")
            logger.debug(f"Response from target: {response}")
            logger.debug(f"Response Code from target: {response.status_code}")
            logger.debug(f"Response from target in TEXT format : {response.text}")
            api_status = True if response.status_code == (kwargs.get("expected_response_codes") or [200]) else False
            response_code = response.status_code
            try:
                out_json = response.json()
            except ValueError:
                out_json = {"detail": response.text}
            return api_status, response_code, out_json, response
        except (RequestException, HTTPError) as err:
            logger.exception(err)
            return False, "000", {}, None

    def patch(self, url, data, params=None, timeout=None, headers=None, files=None, **kwargs):  # noqa: C901
        """
        :param params:
        :param headers:
        :param files:
        :param url: REST URL
        :param data:
        :param timeout:
        :return: @response as json
        """
        logger.debug(f"Error Codes: {error_codes}")
        logger.debug(f"Retries with urlib3 in back-off time: {self.retries.get_backoff_time()}")
        self.session.mount(url, self.max_retries)
        try:
            timeout = timeout or self.timeout
            logger.info(f"PATCH request to server URL: {url}")
            headers = headers or self.headers
            content_type = kwargs.get("content_type")
            if content_type and headers.get("Content-Type") is not None:
                del headers["Content-Type"]
            self.verify_token()
            response = self.session.patch(
                url=url, params=params, data=data, timeout=timeout, headers=headers, files=files
            )
            logger.debug(f"Request header in PATCH method is : {headers}")
            logger.debug(f"Response from target: {response}")
            logger.debug(f"Response Code from target: {response.status_code}")
            logger.debug(f"Response from target in TEXT format : {response.text}")
            api_status = True if response.status_code == (kwargs.get("expected_response_codes") or [200]) else False
            response_code = response.status_code
            try:
                out_json = response.json()
            except ValueError:
                out_json = {"detail": response.text}
            return api_status, response_code, out_json, response
        except (RequestException, HTTPError) as err:
            logger.exception(err)
            return False, "000", {}, None
