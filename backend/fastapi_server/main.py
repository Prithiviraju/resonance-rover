from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/telemetry")
def get_telemetry():
    return {
        "battery_voltage": 24.2,
        "current_draw_amps": 4.5,
        "system_status": "nominal",
        "timestamp": time.time()
    }

@app.post("/move")
def control_rover(linear_velocity: float, angular_velocity: float):
    return {
        "status": "command_executed",
        "linear_velocity": linear_velocity,
        "angular_velocity": angular_velocity
    }