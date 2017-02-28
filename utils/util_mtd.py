from utils import register, count


@register
def display_count():
    print('crwaled pages:{count}'.format(count=count))