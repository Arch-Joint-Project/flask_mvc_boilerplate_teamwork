# local imports
from app.definitions.service_result import handle_result
from app.controllers import BillController
from app.repositories import BillRepository

# third party imports
import pinject
from flask import Blueprint

account = Blueprint("account", __name__)

obj_graph = pinject.new_object_graph(modules=None,
                                     classes=[BillController,
                                              BillRepository])

bill_controller = obj_graph.provide(BillController)


# customer_controller = CustomerController(CustomerRepository)


@account.route("/invoice/<company>", methods=["GET"])
def invoice(company):
    data = bill_controller.generate_invoice({"company": company})
    return handle_result(data)
