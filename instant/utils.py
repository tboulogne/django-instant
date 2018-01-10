# -*- coding: utf-8 -*-
from cent.core import generate_channel_sign
from .conf import PUBLIC_CHANNEL, SECRET_KEY, PUBLIC_CHANNELS, \
    USERS_CHANNELS, STAFF_CHANNELS, SUPERUSER_CHANNELS, ENABLE_PUBLIC_CHANNEL, \
    ENABLE_USERS_CHANNEL, ENABLE_STAFF_CHANNEL, ENABLE_SUPERUSER_CHANNEL, \
    DEFAULT_USERS_CHANNEL, DEFAULT_STAFF_CHANNEL, DEFAULT_SUPERUSER_CHANNEL


def signed_response(channel, client):
    signature = generate_channel_sign(SECRET_KEY, client, channel, info="")
    return {"sign": signature}


def _get_public_channel():
    return PUBLIC_CHANNEL


def _ensure_channel_is_private(chan):
    if chan.startswith("$") is False:
        return "$" + chan
    return chan


def _check_chanconf(chanconf, private=True):
    chan = chanconf[0]
    if private is True:
        chan = _ensure_channel_is_private(chan)
    path = None
    if len(chanconf) > 1:
        path = chanconf[1]
    chan = dict(slug=chan, path=path)
    return chan


def channels_for_role(role):
    """
    Get the channels for a role
    """
    chans = []
    # default channels
    if role == "public":
        if ENABLE_PUBLIC_CHANNEL is True:
            chan = dict(slug=PUBLIC_CHANNEL, path=None)
            chans.append(chan)
    elif role == "users":
        if ENABLE_USERS_CHANNEL is True:
            chan = _ensure_channel_is_private(DEFAULT_USERS_CHANNEL)
            chan = dict(slug=chan, path=None)
            chans.append(chan)
    elif role == "staff":
        if ENABLE_STAFF_CHANNEL is True:
            chan = _ensure_channel_is_private(DEFAULT_STAFF_CHANNEL)
            chan = dict(slug=chan, path=None)
            chans.append(chan)
    elif role == "superuser":
        if ENABLE_SUPERUSER_CHANNEL is True:
            chan = _ensure_channel_is_private(DEFAULT_SUPERUSER_CHANNEL)
            chan = dict(slug=chan, path=None)
            chans.append(chan)
    # declared channels
    if role == "public":
        if len(PUBLIC_CHANNELS) > 0:
            for chanconf in PUBLIC_CHANNELS:
                chan = _check_chanconf(chanconf, False)
                chans.append(chan)
    if role == "users":
        if len(USERS_CHANNELS) > 0:
            for chanconf in USERS_CHANNELS:
                chan = _check_chanconf(chanconf)
                chans.append(chan)
    if role == "staff":
        if len(STAFF_CHANNELS) > 0:
            for chanconf in STAFF_CHANNELS:
                chan = _check_chanconf(chanconf)
                chans.append(chan)
    if role == "superuser":
        if len(SUPERUSER_CHANNELS) > 0:
            for chanconf in SUPERUSER_CHANNELS:
                chan = _check_chanconf(chanconf)
                chans.append(chan)
    return chans


def get_channels_for_roles():
    chans = dict(public=[], users=[], staff=[], superuser=[])
    roles = ["public", "users", "staff", "superuser"]
    for role in roles:
        chans[role] = channels_for_role(role)
    return chans
