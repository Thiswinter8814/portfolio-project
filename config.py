
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드
load_dotenv()

class Config:
    """기본 설정 클래스"""
    # 데이터베이스 설정
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # JWT 시크릿 키는 .env 파일에서 불러옴
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    """개발 환경 설정 클래스"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///development.db')

class ProductionConfig(Config):
    """운영 환경 설정 클래스"""
    DEBUG = False
    # 운영 환경에서는 보통 PostgreSQL, MySQL 등 다른 DB를 사용
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# 어떤 설정을 사용할지 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
