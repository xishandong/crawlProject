# -*- coding: utf-8 -*-
"""
Created on 2023-09-08 19:08:21
---------
@summary:
---------
@author: dongxishan
"""

import feapder
from feapder.utils.log import log

from RedBook.items.items import NoteItem
from RedBook.midware.add_cookie import add_cookie
from RedBook.midware.get_XsXt import add_XsXt
from RedBook.types.QueryJsonType import QueryHomeFeedNote
from RedBook.setting import CSV_PATH, ITEM_PIPELINES


class GetHomeFeed(feapder.AirSpider):
    MAPPING: dict = dict(zip(
        range(10),
        [
            'homefeed_recommend', 'homefeed.fashion_v3', 'homefeed.food_v3', 'homefeed.cosmetics_v3',
            'homefeed.movie_and_tv_v3', 'homefeed.career_v3', 'homefeed.love_v3',
            'homefeed.household_product_v3', 'homefeed.gaming_v3', 'homefeed.travel_v3', 'homefeed.fitness_v3'
        ]
    ))
    # 默认采集主页推荐
    QUERY = QueryHomeFeedNote(
        cursor_score='',
        num=36,
        refresh_type=1,
        note_index=29,
        unread_begin_note_id='',
        unread_end_note_id='',
        unread_note_count=0,
        category='homefeed_recommend'
    )

    def __init__(self, types: int = 0):
        super().__init__()
        self.QUERY['category'] = self.MAPPING[types]
        if "RedBook.custom_pipeline.csvPipeline.CsvPipeline" in ITEM_PIPELINES:
            log.info("csvPipeline已启用, 保存文件路径为: RedBook/custom/csv_data/{}".format(CSV_PATH))

    def start_requests(self):
        yield feapder.Request(
            url="https://edith.xiaohongshu.com/api/sns/web/v1/homefeed",
            method='POST',
            json=self.QUERY,
            download_midware=[add_cookie, add_XsXt]
        )

    def parse(self, request, response):
        resp = response.json
        cursor_score = resp.get('data', {}).get('cursor_score')
        if cursor_score:
            self.QUERY['cursor_score'] = cursor_score
            yield feapder.Request(
                url="https://edith.xiaohongshu.com/api/sns/web/v1/homefeed",
                method='POST',
                json=self.QUERY,
                download_midware=[add_cookie, add_XsXt]
            )
        data = resp.get('data', {}).get('items')
        for note in data:
            if note.get('hot_query'):
                continue
            else:
                yield self.parse_dict(note)

    @staticmethod
    def parse_dict(note: dict) -> NoteItem:
        id = note.get('id')
        note = note.get('note_card')
        user_name = note.get('user', {}).get('nick_name')
        if not user_name:
            user_name = note.get('user', {}).get('nickname')

        return NoteItem(
            note_id=id,
            note_type=note.get('type'),
            display_title=note.get('display_title'),
            note_cover=note.get('cover', {}).get('url'),
            liked_count=note.get('interact_info', {}).get('liked_count'),
            user_name=user_name,
            user_id=note.get('user', {}).get('user_id'),
            avatar=note.get('user', {}).get('avatar')
        )


if __name__ == "__main__":
    GetHomeFeed(0).start()
