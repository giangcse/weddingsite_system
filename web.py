import pandas as pd
import json
import os
import uvicorn
import sqlite3

# from starlette.requests import Request
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.requests import Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

class Website:
    def __init__(self) -> None:
        '''
        HÀM KHỞI TẠO
        ------
        Khởi tạo API
        '''
        self.app = FastAPI()
        self.app.mount("/statics", StaticFiles(directory="statics"), name="statics")
        self.templates = Jinja2Templates(directory="templates/")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        # Connect to SQLite database
        self.database = 'database.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()
        # Trang chủ
        @self.app.get('/')
        async def index(request: Request, id: Union[str, None] = None):
            if id != '':
                try:
                    result = self.cursor.execute('SELECT * FROM data WHERE ID = ?', (id,))
                    data = result.fetchall()[0]

                    return self.templates.TemplateResponse('index.html', context={'request': request, "data": {"call": data[1], "name": data[0], "time": data[2], "date": data[3]}})
                except Exception:
                    return self.templates.TemplateResponse('index.html', context={'request': request})
            else:
                return self.templates.TemplateResponse('index.html', context={'request': request})


web = Website()

if __name__=="__main__":
    # config = uvicorn.Config("web:web.app", host="0.0.0.0", port=88)
    # server = uvicorn.Server(config)
    # server.run()
    uvicorn.run("web:web.app", host='0.0.0.0')