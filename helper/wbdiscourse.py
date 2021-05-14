import os
import discord
from dotenv import load_dotenv

import logging
import time

import requests

from datetime import timedelta, datetime

from helper.exceptions import (
    DiscourseError,
    DiscourseServerError,
    DiscourseClientError,
    DiscourseRateLimitedError,
)

# HTTP verbs to be used as non string literals
DELETE = "DELETE"
GET = "GET"
POST = "POST"
PUT = "PUT"


class WBDiscourse:

    def __init__(self, timeout=None):
        """
        Initialize the Discourse API client. The host-url, api_username & api_key will be received from environment variables.
        Args:
            timeout: optional timeout for the requests (in seconds)
        Returns:
        """
        self.__loadEnv__()

        self.timeout = timeout

        self.categories = {
            3: "Teamtalk",
            5: "Modulthemen",
            7: "Stammtisch",
            9: "Erfahrungsbericht",
            10: "Wissenssammlung",
            11: "Tipps und Tricks",
            12: "WBH-Beschwerden",
            999: "Unknown",
        }

        self.colors = {
            3: discord.Colour.dark_orange(),
            5: discord.Colour.blue(),
            7: discord.Colour.green(),
            9: discord.Colour.blurple(),
            10: discord.Colour.dark_red(),
            11: discord.Colour.orange(),
            12: discord.Colour.darker_gray(),
        }

    def __loadEnv__(self):
        """
        Loads the required environment variables like url, api_key, etc. 
        """
        load_dotenv()
        # PROTOKOLL = 'https://'
        self.prot = os.getenv('PROTOKOLL')
        # URL = 'talk.wb-student.org/'
        self.url = os.getenv('URL')

        BASEURL = os.getenv('BASEURL')

        self.host = BASEURL if BASEURL else self.prot + self.url

        self.api_key = os.getenv('API_KEY')
        self.api_username = os.getenv('API_USERNAME')

        # initialize global logger
        self.log = logging.getLogger("helper.WBDiscourse")

    def getCategorieName(self, catID):
        # TODO: maybe use self.categories to get all categories from discourse server
        if catID in self.categories:
            return self.categories[catID]
        else:
            return self.categories[999]

    def getCategorieColor(self, catID):
        # TODO: maybe use self.color_schemes
        if catID in self.colors:
            return self.colors[catID]
        else:
            return self.colors[5]

    def BaseUrl(self):
        return self.host

    
    # --------------------------------     <start of API-Actions>     --------------------------------
    # The following functions are a python reproduction of the [Discourse-API](https://docs.discourse.org/)
    # The official discour_api repository can be found [here](https://github.com/discourse/discourse_api)
    #
    # © by bennylope 'pydiscourse' https://github.com/bennylope/pydiscourse/blob/master/pydiscourse/client.py
    # -------------------------------------------------------------------------------------------------

    # region ------------------     <start of USER-Functions>     ------------------

    # endregion ------------------     <end of USER-Functions>     ------------------

    # region ------------------     <start of INVITE-Functions>     ------------------

    # endregion ------------------     <end of INVITE-Functions>     ------------------

    # region ------------------     <start of ADMIN-Functions>     ------------------

    # endregion ------------------     <end of ADMIN-Functions>     ------------------

    # region ------------------     <start of Private-Message-Functions>     ------------------

    # endregion ------------------     <end of Private-Message-Functions>     ------------------

    # region ------------------     <start of Category-Functions>     ------------------

    # endregion ------------------     <end of Category-Functions>     ------------------

    # region ------------------     <start of Topic-Functions>     ------------------

    def posts_by_topic_id(self, topic_id, post_ids=None, **kwargs):
        """
        Get a set of posts from a topic
        Args:
            topic_id:
            post_ids: a list of post ids from the topic stream
            **kwargs:
        Returns:
        """
        if post_ids:
            kwargs["post_ids[]"] = post_ids
        return self._get("/t/{0}/posts.json".format(topic_id), **kwargs)

    def first_post_by_topic_id(self, topic_id, **kwards):
        """
        Same as posts_by_topic_id
        Args:
            topic_id:
            **kwargs:
        Returns:
            The first topic as json
        """
        posts = self.posts_by_topic_id(topic_id, None, **kwards)
        return posts['post_stream']['posts'][0]

    # endregion ------------------     <end of Topic-Functions>     ------------------

    # region ------------------     <start of Posts-Functions>     ------------------

    # endregion ------------------     <end of Posts-Functions>     ------------------

    # region ------------------     <start of Search-Functions>     ------------------

    def search(self, term, **kwargs):
        """
        Args:
            term:
            **kwargs:
        Returns:
        """
        kwargs["q"] = term
        return self._get("/search.json", **kwargs)

    # endregion ------------------     <end of Search-Functions>     ------------------

    # region ------------------     <start of Group-Functions>     ------------------

    # endregion ------------------     <end of Group-Functions>     ------------------

    # region ------------------     <start of Miscellaneous-Functions>     ------------------

    def color_schemes(self, **kwargs):
        """
        List color schemes in site
        Args:
            **kwargs:
        Returns:
        """
        return self._get("/admin/color_schemes.json", **kwargs)

    # endregion ------------------     <end of Miscellaneous-Functions>     ------------------

    # region ------------------     <start of HTTP-Default-Functions>     ------------------

    def _get(self, path, override_request_kwargs=None, **kwargs):
        """
        Args:
            path:
            **kwargs:
        Returns: A request object as json
        """
        return self._request(GET, path, params=kwargs, override_request_kwargs=override_request_kwargs)

    def _put(self, path, json=False, override_request_kwargs=None, **kwargs):
        """
        Args:
            path:
            **kwargs:
        Returns: A request object as json
        """
        if not json:
            return self._request(PUT, path, data=kwargs, override_request_kwargs=override_request_kwargs)

        else:
            return self._request(PUT, path, json=kwargs, override_request_kwargs=override_request_kwargs)

    def _post(self, path, files=None, json=False, override_request_kwargs=None, **kwargs):
        """
        Args:
            path:
            **kwargs:
        Returns: A request object as json
        """
        if not json:
            return self._request(POST, path, files=files, data=kwargs, override_request_kwargs=override_request_kwargs)

        else:
            return self._request(POST, path, files=files, json=kwargs, override_request_kwargs=override_request_kwargs)

    def _delete(self, path, override_request_kwargs=None, **kwargs):
        """
        Args:
            path:
            **kwargs:
        Returns: A request object as json
        """
        return self._request(DELETE, path, params=kwargs, override_request_kwargs=override_request_kwargs)

    def _request(self, verb, path, params=None, files=None, data=None, json=None, override_request_kwargs=None):
        """
        Executes HTTP request to API and handles response
        Args:
            verb: HTTP verb as string: GET, DELETE, PUT, POST
            path: the path on the Discourse API
            params: dictionary of parameters to include to the API
            override_request_kwargs: dictionary of requests.request keyword arguments to override defaults
        Returns:
            dictionary of response body data or None
        """
        override_request_kwargs = override_request_kwargs or {}

        url = self.BaseUrl() + path

        headers = {
            "Accept": "application/json; charset=utf-8",
            "Api-Key": self.api_key,
            "Api-Username": self.api_username,
        }

        # How many times should we retry if rate limited
        retry_count = 4
        # Extra time (on top of that required by API) to wait on a retry.
        retry_backoff = 1

        while retry_count > 0:
            request_kwargs = dict(
                allow_redirects=False,
                params=params,
                files=files,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )

            request_kwargs.update(override_request_kwargs)

            response = requests.request(verb, url, **request_kwargs)

            self.log.debug("response %s: %s", response.status_code,
                           repr(response.text))
            if response.ok:
                break
            if not response.ok:
                try:
                    msg = u",".join(response.json()["errors"])
                except (ValueError, TypeError, KeyError):
                    if response.reason:
                        msg = response.reason
                    else:
                        msg = u"{0}: {1}".format(
                            response.status_code, response.text)

                if 400 <= response.status_code < 500:
                    if 429 == response.status_code:
                        # This codepath relies on wait_seconds from Discourse v2.0.0.beta3 / v1.9.3 or higher.
                        rj = response.json()
                        wait_delay = (
                            retry_backoff + rj["extras"]["wait_seconds"]
                        )  # how long to back off for.

                        if retry_count > 1:
                            time.sleep(wait_delay)
                        retry_count -= 1
                        self.log.info(
                            "We have been rate limited and waited {0} seconds ({1} retries left)".format(
                                wait_delay, retry_count
                            )
                        )
                        self.log.debug("API returned {0}".format(rj))
                        continue
                    else:
                        raise DiscourseClientError(msg, response=response)

                # Any other response.ok resulting in False
                raise DiscourseServerError(msg, response=response)

        if retry_count == 0:
            raise DiscourseRateLimitedError(
                "Number of rate limit retries exceeded. Increase retry_backoff or retry_count",
                response=response,
            )

        if response.status_code == 302:
            raise DiscourseError(
                "Unexpected Redirect, invalid api key or host?", response=response
            )

        json_content = "application/json; charset=utf-8"
        content_type = response.headers["content-type"]
        if content_type != json_content:
            # some calls return empty html documents
            if not response.content.strip():
                return None

            raise DiscourseError(
                'Invalid Response, expecting "{0}" got "{1}"'.format(
                    json_content, content_type
                ),
                response=response,
            )

        try:
            decoded = response.json()
        except ValueError:
            raise DiscourseError(
                "failed to decode response", response=response)

        # Checking "errors" length because
        # data-explorer (e.g. POST /admin/plugins/explorer/queries/{}/run)
        # sends an empty errors array
        if "errors" in decoded and len(decoded["errors"]) > 0:
            message = decoded.get("message")
            if not message:
                message = u",".join(decoded["errors"])
            raise DiscourseError(message, response=response)

        return decoded
    # endregion ------------------     <end of HTTP-Default-Functions>     ------------------

    # --------------------------------     <end of API-Actions>     --------------------------------
