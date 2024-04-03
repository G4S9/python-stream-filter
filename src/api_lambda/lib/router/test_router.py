import unittest

from .router import Router


class RouterTestCase(unittest.TestCase):
    def setUp(self):
        self.default_result = "default_result"
        self.default_route = lambda: self.default_result
        self.router = Router(self.default_route)

    def test_set_and_get_route(self):
        path = "/test"
        method = "GET"
        target = "test_handler"

        self.router.set(path, method, target)
        retrieved_target = self.router.get(path, method)
        self.assertEqual(retrieved_target, target)

    def test_default_route_returned_for_nonexistent_route(self):
        non_existent_path = "/does_not_exist"
        method = "GET"
        retrieved_target = self.router.get(non_existent_path, method)
        self.assertEqual(retrieved_target, self.default_route)

    def test_set_and_get_multiple_routes(self):
        routes = [
            ("/home", "GET", "home_handler"),
            ("/about", "GET", "about_handler"),
            ("/contact", "POST", "contact_handler"),
        ]

        for path, method, target in routes:
            self.router.set(path, method, target)

        for path, method, target in routes:
            retrieved_target = self.router.get(path, method)
            self.assertEqual(retrieved_target, target)
