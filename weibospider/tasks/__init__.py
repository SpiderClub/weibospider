from .login import execute_login_task
from .search import execute_search_task
from .comment import execute_comment_task
from .home import execute_home_task
from .repost import execute_repost_task
from .user import execute_user_task
from .praise import execute_praise_task
from .dialogue import execute_dialogue_task


task_maps = {
    'login': execute_login_task,
    'search': execute_search_task,
    'comment': execute_comment_task,
    'home': execute_home_task,
    'repost': execute_repost_task,
    'user': execute_user_task,
    'praise': execute_praise_task,
    'dialogue': execute_dialogue_task
}