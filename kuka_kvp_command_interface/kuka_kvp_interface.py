import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import socket
from collections import deque
import time
import numpy



# TODO: Refactor KUKA class into its own file
ROBOT_IP = '172.31.1.147'
KVP_JOINT_COMMAND_VARIABLE = 'COM_E6AXIS'
KVP_LIN_COMMAND_VARIABLE = 'WAAM_POS'
KVP_ROBOT_POSITION_VARIABLE = '$POS_ACT'
KVP_PROGRAM_SPEED_VARIABLE = '$OV_PRO' # Percentage of maximum speed
KVP_LINEAR_VELOCITY_VARIABLE = 'WAAM_VEL'
KVP_LINEAR_ACCELERATION_VARIABLE = 'WAAM_ACC'

SEND_DELAY = 0.8 # seconds
ACCEPTABLE_ERROR = 0.01 # mm

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# Initializing client connection

class KUKA(object):

    def __init__(self, TCP_IP):
        try: 
            client.connect((TCP_IP, 7000))                      # Open socket. kukavarproxy actively listens on TCP port 7000
        except: 
            self.error_list(1)


    def send (self, var, val, msgID):
        """
        kukavarproxy message format is 
        msg ID in HEX                       2 bytes
        msg length in HEX                   2 bytes
        read (0) or write (1)               1 byte
        variable name length in HEX         2 bytes
        variable name in ASCII              # bytes
        variable value length in HEX        2 bytes
        variable value in ASCII             # bytes
        """
        try:
            msg = bytearray()
            temp = bytearray()
            if val != "":
                val = str(val)
                msg.append((len(val) & 0xff00) >> 8)            # MSB of variable value length
                msg.append((len(val) & 0x00ff))                 # LSB of variable value length
                msg.extend(map(ord, val))                       # Variable value in ASCII
            temp.append(bool(val))                              # Read (0) or Write (1)
            temp.append(((len(var)) & 0xff00) >> 8)             # MSB of variable name length
            temp.append((len(var)) & 0x00ff)                    # LSB of variable name length
            temp.extend(map(ord, var))                          # Variable name in ASCII 
            msg = temp + msg
            del temp[:]
            temp.append((msgID & 0xff00) >> 8)                  # MSB of message ID
            temp.append(msgID & 0x00ff)                         # LSB of message ID
            temp.append((len(msg) & 0xff00) >> 8)               # MSB of message length
            temp.append((len(msg) & 0x00ff))                    # LSB of message length
            msg = temp + msg
        except :
            self.error_list(2)
        try:
            client.send(msg)
            return  client.recv(1024)                           # Return response with buffer size of 1024 bytes
        except :
            self.error_list(1)


    def __get_var(self, msg):
        """
        kukavarproxy response format is 
        msg ID in HEX                       2 bytes
        msg length in HEX                   2 bytes
        read (0) or write (1)               1 byte
        variable value length in HEX        2 bytes
        variable value in ASCII             # bytes
        Not sure if the following bytes contain the client number, or they're just check bytes. I'll check later.
        """
        try:
            lsb = int( msg[5])
            msb = int( msg[6])
            lenValue = (lsb <<8 | msb)
            return str(msg [7: 7+lenValue],'utf-8')  

        except:
            self.error_list(2)

    def read (self, var, msgID=0):
        try:
            return self.__get_var(self.send(var,"",msgID))  
        except :
            self.error_list(2)


    def write (self, var, val, msgID=0):
        try:
            if val != (""): return self.__get_var(self.send(var,val,msgID))
            else: raise self.error_list(3)
        except :
            self.error_list(2)


    def disconnect (self):
            # CLose socket
            client.close()


    def error_list (self, ID):
        if ID == 1:
            print ("Network Error (tcp_error)")
            print ("    Check your KRC's IP address on the network, and make sure the KVP Server is running.")
            self.disconnect()
            raise SystemExit
        elif ID == 2:
            print ("Python Error.")
            print ("    Update your python version >= 3.8.x.")
            self.disconnect()
            raise SystemExit
        elif ID == 3:
            print ("Error in write() statement.")
            print ("    Variable value is not defined.")
    

