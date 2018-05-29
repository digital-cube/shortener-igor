#!/usr/bin/env python3
import tornado.ioloop
import json
import random
import tornado.web
from singleton_decorator import singleton

@singleton
class MyDB:

    def __init__(self):
        self.load_db()
#        print("sadrzaj baze je:",self.db)
        
    def load_db(self):
        try:
            with open('db.json','rt') as f:
                self.db = json.load(f)
        except:
            self.db = {}

    def save_db(self):
        try:
            with open('db.json','wt') as f:
                json.dump(self.db, f)
            return True
                
        except Exception as e:
            print(e)
            return False
        
        
    def gen_id(self):
        for retries in range(0,10):
            _id = str(random.randint(100000000,999999999))
#            _id = str(random.randint(1,5))

            if _id not in self.db:
                break
        
        if _id in self.db:
            return False        
        
        return _id
    
    def get(self, _id):

        return self.db[_id] if _id in self.db else False    
    
    def put(self, url):
        
        _id = self.gen_id()
        
        if not _id:
            return False
        
        self.db[_id] = url
        self.save_db()

        return _id
        

class RedirectHandler(tornado.web.RequestHandler):
    def get(self, _id):
        db = MyDB()
        url = db.get(_id)
        if not url:
            self.set_status(400)
            self.write(json.dumps({'error': 'not found'}))
            return
        
        self.redirect(url)

class SaveHandler(tornado.web.RequestHandler):

    def put(self):
        
        url = json.loads(self.request.body.decode('utf-8'))['url']
        
        db = MyDB()
        
        _id = db.put(url)
        
        if not _id:
            self.set_status(400)
            self.write(json.dumps({'error': 'error generating id'}))
            return
        
        print("URL",url)        

        self.write(json.dumps({'id':_id}))

def make_app():
    return tornado.web.Application([
        (r"/", SaveHandler),
        (r"/r/(.*)",RedirectHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(6555)
    tornado.ioloop.IOLoop.current().start()

