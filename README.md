# QProjectPython
Collection Server 와 API Server 를 위한 Python 프로젝트 입니다.

[FastAPI참고]
https://github.com/riseryan89/notification-api

### TO DO
1. python -m venv venv : 가상환경 설정
2. .\venv\Scripts\activate.ps1 (윈도우) / $ source venv/bin/activate (Linux)
    (* [Powershell] Set-ExcutionPolicy RemoteSigned : Powershell인 경우 RemoteSigned 설정을 해야 가상환경을 활성화 할 수 있다.)
3. pip install pip --upgrade
4. pip install -r requirement.txt : txt파일에 서술된 pkg 항목을 설치
    (* pip freeze : 설치 된 pkg 항목을 표기)
5. cd APIServer or CollectionServer > python main.py


### Install Pkg 설명
1. fastapi : api Framework(?)
2. uvicorn : webserver Framework(?)
3. PyJWT : Json Web Token
4. bcrypt : Encryption
5. sqlalchemy : Data base Orm
6. pymysql : mysql driver(?)


### Error Code
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method not allowed
500 Internal Error
502 Bad Gateway 
504 Timeout
