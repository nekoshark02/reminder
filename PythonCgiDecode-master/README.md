# PythonCgiDecode
Python用のCGIデコード。PHP風にデータを扱えるようにします。

    import cgi_decode
    q = cgi_decode.Set()
    # GET,POST,COOKIE,FILES が使えるように
---
+ ファイルは一時ファイルとして/tmp/に保存されます
+ FILES にはファイル情報のみが入っています
+ ファイルはチェック後、移動してください
---
    for i,f in enumerate(FILES):

        # f['name'] form name
        # f['type'] file type
        # f['up_name'] upload file name
        # f['tmp_name'] /tmp/*****
        new_name = q.move(f,'save_name')

---
さらに詳しくは下記に掲載しています  
https://code-notes.com/lesson/20
---
This software is released under the MIT License, see LICENSE.txt.
