import logging
import os

import enoslib as en

logger = logging.getLogger(__name__)


@en.enostask(new=True)
def g5k(config, force, env=None, **kwargs):
    # Load the configuration.
    # Alternatively you can build the configuration programmatically
    conf = en.G5kConf.from_dictionnary(config["g5k"])
    provider = en.G5k(conf)
    roles, networks = provider.init(force_deploy=force)
    env["config"] = config
    env["roles"] = roles
    env["networks"] = networks
    env["provider"] = provider


@en.enostask(new=True)
def vagrant(config, force, env=None, **kwargs):
    # Load the configuration.
    # Alternatively you can build the configuration programmatically
    conf = en.VagrantConf.from_dictionnary(config["vagrant"])
    provider = en.Vagrant(conf)
    roles, networks = provider.init(force_deploy=force)
    env["config"] = config
    env["roles"] = roles
    env["networks"] = networks
    env["provider"] = provider


@en.enostask()
def prepare(env=None, **kwargs):
    roles = env["roles"]
    with en.play_on(roles=roles) as p:
        p.debug(msg="Hello World !")


@en.enostask()
def destroy(env=None, **kwargs):
    provider = env["provider"]
    provider.destroy()


PROVIDERS = {
    "g5k": g5k,
    "vagrant": vagrant,
    #    "static": static
    #    "chameleon": chameleon
}
