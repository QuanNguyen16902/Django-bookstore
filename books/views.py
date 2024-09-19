from django.shortcuts import render, redirect,  get_object_or_404
import requests
from django.contrib import messages
from .forms import LoginForm

# Create your views here.
def index(request):
    return render(request, 'app2/index1.html')


import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Gửi yêu cầu đăng nhập đến API
            response = requests.post('http://localhost:8080/auth/login', json={
                'email': email,
                'password': password
            })

            data = response.json()

            if response.status_code == 200:
                # Lưu token vào session
                token = data.get('token')
                request.session['token'] = token

                # Lấy thông tin người dùng từ phản hồi đăng nhập
                user_id = data['user']['id']
                user_name = data['user']['username']
                request.session['currentUser'] = {
                    'id': user_id,
                    'username': user_name,
                    'email': data['user']['email']
                }

                # In ra token và thông tin người dùng để kiểm tra
                print(f"Token: {request.session.get('token')}")
                print(f"Current User: {request.session.get('currentUser')}")

                # Lấy thông tin chi tiết của người dùng qua API với id
                headers = {'Authorization': f'Bearer {token}'}
                user_response = requests.get(f'http://localhost:8080/api/users/{user_id}', headers=headers)

                if user_response.status_code == 200:
                    user_details = user_response.json()
                    # Cập nhật thêm thông tin người dùng chi tiết nếu cần
                    request.session['userDetails'] = user_details
                    messages.success(request, 'Login successful')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Failed to retrieve user information.')
            else:
                messages.error(request, data.get('message', 'Login failed'))
    else:
        form = LoginForm()

    return render(request, 'app2/login.html', {'form': form})


def logout(request):
    # Xóa token khỏi session
    request.session.pop('token', None)

    # Xóa bất kỳ thông tin người dùng nào khỏi session
    request.session.flush()

    # Hiển thị thông báo thành công
    messages.success(request, 'You have been logged out successfully.')

    # Chuyển hướng người dùng về trang login hoặc trang chính
    return render(request, 'app2/logout.html')


def dashboard(request):
    token = request.session.get('token')  # Lấy token từ session
    user_logged_in = False
    username = None
    books = []
    if token:
        user_logged_in = True
        username = request.session.get('userDetails')['username']
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get('http://localhost:8080/api/books', headers=headers)

            # Kiểm tra phản hồi từ API
            if response.status_code == 200:
                books = response.json()  # Lấy dữ liệu sách từ phản hồi API
            else:
                books = []  # Trường hợp không nhận được phản hồi thành công
                user_logged_in = False
                username = None
                messages.error(request, 'Failed to retrieve books from the server.')
        except requests.exceptions.RequestException as e:
            books = []  # Trường hợp có lỗi khi gửi yêu cầu đến API
            user_logged_in = False
            username = None
            messages.error(request, f'Error occurred while connecting to API: {e}')
    else:
        # Nếu không có token, chuyển hướng người dùng về trang đăng nhập
        messages.error(request, 'You must be logged in to view the dashboard.')
        return redirect('login')  # Thay 'login' bằng tên URL đăng nhập của bạn
    return render(request, 'app2/index1.html', {'books': books, 'user_logged_in': user_logged_in, 'username': username})


def book_detail(request, pk):
    token = request.session.get('token')
    if not token:
        return redirect('login')
    response = requests.get('http://localhost:8080/books/<:id>')
    book = response.json()
    return render(request, 'books/book_detail.html', {'book': book})
# @app.route('/add_product', methods=['POST'])
def add_book(request):
    if request.method == 'POST':
        data = {
            'title': request.POST['title'],
            'author': request.POST['author'],
            'price': request.POST['price'],
            'stock': request.POST['stock']
        }
        response = requests.post('http://localhost:3000/books/add', json=data)
        return redirect('book_list')
    return render(request, 'app2/books/add.html')
