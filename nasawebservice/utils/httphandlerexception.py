def aiohttp_handler_exception(status_code: int) -> str:
    """The aiohttp.web defines a set of exceptions for every HTTP status code.
    This returns a label about the HTTP Exception.

        via [aiohttp Web Server Exceptions] https://docs.aiohttp.org/en/latest/web_exceptions.html

        via [RFC 2068] https://datatracker.ietf.org/doc/html/rfc2068.html

    HTTPException -> HTTPSuccessful: 200, 201, 202, 203, 204, 205, 206
    HTTPException -> HTTPRedirection: 304
    HTTPException -> HTTPRedirection -> HTTPMove: 300, 301, 302, 303, 305, 307, 308
    HTTPException -> HTTPError -> HTTPClientError: 400, 401, 402, ..., 429, 431, 451
    HTTPException -> HTTPError -> HTTPServerError: 500, ..., 507, 510, 511

    Parameters
    ----------
    status_code: int
        HTTP status code according to RFC 2068.

    Returns
    -------
    str
        HTTP Exception label. If Unknown status code is used, the methods return 'Unknown status code' label.

    Notes
    -----
    .. [1] Each exception class has a status code according to RFC 2068: codes with 100-300 are not really errors; 400s are client errors, and 500s are server errors.

    """
    switcher = {
        # HTTPException -> HTTPSuccessful
        200: 'HTTPOk',
        201: 'HTTPCreated',
        202: 'HTTPAccepted',
        203: 'HTTPNonAuthoritativeInformation',
        204: 'HTTPNoContent',
        205: 'HTTPResetContent',
        206: 'HTTPPartialContent',
        # HTTPException -> HTTPRedirection
        304: 'HTTPNotModified',
        # HTTPException -> HTTPRedirection -> HTTPMove
        300: 'HTTPMultipleChoices',
        301: 'HTTPMovedPermanently',
        302: 'HTTPFound',
        303: 'HTTPSeeOther',
        305: 'HTTPUseProxy',
        307: 'HTTPTemporaryRedirect',
        308: 'HTTPPermanentRedirect',
        # HTTPException -> HTTPError -> HTTPClientError
        400: 'HTTPBadRequest',
        401: 'HTTPUnauthorized',
        402: 'HTTPPaymentRequired',
        403: 'HTTPForbidden',
        404: 'HTTPNotFound',
        405: 'HTTPMethodNotAllowed',
        406: 'HTTPNotAcceptable',
        407: 'HTTPProxyAuthenticationRequired',
        408: 'HTTPRequestTimeout',
        409: 'HTTPConflict',
        410: 'HTTPGone',
        411: 'HTTPLengthRequired',
        412: 'HTTPPreconditionFailed',
        413: 'HTTPRequestEntityTooLarge',
        414: 'HTTPRequestURITooLong',
        415: 'HTTPUnsupportedMediaType',
        416: 'HTTPRequestRangeNotSatisfiable',
        417: 'HTTPExpectationFailed',
        421: 'HTTPMisdirectedRequest',
        422: 'HTTPUnprocessableEntity',
        424: 'HTTPFailedDependency',
        426: 'HTTPUpgradeRequired',
        428: 'HTTPPreconditionRequired',
        429: 'HTTPTooManyRequests',
        431: 'HTTPRequestHeaderFieldsTooLarge',
        451: 'HTTPUnavailableForLegalReasons',
        # HTTPException -> HTTPError -> HTTPServerError
        500: 'HTTPInternalServerError',
        501: 'HTTPNotImplemented',
        502: 'HTTPBadGateway',
        503: 'HTTPServiceUnavailable',
        504: 'HTTPGatewayTimeout',
        505: 'HTTPVersionNotSupported',
        506: 'HTTPVariantAlsoNegotiates',
        507: 'HTTPInsufficientStorage',
        510: 'HTTPNotExtended',
        511: 'HTTPNetworkAuthenticationRequired'
    }
    return switcher.get(status_code, 'Unknown status code')
