# -*- coding: utf-8 -*-
from distutils.core import setup
LONGDOC = """
AutoBaiduMachine
=====

自动百度机
让机器学会百度

完整文档见 ``README.md``

GitHub: https://github.com/qiqipipioioi/AutoBaiduMachine


安装说明
========

python2.7通过测试

-  半自动安装：先下载 https://pypi.python.org/pypi/jieba/ ，解压后运行
   python setup.py install
-  手动安装：将 jieba 目录放置于当前目录或者 site-packages 目录
-  通过 ``import AutoBaiduMachine`` 来引用

"""

setup(name='AutoBaiduMachine',
      version='0.1',
      description='Let Machine baidu automatically',
      long_description=LONGDOC,
      author='Tu, Xun',
      author_email='qiqipipioioi@qq.com',
      url='https://github.com/qiqipipioioi/AutoBaiduMachine',
      license="MIT",
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='auto, baidu',
      packages=['AutoBaiduMachine'],
      package_dir={'AutoBaiduMachine':'AutoBaiduMachine'},
      package_data={'AutoBaiduMachine':['AutoBaidu.py','__init__.py','hanzi2pinyin.txt','pinyin.txt','stopword.data']}
)
