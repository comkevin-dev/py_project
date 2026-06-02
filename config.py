import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DB_PATH    = os.path.join(os.path.dirname(__file__), 'portfolio.db')

PROJECTS = [
    {
        'title': 'AI Chatbot',
        'description': 'OpenAI API 기반 챗봇 시스템 구축',
        'tech': ['Python', 'Flask', 'OpenAI API'],
        'github': '#',
    },
    {
        'title': 'Vision AI',
        'description': '이미지 인식 기반 분석 시스템',
        'tech': ['Python', 'TensorFlow', 'OpenCV'],
        'github': '#',
    },
    {
        'title': 'Data Dashboard',
        'description': 'Python 데이터 자동 분석 플랫폼',
        'tech': ['Python', 'Pandas', 'Matplotlib'],
        'github': '#',
    },
]

SKILLS = ['Python', 'Flask', 'AI / ML', 'TensorFlow', 'OpenAI API', 'Data Analysis']

PROFILE = {
    'name': 'Your Name',
    'email': 'example@gmail.com',
    'github': 'github.com/example',
}
