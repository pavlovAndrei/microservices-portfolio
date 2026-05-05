import grpc
from concurrent import futures
import time

import payment_pb2
import payment_pb2_grpc


class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    def ProcessPayment(self, request, context):
        print(f"Processing payment for order {request.order_id}, amount={request.amount}")

        if request.amount > 1000:
            status = "FAILED"
        else:
            status = "SUCCESS"

        return payment_pb2.PaymentResponse(status=status)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Payment gRPC server running on port 50051")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()