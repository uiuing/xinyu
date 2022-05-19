import json


def parser_post(request):
    """
    解析post请求
    :param request: 请求
    :return: 返回解析后的json数据
    """
    return json.loads(request.get_data(as_text=True))
