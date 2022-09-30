from .models import UserLog


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("one time  Intialization")

    def __call__(self, request):
        print("this is  before view")
        response = self.get_response(request)
        self.user_log(request)
        print("this is  after view")
        return response

    def user_log(self, request):
        user_data = UserLog.objects.filter(
            request_method=request.method, request_url=request.get_full_path())
        # _get_full_path:<bound method HttpRequest._get_full_path of <WSGIRequest: POST '/user/register/'>>
        # method:'POST'
        if not user_data.exists():
            UserLog.objects.create(request_method=request.method,
                                   request_url=request.get_full_path())
        else:
            user = user_data.first()
            user.save()
