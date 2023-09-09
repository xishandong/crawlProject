def add_cookie(request):
    # 这个中间件是用来添加cookie的，注意此处的cookie需要和js补环境的cookie一致
    request.cookies = {

    }

    return request
