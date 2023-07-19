from lxml import etree

if __name__ == "__main__":
    # 实例化一个etree对象
    tree = etree.parse('./test.html')
    #  r = tree.xpath('/html//title')
    # r = tree.xpath('//div[@class="song"]')
    # r = tree.xpath('//div[@class="song"]/p[3]')
    # r = tree.xpath('//div[@class="tang"]/ul/li[4]/a/text()')
    # r = tree.xpath('//div[@class="tang"]//text()')
    # r = tree.xpath('//div[@class="song"]/img/@src')
    r = tree.xpath('//div[@class="song"]/p/text()')
    print(r)