robot = KUKA(ROBOT_IP)




# Define Custom Buffer
class CoordinateQueue:
    def __init__(self, *elements):
        self._elements = deque(elements)
        self._counter = 0

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        self._counter += 1
        return self._elements.popleft()
    
    def peek(self):
        return self._elements[0]
    
    def counter(self):
        return self._counter


coordinate_queue = CoordinateQueue()

def format_joint_states(joint_states: list):
    
    if joint_states:
        a1 = joint_states[0]
        a2 = joint_states[1]
        a3 = joint_states[2]
        a4 = joint_states[3]
        a5 = joint_states[4]
        a6 = joint_states[5]
        
        formatted_joint_state = "{E6AXIS: A1 " + f"{a1}," + " A2 " + f"{a2}," + " A3 "+f"{a3}," + " A4 " + f"{a4}," + " A5 " + f"{a5}," + " A6 " + f"{a6}," + " E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}"
        
        return formatted_joint_state

    else:
        print("No data")



def format_linear_position(position: list, rotation: list):
    
    # assume both position and rotation are given
    if position:
        X = position.x
        Y = position.y
        Z = position.z
        
        A = rotation.x
        B = rotation.y
        C = rotation.z

        # NOTE: This is an acceptable sin for now. Encode velocity in orientation information (For synchronization purposes)
        received_message = rotation.w


        # Extract torch action
        received_torch_action = received_message - 1
        
        # Extract velocity
        linear_velocity = abs(received_torch_action)

        if received_torch_action >= 0:
            formatted_torch_action = "ON"
        elif received_torch_action < 0:
            formatted_torch_action = "OFF"
        
        # Default to Torch OFF (Safety Approach)
        else:
            formatted_torch_action = "OFF"
        
        formated_linear_position = "{POS: X " + f"{X}," + " Y " + f"{Y}," + " Z "+f"{Z}," + " A " + f"{A}," + " B " + f"{B}," + " C " + f"{C}" + "}"
        
        
        # print(f"formated_linear_position - (torch_action): {formated_linear_position} - ({formatted_torch_action})")
        return (formated_linear_position, linear_velocity, formatted_torch_action)

    else:
        print("No data")



def radians_to_degrees(joint_states: list):
    degrees_list = []
    
    for index, i in enumerate(joint_states):
        degrees_list.append(round(i * 57.2957795, 6))
        
    return degrees_list



# Callback function; sends data from the subscribed topic to the robot
def joint_command_callback_fn(subscribedData):
    
    joint_info = subscribedData
    print(f'Received joint_info: {joint_info}')
    
    joint_positions = subscribedData.position
    joint_position_degrees = radians_to_degrees(joint_positions)
    print(f'joint_position_degrees: {joint_position_degrees}')
    
    
    joint_states = format_joint_states(joint_position_degrees)
    # joint_states = "{E6AXIS: A1 0.3618088, A2 -103.051071, A3 101.322342, A4 -87.7924, A5 5.59045029, A6 -2.81264663, E1 0.0, E2 0.0, E3 0.0, E4 0.0, E5 0.0, E6 0.0}"
    
    
    robot.write(KVP_JOINT_COMMAND_VARIABLE, joint_states)
    print(f'Sending to robot (joint_info): {joint_states}')


def format_actual_robot_position(robot_position) -> str:
    
    print(f'robot_position to format (robot_position): {robot_position}')
    
    reduced_position = robot_position.split(', ')[:6]
    print(f'reduced_position: {reduced_position}')
    
    clean_reduced_position = [round(float(pos.split(" ")[-1].strip("}")),3) for pos in reduced_position]
    print(f'clean_reduced_position: {clean_reduced_position}')
    
        
    formatted_position = "{POS: X " + f"{clean_reduced_position[0]}," + " Y " + f"{clean_reduced_position[1]}," + " Z "+f"{clean_reduced_position[2]}," + " A " + f"{clean_reduced_position[3]}," + " B " + f"{clean_reduced_position[4]}," + " C " + f"{clean_reduced_position[5]}" + "}"
        
    
    return formatted_position


