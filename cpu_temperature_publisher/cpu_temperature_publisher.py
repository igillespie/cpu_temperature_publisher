import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32  # Standard message type for floating-point numbers

class CPUTemperaturePublisher(Node):
    def __init__(self):
        super().__init__('cpu_temperature_publisher')
        self.publisher_ = self.create_publisher(Float32, 'cpu_temperature', 10)
        self.timer = self.create_timer(1.0, self.publish_cpu_temperature)  # Publish every second
        self.get_logger().info("CPU Temperature Publisher Node has been started.")

    def get_cpu_temperature(self):
        try:
            # Read the CPU temperature from the system file
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp_str = f.read().strip()
                # Convert millidegrees Celsius to degrees Celsius
                temperature = float(temp_str) / 1000.0
                return temperature
        except Exception as e:
            self.get_logger().error(f"Failed to read CPU temperature: {e}")
            return None

    def publish_cpu_temperature(self):
        temperature = self.get_cpu_temperature()
        if temperature is not None:
            msg = Float32()
            msg.data = temperature
            self.publisher_.publish(msg)
            #self.get_logger().info(f"Published CPU Temperature: {temperature:.2f}°C")

def main(args=None):
    rclpy.init(args=args)
    node = CPUTemperaturePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()