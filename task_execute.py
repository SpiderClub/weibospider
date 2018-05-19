import click

from weibospider.tasks import task_maps
from weibospider.exceptions import NoAssignedTaskError


@click.command()
@click.option('--task', type=click.Choice(task_maps.keys()), help='task name in task maps')
def task_execute(task):
    if not task:
        raise NoAssignedTaskError('You must type in a task assigned in task map')
    schedule = task_maps.get(task)
    schedule()


if __name__ == '__main__':
    task_execute()