# QProjectPython
Collection Server 와 API Server 를 위한 Python 프로젝트 입니다.
2022-01-13 이 프로젝트는 공용 프로젝트 입니다!!!!
[FastAPI참고]
https://github.com/riseryan89/notification-api

### TO DO
1. python -m venv venv : 가상환경 설정
2. .\venv\Scripts\activate.ps1 : 가상환경 활성화 
    $ source venv/bin/activate : Termux
    (* [Powershell] Set-ExcutionPolicy RemoteSigned : Powershell인 경우 RemoteSigned 설정을 해야 가상환경을 활성화 할 수 있다.)
3. pip install -r requirements.txt : txt파일에 서술된 pkg 항목을 설치
    (* pip freeze : 설치 된 pkg 항목을 표기)


### Issues
1. import 경로 문제로 인하여 해당 내용 삽입
    - import sys, os
    - sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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


### Authrization 형태
- Authorization: <type> <credentials> (일반적으로 사용)
1. Basic : 사용자 아이디와 암호를 Base64 로 인코딩한 값을 토큰으로 사용
2. Bearer : JWT 또는 OAuth 에 대한 토큰을 사용
3. Digest : 서버에서 난수 데이터 문자열을 클라이언트에 보내고, 클라이언트는 사용자 정보와 nonce 를 포함하는 해시값을 사용하여 응답
4. HOBA : 전자 서명 기반 인증
5. Mutual : 암호를 이용한 클라이언트-서버 상호 인증
6. AWS4-HMAC-SHA256 : AWS 전자 서명 기반 인증


### sys 사용이유
1. sys.dont_write_bytecode = True : ByteCode를 만들지 안도록 하여 폴더 가시성 향상 (__pycache__) 
2. sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) : 절대경로를 프로젝트 폴더 기준으로 설정