# {POS: X 450.032, Y 180.996, Z 304.55, A 180.0, B 0.0, C -180.0}

#? In need of a refactor -> readability
def calculate_error(current_position, next_position):
    
    # subtract the two positions
    # if the difference is less than 0.1, then return True
    
    # {POS: X 450.032, Y 180.996, Z 304.55, A 180.0, B 0.0, C -180.0}
    #? I am ignoring orientation for now
    cur_pos = [float(i.split(" ")[-1].strip("}")) for i in current_position.split(", ")[:3]]
    next_pos = [float(i.split(" ")[-1].strip("}")) for i in next_position.split(", ")[:3]]
    
    # print(f'cur_pos: {cur_pos}')
    # print(f'next_pos: {next_pos}')
    
    print(f'cur_pos: {cur_pos}')
    print(f'next_pos: {next_pos}')
    
    error = sum(numpy.abs(numpy.subtract(cur_pos, next_pos)))
    error = round(error, 5)
        
    # print(f'error: {error}')
    print(f'error: {error}')
    
    if error <= ACCEPTABLE_ERROR:
        return True
    else:
        return False



def feedback_loop():
    global coordinate_queue
    
    if not coordinate_queue:
        # TODO: Re-enable logging once tested
        print('.')
        return
    
    next_coordinate = coordinate_queue.peek()

    print(f"next_coordinate: {next_coordinate}")
    next_position = next_coordinate[0]
    next_linear_velocity = next_coordinate[1]
    next_torch_action = (next_coordinate[2])

    # TODO: Re-enable logging once tested
    print(f'Sending to robot (count) - (next_position) - (next_linear_velocity) - (torch_action) : ({coordinate_queue.counter()}) - ({next_position}) - ({next_linear_velocity}) - ({next_torch_action})')

    # format next torch action to ROS String
    next_torch_action_str = String()
    next_torch_action_str.data=next_torch_action
        
    node.torch_command_publisher.publish(next_torch_action_str)
    robot.write(KVP_LIN_COMMAND_VARIABLE, next_position)
    robot.write(KVP_LINEAR_VELOCITY_VARIABLE, next_linear_velocity)

    # TODO: Re-enable logging once tested
    print(f'Buffer Size: {len(coordinate_queue)} coordinates')
    
    
    current_position = robot.read(KVP_ROBOT_POSITION_VARIABLE)    
    
    # TODO: Re-enable logging once tested
    print(f'Reading robot current position: {current_position}')
    if not current_position:
        # TODO: Re-enable logging once tested
        print(f'Could not read Robot\'s current position: {current_position}')
        return
    
    if len(current_position.encode('utf-8')) < 100:
        # TODO: Re-enable logging once tested
        print(f'Invalid Robot position (size) - (reading current_position):{len(current_position.encode("utf-8"))} - {current_position}')
        return
    
    # get current position from robot
    current_position = format_actual_robot_position(current_position)

    # TODO: Re-enable logging once tested
    print(f'Reading robot current position: {current_position}')
    
    # Check error between current position and next position
    if calculate_error(current_position, next_position):
        # TODO: Re-enable logging once tested
        print(f'Finished moving to target position: {next_position}')
        print(f'Buffer Size: {len(coordinate_queue)}  coordinates')
        time.sleep(SEND_DELAY)
        # Remove the completed coordinate
        coordinate_queue.dequeue()
    else:
        # TODO: Re-enable logging once tested
        print(f'Not done moving >>> count - current_position: {coordinate_queue.counter()} - {current_position}')
        return
    
    # # while current position is not equal to next position: keep waiting
    # # Wait for KUKA robot to move to the designated position
    # if current_position == next_position:
    #     print(f'Finished moving to target position: {next_position}')
    #     time.sleep(SEND_DELAY)
    #     # Remove the completed coordinate
    #     coordinate_queue.dequeue  
    # else:
    #     current_position = format_actual_robot_position(robot.read(KVP_ROBOT_POSITION_VARIABLE))
    #     print(f'Not done moving >>> current_position: {current_position}')
        


