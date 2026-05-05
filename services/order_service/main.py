from fastapi import FastAPI
import grpc

import payment_pb2
import payment_pb2_grpc

app = FastAPI()


def call_payment_service(order_id: str, amount: float):
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = payment_pb2_grpc.PaymentServiceStub(channel)

        response = stub.ProcessPayment(
            payment_pb2.PaymentRequest(
                order_id=order_id,
                amount=amount
            ),
            timeout=2
        )

        return response.status

    except Exception as e:
        return f"ERROR: {str(e)}"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/order")
def create_order():
    order_id = "123"
    amount = 100

    payment_status = call_payment_service(order_id, amount)

    return {
        "order_id": order_id,
        "payment_status": payment_status
    }