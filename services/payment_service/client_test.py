import grpc
import payment_pb2
import payment_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = payment_pb2_grpc.PaymentServiceStub(channel)

    response = stub.ProcessPayment(
        payment_pb2.PaymentRequest(order_id="123", amount=100)
    )

    print("Payment response:", response.status)


if __name__ == "__main__":
    run()