from enoslib.api import generate_inventory, run_ansible
from enoslib.task import enostask
from enoslib.infra.enos_g5k.provider import G5k
from enoslib.infra.enos_vagrant.provider import Enos_vagrant
import logging
import os

from {{ cookiecutter.project_slug }}.constants import ANSIBLE_DIR

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
    env["inventory"] = os.path.join(env["resultdir"], "hosts")
    generate_inventory(roles, networks, env["inventory"], check_networks=True)


@enostask()
def prepare(**kwargs):
    env = kwargs["env"]
    extra_vars = {
        "enos_action": "deploy"
    }
    run_ansible([os.path.join(ANSIBLE_DIR, "site.yml")],
                env["inventory"], extra_vars=extra_vars)


@enostask()
def backup(**kwargs):
    env = kwargs["env"]
    extra_vars = {
        "enos_action": "backup"
    }
    run_ansible([os.path.join(ANSIBLE_DIR, "site.yml")],
                env["inventory"], extra_vars=extra_vars)


@enostask()
def destroy(**kwargs):
    env = kwargs["env"]
    extra_vars = {
        "enos_action": "destroy"
    }
    run_ansible([os.path.join(ANSIBLE_DIR, "site.yml")],
                env["inventory"], extra_vars=extra_vars)


PROVIDERS = {
    "g5k": g5k,
    "vagrant": vagrant,
#    "static": static
#    "chameleon": chameleon
}
