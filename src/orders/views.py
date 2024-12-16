import json
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.converters import convert_data_from_request_to_dto
from common.errors import InvalidNumberParametersError, WrongParameterTypeError
from orders.business_logic.dto import OrderDTO
from orders.business_logic.orders import create_order
from robots.business_logic.services import get_robots_by_serial


@method_decorator(csrf_exempt, name="dispatch")
class OrdersView(View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = json.loads(request.body)
        try:
            data["customer_id"] = request.user.pk
            order_dto = convert_data_from_request_to_dto(dto=OrderDTO, data_from_request=data)
            order = create_order(data=order_dto)
            if not get_robots_by_serial(serial=order.serial, is_active=True):
                order.is_waiting = True
                order.save()

            return HttpResponse(content={"id": order.pk, "robot_serial": order.serial}, status=200)
        except InvalidNumberParametersError:
            return HttpResponseBadRequest(content="Invalid number of parameters to create a robot instance.")
        except WrongParameterTypeError:
            return HttpResponseBadRequest(content="Invalid type of parameters.")
