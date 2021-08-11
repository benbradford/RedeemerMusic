from flask import redirect, url_for

UNAUTHORISED = "The current user is not authorised to perform that operation"


def redirect_url(url, **kwargs):
    return redirect(url_for(url, _external=True, _scheme='https', **kwargs))


