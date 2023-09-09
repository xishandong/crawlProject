# -*- coding: utf-8 -*-
"""
Created on 2023-09-09 16:11:59
---------
@summary:
---------
@author: dongxishan
"""
from typing import Union

import feapder

from RedBook.items.items import Comment
from RedBook.midware.add_cookie import add_cookie
from RedBook.midware.get_XsXt import add_XsXt
from RedBook.types.QueryJsonType import QueryNoteComment, QueryNoteSubComment


class GetComment(feapder.AirSpider):
    name = "get_comment"

    def __init__(self, notes: Union[str, list], **kwargs):
        super().__init__(**kwargs)
        self.notes = notes

    def start_requests(self):
        if isinstance(self.notes, str):
            yield feapder.Request(
                url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/page",
                method='GET',
                params=QueryNoteComment(
                    note_id=self.notes,
                    cursor=''
                ),
                download_midware=[add_cookie, add_XsXt]
            )
        elif isinstance(self.notes, list):
            for id in self.notes:
                yield feapder.Request(
                    url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/page",
                    method='GET',
                    params=QueryNoteComment(
                        note_id=id,
                        cursor=''
                    ),
                    download_midware=[add_cookie, add_XsXt]
                )

    def parse(self, request, response):
        resp = response.json
        note_id = request.params.get('note_id')
        has_more = resp.get('data', {}).get('has_more')
        if has_more:
            yield feapder.Request(
                url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/page",
                method='GET',
                params=QueryNoteComment(
                    note_id=note_id,
                    cursor=resp['data']['cursor']
                ),
                download_midware=[add_cookie, add_XsXt]
            )
        data = resp.get('data', {}).get('comments')
        for comment in data:
            yield from self.parse_comment(note_id, comment)

    def parse_comment(self, note_id: str, comment: dict):
        # 子评
        if comment.get('target_comment', {}):
            target_comment = comment.get('target_comment', {}).get('id')
        else:
            target_comment = 'root_comment'
        root_id = None
        # 传递第一次的子评论
        if comment.get('sub_comments'):
            root_id = comment['id']
            for sub_comment in comment['sub_comments']:
                yield from self.parse_comment(note_id, sub_comment)
        # 点击更多
        if comment.get('sub_comment_has_more') and root_id:
            sub_comment_cursor = comment.get('sub_comment_cursor')
            root_comment_id = root_id
            yield from self.start_more_comment(sub_comment_cursor, note_id, root_comment_id)

        yield Comment(
            note_id=note_id,
            target_comment=target_comment,
            comment_id=comment['id'],
            content=comment['content'],
            like_count=comment['like_count'],
            user_id=comment['user_info']['user_id'],
            user_name=comment['user_info']['nickname'],
        )

    def start_more_comment(self, cursor, note_id, root_id):
        yield feapder.Request(
            url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
            method='GET',
            params=QueryNoteSubComment(
                note_id=note_id,
                cursor=cursor,
                num='10',
                root_comment_id=root_id
            ),
            download_midware=[add_cookie, add_XsXt],
            callback=self.parse_sub_comment
        )

    def parse_sub_comment(self, request, response):
        resp = response.json
        has_more = resp.get('data', {}).get('has_more')
        if has_more:
            yield from self.start_more_comment(
                cursor=resp['data']['cursor'],
                note_id=request.params.get('note_id'),
                root_id=request.params.get('root_comment_id')
            )
        data = resp.get('data', {}).get('comments')
        for comment in data:
            yield from self.parse_comment(request.params.get('note_id'), comment)


if __name__ == "__main__":
    GetComment(
        ['64cb8674000000000b02b8de', '64a7e168000000000f00efcb', '64eca3da000000001f03d11b'],
        thread_count=10
    ).start()
