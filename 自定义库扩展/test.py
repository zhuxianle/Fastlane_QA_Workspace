#!/usr/bin/python
#coding=utf-8
s ='E:\\Work_Space\\SVN_SPACEWORK\\\xd7\xd4\xb6\xa8\xd2\xe5\xbf\xe2\xc0\xa9\xd5\xb9\\AppiumLibrary\xbf\xe2\xc0\xa9\xd5\xb9/keywords'
ss = s.encode('raw_unicode_escape')
print(ss)  # 结果：b'\xe9\x9d\x92\xe8\x9b\x99\xe7\x8e\x8b\xe5\xad\x90'
sss = ss.decode()
print(sss)