# Callback function; sends data from the subscribed topic to the robot
def linear_position_callback_fn(subscribedData):
    global coordinate_queue
    
    linear_position = subscribedData
    # TODO: Re-enable logging once tested
    print(f'Received linear_position: {linear_position}')
    
    linear_position_value = subscribedData.pose.position
    linear_position_rotation = subscribedData.pose.orientation
    
    position_velocity_info = format_linear_position(linear_position_value, linear_position_rotation)
    
    formated_linear_position = position_velocity_info[0]
    linear_velocity = position_velocity_info[1]
    formatted_torch_action = position_velocity_info[2]

    position_velocity_object = [formated_linear_position, linear_velocity, formatted_torch_action]
    
    
    coordinate_queue.enqueue(position_velocity_object)

    # TODO: Re-enable logging once tested
    print(f'Adding to coordinate_queue (position_velocity_object): {position_velocity_object}')
    print(f'Buffer Size: {len(coordinate_queue)}  coordinates')
    
    
    
    # robot.write(KVP_LIN_COMMAND_VARIABLE, formated_linear_position)
    # print(f'Sending to robot (formated_linear_position): {formated_linear_position}')


# Callback function; sends data from the subscribed topic to the robot
def program_speed_callback_fn(subscribedData):
    
    speed_info = int(subscribedData.data)
    # rospy.loginfo(f'Received speed_info: {speed_info}')

    
    robot.write(KVP_PROGRAM_SPEED_VARIABLE, speed_info)
    # rospy.loginfo(f'Sending to robot (speed_info): {speed_info}')


# Callback function; sends data from the subscribed topic to the robot
# NOTE: Not being triggered since this topic isn't being published to at the moment
# NOTE: This callback is left here for manual overrides.
def linear_velocity_callback_fn(subscribedData):
    
    linear_velocity = float(subscribedData.data)
    print(f"Transcribed linear_velocity: {linear_velocity}")
    # rospy.loginfo(f'Received linear_velocity: {linear_velocity}')

    
    robot.write(KVP_LINEAR_VELOCITY_VARIABLE, linear_velocity)

    # TODO: Re-enable logging once tested
    print(f'Sending to robot (linear_velocity): {linear_velocity}')
    
    
# Callback function; sends data from the subscribed topic to the robot
def linear_acceleration_callback_fn(subscribedData):
    
    linear_acceleration = float(subscribedData.data)
    # rospy.loginfo(f'Received linear_acceleration: {linear_acceleration}')

    
    robot.write(KVP_LINEAR_ACCELERATION_VARIABLE, linear_acceleration)
    
    # TODO: Re-enable logging once tested
    print(f'Sending to robot (linear_acceleration): {linear_acceleration}')
    




class KVPInterfaceNode(Node):
    def __init__(self):
        super().__init__('kvp_interface_node')
        
        # Create Publishers and Subscribers
        # Publisher for Torch Command
        self.torch_command_publisher = self.create_publisher(String, '/torch', 10)

        self.solved_joint_states_subscription = self.create_subscription(
            JointState,
            '/solved_joint_states',
            joint_command_callback_fn,
            10)
        self.linear_position_subscription = self.create_subscription(
            PoseStamped,
            '/linear_position',
            linear_position_callback_fn,
            10)
        self.speed_info_subscription = self.create_subscription(
            String,
            '/speed_info',
            program_speed_callback_fn,
            10)
        self.linear_velocity_subscription = self.create_subscription(
            String,
            '/linear_velocity',
            linear_velocity_callback_fn,
            10)
        self.linear_acceleration_subscription = self.create_subscription(
            String,
            '/linear_acceleration',
            linear_acceleration_callback_fn,
            10)





        # This timer calls feedback_loop at specified rate (0.1 => 10Hz)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, feedback_loop)
        self.get_logger().info("KVP Interface Node has started.")

def main(args=None):
    rclpy.init(args=args)
    global node
    node = KVPInterfaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("kvp_interface_node stopped cleanly")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
