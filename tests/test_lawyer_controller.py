import dataclasses
import json
from datetime import date, time

from app.controllers import LawyerController
from app.repositories import LawyerRepository
from app.schema.lawyer_schema import LawyerSchema, LawyerReadSchema, \
    LawyerCreateSchema
from app.services import RedisService
from tests import BaseTestCase
import pytest



class TestLawyerController(BaseTestCase):

    lawyer_repository = LawyerRepository(redis_service=RedisService);
    the_test_lawyer_controller = LawyerController(lawyer_repository)
    the_expected_service_result_response = None


    # Test Case #1 - Test that create method in lawyer controller can create lawyer.
    # Expected Result: create method must return true for a successful lawyer creation
    @pytest.mark.lawyer_controller
    def test_create(self):
       # incoming json data from admin.
       test_data = {
               "id": 10,
               "name": "John Doe",
               "username": "jdoe",
               "email": "jdoe@gmail.com",
               "password": "welcome",
           }
       admin_id = 2;
       the_expected_service_result_response = True # for a create in lawyer controller method, service result must say True.
       the_test_lawyer_controller_create_response = self.the_test_lawyer_controller.create(data=test_data,id=admin_id); # call the create method in the LawyerController
       self.assertTrue(the_test_lawyer_controller_create_response.success, the_expected_service_result_response); # confirm that the service result of True is True

    # Test Case #2 - Test that index method in lawyer controller can retrieve all lawyer details.
    # Expected Result: index method must return true for a successful retrieval
    @pytest.mark.lawyer_controller
    def test_index(self):
        the_expected_service_result_response = True # for an index into the db, service result returns True.
        the_test_lawyer_controller_index_response = self.the_test_lawyer_controller.index() # call the index method in the LawyerController
        self.assertTrue(the_test_lawyer_controller_index_response.success,the_expected_service_result_response) # confirm that the service result of True is True

    # Test Case #3 - Test that find method in lawyer controller can find lawyer details
    # Expected Result: find method must return true for a successful query.
    @pytest.mark.lawyer_controller
    def test_find(self):
        lawyer_id = 1 # id of 1 from testing environment setup i.e file db. # self.test_data["id"] # id of 10 from test_data model
        the_expected_service_result_response = True # for a find into the db, service result should return true.
        the_test_lawyer_controller_find_response = self.the_test_lawyer_controller.find_by_id(obj_id=lawyer_id)
        self.assertTrue(the_test_lawyer_controller_find_response.success, the_expected_service_result_response)

    # Test Case #4 - Test that delete method in lawyer controller can delete a lawyer by ID
    # Expected Result: delete method must return true for a successful query.
    @pytest.mark.lawyer_controller
    def test_delete(self):
        lawyer_id = 1 # id of 1 from testing environment setup i.e file db.
        the_expected_service_result_response = True # for a delete into the db, service result should return true.
        the_test_lawyer_controller_delete_response = self.the_test_lawyer_controller.delete(obj_id=lawyer_id)
        self.assertTrue(the_test_lawyer_controller_delete_response.success, the_expected_service_result_response)



