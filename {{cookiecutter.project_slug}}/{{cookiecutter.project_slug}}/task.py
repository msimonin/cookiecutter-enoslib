from enoslib.api import generate_inventory
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_vagrant.provider import Enos_vagrant
import logging

logger = logging.getLogger(__name__)


def init_provider(provider, name, force, config, env):
    instance = provider(config[name])
    roles, networks = instance.init(force_deploy=force)
    env["config"] = config
    env["roles"] = roles
    env["networks"] = networks


@enostask(new=True)
def g5k(**kwargs):
    init_provider(G5k, "g5k", **kwargs)


@enostask(new=True)
def vagrant(**kwargs):
    init_provider(Enos_vagrant, "vagrant", **kwargs)


@enostask()
def inventory(**kwargs):
    env = kwargs["env"]
    roles = env["roles"]
    networks = env["networks"]
    env["inventory"] = path.join(env["resultdir"], "hosts")
    generate_inventory(roles, networks, env["inventory"], check_networks=True)
