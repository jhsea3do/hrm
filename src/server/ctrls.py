from flask import Blueprint, url_for

js = Blueprint('js', __name__, \
    static_url_path='js',  \
    static_folder="../public/js" \
)

public = Blueprint('public', __name__, \
    static_url_path='',  \
    static_folder="../public" \
)

main = Blueprint('main', __name__, \
    template_folder="templates" \
)

@main.route("/")
def index():
    return public.send_static_file('index.html')

@main.route("/login")
def login(): pass
