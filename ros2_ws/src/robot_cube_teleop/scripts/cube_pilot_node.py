#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pymavlink import mavutil
import time

class CubePilotTeleopNode(Node):
    def __init__(self):
        super().__init__('cubepilot_teleop_node')

        # 1. Conexión MAVLink
        self.get_logger().info('Conectando al CubePilot por /dev/ttyACM0...')
        self.master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)
        self.master.wait_heartbeat()
        self.get_logger().info('CubePilot conectado. Armando motores...')

        # 2. Armar el sistema
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0
        )
        time.sleep(1)
        self.get_logger().info('¡Sistema Armado! Escuchando comandos en /cmd_vel...')

        # 3. Suscriptor al tópico /cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Máxima potencia que se sumará/restará a los 1500 (equivale a tu potencia = 400)
        self.max_pwm_offset = 400

    def cmd_vel_callback(self, msg):
        # Extraer velocidad lineal (adelante/atrás) y angular (giros)
        linear = msg.linear.x
        angular = msg.angular.z

        # Lógica de mezcla diferencial (basada en tu código donde CH3 está invertido)
        # linear > 0 es Adelante (W)
        # angular > 0 es Izquierda (A)
        offset_1 = (linear) - (angular)
        offset_3 = (-linear) - (angular)

        # teleop_twist_keyboard envía valores decimales (ej. 0.5), los multiplicamos por nuestra potencia máxima
        pwm1 = 1500 + int(offset_1 * self.max_pwm_offset)
        pwm3 = 1500 + int(offset_3 * self.max_pwm_offset)

        # Limitar por seguridad para que nunca pase de 1100 o 1900
        pwm1 = max(1100, min(1900, pwm1))
        pwm3 = max(1100, min(1900, pwm3))

        self.enviar_pwm(pwm1, pwm3)

    def enviar_pwm(self, pwm1, pwm3):
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, pwm1, 0, 0, 0, 0, 0
        )
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 3, pwm3, 0, 0, 0, 0, 0
        )

    def destroy_node(self):
        # Asegurarnos de detener los motores y desarmar al presionar Ctrl+C
        self.get_logger().info('Apagando motores y desarmando sistema...')
        self.enviar_pwm(1500, 1500)
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0
        )
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CubePilotTeleopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()