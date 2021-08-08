"""
cgi_decode.py

Copyright (c) [2018] [code-notes.com]

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

import os
import re
import sys
import tempfile

class Set:

    def __init__(self):

        __builtins__['POST'] = {}
        __builtins__['FILES'] = []

        if os.environ.get('REQUEST_METHOD')=='POST':

            m = re.search("multipart/form-data; boundary=(.+)", os.environ.get('CONTENT_TYPE'))
            if m:
                __builtins__['POST'] = self.__multipart(m.group(1))
            else:
                __builtins__['POST'] = self.__decode(sys.stdin.read())

        __builtins__['GET'] = self.__decode(os.environ.get('QUERY_STRING'))
        __builtins__['COOKIE'] = self.__decode(os.environ.get('HTTP_COOKIE'), '; ')


    def __decode(self, buf, de='&'):

        h = {}
        buf = bytes(buf.encode('utf-8'))

        r1 = re.compile(b'([^=]+)=([^=]*)')
        r2 = re.compile(b'\+')
        r3 = re.compile(b'%([a-fA-F0-9][a-fA-F0-9])')

        for v in buf.split(bytes(de.encode('utf-8'))):

            if v==b'':
                continue

            m = re.search(r1,v)
            if m:
                (key,val) = (m.group(1),m.group(2))
            else:
                (key,val) = (v,b'')

            key = re.sub(r2,b' ',key)
            if sys.version_info[0]==3:
                key = re.sub(r3,lambda x:bytes([int(x.group(1),16)]),key).decode('utf-8')
            else:
                key = re.sub(r3,lambda x:chr(int(x.group(1),16)),key)

            val = re.sub(r2,b' ',val)
            if sys.version_info[0]==3:
                val = re.sub(r3,lambda x:bytes([int(x.group(1),16)]),val).decode('utf-8')
            else:
                val = re.sub(r3,lambda x:chr(int(x.group(1),16)),val)

            self.__setHash(key,val,h)

        return h


    def __setHash(self, k, v, h):

        if k in h:
            if isinstance(h[k], list):
                h[k].append(v)
            else:
                h[k] = [h[k],v]
        else:
            h[k] = v


    def __multipart(self, bound):

        (key,fi,ty) = ('','','')
        val = []
        h = {}
        f = []
        rec = 0

        r1 = re.compile(bytes(bound.encode('utf-8')))
        r2 = re.compile(b'\r\n$')
        r3 = re.compile(b'Content-Disposition: form-data; name="([^"]+)"; filename="([^"]+)"')
        r4 = re.compile(b'Content-Disposition: form-data; name="([^"]+)"')
        r5 = re.compile(b'Content-Type: (.+)')
        r6 = re.compile(b'\A\r\n\Z')

        for li in sys.stdin.buffer if sys.version_info[0]==3 else sys.stdin:

            if re.search(r1,li):

                if key!='':

                    val = re.sub(r2,b'',b''.join(val))

                    if fi!= '':
                        tf = tempfile.NamedTemporaryFile(delete=False)
                        tf.write(val)
                        f.append({
                            'name':key.decode('utf-8'),
                            'up_name':fi.decode('utf-8'),
                            'type':ty.decode('utf-8'),
                            'tmp_name':tf.name
                            })
                        fi = ''
                        ty = ''

                    else:
                        self.__setHash(key.decode('utf-8'), val.decode('utf-8'), h)

                key = ''
                val = []
                rec = 0
                continue

            if(rec==1):
                val.append(li)
                continue

            m = re.search(r3,li)
            if m:
                key = m.group(1)
                fi = m.group(2)
                continue

            m = re.search(r4,li)
            if m:
                key = m.group(1)
                continue

            m = re.search(r5,li)
            if m:
                ty = m.group(1).rstrip()
                continue

            if rec==0:
                m = re.search(r6,li)
                if m:
                    rec = 1

        __builtins__['FILES'] = f

        return h


    def move(self,f,name):

        if not 'tmp_name' in f or not os.path.isfile(f['tmp_name']) or name=='':
            return 0

        with open(name,'wb') as nf:
            with open(f['tmp_name'],'rb') as tf:
                data = tf.read()

            nf.write(data)
            os.remove(f['tmp_name'])

            return name

        return 0


    def clear(self):

        for f in FILES:
            if os.path.isfile(f['tmp_name']):
                os.remove(f['tmp_name'])
