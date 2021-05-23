from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os


class TempCreateView(APIView):
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            name = data['name'] 
            print("======= TempCreateView API =========")
            print(name)
            return Response({'success':'success'})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})