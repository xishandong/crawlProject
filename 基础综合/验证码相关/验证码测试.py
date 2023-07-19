import ddddocr

ocr = ddddocr.DdddOcr()
# 简单的图片数字英文识别
with open('1.png', 'rb') as f:
    img_bytes = f.read()
res = ocr.classification(img_bytes)

print(res)