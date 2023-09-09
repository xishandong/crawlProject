# -*- coding: utf-8 -*-
"""
Created on 2023-09-09 12:22:13
---------
@summary:
---------
@author: dongxishan
"""

from feapder import Item


class NoteItem(Item):
    """
    帖子实体
    """

    __table_name__ = "note"
    __unique_key__ = "note_id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.avatar = kwargs.get('avatar')
        self.display_title = kwargs.get('display_title')
        self.liked_count = kwargs.get('liked_count')
        self.note_cover = kwargs.get('note_cover')
        self.note_id = kwargs.get('note_id')
        self.note_type = kwargs.get('note_type')
        self.user_id = kwargs.get('user_id')
        self.user_name = kwargs.get('user_name')


class Comment(Item):
    """
    评论实体
    """
    __table_name__ = "comment"
    __unique_key__ = "comment_id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.note_id = kwargs.get('note_id')
        self.comment_id = kwargs.get('comment_id')
        self.content = kwargs.get('content')
        self.target_comment = kwargs.get('target_comment')
        self.user_id = kwargs.get('user_id')
        self.user_name = kwargs.get('user_name')