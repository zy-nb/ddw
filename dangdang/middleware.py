from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):  # �Զ�����м��
    def __init__(self, get_response):  # ��ʼ��
        super().__init__(get_response)
        print("init1")

    # view��������ǰִ��
    def process_request(self, request):  # ĳһ��view
        login_status=request.session.get('login')
        if 'lok' in request.path:
            if not login_status:
                return redirect('loregapp:login')


    # ��process_request֮��View֮ǰִ��
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("view:", request, view_func, view_args, view_kwargs)

    # viewִ��֮����Ӧ֮ǰִ��
    def process_response(self, request, response):
        print("response:", request, response)
        return response  # ���뷵��response

    # ���View���׳����쳣
    def process_exception(self, request, ex):  # View�г����쳣ʱִ��
        print("exception:", request, ex)