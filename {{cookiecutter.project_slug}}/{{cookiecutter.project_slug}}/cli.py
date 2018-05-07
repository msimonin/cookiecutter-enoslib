import logging

import click

import {{ cookiecutter.project_slug }}.tasks as t

logging.basicConfig(level=logging.DEBUG)


@click.group()
def cli():
    pass


def load_config(file_path):
    """
    Read configuration from a file in YAML format.
    :param file_path: Path of the configuration file.
    :return:
    """
    with open(file_path) as f:
        configuration = yaml.safe_load(f)
    return configuration


@cli.command(help="Claim resources on Grid'5000 (frontend).")
@click.option("--force",
              is_flag=True,
              help="force redeployment")
@click.option("--conf",
              default=CONF,
              help="alternative configuration file")
@click.option("--env",
              help="alternative environment directory")
def g5k(constraints, force, conf, env):
    config = load_config(conf)
    t.g5k(force=force, config=config, env=env)


@cli.command(help="Claim resources on vagrant (localhost).")
@click.option("--force",
              is_flag=True,
              help="force redeployment")
@click.option("--conf",
              default=CONF,
              help="alternative configuration file")
@click.option("--env",
              help="alternative environment directory")
def vagrant(constraints, force, conf, env):
    config = load_config(conf)
    t.vagrant(force=force, config=config, env=env)


@cli.command(help="Generate the Ansible inventory [after g5k or vagrant].")
@click.option("--env",
              help="alternative environment directory")
def inventory(env):
    t.inventory(env=env)
