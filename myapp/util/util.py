from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)


"""
我们也可以按照自己的需求打造自定义的转换器。 Reddit - 一个知名的链接分享网站 - 用户在此可以创建和管理基于主题和链接分享的社区。 比如/r/python和/r/flask，分别由URLreddit.com/r/python和reddit.com/r/flask表示。 Reddit有一个有趣的特性是，通过在URL中用一个+隔开各个社区名，你可以同时看到来自多个社区的帖子。比如reddit.com/r/python+flask。

我们可以使用一个自定义转换器来实现这种特性。 我们可以接受由加号隔离开来的任意数目参数，通过我们的ListConverter转换成一个列表，并传递给视图函数。

"""
