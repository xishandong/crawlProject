from typing import TypedDict, Literal


class QueryTopicNote(TypedDict):
    """
    话题请求类型
    """
    page_size: int  # 每页大小
    sort: Literal['hot', 'time']  # 话题类型
    page_id: str  # 话题的id
    cursor: str  # 话题位移
    sid: str  # 暂时不清楚


class QueryHomeFeedNote(TypedDict):
    """
    首页请求类型
    """
    category: Literal[
        'homefeed_recommend', 'homefeed.fashion_v3', 'homefeed.food_v3', 'homefeed.cosmetics_v3',
        'homefeed.movie_and_tv_v3', 'homefeed.career_v3', 'homefeed.love_v3',
        'homefeed.household_product_v3','homefeed.gaming_v3', 'homefeed.travel_v3', 'homefeed.fitness_v3'
    ]
    cursor_score: str
    num: int
    refresh_type: int
    note_index: Literal[29]
    unread_begin_note_id: Literal['']
    unread_end_note_id: Literal['']
    unread_note_count: Literal[0]


class QueryUserInfo(TypedDict):
    """
    用户信息请求类型
    """
    pass


class QueryNoteDetail(TypedDict):
    """
    笔记详情请求类型
    """
    pass


class QueryUserNote(TypedDict):
    """
    用户笔记请求类型
    """
    pass


class QueryNoteComment(TypedDict):
    """
    笔记评论请求类型
    """
    note_id: str
    cursor: str


class QueryNoteSubComment(TypedDict):
    """
    笔记评论请求类型
    """
    note_id: str
    cursor: str
    root_comment_id: str
    num: str
